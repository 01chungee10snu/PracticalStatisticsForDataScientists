"""
Integrated Result Interpretation System - Task 2.2 Complete
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from simple_demo import SimplePythonExecutor
from result_interpreter import ResultInterpreter
from typing import Dict, Any


class IntegratedCodeExecutor:
    """통합 코드 실행 및 해석 시스템"""
    
    def __init__(self):
        self.executor = SimplePythonExecutor()
        self.interpreter = ResultInterpreter()
    
    def execute_and_interpret(self, code: str, context: str = "general") -> Dict[str, Any]:
        """코드 실행 및 결과 해석"""
        # 1. 코드 실행
        execution_result = self.executor.execute(code)
        
        # 2. 결과 해석 (성공한 경우에만)
        if execution_result['success']:
            interpretation = self.interpreter.interpret_result(execution_result, context)
            
            # 통합 결과 생성
            integrated_result = {
                'execution': execution_result,
                'interpretation': interpretation,
                'has_interpretation': True,
                'context': context
            }
        else:
            # 실행 실패 시 오류 해석
            error_interpretation = self._interpret_error(execution_result)
            
            integrated_result = {
                'execution': execution_result,
                'error_interpretation': error_interpretation,
                'has_interpretation': False,
                'context': context
            }
        
        return integrated_result
    
    def _interpret_error(self, error_result: Dict[str, Any]) -> Dict[str, Any]:
        """오류 해석"""
        error_type = error_result.get('error_type', 'Unknown')
        error_message = error_result.get('error', '')
        
        # 일반적인 오류 패턴과 해결 방법
        error_solutions = {
            'NameError': {
                'meaning': '정의되지 않은 변수나 함수를 사용했습니다.',
                'solutions': [
                    '변수명의 철자를 확인하세요.',
                    '변수를 사용하기 전에 먼저 정의했는지 확인하세요.',
                    'import 문이 필요한 모듈인지 확인하세요.'
                ]
            },
            'SyntaxError': {
                'meaning': '파이썬 문법에 오류가 있습니다.',
                'solutions': [
                    '괄호, 대괄호, 중괄호가 올바르게 닫혔는지 확인하세요.',
                    '들여쓰기가 일관되게 되어 있는지 확인하세요.',
                    '콜론(:)이 필요한 곳에 있는지 확인하세요.'
                ]
            },
            'TypeError': {
                'meaning': '잘못된 데이터 타입을 사용했습니다.',
                'solutions': [
                    '변수의 데이터 타입을 확인하세요.',
                    '함수에 올바른 타입의 인수를 전달했는지 확인하세요.',
                    '타입 변환이 필요한지 확인하세요.'
                ]
            },
            'ValueError': {
                'meaning': '올바른 타입이지만 부적절한 값을 사용했습니다.',
                'solutions': [
                    '함수에 전달하는 값의 범위를 확인하세요.',
                    '문자열을 숫자로 변환할 때 형식을 확인하세요.',
                    '리스트나 문자열의 인덱스 범위를 확인하세요.'
                ]
            },
            'IndexError': {
                'meaning': '리스트나 문자열의 인덱스가 범위를 벗어났습니다.',
                'solutions': [
                    '리스트의 길이를 확인하세요.',
                    '인덱스가 0부터 시작한다는 점을 기억하세요.',
                    '음수 인덱스를 사용할 때 주의하세요.'
                ]
            }
        }
        
        solution_info = error_solutions.get(error_type, {
            'meaning': '예상치 못한 오류가 발생했습니다.',
            'solutions': [
                '코드를 다시 검토해보세요.',
                '오류 메시지를 자세히 읽어보세요.',
                '간단한 예제부터 시작해보세요.'
            ]
        })
        
        return {
            'error_type': error_type,
            'error_message': error_message,
            'meaning': solution_info['meaning'],
            'solutions': solution_info['solutions'],
            'general_tips': [
                '코드를 작은 부분으로 나누어 테스트해보세요.',
                'print() 문을 사용해 변수 값을 확인해보세요.',
                '온라인 문서나 예제를 참고하세요.'
            ]
        }
    
    def create_formatted_output(self, result: Dict[str, Any]) -> str:
        """포맷된 출력 생성"""
        output_lines = []
        
        # 실행 결과
        execution = result['execution']
        output_lines.append("🐍 코드 실행 결과")
        output_lines.append("=" * 50)
        
        if execution['success']:
            output_lines.append("✅ 실행 성공")
            output_lines.append(f"⏱️  실행 시간: {execution['execution_time']}초")
            output_lines.append(f"\n📤 출력:")
            output_lines.append(execution['output'])
            
            if execution.get('variables'):
                output_lines.append(f"\n📊 생성된 변수: {list(execution['variables'].keys())}")
            
            # 해석 결과
            if result['has_interpretation']:
                interpretation = result['interpretation']
                
                output_lines.append(f"\n🔍 결과 해석 ({result['context']} 맥락)")
                output_lines.append("-" * 50)
                
                # 통계적 의미
                stat_meanings = interpretation['statistical_analysis']['statistical_meaning']
                if stat_meanings:
                    output_lines.append("\n📈 통계적 의미:")
                    for meaning in stat_meanings[:3]:  # 상위 3개만 표시
                        output_lines.append(f"  • {meaning}")
                
                # 실무적 해석
                practical_insights = interpretation['practical_analysis']['practical_insights']
                if practical_insights:
                    output_lines.append(f"\n💡 실무적 해석:")
                    for insight in practical_insights:
                        output_lines.append(f"  • {insight}")
                
                # 권장사항
                recommendations = interpretation['practical_analysis']['actionable_recommendations']
                if recommendations:
                    output_lines.append(f"\n🎯 권장사항:")
                    for rec in recommendations:
                        output_lines.append(f"  • {rec}")
                
                # 다음 단계
                next_steps = interpretation['practical_analysis']['next_steps']
                if next_steps:
                    output_lines.append(f"\n🚀 다음 단계:")
                    for step in next_steps:
                        output_lines.append(f"  • {step}")
        
        else:
            # 오류 처리
            output_lines.append("❌ 실행 실패")
            output_lines.append(f"🚫 오류: {execution['error']}")
            
            if 'error_interpretation' in result:
                error_interp = result['error_interpretation']
                output_lines.append(f"\n🔍 오류 분석")
                output_lines.append("-" * 50)
                output_lines.append(f"📋 의미: {error_interp['meaning']}")
                
                output_lines.append(f"\n💡 해결 방법:")
                for solution in error_interp['solutions']:
                    output_lines.append(f"  • {solution}")
                
                output_lines.append(f"\n📚 일반적인 팁:")
                for tip in error_interp['general_tips']:
                    output_lines.append(f"  • {tip}")
        
        return '\n'.join(output_lines)


def demo_integrated_system():
    """통합 시스템 데모"""
    print("🚀 Task 2.2: 통합 결과 해석 시스템 데모")
    print("=" * 60)
    
    system = IntegratedCodeExecutor()
    
    # 데모 케이스들
    demo_cases = [
        {
            'title': '성공적인 통계 분석 (교육 맥락)',
            'code': '''
# 학생 성적 분석
scores = [78, 85, 92, 88, 76, 94, 89, 83, 91, 87]

# 기본 통계량 계산
total = sum(scores)
count = len(scores)
mean_score = total / count

# 최고점, 최저점
highest = scores[0]
lowest = scores[0]
for score in scores:
    if score > highest:
        highest = score
    if score < lowest:
        lowest = score

print("=== 학급 성적 분석 ===")
print(f"학생 수: {count}명")
print(f"총점: {total}점")
print(f"평균 점수: {mean_score:.1f}점")
print(f"최고점: {highest}점")
print(f"최저점: {lowest}점")
print(f"점수 범위: {highest - lowest}점")
''',
            'context': 'education'
        },
        {
            'title': '비즈니스 데이터 분석',
            'code': '''
# 월별 매출 데이터 분석
monthly_sales = [120, 135, 128, 142, 156, 148, 162, 139, 145, 158, 171, 163]

total_sales = sum(monthly_sales)
avg_monthly = total_sales / len(monthly_sales)
growth_rate = (monthly_sales[-1] - monthly_sales[0]) / monthly_sales[0] * 100

print("=== 연간 매출 분석 ===")
print(f"총 매출: {total_sales:,}만원")
print(f"월평균 매출: {avg_monthly:.1f}만원")
print(f"연간 성장률: {growth_rate:.1f}%")
print(f"최고 매출 월: {max(monthly_sales)}만원")
print(f"최저 매출 월: {min(monthly_sales)}만원")
''',
            'context': 'business'
        },
        {
            'title': '오류가 있는 코드 (오류 해석 테스트)',
            'code': '''
# 의도적 오류 - 정의되지 않은 변수 사용
data = [1, 2, 3, 4, 5]
result = undefined_variable + sum(data)
print(f"결과: {result}")
''',
            'context': 'general'
        }
    ]
    
    # 각 데모 케이스 실행
    for i, case in enumerate(demo_cases, 1):
        print(f"\n📝 데모 {i}: {case['title']}")
        print("=" * 60)
        
        result = system.execute_and_interpret(case['code'], case['context'])
        formatted_output = system.create_formatted_output(result)
        
        print(formatted_output)
        
        if i < len(demo_cases):
            print(f"\n{'='*60}")
    
    print(f"\n🎉 Task 2.2 완료!")
    print("✅ 통계적 의미와 실무적 해석 자동 생성")
    print("✅ 맥락에 맞는 해석 가이드 제공")
    print("✅ 명확한 오류 메시지와 해결 방법 제시")


if __name__ == "__main__":
    demo_integrated_system()