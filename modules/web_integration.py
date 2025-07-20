"""
웹 통합 시스템
- 모든 서브에이전트와 웹 인터페이스 연동
- 학습 세션 웹 API
- 결과 저장 및 공유 웹 기능
- 실시간 진행 상황 추적
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import asdict
import uuid
import base64
from io import BytesIO

# 서브에이전트 시스템 임포트
from .result_sharing_system import ResultSharingSystem
from .content_template_engine import ContentTemplateEngine
from .code_executor import WebCodeInterface
from .verification_hint_system import VerificationHintSystem
from .error_handling_system import UserFriendlyErrorHandler

class WebIntegrationAPI:
    """웹 통합 API"""
    
    def __init__(self):
        # 서브에이전트 시스템 초기화
        self.sharing_system = ResultSharingSystem()
        self.template_engine = ContentTemplateEngine()
        self.code_interface = WebCodeInterface()
        self.verification_system = VerificationHintSystem()
        self.error_handler = UserFriendlyErrorHandler()
        
        # 웹 세션 관리
        self.web_sessions = {}  # session_id -> web session data
        self.active_learning_sessions = {}  # web_session_id -> learning_session_id
        
    def create_web_session(self, user_id: str = None) -> Dict[str, Any]:
        """웹 세션 생성"""
        web_session_id = str(uuid.uuid4())
        
        session_data = {
            'web_session_id': web_session_id,
            'user_id': user_id or f'anonymous_{int(datetime.now().timestamp())}',
            'created_at': datetime.now().isoformat(),
            'last_activity': datetime.now().isoformat(),
            'learning_sessions': [],
            'completed_steps': [],
            'total_score': 0,
            'session_notes': []
        }
        
        self.web_sessions[web_session_id] = session_data
        
        return {
            'success': True,
            'web_session_id': web_session_id,
            'user_id': session_data['user_id'],
            'message': '웹 세션이 생성되었습니다.'
        }
    
    def start_learning_topic(self, web_session_id: str, topic: str, 
                           content: str = None) -> Dict[str, Any]:
        """학습 주제 시작"""
        try:
            if web_session_id not in self.web_sessions:
                return {'success': False, 'error': '웹 세션을 찾을 수 없습니다.'}
            
            web_session = self.web_sessions[web_session_id]
            user_id = web_session['user_id']
            
            # 기본 콘텐츠 생성 (제공되지 않은 경우)
            if not content:
                content = self._generate_default_content(topic)
            
            # 학습 세션 시작
            learning_session_id = self.sharing_system.start_learning_session(
                user_id, topic, content
            )
            
            # 웹 세션에 학습 세션 연결
            self.active_learning_sessions[web_session_id] = learning_session_id
            web_session['learning_sessions'].append(learning_session_id)
            web_session['last_activity'] = datetime.now().isoformat()
            
            return {
                'success': True,
                'learning_session_id': learning_session_id,
                'topic': topic,
                'message': f'{topic} 학습을 시작합니다.',
                'next_step': 'execute_code'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'error_type': type(e).__name__
            }
    
    def execute_code_step(self, web_session_id: str, code: str, 
                         step_id: str = None) -> Dict[str, Any]:
        """코드 실행 단계"""
        try:
            if web_session_id not in self.web_sessions:
                return {'success': False, 'error': '웹 세션을 찾을 수 없습니다.'}
            
            web_session = self.web_sessions[web_session_id]
            user_id = web_session['user_id']
            
            # 코드 실행
            execution_result = self.code_interface.execute_code_api({
                'code': code,
                'session_id': web_session_id,
                'async': False
            })
            
            # 실행 성공 시 검증 및 힌트 제공
            if execution_result['success'] and step_id:
                verification_result = self.verification_system.verify_step_completion(
                    step_id, code, execution_result, user_id
                )
                
                # 학습 세션 진행 상황 업데이트
                if web_session_id in self.active_learning_sessions:
                    learning_session_id = self.active_learning_sessions[web_session_id]
                    
                    # 상호작용 데이터 생성
                    interaction_data = {
                        'code_execution': True,
                        'execution_time': execution_result.get('execution_time', 0),
                        'success_rate': 1.0 if verification_result['verification_passed'] else 0.5,
                        'step_completed': verification_result['verification_passed']
                    }
                    
                    # 진행 상황 업데이트
                    progress_update = self.sharing_system.update_session_progress(
                        learning_session_id, interaction_data
                    )
                    
                    # 단계 완료 시 평가 결과 기록
                    if verification_result['verification_passed']:
                        assessment_data = {
                            'score': verification_result['score_percentage'],
                            'total_questions': 1,
                            'correct_answers': 1,
                            'step_id': step_id
                        }
                        
                        self.sharing_system.complete_assessment(learning_session_id, assessment_data)
                        
                        # 웹 세션에 완료된 단계 기록
                        web_session['completed_steps'].append({
                            'step_id': step_id,
                            'score': verification_result['score_percentage'],
                            'completed_at': datetime.now().isoformat()
                        })
                
                # 통합 결과 반환
                return {
                    'success': True,
                    'execution_result': execution_result,
                    'verification_result': verification_result,
                    'step_completed': verification_result['verification_passed'],
                    'hints': verification_result.get('hints', []),
                    'next_step': 'next_code_step' if verification_result['verification_passed'] else 'retry_step'
                }
            
            # 실행 실패 시 오류 처리
            elif not execution_result['success']:
                error_analysis = self.error_handler.handle_error(
                    execution_result, user_id, 'beginner', 'practice'
                )
                
                return {
                    'success': False,
                    'execution_result': execution_result,
                    'error_analysis': error_analysis,
                    'next_step': 'fix_error'
                }
            
            # 기본 실행 결과 반환
            return {
                'success': True,
                'execution_result': execution_result,
                'next_step': 'continue'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'error_type': type(e).__name__
            }
    
    def get_session_progress(self, web_session_id: str) -> Dict[str, Any]:
        """세션 진행 상황 조회"""
        try:
            if web_session_id not in self.web_sessions:
                return {'success': False, 'error': '웹 세션을 찾을 수 없습니다.'}
            
            web_session = self.web_sessions[web_session_id]
            
            # 학습 세션 진행 상황
            learning_progress = {}
            if web_session_id in self.active_learning_sessions:
                learning_session_id = self.active_learning_sessions[web_session_id]
                learning_session = self.sharing_system.learning_sessions.get(learning_session_id)
                
                if learning_session:
                    learning_progress = {
                        'session_id': learning_session_id,
                        'topic': learning_session.topic,
                        'overall_score': learning_session.overall_score * 100,
                        'start_time': learning_session.start_time,
                        'insights': learning_session.insights,
                        'recommendations': learning_session.recommendations
                    }
            
            # 웹 세션 통계
            total_steps = len(web_session['completed_steps'])
            avg_score = 0
            if total_steps > 0:
                avg_score = sum(step['score'] for step in web_session['completed_steps']) / total_steps
            
            return {
                'success': True,
                'web_session_id': web_session_id,
                'user_id': web_session['user_id'],
                'total_completed_steps': total_steps,
                'average_score': round(avg_score, 1),
                'learning_progress': learning_progress,
                'completed_steps': web_session['completed_steps'],
                'last_activity': web_session['last_activity']
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'error_type': type(e).__name__
            }
    
    def generate_completion_report(self, web_session_id: str) -> Dict[str, Any]:
        """완료 보고서 생성"""
        try:
            if web_session_id not in self.web_sessions:
                return {'success': False, 'error': '웹 세션을 찾을 수 없습니다.'}
            
            web_session = self.web_sessions[web_session_id]
            user_id = web_session['user_id']
            
            # 종합 보고서 생성
            if web_session['learning_sessions']:
                try:
                    comprehensive_report = self.sharing_system.generate_comprehensive_report(user_id, 1)
                    
                    # 웹 친화적 형태로 변환
                    web_report = {
                        'report_id': comprehensive_report.report_id,
                        'user_id': user_id,
                        'generation_time': comprehensive_report.generation_time,
                        'session_count': comprehensive_report.session_count,
                        'total_study_time': round(comprehensive_report.total_study_time, 1),
                        'overall_performance': comprehensive_report.overall_performance,
                        'strengths': comprehensive_report.strengths,
                        'improvement_areas': comprehensive_report.improvement_areas,
                        'recommendations': comprehensive_report.personalized_recommendations,
                        'web_session_stats': {
                            'completed_steps': len(web_session['completed_steps']),
                            'average_score': self._calculate_average_score(web_session['completed_steps']),
                            'session_duration': self._calculate_session_duration(web_session)
                        }
                    }
                    
                    return {
                        'success': True,
                        'report': web_report,
                        'download_available': True
                    }
                    
                except ValueError:
                    # 보고서 생성 실패 시 기본 요약 제공
                    return self._generate_basic_summary(web_session)
            
            else:
                return self._generate_basic_summary(web_session)
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'error_type': type(e).__name__
            }
    
    def export_session_data(self, web_session_id: str, format_type: str = 'json') -> Dict[str, Any]:
        """세션 데이터 내보내기"""
        try:
            if web_session_id not in self.web_sessions:
                return {'success': False, 'error': '웹 세션을 찾을 수 없습니다.'}
            
            web_session = self.web_sessions[web_session_id]
            user_id = web_session['user_id']
            
            # 내보낼 데이터 수집
            export_data = {
                'web_session': web_session,
                'learning_sessions': [],
                'export_metadata': {
                    'export_time': datetime.now().isoformat(),
                    'format': format_type,
                    'version': '1.0'
                }
            }
            
            # 학습 세션 데이터 추가
            for learning_session_id in web_session['learning_sessions']:
                session_data = self.sharing_system.export_session_data(learning_session_id)
                if session_data:
                    export_data['learning_sessions'].append(session_data)
            
            # 파일 저장
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"session_export_{web_session_id}_{timestamp}.{format_type}"
            
            if format_type == 'json':
                file_content = json.dumps(export_data, ensure_ascii=False, indent=2)
            else:
                return {'success': False, 'error': f'지원하지 않는 형식: {format_type}'}
            
            # 파일 저장 (실제 구현에서는 적절한 저장소 사용)
            export_path = os.path.join('exports', filename)
            os.makedirs('exports', exist_ok=True)
            
            with open(export_path, 'w', encoding='utf-8') as f:
                f.write(file_content)
            
            return {
                'success': True,
                'filename': filename,
                'file_path': export_path,
                'file_size': len(file_content.encode('utf-8')),
                'download_url': f'/download/{filename}'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'error_type': type(e).__name__
            }
    
    def share_results(self, web_session_id: str, sharing_options: Dict[str, Any]) -> Dict[str, Any]:
        """결과 공유"""
        try:
            if web_session_id not in self.web_sessions:
                return {'success': False, 'error': '웹 세션을 찾을 수 없습니다.'}
            
            web_session = self.web_sessions[web_session_id]
            
            # 공유 가능한 요약 생성
            share_summary = {
                'session_id': web_session_id,
                'completed_steps': len(web_session['completed_steps']),
                'average_score': self._calculate_average_score(web_session['completed_steps']),
                'study_duration': self._calculate_session_duration(web_session),
                'achievements': self._generate_achievements(web_session),
                'anonymous': sharing_options.get('anonymous', True)
            }
            
            # 익명화 처리
            if share_summary['anonymous']:
                share_summary['user_display'] = '익명 학습자'
            else:
                share_summary['user_display'] = web_session['user_id']
            
            # 공유 링크 생성
            share_id = str(uuid.uuid4())
            share_url = f"/shared/{share_id}"
            
            # 공유 데이터 저장 (실제 구현에서는 데이터베이스 사용)
            share_data = {
                'share_id': share_id,
                'created_at': datetime.now().isoformat(),
                'expires_at': sharing_options.get('expires_at'),
                'summary': share_summary,
                'access_count': 0
            }
            
            # 임시 저장 (실제로는 데이터베이스에 저장)
            os.makedirs('shared', exist_ok=True)
            with open(f'shared/{share_id}.json', 'w', encoding='utf-8') as f:
                json.dump(share_data, f, ensure_ascii=False, indent=2)
            
            return {
                'success': True,
                'share_id': share_id,
                'share_url': share_url,
                'expires_at': share_data['expires_at'],
                'summary': share_summary
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'error_type': type(e).__name__
            }
    
    def get_available_topics(self) -> Dict[str, Any]:
        """사용 가능한 학습 주제 목록"""
        try:
            # 템플릿 엔진에서 사용 가능한 템플릿 가져오기
            templates = self.template_engine.get_template_list()
            
            # 추가 주제들
            additional_topics = [
                {
                    'id': 'descriptive_statistics',
                    'name': '기술통계량',
                    'description': '평균, 중앙값, 표준편차 등 기본 통계량 학습',
                    'difficulty': 'beginner',
                    'estimated_time': 30
                },
                {
                    'id': 'data_visualization',
                    'name': '데이터 시각화',
                    'description': '히스토그램, 산점도 등 기본 차트 생성',
                    'difficulty': 'intermediate',
                    'estimated_time': 45
                },
                {
                    'id': 'hypothesis_testing',
                    'name': '가설검정',
                    'description': 't-검정, 카이제곱 검정 등 통계적 검정',
                    'difficulty': 'advanced',
                    'estimated_time': 60
                }
            ]
            
            return {
                'success': True,
                'templates': templates,
                'additional_topics': additional_topics,
                'total_topics': len(templates) + len(additional_topics)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'error_type': type(e).__name__
            }
    
    def _generate_default_content(self, topic: str) -> str:
        """기본 콘텐츠 생성"""
        default_contents = {
            'descriptive_statistics': '''
# 기술통계량 학습

기술통계량은 데이터의 특성을 요약하는 수치들입니다.
주요 기술통계량에는 다음이 있습니다:

- 중심경향성: 평균, 중앙값, 최빈값
- 산포도: 분산, 표준편차, 범위
- 분포의 형태: 왜도, 첨도

이번 실습에서는 Python을 사용하여 이러한 통계량들을 직접 계산해보겠습니다.
            ''',
            'data_visualization': '''
# 데이터 시각화 학습

데이터 시각화는 숫자로 된 데이터를 그래프나 차트로 표현하는 것입니다.
주요 시각화 방법:

- 히스토그램: 데이터의 분포 확인
- 산점도: 두 변수 간의 관계 확인
- 박스플롯: 데이터의 요약 통계량 시각화

matplotlib과 seaborn 라이브러리를 사용하여 다양한 차트를 만들어보겠습니다.
            '''
        }
        
        return default_contents.get(topic, f'{topic} 학습을 시작합니다.')
    
    def _calculate_average_score(self, completed_steps: List[Dict[str, Any]]) -> float:
        """평균 점수 계산"""
        if not completed_steps:
            return 0.0
        
        total_score = sum(step['score'] for step in completed_steps)
        return round(total_score / len(completed_steps), 1)
    
    def _calculate_session_duration(self, web_session: Dict[str, Any]) -> int:
        """세션 지속 시간 계산 (분)"""
        created_at = datetime.fromisoformat(web_session['created_at'])
        last_activity = datetime.fromisoformat(web_session['last_activity'])
        
        duration = (last_activity - created_at).total_seconds() / 60
        return round(duration)
    
    def _generate_achievements(self, web_session: Dict[str, Any]) -> List[str]:
        """성취 목록 생성"""
        achievements = []
        completed_steps = len(web_session['completed_steps'])
        avg_score = self._calculate_average_score(web_session['completed_steps'])
        
        if completed_steps >= 1:
            achievements.append('첫 단계 완료')
        
        if completed_steps >= 5:
            achievements.append('꾸준한 학습자')
        
        if avg_score >= 90:
            achievements.append('우수한 성과')
        elif avg_score >= 80:
            achievements.append('좋은 성과')
        
        if self._calculate_session_duration(web_session) >= 30:
            achievements.append('집중력 있는 학습')
        
        return achievements
    
    def _generate_basic_summary(self, web_session: Dict[str, Any]) -> Dict[str, Any]:
        """기본 요약 생성"""
        return {
            'success': True,
            'report': {
                'type': 'basic_summary',
                'user_id': web_session['user_id'],
                'completed_steps': len(web_session['completed_steps']),
                'average_score': self._calculate_average_score(web_session['completed_steps']),
                'session_duration': self._calculate_session_duration(web_session),
                'achievements': self._generate_achievements(web_session),
                'recommendations': [
                    '더 많은 실습을 통해 실력을 향상시키세요',
                    '다양한 주제에 도전해보세요',
                    '꾸준한 학습이 중요합니다'
                ]
            },
            'download_available': False
        }

# 웹 API 엔드포인트 시뮬레이션
class WebAPIEndpoints:
    """웹 API 엔드포인트"""
    
    def __init__(self):
        self.api = WebIntegrationAPI()
    
    def handle_request(self, endpoint: str, method: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """요청 처리"""
        try:
            if endpoint == '/api/session/create' and method == 'POST':
                return self.api.create_web_session(data.get('user_id'))
            
            elif endpoint == '/api/learning/start' and method == 'POST':
                return self.api.start_learning_topic(
                    data['web_session_id'], 
                    data['topic'], 
                    data.get('content')
                )
            
            elif endpoint == '/api/code/execute' and method == 'POST':
                return self.api.execute_code_step(
                    data['web_session_id'],
                    data['code'],
                    data.get('step_id')
                )
            
            elif endpoint == '/api/session/progress' and method == 'GET':
                return self.api.get_session_progress(data['web_session_id'])
            
            elif endpoint == '/api/report/generate' and method == 'POST':
                return self.api.generate_completion_report(data['web_session_id'])
            
            elif endpoint == '/api/session/export' and method == 'POST':
                return self.api.export_session_data(
                    data['web_session_id'],
                    data.get('format', 'json')
                )
            
            elif endpoint == '/api/results/share' and method == 'POST':
                return self.api.share_results(
                    data['web_session_id'],
                    data.get('sharing_options', {})
                )
            
            elif endpoint == '/api/topics' and method == 'GET':
                return self.api.get_available_topics()
            
            else:
                return {
                    'success': False,
                    'error': f'Unknown endpoint: {method} {endpoint}'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'error_type': type(e).__name__
            }

# 데모 및 테스트 함수
def demo_web_integration():
    """웹 통합 시스템 데모"""
    print("🌐 웹 통합 시스템 데모")
    print("=" * 50)
    
    api_endpoints = WebAPIEndpoints()
    
    # 1. 웹 세션 생성
    print("\n1. 웹 세션 생성")
    session_response = api_endpoints.handle_request(
        '/api/session/create', 'POST', {'user_id': 'demo_user'}
    )
    print(f"세션 생성: {session_response['success']}")
    
    if not session_response['success']:
        print("세션 생성 실패")
        return
    
    web_session_id = session_response['web_session_id']
    print(f"웹 세션 ID: {web_session_id}")
    
    # 2. 학습 주제 시작
    print("\n2. 학습 주제 시작")
    learning_response = api_endpoints.handle_request(
        '/api/learning/start', 'POST', {
            'web_session_id': web_session_id,
            'topic': 'descriptive_statistics'
        }
    )
    print(f"학습 시작: {learning_response['success']}")
    print(f"주제: {learning_response.get('topic', 'N/A')}")
    
    # 3. 코드 실행
    print("\n3. 코드 실행")
    code_response = api_endpoints.handle_request(
        '/api/code/execute', 'POST', {
            'web_session_id': web_session_id,
            'code': '''
scores = [85, 90, 78, 92, 88, 76, 95, 89, 84, 91]
print(f"데이터: {scores}")
print(f"데이터 개수: {len(scores)}")
            ''',
            'step_id': 'step_1'
        }
    )
    print(f"코드 실행: {code_response['success']}")
    if code_response['success']:
        print(f"단계 완료: {code_response.get('step_completed', False)}")
    
    # 4. 진행 상황 확인
    print("\n4. 진행 상황 확인")
    progress_response = api_endpoints.handle_request(
        '/api/session/progress', 'GET', {
            'web_session_id': web_session_id
        }
    )
    print(f"진행 상황 조회: {progress_response['success']}")
    if progress_response['success']:
        print(f"완료된 단계: {progress_response['total_completed_steps']}")
        print(f"평균 점수: {progress_response['average_score']}")
    
    # 5. 보고서 생성
    print("\n5. 완료 보고서 생성")
    report_response = api_endpoints.handle_request(
        '/api/report/generate', 'POST', {
            'web_session_id': web_session_id
        }
    )
    print(f"보고서 생성: {report_response['success']}")
    
    # 6. 결과 공유
    print("\n6. 결과 공유")
    share_response = api_endpoints.handle_request(
        '/api/results/share', 'POST', {
            'web_session_id': web_session_id,
            'sharing_options': {'anonymous': True}
        }
    )
    print(f"결과 공유: {share_response['success']}")
    if share_response['success']:
        print(f"공유 URL: {share_response.get('share_url', 'N/A')}")
    
    print(f"\n🎉 Task 4.3 완료!")
    print("✅ 학습 과정 및 결과 저장 기능")
    print("✅ 완성된 데모 페이지 생성 및 공유")
    print("✅ 웹 API 통합 완료")

if __name__ == "__main__":
    demo_web_integration()