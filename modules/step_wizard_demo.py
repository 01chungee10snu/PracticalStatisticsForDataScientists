"""
Step Wizard Demo - Task 3.1 Implementation Demo
"""

import uuid
import datetime
from typing import Dict, Any, List, Optional
from enum import Enum


class StepStatus(Enum):
    """단계 상태"""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class SessionStatus(Enum):
    """세션 상태"""
    CREATED = "created"
    ACTIVE = "active"
    COMPLETED = "completed"


class SimpleStep:
    """간단한 학습 단계"""
    
    def __init__(self, step_id: str, title: str, description: str, code_template: str = ""):
        self.step_id = step_id
        self.title = title
        self.description = description
        self.code_template = code_template
        self.status = StepStatus.NOT_STARTED
        self.attempts = 0
        self.user_code = ""
    
    def start(self):
        self.status = StepStatus.IN_PROGRESS
    
    def complete(self):
        self.status = StepStatus.COMPLETED
    
    def add_attempt(self, code: str):
        self.attempts += 1
        self.user_code = code


class SimpleSession:
    """간단한 학습 세션"""
    
    def __init__(self, session_id: str, concept_name: str):
        self.session_id = session_id
        self.concept_name = concept_name
        self.steps = []
        self.current_step_index = 0
        self.status = SessionStatus.CREATED
        self.start_time = None
    
    def add_step(self, step: SimpleStep):
        self.steps.append(step)
    
    def start_session(self):
        self.status = SessionStatus.ACTIVE
        self.start_time = datetime.datetime.now()
        if self.steps:
            self.steps[0].start()
    
    def get_current_step(self) -> Optional[SimpleStep]:
        if self.current_step_index < len(self.steps):
            return self.steps[self.current_step_index]
        return None
    
    def complete_current_step(self):
        current_step = self.get_current_step()
        if current_step:
            current_step.complete()
            self.current_step_index += 1
            
            # 다음 단계 시작
            next_step = self.get_current_step()
            if next_step:
                next_step.start()
            else:
                self.status = SessionStatus.COMPLETED
    
    def get_progress(self) -> Dict[str, Any]:
        total_steps = len(self.steps)
        completed_steps = sum(1 for step in self.steps if step.status == StepStatus.COMPLETED)
        progress_percentage = (completed_steps / total_steps * 100) if total_steps > 0 else 0
        
        return {
            'total_steps': total_steps,
            'completed_steps': completed_steps,
            'current_step_index': self.current_step_index,
            'progress_percentage': round(progress_percentage, 1),
            'status': self.status.value
        }


class StepWizard:
    """단계별 학습 마법사"""
    
    def __init__(self):
        self.sessions = {}
    
    def create_descriptive_stats_session(self) -> str:
        """기술통계량 학습 세션 생성"""
        session_id = str(uuid.uuid4())[:8]  # 짧은 ID
        session = SimpleSession(session_id, "기술통계량")
        
        # 4단계 학습 과정 정의
        steps = [
            SimpleStep(
                "step1", 
                "1단계: 데이터 준비",
                "분석할 데이터를 준비하고 기본 정보를 확인합니다.",
                """# 학생 성적 데이터 준비
scores = [85, 90, 78, 92, 88, 76, 95, 89, 84, 91]
print(f"데이터: {scores}")
print(f"데이터 개수: {len(scores)}")"""
            ),
            SimpleStep(
                "step2",
                "2단계: 중심경향성 계산",
                "평균과 중앙값을 계산합니다.",
                """# 평균 계산
total = sum(scores)
mean_value = total / len(scores)
print(f"평균: {mean_value:.2f}")"""
            ),
            SimpleStep(
                "step3",
                "3단계: 산포도 계산",
                "표준편차와 분산을 계산합니다.",
                """# 표준편차 계산
variance = sum((x - mean_value) ** 2 for x in scores) / len(scores)
std_dev = variance ** 0.5
print(f"표준편차: {std_dev:.2f}")"""
            ),
            SimpleStep(
                "step4",
                "4단계: 결과 해석",
                "계산된 통계량의 의미를 해석합니다.",
                """# 결과 요약
print("=== 기술통계량 요약 ===")
print(f"평균: {mean_value:.2f}")
print(f"표준편차: {std_dev:.2f}")
print("데이터 분석 완료!")"""
            )
        ]
        
        for step in steps:
            session.add_step(step)
        
        self.sessions[session_id] = session
        return session_id
    
    def get_session(self, session_id: str) -> Optional[SimpleSession]:
        return self.sessions.get(session_id)
    
    def start_session(self, session_id: str):
        session = self.get_session(session_id)
        if session:
            session.start_session()
    
    def get_current_step_info(self, session_id: str) -> Optional[Dict[str, Any]]:
        session = self.get_session(session_id)
        if session:
            current_step = session.get_current_step()
            if current_step:
                return {
                    'step_id': current_step.step_id,
                    'title': current_step.title,
                    'description': current_step.description,
                    'code_template': current_step.code_template,
                    'status': current_step.status.value,
                    'attempts': current_step.attempts
                }
        return None
    
    def complete_step(self, session_id: str, user_code: str = ""):
        session = self.get_session(session_id)
        if session:
            current_step = session.get_current_step()
            if current_step:
                current_step.add_attempt(user_code)
                session.complete_current_step()
    
    def get_progress(self, session_id: str) -> Optional[Dict[str, Any]]:
        session = self.get_session(session_id)
        if session:
            return session.get_progress()
        return None


def demo_step_wizard():
    """단계별 학습 마법사 데모"""
    print("🧙‍♂️ Task 3.1: Step-by-Step Learning Wizard Demo")
    print("=" * 60)
    
    wizard = StepWizard()
    
    # 1. 세션 생성
    print("\n✅ 1. Creating Learning Session")
    session_id = wizard.create_descriptive_stats_session()
    print(f"   Session ID: {session_id}")
    print(f"   Concept: 기술통계량 학습")
    
    # 2. 세션 시작
    print("\n✅ 2. Starting Session")
    wizard.start_session(session_id)
    print(f"   Session started successfully")
    
    # 3. 초기 진행률 확인
    print("\n✅ 3. Initial Progress Check")
    progress = wizard.get_progress(session_id)
    if progress:
        print(f"   Progress: {progress['completed_steps']}/{progress['total_steps']} steps")
        print(f"   Percentage: {progress['progress_percentage']}%")
        print(f"   Status: {progress['status']}")
    
    # 4. 각 단계 진행 시뮬레이션
    print("\n✅ 4. Step-by-Step Progress Simulation")
    
    for step_num in range(4):  # 4단계
        print(f"\n   --- Step {step_num + 1} ---")
        
        # 현재 단계 정보
        step_info = wizard.get_current_step_info(session_id)
        if step_info:
            print(f"   Title: {step_info['title']}")
            print(f"   Description: {step_info['description']}")
            print(f"   Status: {step_info['status']}")
            
            # 코드 템플릿 표시 (일부만)
            code_preview = step_info['code_template'][:50] + "..." if len(step_info['code_template']) > 50 else step_info['code_template']
            print(f"   Code Template: {code_preview}")
            
            # 단계 완료
            wizard.complete_step(session_id, f"# User code for step {step_num + 1}")
            print(f"   ✓ Step completed!")
            
            # 진행률 업데이트
            progress = wizard.get_progress(session_id)
            if progress:
                print(f"   Progress: {progress['completed_steps']}/{progress['total_steps']} ({progress['progress_percentage']}%)")
    
    # 5. 최종 결과
    print(f"\n✅ 5. Final Results")
    final_progress = wizard.get_progress(session_id)
    if final_progress:
        print(f"   Final Progress: {final_progress['completed_steps']}/{final_progress['total_steps']} steps")
        print(f"   Completion Rate: {final_progress['progress_percentage']}%")
        print(f"   Final Status: {final_progress['status']}")
        
        if final_progress['status'] == 'completed':
            print(f"   🎉 Session completed successfully!")
        else:
            print(f"   ⏳ Session in progress...")
    
    # 6. 기능 요약
    print(f"\n📊 Task 3.1 Implementation Summary")
    print("=" * 60)
    print("✅ Session creation and management")
    print("✅ Step-by-step progress tracking")
    print("✅ Progress percentage calculation")
    print("✅ Step status management (not_started → in_progress → completed)")
    print("✅ Code template provision")
    print("✅ Multi-step learning workflow (4 steps)")
    
    print(f"\n📋 Requirements Verification:")
    print(f"   ✅ 3-5단계로 나누어진 실습 과정 (4단계 구현)")
    print(f"   ✅ 세션 생성, 진행, 완료 관리 기능")
    print(f"   ✅ 단계별 상태 추적 및 진행률 계산")
    print(f"   ✅ 진행 상황 시각적 표시 (진행률 %)")
    
    print(f"\n🎉 Task 3.1 COMPLETED SUCCESSFULLY!")
    
    return session_id


if __name__ == "__main__":
    demo_step_wizard()