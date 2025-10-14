"""
결과 해석 시스템
- 코드 실행 결과의 통계적 의미 해석
- 실무적 관점에서의 결과 해석
- 맥락에 맞는 추천 제공
"""

import re
import json
import numpy as np
from typing import Dict, Any, List, Optional, Union, Tuple

class ResultInterpreter:
    """
    코드 실행 결과를 해석하는 클래스
    """
    
    def __init__(self):
        """초기화"""
        # 통계 용어 사전
        self.stats_terms = {
            "mean": "평균",
            "median": "중앙값",
            "mode": "최빈값",
            "std": "표준편차",
            "var": "분산",
            "min": "최솟값",
            "max": "최댓값",
            "quantile": "분위수",
            "percentile": "백분위수",
            "correlation": "상관관계",
            "p-value": "p-값",
            "t-test": "t-검정",
            "chi-square": "카이제곱 검정",
            "anova": "분산분석",
            "regression": "회귀분석"
        }
        
        # 결과 해석 템플릿
        self.interpretation_templates = {
            "mean": "평균 {value:.2f}은(는) 데이터의 중심 경향성을 나타냅니다. 모든 값의 합을 개수로 나눈 값입니다.",
            "median": "중앙값 {value:.2f}은(는) 데이터를 크기 순으로 나열했을 때 가운데 위치한 값입니다. 이상치에 덜 민감한 중심 경향성 측정값입니다.",
            "std": "표준편차 {value:.2f}은(는) 데이터가 평균으로부터 얼마나 퍼져 있는지를 나타냅니다. 값이 클수록 데이터의 변동성이 큽니다.",
            "correlation": "상관계수 {value:.2f}은(는) 두 변수 간의 선형 관계 강도를 나타냅니다. 1에 가까울수록 강한 양의 상관관계, -1에 가까울수록 강한 음의 상관관계를 의미합니다.",
            "p_value": "p-값 {value:.4f}은(는) 귀무가설이 참일 때 관측된 결과(또는 더 극단적인 결과)가 나올 확률입니다. 일반적으로 0.05보다 작으면 통계적으로 유의하다고 판단합니다."
        }
    
    def interpret_result(self, result: Any, code: str = None, concept_type: str = None) -> Dict[str, Any]:
        """
        결과 해석
        
        Args:
            result (Any): 코드 실행 결과
            code (str, optional): 실행된 코드
            concept_type (str, optional): 개념 유형 (descriptive_stats, inferential_stats, regression, etc.)
            
        Returns:
            dict: 해석 결과
        """
        interpretation = {
            "statistical_meaning": [],
            "practical_interpretation": [],
            "recommendations": [],
            "code_analysis": self._analyze_code(code) if code else {}
        }
        
        # 결과 유형에 따른 해석
        if isinstance(result, dict):
            interpretation.update(self._interpret_dict_result(result, concept_type))
        elif isinstance(result, (list, tuple, np.ndarray)):
            interpretation.update(self._interpret_array_result(result, concept_type))
        elif isinstance(result, (int, float)):
            interpretation.update(self._interpret_numeric_result(result, code, concept_type))
        elif isinstance(result, str):
            interpretation.update(self._interpret_string_result(result, concept_type))
        else:
            interpretation["statistical_meaning"].append("결과 유형에 대한 통계적 해석을 제공할 수 없습니다.")
            interpretation["practical_interpretation"].append("실행 결과를 확인하고 필요한 추가 분석을 수행하세요.")
        
        # 코드 분석 기반 추가 해석
        if code:
            code_analysis = self._analyze_code(code)
            
            # 통계 분석 코드인 경우
            if code_analysis.get("is_statistical_analysis", False):
                stats_functions = code_analysis.get("statistical_functions", [])
                
                if "mean" in stats_functions:
                    interpretation["statistical_meaning"].append("평균은 데이터의 중심 경향성을 나타내는 기본적인 통계량입니다.")
                    interpretation["practical_interpretation"].append("평균은 이상치에 민감하므로, 데이터에 극단값이 있는 경우 중앙값도 함께 확인하는 것이 좋습니다.")
                
                if "std" in stats_functions or "var" in stats_functions:
                    interpretation["statistical_meaning"].append("표준편차와 분산은 데이터의 퍼짐 정도를 나타내는 지표입니다.")
                    interpretation["practical_interpretation"].append("표준편차가 클수록 데이터의 변동성이 크며, 작을수록 평균 주변에 데이터가 밀집되어 있음을 의미합니다.")
                
                if "corr" in stats_functions or "correlation" in stats_functions:
                    interpretation["statistical_meaning"].append("상관계수는 두 변수 간의 선형 관계 강도를 -1에서 1 사이의 값으로 나타냅니다.")
                    interpretation["practical_interpretation"].append("상관관계가 있다고 해서 반드시 인과관계가 있는 것은 아닙니다. 다른 요인의 영향도 고려해야 합니다.")
            
            # 시각화 코드인 경우
            if code_analysis.get("is_visualization", False):
                viz_types = code_analysis.get("visualization_types", [])
                
                if "histogram" in viz_types:
                    interpretation["statistical_meaning"].append("히스토그램은 데이터의 분포를 시각화하는 도구로, 구간별 빈도를 보여줍니다.")
                    interpretation["practical_interpretation"].append("히스토그램의 모양을 통해 데이터가 정규분포를 따르는지, 치우침이 있는지 등을 파악할 수 있습니다.")
                
                if "scatter" in viz_types:
                    interpretation["statistical_meaning"].append("산점도는 두 변수 간의 관계를 시각화하는 도구입니다.")
                    interpretation["practical_interpretation"].append("점들이 일정한 패턴을 보이면 두 변수 간에 관계가 있을 가능성이 높습니다.")
                
                if "boxplot" in viz_types:
                    interpretation["statistical_meaning"].append("박스플롯은 데이터의 분포, 중앙값, 사분위수, 이상치 등을 한눈에 보여줍니다.")
                    interpretation["practical_interpretation"].append("박스의 크기(IQR)는 데이터의 산포도를 나타내며, 박스 바깥의 점들은 이상치일 가능성이 있습니다.")
        
        # 추천사항 추가
        if not interpretation["recommendations"]:
            interpretation["recommendations"] = self._generate_recommendations(result, code, concept_type)
        
        return interpretation
    
    def _interpret_dict_result(self, result: Dict, concept_type: str = None) -> Dict[str, List[str]]:
        """딕셔너리 결과 해석"""
        interpretation = {
            "statistical_meaning": [],
            "practical_interpretation": []
        }
        
        # 통계 결과 딕셔너리인지 확인
        if "mean" in result or "median" in result or "std" in result:
            interpretation["statistical_meaning"].append("이 결과는 기술통계량을 포함하고 있습니다.")
            
            if "mean" in result and isinstance(result["mean"], (int, float)):
                interpretation["statistical_meaning"].append(
                    self.interpretation_templates["mean"].format(value=result["mean"])
                )
            
            if "median" in result and isinstance(result["median"], (int, float)):
                interpretation["statistical_meaning"].append(
                    self.interpretation_templates["median"].format(value=result["median"])
                )
            
            if "std" in result and isinstance(result["std"], (int, float)):
                interpretation["statistical_meaning"].append(
                    self.interpretation_templates["std"].format(value=result["std"])
                )
            
            # 평균과 중앙값 비교
            if "mean" in result and "median" in result:
                mean = result["mean"]
                median = result["median"]
                
                if isinstance(mean, (int, float)) and isinstance(median, (int, float)):
                    if mean > median:
                        interpretation["practical_interpretation"].append(
                            f"평균({mean:.2f})이 중앙값({median:.2f})보다 크므로, 데이터가 오른쪽으로 치우친(right-skewed) 분포를 가질 가능성이 있습니다. 이는 큰 값의 이상치가 있을 수 있음을 의미합니다."
                        )
                    elif mean < median:
                        interpretation["practical_interpretation"].append(
                            f"평균({mean:.2f})이 중앙값({median:.2f})보다 작으므로, 데이터가 왼쪽으로 치우친(left-skewed) 분포를 가질 가능성이 있습니다. 이는 작은 값의 이상치가 있을 수 있음을 의미합니다."
                        )
                    else:
                        interpretation["practical_interpretation"].append(
                            f"평균({mean:.2f})과 중앙값({median:.2f})이 같으므로, 데이터가 대칭적인 분포를 가질 가능성이 높습니다."
                        )
        
        # 상관관계 결과인지 확인
        if "correlation" in result or "corr" in result:
            corr_key = "correlation" if "correlation" in result else "corr"
            corr_value = result[corr_key]
            
            if isinstance(corr_value, (int, float)):
                interpretation["statistical_meaning"].append(
                    self.interpretation_templates["correlation"].format(value=corr_value)
                )
                
                # 상관관계 강도 해석
                if abs(corr_value) > 0.7:
                    strength = "강한"
                elif abs(corr_value) > 0.3:
                    strength = "중간 정도의"
                else:
                    strength = "약한"
                
                direction = "양의" if corr_value > 0 else "음의"
                
                interpretation["practical_interpretation"].append(
                    f"상관계수 {corr_value:.2f}는 두 변수 간에 {strength} {direction} 선형 관계가 있음을 나타냅니다."
                )
                
                if abs(corr_value) > 0.7:
                    interpretation["practical_interpretation"].append(
                        "두 변수가 매우 밀접하게 관련되어 있으므로, 한 변수의 변화가 다른 변수의 변화와 강하게 연관될 가능성이 높습니다."
                    )
        
        # 가설 검정 결과인지 확인
        if "p_value" in result or "pvalue" in result:
            p_key = "p_value" if "p_value" in result else "pvalue"
            p_value = result[p_key]
            
            if isinstance(p_value, (int, float)):
                interpretation["statistical_meaning"].append(
                    self.interpretation_templates["p_value"].format(value=p_value)
                )
                
                # p-값 해석
                if p_value < 0.01:
                    interpretation["practical_interpretation"].append(
                        f"p-값({p_value:.4f})이 0.01보다 작으므로, 매우 강한 통계적 유의성을 나타냅니다. 귀무가설을 기각할 충분한 증거가 있습니다."
                    )
                elif p_value < 0.05:
                    interpretation["practical_interpretation"].append(
                        f"p-값({p_value:.4f})이 0.05보다 작으므로, 통계적으로 유의합니다. 귀무가설을 기각할 충분한 증거가 있습니다."
                    )
                else:
                    interpretation["practical_interpretation"].append(
                        f"p-값({p_value:.4f})이 0.05보다 크므로, 통계적으로 유의하지 않습니다. 귀무가설을 기각할 충분한 증거가 없습니다."
                    )
        
        return interpretation
    
    def _interpret_array_result(self, result: Union[List, Tuple, np.ndarray], concept_type: str = None) -> Dict[str, List[str]]:
        """배열 결과 해석"""
        interpretation = {
            "statistical_meaning": [],
            "practical_interpretation": []
        }
        
        # 숫자 배열인지 확인
        try:
            # NumPy 배열로 변환 시도
            if not isinstance(result, np.ndarray):
                arr = np.array(result, dtype=float)
            else:
                arr = result
            
            # 숫자 배열이면 기술통계량 계산
            if arr.size > 0 and np.issubdtype(arr.dtype, np.number):
                mean = np.mean(arr)
                median = np.median(arr)
                std = np.std(arr)
                min_val = np.min(arr)
                max_val = np.max(arr)
                
                interpretation["statistical_meaning"].append(f"데이터 개수: {arr.size}")
                interpretation["statistical_meaning"].append(f"평균: {mean:.2f}")
                interpretation["statistical_meaning"].append(f"중앙값: {median:.2f}")
                interpretation["statistical_meaning"].append(f"표준편차: {std:.2f}")
                interpretation["statistical_meaning"].append(f"범위: {min_val:.2f} ~ {max_val:.2f}")
                
                # 분포 특성 해석
                if mean > median:
                    interpretation["practical_interpretation"].append(
                        f"평균({mean:.2f})이 중앙값({median:.2f})보다 크므로, 데이터가 오른쪽으로 치우친 분포를 가질 가능성이 있습니다."
                    )
                elif mean < median:
                    interpretation["practical_interpretation"].append(
                        f"평균({mean:.2f})이 중앙값({median:.2f})보다 작으므로, 데이터가 왼쪽으로 치우친 분포를 가질 가능성이 있습니다."
                    )
                else:
                    interpretation["practical_interpretation"].append(
                        f"평균({mean:.2f})과 중앙값({median:.2f})이 같으므로, 데이터가 대칭적인 분포를 가질 가능성이 높습니다."
                    )
                
                # 변동계수(CV) 계산 및 해석
                if mean != 0:
                    cv = std / mean
                    interpretation["statistical_meaning"].append(f"변동계수(CV): {cv:.2f}")
                    
                    if cv < 0.1:
                        interpretation["practical_interpretation"].append(
                            "변동계수가 0.1보다 작으므로, 데이터의 변동성이 낮습니다. 값들이 평균 주변에 밀집되어 있습니다."
                        )
                    elif cv > 0.3:
                        interpretation["practical_interpretation"].append(
                            "변동계수가 0.3보다 크므로, 데이터의 변동성이 높습니다. 값들이 평균으로부터 넓게 퍼져 있습니다."
                        )
                    else:
                        interpretation["practical_interpretation"].append(
                            "변동계수가 중간 정도로, 데이터가 적절한 변동성을 가지고 있습니다."
                        )
        except:
            # 숫자 배열이 아니면 일반적인 정보 제공
            interpretation["statistical_meaning"].append(f"데이터 개수: {len(result)}")
            interpretation["practical_interpretation"].append("비숫자 데이터이므로 기술통계량을 계산할 수 없습니다.")
        
        return interpretation
    
    def _interpret_numeric_result(self, result: Union[int, float], code: str = None, concept_type: str = None) -> Dict[str, List[str]]:
        """숫자 결과 해석"""
        interpretation = {
            "statistical_meaning": [],
            "practical_interpretation": []
        }
        
        # 코드 분석을 통한 맥락 파악
        if code:
            code_analysis = self._analyze_code(code)
            
            # 평균 계산 결과인지 확인
            if re.search(r'mean|average|np\.mean|\.mean\(\)', code):
                interpretation["statistical_meaning"].append(
                    self.interpretation_templates["mean"].format(value=result)
                )
                interpretation["practical_interpretation"].append(
                    "평균은 이상치에 민감하므로, 데이터에 극단값이 있는 경우 중앙값도 함께 확인하는 것이 좋습니다."
                )
            
            # 중앙값 계산 결과인지 확인
            elif re.search(r'median|np\.median|\.median\(\)', code):
                interpretation["statistical_meaning"].append(
                    self.interpretation_templates["median"].format(value=result)
                )
                interpretation["practical_interpretation"].append(
                    "중앙값은 이상치에 덜 민감하므로, 치우친 분포나 이상치가 있는 데이터에서 중심 경향성을 파악하는 데 유용합니다."
                )
            
            # 표준편차 계산 결과인지 확인
            elif re.search(r'std|standard deviation|np\.std|\.std\(\)', code):
                interpretation["statistical_meaning"].append(
                    self.interpretation_templates["std"].format(value=result)
                )
                interpretation["practical_interpretation"].append(
                    "표준편차가 클수록 데이터의 변동성이 크며, 작을수록 평균 주변에 데이터가 밀집되어 있음을 의미합니다."
                )
            
            # 상관계수 계산 결과인지 확인
            elif re.search(r'corr|correlation|np\.corrcoef|\.corr\(\)', code):
                interpretation["statistical_meaning"].append(
                    self.interpretation_templates["correlation"].format(value=result)
                )
                
                # 상관관계 강도 해석
                if abs(result) > 0.7:
                    strength = "강한"
                elif abs(result) > 0.3:
                    strength = "중간 정도의"
                else:
                    strength = "약한"
                
                direction = "양의" if result > 0 else "음의"
                
                interpretation["practical_interpretation"].append(
                    f"상관계수 {result:.2f}는 두 변수 간에 {strength} {direction} 선형 관계가 있음을 나타냅니다."
                )
                
                interpretation["practical_interpretation"].append(
                    "상관관계가 있다고 해서 반드시 인과관계가 있는 것은 아닙니다. 다른 요인의 영향도 고려해야 합니다."
                )
            
            # p-값 계산 결과인지 확인
            elif re.search(r'p-value|pvalue|\.pvalue|significance', code):
                interpretation["statistical_meaning"].append(
                    self.interpretation_templates["p_value"].format(value=result)
                )
                
                # p-값 해석
                if result < 0.01:
                    interpretation["practical_interpretation"].append(
                        f"p-값({result:.4f})이 0.01보다 작으므로, 매우 강한 통계적 유의성을 나타냅니다. 귀무가설을 기각할 충분한 증거가 있습니다."
                    )
                elif result < 0.05:
                    interpretation["practical_interpretation"].append(
                        f"p-값({result:.4f})이 0.05보다 작으므로, 통계적으로 유의합니다. 귀무가설을 기각할 충분한 증거가 있습니다."
                    )
                else:
                    interpretation["practical_interpretation"].append(
                        f"p-값({result:.4f})이 0.05보다 크므로, 통계적으로 유의하지 않습니다. 귀무가설을 기각할 충분한 증거가 없습니다."
                    )
            
            # 일반적인 숫자 결과
            else:
                interpretation["statistical_meaning"].append(f"계산 결과: {result}")
                interpretation["practical_interpretation"].append("이 값의 맥락과 의미는 계산 방법과 데이터의 특성에 따라 달라집니다.")
        else:
            # 코드 정보가 없는 경우
            interpretation["statistical_meaning"].append(f"계산 결과: {result}")
            interpretation["practical_interpretation"].append("이 값의 맥락과 의미는 계산 방법과 데이터의 특성에 따라 달라집니다.")
        
        return interpretation
    
    def _interpret_string_result(self, result: str, concept_type: str = None) -> Dict[str, List[str]]:
        """문자열 결과 해석"""
        interpretation = {
            "statistical_meaning": [],
            "practical_interpretation": []
        }
        
        # 통계 결과가 포함된 문자열인지 확인
        stats_patterns = {
            "mean": r'mean[:\s=]+(\d+\.?\d*)',
            "median": r'median[:\s=]+(\d+\.?\d*)',
            "std": r'std|standard deviation[:\s=]+(\d+\.?\d*)',
            "correlation": r'corr|correlation[:\s=]+([-]?\d+\.?\d*)',
            "p_value": r'p-?value[:\s=]+([\d\.e\-]+)'
        }
        
        for stat, pattern in stats_patterns.items():
            match = re.search(pattern, result, re.IGNORECASE)
            if match:
                try:
                    value = float(match.group(1))
                    if stat in self.interpretation_templates:
                        interpretation["statistical_meaning"].append(
                            self.interpretation_templates[stat].format(value=value)
                        )
                except:
                    pass
        
        # 일반적인 문자열 결과
        if not interpretation["statistical_meaning"]:
            interpretation["statistical_meaning"].append("텍스트 결과에서 통계적 의미를 추출할 수 없습니다.")
            interpretation["practical_interpretation"].append("결과를 직접 검토하여 관련 정보를 확인하세요.")
        
        return interpretation
    
    def _analyze_code(self, code: str) -> Dict[str, Any]:
        """코드 분석"""
        if not code:
            return {}
        
        analysis = {
            "is_statistical_analysis": False,
            "is_visualization": False,
            "statistical_functions": [],
            "visualization_types": [],
            "libraries_used": []
        }
        
        # 라이브러리 사용 확인
        if re.search(r'import\s+numpy|import\s+np|from\s+numpy', code):
            analysis["libraries_used"].append("numpy")
        
        if re.search(r'import\s+pandas|import\s+pd|from\s+pandas', code):
            analysis["libraries_used"].append("pandas")
        
        if re.search(r'import\s+matplotlib|import\s+plt|from\s+matplotlib', code):
            analysis["libraries_used"].append("matplotlib")
            analysis["is_visualization"] = True
        
        if re.search(r'import\s+seaborn|import\s+sns|from\s+seaborn', code):
            analysis["libraries_used"].append("seaborn")
            analysis["is_visualization"] = True
        
        if re.search(r'import\s+scipy|from\s+scipy', code):
            analysis["libraries_used"].append("scipy")
        
        if re.search(r'import\s+statsmodels|from\s+statsmodels', code):
            analysis["libraries_used"].append("statsmodels")
        
        # 통계 함수 사용 확인
        stat_functions = [
            "mean", "median", "mode", "std", "var", "min", "max",
            "quantile", "percentile", "corr", "correlation",
            "ttest", "t-test", "chi2", "chi-square", "anova", "regression"
        ]
        
        for func in stat_functions:
            if re.search(rf'\b{func}\b', code):
                analysis["statistical_functions"].append(func)
                analysis["is_statistical_analysis"] = True
        
        # 시각화 유형 확인
        viz_types = [
            "histogram", "hist", "bar", "barplot", "scatter", "scatterplot",
            "line", "lineplot", "box", "boxplot", "violin", "violinplot",
            "heatmap", "pie", "piechart"
        ]
        
        for viz in viz_types:
            if re.search(rf'\b{viz}\b', code):
                analysis["visualization_types"].append(viz)
                analysis["is_visualization"] = True
        
        return analysis
    
    def _generate_recommendations(self, result: Any, code: str = None, concept_type: str = None) -> List[str]:
        """추천사항 생성"""
        recommendations = []
        
        # 코드 분석 기반 추천
        if code:
            code_analysis = self._analyze_code(code)
            
            # 통계 분석 코드인 경우
            if code_analysis.get("is_statistical_analysis", False):
                recommendations.append("데이터의 분포를 시각화하여 더 깊은 인사이트를 얻어보세요.")
                recommendations.append("이상치가 있는지 확인하고, 필요한 경우 처리 방법을 고려하세요.")
                
                if "mean" in code_analysis.get("statistical_functions", []):
                    recommendations.append("평균과 함께 중앙값도 확인하여 데이터의 치우침을 파악하세요.")
                
                if "correlation" in code_analysis.get("statistical_functions", []):
                    recommendations.append("상관관계가 있다고 해서 인과관계가 있는 것은 아닙니다. 다른 요인의 영향도 고려하세요.")
            
            # 시각화 코드인 경우
            if code_analysis.get("is_visualization", False):
                recommendations.append("그래프에 제목, 축 레이블, 범례를 추가하여 가독성을 높이세요.")
                recommendations.append("색상과 마커를 적절히 사용하여 정보를 효과적으로 전달하세요.")
                
                if "histogram" in code_analysis.get("visualization_types", []):
                    recommendations.append("히스토그램의 구간(bin) 개수를 조정하여 데이터의 패턴을 더 잘 파악해보세요.")
                
                if "scatter" in code_analysis.get("visualization_types", []):
                    recommendations.append("산점도에 추세선을 추가하여 관계의 방향과 강도를 시각화해보세요.")
        
        # 결과 유형에 따른 추천
        if isinstance(result, (list, tuple, np.ndarray)):
            try:
                arr = np.array(result, dtype=float)
                if arr.size > 0:
                    recommendations.append("데이터의 분포를 히스토그램으로 시각화하여 패턴을 파악해보세요.")
                    recommendations.append("박스플롯을 사용하여 이상치를 확인해보세요.")
            except:
                pass
        
        # 기본 추천사항
        if not recommendations:
            recommendations.append("결과를 다양한 관점에서 해석하고, 맥락에 맞게 활용하세요.")
            recommendations.append("추가 분석을 통해 더 깊은 인사이트를 얻어보세요.")
        
        return recommendations
    
    def generate_interpretation_html(self, result: Any, code: str = None, concept_type: str = None) -> str:
        """
        결과 해석 HTML 생성
        
        Args:
            result (Any): 코드 실행 결과
            code (str, optional): 실행된 코드
            concept_type (str, optional): 개념 유형
            
        Returns:
            str: HTML 코드
        """
        # 결과 해석
        interpretation = self.interpret_result(result, code, concept_type)
        
        # HTML 생성
        html = """
        <div class="interpretation-container" style="margin: 20px 0; border: 1px solid #ddd; border-radius: 4px; overflow: hidden;">
            <div class="interpretation-header" style="background: #f5f5f5; padding: 10px; border-bottom: 1px solid #ddd;">
                <h3 style="margin: 0; color: #333;">결과 해석</h3>
            </div>
            <div class="interpretation-body" style="padding: 15px;">
        """
        
        # 통계적 의미
        if interpretation["statistical_meaning"]:
            html += """
                <div class="section">
                    <h4 style="color: #2196F3; margin-top: 0;">📊 통계적 의미</h4>
                    <ul style="padding-left: 20px; margin-bottom: 15px;">
            """
            
            for meaning in interpretation["statistical_meaning"]:
                html += f"<li>{meaning}</li>"
            
            html += """
                    </ul>
                </div>
            """
        
        # 실무적 해석
        if interpretation["practical_interpretation"]:
            html += """
                <div class="section">
                    <h4 style="color: #4CAF50; margin-top: 0;">💡 실무적 해석</h4>
                    <ul style="padding-left: 20px; margin-bottom: 15px;">
            """
            
            for interp in interpretation["practical_interpretation"]:
                html += f"<li>{interp}</li>"
            
            html += """
                    </ul>
                </div>
            """
        
        # 추천사항
        if interpretation["recommendations"]:
            html += """
                <div class="section">
                    <h4 style="color: #FF9800; margin-top: 0;">🔍 추천사항</h4>
                    <ul style="padding-left: 20px; margin-bottom: 0;">
            """
            
            for rec in interpretation["recommendations"]:
                html += f"<li>{rec}</li>"
            
            html += """
                    </ul>
                </div>
            """
        
        html += """
            </div>
        </div>
        """
        
        return html

# 결과 해석기 인스턴스 생성
result_interpreter = ResultInterpreter()