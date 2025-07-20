"""
고급 오류 처리 시스템
- 사용자 친화적 오류 메시지 생성
- 해결 방법 제안 기능
- 맥락별 오류 분석
- 학습 지원 오류 가이드
"""

import re
import traceback
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import json

@dataclass
class ErrorContext:
    """오류 컨텍스트 정보"""
    error_type: str
    error_message: str
    line_number: Optional[int]
    code_snippet: str
    user_level: str  # beginner, intermediate, advanced
    learning_context: str  # education, practice, assessment
    previous_errors: List[str]

@dataclass
class ErrorSolution:
    """오류 해결 방안"""
    solution_id: str
    title: str
    description: str
    code_example: Optional[str]
    difficulty: str  # easy, medium, hard
    success_rate: float  # 0-1
    learning_resources: List[str]

class ErrorPatternAnalyzer:
    """오류 패턴 분석기"""
    
    def __init__(self):
        self.error_patterns = self._initialize_error_patterns()
        self.common_mistakes = self._initialize_common_mistakes()
        self.learning_progressions = self._initialize_learning_progressions()
    
    def _initialize_error_patterns(self) -> Dict[str, Dict[str, Any]]:
        """오류 패턴 초기화"""
        return {
            'SyntaxError': {
                'patterns': [
                    {
                        'pattern': r'invalid syntax.*\(',
                        'cause': '괄호 불일치',
                        'solutions': ['missing_parenthesis', 'extra_parenthesis']
                    },
                    {
                        'pattern': r'invalid syntax.*:',
                        'cause': '콜론 누락 또는 잘못된 위치',
                        'solutions': ['missing_colon', 'incorrect_colon_placement']
                    },
                    {
                        'pattern': r'unexpected indent',
                        'cause': '들여쓰기 오류',
                        'solutions': ['fix_indentation', 'consistent_indentation']
                    },
                    {
                        'pattern': r'unindent does not match',
                        'cause': '들여쓰기 불일치',
                        'solutions': ['fix_indentation_consistency']
                    }
                ],
                'general_advice': '파이썬 문법 규칙을 확인하세요'
            },
            'NameError': {
                'patterns': [
                    {
                        'pattern': r"name '(\w+)' is not defined",
                        'cause': '정의되지 않은 변수 사용',
                        'solutions': ['define_variable', 'check_spelling', 'import_module']
                    }
                ],
                'general_advice': '변수를 사용하기 전에 정의했는지 확인하세요'
            },
            'TypeError': {
                'patterns': [
                    {
                        'pattern': r"unsupported operand type.*'(\w+)'.*'(\w+)'",
                        'cause': '호환되지 않는 데이터 타입 연산',
                        'solutions': ['type_conversion', 'check_data_types']
                    },
                    {
                        'pattern': r"'(\w+)' object is not callable",
                        'cause': '함수가 아닌 객체를 함수처럼 호출',
                        'solutions': ['check_function_call', 'variable_name_conflict']
                    },
                    {
                        'pattern': r"takes (\d+) positional argument.*but (\d+) were given",
                        'cause': '함수 인수 개수 불일치',
                        'solutions': ['check_function_arguments', 'function_documentation']
                    }
                ],
                'general_advice': '데이터 타입과 함수 사용법을 확인하세요'
            },
            'ValueError': {
                'patterns': [
                    {
                        'pattern': r"invalid literal for int\(\).*'(\w+)'",
                        'cause': '숫자로 변환할 수 없는 문자열',
                        'solutions': ['validate_input', 'handle_conversion_error']
                    },
                    {
                        'pattern': r"math domain error",
                        'cause': '수학 함수의 정의역 오류',
                        'solutions': ['check_math_domain', 'validate_math_input']
                    }
                ],
                'general_advice': '입력 값의 유효성을 확인하세요'
            },
            'IndexError': {
                'patterns': [
                    {
                        'pattern': r"list index out of range",
                        'cause': '리스트 인덱스 범위 초과',
                        'solutions': ['check_list_length', 'safe_indexing']
                    }
                ],
                'general_advice': '리스트나 문자열의 길이를 먼저 확인하세요'
            },
            'KeyError': {
                'patterns': [
                    {
                        'pattern': r"'(\w+)'",
                        'cause': '딕셔너리에 존재하지 않는 키 접근',
                        'solutions': ['check_dictionary_keys', 'use_get_method']
                    }
                ],
                'general_advice': '딕셔너리 키의 존재 여부를 확인하세요'
            },
            'ImportError': {
                'patterns': [
                    {
                        'pattern': r"No module named '(\w+)'",
                        'cause': '설치되지 않은 모듈 import',
                        'solutions': ['install_module', 'check_module_name']
                    }
                ],
                'general_advice': '필요한 라이브러리가 설치되어 있는지 확인하세요'
            }
        }
    
    def _initialize_common_mistakes(self) -> Dict[str, Dict[str, Any]]:
        """일반적인 실수 패턴 초기화"""
        return {
            'beginner': [
                {
                    'mistake': '들여쓰기 혼용 (탭과 스페이스)',
                    'detection': r'[\t ]+',
                    'solution': '일관된 들여쓰기 사용 (스페이스 4개 권장)'
                },
                {
                    'mistake': '변수명 오타',
                    'detection': r'similar_variable_names',
                    'solution': '변수명 철자 확인 및 자동완성 활용'
                },
                {
                    'mistake': '함수 호출 시 괄호 누락',
                    'detection': r'function_without_parentheses',
                    'solution': '함수 호출 시 반드시 괄호 사용'
                }
            ],
            'intermediate': [
                {
                    'mistake': '리스트와 문자열 인덱싱 혼동',
                    'detection': r'string_list_confusion',
                    'solution': '데이터 타입별 인덱싱 방법 숙지'
                },
                {
                    'mistake': '반복문에서 인덱스 오류',
                    'detection': r'loop_index_error',
                    'solution': 'range() 함수와 len() 함수 올바른 사용'
                }
            ],
            'advanced': [
                {
                    'mistake': '스코프 관련 오류',
                    'detection': r'scope_error',
                    'solution': '변수 스코프와 네임스페이스 이해'
                }
            ]
        }
    
    def _initialize_learning_progressions(self) -> Dict[str, List[str]]:
        """학습 진행 단계별 가이드"""
        return {
            'syntax_mastery': [
                '기본 문법 규칙 학습',
                '들여쓰기와 코드 블록 이해',
                '함수와 클래스 정의 문법',
                '예외 처리 문법'
            ],
            'data_types': [
                '기본 데이터 타입 이해',
                '타입 변환과 검증',
                '컬렉션 타입 활용',
                '사용자 정의 타입'
            ],
            'error_handling': [
                '오류 메시지 읽기',
                '디버깅 기법 습득',
                '예외 처리 구현',
                '로깅과 모니터링'
            ]
        }
    
    def analyze_error_pattern(self, error_context: ErrorContext) -> Dict[str, Any]:
        """오류 패턴 분석"""
        error_type = error_context.error_type
        error_message = error_context.error_message
        
        analysis = {
            'error_category': error_type,
            'specific_cause': 'unknown',
            'confidence': 0.0,
            'pattern_matches': [],
            'suggested_solutions': []
        }
        
        if error_type in self.error_patterns:
            patterns = self.error_patterns[error_type]['patterns']
            
            for pattern_info in patterns:
                pattern = pattern_info['pattern']
                if re.search(pattern, error_message, re.IGNORECASE):
                    analysis['specific_cause'] = pattern_info['cause']
                    analysis['confidence'] = 0.9
                    analysis['pattern_matches'].append(pattern_info)
                    analysis['suggested_solutions'].extend(pattern_info['solutions'])
                    break
            
            # 일반적인 조언 추가
            analysis['general_advice'] = self.error_patterns[error_type]['general_advice']
        
        return analysis

class SolutionGenerator:
    """해결 방안 생성기"""
    
    def __init__(self):
        self.solution_templates = self._initialize_solution_templates()
        self.code_examples = self._initialize_code_examples()
    
    def _initialize_solution_templates(self) -> Dict[str, ErrorSolution]:
        """해결 방안 템플릿 초기화"""
        return {
            'missing_parenthesis': ErrorSolution(
                solution_id='missing_parenthesis',
                title='누락된 괄호 추가',
                description='함수 호출이나 수식에서 괄호가 누락되었습니다.',
                code_example='''
# 잘못된 예
print "Hello World"  # 괄호 누락

# 올바른 예
print("Hello World")  # 괄호 추가
''',
                difficulty='easy',
                success_rate=0.95,
                learning_resources=['Python 기본 문법 가이드', '함수 호출 방법']
            ),
            
            'define_variable': ErrorSolution(
                solution_id='define_variable',
                title='변수 정의하기',
                description='사용하기 전에 변수를 먼저 정의해야 합니다.',
                code_example='''
# 잘못된 예
print(my_variable)  # my_variable이 정의되지 않음

# 올바른 예
my_variable = "Hello"  # 변수 먼저 정의
print(my_variable)     # 그 다음 사용
''',
                difficulty='easy',
                success_rate=0.9,
                learning_resources=['변수와 할당', 'Python 변수 명명 규칙']
            ),
            
            'type_conversion': ErrorSolution(
                solution_id='type_conversion',
                title='데이터 타입 변환',
                description='호환되지 않는 타입 간 연산을 위해 타입 변환이 필요합니다.',
                code_example='''
# 잘못된 예
age = "25"
next_year = age + 1  # 문자열과 숫자 연산 불가

# 올바른 예
age = "25"
next_year = int(age) + 1  # 문자열을 정수로 변환
print(f"내년 나이: {next_year}")
''',
                difficulty='medium',
                success_rate=0.85,
                learning_resources=['데이터 타입 변환', 'int(), float(), str() 함수']
            ),
            
            'check_list_length': ErrorSolution(
                solution_id='check_list_length',
                title='리스트 길이 확인',
                description='인덱스 접근 전에 리스트의 길이를 확인하세요.',
                code_example='''
# 잘못된 예
my_list = [1, 2, 3]
print(my_list[5])  # 인덱스 5는 존재하지 않음

# 올바른 예
my_list = [1, 2, 3]
if len(my_list) > 5:
    print(my_list[5])
else:
    print("인덱스가 범위를 벗어났습니다")
    
# 또는 안전한 접근 방법
index = 5
if 0 <= index < len(my_list):
    print(my_list[index])
''',
                difficulty='medium',
                success_rate=0.8,
                learning_resources=['리스트 인덱싱', '안전한 리스트 접근 방법']
            ),
            
            'use_get_method': ErrorSolution(
                solution_id='use_get_method',
                title='딕셔너리 안전한 접근',
                description='딕셔너리 키 접근 시 get() 메서드를 사용하세요.',
                code_example='''
# 잘못된 예
student = {"name": "김철수", "age": 20}
print(student["grade"])  # "grade" 키가 없어서 오류

# 올바른 예 1: get() 메서드 사용
grade = student.get("grade", "정보 없음")
print(f"성적: {grade}")

# 올바른 예 2: 키 존재 확인
if "grade" in student:
    print(student["grade"])
else:
    print("성적 정보가 없습니다")
''',
                difficulty='medium',
                success_rate=0.88,
                learning_resources=['딕셔너리 메서드', '안전한 딕셔너리 접근']
            ),
            
            'fix_indentation': ErrorSolution(
                solution_id='fix_indentation',
                title='들여쓰기 수정',
                description='파이썬은 들여쓰기로 코드 블록을 구분합니다.',
                code_example='''
# 잘못된 예
if True:
print("Hello")  # 들여쓰기 없음

# 올바른 예
if True:
    print("Hello")  # 4칸 들여쓰기

# 함수 정의 예
def my_function():
    x = 10
    y = 20
    return x + y  # 모든 줄이 같은 수준으로 들여쓰기
''',
                difficulty='easy',
                success_rate=0.92,
                learning_resources=['Python 들여쓰기 규칙', 'PEP 8 스타일 가이드']
            )
        }
    
    def _initialize_code_examples(self) -> Dict[str, List[str]]:
        """코드 예제 초기화"""
        return {
            'basic_syntax': [
                '변수 정의와 사용',
                '함수 정의와 호출',
                '조건문과 반복문',
                '리스트와 딕셔너리 사용'
            ],
            'error_prevention': [
                '입력 검증 코드',
                '예외 처리 구문',
                '안전한 타입 변환',
                '디버깅 기법'
            ]
        }
    
    def generate_solutions(self, error_analysis: Dict[str, Any], 
                         error_context: ErrorContext) -> List[ErrorSolution]:
        """해결 방안 생성"""
        solutions = []
        
        # 분석된 해결 방안들 추가
        for solution_id in error_analysis.get('suggested_solutions', []):
            if solution_id in self.solution_templates:
                solution = self.solution_templates[solution_id]
                solutions.append(solution)
        
        # 사용자 수준에 맞는 추가 해결 방안
        additional_solutions = self._get_level_appropriate_solutions(
            error_context.user_level, error_context.error_type
        )
        solutions.extend(additional_solutions)
        
        # 중복 제거 및 우선순위 정렬
        unique_solutions = self._deduplicate_solutions(solutions)
        sorted_solutions = self._sort_solutions_by_relevance(
            unique_solutions, error_context
        )
        
        return sorted_solutions[:3]  # 최대 3개 해결 방안 반환
    
    def _get_level_appropriate_solutions(self, user_level: str, 
                                       error_type: str) -> List[ErrorSolution]:
        """사용자 수준에 맞는 해결 방안"""
        level_solutions = {
            'beginner': ['missing_parenthesis', 'define_variable', 'fix_indentation'],
            'intermediate': ['type_conversion', 'check_list_length', 'use_get_method'],
            'advanced': []  # 고급 사용자는 기본 해결 방안으로 충분
        }
        
        solutions = []
        for solution_id in level_solutions.get(user_level, []):
            if solution_id in self.solution_templates:
                solutions.append(self.solution_templates[solution_id])
        
        return solutions
    
    def _deduplicate_solutions(self, solutions: List[ErrorSolution]) -> List[ErrorSolution]:
        """중복 해결 방안 제거"""
        seen_ids = set()
        unique_solutions = []
        
        for solution in solutions:
            if solution.solution_id not in seen_ids:
                seen_ids.add(solution.solution_id)
                unique_solutions.append(solution)
        
        return unique_solutions
    
    def _sort_solutions_by_relevance(self, solutions: List[ErrorSolution], 
                                   context: ErrorContext) -> List[ErrorSolution]:
        """관련성에 따른 해결 방안 정렬"""
        def relevance_score(solution: ErrorSolution) -> float:
            score = solution.success_rate
            
            # 사용자 수준에 따른 가중치
            if context.user_level == 'beginner' and solution.difficulty == 'easy':
                score += 0.2
            elif context.user_level == 'intermediate' and solution.difficulty == 'medium':
                score += 0.1
            
            return score
        
        return sorted(solutions, key=relevance_score, reverse=True)

class UserFriendlyErrorHandler:
    """사용자 친화적 오류 처리기"""
    
    def __init__(self):
        self.pattern_analyzer = ErrorPatternAnalyzer()
        self.solution_generator = SolutionGenerator()
        self.error_history = {}  # 사용자별 오류 기록
    
    def handle_error(self, error_info: Dict[str, Any], user_id: str = "default",
                    user_level: str = "beginner", learning_context: str = "general") -> Dict[str, Any]:
        """종합적인 오류 처리"""
        
        # 오류 컨텍스트 생성
        error_context = ErrorContext(
            error_type=error_info.get('error_type', 'Unknown'),
            error_message=error_info.get('error', ''),
            line_number=self._extract_line_number(error_info.get('traceback', '')),
            code_snippet=error_info.get('code', ''),
            user_level=user_level,
            learning_context=learning_context,
            previous_errors=self._get_user_error_history(user_id)
        )
        
        # 오류 패턴 분석
        error_analysis = self.pattern_analyzer.analyze_error_pattern(error_context)
        
        # 해결 방안 생성
        solutions = self.solution_generator.generate_solutions(error_analysis, error_context)
        
        # 학습 가이드 생성
        learning_guide = self._generate_learning_guide(error_context, error_analysis)
        
        # 오류 기록 업데이트
        self._update_error_history(user_id, error_context)
        
        # 종합 결과 생성
        comprehensive_response = {
            'error_summary': {
                'type': error_context.error_type,
                'message': error_context.error_message,
                'cause': error_analysis.get('specific_cause', 'unknown'),
                'confidence': error_analysis.get('confidence', 0.0)
            },
            'user_friendly_explanation': self._generate_friendly_explanation(
                error_context, error_analysis
            ),
            'solutions': [
                {
                    'title': sol.title,
                    'description': sol.description,
                    'code_example': sol.code_example,
                    'difficulty': sol.difficulty,
                    'success_rate': sol.success_rate
                }
                for sol in solutions
            ],
            'learning_guide': learning_guide,
            'prevention_tips': self._generate_prevention_tips(error_context),
            'next_steps': self._suggest_next_steps(error_context, error_analysis)
        }
        
        return comprehensive_response
    
    def _extract_line_number(self, traceback_str: str) -> Optional[int]:
        """트레이스백에서 라인 번호 추출"""
        match = re.search(r'line (\d+)', traceback_str)
        return int(match.group(1)) if match else None
    
    def _get_user_error_history(self, user_id: str) -> List[str]:
        """사용자 오류 기록 조회"""
        return self.error_history.get(user_id, [])
    
    def _update_error_history(self, user_id: str, error_context: ErrorContext):
        """사용자 오류 기록 업데이트"""
        if user_id not in self.error_history:
            self.error_history[user_id] = []
        
        self.error_history[user_id].append(error_context.error_type)
        
        # 최근 10개 오류만 유지
        if len(self.error_history[user_id]) > 10:
            self.error_history[user_id] = self.error_history[user_id][-10:]
    
    def _generate_friendly_explanation(self, error_context: ErrorContext, 
                                     error_analysis: Dict[str, Any]) -> str:
        """사용자 친화적 설명 생성"""
        error_type = error_context.error_type
        specific_cause = error_analysis.get('specific_cause', 'unknown')
        
        explanations = {
            'SyntaxError': {
                'general': '파이썬 문법에 맞지 않는 코드가 있습니다.',
                'specific': {
                    '괄호 불일치': '괄호가 제대로 닫히지 않았거나 누락되었습니다.',
                    '콜론 누락 또는 잘못된 위치': 'if, for, def 등 뒤에 콜론(:)이 필요합니다.',
                    '들여쓰기 오류': '코드 블록의 들여쓰기가 올바르지 않습니다.'
                }
            },
            'NameError': {
                'general': '정의되지 않은 변수나 함수를 사용하려고 했습니다.',
                'specific': {
                    '정의되지 않은 변수 사용': '변수를 사용하기 전에 먼저 값을 할당해야 합니다.'
                }
            },
            'TypeError': {
                'general': '데이터 타입이 맞지 않아 연산을 수행할 수 없습니다.',
                'specific': {
                    '호환되지 않는 데이터 타입 연산': '서로 다른 타입의 데이터를 연산하려고 했습니다.',
                    '함수가 아닌 객체를 함수처럼 호출': '변수를 함수처럼 호출하려고 했습니다.'
                }
            }
        }
        
        error_info = explanations.get(error_type, {'general': '예상치 못한 오류가 발생했습니다.'})
        
        if specific_cause in error_info.get('specific', {}):
            return error_info['specific'][specific_cause]
        else:
            return error_info['general']
    
    def _generate_learning_guide(self, error_context: ErrorContext, 
                               error_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """학습 가이드 생성"""
        error_type = error_context.error_type
        user_level = error_context.user_level
        
        # 기본 학습 자료
        learning_resources = {
            'SyntaxError': {
                'beginner': [
                    'Python 기본 문법 튜토리얼',
                    '들여쓰기와 코드 블록 이해하기',
                    '함수와 조건문 문법 연습'
                ],
                'intermediate': [
                    'Python 스타일 가이드 (PEP 8)',
                    '고급 문법 구조 학습'
                ]
            },
            'NameError': {
                'beginner': [
                    '변수 선언과 사용법',
                    'Python 변수 명명 규칙',
                    '스코프와 네임스페이스 기초'
                ]
            },
            'TypeError': {
                'beginner': [
                    'Python 데이터 타입 이해하기',
                    '타입 변환 함수 사용법',
                    '함수 정의와 호출 방법'
                ]
            }
        }
        
        # 실습 제안
        practice_suggestions = {
            'SyntaxError': [
                '간단한 계산기 프로그램 작성하기',
                '조건문을 사용한 프로그램 만들기'
            ],
            'NameError': [
                '변수를 사용한 데이터 저장 연습',
                '함수 정의와 호출 연습'
            ],
            'TypeError': [
                '다양한 데이터 타입 변환 연습',
                '타입 검사 함수 만들어보기'
            ]
        }
        
        return {
            'recommended_resources': learning_resources.get(error_type, {}).get(user_level, []),
            'practice_suggestions': practice_suggestions.get(error_type, []),
            'difficulty_progression': self._get_difficulty_progression(error_type, user_level)
        }
    
    def _get_difficulty_progression(self, error_type: str, user_level: str) -> List[str]:
        """난이도별 학습 진행 단계"""
        progressions = {
            'SyntaxError': [
                '기본 문법 규칙 숙지',
                '간단한 프로그램 작성',
                '복잡한 구조 이해',
                '코드 스타일 개선'
            ],
            'NameError': [
                '변수 개념 이해',
                '스코프 규칙 학습',
                '모듈과 패키지 사용',
                '네임스페이스 관리'
            ],
            'TypeError': [
                '기본 타입 이해',
                '타입 변환 숙지',
                '객체 지향 개념',
                '고급 타입 시스템'
            ]
        }
        
        return progressions.get(error_type, ['기본기 다지기', '실습 늘리기', '고급 기법 학습'])
    
    def _generate_prevention_tips(self, error_context: ErrorContext) -> List[str]:
        """오류 예방 팁 생성"""
        general_tips = [
            '코드를 작성한 후 한 번 더 검토하세요',
            '작은 단위로 나누어 테스트하세요',
            '오류 메시지를 주의 깊게 읽어보세요'
        ]
        
        specific_tips = {
            'SyntaxError': [
                '코드 에디터의 문법 하이라이팅을 활용하세요',
                '괄호와 들여쓰기를 일관되게 사용하세요'
            ],
            'NameError': [
                '변수명을 명확하고 의미 있게 지으세요',
                '변수를 사용하기 전에 정의했는지 확인하세요'
            ],
            'TypeError': [
                'type() 함수로 데이터 타입을 확인하세요',
                '타입 변환이 필요한지 미리 생각해보세요'
            ]
        }
        
        error_specific = specific_tips.get(error_context.error_type, [])
        return general_tips + error_specific
    
    def _suggest_next_steps(self, error_context: ErrorContext, 
                          error_analysis: Dict[str, Any]) -> List[str]:
        """다음 단계 제안"""
        next_steps = []
        
        # 즉시 해결 단계
        next_steps.append('제안된 해결 방법을 하나씩 시도해보세요')
        
        # 학습 단계
        if error_context.user_level == 'beginner':
            next_steps.extend([
                '기본 문법 튜토리얼을 복습하세요',
                '간단한 예제부터 다시 시작해보세요'
            ])
        
        # 반복 오류 방지
        if error_context.error_type in error_context.previous_errors:
            next_steps.append('이 오류가 반복되고 있습니다. 관련 개념을 집중적으로 학습하세요')
        
        # 도움 요청
        next_steps.append('해결되지 않으면 온라인 커뮤니티나 문서를 참고하세요')
        
        return next_steps

# 사용 예제 및 테스트
def demo_error_handling_system():
    """오류 처리 시스템 데모"""
    print("🚨 고급 오류 처리 시스템 데모")
    print("=" * 50)
    
    handler = UserFriendlyErrorHandler()
    
    # 테스트 오류 케이스들
    test_cases = [
        {
            'title': '구문 오류 (괄호 누락)',
            'error_info': {
                'error_type': 'SyntaxError',
                'error': 'invalid syntax',
                'code': 'print "Hello World"',
                'traceback': 'File "<string>", line 1\n    print "Hello World"\n                      ^\nSyntaxError: invalid syntax'
            },
            'user_level': 'beginner'
        },
        {
            'title': '이름 오류 (정의되지 않은 변수)',
            'error_info': {
                'error_type': 'NameError',
                'error': "name 'undefined_var' is not defined",
                'code': 'result = undefined_var + 10',
                'traceback': 'NameError: name \'undefined_var\' is not defined'
            },
            'user_level': 'beginner'
        },
        {
            'title': '타입 오류 (문자열과 숫자 연산)',
            'error_info': {
                'error_type': 'TypeError',
                'error': "unsupported operand type(s) for +: 'str' and 'int'",
                'code': 'age = "25"\nresult = age + 1',
                'traceback': 'TypeError: unsupported operand type(s) for +: \'str\' and \'int\''
            },
            'user_level': 'intermediate'
        }
    ]
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n📝 테스트 케이스 {i}: {case['title']}")
        print("-" * 50)
        
        response = handler.handle_error(
            case['error_info'], 
            user_id=f"test_user_{i}",
            user_level=case['user_level']
        )
        
        print(f"🔍 오류 분석:")
        print(f"  타입: {response['error_summary']['type']}")
        print(f"  원인: {response['error_summary']['cause']}")
        print(f"  신뢰도: {response['error_summary']['confidence']:.1%}")
        
        print(f"\n💡 친화적 설명:")
        print(f"  {response['user_friendly_explanation']}")
        
        print(f"\n🛠️  해결 방법:")
        for j, solution in enumerate(response['solutions'][:2], 1):
            print(f"  {j}. {solution['title']}")
            print(f"     {solution['description']}")
            print(f"     난이도: {solution['difficulty']}, 성공률: {solution['success_rate']:.1%}")
        
        print(f"\n🎯 예방 팁:")
        for tip in response['prevention_tips'][:2]:
            print(f"  • {tip}")
        
        if i < len(test_cases):
            print(f"\n{'='*50}")
    
    print(f"\n🎉 Task 2.3 완료!")
    print("✅ 사용자 친화적 오류 메시지 생성")
    print("✅ 맞춤형 해결 방법 제안")
    print("✅ 학습 지원 오류 가이드 제공")

if __name__ == "__main__":
    demo_error_handling_system()