"""
통합 결과 해석 시스템 데모
인라인 코드 실행기와 결과 해석 가이드의 통합 예시
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import pandas as pd
from modules.result_interpretation_system import (
    ResultInterpretationSystem,
    ConceptType,
    create_statistical_result,
    create_expected_result,
    interpret_pandas_describe,
    interpret_correlation
)
# Mock InlineCodeRunner for demo purposes
class MockExecutionResult:
    def __init__(self, success, output, result, error=None):
        self.success = success
        self.output = output
        self.result = result
        self.error = error

class InlineCodeRunner:
    def execute_code(self, code):
        """Mock code execution for demo"""
        try:
            # Create a safe execution environment
            exec_globals = {
                'np': np, 'pd': pd, 'stats': __import__('scipy.stats', fromlist=['stats'])
            }
            exec_locals = {}
            
            # Execute the code
            exec(code, exec_globals, exec_locals)
            
            # Get the result (last expression or 'result' variable)
            result = exec_locals.get('result', None)
            
            # Capture output (simplified)
            output = "Code executed successfully"
            
            return MockExecutionResult(True, output, result)
        except Exception as e:
            return MockExecutionResult(False, "", None, str(e))


class IntegratedPracticeWithInterpretation:
    """실습과 해석이 통합된 시스템"""
    
    def __init__(self):
        self.code_runner = InlineCodeRunner()
        self.interpreter = ResultInterpretationSystem()
    
    def execute_with_interpretation(self, code: str, concept_type: ConceptType = None,
                                  expected_result=None, context: dict = None):
        """코드 실행과 동시에 결과 해석 제공"""
        print("🔧 코드 실행 중...")
        print(f"```python\n{code}\n```")
        print()
        
        # 코드 실행
        execution_result = self.code_runner.execute_code(code)
        
        if execution_result.success:
            print("✅ 실행 성공!")
            print("📊 실행 결과:")
            print(execution_result.output)
            print()
            
            # 결과 해석 (결과가 해석 가능한 형태인 경우)
            if self._is_interpretable_result(execution_result.result):
                print("🧠 AI 해석:")
                interpretation = self._interpret_execution_result(
                    execution_result, code, concept_type, expected_result, context
                )
                self._display_interpretation(interpretation)
            else:
                print("ℹ️  이 결과는 자동 해석이 어려운 형태입니다.")
        else:
            print("❌ 실행 실패:")
            print(execution_result.error)
    
    def _is_interpretable_result(self, result):
        """결과가 해석 가능한지 확인"""
        if result is None:
            return False
        
        # pandas Series/DataFrame의 describe() 결과
        if hasattr(result, 'describe') or (hasattr(result, 'index') and 'mean' in str(result.index)):
            return True
        
        # 상관계수 행렬
        if isinstance(result, (np.ndarray, pd.DataFrame)) and hasattr(result, 'shape'):
            return True
        
        # 단일 상관계수 값
        if isinstance(result, (int, float)):
            return True
        
        return False
    
    def _interpret_execution_result(self, execution_result, code, concept_type, expected_result, context):
        """실행 결과 해석"""
        result = execution_result.result
        
        # pandas describe 결과 처리
        if hasattr(result, 'describe') or (hasattr(result, 'index') and 'mean' in str(result.index)):
            return interpret_pandas_describe(result)
        
        # 상관관계 결과 처리
        elif 'corr' in code.lower() or (isinstance(result, (int, float)) and -1 <= result <= 1):
            return interpret_correlation(result, context)
        
        # 일반적인 통계 결과 처리
        else:
            if concept_type is None:
                concept_type = ConceptType.DESCRIPTIVE_STATS
            
            # 결과를 딕셔너리 형태로 변환
            if isinstance(result, (pd.Series, pd.DataFrame)):
                values = result.to_dict() if hasattr(result, 'to_dict') else {"result": str(result)}
            elif isinstance(result, (int, float)):
                values = {"value": result}
            else:
                values = {"result": str(result)}
            
            stat_result = create_statistical_result(concept_type, values, context or {})
            return self.interpreter.interpret_result(stat_result, code, expected_result)
    
    def _display_interpretation(self, interpretation):
        """해석 결과 표시"""
        print("=" * 60)
        print("📖 개념 설명:")
        print(interpretation.concept_explanation)
        print()
        
        print("📊 통계량 의미:")
        print(interpretation.statistical_meaning)
        print()
        
        print("💼 실무적 해석:")
        print(interpretation.practical_interpretation)
        print()
        
        if interpretation.comparison_analysis:
            print("🔍 비교 분석:")
            print(interpretation.comparison_analysis)
            print()
        
        print(f"🎯 해석 신뢰도: {interpretation.confidence_level:.0%}")
        print()
        
        print("💡 추천사항:")
        for i, rec in enumerate(interpretation.recommendations, 1):
            print(f"  {i}. {rec}")
        print("=" * 60)


def demo_basic_statistics():
    """기본 통계량 분석 데모"""
    print("🎓 실습 1: 기본 통계량 분석")
    print("=" * 50)
    
    system = IntegratedPracticeWithInterpretation()
    
    code = """
# 학생들의 시험 점수 데이터
import numpy as np
import pandas as pd

np.random.seed(42)
scores = np.random.normal(75, 12, 100)  # 평균 75, 표준편차 12
scores = np.clip(scores, 0, 100)  # 0-100 범위로 제한

df = pd.DataFrame({'score': scores})
result = df['score'].describe()
print("기술통계량:")
print(result)
result
"""
    
    expected = create_expected_result(
        concept_type=ConceptType.DESCRIPTIVE_STATS,
        expected_values={"mean": 75.0, "std": 12.0},
        acceptable_ranges={"mean": (70.0, 80.0), "std": (10.0, 15.0)},
        explanation="평균 75점, 표준편차 12점 정도를 예상"
    )
    
    system.execute_with_interpretation(
        code, 
        ConceptType.DESCRIPTIVE_STATS, 
        expected,
        {"subject": "수학 시험", "class_size": 100}
    )


def demo_correlation_analysis():
    """상관관계 분석 데모"""
    print("\n🎓 실습 2: 상관관계 분석")
    print("=" * 50)
    
    system = IntegratedPracticeWithInterpretation()
    
    code = """
# 공부 시간과 시험 점수의 관계
import numpy as np
import pandas as pd

np.random.seed(123)
study_hours = np.random.uniform(1, 10, 50)
# 공부 시간이 많을수록 점수가 높아지는 관계 + 노이즈
test_scores = 60 + 3 * study_hours + np.random.normal(0, 5, 50)
test_scores = np.clip(test_scores, 0, 100)

df = pd.DataFrame({
    'study_hours': study_hours,
    'test_score': test_scores
})

correlation = df['study_hours'].corr(df['test_score'])
print(f"상관계수: {correlation:.3f}")
correlation
"""
    
    system.execute_with_interpretation(
        code,
        ConceptType.CORRELATION,
        context={
            "variables": ["공부 시간", "시험 점수"],
            "business_context": "학습 효과 분석을 통한 교육 방법 개선"
        }
    )


def demo_hypothesis_testing():
    """가설검정 데모"""
    print("\n🎓 실습 3: 가설검정 분석")
    print("=" * 50)
    
    system = IntegratedPracticeWithInterpretation()
    
    code = """
# 두 교육 방법의 효과 비교
import numpy as np
from scipy import stats

np.random.seed(456)
# 기존 방법으로 교육받은 학생들의 점수
traditional_scores = np.random.normal(70, 10, 30)
# 새로운 방법으로 교육받은 학생들의 점수  
new_method_scores = np.random.normal(75, 10, 30)

# 독립표본 t검정
t_stat, p_value = stats.ttest_ind(traditional_scores, new_method_scores)

print(f"t-통계량: {t_stat:.3f}")
print(f"p-값: {p_value:.3f}")
print(f"기존 방법 평균: {traditional_scores.mean():.2f}")
print(f"새 방법 평균: {new_method_scores.mean():.2f}")

# 결과를 딕셔너리로 반환
result = {
    'statistic': t_stat,
    'p_value': p_value,
    'traditional_mean': traditional_scores.mean(),
    'new_method_mean': new_method_scores.mean()
}
result
"""
    
    # 이 경우는 직접 해석 시스템을 사용
    execution_result = system.code_runner.execute_code(code)
    
    if execution_result.success:
        print("✅ 실행 성공!")
        print("📊 실행 결과:")
        print(execution_result.output)
        print()
        
        # 수동으로 결과 해석
        result_dict = execution_result.result
        stat_result = create_statistical_result(
            concept_type=ConceptType.HYPOTHESIS_TEST,
            values={
                'statistic': result_dict['statistic'],
                'p_value': result_dict['p_value']
            },
            context={
                'test_type': '독립표본 t검정',
                'hypothesis': '새로운 교육 방법이 더 효과적이다',
                'groups': ['기존 방법', '새로운 방법']
            }
        )
        
        expected = create_expected_result(
            concept_type=ConceptType.HYPOTHESIS_TEST,
            expected_values={'p_value': 0.05},
            acceptable_ranges={'p_value': (0.0, 0.1)},
            explanation="유의수준 0.05에서 통계적 차이 검증"
        )
        
        interpretation = system.interpreter.interpret_result(stat_result, code, expected)
        system._display_interpretation(interpretation)


def main():
    """모든 데모 실행"""
    print("🚀 통합 결과 해석 시스템 데모")
    print("=" * 60)
    print("이 데모는 코드 실행과 동시에 AI가 결과를 해석해주는 시스템을 보여줍니다.")
    print("실제 교육 환경에서 학습자가 코드를 실행하면 즉시 전문가 수준의 해석을 받을 수 있습니다.")
    print()
    
    demo_basic_statistics()
    demo_correlation_analysis()
    demo_hypothesis_testing()
    
    print("\n✨ 데모 완료!")
    print("이 시스템을 통해 학습자는:")
    print("1. 코드 실행 결과를 즉시 확인할 수 있습니다")
    print("2. 통계량의 의미를 자동으로 해석받을 수 있습니다")
    print("3. 실무적 관점에서의 해석을 제공받을 수 있습니다")
    print("4. 예상 결과와의 비교를 통해 학습 효과를 높일 수 있습니다")


if __name__ == "__main__":
    main()