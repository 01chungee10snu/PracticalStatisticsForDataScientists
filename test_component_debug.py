"""
컴포넌트 통합 디버그 테스트
"""

import sys
sys.path.append('modules')

from modules.integrated_learning_system import IntegratedLearningSystem

def debug_component_integration():
    """컴포넌트 통합 디버그"""
    system = IntegratedLearningSystem()
    session_id = system.create_learning_session("debug_test")
    
    # 문제가 되는 복합 코드 테스트
    complex_code = """
data = [10, 20, 30, 40, 50]
average = sum(data) / len(data)
variance = sum((x - average) ** 2 for x in data) / len(data)
std_dev = variance ** 0.5
print(f"평균: {average}, 표준편차: {std_dev:.2f}")
"""
    
    print("=== 복합 코드 실행 테스트 ===")
    print("코드:")
    print(complex_code)
    print()
    
    # 단계별 실행 확인
    result = system.execute_learning_step(session_id, complex_code)
    
    print("실행 결과:")
    print(f"- 실행 성공: {result['execution']['success']}")
    if not result['execution']['success']:
        print(f"- 오류: {result['execution']['error']}")
    else:
        print(f"- 출력: {result['execution']['output']}")
        print(f"- 변수: {result['execution']['variables']}")
    
    print(f"- 검증 성공: {result['practice']['verification']['success']}")
    if not result['practice']['verification']['success']:
        print(f"- 검증 메시지: {result['practice']['verification']['message']}")
    
    print(f"- 해석 존재: {result['interpretation'] is not None}")
    print(f"- 표준화 성공: {result['standardized']['success']}")
    
    # 더 간단한 코드로 테스트
    print("\n=== 간단한 코드 테스트 ===")
    simple_code = """
data = [10, 20, 30, 40, 50]
average = sum(data) / len(data)
print(f"평균: {average}")
"""
    
    simple_result = system.execute_learning_step(session_id, simple_code)
    print(f"간단한 코드 실행 성공: {simple_result['execution']['success']}")
    
    return result

if __name__ == "__main__":
    debug_component_integration()