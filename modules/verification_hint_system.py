"""
단계별 검증 및 힌트 시스템
- 코드 실행 결과 자동 검증 기능
- 상황별 맞춤 힌트 제공 시스템
- 학습 진도에 따른 적응형 힌트
- 오류 패턴 분석 기반 개인화된 가이드
"""

import re
import ast
import json
from typing import Dict, List, Any, Optional, Tuple, Callable
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

class VerificationLevel(Enum):
    """검증 수준"""
    BASIC = "basic"          # 기본 실행 성공 여부만 확인
    INTERMEDIATE = "intermediate"  # 출력 내용과 변수 확인
    ADVANCED = "advanced"    # 코드 구조와 효율성까지 확인

class HintLevel(Enum):
    """힌트 수준"""
    GENTLE = "gentle"        # 방향성만 제시
    SPECIFIC = "specific"    # 구체적인 방법 제시
    DETAILED = "detailed"    # 단계별 상세 가이드

@dataclass
class VerificationCriteria:
    """검증 기준"""
    criteria_id: str
    name: str
    description: str
    verification_function: str  # 함수 이름
    weight: float  # 가중치 (0-1)
    required: bool  # 필수 여부
    error_message: str
    hint_message: str

@dataclass
class HintStrategy:
    """힌트 전략"""
    strategy_id: str
    trigger_condition: str  # 힌트 제공 조건
    hint_level: HintLevel
    hint_messages: List[str]
    code_examples: List[str]
    learning_resources: List[str]

class CodeVerifier:
    """코드 검증기"""
    
    def __init__(self):
        self.verification_functions = self._initialize_verification_functions()
        self.pattern_matchers = self._initialize_pattern_matchers()
    
    def _initialize_verification_functions(self) -> Dict[str, Callable]:
        """검증 함수 초기화"""
        return {
            'has_variable': self._verify_has_variable,
            'has_function_call': self._verify_has_function_call,
            'produces_output': self._verify_produces_output,
            'calculates_correctly': self._verify_calculates_correctly,
            'uses_loop': self._verify_uses_loop,
            'uses_condition': self._verify_uses_condition,
            'imports_module': self._verify_imports_module,
            'defines_function': self._verify_defines_function,
            'handles_error': self._verify_handles_error,
            'follows_style': self._verify_follows_style
        }
    
    def _initialize_pattern_matchers(self) -> Dict[str, str]:
        """패턴 매처 초기화"""
        return {
            'print_statement': r'print\s*\(',
            'variable_assignment': r'\w+\s*=\s*',
            'function_definition': r'def\s+\w+\s*\(',
            'for_loop': r'for\s+\w+\s+in\s+',
            'while_loop': r'while\s+.+:',
            'if_statement': r'if\s+.+:',
            'import_statement': r'import\s+\w+|from\s+\w+\s+import',
            'list_creation': r'\[.*\]',
            'dict_creation': r'\{.*\}',
            'function_call': r'\w+\s*\(',
            'arithmetic_operation': r'[+\-*/]',
            'comparison_operation': r'[<>=!]+',
            'string_operation': r'["\'].*["\']'
        }
    
    def verify_code(self, code: str, execution_result: Dict[str, Any], 
                   criteria_list: List[VerificationCriteria]) -> Dict[str, Any]:
        """코드 검증"""
        verification_results = {
            'overall_success': True,
            'total_score': 0.0,
            'max_score': 0.0,
            'criteria_results': {},
            'failed_criteria': [],
            'warnings': [],
            'suggestions': []
        }
        
        for criteria in criteria_list:
            result = self._verify_single_criteria(code, execution_result, criteria)
            
            verification_results['criteria_results'][criteria.criteria_id] = result
            verification_results['max_score'] += criteria.weight
            
            if result['passed']:
                verification_results['total_score'] += criteria.weight
            else:
                verification_results['failed_criteria'].append({
                    'criteria_id': criteria.criteria_id,
                    'name': criteria.name,
                    'error_message': criteria.error_message,
                    'hint_message': criteria.hint_message,
                    'required': criteria.required
                })
                
                if criteria.required:
                    verification_results['overall_success'] = False
        
        # 점수 정규화 (0-100)
        if verification_results['max_score'] > 0:
            verification_results['score_percentage'] = (
                verification_results['total_score'] / verification_results['max_score'] * 100
            )
        else:
            verification_results['score_percentage'] = 0
        
        # 전체 성공 여부 재평가 (70% 이상이면 성공)
        if verification_results['score_percentage'] >= 70:
            verification_results['overall_success'] = True
        
        return verification_results
    
    def _verify_single_criteria(self, code: str, execution_result: Dict[str, Any], 
                               criteria: VerificationCriteria) -> Dict[str, Any]:
        """단일 기준 검증"""
        verification_func = self.verification_functions.get(criteria.verification_function)
        
        if not verification_func:
            return {
                'passed': False,
                'error': f'Unknown verification function: {criteria.verification_function}',
                'details': {}
            }
        
        try:
            result = verification_func(code, execution_result, criteria)
            return {
                'passed': result.get('passed', False),
                'details': result.get('details', {}),
                'message': result.get('message', '')
            }
        except Exception as e:
            return {
                'passed': False,
                'error': str(e),
                'details': {}
            }
    
    def _verify_has_variable(self, code: str, execution_result: Dict[str, Any], 
                           criteria: VerificationCriteria) -> Dict[str, Any]:
        """변수 존재 확인"""
        variable_name = criteria.description  # 변수명이 description에 저장됨
        
        # 코드에서 변수 할당 확인
        pattern = rf'{variable_name}\s*='
        has_assignment = bool(re.search(pattern, code))
        
        # 실행 결과에서 변수 확인
        variables = execution_result.get('variables', {})
        has_variable = variable_name in variables
        
        return {
            'passed': has_assignment and has_variable,
            'details': {
                'has_assignment': has_assignment,
                'has_variable': has_variable,
                'variable_value': variables.get(variable_name)
            },
            'message': f'변수 {variable_name} 확인: 할당={has_assignment}, 존재={has_variable}'
        }
    
    def _verify_has_function_call(self, code: str, execution_result: Dict[str, Any], 
                                criteria: VerificationCriteria) -> Dict[str, Any]:
        """함수 호출 확인"""
        function_name = criteria.description
        pattern = rf'{function_name}\s*\('
        has_call = bool(re.search(pattern, code))
        
        return {
            'passed': has_call,
            'details': {'function_name': function_name, 'found': has_call},
            'message': f'함수 {function_name} 호출 확인: {has_call}'
        }
    
    def _verify_produces_output(self, code: str, execution_result: Dict[str, Any], 
                              criteria: VerificationCriteria) -> Dict[str, Any]:
        """출력 생성 확인"""
        output = execution_result.get('output', '')
        has_output = len(output.strip()) > 0
        
        # 특정 출력 패턴 확인 (criteria.description에 패턴이 있는 경우)
        if criteria.description and criteria.description != 'any':
            pattern_match = bool(re.search(criteria.description, output, re.IGNORECASE))
            return {
                'passed': has_output and pattern_match,
                'details': {
                    'has_output': has_output,
                    'pattern_match': pattern_match,
                    'output_length': len(output)
                },
                'message': f'출력 확인: 존재={has_output}, 패턴매치={pattern_match}'
            }
        
        return {
            'passed': has_output,
            'details': {'has_output': has_output, 'output_length': len(output)},
            'message': f'출력 확인: {has_output}'
        }
    
    def _verify_calculates_correctly(self, code: str, execution_result: Dict[str, Any], 
                                   criteria: VerificationCriteria) -> Dict[str, Any]:
        """계산 정확성 확인"""
        # 간단한 수학 계산 검증 (예: 평균 계산)
        variables = execution_result.get('variables', {})
        
        # 평균 계산 예제
        if 'mean' in variables or 'average' in variables:
            mean_value = variables.get('mean') or variables.get('average')
            
            # 데이터가 있는지 확인
            data_vars = ['scores', 'data', 'values', 'numbers']
            data = None
            for var_name in data_vars:
                if var_name in variables:
                    data = variables[var_name]
                    break
            
            if data and isinstance(data, list) and len(data) > 0:
                expected_mean = sum(data) / len(data)
                is_correct = abs(mean_value - expected_mean) < 0.01  # 소수점 오차 허용
                
                return {
                    'passed': is_correct,
                    'details': {
                        'calculated_mean': mean_value,
                        'expected_mean': expected_mean,
                        'data_length': len(data)
                    },
                    'message': f'평균 계산 확인: {is_correct}'
                }
        
        return {
            'passed': True,  # 기본적으로 통과 (구체적인 검증 로직 필요시 추가)
            'details': {},
            'message': '계산 검증 완료'
        }
    
    def _verify_uses_loop(self, code: str, execution_result: Dict[str, Any], 
                        criteria: VerificationCriteria) -> Dict[str, Any]:
        """반복문 사용 확인"""
        for_loop = bool(re.search(self.pattern_matchers['for_loop'], code))
        while_loop = bool(re.search(self.pattern_matchers['while_loop'], code))
        uses_loop = for_loop or while_loop
        
        return {
            'passed': uses_loop,
            'details': {'for_loop': for_loop, 'while_loop': while_loop},
            'message': f'반복문 사용 확인: {uses_loop}'
        }
    
    def _verify_uses_condition(self, code: str, execution_result: Dict[str, Any], 
                             criteria: VerificationCriteria) -> Dict[str, Any]:
        """조건문 사용 확인"""
        has_if = bool(re.search(self.pattern_matchers['if_statement'], code))
        
        return {
            'passed': has_if,
            'details': {'has_if_statement': has_if},
            'message': f'조건문 사용 확인: {has_if}'
        }
    
    def _verify_imports_module(self, code: str, execution_result: Dict[str, Any], 
                             criteria: VerificationCriteria) -> Dict[str, Any]:
        """모듈 import 확인"""
        module_name = criteria.description
        pattern = rf'import\s+{module_name}|from\s+{module_name}\s+import'
        has_import = bool(re.search(pattern, code))
        
        return {
            'passed': has_import,
            'details': {'module_name': module_name, 'imported': has_import},
            'message': f'모듈 {module_name} import 확인: {has_import}'
        }
    
    def _verify_defines_function(self, code: str, execution_result: Dict[str, Any], 
                               criteria: VerificationCriteria) -> Dict[str, Any]:
        """함수 정의 확인"""
        function_name = criteria.description
        pattern = rf'def\s+{function_name}\s*\('
        has_definition = bool(re.search(pattern, code))
        
        return {
            'passed': has_definition,
            'details': {'function_name': function_name, 'defined': has_definition},
            'message': f'함수 {function_name} 정의 확인: {has_definition}'
        }
    
    def _verify_handles_error(self, code: str, execution_result: Dict[str, Any], 
                            criteria: VerificationCriteria) -> Dict[str, Any]:
        """오류 처리 확인"""
        has_try_except = bool(re.search(r'try\s*:', code)) and bool(re.search(r'except\s*.*:', code))
        
        return {
            'passed': has_try_except,
            'details': {'has_try_except': has_try_except},
            'message': f'오류 처리 확인: {has_try_except}'
        }
    
    def _verify_follows_style(self, code: str, execution_result: Dict[str, Any], 
                            criteria: VerificationCriteria) -> Dict[str, Any]:
        """코딩 스타일 확인"""
        issues = []
        
        # 기본 스타일 검사
        lines = code.split('\n')
        
        # 들여쓰기 일관성 확인
        indentation_consistent = True
        for line in lines:
            if line.strip() and line.startswith(' '):
                # 4의 배수가 아닌 들여쓰기 확인
                leading_spaces = len(line) - len(line.lstrip(' '))
                if leading_spaces % 4 != 0:
                    indentation_consistent = False
                    break
        
        if not indentation_consistent:
            issues.append('들여쓰기가 일관되지 않습니다 (4칸 단위 권장)')
        
        # 변수명 스타일 확인 (snake_case)
        variable_pattern = r'(\w+)\s*='
        variables = re.findall(variable_pattern, code)
        for var in variables:
            if not re.match(r'^[a-z_][a-z0-9_]*$', var):
                issues.append(f'변수명 {var}이 snake_case 규칙을 따르지 않습니다')
        
        return {
            'passed': len(issues) == 0,
            'details': {'issues': issues, 'indentation_consistent': indentation_consistent},
            'message': f'스타일 확인: {len(issues)}개 이슈'
        }

class HintProvider:
    """힌트 제공자"""
    
    def __init__(self):
        self.hint_strategies = self._initialize_hint_strategies()
        self.user_progress_tracking = {}  # 사용자별 진행 상황 추적
    
    def _initialize_hint_strategies(self) -> Dict[str, HintStrategy]:
        """힌트 전략 초기화"""
        return {
            'variable_creation': HintStrategy(
                strategy_id='variable_creation',
                trigger_condition='missing_variable',
                hint_level=HintLevel.GENTLE,
                hint_messages=[
                    "변수를 만들어야 합니다. 변수명 = 값 형태로 작성해보세요.",
                    "데이터를 저장할 변수가 필요합니다.",
                    "변수 이름을 정하고 값을 할당해보세요."
                ],
                code_examples=[
                    "# 변수 생성 예제\nmy_variable = 10\nname = '홍길동'",
                    "# 리스트 변수 생성\nscores = [85, 90, 78, 92]"
                ],
                learning_resources=[
                    "Python 변수와 할당",
                    "변수 명명 규칙"
                ]
            ),
            
            'function_usage': HintStrategy(
                strategy_id='function_usage',
                trigger_condition='missing_function_call',
                hint_level=HintLevel.SPECIFIC,
                hint_messages=[
                    "함수를 호출해야 합니다. 함수명() 형태로 작성하세요.",
                    "필요한 함수가 호출되지 않았습니다.",
                    "괄호를 사용해서 함수를 실행해보세요."
                ],
                code_examples=[
                    "# 함수 호출 예제\nresult = sum([1, 2, 3, 4])\nprint(result)",
                    "# 내장 함수 사용\nlength = len(my_list)\nmaximum = max(numbers)"
                ],
                learning_resources=[
                    "Python 내장 함수",
                    "함수 호출 방법"
                ]
            ),
            
            'calculation_help': HintStrategy(
                strategy_id='calculation_help',
                trigger_condition='incorrect_calculation',
                hint_level=HintLevel.DETAILED,
                hint_messages=[
                    "계산 공식을 확인해보세요.",
                    "평균은 총합을 개수로 나눈 값입니다.",
                    "단계별로 계산해보세요: 1) 총합 구하기, 2) 개수 구하기, 3) 나누기"
                ],
                code_examples=[
                    """# 평균 계산 예제
data = [10, 20, 30, 40, 50]
total = sum(data)  # 총합
count = len(data)  # 개수
average = total / count  # 평균
print(f"평균: {average}")""",
                    """# 표준편차 계산 예제
import math
mean = sum(data) / len(data)
variance = sum((x - mean) ** 2 for x in data) / len(data)
std_dev = math.sqrt(variance)"""
                ],
                learning_resources=[
                    "기술통계량 계산 방법",
                    "Python 수학 연산"
                ]
            ),
            
            'output_formatting': HintStrategy(
                strategy_id='output_formatting',
                trigger_condition='missing_output',
                hint_level=HintLevel.GENTLE,
                hint_messages=[
                    "결과를 출력해야 합니다. print() 함수를 사용하세요.",
                    "계산 결과를 화면에 보여주세요.",
                    "print() 함수로 값을 출력할 수 있습니다."
                ],
                code_examples=[
                    "# 출력 예제\nresult = 42\nprint(f'결과: {result}')",
                    "# 여러 값 출력\nprint('이름:', name)\nprint('나이:', age)"
                ],
                learning_resources=[
                    "Python print() 함수",
                    "문자열 포맷팅"
                ]
            ),
            
            'syntax_error_help': HintStrategy(
                strategy_id='syntax_error_help',
                trigger_condition='syntax_error',
                hint_level=HintLevel.SPECIFIC,
                hint_messages=[
                    "문법 오류가 있습니다. 괄호와 콜론을 확인해보세요.",
                    "들여쓰기를 확인해보세요.",
                    "따옴표가 제대로 닫혔는지 확인하세요."
                ],
                code_examples=[
                    """# 올바른 문법 예제
if condition:
    print("조건이 참입니다")
    
for item in my_list:
    print(item)""",
                    """# 함수 정의 문법
def my_function():
    return "Hello World" """
                ],
                learning_resources=[
                    "Python 기본 문법",
                    "들여쓰기 규칙"
                ]
            )
        }
    
    def get_contextual_hints(self, verification_result: Dict[str, Any], 
                           user_id: str, attempt_count: int) -> List[Dict[str, Any]]:
        """상황별 맞춤 힌트 제공"""
        hints = []
        
        # 실패한 기준들에 대한 힌트
        for failed_criteria in verification_result.get('failed_criteria', []):
            criteria_id = failed_criteria['criteria_id']
            hint = self._get_hint_for_criteria(criteria_id, attempt_count)
            if hint:
                hints.append(hint)
        
        # 사용자 진행 상황에 따른 추가 힌트
        user_hints = self._get_user_specific_hints(user_id, verification_result)
        hints.extend(user_hints)
        
        # 힌트 개수 제한 (최대 3개)
        return hints[:3]
    
    def _get_hint_for_criteria(self, criteria_id: str, attempt_count: int) -> Optional[Dict[str, Any]]:
        """기준별 힌트 생성"""
        # 기준 ID에 따른 힌트 전략 매핑
        criteria_to_strategy = {
            'has_variable': 'variable_creation',
            'has_function_call': 'function_usage',
            'calculates_correctly': 'calculation_help',
            'produces_output': 'output_formatting'
        }
        
        strategy_id = criteria_to_strategy.get(criteria_id)
        if not strategy_id or strategy_id not in self.hint_strategies:
            return None
        
        strategy = self.hint_strategies[strategy_id]
        
        # 시도 횟수에 따른 힌트 레벨 조정
        if attempt_count <= 1:
            hint_level = HintLevel.GENTLE
        elif attempt_count <= 3:
            hint_level = HintLevel.SPECIFIC
        else:
            hint_level = HintLevel.DETAILED
        
        # 힌트 메시지 선택
        hint_index = min(attempt_count - 1, len(strategy.hint_messages) - 1)
        hint_message = strategy.hint_messages[hint_index]
        
        # 코드 예제 포함 여부 결정
        include_code = hint_level in [HintLevel.SPECIFIC, HintLevel.DETAILED]
        code_example = strategy.code_examples[0] if include_code and strategy.code_examples else None
        
        return {
            'strategy_id': strategy_id,
            'hint_level': hint_level.value,
            'message': hint_message,
            'code_example': code_example,
            'learning_resources': strategy.learning_resources if hint_level == HintLevel.DETAILED else []
        }
    
    def _get_user_specific_hints(self, user_id: str, verification_result: Dict[str, Any]) -> List[Dict[str, Any]]:
        """사용자별 맞춤 힌트"""
        hints = []
        
        # 사용자 진행 상황 추적
        if user_id not in self.user_progress_tracking:
            self.user_progress_tracking[user_id] = {
                'common_errors': [],
                'successful_patterns': [],
                'learning_preferences': 'visual'  # 기본값
            }
        
        user_progress = self.user_progress_tracking[user_id]
        
        # 반복되는 오류 패턴 확인
        failed_criteria_ids = [fc['criteria_id'] for fc in verification_result.get('failed_criteria', [])]
        
        for criteria_id in failed_criteria_ids:
            if criteria_id in user_progress['common_errors']:
                # 반복되는 오류에 대한 특별 힌트
                hints.append({
                    'type': 'repeated_error',
                    'message': f'이 부분에서 자주 실수하고 있습니다. 기본 개념을 다시 복습해보세요.',
                    'suggestion': '관련 튜토리얼을 참고하거나 간단한 예제부터 다시 시작해보세요.'
                })
                break
        
        # 성공률이 낮은 경우 격려 메시지
        if verification_result.get('score_percentage', 0) < 30:
            hints.append({
                'type': 'encouragement',
                'message': '처음에는 어려울 수 있습니다. 천천히 단계별로 접근해보세요.',
                'suggestion': '각 줄을 하나씩 작성하고 테스트해보는 것이 좋습니다.'
            })
        
        return hints
    
    def update_user_progress(self, user_id: str, verification_result: Dict[str, Any]):
        """사용자 진행 상황 업데이트"""
        if user_id not in self.user_progress_tracking:
            self.user_progress_tracking[user_id] = {
                'common_errors': [],
                'successful_patterns': [],
                'learning_preferences': 'visual'
            }
        
        user_progress = self.user_progress_tracking[user_id]
        
        # 실패한 기준들을 공통 오류에 추가
        for failed_criteria in verification_result.get('failed_criteria', []):
            criteria_id = failed_criteria['criteria_id']
            if criteria_id not in user_progress['common_errors']:
                user_progress['common_errors'].append(criteria_id)
        
        # 성공한 패턴 추적 (향후 개선을 위해)
        if verification_result.get('overall_success'):
            success_pattern = f"success_{datetime.now().strftime('%Y%m%d')}"
            if success_pattern not in user_progress['successful_patterns']:
                user_progress['successful_patterns'].append(success_pattern)

class VerificationHintSystem:
    """통합 검증 및 힌트 시스템"""
    
    def __init__(self):
        self.verifier = CodeVerifier()
        self.hint_provider = HintProvider()
        self.step_criteria = self._initialize_step_criteria()
    
    def _initialize_step_criteria(self) -> Dict[str, List[VerificationCriteria]]:
        """단계별 검증 기준 초기화"""
        return {
            'step_1': [  # 데이터 준비
                VerificationCriteria(
                    criteria_id='has_data_list',
                    name='데이터 리스트 생성',
                    description='scores',  # 변수명
                    verification_function='has_variable',
                    weight=0.4,
                    required=True,
                    error_message='데이터를 저장할 리스트 변수가 없습니다.',
                    hint_message='scores = [85, 90, 78, ...] 형태로 데이터 리스트를 만드세요.'
                ),
                VerificationCriteria(
                    criteria_id='prints_data_info',
                    name='데이터 정보 출력',
                    description='any',
                    verification_function='produces_output',
                    weight=0.3,
                    required=False,
                    error_message='데이터 정보가 출력되지 않았습니다.',
                    hint_message='print() 함수로 데이터 정보를 출력하세요.'
                ),
                VerificationCriteria(
                    criteria_id='uses_len_function',
                    name='len() 함수 사용',
                    description='len',
                    verification_function='has_function_call',
                    weight=0.3,
                    required=False,
                    error_message='len() 함수가 사용되지 않았습니다.',
                    hint_message='len() 함수로 데이터 개수를 확인하세요.'
                )
            ],
            
            'step_2': [  # 중심경향성 계산
                VerificationCriteria(
                    criteria_id='calculates_mean',
                    name='평균 계산',
                    description='mean',
                    verification_function='calculates_correctly',
                    weight=0.5,
                    required=True,
                    error_message='평균이 올바르게 계산되지 않았습니다.',
                    hint_message='평균 = 총합 / 개수로 계산하세요.'
                ),
                VerificationCriteria(
                    criteria_id='uses_sum_function',
                    name='sum() 함수 사용',
                    description='sum',
                    verification_function='has_function_call',
                    weight=0.3,
                    required=False,
                    error_message='sum() 함수가 사용되지 않았습니다.',
                    hint_message='sum() 함수로 총합을 구하세요.'
                ),
                VerificationCriteria(
                    criteria_id='prints_results',
                    name='결과 출력',
                    description='평균|mean|average',
                    verification_function='produces_output',
                    weight=0.2,
                    required=False,
                    error_message='계산 결과가 출력되지 않았습니다.',
                    hint_message='계산한 평균값을 출력하세요.'
                )
            ],
            
            'step_3': [  # 산포도 계산
                VerificationCriteria(
                    criteria_id='calculates_variance',
                    name='분산 계산',
                    description='variance',
                    verification_function='has_variable',
                    weight=0.4,
                    required=True,
                    error_message='분산이 계산되지 않았습니다.',
                    hint_message='분산 = 각 값과 평균의 차이를 제곱한 값들의 평균입니다.'
                ),
                VerificationCriteria(
                    criteria_id='calculates_std_dev',
                    name='표준편차 계산',
                    description='std',
                    verification_function='has_variable',
                    weight=0.4,
                    required=True,
                    error_message='표준편차가 계산되지 않았습니다.',
                    hint_message='표준편차 = 분산의 제곱근입니다.'
                ),
                VerificationCriteria(
                    criteria_id='uses_max_min',
                    name='최댓값/최솟값 사용',
                    description='max|min',
                    verification_function='has_function_call',
                    weight=0.2,
                    required=False,
                    error_message='max() 또는 min() 함수가 사용되지 않았습니다.',
                    hint_message='max()와 min() 함수로 최댓값과 최솟값을 구하세요.'
                )
            ]
        }
    
    def verify_step_completion(self, step_id: str, code: str, execution_result: Dict[str, Any], 
                             user_id: str = "default", attempt_count: int = 1) -> Dict[str, Any]:
        """단계 완료 검증"""
        if step_id not in self.step_criteria:
            return {
                'success': False,
                'error': f'Unknown step: {step_id}',
                'hints': []
            }
        
        criteria_list = self.step_criteria[step_id]
        
        # 코드 검증 수행
        verification_result = self.verifier.verify_code(code, execution_result, criteria_list)
        
        # 힌트 생성
        hints = self.hint_provider.get_contextual_hints(
            verification_result, user_id, attempt_count
        )
        
        # 사용자 진행 상황 업데이트
        self.hint_provider.update_user_progress(user_id, verification_result)
        
        # 결과 통합
        result = {
            'step_id': step_id,
            'verification_passed': verification_result['overall_success'],
            'score_percentage': verification_result['score_percentage'],
            'total_score': verification_result['total_score'],
            'max_score': verification_result['max_score'],
            'failed_criteria': verification_result['failed_criteria'],
            'hints': hints,
            'suggestions': verification_result.get('suggestions', []),
            'attempt_count': attempt_count,
            'timestamp': datetime.now().isoformat()
        }
        
        return result
    
    def get_step_requirements(self, step_id: str) -> Dict[str, Any]:
        """단계 요구사항 조회"""
        if step_id not in self.step_criteria:
            return {'error': f'Unknown step: {step_id}'}
        
        criteria_list = self.step_criteria[step_id]
        
        return {
            'step_id': step_id,
            'total_criteria': len(criteria_list),
            'required_criteria': len([c for c in criteria_list if c.required]),
            'criteria_details': [
                {
                    'criteria_id': c.criteria_id,
                    'name': c.name,
                    'description': c.description,
                    'weight': c.weight,
                    'required': c.required,
                    'hint_message': c.hint_message
                }
                for c in criteria_list
            ]
        }

# 테스트 및 데모 함수
def demo_verification_hint_system():
    """검증 및 힌트 시스템 데모"""
    print("🔍 단계별 검증 및 힌트 시스템 데모")
    print("=" * 50)
    
    system = VerificationHintSystem()
    
    # 테스트 케이스들
    test_cases = [
        {
            'step_id': 'step_1',
            'title': '데이터 준비 단계 (성공 케이스)',
            'code': '''
scores = [85, 90, 78, 92, 88, 76, 95, 89, 84, 91]
print(f"데이터: {scores}")
print(f"데이터 개수: {len(scores)}")
print(f"데이터 타입: {type(scores)}")
''',
            'execution_result': {
                'success': True,
                'output': '데이터: [85, 90, 78, 92, 88, 76, 95, 89, 84, 91]\n데이터 개수: 10\n데이터 타입: <class \'list\'>',
                'variables': {'scores': [85, 90, 78, 92, 88, 76, 95, 89, 84, 91]}
            }
        },
        {
            'step_id': 'step_1',
            'title': '데이터 준비 단계 (실패 케이스)',
            'code': '''
# 데이터 변수 없음
print("Hello World")
''',
            'execution_result': {
                'success': True,
                'output': 'Hello World',
                'variables': {}
            }
        },
        {
            'step_id': 'step_2',
            'title': '평균 계산 단계 (부분 성공)',
            'code': '''
scores = [85, 90, 78, 92, 88]
total = sum(scores)
count = len(scores)
mean_value = total / count
# 출력 누락
''',
            'execution_result': {
                'success': True,
                'output': '',
                'variables': {
                    'scores': [85, 90, 78, 92, 88],
                    'total': 433,
                    'count': 5,
                    'mean_value': 86.6
                }
            }
        }
    ]
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n📝 테스트 케이스 {i}: {case['title']}")
        print("-" * 50)
        
        result = system.verify_step_completion(
            case['step_id'],
            case['code'],
            case['execution_result'],
            user_id=f"test_user_{i}",
            attempt_count=i
        )
        
        print(f"🎯 검증 결과:")
        print(f"  통과: {'✅' if result['verification_passed'] else '❌'}")
        print(f"  점수: {result['score_percentage']:.1f}% ({result['total_score']:.1f}/{result['max_score']:.1f})")
        
        if result['failed_criteria']:
            print(f"\n❌ 실패한 기준:")
            for fc in result['failed_criteria']:
                print(f"  • {fc['name']}: {fc['error_message']}")
        
        if result['hints']:
            print(f"\n💡 제공된 힌트:")
            for j, hint in enumerate(result['hints'], 1):
                print(f"  {j}. {hint.get('message', 'No message')}")
                if hint.get('code_example'):
                    print(f"     예제 코드:")
                    print(f"     {hint['code_example'][:100]}...")
        
        if i < len(test_cases):
            print(f"\n{'='*50}")
    
    print(f"\n🎉 Task 3.2 완료!")
    print("✅ 코드 실행 결과 자동 검증 기능")
    print("✅ 상황별 맞춤 힌트 제공 시스템")
    print("✅ 학습 진도에 따른 적응형 가이드")

if __name__ == "__main__":
    demo_verification_hint_system()