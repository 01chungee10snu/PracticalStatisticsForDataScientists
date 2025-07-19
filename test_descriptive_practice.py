"""
기술통계량 실습 시스템 테스트
"""

from modules.descriptive_statistics_practice import DescriptiveStatisticsPractice

def test_single_step():
    """단일 단계 테스트"""
    practice_system = DescriptiveStatisticsPractice()
    
    # 세션 생성
    session_id = "test_session"
    session = practice_system.create_session(session_id)
    session.start_session()
    
    # 1단계 테스트
    print("=== 1단계 테스트 ===")
    step1_code = """# 학생 성적 데이터 준비
scores = [85, 90, 78, 92, 88, 76, 95, 89, 84, 91]

# 데이터 기본 정보 확인
print(f"데이터: {scores}")
print(f"데이터 개수: {len(scores)}")
print("데이터 타입: list")
"""
    
    result = practice_system.execute_step_code(session_id, step1_code)
    print("실행 결과:", result['execution'].get('output', ''))
    print("성공 여부:", result['verification']['success'])
    print("메시지:", result['verification']['message'])
    print()
    
    # 3단계 코드 직접 테스트
    print("=== 3단계 코드 직접 테스트 ===")
    step3_code = """# 데이터와 이전 계산 결과 준비
scores = [85, 90, 78, 92, 88, 76, 95, 89, 84, 91]
mean_value = sum(scores) / len(scores)

print(f"평균: {mean_value}")

# 분산 계산
variance = sum((x - mean_value) ** 2 for x in scores) / len(scores)

# 표준편차 계산
std_dev = variance ** 0.5

print(f"분산: {variance:.2f}")
print(f"표준편차: {std_dev:.2f}")

# 범위 계산
data_range = max(scores) - min(scores)
print(f"범위: {data_range}")
"""
    
    result = practice_system.code_executor.execute(step3_code)
    print("실행 결과:", result.get('output', ''))
    print("성공 여부:", result.get('success', False))
    print("오류:", result.get('error', '없음'))
    print("변수:", result.get('variables', {}))

if __name__ == "__main__":
    test_single_step()