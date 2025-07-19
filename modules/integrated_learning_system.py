"""
Task 4.2: 통합 학습 시스템 - 기능 통합 및 연동
모든 핵심 기능을 통합한 완전한 교육 시스템
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from typing import Dict, Any, List, Optional, Tuple
import json
import datetime
from dataclasses import dataclass, asdict

# 기존 모듈들 import
from simple_demo import SimplePythonExecutor
from descriptive_statistics_practice import DescriptiveStatisticsPractice, PracticeSession, PracticeStep
from content_standardization import ContentStandardizer
from result_interpretation_system import ResultInterpreter
from verification_hint_system import VerificationHintSystem


@dataclass
class LearningSession:
    """통합 학습 세션"""
    session_id: str
    user_id: str
    title: str
    created_at: str
    updated_at: str
    status: str  # 'active', 'completed', 'paused'
    progress: Dict[str, Any]
    content_data: Dict[str, Any]
    practice_data: Dict[str, Any]
    results: List[Dict[str, Any]]
    notes: List[str]


class IntegratedLearningSystem:
    """통합 학습 시스템"""
    
    def __init__(self):
        # 핵심 컴포넌트 초기화
        self.code_executor = SimplePythonExecutor()
        self.practice_system = DescriptiveStatisticsPractice()
        self.content_standardizer = ContentStandardizer()
        self.result_interpreter = ResultInterpreter()
        self.verification_system = VerificationHintSystem()
        
        # 세션 관리
        self.sessions = {}  # session_id -> LearningSession
        self.active_sessions = {}  # user_id -> session_id
        
        # 시스템 상태
        self.system_stats = {
            'total_sessions': 0,
            'completed_sessions': 0,
            'total_code_executions': 0,
            'average_completion_time': 0.0
        }
    
    def create_learning_session(self, user_id: str, title: str = "기술통계량 학습") -> str:
        """새로운 학습 세션 생성"""
        session_id = f"session_{user_id}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # 실습 세션 생성
        practice_session = self.practice_system.create_session(session_id, title)
        practice_session.start_session()
        
        # 통합 세션 생성
        learning_session = LearningSession(
            session_id=session_id,
            user_id=user_id,
            title=title,
            created_at=datetime.datetime.now().isoformat(),
            updated_at=datetime.datetime.now().isoformat(),
            status='active',
            progress={
                'current_step': 0,
                'total_steps': len(practice_session.step_order),
                'completion_percentage': 0.0,
                'steps_completed': []
            },
            content_data={
                'standardized_content': {},
                'learning_materials': []
            },
            practice_data={
                'session_id': session_id,
                'attempts': 0,
                'successful_executions': 0,
                'hints_used': 0
            },
            results=[],
            notes=[]
        )
        
        self.sessions[session_id] = learning_session
        self.active_sessions[user_id] = session_id
        self.system_stats['total_sessions'] += 1
        
        return session_id
    
    def get_session(self, session_id: str) -> Optional[LearningSession]:
        """세션 가져오기"""
        return self.sessions.get(session_id)
    
    def execute_learning_step(self, session_id: str, code: str, 
                            include_interpretation: bool = True) -> Dict[str, Any]:
        """학습 단계 실행 (통합 기능)"""
        session = self.get_session(session_id)
        if not session:
            return {"error": "세션을 찾을 수 없습니다."}
        
        # 1. 코드 실행
        execution_result = self.code_executor.execute(code)
        self.system_stats['total_code_executions'] += 1
        
        # 2. 실습 시스템을 통한 검증
        practice_result = self.practice_system.execute_step_code(session_id, code)
        
        # 3. 결과 해석 (성공한 경우에만)
        interpretation = None
        if execution_result.get('success') and include_interpretation:
            interpretation = self._interpret_execution_result(execution_result)
        
        # 4. 콘텐츠 표준화 (결과 정리)
        standardized_result = self._standardize_result(
            execution_result, practice_result, interpretation
        )
        
        # 5. 세션 업데이트
        self._update_session_progress(session, standardized_result)
        
        # 6. 통합 결과 반환
        integrated_result = {
            'session_id': session_id,
            'execution': execution_result,
            'practice': practice_result,
            'interpretation': interpretation,
            'standardized': standardized_result,
            'session_progress': session.progress,
            'timestamp': datetime.datetime.now().isoformat()
        }
        
        # 결과 저장
        session.results.append(integrated_result)
        session.updated_at = datetime.datetime.now().isoformat()
        
        return integrated_result
    
    def _interpret_execution_result(self, execution_result: Dict[str, Any]) -> Dict[str, Any]:
        """실행 결과 해석"""
        if not execution_result.get('success'):
            return {
                'type': 'error',
                'message': '코드 실행 중 오류가 발생했습니다.',
                'suggestion': '오류 메시지를 확인하고 코드를 수정해보세요.'
            }
        
        variables = execution_result.get('variables', {})
        output = execution_result.get('output', '')
        
        # 통계 관련 변수 해석
        statistical_interpretation = self._interpret_statistical_variables(variables)
        
        # 출력 결과 해석
        output_interpretation = self._interpret_output(output)
        
        return {
            'type': 'success',
            'statistical_analysis': statistical_interpretation,
            'output_analysis': output_interpretation,
            'learning_insights': self._generate_learning_insights(variables, output),
            'next_steps': self._suggest_next_steps(variables)
        }
    
    def _interpret_statistical_variables(self, variables: Dict[str, Any]) -> Dict[str, Any]:
        """통계 변수 해석"""
        interpretation = {}
        
        if 'mean_value' in variables:
            mean_val = variables['mean_value']
            interpretation['mean'] = {
                'value': mean_val,
                'interpretation': f"평균값 {mean_val:.2f}는 데이터의 중심 경향을 나타냅니다.",
                'context': "평균은 모든 값을 더한 후 개수로 나눈 값으로, 데이터의 대표값입니다."
            }
        
        if 'median_value' in variables:
            median_val = variables['median_value']
            interpretation['median'] = {
                'value': median_val,
                'interpretation': f"중앙값 {median_val}는 데이터를 정렬했을 때 가운데 위치한 값입니다.",
                'context': "중앙값은 극값의 영향을 받지 않는 안정적인 중심 경향 측도입니다."
            }
        
        if 'std_dev' in variables:
            std_val = variables['std_dev']
            interpretation['standard_deviation'] = {
                'value': std_val,
                'interpretation': f"표준편차 {std_val:.2f}는 데이터의 퍼짐 정도를 나타냅니다.",
                'context': "표준편차가 작을수록 데이터가 평균 주변에 집중되어 있습니다."
            }
        
        if 'variance' in variables:
            var_val = variables['variance']
            interpretation['variance'] = {
                'value': var_val,
                'interpretation': f"분산 {var_val:.2f}는 데이터의 변동성을 측정합니다.",
                'context': "분산은 표준편차의 제곱으로, 데이터의 산포를 나타냅니다."
            }
        
        return interpretation
    
    def _interpret_output(self, output: str) -> Dict[str, Any]:
        """출력 결과 해석"""
        lines = output.strip().split('\n')
        
        return {
            'line_count': len(lines),
            'contains_statistics': any('평균' in line or '중앙값' in line or '표준편차' in line 
                                    for line in lines),
            'contains_data': any('데이터' in line for line in lines),
            'summary': f"{len(lines)}줄의 출력이 생성되었습니다."
        }
    
    def _generate_learning_insights(self, variables: Dict[str, Any], output: str) -> List[str]:
        """학습 인사이트 생성"""
        insights = []
        
        if 'mean_value' in variables and 'median_value' in variables:
            mean_val = variables['mean_value']
            median_val = variables['median_value']
            
            if abs(mean_val - median_val) < 1:
                insights.append("평균과 중앙값이 비슷하여 데이터가 대칭적으로 분포되어 있습니다.")
            elif mean_val > median_val:
                insights.append("평균이 중앙값보다 커서 오른쪽으로 치우친 분포를 보입니다.")
            else:
                insights.append("평균이 중앙값보다 작아서 왼쪽으로 치우친 분포를 보입니다.")
        
        if 'std_dev' in variables:
            std_val = variables['std_dev']
            if std_val < 5:
                insights.append("표준편차가 작아 데이터가 평균 주변에 집중되어 있습니다.")
            elif std_val > 10:
                insights.append("표준편차가 커서 데이터의 변동성이 큽니다.")
            else:
                insights.append("표준편차가 적당하여 데이터가 적절히 분산되어 있습니다.")
        
        return insights
    
    def _suggest_next_steps(self, variables: Dict[str, Any]) -> List[str]:
        """다음 단계 제안"""
        suggestions = []
        
        if 'scores' in variables and 'mean_value' not in variables:
            suggestions.append("다음으로 평균값을 계산해보세요.")
        elif 'mean_value' in variables and 'median_value' not in variables:
            suggestions.append("중앙값을 계산하여 평균과 비교해보세요.")
        elif 'median_value' in variables and 'std_dev' not in variables:
            suggestions.append("표준편차를 계산하여 데이터의 퍼짐 정도를 확인해보세요.")
        elif 'std_dev' in variables:
            suggestions.append("결과를 해석하고 데이터의 특성을 분석해보세요.")
        
        return suggestions
    
    def _standardize_result(self, execution_result: Dict[str, Any], 
                          practice_result: Dict[str, Any], 
                          interpretation: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """결과 표준화"""
        return {
            'success': execution_result.get('success', False) and practice_result.get('verification', {}).get('success', False),
            'execution_time': execution_result.get('execution_time', 0),
            'output_summary': execution_result.get('output', '')[:200] + '...' if len(execution_result.get('output', '')) > 200 else execution_result.get('output', ''),
            'variables_created': list(execution_result.get('variables', {}).keys()),
            'step_completed': practice_result.get('step_completed', False),
            'verification_message': practice_result.get('verification', {}).get('message', ''),
            'has_interpretation': interpretation is not None,
            'learning_level': self._assess_learning_level(execution_result, practice_result)
        }
    
    def _assess_learning_level(self, execution_result: Dict[str, Any], 
                             practice_result: Dict[str, Any]) -> str:
        """학습 수준 평가"""
        if not execution_result.get('success'):
            return 'beginner'
        elif not practice_result.get('step_completed'):
            return 'intermediate'
        else:
            return 'advanced'
    
    def _update_session_progress(self, session: LearningSession, result: Dict[str, Any]):
        """세션 진행 상황 업데이트"""
        session.practice_data['attempts'] += 1
        
        if result['success']:
            session.practice_data['successful_executions'] += 1
            
            if result['step_completed']:
                current_step = session.progress['current_step']
                if current_step not in session.progress['steps_completed']:
                    session.progress['steps_completed'].append(current_step)
                    session.progress['current_step'] += 1
                
                # 진행률 계산
                completed_steps = len(session.progress['steps_completed'])
                total_steps = session.progress['total_steps']
                session.progress['completion_percentage'] = (completed_steps / total_steps) * 100
                
                # 완료 확인
                if completed_steps >= total_steps:
                    session.status = 'completed'
                    self.system_stats['completed_sessions'] += 1
    
    def get_learning_hint(self, session_id: str, hint_level: str = 'basic') -> Dict[str, Any]:
        """학습 힌트 제공"""
        session = self.get_session(session_id)
        if not session:
            return {"error": "세션을 찾을 수 없습니다."}
        
        # 실습 시스템에서 힌트 가져오기
        practice_hint = self.practice_system.get_step_hint(session_id, hint_level)
        
        # 추가 학습 가이드
        additional_guidance = self._generate_additional_guidance(session)
        
        session.practice_data['hints_used'] += 1
        
        return {
            'practice_hint': practice_hint,
            'additional_guidance': additional_guidance,
            'learning_resources': self._get_learning_resources(session),
            'timestamp': datetime.datetime.now().isoformat()
        }
    
    def _generate_additional_guidance(self, session: LearningSession) -> Dict[str, Any]:
        """추가 학습 가이드 생성"""
        current_step = session.progress['current_step']
        
        guidance = {
            0: {
                'concept': '데이터 준비',
                'tips': ['리스트를 사용하여 데이터를 저장하세요', 'len() 함수로 데이터 개수를 확인하세요'],
                'common_errors': ['변수명 오타', '대괄호 누락']
            },
            1: {
                'concept': '중심경향성',
                'tips': ['sum() 함수로 총합을 구하세요', '정렬을 통해 중앙값을 찾으세요'],
                'common_errors': ['나눗셈 연산자 실수', '정렬 로직 오류']
            },
            2: {
                'concept': '산포도',
                'tips': ['편차의 제곱을 계산하세요', '제곱근을 구하려면 ** 0.5를 사용하세요'],
                'common_errors': ['변수 스코프 문제', '수식 계산 오류']
            }
        }
        
        return guidance.get(current_step, {
            'concept': '고급 분석',
            'tips': ['결과를 해석하고 의미를 찾아보세요'],
            'common_errors': ['논리적 해석 오류']
        })
    
    def _get_learning_resources(self, session: LearningSession) -> List[Dict[str, str]]:
        """학습 자료 제공"""
        return [
            {
                'title': '기술통계량 기초',
                'type': 'concept',
                'description': '평균, 중앙값, 표준편차의 개념과 계산 방법'
            },
            {
                'title': 'Python 기초 문법',
                'type': 'syntax',
                'description': '리스트, 반복문, 함수 사용법'
            },
            {
                'title': '데이터 해석 가이드',
                'type': 'interpretation',
                'description': '통계량의 의미와 실무적 해석 방법'
            }
        ]
    
    def get_session_summary(self, session_id: str) -> Dict[str, Any]:
        """세션 요약 정보"""
        session = self.get_session(session_id)
        if not session:
            return {"error": "세션을 찾을 수 없습니다."}
        
        # 실습 시스템 요약
        practice_summary = self.practice_system.get_session_summary(session_id)
        
        # 통합 요약
        return {
            'session_info': asdict(session),
            'practice_summary': practice_summary,
            'performance_metrics': self._calculate_performance_metrics(session),
            'learning_achievements': self._assess_learning_achievements(session),
            'recommendations': self._generate_recommendations(session)
        }
    
    def _calculate_performance_metrics(self, session: LearningSession) -> Dict[str, Any]:
        """성과 지표 계산"""
        attempts = session.practice_data['attempts']
        successful = session.practice_data['successful_executions']
        
        return {
            'success_rate': (successful / attempts * 100) if attempts > 0 else 0,
            'total_attempts': attempts,
            'successful_executions': successful,
            'hints_used': session.practice_data['hints_used'],
            'completion_percentage': session.progress['completion_percentage'],
            'efficiency_score': (successful / (attempts + session.practice_data['hints_used'])) * 100 if (attempts + session.practice_data['hints_used']) > 0 else 0
        }
    
    def _assess_learning_achievements(self, session: LearningSession) -> List[str]:
        """학습 성취 평가"""
        achievements = []
        
        if session.progress['completion_percentage'] >= 100:
            achievements.append("🎉 모든 실습 단계를 완료했습니다!")
        elif session.progress['completion_percentage'] >= 80:
            achievements.append("🌟 대부분의 실습을 완료했습니다!")
        elif session.progress['completion_percentage'] >= 50:
            achievements.append("👍 실습의 절반을 완료했습니다!")
        
        success_rate = (session.practice_data['successful_executions'] / session.practice_data['attempts'] * 100) if session.practice_data['attempts'] > 0 else 0
        
        if success_rate >= 90:
            achievements.append("🏆 매우 높은 성공률을 달성했습니다!")
        elif success_rate >= 70:
            achievements.append("✨ 좋은 성공률을 보여주고 있습니다!")
        
        if session.practice_data['hints_used'] == 0:
            achievements.append("🧠 힌트 없이 스스로 해결했습니다!")
        
        return achievements
    
    def _generate_recommendations(self, session: LearningSession) -> List[str]:
        """개선 권장사항"""
        recommendations = []
        
        success_rate = (session.practice_data['successful_executions'] / session.practice_data['attempts'] * 100) if session.practice_data['attempts'] > 0 else 0
        
        if success_rate < 50:
            recommendations.append("기초 개념을 다시 한 번 복습해보세요.")
            recommendations.append("힌트를 적극 활용하여 학습 효과를 높이세요.")
        
        if session.practice_data['hints_used'] > session.practice_data['attempts']:
            recommendations.append("스스로 문제를 해결해보는 시간을 늘려보세요.")
        
        if session.progress['completion_percentage'] < 100:
            recommendations.append("남은 단계들을 완료하여 전체 학습 과정을 마무리하세요.")
        
        return recommendations
    
    def get_system_statistics(self) -> Dict[str, Any]:
        """시스템 통계"""
        return {
            'system_stats': self.system_stats,
            'active_sessions': len(self.active_sessions),
            'total_sessions': len(self.sessions),
            'completion_rate': (self.system_stats['completed_sessions'] / self.system_stats['total_sessions'] * 100) if self.system_stats['total_sessions'] > 0 else 0
        }


def demo_integrated_learning_system():
    """통합 학습 시스템 데모"""
    print("=== 통합 학습 시스템 데모 ===\n")
    
    # 시스템 초기화
    learning_system = IntegratedLearningSystem()
    
    # 사용자 세션 생성
    user_id = "demo_user"
    session_id = learning_system.create_learning_session(user_id, "기술통계량 마스터 과정")
    
    print(f"학습 세션 생성: {session_id}")
    print(f"사용자: {user_id}")
    print()
    
    # 1단계 실행
    print("=== 1단계: 데이터 준비 ===")
    step1_code = """# 학생 성적 데이터 준비
scores = [85, 90, 78, 92, 88, 76, 95, 89, 84, 91]

# 데이터 기본 정보 확인
print(f"데이터: {scores}")
print(f"데이터 개수: {len(scores)}")
print("데이터 타입: list")
"""
    
    result1 = learning_system.execute_learning_step(session_id, step1_code)
    print(f"실행 성공: {result1['standardized']['success']}")
    print(f"단계 완료: {result1['standardized']['step_completed']}")
    print(f"진행률: {result1['session_progress']['completion_percentage']:.1f}%")
    
    if result1['interpretation']:
        print("학습 인사이트:")
        for insight in result1['interpretation']['learning_insights']:
            print(f"  - {insight}")
    print()
    
    # 2단계 실행
    print("=== 2단계: 중심경향성 계산 ===")
    step2_code = """# 데이터 준비 (이전 단계에서 계속)
scores = [85, 90, 78, 92, 88, 76, 95, 89, 84, 91]

# 평균 계산
total = sum(scores)
count = len(scores)
mean_value = total / count

print(f"총합: {total}")
print(f"평균: {mean_value:.2f}")

# 중앙값 계산 (수동 정렬)
sorted_scores = scores[:]
for i in range(len(sorted_scores)):
    for j in range(i + 1, len(sorted_scores)):
        if sorted_scores[i] > sorted_scores[j]:
            sorted_scores[i], sorted_scores[j] = sorted_scores[j], sorted_scores[i]

if len(sorted_scores) % 2 == 1:
    median_value = sorted_scores[len(sorted_scores) // 2]
else:
    mid1 = sorted_scores[len(sorted_scores) // 2 - 1]
    mid2 = sorted_scores[len(sorted_scores) // 2]
    median_value = (mid1 + mid2) / 2

print(f"중앙값: {median_value}")
"""
    
    result2 = learning_system.execute_learning_step(session_id, step2_code)
    print(f"실행 성공: {result2['standardized']['success']}")
    print(f"단계 완료: {result2['standardized']['step_completed']}")
    print(f"진행률: {result2['session_progress']['completion_percentage']:.1f}%")
    
    if result2['interpretation'] and result2['interpretation']['statistical_analysis']:
        print("통계 분석:")
        stats = result2['interpretation']['statistical_analysis']
        if 'mean' in stats:
            print(f"  평균: {stats['mean']['interpretation']}")
        if 'median' in stats:
            print(f"  중앙값: {stats['median']['interpretation']}")
    print()
    
    # 힌트 시스템 테스트
    print("=== 힌트 시스템 테스트 ===")
    hint_result = learning_system.get_learning_hint(session_id, 'basic')
    print(f"실습 힌트: {hint_result['practice_hint']['hint']}")
    print(f"추가 가이드: {hint_result['additional_guidance']['concept']}")
    print()
    
    # 세션 요약
    print("=== 세션 요약 ===")
    summary = learning_system.get_session_summary(session_id)
    metrics = summary['performance_metrics']
    print(f"성공률: {metrics['success_rate']:.1f}%")
    print(f"총 시도: {metrics['total_attempts']}")
    print(f"완료율: {metrics['completion_percentage']:.1f}%")
    print(f"효율성 점수: {metrics['efficiency_score']:.1f}")
    
    print("학습 성취:")
    for achievement in summary['learning_achievements']:
        print(f"  {achievement}")
    
    print("권장사항:")
    for recommendation in summary['recommendations']:
        print(f"  - {recommendation}")
    print()
    
    # 시스템 통계
    print("=== 시스템 통계 ===")
    system_stats = learning_system.get_system_statistics()
    print(f"전체 세션: {system_stats['total_sessions']}")
    print(f"활성 세션: {system_stats['active_sessions']}")
    print(f"완료율: {system_stats['completion_rate']:.1f}%")
    
    return learning_system


if __name__ == "__main__":
    demo_integrated_learning_system()