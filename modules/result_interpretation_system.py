"""
결과 해석 시스템 (Result Interpretation System)
- 통계적 의미와 실무적 해석 자동 생성
- 맥락에 맞는 해석 가이드 제공
- 요구사항 2.2 구현
"""

import re
import json
import numpy as np
import pandas as pd
from typing import Dict, Any, List, Optional, Tuple, Union
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import ast


class StatisticalConcept(Enum):
    """통계 개념 분류"""
    DESCRIPTIVE_STATS = "descriptive_statistics"
    CENTRAL_TENDENCY = "central_tendency"
    DISPERSION = "dispersion"
    CORRELATION = "correlation"
    PROBABILITY = "probability"
    HYPOTHESIS_TEST = "hypothesis_test"
    REGRESSION = "regression"
    VISUALIZATION = "visualization"


@dataclass
class InterpretationResult:
    """해석 결과"""
    statistical_meaning: str
    practical_interpretation: str
    key_insights: List[str]
    recommendations: List[str]
    context_notes: List[str]
    confidence_level: float  # 해석의 신뢰도 (0-1)
    
    def to_dict(self) -> Dict[str, Any]:
        """딕셔너리로 변환"""
        return {
            'statistical_meaning': self.statistical_meaning,
            'practical_interpretation': self.practical_interpretation,
            'key_insights': self.key_insights,
            'recommendations': self.recommendations,
            'context_notes': self.context_notes,
            'confidence_level': self.confidence_level
        }


class CodeAnalyzer:
    """코드 분석기"""
    
    def __init__(self):
        self.statistical_patterns = self._initialize_patterns()
    
    def _initialize_patterns(self) -> Dict[str, Dict[str, Any]]:
        """통계 패턴 초기화"""
        return {
            'mean': {
                'patterns': [r'\.mean\(\)', r'np\.mean\(', r'statistics\.mean\('],
                'concept': StatisticalConcept.CENTRAL_TENDENCY,
                'description': '평균 계산'
            },
            'median': {
                'patterns': [r'\.median\(\)', r'np\.median\(', r'statistics\.median\('],
                'concept': StatisticalConcept.CENTRAL_TENDENCY,
                'description': '중앙값 계산'
            },
            'mode': {
                'patterns': [r'\.mode\(\)', r'statistics\.mode\('],
                'concept': StatisticalConcept.CENTRAL_TENDENCY,
                'description': '최빈값 계산'
            },
            'std': {
                'patterns': [r'\.std\(\)', r'np\.std\(', r'statistics\.stdev\('],
                'concept': StatisticalConcept.DISPERSION,
                'description': '표준편차 계산'
            },
            'var': {
                'patterns': [r'\.var\(\)', r'np\.var\(', r'statistics\.variance\('],
                'concept': StatisticalConcept.DISPERSION,
                'description': '분산 계산'
            },
            'correlation': {
                'patterns': [r'\.corr\(\)', r'np\.corrcoef\(', r'pearsonr\('],
                'concept': StatisticalConcept.CORRELATION,
                'description': '상관관계 분석'
            },
            'histogram': {
                'patterns': [r'plt\.hist\(', r'\.hist\('],
                'concept': StatisticalConcept.VISUALIZATION,
                'description': '히스토그램 생성'
            },
            'scatter': {
                'patterns': [r'plt\.scatter\(', r'\.scatter\('],
                'concept': StatisticalConcept.VISUALIZATION,
                'description': '산점도 생성'
            },
            'boxplot': {
                'patterns': [r'plt\.boxplot\(', r'\.boxplot\('],
                'concept': StatisticalConcept.VISUALIZATION,
                'description': '박스플롯 생성'
            },
            'describe': {
                'patterns': [r'\.describe\(\)'],
                'concept': StatisticalConcept.DESCRIPTIVE_STATS,
                'description': '기술통계량 요약'
            }
        }
    
    def analyze_code(self, code: str) -> Dict[str, Any]:
        """코드 분석"""
        detected_operations = []
        concepts = set()
        
        for operation, info in self.statistical_patterns.items():
            for pattern in info['patterns']:
                if re.search(pattern, code):
                    detected_operations.append({
                        'operation': operation,
                        'description': info['description'],
                        'concept': info['concept']
                    })
                    concepts.add(info['concept'])
        
        # 변수 추출
        variables = self._extract_variables(code)
        
        # 데이터 타입 추정
        data_context = self._infer_data_context(code, variables)
        
        return {
            'detected_operations': detected_operations,
            'concepts': list(concepts),
            'variables': variables,
            'data_context': data_context
        }
    
    def _extract_variables(self, code: str) -> List[str]:
        """변수명 추출"""
        variables = []
        
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            variables.append(target.id)
        except:
            # AST 파싱 실패 시 정규식으로 대체
            var_pattern = r'(\w+)\s*='
            variables = re.findall(var_pattern, code)
        
        return list(set(variables))
    
    def _infer_data_context(self, code: str, variables: List[str]) -> Dict[str, str]:
        """데이터 맥락 추정"""
        context_keywords = {
            'score': '점수 데이터',
            'price': '가격 데이터',
            'age': '연령 데이터',
            'height': '신장 데이터',
            'weight': '체중 데이터',
            'income': '소득 데이터',
            'sales': '판매 데이터',
            'temperature': '온도 데이터',
            'time': '시간 데이터',
            'student': '학생 데이터',
            'exam': '시험 데이터'
        }
        
        inferred_context = {}
        
        for var in variables:
            var_lower = var.lower()
            for keyword, context in context_keywords.items():
                if keyword in var_lower:
                    inferred_context[var] = context
                    break
            else:
                inferred_context[var] = '일반 데이터'
        
        return inferred_context


class ResultAnalyzer:
    """결과 분석기"""
    
    def __init__(self):
        self.interpretation_templates = self._initialize_templates()
    
    def _initialize_templates(self) -> Dict[str, Dict[str, Any]]:
        """해석 템플릿 초기화"""
        return {
            'mean': {
                'statistical_meaning': "평균은 모든 데이터 값의 합을 데이터 개수로 나눈 값으로, 데이터의 중심 위치를 나타냅니다.",
                'interpretation_rules': [
                    {
                        'condition': lambda x: isinstance(x, (int, float)),
                        'template': "계산된 평균값은 {value:.2f}입니다. 이는 데이터가 이 값을 중심으로 분포되어 있음을 의미합니다."
                    }
                ],
                'insights': [
                    "평균은 이상치(outlier)에 민감하므로, 극값이 있는 경우 중앙값과 함께 고려해야 합니다.",
                    "정규분포에서 평균은 가장 효율적인 중심경향성 측도입니다."
                ]
            },
            'median': {
                'statistical_meaning': "중앙값은 데이터를 크기 순으로 정렬했을 때 가운데 위치하는 값으로, 이상치에 강건한 중심경향성 측도입니다.",
                'interpretation_rules': [
                    {
                        'condition': lambda x: isinstance(x, (int, float)),
                        'template': "중앙값은 {value:.2f}로, 전체 데이터의 50%가 이 값보다 작고 50%가 이 값보다 큽니다."
                    }
                ],
                'insights': [
                    "중앙값은 이상치의 영향을 받지 않아 왜곡된 분포에서 유용합니다.",
                    "평균과 중앙값의 차이가 클수록 데이터가 비대칭적으로 분포되어 있습니다."
                ]
            },
            'std': {
                'statistical_meaning': "표준편차는 데이터가 평균으로부터 얼마나 퍼져있는지를 나타내는 측도로, 분산의 제곱근입니다.",
                'interpretation_rules': [
                    {
                        'condition': lambda x: isinstance(x, (int, float)) and x < 1,
                        'template': "표준편차가 {value:.2f}로 작아서, 데이터가 평균 주변에 밀집되어 있습니다."
                    },
                    {
                        'condition': lambda x: isinstance(x, (int, float)) and x >= 1,
                        'template': "표준편차가 {value:.2f}로, 데이터가 평균으로부터 상당히 퍼져있습니다."
                    }
                ],
                'insights': [
                    "표준편차가 0에 가까울수록 데이터가 평균 주변에 집중되어 있습니다.",
                    "정규분포에서 약 68%의 데이터가 평균 ± 1표준편차 범위에 있습니다."
                ]
            },
            'correlation': {
                'statistical_meaning': "상관계수는 두 변수 간의 선형 관계의 강도와 방향을 나타내는 측도입니다.",
                'interpretation_rules': [
                    {
                        'condition': lambda x: isinstance(x, (int, float)) and abs(x) >= 0.7,
                        'template': "상관계수가 {value:.3f}로 강한 {direction} 상관관계를 보입니다."
                    },
                    {
                        'condition': lambda x: isinstance(x, (int, float)) and 0.3 <= abs(x) < 0.7,
                        'template': "상관계수가 {value:.3f}로 중간 정도의 {direction} 상관관계를 보입니다."
                    },
                    {
                        'condition': lambda x: isinstance(x, (int, float)) and abs(x) < 0.3,
                        'template': "상관계수가 {value:.3f}로 약한 상관관계를 보입니다."
                    }
                ],
                'insights': [
                    "상관관계는 인과관계를 의미하지 않습니다.",
                    "상관계수는 선형 관계만을 측정하므로, 비선형 관계는 놓칠 수 있습니다."
                ]
            }
        }
    
    def analyze_result(self, operation: str, result_value: Any, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """결과 분석"""
        if operation not in self.interpretation_templates:
            return self._create_generic_interpretation(operation, result_value)
        
        template = self.interpretation_templates[operation]
        
        # 통계적 의미
        statistical_meaning = template['statistical_meaning']
        
        # 실무적 해석 생성
        practical_interpretation = self._generate_practical_interpretation(
            operation, result_value, template['interpretation_rules']
        )
        
        # 주요 인사이트
        key_insights = template.get('insights', [])
        
        # 권장사항 생성
        recommendations = self._generate_recommendations(operation, result_value, context)
        
        return {
            'statistical_meaning': statistical_meaning,
            'practical_interpretation': practical_interpretation,
            'key_insights': key_insights,
            'recommendations': recommendations
        }
    
    def _generate_practical_interpretation(self, operation: str, value: Any, rules: List[Dict]) -> str:
        """실무적 해석 생성"""
        for rule in rules:
            if rule['condition'](value):
                template = rule['template']
                
                # 상관관계의 경우 방향 정보 추가
                if operation == 'correlation' and isinstance(value, (int, float)):
                    direction = '양의' if value > 0 else '음의'
                    return template.format(value=value, direction=direction)
                else:
                    return template.format(value=value)
        
        # 기본 해석
        return f"{operation} 연산의 결과는 {value}입니다."
    
    def _generate_recommendations(self, operation: str, value: Any, context: Dict[str, Any] = None) -> List[str]:
        """권장사항 생성"""
        recommendations = []
        
        if operation == 'mean':
            recommendations.extend([
                "중앙값과 비교하여 데이터의 분포 특성을 파악해보세요.",
                "히스토그램을 그려서 데이터의 분포를 시각적으로 확인해보세요."
            ])
        
        elif operation == 'std':
            if isinstance(value, (int, float)):
                if value > 10:  # 임의의 기준
                    recommendations.append("표준편차가 큰 편이므로 이상치가 있는지 확인해보세요.")
                recommendations.append("변동계수(CV = 표준편차/평균)를 계산하여 상대적 변동성을 확인해보세요.")
        
        elif operation == 'correlation':
            if isinstance(value, (int, float)):
                if abs(value) > 0.5:
                    recommendations.append("강한 상관관계가 발견되었으므로 산점도를 그려서 관계를 시각화해보세요.")
                recommendations.append("상관관계가 인과관계를 의미하지 않음을 유의하세요.")
        
        return recommendations
    
    def _create_generic_interpretation(self, operation: str, value: Any) -> Dict[str, Any]:
        """일반적인 해석 생성"""
        return {
            'statistical_meaning': f"{operation} 연산이 수행되었습니다.",
            'practical_interpretation': f"결과값은 {value}입니다.",
            'key_insights': ["추가적인 분석이 필요합니다."],
            'recommendations': ["결과를 다른 통계량과 함께 해석해보세요."]
        }


class ResultInterpreter:
    """결과 해석기 (메인 클래스)"""
    
    def __init__(self):
        self.code_analyzer = CodeAnalyzer()
        self.result_analyzer = ResultAnalyzer()
        self.interpretation_history = []
    
    def interpret_execution_result(self, code: str, execution_output: str, 
                                 execution_result: Dict[str, Any] = None) -> InterpretationResult:
        """실행 결과 해석"""
        # 1. 코드 분석
        code_analysis = self.code_analyzer.analyze_code(code)
        
        # 2. 출력에서 수치 결과 추출
        extracted_values = self._extract_numerical_results(execution_output)
        
        # 3. 각 연산에 대한 해석 생성
        interpretations = []
        
        for operation_info in code_analysis['detected_operations']:
            operation = operation_info['operation']
            
            # 해당 연산의 결과값 찾기
            result_value = self._find_result_for_operation(operation, extracted_values, execution_output)
            
            if result_value is not None:
                analysis = self.result_analyzer.analyze_result(
                    operation, result_value, code_analysis['data_context']
                )
                interpretations.append({
                    'operation': operation,
                    'description': operation_info['description'],
                    'analysis': analysis
                })
        
        # 4. 통합 해석 생성
        integrated_interpretation = self._create_integrated_interpretation(
            interpretations, code_analysis, execution_output
        )
        
        # 5. 해석 기록 저장
        self.interpretation_history.append({
            'code': code,
            'output': execution_output,
            'interpretation': integrated_interpretation.to_dict(),
            'timestamp': datetime.now().isoformat()
        })
        
        return integrated_interpretation
    
    def _extract_numerical_results(self, output: str) -> List[Dict[str, Any]]:
        """출력에서 수치 결과 추출"""
        results = []
        
        # 숫자 패턴 찾기
        number_patterns = [
            r'평균[:\s]*([0-9]+\.?[0-9]*)',
            r'중앙값[:\s]*([0-9]+\.?[0-9]*)',
            r'표준편차[:\s]*([0-9]+\.?[0-9]*)',
            r'분산[:\s]*([0-9]+\.?[0-9]*)',
            r'상관계수[:\s]*([0-9\-]+\.?[0-9]*)',
            r'결과[:\s]*([0-9\-]+\.?[0-9]*)',
            r'([0-9\-]+\.?[0-9]+)'  # 일반적인 숫자
        ]
        
        for pattern in number_patterns:
            matches = re.findall(pattern, output)
            for match in matches:
                try:
                    value = float(match)
                    results.append({
                        'value': value,
                        'context': pattern,
                        'raw_match': match
                    })
                except ValueError:
                    continue
        
        return results
    
    def _find_result_for_operation(self, operation: str, extracted_values: List[Dict], 
                                 output: str) -> Optional[float]:
        """특정 연산의 결과값 찾기"""
        # 연산별 키워드 매핑
        operation_keywords = {
            'mean': ['평균', 'mean'],
            'median': ['중앙값', 'median'],
            'std': ['표준편차', 'std'],
            'var': ['분산', 'var', 'variance'],
            'correlation': ['상관', 'corr', 'correlation']
        }
        
        keywords = operation_keywords.get(operation, [operation])
        
        # 키워드와 매칭되는 값 찾기
        for result in extracted_values:
            for keyword in keywords:
                if keyword in output.lower():
                    return result['value']
        
        # 매칭되는 값이 없으면 첫 번째 값 반환
        if extracted_values:
            return extracted_values[0]['value']
        
        return None
    
    def _create_integrated_interpretation(self, interpretations: List[Dict], 
                                       code_analysis: Dict, output: str) -> InterpretationResult:
        """통합 해석 생성"""
        if not interpretations:
            return InterpretationResult(
                statistical_meaning="코드가 실행되었지만 인식된 통계 연산이 없습니다.",
                practical_interpretation="출력을 확인하여 결과를 해석해보세요.",
                key_insights=["추가적인 분석이 필요합니다."],
                recommendations=["통계 함수를 사용하여 데이터를 분석해보세요."],
                context_notes=[],
                confidence_level=0.3
            )
        
        # 주요 해석 통합
        statistical_meanings = []
        practical_interpretations = []
        all_insights = []
        all_recommendations = []
        
        for interp in interpretations:
            analysis = interp['analysis']
            statistical_meanings.append(f"• {interp['description']}: {analysis['statistical_meaning']}")
            practical_interpretations.append(analysis['practical_interpretation'])
            all_insights.extend(analysis['key_insights'])
            all_recommendations.extend(analysis['recommendations'])
        
        # 중복 제거
        unique_insights = list(set(all_insights))
        unique_recommendations = list(set(all_recommendations))
        
        # 맥락 노트 생성
        context_notes = []
        if code_analysis['data_context']:
            context_notes.append(f"분석된 데이터 유형: {', '.join(code_analysis['data_context'].values())}")
        
        # 신뢰도 계산 (간단한 휴리스틱)
        confidence = min(0.9, 0.5 + len(interpretations) * 0.1)
        
        return InterpretationResult(
            statistical_meaning='\n'.join(statistical_meanings),
            practical_interpretation='\n'.join(practical_interpretations),
            key_insights=unique_insights[:5],  # 상위 5개만
            recommendations=unique_recommendations[:5],  # 상위 5개만
            context_notes=context_notes,
            confidence_level=confidence
        )
    
    def get_interpretation_history(self) -> List[Dict[str, Any]]:
        """해석 기록 조회"""
        return self.interpretation_history.copy()
    
    def clear_history(self):
        """해석 기록 삭제"""
        self.interpretation_history.clear()
    
    def interpret_statistical_concept(self, concept: str) -> Dict[str, str]:
        """통계 개념 해석"""
        concept_explanations = {
            'mean': {
                'definition': '평균은 모든 데이터 값의 합을 데이터 개수로 나눈 값입니다.',
                'when_to_use': '데이터가 정규분포를 따르고 이상치가 적을 때 사용합니다.',
                'limitations': '이상치에 민감하며, 왜곡된 분포에서는 대표값으로 부적절할 수 있습니다.',
                'example': '학생 5명의 점수가 [80, 85, 90, 95, 100]일 때, 평균은 90점입니다.'
            },
            'median': {
                'definition': '중앙값은 데이터를 크기 순으로 정렬했을 때 가운데 위치하는 값입니다.',
                'when_to_use': '이상치가 있거나 분포가 왜곡되어 있을 때 사용합니다.',
                'limitations': '모든 데이터 정보를 활용하지 않으며, 작은 표본에서는 불안정할 수 있습니다.',
                'example': '소득 데이터 [30, 35, 40, 45, 200]에서 중앙값은 40으로, 평균(70)보다 대표성이 높습니다.'
            },
            'std': {
                'definition': '표준편차는 데이터가 평균으로부터 얼마나 퍼져있는지를 나타내는 측도입니다.',
                'when_to_use': '데이터의 변동성이나 일관성을 평가할 때 사용합니다.',
                'limitations': '이상치에 민감하며, 분포의 형태에 대한 정보는 제공하지 않습니다.',
                'example': '두 반의 평균 점수가 같아도 표준편차가 다르면 점수 분포의 일관성이 다릅니다.'
            }
        }
        
        return concept_explanations.get(concept, {
            'definition': f'{concept}에 대한 설명이 준비되지 않았습니다.',
            'when_to_use': '추가 정보가 필요합니다.',
            'limitations': '추가 정보가 필요합니다.',
            'example': '예제가 준비되지 않았습니다.'
        })


# 테스트 함수
def test_result_interpreter():
    """결과 해석기 테스트"""
    interpreter = ResultInterpreter()
    
    test_cases = [
        {
            'name': '평균 계산',
            'code': '''
import numpy as np
data = [85, 90, 78, 92, 88]
mean_value = np.mean(data)
print(f"평균: {mean_value}")
            ''',
            'output': '평균: 86.6'
        },
        {
            'name': '기술통계량 요약',
            'code': '''
import pandas as pd
scores = [75, 80, 85, 90, 95, 100]
df = pd.DataFrame({'scores': scores})
print(df.describe())
            ''',
            'output': '''       scores
count    6.000000
mean    87.500000
std      9.354143
min     75.000000
25%     81.250000
50%     87.500000
75%     93.750000
max    100.000000'''
        },
        {
            'name': '상관관계 분석',
            'code': '''
import numpy as np
x = [1, 2, 3, 4, 5]
y = [2, 4, 6, 8, 10]
correlation = np.corrcoef(x, y)[0, 1]
print(f"상관계수: {correlation}")
            ''',
            'output': '상관계수: 1.0'
        }
    ]
    
    results = []
    
    for test_case in test_cases:
        print(f"\n🧪 테스트: {test_case['name']}")
        print("-" * 50)
        
        interpretation = interpreter.interpret_execution_result(
            test_case['code'], 
            test_case['output']
        )
        
        print(f"📊 통계적 의미:")
        print(interpretation.statistical_meaning)
        
        print(f"\n💡 실무적 해석:")
        print(interpretation.practical_interpretation)
        
        print(f"\n🔍 주요 인사이트:")
        for insight in interpretation.key_insights:
            print(f"  • {insight}")
        
        print(f"\n📋 권장사항:")
        for rec in interpretation.recommendations:
            print(f"  • {rec}")
        
        print(f"\n신뢰도: {interpretation.confidence_level:.1%}")
        
        results.append({
            'name': test_case['name'],
            'confidence': interpretation.confidence_level,
            'insights_count': len(interpretation.key_insights),
            'recommendations_count': len(interpretation.recommendations)
        })
    
    return results


if __name__ == "__main__":
    print("🔍 결과 해석 시스템 테스트")
    print("=" * 60)
    
    test_results = test_result_interpreter()
    
    print(f"\n📊 테스트 요약")
    print("=" * 30)
    
    total_tests = len(test_results)
    avg_confidence = sum(r['confidence'] for r in test_results) / total_tests
    total_insights = sum(r['insights_count'] for r in test_results)
    total_recommendations = sum(r['recommendations_count'] for r in test_results)
    
    print(f"전체 테스트: {total_tests}개")
    print(f"평균 신뢰도: {avg_confidence:.1%}")
    print(f"생성된 인사이트: {total_insights}개")
    print(f"생성된 권장사항: {total_recommendations}개")
    
    print(f"\n✅ Task 2.2 결과 해석 시스템 구현 완료!")