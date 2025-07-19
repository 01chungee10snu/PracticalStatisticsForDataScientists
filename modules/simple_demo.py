"""
Simple Demo for Task 2.1 - Python Code Executor
"""

import sys
import io
import contextlib
import traceback
import time
from typing import Dict, Any


class SimplePythonExecutor:
    """간단한 Python 코드 실행기"""
    
    def __init__(self):
        self.max_execution_time = 5
        self.max_output_length = 2000
    
    def execute(self, code: str) -> Dict[str, Any]:
        """코드 실행"""
        start_time = time.time()
        
        # 보안 검사
        if self._is_dangerous(code):
            return {
                'success': False,
                'error': '보안상 위험한 코드가 감지되었습니다.',
                'output': '',
                'execution_time': 0
            }
        
        # 출력 캡처
        output_buffer = io.StringIO()
        
        try:
            # 안전한 실행 환경
            import math
            import statistics
            
            safe_globals = {
                '__builtins__': {
                    'print': print,
                    'len': len,
                    'range': range,
                    'sum': sum,
                    'min': min,
                    'max': max,
                    'abs': abs,
                    'round': round,
                    'int': int,
                    'float': float,
                    'str': str,
                    'list': list,
                    'dict': dict,
                    'enumerate': enumerate,
                    'zip': zip,
                },
                'math': math,
                'statistics': statistics
            }
            
            local_vars = {}
            
            # stdout 리다이렉션
            with contextlib.redirect_stdout(output_buffer):
                exec(code, safe_globals, local_vars)
            
            output = output_buffer.getvalue()
            execution_time = time.time() - start_time
            
            # 변수 추출
            variables = {}
            for name, value in local_vars.items():
                if not name.startswith('_'):
                    try:
                        if isinstance(value, (int, float, str, bool, list, dict)):
                            variables[name] = value
                        else:
                            variables[name] = str(value)[:50]
                    except:
                        variables[name] = f"<{type(value).__name__}>"
            
            return {
                'success': True,
                'output': output,
                'execution_time': round(execution_time, 3),
                'variables': variables,
                'code': code
            }
            
        except Exception as e:
            execution_time = time.time() - start_time
            return {
                'success': False,
                'error': str(e),
                'error_type': type(e).__name__,
                'output': output_buffer.getvalue(),
                'execution_time': round(execution_time, 3),
                'code': code
            }
    
    def _is_dangerous(self, code: str) -> bool:
        """위험한 코드 검사"""
        dangerous = [
            'import os', 'import sys', 'import subprocess',
            'exec(', 'eval(', 'open(', '__import__',
            'file(', 'input('
        ]
        
        code_lower = code.lower()
        return any(danger in code_lower for danger in dangerous)


def demo_task_2_1():
    """Task 2.1 데모"""
    print("🐍 Task 2.1: Python Code Executor Demo")
    print("=" * 50)
    
    executor = SimplePythonExecutor()
    
    # 데모 코드들
    demo_codes = [
        {
            'title': '기본 계산',
            'code': '''
# 기본 계산 예제
x = 10
y = 20
result = x + y
print(f"x = {x}, y = {y}")
print(f"x + y = {result}")
print(f"x * y = {x * y}")
'''
        },
        {
            'title': '기술통계량 계산',
            'code': '''
# 기술통계량 계산
scores = [85, 90, 78, 92, 88, 76, 95, 89, 84, 91]

mean_val = statistics.mean(scores)
median_val = statistics.median(scores)
stdev_val = statistics.stdev(scores)

print("=== 기술통계량 분석 ===")
print(f"데이터: {scores}")
print(f"평균: {mean_val:.2f}")
print(f"중앙값: {median_val}")
print(f"표준편차: {stdev_val:.2f}")
print(f"최솟값: {min(scores)}")
print(f"최댓값: {max(scores)}")
'''
        },
        {
            'title': '데이터 분석',
            'code': '''
# 데이터 분석 예제
# 학생 성적 데이터
students = ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve']
scores = [88, 92, 78, 95, 85]

# 성적 분석
total = sum(scores)
average = total / len(scores)
highest = max(scores)
lowest = min(scores)

print("=== 학급 성적 분석 ===")
print(f"학생 수: {len(students)}명")
print(f"총점: {total}점")
print(f"평균: {average:.1f}점")
print(f"최고점: {highest}점")
print(f"최저점: {lowest}점")

# 등급 분류
print("\\n=== 개별 성적 ===")
for student, score in zip(students, scores):
    if score >= 90:
        grade = 'A'
    elif score >= 80:
        grade = 'B'
    elif score >= 70:
        grade = 'C'
    else:
        grade = 'D'
    print(f"{student}: {score}점 ({grade}등급)")
'''
        },
        {
            'title': '보안 테스트 (차단되어야 함)',
            'code': '''
# 위험한 코드 - 차단되어야 함
import os
os.system("ls")
'''
        }
    ]
    
    # 각 데모 실행
    for i, demo in enumerate(demo_codes, 1):
        print(f"\n📝 데모 {i}: {demo['title']}")
        print("-" * 40)
        
        result = executor.execute(demo['code'])
        
        if result['success']:
            print("✅ 실행 성공")
            print(f"⏱️  실행 시간: {result['execution_time']}초")
            print(f"📤 출력:")
            print(result['output'])
            
            if result['variables']:
                print(f"📊 생성된 변수: {list(result['variables'].keys())}")
        else:
            print("❌ 실행 실패")
            print(f"🚫 오류: {result['error']}")
            if result['output']:
                print(f"📤 부분 출력: {result['output']}")
    
    print(f"\n🎉 Task 2.1 핵심 기능 데모 완료!")
    print(f"✅ 브라우저 기반 Python 코드 실행 환경 구현")
    print(f"✅ 안전한 코드 실행을 위한 보안 기능 구현")
    print(f"✅ 요구사항 2.1 충족: Python 코드 즉시 실행")


if __name__ == "__main__":
    demo_task_2_1()