"""
Task 4.2: 기능 통합 및 연동 시스템
모든 핵심 기능을 통합한 백엔드 시스템
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from descriptive_statistics_practice import DescriptiveStatisticsPractice
from content_standardization import ContentStandardizer
from simple_demo import SimplePythonExecutor
from result_interpretation_system import ResultInterpreter
from verification_hint_system import VerificationHintSystem
from typing import Dict, Any, List, Optional
import json
import datetime
import uuid


class IntegratedPracticeSystem:
    """통합 실습 시스템"""
    
    def __init__(self):
        # 각 모듈 초기화
        self.practice_system = DescriptiveStatisticsPractice()
        self.content_standardizer = ContentStandardizer()
        self.code_executor = SimplePythonExecutor()
        self.result_interpreter = ResultInterpreter()
        self.verification_system = VerificationHintSystem()
        
        # 시스템 상태
        self.active_sessions = {}  # session_id -> session_data
        self.system_stats = {
            'total_sessions': 0,
            'completed_sessions': 0,
            'total_code_executions': 0,
            'average_completion_time': 0,
            'start_time': datetime.datetime.now()
        }
    
    def create_learning_session(self, user_id: str = None, session_title: str = "기술통계량 실습") -> Dict[str, Any]:
        """새로운 학습 세션 생성"""
        session_id = str(uuid.uuid4())
        
        # 실습 세션 생성
        practice_session = self.practice_system.create_session(session_id, session_title)
        practice_session.start_session()
        
        # 통합 세션 데이터 생성
        session_data = {
            'session_id': session_id,
            'user_id': user_id,
            'title': session_title,
            'created_at': datetime.datetime.now().isoformat(),
            'status': 'active',
            'practice_session': practice_session,
            'content_history': [],
            'execution_history': [],
            'interpretation_history': [],
            'current_step': 1,
            'total_steps': 5,
            'completed_steps': [],
            'session_notes': [],
            'performance_metrics': {
                'start_time': datetime.datetime.now(),
                'step_times': {},
                'total_attempts': 0,
                'successful_executions': 0,
                'hints_used': 0
            }
        }
        
        self.active_sessions[session_id] = session_data
        self.system_stats['total_sessions'] += 1
        
        return {
            'success': True,
            'session_id': session_id,
            'session_data': self._serialize_session_data(session_data),
            'message': '새로운 학습 세션이 생성되었습니다.'
        }
    
    def get_session_info(self, session_id: str) -> Dict[str, Any]:
        """세션 정보 조회"""
        if session_id not in self.active_sessions:
            return {
                'success': False,
                'error': '세션을 찾을 수 없습니다.',
                'session_id': session_id
            }
        
        session_data = self.active_sessions[session_id]
        current_step = session_data['practice_session'].get_current_step()
        
        return {
            'success': True,
            'session_id': session_id,
            'session_info': self._serialize_session_data(session_data),
            'current_step': {
                'step_number': session_data['current_step'],
                'step_data': current_step.to_dict() if current_step else None
            },
            'progress': session_data['practice_session'].get_progress()
        }
    
    def execute_code_with_integration(self, session_id: str, code: str, 
                                    apply_content_standards: bool = True) -> Dict[str, Any]:
        """통합된 코드 실행 (콘텐츠 표준화 + 실행 + 해석)"""
        if session_id not in self.active_sessions:
            return {
                'success': False,
                'error': '세션을 찾을 수 없습니다.'
            }
        
        session_data = self.active_sessions[session_id]
        
        try:
            # 1. 콘텐츠 표준화 적용 (선택적)
            processed_code = code
            if apply_content_standards:
                try:
                    # 코드를 콘텐츠 데이터 형태로 변환
                    content_data = {
                        'sections': {
                            'code': {
                                'content': code,
                                'type': 'code'
                            }
                        }
                    }
                    standardized_data = self.content_standardizer.standardize_content(content_data)
                    if 'sections' in standardized_data and 'code' in standardized_data['sections']:
                        processed_code = standardized_data['sections']['code'].get('content', code)
                except Exception:
                    # 표준화 실패 시 원본 코드 사용
                    processed_code = code
            
            # 2. 코드 실행
            execution_result = self.code_executor.execute(processed_code)
            
            # 3. 결과 해석
            interpretation_result = None
            if execution_result.get('success'):
                interpretation_result = self.result_interpreter.interpret_result(
                    execution_result, 'education'
                )
            
            # 4. 실습 시스템과 연동
            practice_result = self.practice_system.execute_step_code(session_id, processed_code)
            
            # 5. 세션 데이터 업데이트
            execution_record = {
                'timestamp': datetime.datetime.now().isoformat(),
                'original_code': code,
                'processed_code': processed_code,
                'execution_result': execution_result,
                'interpretation_result': interpretation_result,
                'practice_result': practice_result,
                'step_number': session_data['current_step']
            }
            
            session_data['execution_history'].append(execution_record)
            session_data['performance_metrics']['total_attempts'] += 1
            
            if execution_result.get('success'):
                session_data['performance_metrics']['successful_executions'] += 1
            
            # 6. 단계 완료 처리
            if practice_result.get('step_completed'):
                session_data['completed_steps'].append(session_data['current_step'])
                session_data['current_step'] = min(session_data['current_step'] + 1, 
                                                 session_data['total_steps'])
                
                # 단계 완료 시간 기록
                step_key = f"step_{len(session_data['completed_steps'])}"
                session_data['performance_metrics']['step_times'][step_key] = datetime.datetime.now()
            
            # 7. 시스템 통계 업데이트
            self.system_stats['total_code_executions'] += 1
            
            return {
                'success': True,
                'session_id': session_id,
                'execution': execution_result,
                'interpretation': interpretation_result,
                'practice': practice_result,
                'step_completed': practice_result.get('step_completed', False),
                'session_progress': session_data['practice_session'].get_progress(),
                'performance_metrics': session_data['performance_metrics']
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'통합 실행 중 오류 발생: {str(e)}',
                'session_id': session_id
            }
    
    def get_integrated_hint(self, session_id: str, hint_type: str = 'basic') -> Dict[str, Any]:
        """통합된 힌트 시스템"""
        if session_id not in self.active_sessions:
            return {
                'success': False,
                'error': '세션을 찾을 수 없습니다.'
            }
        
        session_data = self.active_sessions[session_id]
        
        # 실습 시스템에서 힌트 가져오기
        practice_hint = self.practice_system.get_step_hint(session_id, hint_type)
        
        # 검증 시스템에서 추가 힌트 가져오기
        current_step = session_data['practice_session'].get_current_step()
        verification_hint = None
        
        if current_step and session_data['execution_history']:
            last_execution = session_data['execution_history'][-1]
            if not last_execution['execution_result'].get('success'):
                verification_hint = self.verification_system.get_contextual_hint(
                    last_execution['original_code'],
                    last_execution['execution_result'].get('error', '')
                )
        
        # 힌트 사용 통계 업데이트
        session_data['performance_metrics']['hints_used'] += 1
        
        return {
            'success': True,
            'session_id': session_id,
            'practice_hint': practice_hint,
            'verification_hint': verification_hint,
            'hint_type': hint_type,
            'step_number': session_data['current_step']
        }
    
    def generate_content_with_standards(self, content_type: str, topic: str, 
                                      difficulty_level: str = 'beginner') -> Dict[str, Any]:
        """표준화된 콘텐츠 생성"""
        try:
            # 콘텐츠 표준화 시스템을 사용하여 콘텐츠 생성
            content_result = self.content_standardizer.create_standardized_content(
                content_type, topic, difficulty_level
            )
            
            if content_result.get('success'):
                # 품질 검증
                quality_result = self.content_standardizer.validate_content_quality(
                    content_result.get('content', '')
                )
                
                return {
                    'success': True,
                    'content': content_result.get('content'),
                    'metadata': content_result.get('metadata'),
                    'quality_score': quality_result.get('quality_score', 0),
                    'quality_feedback': quality_result.get('feedback', [])
                }
            else:
                return content_result
                
        except Exception as e:
            return {
                'success': False,
                'error': f'콘텐츠 생성 중 오류 발생: {str(e)}'
            }
    
    def complete_session(self, session_id: str) -> Dict[str, Any]:
        """세션 완료 처리"""
        if session_id not in self.active_sessions:
            return {
                'success': False,
                'error': '세션을 찾을 수 없습니다.'
            }
        
        session_data = self.active_sessions[session_id]
        
        # 세션 완료 처리
        session_data['status'] = 'completed'
        session_data['completed_at'] = datetime.datetime.now().isoformat()
        
        # 성과 지표 계산
        performance = session_data['performance_metrics']
        total_time = (datetime.datetime.now() - performance['start_time']).total_seconds() / 60
        success_rate = (performance['successful_executions'] / max(performance['total_attempts'], 1)) * 100
        
        # 세션 요약 생성
        session_summary = {
            'session_id': session_id,
            'title': session_data['title'],
            'completed_steps': len(session_data['completed_steps']),
            'total_steps': session_data['total_steps'],
            'completion_rate': (len(session_data['completed_steps']) / session_data['total_steps']) * 100,
            'total_time_minutes': round(total_time, 1),
            'total_attempts': performance['total_attempts'],
            'successful_executions': performance['successful_executions'],
            'success_rate': round(success_rate, 1),
            'hints_used': performance['hints_used'],
            'execution_history_count': len(session_data['execution_history'])
        }
        
        # 시스템 통계 업데이트
        if len(session_data['completed_steps']) == session_data['total_steps']:
            self.system_stats['completed_sessions'] += 1
        
        return {
            'success': True,
            'session_id': session_id,
            'session_summary': session_summary,
            'message': '세션이 성공적으로 완료되었습니다.'
        }
    
    def get_system_dashboard(self) -> Dict[str, Any]:
        """시스템 대시보드 데이터"""
        current_time = datetime.datetime.now()
        uptime = (current_time - self.system_stats['start_time']).total_seconds() / 3600  # 시간 단위
        
        # 활성 세션 통계
        active_sessions_count = len([s for s in self.active_sessions.values() if s['status'] == 'active'])
        completed_sessions_count = len([s for s in self.active_sessions.values() if s['status'] == 'completed'])
        
        # 평균 완료 시간 계산
        completed_sessions = [s for s in self.active_sessions.values() if s['status'] == 'completed']
        if completed_sessions:
            total_completion_time = sum(
                (datetime.datetime.fromisoformat(s['completed_at']) - 
                 s['performance_metrics']['start_time']).total_seconds() / 60
                for s in completed_sessions
            )
            avg_completion_time = total_completion_time / len(completed_sessions)
        else:
            avg_completion_time = 0
        
        return {
            'system_info': {
                'uptime_hours': round(uptime, 1),
                'start_time': self.system_stats['start_time'].isoformat(),
                'current_time': current_time.isoformat()
            },
            'session_statistics': {
                'total_sessions': self.system_stats['total_sessions'],
                'active_sessions': active_sessions_count,
                'completed_sessions': completed_sessions_count,
                'completion_rate': round((completed_sessions_count / max(self.system_stats['total_sessions'], 1)) * 100, 1),
                'average_completion_time_minutes': round(avg_completion_time, 1)
            },
            'execution_statistics': {
                'total_code_executions': self.system_stats['total_code_executions'],
                'executions_per_session': round(self.system_stats['total_code_executions'] / max(self.system_stats['total_sessions'], 1), 1)
            },
            'active_sessions_summary': [
                {
                    'session_id': s['session_id'],
                    'title': s['title'],
                    'current_step': s['current_step'],
                    'progress': round((len(s['completed_steps']) / s['total_steps']) * 100, 1),
                    'created_at': s['created_at']
                }
                for s in self.active_sessions.values() if s['status'] == 'active'
            ]
        }
    
    def export_session_data(self, session_id: str, format_type: str = 'json') -> Dict[str, Any]:
        """세션 데이터 내보내기"""
        if session_id not in self.active_sessions:
            return {
                'success': False,
                'error': '세션을 찾을 수 없습니다.'
            }
        
        session_data = self.active_sessions[session_id]
        
        try:
            if format_type == 'json':
                exported_data = self._serialize_session_data(session_data)
                return {
                    'success': True,
                    'format': 'json',
                    'data': exported_data,
                    'session_id': session_id
                }
            elif format_type == 'summary':
                # 요약 형태로 내보내기
                summary_data = {
                    'session_info': {
                        'id': session_data['session_id'],
                        'title': session_data['title'],
                        'status': session_data['status'],
                        'created_at': session_data['created_at']
                    },
                    'progress': {
                        'completed_steps': len(session_data['completed_steps']),
                        'total_steps': session_data['total_steps'],
                        'current_step': session_data['current_step']
                    },
                    'performance': session_data['performance_metrics'],
                    'execution_summary': {
                        'total_executions': len(session_data['execution_history']),
                        'successful_executions': sum(1 for e in session_data['execution_history'] 
                                                   if e['execution_result'].get('success')),
                        'steps_with_executions': list(set(e['step_number'] for e in session_data['execution_history']))
                    }
                }
                return {
                    'success': True,
                    'format': 'summary',
                    'data': summary_data,
                    'session_id': session_id
                }
            else:
                return {
                    'success': False,
                    'error': f'지원하지 않는 형식: {format_type}'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'데이터 내보내기 중 오류 발생: {str(e)}'
            }
    
    def _serialize_session_data(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """세션 데이터 직렬화 (JSON 호환)"""
        serialized = session_data.copy()
        
        # datetime 객체들을 문자열로 변환
        if 'performance_metrics' in serialized:
            metrics = serialized['performance_metrics']
            if 'start_time' in metrics and hasattr(metrics['start_time'], 'isoformat'):
                metrics['start_time'] = metrics['start_time'].isoformat()
            
            if 'step_times' in metrics:
                step_times = {}
                for key, value in metrics['step_times'].items():
                    if hasattr(value, 'isoformat'):
                        step_times[key] = value.isoformat()
                    else:
                        step_times[key] = value
                metrics['step_times'] = step_times
        
        # PracticeSession 객체를 딕셔너리로 변환
        if 'practice_session' in serialized:
            serialized['practice_session'] = serialized['practice_session'].to_dict()
        
        return serialized


def demo_integrated_system():
    """통합 시스템 데모"""
    print("=== 통합 실습 시스템 데모 ===\n")
    
    # 시스템 초기화
    integrated_system = IntegratedPracticeSystem()
    
    # 1. 새 세션 생성
    print("1. 새 학습 세션 생성")
    session_result = integrated_system.create_learning_session(
        user_id="demo_user",
        session_title="통합 기술통계량 실습"
    )
    
    if session_result['success']:
        session_id = session_result['session_id']
        print(f"✅ 세션 생성 성공: {session_id}")
        print(f"세션 제목: {session_result['session_data']['title']}")
    else:
        print("❌ 세션 생성 실패")
        return
    
    print()
    
    # 2. 첫 번째 단계 코드 실행
    print("2. 첫 번째 단계 코드 실행 (통합)")
    code1 = """# 학생 성적 데이터 준비
scores = [85, 90, 78, 92, 88, 76, 95, 89, 84, 91]

# 데이터 기본 정보 확인
print(f"데이터: {scores}")
print(f"데이터 개수: {len(scores)}")
print("데이터 타입: list")"""
    
    execution_result = integrated_system.execute_code_with_integration(
        session_id, code1, apply_content_standards=True
    )
    
    if execution_result['success']:
        print("✅ 코드 실행 성공")
        print(f"실행 결과: {execution_result['execution']['output'][:100]}...")
        print(f"단계 완료: {execution_result['step_completed']}")
        print(f"진행률: {execution_result['session_progress']['progress_percentage']}%")
        
        if execution_result['interpretation']:
            print(f"결과 해석: {execution_result['interpretation'].get('summary', 'N/A')}")
    else:
        print(f"❌ 코드 실행 실패: {execution_result.get('error')}")
    
    print()
    
    # 3. 힌트 시스템 테스트
    print("3. 통합 힌트 시스템 테스트")
    hint_result = integrated_system.get_integrated_hint(session_id, 'basic')
    
    if hint_result['success']:
        print("✅ 힌트 조회 성공")
        print(f"실습 힌트: {hint_result['practice_hint'].get('hint', 'N/A')}")
        if hint_result['verification_hint']:
            print(f"검증 힌트: {hint_result['verification_hint'].get('suggestion', 'N/A')}")
    else:
        print(f"❌ 힌트 조회 실패: {hint_result.get('error')}")
    
    print()
    
    # 4. 세션 정보 조회
    print("4. 세션 정보 조회")
    session_info = integrated_system.get_session_info(session_id)
    
    if session_info['success']:
        print("✅ 세션 정보 조회 성공")
        print(f"현재 단계: {session_info['current_step']['step_number']}")
        print(f"진행률: {session_info['progress']['progress_percentage']}%")
        print(f"완료된 단계: {session_info['progress']['completed_steps']}")
    else:
        print(f"❌ 세션 정보 조회 실패: {session_info.get('error')}")
    
    print()
    
    # 5. 시스템 대시보드
    print("5. 시스템 대시보드")
    dashboard = integrated_system.get_system_dashboard()
    
    print(f"총 세션 수: {dashboard['session_statistics']['total_sessions']}")
    print(f"활성 세션 수: {dashboard['session_statistics']['active_sessions']}")
    print(f"총 코드 실행 수: {dashboard['execution_statistics']['total_code_executions']}")
    print(f"시스템 가동 시간: {dashboard['system_info']['uptime_hours']:.1f}시간")
    
    print()
    
    # 6. 세션 데이터 내보내기
    print("6. 세션 데이터 내보내기")
    export_result = integrated_system.export_session_data(session_id, 'summary')
    
    if export_result['success']:
        print("✅ 데이터 내보내기 성공")
        summary = export_result['data']
        print(f"세션 ID: {summary['session_info']['id']}")
        print(f"진행률: {summary['progress']['completed_steps']}/{summary['progress']['total_steps']}")
        print(f"총 실행 횟수: {summary['execution_summary']['total_executions']}")
    else:
        print(f"❌ 데이터 내보내기 실패: {export_result.get('error')}")
    
    print("\n=== 통합 시스템 데모 완료 ===")
    return integrated_system


if __name__ == "__main__":
    demo_integrated_system()