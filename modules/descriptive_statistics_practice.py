"""
Descriptive Statistics Practice - Task 3.3 Implementation
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from verification_hint_system import VerificationHintSystem, VerificationResult, HintLevel
from simple_demo import SimplePythonExecutor
from typing import Dict, Any, List, Optional, Tuple
import json
import datetime


class PracticeStep:
    """실습 단계"""
    
    def __init__(self, step_id: str, title: str, description: str, 
                 learning_objective: str, code_template: str = "",
                 expected_output: str = "", expected_variables: List[str] = None):
        self.step_id = step_id
        self.title = title
        self.description = description
        self.learning_objective = learning_objective
        self.code_template = code_template
        self.expected_output = expected_output
        self.expected_variables = expected_variables or []
        self.attempts = 0
        self.completed = False
        self.start_time = None
        self.completion_time = None
        self.user_code = ""
        self.execution_results = []
    
    def start(self):
        """단계 시작"""
        if not self.start_time:
            self.start_time = datetime.datetime.now()
    
    def complete(self):
        """단계 완료"""
        self.completed = True
        self.completion_time = datetime.datetime.now()
    
    def add_attempt(self, code: str, result: Dict[str, Any]):
        """시도 추가"""
        self.attempts += 1
        self.user_code = code
        self.execution_results.append({
            'attempt': self.attempts,
            'code': code,
            'result': result,
            'timestamp': datetime.datetime.now().isoformat()
        })
    
    def get_duration(self) -> Optional[float]:
        """소요 시간 계산 (분)"""
        if self.start_time and self.completion_time:
            return (self.completion_time - self.start_time).total_seconds() / 60
        return None
    
    def to_dict(self) -> Dict[str, Any]:
        """딕셔너리로 변환"""
        return {
            'step_id': self.step_id,
            'title': self.title,
            'description': self.description,
            'learning_objective': self.learning_objective,
            'code_template': self.code_template,
            'expected_output': self.expected_output,
            'expected_variables': self.expected_variables,
            'attempts': self.attempts,
            'completed': self.completed,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'completion_time': self.completion_time.isoformat() if self.completion_time else None,
            'user_code': self.user_code,
            'duration_minutes': self.get_duration()
        }


class PracticeSession:
    """실습 세션"""
    
    def __init__(self, session_id: str, title: str):
        self.session_id = session_id
        self.title = title
        self.steps = {}  # step_id -> PracticeStep
        self.step_order = []
        self.current_step_index = 0
        self.start_time = None
        self.completion_time = None
        self.completed = False
        self.user_notes = []
        self.session_variables = {}
    
    def add_step(self, step: PracticeStep):
        """단계 추가"""
        self.steps[step.step_id] = step
        self.step_order.append(step.step_id)
    
    def start_session(self):
        """세션 시작"""
        self.start_time = datetime.datetime.now()
        if self.step_order:
            first_step = self.steps[self.step_order[0]]
            first_step.start()
    
    def get_current_step(self) -> Optional[PracticeStep]:
        """현재 단계 가져오기"""
        if 0 <= self.current_step_index < len(self.step_order):
            step_id = self.step_order[self.current_step_index]
            return self.steps[step_id]
        return None
    
    def complete_current_step(self):
        """현재 단계 완료"""
        current_step = self.get_current_step()
        if current_step:
            current_step.complete()
            self.current_step_index += 1
            
            # 다음 단계 시작
            next_step = self.get_current_step()
            if next_step:
                next_step.start()
            else:
                # 모든 단계 완료
                self.complete_session()
    
    def complete_session(self):
        """세션 완료"""
        self.completed = True
        self.completion_time = datetime.datetime.now()
    
    def add_note(self, note: str):
        """노트 추가"""
        self.user_notes.append({
            'note': note,
            'timestamp': datetime.datetime.now().isoformat()
        })
    
    def update_variables(self, variables: Dict[str, Any]):
        """세션 변수 업데이트"""
        self.session_variables.update(variables)
    
    def get_progress(self) -> Dict[str, Any]:
        """진행률 계산"""
        total_steps = len(self.step_order)
        completed_steps = sum(1 for step in self.steps.values() if step.completed)
        
        return {
            'total_steps': total_steps,
            'completed_steps': completed_steps,
            'current_step_index': self.current_step_index,
            'progress_percentage': round(completed_steps / total_steps * 100, 1) if total_steps > 0 else 0,
            'completed': self.completed
        }
    
    def get_duration(self) -> Optional[float]:
        """세션 소요 시간 (분)"""
        if self.start_time:
            end_time = self.completion_time or datetime.datetime.now()
            return (end_time - self.start_time).total_seconds() / 60
        return None
    
    def to_dict(self) -> Dict[str, Any]:
        """딕셔너리로 변환"""
        return {
            'session_id': self.session_id,
            'title': self.title,
            'steps': {step_id: step.to_dict() for step_id, step in self.steps.items()},
            'step_order': self.step_order,
            'current_step_index': self.current_step_index,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'completion_time': self.completion_time.isoformat() if self.completion_time else None,
            'completed': self.completed,
            'user_notes': self.user_notes,
            'session_variables': self.session_variables,
            'progress': self.get_progress(),
            'duration_minutes': self.get_duration()
        }


class DescriptiveStatisticsPractice:
    """기술통계량 실습 시스템"""
    
    def __init__(self):
        self.verification_system = VerificationHintSystem()
        self.code_executor = SimplePythonExecutor()
        self.sessions = {}  # session_id -> PracticeSession
        self._initialize_practice_steps()
    
    def _initialize_practice_steps(self):
        """실습 단계 초기화"""
        self.practice_steps = {
            'step1': PracticeStep(
                step_id="step1",
                title="1단계: 데이터 준비",
                description="분석할 데이터를 준비하고 기본 정보를 파악합니다.",
                learning_objective="데이터를 리스트로 생성하고 기본 정보를 확인할 수 있다.",
                code_template="""# 학생 성적 데이터 준비
scores = [85, 90, 78, 92, 88, 76, 95, 89, 84, 91]

# 데이터 기본 정보 확인
print(f"데이터: {scores}")
print(f"데이터 개수: {len(scores)}")
print("데이터 타입: list")
""",
                expected_output="데이터: [85, 90, 78, 92, 88, 76, 95, 89, 84, 91]",
                expected_variables=["scores"]
            ),
            'step2': PracticeStep(
                step_id="step2",
                title="2단계: 중심경향성 계산",
                description="평균, 중앙값을 계산하여 데이터의 중심을 파악합니다.",
                learning_objective="평균과 중앙값을 계산하고 그 의미를 이해할 수 있다.",
                code_template="""# 데이터 준비 (이전 단계에서 계속)
scores = [85, 90, 78, 92, 88, 76, 95, 89, 84, 91]

# 평균 계산
total = sum(scores)
count = len(scores)
mean_value = total / count

print(f"총합: {total}")
print(f"평균: {mean_value:.2f}")

# 중앙값 계산 (수동 정렬)
sorted_scores = scores[:]  # 복사본 생성
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
""",
                expected_output="총합: 868",
                expected_variables=["mean_value", "median_value"]
            ),
            'step3': PracticeStep(
                step_id="step3",
                title="3단계: 산포도 계산",
                description="표준편차와 분산을 계산하여 데이터의 퍼짐 정도를 파악합니다.",
                learning_objective="분산과 표준편차를 계산하고 그 의미를 이해할 수 있다.",
                code_template="""# 데이터와 이전 계산 결과 준비
scores = [85, 90, 78, 92, 88, 76, 95, 89, 84, 91]
mean_value = sum(scores) / len(scores)

# 분산 계산 (단계별로)
squared_diffs = []
for x in scores:
    diff = x - mean_value
    squared_diff = diff * diff
    squared_diffs.append(squared_diff)

variance = sum(squared_diffs) / len(scores)

# 표준편차 계산
std_dev = variance ** 0.5

print(f"분산: {variance:.2f}")
print(f"표준편차: {std_dev:.2f}")

# 범위 계산
data_range = max(scores) - min(scores)
print(f"범위: {data_range}")
""",
                expected_output="분산:",
                expected_variables=["variance", "std_dev", "data_range"]
            ),
            'step4': PracticeStep(
                step_id="step4",
                title="4단계: 결과 해석",
                description="계산된 통계량들의 의미를 해석하고 결론을 도출합니다.",
                learning_objective="기술통계량의 의미를 해석하고 데이터의 특성을 설명할 수 있다.",
                code_template="""# 데이터와 이전 계산 결과 준비
scores = [85, 90, 78, 92, 88, 76, 95, 89, 84, 91]
mean_value = sum(scores) / len(scores)

# 수동 정렬
sorted_scores = scores[:]
for i in range(len(sorted_scores)):
    for j in range(i + 1, len(sorted_scores)):
        if sorted_scores[i] > sorted_scores[j]:
            sorted_scores[i], sorted_scores[j] = sorted_scores[j], sorted_scores[i]

median_value = (sorted_scores[4] + sorted_scores[5]) / 2

# 분산 계산 (단계별로)
squared_diffs = []
for x in scores:
    diff = x - mean_value
    squared_diff = diff * diff
    squared_diffs.append(squared_diff)

variance = sum(squared_diffs) / len(scores)
std_dev = variance ** 0.5
data_range = max(scores) - min(scores)

# 모든 통계량 요약
print("=== 기술통계량 요약 ===")
print(f"데이터 개수: {len(scores)}")
print(f"평균: {mean_value:.2f}")
print(f"중앙값: {median_value}")
print(f"표준편차: {std_dev:.2f}")
print(f"분산: {variance:.2f}")
print(f"최솟값: {min(scores)}")
print(f"최댓값: {max(scores)}")
print(f"범위: {data_range}")

print("\\n=== 해석 ===")
print("이 학급의 평균 점수는 86.8점으로 양호한 수준입니다.")
print("중앙값(88.5)이 평균보다 높아 약간 왼쪽으로 치우친 분포를 보입니다.")
""",
                expected_output="=== 기술통계량 요약 ===",
                expected_variables=[]
            ),
            'step5': PracticeStep(
                step_id="step5",
                title="5단계: 시각화 및 종합 분석",
                description="데이터를 시각화하고 종합적인 분석을 수행합니다.",
                learning_objective="기술통계량과 시각화를 통해 데이터를 종합적으로 분석할 수 있다.",
                code_template="""# 데이터와 이전 계산 결과 준비
scores = [85, 90, 78, 92, 88, 76, 95, 89, 84, 91]

# 수동 정렬
sorted_scores = scores[:]
for i in range(len(sorted_scores)):
    for j in range(i + 1, len(sorted_scores)):
        if sorted_scores[i] > sorted_scores[j]:
            sorted_scores[i], sorted_scores[j] = sorted_scores[j], sorted_scores[i]

# 히스토그램 시뮬레이션
print("=== 히스토그램 시뮬레이션 ===")
print("70-75: |")
print("76-80: |██")
print("81-85: |██")
print("86-90: |████")
print("91-95: |███")

print("\\n=== 종합 분석 ===")
print("1. 중심경향성: 평균 86.8점, 중앙값 88.5점")
print("2. 산포도: 표준편차 6.1점으로 적당한 분산")
print("3. 분포 형태: 약간 왼쪽으로 치우친 분포")

# 사분위수 계산
q1_index = len(sorted_scores) // 4
q3_index = 3 * len(sorted_scores) // 4
q1 = sorted_scores[q1_index]
q3 = sorted_scores[q3_index]
iqr = q3 - q1

print(f"\\n=== 사분위수 ===")
print(f"1사분위수 (Q1): {q1}")
print(f"3사분위수 (Q3): {q3}")
print(f"사분위수 범위 (IQR): {iqr}")
""",
                expected_output="=== 히스토그램 시뮬레이션 ===",
                expected_variables=["q1", "q3", "iqr"]
            )
        }
    
    def create_session(self, session_id: str, title: str = "기술통계량 실습") -> PracticeSession:
        """새 실습 세션 생성"""
        session = PracticeSession(session_id, title)
        
        # 모든 단계를 세션에 추가
        for step_id in ['step1', 'step2', 'step3', 'step4', 'step5']:
            step = self.practice_steps[step_id]
            session.add_step(step)
        
        self.sessions[session_id] = session
        return session
    
    def get_session(self, session_id: str) -> Optional[PracticeSession]:
        """세션 가져오기"""
        return self.sessions.get(session_id)
    
    def execute_step_code(self, session_id: str, code: str) -> Dict[str, Any]:
        """단계 코드 실행"""
        session = self.get_session(session_id)
        if not session:
            return {"error": "세션을 찾을 수 없습니다."}
        
        current_step = session.get_current_step()
        if not current_step:
            return {"error": "현재 단계를 찾을 수 없습니다."}
        
        # 코드 실행
        execution_result = self.code_executor.execute(code)
        
        # 결과 검증
        verification_result = self._verify_step_completion(current_step, code, execution_result)
        
        # 시도 기록
        current_step.add_attempt(code, {
            'execution': execution_result,
            'verification': verification_result
        })
        
        # 단계 완료 확인
        if verification_result.get('success', False):
            session.complete_current_step()
        
        return {
            'execution': execution_result,
            'verification': verification_result,
            'step_completed': verification_result.get('success', False),
            'session_progress': session.get_progress()
        }
    
    def _verify_step_completion(self, step: PracticeStep, code: str, execution_result: Dict[str, Any]) -> Dict[str, Any]:
        """단계 완료 검증"""
        if not execution_result.get('success', True):
            return {
                'success': False,
                'message': f'코드 실행 중 오류가 발생했습니다: {execution_result.get("error", "알 수 없는 오류")}',
                'hint': '오류 메시지를 확인하고 코드를 수정해보세요.'
            }
        
        # 변수 존재 확인
        variables = execution_result.get('variables', {})
        missing_vars = [var for var in step.expected_variables if var not in variables]
        
        if missing_vars:
            return {
                'success': False,
                'message': f'필요한 변수가 누락되었습니다: {", ".join(missing_vars)}',
                'hint': f'다음 변수들을 정의해주세요: {", ".join(missing_vars)}'
            }
        
        # 출력 확인 (부분 일치)
        output = execution_result.get('output', '')
        if step.expected_output and step.expected_output not in output:
            return {
                'success': False,
                'message': '예상된 출력과 다릅니다.',
                'hint': f'예상 출력에 다음이 포함되어야 합니다: {step.expected_output[:50]}...'
            }
        
        return {
            'success': True,
            'message': '단계를 성공적으로 완료했습니다!',
            'hint': '다음 단계로 진행하세요.'
        }
    
    def get_step_hint(self, session_id: str, hint_level: str = 'basic') -> Dict[str, Any]:
        """단계별 힌트 제공"""
        session = self.get_session(session_id)
        if not session:
            return {"error": "세션을 찾을 수 없습니다."}
        
        current_step = session.get_current_step()
        if not current_step:
            return {"error": "현재 단계를 찾을 수 없습니다."}
        
        hints = {
            'step1': {
                'basic': '리스트를 생성하고 len() 함수를 사용해보세요.',
                'detailed': 'scores = [85, 90, 78, ...] 형태로 리스트를 만들고, print()와 len()을 사용하세요.',
                'solution': current_step.code_template
            },
            'step2': {
                'basic': 'sum() 함수와 정렬을 활용해보세요.',
                'detailed': '평균은 sum(scores)/len(scores), 중앙값은 정렬 후 가운데 값을 찾으세요.',
                'solution': current_step.code_template
            },
            'step3': {
                'basic': '분산은 편차의 제곱의 평균입니다.',
                'detailed': 'variance = sum((x - mean_value) ** 2 for x in scores) / len(scores)',
                'solution': current_step.code_template
            },
            'step4': {
                'basic': '계산된 값들을 정리하고 의미를 해석해보세요.',
                'detailed': '각 통계량의 값을 출력하고 데이터의 특성을 설명하세요.',
                'solution': current_step.code_template
            },
            'step5': {
                'basic': '사분위수를 계산하고 종합적인 분석을 해보세요.',
                'detailed': 'Q1, Q3를 구하고 IQR을 계산한 후 전체적인 분석을 제시하세요.',
                'solution': current_step.code_template
            }
        }
        
        step_hints = hints.get(current_step.step_id, {})
        return {
            'hint': step_hints.get(hint_level, '힌트를 찾을 수 없습니다.'),
            'step_id': current_step.step_id,
            'step_title': current_step.title
        }
    
    def get_session_summary(self, session_id: str) -> Dict[str, Any]:
        """세션 요약 정보"""
        session = self.get_session(session_id)
        if not session:
            return {"error": "세션을 찾을 수 없습니다."}
        
        return {
            'session_info': session.to_dict(),
            'current_step': session.get_current_step().to_dict() if session.get_current_step() else None,
            'progress': session.get_progress(),
            'total_attempts': sum(step.attempts for step in session.steps.values()),
            'completed_steps': [step.step_id for step in session.steps.values() if step.completed]
        }


def demo_descriptive_statistics_practice():
    """기술통계량 실습 시스템 데모"""
    print("=== 기술통계량 실습 시스템 데모 ===\n")
    
    # 실습 시스템 초기화
    practice_system = DescriptiveStatisticsPractice()
    
    # 새 세션 생성
    session_id = "demo_session_001"
    session = practice_system.create_session(session_id, "기술통계량 실습 데모")
    session.start_session()
    
    print(f"세션 시작: {session.title}")
    print(f"총 단계 수: {len(session.step_order)}")
    print()
    
    # 각 단계별 데모
    for i, step_id in enumerate(session.step_order, 1):
        current_step = session.get_current_step()
        if not current_step:
            break
            
        print(f"=== {current_step.title} ===")
        print(f"설명: {current_step.description}")
        print(f"학습 목표: {current_step.learning_objective}")
        print()
        
        # 템플릿 코드 실행
        print("템플릿 코드:")
        print("```python")
        print(current_step.code_template.strip())
        print("```")
        print()
        
        # 코드 실행 및 검증
        result = practice_system.execute_step_code(session_id, current_step.code_template)
        
        if result['execution'].get('output'):
            print("실행 결과:")
            print(result['execution']['output'])
            print()
        
        if result['verification']['success']:
            print("✅ 단계 완료!")
        else:
            print("❌ 단계 미완료:", result['verification']['message'])
        
        print(f"진행률: {result['session_progress']['progress_percentage']}%")
        print("-" * 50)
        print()
    
    # 세션 요약
    summary = practice_system.get_session_summary(session_id)
    print("=== 세션 완료 요약 ===")
    print(f"총 소요 시간: {summary['session_info']['duration_minutes']:.1f}분")
    print(f"총 시도 횟수: {summary['total_attempts']}")
    print(f"완료된 단계: {len(summary['completed_steps'])}/{summary['progress']['total_steps']}")
    print(f"완료율: {summary['progress']['progress_percentage']}%")
    
    return practice_system, session


if __name__ == "__main__":
    # 기본 데모 실행
    demo_descriptive_statistics_practice()