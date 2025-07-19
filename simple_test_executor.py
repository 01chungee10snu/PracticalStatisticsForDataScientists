"""
SimplePythonExecutor 직접 테스트
"""

from modules.simple_demo import SimplePythonExecutor

executor = SimplePythonExecutor()

# 간단한 코드 테스트
code1 = """
scores = [1, 2, 3, 4, 5]
mean_value = sum(scores) / len(scores)
print(f"평균: {mean_value}")
"""

result1 = executor.execute(code1)
print("=== 테스트 1 ===")
print("성공:", result1.get('success'))
print("출력:", result1.get('output'))
print("오류:", result1.get('error'))
print("변수:", result1.get('variables'))
print()

# 더 복잡한 코드 테스트
code2 = """
scores = [85, 90, 78, 92, 88, 76, 95, 89, 84, 91]
mean_value = sum(scores) / len(scores)
variance = sum((x - mean_value) ** 2 for x in scores) / len(scores)
print(f"평균: {mean_value}")
print(f"분산: {variance}")
"""

result2 = executor.execute(code2)
print("=== 테스트 2 ===")
print("성공:", result2.get('success'))
print("출력:", result2.get('output'))
print("오류:", result2.get('error'))
print("변수:", result2.get('variables'))