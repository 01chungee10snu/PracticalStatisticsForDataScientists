"""
단계별 검증 및 힌트 시스템
- 코드 실행 결과 자동 검증 기능
- 상황별 맞춤 힌트 제공 시스템
- 학습 진도에 따른 적응형 피드백
"""

import re
import ast
from typing import Dict, List, Any, Optional, Tuple
from enum import Enum

class VerificationLevel(Enum):
    """검증 수준"""
    BASIC = "basic"          # 기본 출력 확인
    INTERMEDIATE = "intermediate"  # 코드 구조 확인
    ADVANCED = "advanced"    # 결과 값 정확성 확인

class HintLevel(Enum):
    """힌트 수준"""
    GENTLE = "gentle"        # 부드러운 힌트
    DIRECT = "direct"        # 직접적인 힌트
    EXPLICIT = "explicit"    # 명시적인 힌트

class VerificationHintSystem:
    """
    단계별 검증 및 힌트 시스템
    코드 실행 결과를 자동으로 검증하고 상황별 맞춤 힌트를 제공합니다.
    """
    
    def __init__(self):
        """초기화"""
        self.verification_rules = self._initialize_verification_rules()
        self.hint_templates = self._initialize_hint_templates()
        self.feedback_messages = self._initialize_feedback_messages()
        self.verification_history = []
    
    def _initialize_verification_rules(self) -> Dict[str, Dict[str, Any]]:
        """검증 규칙 초기화"""
        return {
            "data_preparation": {
                "output_patterns": [
                    r"생성된 데이터 개수:\s*50",
                    r"처음 10개 데이터:",
                    r"\[.*\]"  # 배열 출력 패턴
                ],
                "code_patterns": [
                    r"import\s+numpy",
                    r"np\.random\.normal",
                    r"np\.random\.seed\(42\)",
                    r"print\("
                ],
                "required_variables": ["scores"],
                "forbidden_patterns": [],
                "success_criteria": {
                    "has_import": True,
                    "has_data_generation": True,
                    "has_output": True,
                    "correct_data_size": True
                }
            },
            "central_tendency": {
                "output_patterns": [
                    r"평균:\s*[\d\.]+",
                    r"중앙값:\s*[\d\.]+",
                    r"최빈값:\s*[\d\.]+"
                ],
                "code_patterns": [
                    r"np\.mean\(",
                    r"np\.median\(",
                    r"stats\.mode\("
                ],
                "required_variables": ["mean", "median", "mode"],
                "forbidden_patterns": [],
                "success_criteria": {
                    "calculates_mean": True,
                    "calculates_median": True,
                    "calculates_mode": True,
                    "has_comparison": True
                }
            },
            "dispersion": {
                "output_patterns": [
                    r"범위:\s*[\d\.]+",
                    r"분산:\s*[\d\.]+",
                    r"표준편차:\s*[\d\.]+",
                    r"사분위수 범위\(IQR\):\s*[\d\.]+",
                    r"변동계수\(CV\):\s*[\d\.]+"
                ],
                "code_patterns": [
                    r"np\.var\(",
                    r"np\.std\(",
                    r"np\.percentile\(",
                    r"np\.max\(",
                    r"np\.min\("
                ],
                "required_variables": ["variance", "std_dev", "iqr", "cv"],
                "forbidden_patterns": [],
                "success_criteria": {
                    "calculates_variance": True,
                    "calculates_std": True,
                    "calculates_iqr": True,
                    "calculates_cv": True,
                    "detects_outliers": True
                }
            },
            "visualization": {
                "output_patterns": [
                    r"데이터 시각화 완료!",
                    r"평균:\s*[\d\.]+",
                    r"중앙값:\s*[\d\.]+",
                    r"표준편차:\s*[\d\.]+"
                ],
                "code_patterns": [
                    r"plt\.figure\(",
                    r"plt\.hist\(",
                    r"plt\.boxplot\(",
                    r"plt\.subplot\(",
                    r"plt\.show\(\)"
                ],
                "required_variables": [],
                "forbidden_patterns": [],
                "success_criteria": {
                    "has_histogram": True,
                    "has_boxplot": True,
                    "has_labels": True,
                    "shows_plot": True
                }
            },
            "interpretation": {
                "output_patterns": [
                    r"📊 데이터 분석 종합 결과",
                    r"중심경향성:",
                    r"산포도:",
                    r"분포 특성:",
                    r"해석 및 결론:",
                    r"정규성 검정 p-값:"
                ],
                "code_patterns": [
                    r"stats\.shapiro\(",
                    r"print\(",
                    r"if.*normal_p_value"
                ],
                "required_variables": ["normal_p_value"],
                "forbidden_patterns": [],
                "success_criteria": {
                    "has_summary": True,
                    "has_normality_test": True,
                    "has_interpretation": True,
                    "has_conclusion": True
                }
            }
        }
    
    def _initialize_hint_templates(self) -> Dict[str, Dict[HintLevel, List[str]]]:
        """힌트 템플릿 초기화"""
        return {
            "data_preparation": {
                HintLevel.GENTLE: [
                    "데이터를 생성하는 함수를 사용해보세요.",
                    "numpy 라이브러리를 import 했는지 확인해보세요.",
                    "생성된 데이터의 개수를 출력해보세요."
                ],
                HintLevel.DIRECT: [
                    "np.random.normal() 함수를 사용하여 정규분포 데이터를 생성하세요.",
                    "np.random.seed(42)를 사용하여 재현 가능한 결과를 만드세요.",
                    "print() 함수로 데이터 정보를 출력하세요."
                ],
                HintLevel.EXPLICIT: [
                    "import numpy as np를 코드 맨 위에 추가하세요.",
                    "scores = np.random.normal(loc=70, scale=15, size=50)로 데이터를 생성하세요.",
                    "print(f'생성된 데이터 개수: {len(scores)}')로 개수를 출력하세요."
                ]
            },
            "central_tendency": {
                HintLevel.GENTLE: [
                    "평균, 중앙값, 최빈값을 각각 계산해보세요.",
                    "scipy.stats 모듈이 필요할 수 있습니다.",
                    "계산된 값들을 비교해보세요."
                ],
                HintLevel.DIRECT: [
                    "np.mean()으로 평균을, np.median()으로 중앙값을 계산하세요.",
                    "stats.mode()를 사용하여 최빈값을 구하세요.",
                    "평균과 중앙값의 크기를 비교하여 분포의 치우침을 판단하세요."
                ],
                HintLevel.EXPLICIT: [
                    "from scipy import stats를 추가하세요.",
                    "mean = np.mean(scores)로 평균을 계산하세요.",
                    "mode = stats.mode(scores)[0][0]로 최빈값을 계산하세요."
                ]
            },
            "dispersion": {
                HintLevel.GENTLE: [
                    "데이터의 퍼짐 정도를 나타내는 여러 지표를 계산해보세요.",
                    "분산과 표준편차의 관계를 생각해보세요.",
                    "사분위수를 이용한 지표도 계산해보세요."
                ],
                HintLevel.DIRECT: [
                    "np.var()와 np.std()로 분산과 표준편차를 계산하세요.",
                    "np.percentile()을 사용하여 사분위수를 구하세요.",
                    "변동계수(CV)는 표준편차를 평균으로 나눈 값입니다."
                ],
                HintLevel.EXPLICIT: [
                    "variance = np.var(scores)로 분산을 계산하세요.",
                    "q1, q3 = np.percentile(scores, [25, 75])로 사분위수를 구하세요.",
                    "cv = std_dev / np.mean(scores)로 변동계수를 계산하세요."
                ]
            },
            "visualization": {
                HintLevel.GENTLE: [
                    "히스토그램과 박스플롯을 그려보세요.",
                    "matplotlib 라이브러리를 사용하세요.",
                    "두 그래프를 나란히 배치해보세요."
                ],
                HintLevel.DIRECT: [
                    "plt.hist()로 히스토그램을, plt.boxplot()으로 박스플롯을 그리세요.",
                    "plt.subplot()을 사용하여 두 그래프를 배치하세요.",
                    "평균과 중앙값을 그래프에 표시해보세요."
                ],
                HintLevel.EXPLICIT: [
                    "plt.figure(figsize=(12, 5))로 그래프 크기를 설정하세요.",
                    "plt.subplot(1, 2, 1)과 plt.subplot(1, 2, 2)로 두 영역을 나누세요.",
                    "plt.axvline()을 사용하여 평균선을 그래프에 추가하세요."
                ]
            },
            "interpretation": {
                HintLevel.GENTLE: [
                    "지금까지 계산한 모든 통계량을 종합해보세요.",
                    "정규성 검정을 수행해보세요.",
                    "결과를 실무적 관점에서 해석해보세요."
                ],
                HintLevel.DIRECT: [
                    "stats.shapiro()를 사용하여 정규성 검정을 하세요.",
                    "p-값이 0.05보다 큰지 작은지에 따라 해석이 달라집니다.",
                    "정규분포의 68-95-99.7 규칙을 활용해보세요."
                ],
                HintLevel.EXPLICIT: [
                    "shapiro_test = stats.shapiro(scores)로 정규성 검정을 하세요.",
                    "normal_p_value = shapiro_test[1]로 p-값을 추출하세요.",
                    "if normal_p_value > 0.05: 조건문으로 해석을 분기하세요."
                ]
            }
        }
    
    def _initialize_feedback_messages(self) -> Dict[str, Dict[str, str]]:
        """피드백 메시지 초기화"""
        return {
            "success": {
                "data_preparation": "훌륭합니다! 데이터가 성공적으로 생성되었습니다. 이제 통계 분석을 시작할 준비가 되었네요.",
                "central_tendency": "잘했습니다! 중심경향성 지표들을 모두 계산했습니다. 평균과 중앙값의 차이를 통해 분포의 특성을 파악할 수 있어요.",
                "dispersion": "완벽합니다! 산포도 지표들을 통해 데이터의 변동성을 잘 분석했습니다. 변동계수와 이상치 정보도 유용하네요.",
                "visualization": "멋진 시각화입니다! 히스토그램과 박스플롯을 통해 데이터의 분포를 한눈에 볼 수 있게 되었어요.",
                "interpretation": "종합적인 해석이 훌륭합니다! 통계적 검정과 실무적 관점을 모두 고려한 완성도 높은 분석이에요."
            },
            "partial_success": {
                "data_preparation": "데이터 생성은 되었지만, 일부 출력이 누락되었습니다. 데이터 확인 과정을 추가해보세요.",
                "central_tendency": "일부 중심경향성 지표가 계산되었습니다. 누락된 지표들도 계산해보세요.",
                "dispersion": "산포도 계산이 부분적으로 완료되었습니다. 모든 지표를 계산하여 완전한 분석을 해보세요.",
                "visualization": "그래프가 일부 생성되었습니다. 히스토그램과 박스플롯을 모두 그려보세요.",
                "interpretation": "해석이 시작되었습니다. 정규성 검정과 종합적인 결론을 추가해보세요."
            },
            "failure": {
                "data_preparation": "데이터 생성에 문제가 있습니다. numpy 라이브러리 import와 함수 사용법을 확인해보세요.",
                "central_tendency": "중심경향성 계산에 오류가 있습니다. 각 함수의 사용법을 다시 확인해보세요.",
                "dispersion": "산포도 계산이 제대로 되지 않았습니다. 각 통계량의 계산 방법을 검토해보세요.",
                "visualization": "시각화에 문제가 있습니다. matplotlib 함수들의 사용법을 확인해보세요.",
                "interpretation": "해석 과정에 오류가 있습니다. 필요한 통계량들이 모두 계산되었는지 확인해보세요."
            }
        }
    
    def verify_step(self, step_id: str, code: str, output: str, 
                   verification_level: VerificationLevel = VerificationLevel.BASIC) -> Dict[str, Any]:
        """
        단계 검증
        
        Args:
            step_id (str): 단계 ID
            code (str): 실행된 코드
            output (str): 실행 결과
            verification_level (VerificationLevel): 검증 수준
            
        Returns:
            dict: 검증 결과
        """
        if step_id not in self.verification_rules:
            return {
                "success": False,
                "score": 0,
                "message": "알 수 없는 단계입니다.",
                "details": []
            }
        
        rules = self.verification_rules[step_id]
        verification_result = {
            "success": False,
            "score": 0,
            "message": "",
            "details": [],
            "missing_elements": [],
            "suggestions": []
        }
        
        # 검증 수행
        if verification_level == VerificationLevel.BASIC:
            verification_result = self._verify_basic(step_id, code, output, rules)
        elif verification_level == VerificationLevel.INTERMEDIATE:
            verification_result = self._verify_intermediate(step_id, code, output, rules)
        elif verification_level == VerificationLevel.ADVANCED:
            verification_result = self._verify_advanced(step_id, code, output, rules)
        
        # 검증 기록 저장
        self.verification_history.append({
            "step_id": step_id,
            "timestamp": self._get_timestamp(),
            "verification_level": verification_level.value,
            "result": verification_result
        })
        
        return verification_result
    
    def _verify_basic(self, step_id: str, code: str, output: str, rules: Dict[str, Any]) -> Dict[str, Any]:
        """기본 검증 (출력 패턴 확인)"""
        result = {
            "success": False,
            "score": 0,
            "message": "",
            "details": [],
            "missing_elements": [],
            "suggestions": []
        }
        
        output_patterns = rules.get("output_patterns", [])
        matched_patterns = 0
        
        for pattern in output_patterns:
            if re.search(pattern, output, re.IGNORECASE):
                matched_patterns += 1
                result["details"].append(f"출력 패턴 확인: '{pattern}' ✓")
            else:
                result["details"].append(f"출력 패턴 누락: '{pattern}' ✗")
                result["missing_elements"].append(f"예상 출력: {pattern}")
        
        # 점수 계산
        if output_patterns:
            result["score"] = (matched_patterns / len(output_patterns)) * 100
        
        # 성공 여부 판단
        if result["score"] >= 80:
            result["success"] = True
            result["message"] = self.feedback_messages["success"][step_id]
        elif result["score"] >= 50:
            result["message"] = self.feedback_messages["partial_success"][step_id]
        else:
            result["message"] = self.feedback_messages["failure"][step_id]
        
        return result
    
    def _verify_intermediate(self, step_id: str, code: str, output: str, rules: Dict[str, Any]) -> Dict[str, Any]:
        """중급 검증 (코드 구조 + 출력 확인)"""
        result = self._verify_basic(step_id, code, output, rules)
        
        # 코드 패턴 검증 추가
        code_patterns = rules.get("code_patterns", [])
        matched_code_patterns = 0
        
        for pattern in code_patterns:
            if re.search(pattern, code, re.IGNORECASE):
                matched_code_patterns += 1
                result["details"].append(f"코드 패턴 확인: '{pattern}' ✓")
            else:
                result["details"].append(f"코드 패턴 누락: '{pattern}' ✗")
                result["missing_elements"].append(f"필요한 코드: {pattern}")
        
        # 점수 재계산 (출력 70% + 코드 30%)
        output_score = result["score"]
        code_score = (matched_code_patterns / len(code_patterns) * 100) if code_patterns else 100
        result["score"] = output_score * 0.7 + code_score * 0.3
        
        # 성공 여부 재판단
        if result["score"] >= 80:
            result["success"] = True
            result["message"] = self.feedback_messages["success"][step_id]
        elif result["score"] >= 50:
            result["message"] = self.feedback_messages["partial_success"][step_id]
        else:
            result["message"] = self.feedback_messages["failure"][step_id]
        
        return result
    
    def _verify_advanced(self, step_id: str, code: str, output: str, rules: Dict[str, Any]) -> Dict[str, Any]:
        """고급 검증 (변수 존재 + 값 정확성 확인)"""
        result = self._verify_intermediate(step_id, code, output, rules)
        
        # 변수 존재 확인
        required_variables = rules.get("required_variables", [])
        found_variables = 0
        
        for var_name in required_variables:
            if re.search(rf'\b{var_name}\s*=', code):
                found_variables += 1
                result["details"].append(f"변수 확인: '{var_name}' ✓")
            else:
                result["details"].append(f"변수 누락: '{var_name}' ✗")
                result["missing_elements"].append(f"필요한 변수: {var_name}")
        
        # 금지된 패턴 확인
        forbidden_patterns = rules.get("forbidden_patterns", [])
        forbidden_found = 0
        
        for pattern in forbidden_patterns:
            if re.search(pattern, code, re.IGNORECASE):
                forbidden_found += 1
                result["details"].append(f"금지된 패턴 발견: '{pattern}' ✗")
                result["suggestions"].append(f"'{pattern}' 사용을 피하세요.")
        
        # 점수 재계산 (출력 50% + 코드 30% + 변수 20%)
        output_score = result["score"] * 0.7  # 이전 단계의 점수
        variable_score = (found_variables / len(required_variables) * 100) if required_variables else 100
        penalty = forbidden_found * 10  # 금지된 패턴 페널티
        
        result["score"] = max(0, (result["score"] * 0.8 + variable_score * 0.2) - penalty)
        
        # 성공 여부 재판단
        if result["score"] >= 80:
            result["success"] = True
            result["message"] = self.feedback_messages["success"][step_id]
        elif result["score"] >= 50:
            result["message"] = self.feedback_messages["partial_success"][step_id]
        else:
            result["message"] = self.feedback_messages["failure"][step_id]
        
        return result   
 
    def get_hints(self, step_id: str, attempt_count: int = 1, 
                  verification_result: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        힌트 제공
        
        Args:
            step_id (str): 단계 ID
            attempt_count (int): 시도 횟수
            verification_result (dict, optional): 검증 결과
            
        Returns:
            dict: 힌트 정보
        """
        if step_id not in self.hint_templates:
            return {
                "success": False,
                "message": "해당 단계의 힌트가 없습니다.",
                "hints": []
            }
        
        # 시도 횟수에 따른 힌트 수준 결정
        if attempt_count <= 2:
            hint_level = HintLevel.GENTLE
        elif attempt_count <= 4:
            hint_level = HintLevel.DIRECT
        else:
            hint_level = HintLevel.EXPLICIT
        
        hints = self.hint_templates[step_id][hint_level]
        
        # 검증 결과에 따른 맞춤형 힌트 추가
        customized_hints = hints.copy()
        if verification_result:
            customized_hints.extend(self._generate_contextual_hints(step_id, verification_result))
        
        return {
            "success": True,
            "hint_level": hint_level.value,
            "hints": customized_hints,
            "attempt_count": attempt_count,
            "message": f"시도 {attempt_count}회차 힌트입니다."
        }
    
    def _generate_contextual_hints(self, step_id: str, verification_result: Dict[str, Any]) -> List[str]:
        """맥락적 힌트 생성"""
        contextual_hints = []
        
        # 누락된 요소에 대한 구체적 힌트
        missing_elements = verification_result.get("missing_elements", [])
        for element in missing_elements:
            if "출력" in element:
                contextual_hints.append(f"다음 출력이 누락되었습니다: {element}")
            elif "코드" in element:
                contextual_hints.append(f"다음 코드가 필요합니다: {element}")
            elif "변수" in element:
                contextual_hints.append(f"다음 변수를 정의해야 합니다: {element}")
        
        # 점수에 따른 격려 메시지
        score = verification_result.get("score", 0)
        if score >= 70:
            contextual_hints.append("거의 다 왔습니다! 조금만 더 수정하면 완성이에요.")
        elif score >= 40:
            contextual_hints.append("좋은 시작입니다! 몇 가지 요소를 추가하면 됩니다.")
        else:
            contextual_hints.append("처음부터 차근차근 다시 시도해보세요.")
        
        return contextual_hints
    
    def generate_feedback_html(self, step_id: str, verification_result: Dict[str, Any], 
                              hints: Dict[str, Any] = None) -> str:
        """피드백 HTML 생성"""
        score = verification_result.get("score", 0)
        success = verification_result.get("success", False)
        
        # 점수에 따른 색상 결정
        if score >= 80:
            color = "#28a745"  # 성공 (녹색)
            icon = "✅"
        elif score >= 50:
            color = "#ffc107"  # 부분 성공 (노란색)
            icon = "⚠️"
        else:
            color = "#dc3545"  # 실패 (빨간색)
            icon = "❌"
        
        html = f"""
        <div class="verification-feedback" style="margin: 20px 0; border: 1px solid {color}; border-radius: 8px; overflow: hidden;">
            <div class="feedback-header" style="background-color: {color}; color: white; padding: 12px;">
                <h4 style="margin: 0; display: flex; align-items: center;">
                    <span style="margin-right: 8px;">{icon}</span>
                    단계 검증 결과
                    <span style="margin-left: auto; font-size: 0.9em; background: rgba(255,255,255,0.2); padding: 4px 8px; border-radius: 4px;">
                        점수: {score:.0f}/100
                    </span>
                </h4>
            </div>
            
            <div class="feedback-body" style="padding: 16px;">
                <div class="feedback-message" style="margin-bottom: 16px;">
                    <p style="margin: 0; font-size: 1.1em; font-weight: 500;">
                        {verification_result.get('message', '')}
                    </p>
                </div>
        """
        
        # 검증 세부사항
        if verification_result.get("details"):
            html += """
                <div class="verification-details" style="margin-bottom: 16px;">
                    <h5 style="color: #6c757d; margin-bottom: 8px;">🔍 검증 세부사항</h5>
                    <ul style="margin: 0; padding-left: 20px; font-size: 0.9em;">
            """
            
            for detail in verification_result["details"]:
                html += f"<li style='margin-bottom: 4px;'>{detail}</li>"
            
            html += """
                    </ul>
                </div>
            """
        
        # 힌트 섹션
        if hints and hints.get("success"):
            html += f"""
                <div class="hints-section" style="margin-bottom: 16px;">
                    <h5 style="color: #007bff; margin-bottom: 8px;">💡 힌트 ({hints.get('hint_level', '').title()} 수준)</h5>
                    <ul style="margin: 0; padding-left: 20px; font-size: 0.95em;">
            """
            
            for hint in hints.get("hints", []):
                html += f"<li style='margin-bottom: 6px; color: #495057;'>{hint}</li>"
            
            html += """
                    </ul>
                </div>
            """
        
        # 누락된 요소
        if verification_result.get("missing_elements"):
            html += """
                <div class="missing-elements" style="margin-bottom: 16px;">
                    <h5 style="color: #fd7e14; margin-bottom: 8px;">📋 누락된 요소</h5>
                    <ul style="margin: 0; padding-left: 20px; font-size: 0.9em; color: #6c757d;">
            """
            
            for element in verification_result["missing_elements"]:
                html += f"<li style='margin-bottom: 4px;'>{element}</li>"
            
            html += """
                    </ul>
                </div>
            """
        
        # 제안사항
        if verification_result.get("suggestions"):
            html += """
                <div class="suggestions" style="margin-bottom: 16px;">
                    <h5 style="color: #6f42c1; margin-bottom: 8px;">🎯 제안사항</h5>
                    <ul style="margin: 0; padding-left: 20px; font-size: 0.9em; color: #6c757d;">
            """
            
            for suggestion in verification_result["suggestions"]:
                html += f"<li style='margin-bottom: 4px;'>{suggestion}</li>"
            
            html += """
                    </ul>
                </div>
            """
        
        # 다음 단계 안내
        if success:
            html += """
                <div class="next-step" style="background: #d4edda; border: 1px solid #c3e6cb; border-radius: 4px; padding: 12px;">
                    <p style="margin: 0; color: #155724; font-weight: 500;">
                        🎉 단계를 성공적으로 완료했습니다! 다음 단계로 진행할 수 있습니다.
                    </p>
                </div>
            """
        else:
            html += """
                <div class="retry-encouragement" style="background: #fff3cd; border: 1px solid #ffeaa7; border-radius: 4px; padding: 12px;">
                    <p style="margin: 0; color: #856404; font-weight: 500;">
                        💪 포기하지 마세요! 힌트를 참고하여 다시 시도해보세요.
                    </p>
                </div>
            """
        
        html += """
            </div>
        </div>
        """
        
        return html
    
    def get_verification_statistics(self) -> Dict[str, Any]:
        """검증 통계 반환"""
        if not self.verification_history:
            return {"total_verifications": 0, "step_statistics": {}}
        
        step_stats = {}
        for record in self.verification_history:
            step_id = record["step_id"]
            if step_id not in step_stats:
                step_stats[step_id] = {
                    "attempts": 0,
                    "successes": 0,
                    "average_score": 0,
                    "scores": []
                }
            
            step_stats[step_id]["attempts"] += 1
            score = record["result"]["score"]
            step_stats[step_id]["scores"].append(score)
            
            if record["result"]["success"]:
                step_stats[step_id]["successes"] += 1
        
        # 평균 점수 계산
        for step_id, stats in step_stats.items():
            if stats["scores"]:
                stats["average_score"] = sum(stats["scores"]) / len(stats["scores"])
                stats["success_rate"] = (stats["successes"] / stats["attempts"]) * 100
        
        return {
            "total_verifications": len(self.verification_history),
            "step_statistics": step_stats
        }
    
    def _get_timestamp(self) -> str:
        """현재 시간 반환"""
        from datetime import datetime
        return datetime.now().isoformat()

# 검증 및 힌트 시스템 인스턴스 생성
verification_hint_system = VerificationHintSystem()