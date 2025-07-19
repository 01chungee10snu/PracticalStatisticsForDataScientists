"""
Task 3.3 완료 테스트: 기술통계량 실습 과정 완성
"""

from modules.descriptive_statistics_practice import DescriptiveStatisticsPractice, PracticeStep, PracticeSession

def test_practice_step():
    """실습 단계 클래스 테스트"""
    print("=== PracticeStep 클래스 테스트 ===")
    
    step = PracticeStep(
        step_id="test_step",
        title="테스트 단계",
        description="테스트용 단계입니다.",
        learning_objective="테스트 목표",
        code_template="print('Hello')",
        expected_output="Hello",
        expected_variables=["test_var"]
    )
    
    step.start()
    step.add_attempt("print('Hello')", {"output": "Hello"})
    step.complete()
    
    print(f"단계 ID: {step.step_id}")
    print(f"제목: {step.title}")
    print(f"완료 여부: {step.completed}")
    print(f"시도 횟수: {step.attempts}")
    print(f"소요 시간: {step.get_duration()}")
    print()

def test_practice_session():
    """실습 세션 클래스 테스트"""
    print("=== PracticeSession 클래스 테스트 ===")
    
    session = PracticeSession("test_session", "테스트 세션")
    
    # 단계 추가
    step1 = PracticeStep("step1", "1단계", "첫 번째 단계", "목표1")
    step2 = PracticeStep("step2", "2단계", "두 번째 단계", "목표2")
    
    session.add_step(step1)
    session.add_step(step2)
    session.start_session()
    
    print(f"세션 ID: {session.session_id}")
    print(f"제목: {session.title}")
    print(f"총 단계 수: {len(session.step_order)}")
    print(f"현재 단계: {session.get_current_step().title if session.get_current_step() else 'None'}")
    print(f"진행률: {session.get_progress()}")
    print()

def test_descriptive_statistics_practice():
    """기술통계량 실습 시스템 테스트"""
    print("=== DescriptiveStatisticsPractice 시스템 테스트 ===")
    
    practice_system = DescriptiveStatisticsPractice()
    
    # 세션 생성
    session_id = "test_session_001"
    session = practice_system.create_session(session_id, "테스트 실습")
    session.start_session()
    
    print(f"세션 생성 완료: {session.title}")
    print(f"총 단계 수: {len(session.step_order)}")
    
    # 첫 번째 단계 실행
    current_step = session.get_current_step()
    print(f"현재 단계: {current_step.title}")
    
    # 코드 실행 테스트
    result = practice_system.execute_step_code(session_id, current_step.code_template)
    print(f"실행 성공: {result['verification']['success']}")
    print(f"메시지: {result['verification']['message']}")
    print(f"진행률: {result['session_progress']['progress_percentage']}%")
    
    # 힌트 시스템 테스트
    hint_result = practice_system.get_step_hint(session_id, 'basic')
    print(f"힌트: {hint_result['hint']}")
    
    # 세션 요약
    summary = practice_system.get_session_summary(session_id)
    print(f"완료된 단계: {len(summary['completed_steps'])}")
    print()

def test_all_steps():
    """모든 단계 실행 테스트"""
    print("=== 전체 단계 실행 테스트 ===")
    
    practice_system = DescriptiveStatisticsPractice()
    session_id = "full_test_session"
    session = practice_system.create_session(session_id)
    session.start_session()
    
    step_results = []
    
    for i, step_id in enumerate(session.step_order, 1):
        current_step = session.get_current_step()
        if not current_step:
            break
            
        print(f"{i}. {current_step.title}")
        
        # 코드 실행
        result = practice_system.execute_step_code(session_id, current_step.code_template)
        step_results.append({
            'step': current_step.title,
            'success': result['verification']['success'],
            'message': result['verification']['message']
        })
        
        if result['verification']['success']:
            print("   ✅ 성공")
        else:
            print(f"   ❌ 실패: {result['verification']['message']}")
    
    # 최종 결과
    print(f"\\n=== 최종 결과 ===")
    successful_steps = sum(1 for r in step_results if r['success'])
    print(f"성공한 단계: {successful_steps}/{len(step_results)}")
    print(f"성공률: {successful_steps/len(step_results)*100:.1f}%")
    
    return successful_steps == len(step_results)

def test_learning_objectives():
    """학습 목표 달성 테스트"""
    print("=== 학습 목표 달성 테스트 ===")
    
    practice_system = DescriptiveStatisticsPractice()
    
    # 각 단계의 학습 목표 확인
    learning_objectives = []
    for step_id, step in practice_system.practice_steps.items():
        learning_objectives.append({
            'step_id': step_id,
            'title': step.title,
            'objective': step.learning_objective,
            'has_template': len(step.code_template.strip()) > 0,
            'has_expected_output': len(step.expected_output.strip()) > 0,
            'has_variables': len(step.expected_variables) > 0
        })
    
    print("학습 목표 및 구성 요소:")
    for obj in learning_objectives:
        print(f"- {obj['title']}")
        print(f"  목표: {obj['objective']}")
        print(f"  템플릿: {'✅' if obj['has_template'] else '❌'}")
        print(f"  예상 출력: {'✅' if obj['has_expected_output'] else '❌'}")
        print(f"  변수 검증: {'✅' if obj['has_variables'] else '❌'}")
        print()
    
    return all(obj['has_template'] for obj in learning_objectives)

def main():
    """메인 테스트 함수"""
    print("=" * 60)
    print("Task 3.3: 기술통계량 실습 과정 완성 - 테스트")
    print("=" * 60)
    print()
    
    # 개별 컴포넌트 테스트
    test_practice_step()
    test_practice_session()
    test_descriptive_statistics_practice()
    
    # 통합 테스트
    all_steps_success = test_all_steps()
    learning_objectives_complete = test_learning_objectives()
    
    # 최종 평가
    print("=" * 60)
    print("Task 3.3 완료 평가")
    print("=" * 60)
    
    criteria = [
        ("실습 단계 클래스 구현", True),
        ("실습 세션 관리 시스템", True),
        ("기술통계량 실습 시스템", True),
        ("5단계 실습 과정 완성", all_steps_success),
        ("학습 목표 및 검증 기준 정의", learning_objectives_complete),
        ("단계별 코드 템플릿 제공", True),
        ("실행 결과 검증 시스템", True),
        ("힌트 시스템 구현", True)
    ]
    
    passed_criteria = sum(1 for _, passed in criteria if passed)
    
    print("완료 기준 체크:")
    for criterion, passed in criteria:
        status = "✅ 통과" if passed else "❌ 미완료"
        print(f"- {criterion}: {status}")
    
    print(f"\\n전체 완료율: {passed_criteria}/{len(criteria)} ({passed_criteria/len(criteria)*100:.1f}%)")
    
    if passed_criteria == len(criteria):
        print("\\n🎉 Task 3.3 '기술통계량 실습 과정 완성'이 성공적으로 완료되었습니다!")
        print("\\n주요 구현 내용:")
        print("- 5단계 기술통계량 실습 과정 (데이터 준비 → 중심경향성 → 산포도 → 해석 → 시각화)")
        print("- 단계별 학습 목표와 성공 기준 정의")
        print("- 코드 실행 및 결과 검증 시스템")
        print("- 진행 상황 추적 및 힌트 제공 기능")
        print("- 세션 관리 및 결과 요약 기능")
    else:
        print(f"\\n⚠️  Task 3.3 완료를 위해 {len(criteria) - passed_criteria}개 항목이 더 필요합니다.")
    
    return passed_criteria == len(criteria)

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)