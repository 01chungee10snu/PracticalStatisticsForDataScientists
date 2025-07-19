"""
Step-by-Step Guide System - Task 3.1 Implementation
"""

import uuid
import datetime
from typing import Dict, Any, List, Optional, Tuple
from enum import Enum
import json


class StepStatus(Enum):
    """단계 상태"""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class SessionStatus(Enum):
    """세션 상태"""
    CREATED = "created"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    ABANDONED = "abandoned"


class LearningStep:
    """학습 단계"""
    
    def __init__(self, step_id: str, title: str, description: str, 
                 learning_objective: str, code_template: str = "",
                 hints: List[str] = None, success_criteria: Dict[str, Any] = None):
        self.step_id = step_id
        self.title = title
        self.description = description
        self.learning_objective = learning_objective
        self.code_template = code_template
        self.hints = hints or []
        self.success_criteria = success_criteria or {}
        self.status = StepStatus.NOT_STARTED
        self.start_time = None
        self.completion_time = None
        self.attempts = 0
        self.user_code = ""
        self.execution_results = []
        self.feedback = []
    
    def start(self):
        """단계 시작"""
        self.status = StepStatus.IN_PROGRESS
        self.start_time = datetime.datetime.now()
    
    def complete(self):
        """단계 완료"""
        self.status = StepStatus.COMPLETED
        self.completion_time = datetime.datetime.now()
    
    def fail(self):
        """단계 실패"""
        self.status = StepStatus.FAILED
    
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
    
    def add_feedback(self, feedback: str):
        """피드백 추가"""
        self.feedback.append({
            'message': feedback,
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
            'hints': self.hints,
            'success_criteria': self.success_criteria,
            'status': self.status.value,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'completion_time': self.completion_time.isoformat() if self.completion_time else None,
            'attempts': self.attempts,
            'user_code': self.user_code,
            'execution_results': self.execution_results,
            'feedback': self.feedback,
            'duration_minutes': self.get_duration()
        }


class LearningSession:
    """학습 세션"""
    
    def __init__(self, session_id: str, concept_name: str, steps: List[LearningStep]):
        self.session_id = session_id
        self.concept_name = concept_name
        self.steps = {step.step_id: step for step in steps}
        self.step_order = [step.step_id for step in steps]
        self.current_step_index = 0
        self.status = SessionStatus.CREATED
        self.start_time = None
        self.completion_time = None
        self.total_attempts = 0
        self.session_notes = []
    
    def start_session(self):
        """세션 시작"""
        self.status = SessionStatus.ACTIVE
        self.start_time = datetime.datetime.now()
        
        # 첫 번째 단계 시작
        if self.step_order:
            first_step = self.steps[self.step_order[0]]
            first_step.start()
    
    def get_current_step(self) -> Optional[LearningStep]:
        """현재 단계 가져오기"""
        if self.current_step_index < len(self.step_order):
            step_id = self.step_order[self.current_step_index]
            return self.steps[step_id]
        return None
    
    def complete_current_step(self) -> bool:
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
            
            return True
        return False
    
    def complete_session(self):
        """세션 완료"""
        self.status = SessionStatus.COMPLETED
        self.completion_time = datetime.datetime.now()
    
    def pause_session(self):
        """세션 일시정지"""
        self.status = SessionStatus.PAUSED
    
    def resume_session(self):
        """세션 재개"""
        self.status = SessionStatus.ACTIVE
    
    def abandon_session(self):
        """세션 포기"""
        self.status = SessionStatus.ABANDONED
    
    def get_progress(self) -> Dict[str, Any]:
        """진행률 계산"""
        total_steps = len(self.step_order)
        completed_steps = sum(1 for step in self.steps.values() if step.status == StepStatus.COMPLETED)
        
        progress_percentage = (completed_steps / total_steps * 100) if total_steps > 0 else 0
        
        return {
            'total_steps': total_steps,
            'completed_steps': completed_steps,
            'current_step_index': self.current_step_index,
            'progress_percentage': round(progress_percentage, 1),
            'status': self.status.value,
            'is_completed': self.status == SessionStatus.COMPLETED
        }
    
    def get_session_duration(self) -> Optional[float]:
        """세션 총 소요 시간 (분)"""
        if self.start_time:
            end_time = self.completion_time or datetime.datetime.now()
            return (end_time - self.start_time).total_seconds() / 60
        return None
    
    def add_session_note(self, note: str):
        """세션 노트 추가"""
        self.session_notes.append({
            'note': note,
            'timestamp': datetime.datetime.now().isoformat()
        })
    
    def to_dict(self) -> Dict[str, Any]:
        """딕셔너리로 변환"""
        return {
            'session_id': self.session_id,
            'concept_name': self.concept_name,
            'steps': {step_id: step.to_dict() for step_id, step in self.steps.items()},
            'step_order': self.step_order,
            'current_step_index': self.current_step_index,
            'status': self.status.value,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'completion_time': self.completion_time.isoformat() if self.completion_time else None,
            'total_attempts': self.total_attempts,
            'session_notes': self.session_notes,
            'progress': self.get_progress(),
            'duration_minutes': self.get_session_duration()
        }


class StepByStepGuide:
    """단계별 실습 가이드 시스템"""
    
    def __init__(self):
        self.sessions = {}  # session_id -> LearningSession
        self.concept_templates = {}  # concept_name -> step templates
        self._initialize_concept_templates()
    
    def _initialize_concept_templates(self):
        """개념별 템플릿 초기화"""
        # 기술통계량 학습 과정
        self.concept_templates['descriptive_statistics'] = [
            LearningStep(
                step_id="step_1",
                title="데이터 준비",
                description="분석할 데이터를 준비하고 기본 구조를 파악합니다.",
                learning_objective="데이터를 리스트로 생성하고 기본 정보를 확인할 수 있다.",
                code_template="""# 학생 성적 데이터 준비
scores = [85, 90, 78, 92, 88, 76, 95, 89, 84, 91]

# 데이터 기본 정보 확인
print(f"데이터: {scores}")
print(f"데이터 개수: {len(scores)}")
print(f"데이터 타입: {type(scores)}")""",
                hints=[
                    "리스트를 사용하여 숫자 데이터를 저장하세요.",
                    "len() 함수로 데이터 개수를 확인할 수 있습니다.",
                    "print() 함수로 결과를 출력하세요."
                ],
                success_criteria={
                    'has_data_list': True,
                    'prints_data_info': True,
                    'data_count_correct': True
                }
            ),
            LearningStep(
                step_id="step_2",
                title="중심경향성 계산",
                description="평균, 중앙값을 계산하여 데이터의 중심을 파악합니다.",
                learning_objective="평균과 중앙값을 계산하고 그 의미를 이해할 수 있다.",
                code_template="""# 이전 단계에서 준비한 데이터 사용
# scores = [85, 90, 78, 92, 88, 76, 95, 89, 84, 91]

# 평균 계산
total = sum(scores)
count = len(scores)
mean_value = total / count

print(f"총합: {total}")
print(f"평균: {mean_value:.2f}")

# 중앙값 계산을 위한 정렬
# 여기에 중앙값 계산 코드를 작성하세요""",
                hints=[
                    "sum() 함수로 총합을 구할 수 있습니다.",
                    "중앙값을 구하려면 먼저 데이터를 정렬해야 합니다.",
                    "정렬된 데이터의 가운데 값이 중앙값입니다."
                ],
                success_criteria={
                    'calculates_mean': True,
                    'calculates_median': True,
                    'prints_results': True
                }
            ),
            LearningStep(
                step_id="step_3",
                title="산포도 계산",
                description="표준편차와 분산을 계산하여 데이터의 퍼짐 정도를 파악합니다.",
                learning_objective="분산과 표준편차를 계산하고 그 의미를 이해할 수 있다.",
                code_template="""# 이전 단계의 평균값 사용
# mean_value = 86.8

# 분산 계산
variance = sum((x - mean_value) ** 2 for x in scores) / len(scores)

# 표준편차 계산
std_dev = variance ** 0.5

print(f"분산: {variance:.2f}")
print(f"표준편차: {std_dev:.2f}")

# 범위 계산
data_range = max(scores) - min(scores)
print(f"범위: {data_range}")""",
                hints=[
                    "분산은 각 값과 평균의 차이를 제곱한 값들의 평균입니다.",
                    "표준편차는 분산의 제곱근입니다.",
                    "범위는 최댓값에서 최솟값을 뺀 값입니다."
                ],
                success_criteria={
                    'calculates_variance': True,
                    'calculates_std_dev': True,
                    'calculates_range': True
                }
            ),
            LearningStep(
                step_id="step_4",
                title="결과 해석",
                description="계산된 통계량들의 의미를 해석하고 결론을 도출합니다.",
                learning_objective="기술통계량의 의미를 해석하고 데이터의 특성을 설명할 수 있다.",
                code_template="""# 모든 통계량 요약
print("=== 기술통계량 요약 ===")
print(f"데이터 개수: {len(scores)}")
print(f"평균: {mean_value:.2f}")
print(f"중앙값: {median_value:.2f}")
print(f"표준편차: {std_dev:.2f}")
print(f"최솟값: {min(scores)}")
print(f"최댓값: {max(scores)}")
print(f"범위: {data_range}")

# 해석 추가
print("\\n=== 해석 ===")
print("이 데이터는...")
# 여기에 해석을 추가하세요""",
                hints=[
                    "평균과 중앙값을 비교해보세요.",
                    "표준편차가 크면 데이터가 많이 퍼져있다는 의미입니다.",
                    "실제 상황에 맞는 해석을 추가해보세요."
                ],
                success_criteria={
                    'summarizes_statistics': True,
                    'provides_interpretation': True,
                    'draws_conclusions': True
                }
            )
        ]
    
    def create_session(self, concept_name: str, user_id: str = None) -> str:
        """새 학습 세션 생성"""
        session_id = str(uuid.uuid4())
        
        if concept_name not in self.concept_templates:
            raise ValueError(f"Unknown concept: {concept_name}")
        
        # 템플릿에서 단계들 복사
        steps = []
        for template_step in self.concept_templates[concept_name]:
            step = LearningStep(
                step_id=template_step.step_id,
                title=template_step.title,
                description=template_step.description,
                learning_objective=template_step.learning_objective,
                code_template=template_step.code_template,
                hints=template_step.hints.copy(),
                success_criteria=template_step.success_criteria.copy()
            )
            steps.append(step)
        
        # 세션 생성
        session = LearningSession(session_id, concept_name, steps)
        self.sessions[session_id] = session
        
        return session_id
    
    def get_session(self, session_id: str) -> Optional[LearningSession]:
        """세션 조회"""
        return self.sessions.get(session_id)
    
    def start_session(self, session_id: str) -> bool:
        """세션 시작"""
        session = self.get_session(session_id)
        if session:
            session.start_session()
            return True
        return False
    
    def get_current_step(self, session_id: str) -> Optional[Dict[str, Any]]:
        """현재 단계 정보 조회"""
        session = self.get_session(session_id)
        if session:
            current_step = session.get_current_step()
            if current_step:
                return current_step.to_dict()
        return None
    
    def submit_step_solution(self, session_id: str, code: str, execution_result: Dict[str, Any]) -> Dict[str, Any]:
        """단계 솔루션 제출"""
        session = self.get_session(session_id)
        if not session:
            return {'success': False, 'error': 'Session not found'}
        
        current_step = session.get_current_step()
        if not current_step:
            return {'success': False, 'error': 'No current step'}
        
        # 시도 기록
        current_step.add_attempt(code, execution_result)
        session.total_attempts += 1
        
        # 성공 여부 판단 (간단한 기준)
        is_successful = execution_result.get('success', False)
        
        if is_successful:
            current_step.complete()
            session.complete_current_step()
            
            return {
                'success': True,
                'step_completed': True,
                'message': f'단계 "{current_step.title}" 완료!',
                'progress': session.get_progress()
            }
        else:
            # 힌트 제공
            hint_index = min(current_step.attempts - 1, len(current_step.hints) - 1)
            hint = current_step.hints[hint_index] if current_step.hints else "다시 시도해보세요."
            
            return {
                'success': False,
                'step_completed': False,
                'message': '단계를 완료하지 못했습니다.',
                'hint': hint,
                'attempts': current_step.attempts,
                'progress': session.get_progress()
            }
    
    def get_session_progress(self, session_id: str) -> Optional[Dict[str, Any]]:
        """세션 진행률 조회"""
        session = self.get_session(session_id)
        if session:
            return session.get_progress()
        return None
    
    def get_available_concepts(self) -> List[str]:
        """사용 가능한 개념 목록"""
        return list(self.concept_templates.keys())
    
    def export_session_data(self, session_id: str) -> Optional[Dict[str, Any]]:
        """세션 데이터 내보내기"""
        session = self.get_session(session_id)
        if session:
            return session.to_dict()
        return None


# 테스트용 함수
def test_step_by_step_guide():
    """단계별 가이드 시스템 테스트"""
    guide = StepByStepGuide()
    
    print("=== Step-by-Step Guide System Test ===")
    
    # 1. 세션 생성
    print("\n1. Creating Session")
    session_id = guide.create_session('descriptive_statistics')
    print(f"Session created: {session_id}")
    
    # 2. 세션 시작
    print("\n2. Starting Session")
    guide.start_session(session_id)
    
    # 3. 현재 단계 확인
    print("\n3. Current Step")
    current_step = guide.get_current_step(session_id)
    if current_step:
        print(f"Step: {current_step['title']}")
        print(f"Description: {current_step['description']}")
        print(f"Learning Objective: {current_step['learning_objective']}")
    
    # 4. 진행률 확인
    print("\n4. Progress Check")
    progress = guide.get_session_progress(session_id)
    if progress:
        print(f"Progress: {progress['completed_steps']}/{progress['total_steps']} ({progress['progress_percentage']}%)")
        print(f"Status: {progress['status']}")
    
    # 5. 단계 솔루션 제출 (성공 시뮬레이션)
    print("\n5. Submitting Solution")
    mock_result = {'success': True, 'output': 'Test output'}
    submission_result = guide.submit_step_solution(session_id, "test code", mock_result)
    print(f"Submission result: {submission_result}")
    
    # 6. 업데이트된 진행률 확인
    print("\n6. Updated Progress")
    progress = guide.get_session_progress(session_id)
    if progress:
        print(f"Progress: {progress['completed_steps']}/{progress['total_steps']} ({progress['progress_percentage']}%)")
    
    return session_id


if __name__ == "__main__":
    session_id = test_step_by_step_guide()
    print(f"\nTest completed with session: {session_id}")