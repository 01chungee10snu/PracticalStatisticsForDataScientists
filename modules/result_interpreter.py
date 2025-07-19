"""
Result Interpretation System - Statistical and Practical Analysis
"""

import re
import statistics
from typing import Dict, Any, List, Optional, Tuple
import math


class StatisticalInterpreter:
    """통계적 결과 해석기"""
    
    def __init__(self):
        self.interpretation_rules = {
            'mean': self._interpret_mean,
            'median': self._interpret_median,
            'mode': self._interpret_mode,
            'std': self._interpret_std,
            'variance': self._interpret_variance,
            'correlation': self._interpret_correlation,
            'distribution': self._interpret_distribution
        }
    
    def interpret_statistical_result(self, result: Dict[str, Any], context: str = "general") -> Dict[str, Any]:
        """통계적 결과 해석"""
        interpretation = {
            'statistical_meaning': [],
            'practical_interpretation': [],
            'recommendations': [],
            'context': context,
            'confidence_level': 'medium'
        }
        
        # 변수에서 통계량 추출
        variables = result.get('variables', {})
        output = result.get('output', '')
        
        # 통계량 식별 및 해석
        stats_found = self._identify_statistics(variables, output)
        
        for stat_type, values in stats_found.items():
            if stat_type in self.interpretation_rules:
                stat_interpretation = self.interpretation_rules[stat_type](values, context)
                interpretation['statistical_meaning'].extend(stat_interpretation['meaning'])
                interpretation['practical_interpretation'].extend(stat_interpretation['practical'])
                interpretation['recommendations'].extend(stat_interpretation['recommendations'])
        
        # 전체적인 해석 추가
        if stats_found:
            interpretation['statistical_meaning'].append(
                "계산된 통계량들은 데이터의 중심경향성과 산포도를 나타냅니다."
            )
            interpretation['practical_interpretation'].append(
                "이러한 통계량들을 통해 데이터의 전체적인 패턴과 특성을 파악할 수 있습니다."
            )
        
        return interpretation
    
    def _identify_statistics(self, variables: Dict[str, Any], output: str) -> Dict[str, List[Any]]:
        """통계량 식별"""
        stats_found = {}
        
        # 변수명에서 통계량 식별
        for var_name, value in variables.items():
            var_lower = var_name.lower()
            
            if 'mean' in var_lower or 'average' in var_lower:
                stats_found.setdefault('mean', []).append(value)
            elif 'median' in var_lower:
                stats_found.setdefault('median', []).append(value)
            elif 'mode' in var_lower:
                stats_found.setdefault('mode', []).append(value)
            elif 'std' in var_lower or 'stdev' in var_lower:
                stats_found.setdefault('std', []).append(value)
            elif 'var' in var_lower and 'variance' in var_lower:
                stats_found.setdefault('variance', []).append(value)
        
        # 출력에서 통계량 패턴 식별
        output_patterns = {
            r'평균[:\s]*([0-9.]+)': 'mean',
            r'중앙값[:\s]*([0-9.]+)': 'median',
            r'표준편차[:\s]*([0-9.]+)': 'std',
            r'분산[:\s]*([0-9.]+)': 'variance'
        }
        
        for pattern, stat_type in output_patterns.items():
            matches = re.findall(pattern, output)
            if matches:
                stats_found.setdefault(stat_type, []).extend([float(m) for m in matches])
        
        return stats_found
    
    def _interpret_mean(self, values: List[Any], context: str) -> Dict[str, List[str]]:
        """평균 해석"""
        if not values:
            return {'meaning': [], 'practical': [], 'recommendations': []}
        
        mean_val = values[0] if isinstance(values[0], (int, float)) else 0
        
        return {
            'meaning': [
                f"평균값 {mean_val:.2f}는 데이터의 중심경향성을 나타냅니다.",
                "평균은 모든 데이터 값들의 합을 데이터 개수로 나눈 값입니다."
            ],
            'practical': [
                "평균은 데이터의 전체적인 수준을 파악하는 데 유용합니다.",
                "하지만 이상치(outlier)의 영향을 받을 수 있으므로 중앙값과 함께 고려해야 합니다."
            ],
            'recommendations': [
                "데이터의 분포를 확인하기 위해 히스토그램을 그려보세요.",
                "이상치가 있는지 확인하고, 있다면 중앙값도 함께 고려하세요."
            ]
        }
    
    def _interpret_median(self, values: List[Any], context: str) -> Dict[str, List[str]]:
        """중앙값 해석"""
        if not values:
            return {'meaning': [], 'practical': [], 'recommendations': []}
        
        median_val = values[0] if isinstance(values[0], (int, float)) else 0
        
        return {
            'meaning': [
                f"중앙값 {median_val:.2f}는 데이터를 크기 순으로 정렬했을 때 가운데 위치한 값입니다.",
                "중앙값은 이상치의 영향을 받지 않는 강건한(robust) 통계량입니다."
            ],
            'practical': [
                "중앙값은 데이터에 극값이 있을 때 평균보다 더 대표적인 값을 제공합니다.",
                "소득, 부동산 가격 등 왜곡된 분포를 가진 데이터에서 특히 유용합니다."
            ],
            'recommendations': [
                "평균과 중앙값을 비교하여 데이터의 치우침(skewness)을 파악하세요.",
                "평균 > 중앙값이면 오른쪽 치우침, 평균 < 중앙값이면 왼쪽 치우침입니다."
            ]
        }
    
    def _interpret_mode(self, values: List[Any], context: str) -> Dict[str, List[str]]:
        """최빈값 해석"""
        return {
            'meaning': [
                "최빈값은 데이터에서 가장 자주 나타나는 값입니다.",
                "범주형 데이터의 중심경향성을 나타내는 유일한 측도입니다."
            ],
            'practical': [
                "최빈값은 가장 일반적이거나 전형적인 값을 나타냅니다.",
                "마케팅, 품질관리 등에서 가장 흔한 패턴을 파악하는 데 유용합니다."
            ],
            'recommendations': [
                "데이터에 여러 개의 최빈값이 있는지 확인하세요(다봉분포).",
                "최빈값이 없는 경우도 있으니 데이터의 특성을 고려하세요."
            ]
        }
    
    def _interpret_std(self, values: List[Any], context: str) -> Dict[str, List[str]]:
        """표준편차 해석"""
        if not values:
            return {'meaning': [], 'practical': [], 'recommendations': []}
        
        std_val = values[0] if isinstance(values[0], (int, float)) else 0
        
        return {
            'meaning': [
                f"표준편차 {std_val:.2f}는 데이터가 평균으로부터 얼마나 퍼져있는지를 나타냅니다.",
                "표준편차가 클수록 데이터의 변동성이 크고, 작을수록 데이터가 평균 주변에 집중되어 있습니다."
            ],
            'practical': [
                "표준편차는 데이터의 일관성과 예측가능성을 평가하는 데 중요합니다.",
                "품질관리, 위험관리, 성과평가 등에서 변동성 측정에 활용됩니다."
            ],
            'recommendations': [
                "표준편차를 평균과 함께 고려하여 변동계수(CV)를 계산해보세요.",
                "정규분포에서는 평균 ± 1표준편차 범위에 약 68%의 데이터가 포함됩니다."
            ]
        }
    
    def _interpret_variance(self, values: List[Any], context: str) -> Dict[str, List[str]]:
        """분산 해석"""
        if not values:
            return {'meaning': [], 'practical': [], 'recommendations': []}
        
        var_val = values[0] if isinstance(values[0], (int, float)) else 0
        
        return {
            'meaning': [
                f"분산 {var_val:.2f}는 표준편차의 제곱으로, 데이터의 산포도를 나타냅니다.",
                "분산은 편차 제곱의 평균으로 계산되어 항상 0 이상의 값을 가집니다."
            ],
            'practical': [
                "분산은 포트폴리오 이론, 품질관리 등에서 위험도 측정에 사용됩니다.",
                "단위가 원래 데이터의 제곱이므로 해석 시 표준편차를 함께 고려하세요."
            ],
            'recommendations': [
                "분산의 제곱근인 표준편차가 해석하기 더 쉽습니다.",
                "여러 그룹의 변동성을 비교할 때 분산을 사용하세요."
            ]
        }
    
    def _interpret_correlation(self, values: List[Any], context: str) -> Dict[str, List[str]]:
        """상관관계 해석"""
        return {
            'meaning': [
                "상관계수는 두 변수 간의 선형 관계의 강도와 방향을 나타냅니다.",
                "상관계수는 -1과 1 사이의 값을 가지며, 0에 가까울수록 관계가 약합니다."
            ],
            'practical': [
                "상관관계가 있다고 해서 인과관계가 있는 것은 아닙니다.",
                "상관계수의 절댓값이 0.7 이상이면 강한 관계로 해석할 수 있습니다."
            ],
            'recommendations': [
                "산점도를 그려서 관계의 형태를 시각적으로 확인하세요.",
                "이상치가 상관계수에 미치는 영향을 확인하세요."
            ]
        }
    
    def _interpret_distribution(self, values: List[Any], context: str) -> Dict[str, List[str]]:
        """분포 해석"""
        return {
            'meaning': [
                "데이터의 분포는 값들이 어떻게 퍼져있는지를 보여줍니다.",
                "분포의 형태는 데이터의 특성과 적절한 분석 방법을 결정하는 데 중요합니다."
            ],
            'practical': [
                "정규분포는 많은 통계적 방법의 기본 가정입니다.",
                "치우친 분포는 평균보다 중앙값이 더 적절한 대표값일 수 있습니다."
            ],
            'recommendations': [
                "히스토그램이나 상자그림을 통해 분포의 형태를 확인하세요.",
                "정규성 검정을 통해 정규분포 가정을 확인하세요."
            ]
        }


class PracticalInterpreter:
    """실무적 해석기"""
    
    def __init__(self):
        self.context_interpreters = {
            'education': self._interpret_education_context,
            'business': self._interpret_business_context,
            'research': self._interpret_research_context,
            'quality': self._interpret_quality_context,
            'general': self._interpret_general_context
        }
    
    def interpret_practical_meaning(self, result: Dict[str, Any], context: str = "general") -> Dict[str, Any]:
        """실무적 의미 해석"""
        if context in self.context_interpreters:
            return self.context_interpreters[context](result)
        else:
            return self.context_interpreters['general'](result)
    
    def _interpret_education_context(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """교육 맥락 해석"""
        variables = result.get('variables', {})
        
        interpretation = {
            'context': 'education',
            'practical_insights': [],
            'actionable_recommendations': [],
            'next_steps': []
        }
        
        # 성적 관련 해석
        if any('score' in str(k).lower() or 'grade' in str(k).lower() for k in variables.keys()):
            interpretation['practical_insights'].extend([
                "학생 성적 데이터 분석을 통해 학습 성과를 평가할 수 있습니다.",
                "평균 점수는 전체 학급의 학습 수준을 나타냅니다.",
                "표준편차는 학생들 간의 성취도 차이를 보여줍니다."
            ])
            
            interpretation['actionable_recommendations'].extend([
                "평균보다 낮은 점수의 학생들에게 추가 지원을 제공하세요.",
                "표준편차가 크다면 개별화된 학습 전략이 필요합니다.",
                "상위 성취 학생들을 위한 심화 과정을 고려하세요."
            ])
        
        interpretation['next_steps'].extend([
            "학습 목표 달성도를 평가하세요.",
            "개별 학생의 학습 진도를 추적하세요.",
            "교수법 개선을 위한 데이터를 수집하세요."
        ])
        
        return interpretation
    
    def _interpret_business_context(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """비즈니스 맥락 해석"""
        return {
            'context': 'business',
            'practical_insights': [
                "비즈니스 데이터 분석을 통해 성과 지표를 모니터링할 수 있습니다.",
                "평균값은 전체적인 성과 수준을 나타냅니다.",
                "변동성은 비즈니스 위험도와 안정성을 평가하는 지표입니다."
            ],
            'actionable_recommendations': [
                "목표 대비 실제 성과를 비교 분석하세요.",
                "변동성이 큰 지표는 리스크 관리가 필요합니다.",
                "트렌드 분석을 통해 미래 예측을 수행하세요."
            ],
            'next_steps': [
                "KPI 대시보드를 구성하세요.",
                "정기적인 성과 리뷰를 실시하세요.",
                "데이터 기반 의사결정 프로세스를 구축하세요."
            ]
        }
    
    def _interpret_research_context(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """연구 맥락 해석"""
        return {
            'context': 'research',
            'practical_insights': [
                "연구 데이터의 기술통계량은 표본의 특성을 요약합니다.",
                "중심경향성과 산포도는 데이터의 분포 특성을 나타냅니다.",
                "이러한 통계량은 추후 추론통계의 기초가 됩니다."
            ],
            'actionable_recommendations': [
                "표본의 대표성을 확인하세요.",
                "가설 검정을 위한 적절한 통계 방법을 선택하세요.",
                "효과 크기(effect size)를 함께 보고하세요."
            ],
            'next_steps': [
                "연구 가설에 따른 통계 검정을 수행하세요.",
                "결과의 실질적 유의성을 평가하세요.",
                "연구 결과를 학술적으로 해석하세요."
            ]
        }
    
    def _interpret_quality_context(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """품질관리 맥락 해석"""
        return {
            'context': 'quality',
            'practical_insights': [
                "품질 데이터의 통계량은 공정의 안정성을 나타냅니다.",
                "평균은 공정의 중심값을, 표준편차는 변동성을 보여줍니다.",
                "관리한계를 벗어나는 값들은 특별한 원인이 있을 수 있습니다."
            ],
            'actionable_recommendations': [
                "관리도를 작성하여 공정을 모니터링하세요.",
                "규격 한계와 비교하여 불량률을 계산하세요.",
                "공정 능력 지수(Cp, Cpk)를 계산하세요."
            ],
            'next_steps': [
                "공정 개선 활동을 계획하세요.",
                "품질 목표를 설정하고 추적하세요.",
                "지속적인 개선 활동을 실시하세요."
            ]
        }
    
    def _interpret_general_context(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """일반적 맥락 해석"""
        return {
            'context': 'general',
            'practical_insights': [
                "기술통계량은 데이터의 기본적인 특성을 요약합니다.",
                "이러한 통계량들을 통해 데이터의 패턴과 특징을 파악할 수 있습니다.",
                "추가적인 분석을 위한 기초 정보를 제공합니다."
            ],
            'actionable_recommendations': [
                "데이터의 품질을 확인하세요.",
                "시각화를 통해 패턴을 확인하세요.",
                "목적에 맞는 추가 분석을 계획하세요."
            ],
            'next_steps': [
                "분석 목적을 명확히 하세요.",
                "적절한 통계 방법을 선택하세요.",
                "결과를 이해관계자에게 전달하세요."
            ]
        }


class ResultInterpreter:
    """통합 결과 해석 시스템"""
    
    def __init__(self):
        self.statistical_interpreter = StatisticalInterpreter()
        self.practical_interpreter = PracticalInterpreter()
    
    def interpret_result(self, result: Dict[str, Any], context: str = "general") -> Dict[str, Any]:
        """결과 종합 해석"""
        # 통계적 해석
        statistical_interpretation = self.statistical_interpreter.interpret_statistical_result(result, context)
        
        # 실무적 해석
        practical_interpretation = self.practical_interpreter.interpret_practical_meaning(result, context)
        
        # 종합 해석
        comprehensive_interpretation = {
            'execution_result': result,
            'statistical_analysis': statistical_interpretation,
            'practical_analysis': practical_interpretation,
            'summary': self._generate_summary(statistical_interpretation, practical_interpretation),
            'context': context,
            'timestamp': self._get_timestamp()
        }
        
        return comprehensive_interpretation
    
    def _generate_summary(self, statistical: Dict[str, Any], practical: Dict[str, Any]) -> Dict[str, str]:
        """요약 생성"""
        return {
            'key_findings': "계산된 통계량들을 통해 데이터의 중심경향성과 산포도를 파악했습니다.",
            'main_insight': "이러한 결과는 데이터의 전체적인 패턴과 특성을 이해하는 데 도움이 됩니다.",
            'recommendation': "추가적인 시각화와 분석을 통해 더 깊은 인사이트를 얻을 수 있습니다."
        }
    
    def _get_timestamp(self) -> str:
        """타임스탬프 생성"""
        import datetime
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# 테스트용 함수
def test_result_interpreter():
    """결과 해석기 테스트"""
    interpreter = ResultInterpreter()
    
    # 테스트 결과 데이터
    test_result = {
        'success': True,
        'output': '''=== 기술통계량 분석 ===
데이터: [85, 90, 78, 92, 88, 76, 95, 89, 84, 91]
평균: 86.80
중앙값: 88.5
표준편차: 6.09
최솟값: 76
최댓값: 95''',
        'variables': {
            'scores': [85, 90, 78, 92, 88, 76, 95, 89, 84, 91],
            'mean_val': 86.8,
            'median_val': 88.5,
            'stdev_val': 6.09
        },
        'execution_time': 0.001
    }
    
    # 교육 맥락에서 해석
    interpretation = interpreter.interpret_result(test_result, 'education')
    
    print("=== 결과 해석 시스템 테스트 ===")
    print(f"맥락: {interpretation['context']}")
    print(f"\n통계적 의미:")
    for meaning in interpretation['statistical_analysis']['statistical_meaning']:
        print(f"  - {meaning}")
    
    print(f"\n실무적 해석:")
    for insight in interpretation['practical_analysis']['practical_insights']:
        print(f"  - {insight}")
    
    print(f"\n권장사항:")
    for rec in interpretation['practical_analysis']['actionable_recommendations']:
        print(f"  - {rec}")
    
    return interpretation


if __name__ == "__main__":
    test_result_interpreter()