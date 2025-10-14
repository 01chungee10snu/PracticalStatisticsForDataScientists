"""
향상된 오류 처리 시스템
- 사용자 친화적 오류 메시지 생성
- 해결 방법 제안 기능
- 오류 패턴 분석 및 학습 지원
"""

import re
import traceback
from typing import Dict, Any, List, Optional, Tuple
from enum import Enum

class ErrorType(Enum):
    """오류 유형"""
    SYNTAX_ERROR = "syntax_error"
    NAME_ERROR = "name_error"
    TYPE_ERROR = "type_error"
    VALUE_ERROR = "value_error"
    INDEX_ERROR = "index_error"
    KEY_ERROR = "key_error"
    ATTRIBUTE_ERROR = "attribute_error"
    IMPORT_ERROR = "import_error"
    ZERO_DIVISION_ERROR = "zero_division_error"
    RUNTIME_ERROR = "runtime_error"
    UNKNOWN_ERROR = "unknown_error"

class ErrorSeverity(Enum):
    """오류 심각도"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ErrorHandlingSystem:
    """
    향상된 오류 처리 시스템
    사용자 친화적 오류 메시지와 해결 방법을 제공합니다.
    """
    
    def __init__(self):
        """초기화"""
        self.error_patterns = self._initialize_error_patterns()
        self.solution_templates = self._initialize_solution_templates()
        self.learning_tips = self._initialize_learning_tips()
        self.error_history = []
    
    def _initialize_error_patterns(self) -> Dict[ErrorType, List[str]]:
        """오류 패턴 초기화"""
        return {
            ErrorType.SYNTAX_ERROR: [
                r"SyntaxError: (.+)",
                r"invalid syntax",
                r"unexpected EOF",
                r"unmatched",
                r"invalid character"
            ],
            ErrorType.NAME_ERROR: [
                r"NameError: name '(.+)' is not defined",
                r"NameError: (.+)"
            ],
            ErrorType.TYPE_ERROR: [
                r"TypeError: (.+)",
                r"unsupported operand type",
                r"can't multiply sequence",
                r"object is not callable"
            ],
            ErrorType.VALUE_ERROR: [
                r"ValueError: (.+)",
                r"invalid literal",
                r"could not convert",
                r"math domain error"
            ],
            ErrorType.INDEX_ERROR: [
                r"IndexError: (.+)",
                r"list index out of range",
                r"string index out of range"
            ],
            ErrorType.KEY_ERROR: [
                r"KeyError: (.+)",
                r"key not found"
            ],
            ErrorType.ATTRIBUTE_ERROR: [
                r"AttributeError: (.+)",
                r"has no attribute",
                r"object has no attribute"
            ],
            ErrorType.IMPORT_ERROR: [
                r"ImportError: (.+)",
                r"ModuleNotFoundError: (.+)",
                r"No module named"
            ],
            ErrorType.ZERO_DIVISION_ERROR: [
                r"ZeroDivisionError: (.+)",
                r"division by zero"
            ]
        }
    
    def _initialize_solution_templates(self) -> Dict[ErrorType, Dict[str, Any]]:
        """해결 방법 템플릿 초기화"""
        return {
            ErrorType.SYNTAX_ERROR: {
                "title": "문법 오류",
                "description": "Python 코드 문법에 문제가 있습니다.",
                "solutions": [
                    "괄호, 따옴표, 콜론이 올바르게 짝을 이루는지 확인하세요.",
                    "들여쓰기가 일관되게 되어있는지 확인하세요.",
                    "문자열 안에 따옴표를 사용할 때는 이스케이프(\\) 또는 다른 종류의 따옴표를 사용하세요.",
                    "함수나 조건문 뒤에 콜론(:)을 빠뜨리지 않았는지 확인하세요."
                ],
                "examples": [
                    '# 올바른 문자열 사용법\ntext1 = "그는 \\"안녕\\"이라고 말했다."\ntext2 = \'그는 "안녕"이라고 말했다.\'',
                    '# 올바른 함수 정의\ndef my_function():\n    return "Hello"'
                ],
                "severity": ErrorSeverity.HIGH
            },
            ErrorType.NAME_ERROR: {
                "title": "정의되지 않은 변수/함수",
                "description": "사용하려는 변수나 함수가 정의되지 않았습니다.",
                "solutions": [
                    "변수명이 올바르게 입력되었는지 확인하세요 (대소문자 구분).",
                    "필요한 라이브러리를 import 했는지 확인하세요.",
                    "변수를 먼저 선언했는지 확인하세요.",
                    "함수나 변수의 스코프(범위)를 확인하세요."
                ],
                "examples": [
                    '# 올바른 변수 사용법\nmy_variable = 10  # 변수 먼저 정의\nprint(my_variable)  # 그 후 사용',
                    '# 올바른 라이브러리 import\nimport numpy as np\ndata = np.array([1, 2, 3])'
                ],
                "severity": ErrorSeverity.MEDIUM
            },
            ErrorType.TYPE_ERROR: {
                "title": "타입 오류",
                "description": "데이터 타입이 맞지 않습니다.",
                "solutions": [
                    "함수에 전달된 인자의 타입이 올바른지 확인하세요.",
                    "문자열과 숫자를 연산할 때는 적절한 변환이 필요합니다.",
                    "리스트, 딕셔너리 등의 자료구조를 올바르게 사용하고 있는지 확인하세요.",
                    "함수 호출 시 괄호를 빠뜨리지 않았는지 확인하세요."
                ],
                "examples": [
                    '# 타입 변환 예시\nnum_str = "123"\nnum = int(num_str)  # 문자열을 정수로 변환\nresult = num + 10  # 이제 숫자 연산 가능',
                    '# 올바른 함수 호출\nmy_list = [1, 2, 3]\nprint(len(my_list))  # len() 함수 호출'
                ],
                "severity": ErrorSeverity.MEDIUM
            },
            ErrorType.VALUE_ERROR: {
                "title": "값 오류",
                "description": "함수나 연산에 부적절한 값이 전달되었습니다.",
                "solutions": [
                    "함수에 전달된 인자의 값이 허용 범위 내인지 확인하세요.",
                    "문자열을 숫자로 변환할 때는 유효한 형식인지 확인하세요.",
                    "수학 함수의 정의역을 확인하세요 (예: 음수의 제곱근).",
                    "리스트나 배열의 차원이 올바른지 확인하세요."
                ],
                "examples": [
                    '# 안전한 타입 변환\ntry:\n    num = int(input_str)\nexcept ValueError:\n    print("유효한 숫자를 입력하세요")',
                    '# 수학 함수 사용 시 주의\nimport math\nif x >= 0:\n    result = math.sqrt(x)'
                ],
                "severity": ErrorSeverity.MEDIUM
            },
            ErrorType.INDEX_ERROR: {
                "title": "인덱스 오류",
                "description": "리스트나 배열의 범위를 벗어났습니다.",
                "solutions": [
                    "리스트의 길이를 확인하세요 (len(리스트)).",
                    "인덱스는 0부터 시작합니다 (리스트[0]이 첫 번째 요소).",
                    "음수 인덱스는 뒤에서부터 접근합니다 (리스트[-1]이 마지막 요소).",
                    "반복문에서 인덱스 범위를 올바르게 설정하세요."
                ],
                "examples": [
                    '# 안전한 인덱스 접근\nmy_list = [10, 20, 30]\nif len(my_list) > 2:\n    print(my_list[2])  # 인덱스가 범위 내인지 확인',
                    '# 올바른 반복문\nfor i in range(len(my_list)):\n    print(my_list[i])'
                ],
                "severity": ErrorSeverity.MEDIUM
            },
            ErrorType.KEY_ERROR: {
                "title": "키 오류",
                "description": "딕셔너리나 DataFrame에 존재하지 않는 키를 사용했습니다.",
                "solutions": [
                    "키 이름이 올바른지 확인하세요 (대소문자 구분).",
                    "딕셔너리의 모든 키를 확인하려면 dict.keys()를 사용하세요.",
                    "DataFrame의 열 이름을 확인하려면 df.columns를 사용하세요.",
                    "키가 존재하는지 먼저 확인하세요 (key in dict)."
                ],
                "examples": [
                    '# 안전한 딕셔너리 접근\nmy_dict = {"name": "John", "age": 30}\nif "name" in my_dict:\n    print(my_dict["name"])',
                    '# get() 메서드 사용\nvalue = my_dict.get("height", "키 정보 없음")'
                ],
                "severity": ErrorSeverity.LOW
            },
            ErrorType.ATTRIBUTE_ERROR: {
                "title": "속성 오류",
                "description": "객체에 존재하지 않는 속성이나 메서드를 호출했습니다.",
                "solutions": [
                    "객체의 타입을 확인하세요 (type(객체)).",
                    "메서드나 속성 이름이 올바른지 확인하세요.",
                    "필요한 라이브러리를 import 했는지 확인하세요.",
                    "객체가 None이 아닌지 확인하세요."
                ],
                "examples": [
                    '# 객체 타입 확인\nmy_var = [1, 2, 3]\nprint(type(my_var))  # <class \'list\'>\nprint(dir(my_var))   # 사용 가능한 메서드 확인',
                    '# None 체크\nif my_object is not None:\n    result = my_object.some_method()'
                ],
                "severity": ErrorSeverity.MEDIUM
            },
            ErrorType.IMPORT_ERROR: {
                "title": "모듈 import 오류",
                "description": "필요한 모듈을 찾을 수 없거나 import할 수 없습니다.",
                "solutions": [
                    "모듈 이름이 올바른지 확인하세요.",
                    "필요한 패키지가 설치되어 있는지 확인하세요.",
                    "import 문의 문법이 올바른지 확인하세요.",
                    "상대 경로 import의 경우 패키지 구조를 확인하세요."
                ],
                "examples": [
                    '# 올바른 import 방법\nimport numpy as np\nfrom matplotlib import pyplot as plt\nfrom scipy.stats import norm',
                    '# 조건부 import\ntry:\n    import pandas as pd\nexcept ImportError:\n    print("pandas가 설치되지 않았습니다")'
                ],
                "severity": ErrorSeverity.HIGH
            },
            ErrorType.ZERO_DIVISION_ERROR: {
                "title": "0으로 나누기 오류",
                "description": "0으로 나누려고 했습니다.",
                "solutions": [
                    "나누는 값이 0이 아닌지 확인하세요.",
                    "나누기 전에 조건문으로 0인지 확인하는 방어 코드를 추가하세요.",
                    "분모가 0에 가까운 값인지 확인하세요 (부동소수점 오차).",
                    "수학적으로 의미 있는 연산인지 검토하세요."
                ],
                "examples": [
                    '# 안전한 나누기\nif denominator != 0:\n    result = numerator / denominator\nelse:\n    print("0으로 나눌 수 없습니다")',
                    '# 부동소수점 비교\nif abs(denominator) > 1e-10:\n    result = numerator / denominator'
                ],
                "severity": ErrorSeverity.HIGH
            }
        }
    
    def _initialize_learning_tips(self) -> Dict[ErrorType, List[str]]:
        """학습 팁 초기화"""
        return {
            ErrorType.SYNTAX_ERROR: [
                "코드를 작성할 때는 IDE나 에디터의 문법 하이라이팅을 활용하세요.",
                "복잡한 표현식은 여러 줄로 나누어 작성하면 오류를 찾기 쉽습니다.",
                "괄호의 짝을 맞추기 위해 여는 괄호를 쓸 때 바로 닫는 괄호도 함께 쓰는 습관을 기르세요."
            ],
            ErrorType.NAME_ERROR: [
                "변수명은 의미 있게 짓고, 일관된 명명 규칙을 사용하세요.",
                "전역 변수와 지역 변수의 차이를 이해하고 적절히 사용하세요.",
                "함수나 클래스를 정의한 후에 사용하는 순서를 지키세요."
            ],
            ErrorType.TYPE_ERROR: [
                "Python의 동적 타입 시스템을 이해하고, 필요시 타입을 명시적으로 확인하세요.",
                "함수의 매개변수와 반환값의 타입을 문서화하는 습관을 기르세요.",
                "타입 힌트(Type Hints)를 사용하여 코드의 가독성을 높이세요."
            ],
            ErrorType.VALUE_ERROR: [
                "사용자 입력이나 외부 데이터를 처리할 때는 항상 검증을 수행하세요.",
                "예외 처리(try-except)를 적절히 사용하여 프로그램의 안정성을 높이세요.",
                "함수의 전제조건(precondition)을 명확히 하고 문서화하세요."
            ],
            ErrorType.INDEX_ERROR: [
                "리스트나 배열을 다룰 때는 항상 길이를 확인하는 습관을 기르세요.",
                "반복문에서는 range() 함수를 적절히 사용하여 인덱스 오류를 방지하세요.",
                "슬라이싱을 활용하면 인덱스 오류 없이 안전하게 부분 데이터를 추출할 수 있습니다."
            ]
        }
    
    def analyze_error(self, error_message: str, code: str = None, traceback_info: str = None) -> Dict[str, Any]:
        """
        오류 분석
        
        Args:
            error_message (str): 오류 메시지
            code (str, optional): 실행된 코드
            traceback_info (str, optional): 트레이스백 정보
            
        Returns:
            dict: 오류 분석 결과
        """
        # 오류 유형 식별
        error_type = self._identify_error_type(error_message)
        
        # 오류 세부 정보 추출
        error_details = self._extract_error_details(error_message, error_type)
        
        # 해결 방법 생성
        solutions = self._generate_solutions(error_type, error_details, code)
        
        # 학습 팁 제공
        learning_tips = self.learning_tips.get(error_type, [])
        
        # 오류 기록
        error_record = {
            "timestamp": self._get_timestamp(),
            "error_type": error_type.value,
            "error_message": error_message,
            "code": code,
            "traceback": traceback_info
        }
        self.error_history.append(error_record)
        
        return {
            "error_type": error_type.value,
            "error_details": error_details,
            "solutions": solutions,
            "learning_tips": learning_tips,
            "severity": solutions.get("severity", ErrorSeverity.MEDIUM).value,
            "user_friendly_message": self._generate_user_friendly_message(error_type, error_details),
            "code_suggestions": self._generate_code_suggestions(error_type, error_details, code)
        }
    
    def _identify_error_type(self, error_message: str) -> ErrorType:
        """오류 유형 식별"""
        for error_type, patterns in self.error_patterns.items():
            for pattern in patterns:
                if re.search(pattern, error_message, re.IGNORECASE):
                    return error_type
        
        return ErrorType.UNKNOWN_ERROR
    
    def _extract_error_details(self, error_message: str, error_type: ErrorType) -> Dict[str, Any]:
        """오류 세부 정보 추출"""
        details = {
            "original_message": error_message,
            "extracted_info": {}
        }
        
        if error_type == ErrorType.NAME_ERROR:
            match = re.search(r"name '(.+)' is not defined", error_message)
            if match:
                details["extracted_info"]["undefined_name"] = match.group(1)
        
        elif error_type == ErrorType.KEY_ERROR:
            match = re.search(r"KeyError: ['\"](.+)['\"]", error_message)
            if match:
                details["extracted_info"]["missing_key"] = match.group(1)
        
        elif error_type == ErrorType.ATTRIBUTE_ERROR:
            match = re.search(r"'(.+)' object has no attribute '(.+)'", error_message)
            if match:
                details["extracted_info"]["object_type"] = match.group(1)
                details["extracted_info"]["missing_attribute"] = match.group(2)
        
        elif error_type == ErrorType.IMPORT_ERROR:
            match = re.search(r"No module named ['\"](.+)['\"]", error_message)
            if match:
                details["extracted_info"]["missing_module"] = match.group(1)
        
        return details
    
    def _generate_solutions(self, error_type: ErrorType, error_details: Dict[str, Any], code: str = None) -> Dict[str, Any]:
        """해결 방법 생성"""
        base_solution = self.solution_templates.get(error_type, {
            "title": "알 수 없는 오류",
            "description": "오류 유형을 식별할 수 없습니다.",
            "solutions": ["오류 메시지를 확인하고 코드를 검토해보세요."],
            "examples": [],
            "severity": ErrorSeverity.MEDIUM
        })
        
        # 맞춤형 해결 방법 추가
        customized_solutions = base_solution["solutions"].copy()
        
        if error_type == ErrorType.NAME_ERROR and "undefined_name" in error_details["extracted_info"]:
            var_name = error_details["extracted_info"]["undefined_name"]
            customized_solutions.insert(0, f"'{var_name}' 변수가 정의되지 않았습니다. 변수를 먼저 선언하세요.")
            
            # 코드에서 유사한 변수명 찾기
            if code:
                similar_names = self._find_similar_names(var_name, code)
                if similar_names:
                    customized_solutions.append(f"혹시 다음 중 하나를 의도하셨나요? {', '.join(similar_names)}")
        
        elif error_type == ErrorType.KEY_ERROR and "missing_key" in error_details["extracted_info"]:
            key_name = error_details["extracted_info"]["missing_key"]
            customized_solutions.insert(0, f"'{key_name}' 키가 딕셔너리에 존재하지 않습니다.")
        
        return {
            **base_solution,
            "solutions": customized_solutions
        }
    
    def _generate_user_friendly_message(self, error_type: ErrorType, error_details: Dict[str, Any]) -> str:
        """사용자 친화적 메시지 생성"""
        base_messages = {
            ErrorType.SYNTAX_ERROR: "코드 문법에 오류가 있습니다. 괄호, 따옴표, 들여쓰기를 확인해보세요.",
            ErrorType.NAME_ERROR: "정의되지 않은 변수나 함수를 사용하려고 했습니다.",
            ErrorType.TYPE_ERROR: "데이터 타입이 맞지 않습니다. 변수의 타입을 확인해보세요.",
            ErrorType.VALUE_ERROR: "함수에 잘못된 값이 전달되었습니다.",
            ErrorType.INDEX_ERROR: "리스트나 배열의 범위를 벗어났습니다.",
            ErrorType.KEY_ERROR: "딕셔너리에 존재하지 않는 키를 사용했습니다.",
            ErrorType.ATTRIBUTE_ERROR: "객체에 존재하지 않는 속성이나 메서드를 호출했습니다.",
            ErrorType.IMPORT_ERROR: "필요한 모듈을 찾을 수 없습니다.",
            ErrorType.ZERO_DIVISION_ERROR: "0으로 나누려고 했습니다.",
            ErrorType.UNKNOWN_ERROR: "알 수 없는 오류가 발생했습니다."
        }
        
        return base_messages.get(error_type, "오류가 발생했습니다.")
    
    def _generate_code_suggestions(self, error_type: ErrorType, error_details: Dict[str, Any], code: str = None) -> List[str]:
        """코드 수정 제안 생성"""
        suggestions = []
        
        if error_type == ErrorType.NAME_ERROR and code and "undefined_name" in error_details["extracted_info"]:
            var_name = error_details["extracted_info"]["undefined_name"]
            
            # 일반적인 라이브러리 import 제안
            if var_name in ["np", "numpy"]:
                suggestions.append("import numpy as np")
            elif var_name in ["pd", "pandas"]:
                suggestions.append("import pandas as pd")
            elif var_name in ["plt", "pyplot"]:
                suggestions.append("import matplotlib.pyplot as plt")
            elif var_name in ["stats"]:
                suggestions.append("from scipy import stats")
            else:
                suggestions.append(f"{var_name} = # 여기에 값을 할당하세요")
        
        elif error_type == ErrorType.IMPORT_ERROR and "missing_module" in error_details["extracted_info"]:
            module_name = error_details["extracted_info"]["missing_module"]
            suggestions.append(f"# {module_name} 모듈이 필요합니다. 설치 후 다시 시도하세요.")
        
        return suggestions
    
    def _find_similar_names(self, target_name: str, code: str) -> List[str]:
        """코드에서 유사한 변수명 찾기"""
        # 간단한 변수명 추출 (정규식 사용)
        variable_pattern = r'\b([a-zA-Z_][a-zA-Z0-9_]*)\s*='
        variables = re.findall(variable_pattern, code)
        
        similar_names = []
        for var in set(variables):
            if self._calculate_similarity(target_name, var) > 0.6:
                similar_names.append(var)
        
        return similar_names[:3]  # 최대 3개까지
    
    def _calculate_similarity(self, str1: str, str2: str) -> float:
        """문자열 유사도 계산 (간단한 Levenshtein 거리 기반)"""
        if len(str1) == 0 or len(str2) == 0:
            return 0.0
        
        # 간단한 유사도 계산
        common_chars = set(str1.lower()) & set(str2.lower())
        total_chars = set(str1.lower()) | set(str2.lower())
        
        if len(total_chars) == 0:
            return 0.0
        
        return len(common_chars) / len(total_chars)
    
    def _get_timestamp(self) -> str:
        """현재 시간 반환"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def get_error_statistics(self) -> Dict[str, Any]:
        """오류 통계 반환"""
        if not self.error_history:
            return {"total_errors": 0, "error_types": {}}
        
        error_counts = {}
        for record in self.error_history:
            error_type = record["error_type"]
            error_counts[error_type] = error_counts.get(error_type, 0) + 1
        
        return {
            "total_errors": len(self.error_history),
            "error_types": error_counts,
            "most_common_error": max(error_counts, key=error_counts.get) if error_counts else None
        }
    
    def generate_error_report_html(self, error_analysis: Dict[str, Any]) -> str:
        """오류 보고서 HTML 생성"""
        severity_colors = {
            "low": "#28a745",
            "medium": "#ffc107", 
            "high": "#fd7e14",
            "critical": "#dc3545"
        }
        
        severity_color = severity_colors.get(error_analysis["severity"], "#6c757d")
        
        html = f"""
        <div class="error-report" style="margin: 20px 0; border: 1px solid #dc3545; border-radius: 8px; overflow: hidden;">
            <div class="error-header" style="background-color: {severity_color}; color: white; padding: 12px;">
                <h4 style="margin: 0; display: flex; align-items: center;">
                    <span style="margin-right: 8px;">❌</span>
                    {error_analysis.get('solutions', {}).get('title', '오류 발생')}
                    <span style="margin-left: auto; font-size: 0.8em; background: rgba(255,255,255,0.2); padding: 4px 8px; border-radius: 4px;">
                        {error_analysis['severity'].upper()}
                    </span>
                </h4>
            </div>
            
            <div class="error-body" style="padding: 16px;">
                <div class="error-description" style="margin-bottom: 16px;">
                    <p style="margin: 0; color: #6c757d; font-size: 0.95em;">
                        {error_analysis['user_friendly_message']}
                    </p>
                </div>
                
                <div class="solutions-section" style="margin-bottom: 16px;">
                    <h5 style="color: #28a745; margin-bottom: 8px;">🔧 해결 방법</h5>
                    <ul style="margin: 0; padding-left: 20px;">
        """
        
        for solution in error_analysis.get('solutions', {}).get('solutions', []):
            html += f"<li style='margin-bottom: 4px;'>{solution}</li>"
        
        html += """
                    </ul>
                </div>
        """
        
        # 코드 제안이 있으면 추가
        if error_analysis.get('code_suggestions'):
            html += """
                <div class="code-suggestions" style="margin-bottom: 16px;">
                    <h5 style="color: #007bff; margin-bottom: 8px;">💡 코드 제안</h5>
                    <div style="background: #f8f9fa; border: 1px solid #dee2e6; border-radius: 4px; padding: 12px;">
            """
            
            for suggestion in error_analysis['code_suggestions']:
                html += f'<code style="display: block; margin-bottom: 4px; color: #e83e8c;">{suggestion}</code>'
            
            html += """
                    </div>
                </div>
            """
        
        # 학습 팁이 있으면 추가
        if error_analysis.get('learning_tips'):
            html += """
                <div class="learning-tips">
                    <h5 style="color: #6f42c1; margin-bottom: 8px;">📚 학습 팁</h5>
                    <ul style="margin: 0; padding-left: 20px; font-size: 0.9em; color: #6c757d;">
            """
            
            for tip in error_analysis['learning_tips']:
                html += f"<li style='margin-bottom: 4px;'>{tip}</li>"
            
            html += """
                    </ul>
                </div>
            """
        
        html += """
            </div>
        </div>
        """
        
        return html

# 오류 처리 시스템 인스턴스 생성
error_handler = ErrorHandlingSystem()