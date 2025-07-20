"""
Python Code Executor - Safe Code Execution System
브라우저 기반 Python 코드 실시간 실행 환경
안전한 코드 실행을 위한 보안 기능 포함
"""

import sys
import io
import contextlib
import traceback
import ast
import types
import time
import json
import base64
from typing import Dict, Any, List, Optional, Tuple
import re
import threading
import queue
from datetime import datetime


class SecurityValidator:
    """코드 보안 검증기"""
    
    def __init__(self):
        # 금지된 모듈과 함수들
        self.forbidden_imports = {
            'os', 'subprocess', 'sys', 'importlib', 'exec', 'eval',
            'open', '__import__', 'compile', 'globals', 'locals',
            'vars', 'dir', 'getattr', 'setattr', 'delattr', 'hasattr'
        }
        
        # 허용된 모듈들 (데이터 분석 관련)
        self.allowed_imports = {
            'pandas', 'numpy', 'matplotlib', 'seaborn', 'scipy',
            'sklearn', 'math', 'statistics', 'random', 'datetime',
            'json', 'csv', 're', 'collections', 'itertools'
        }
        
        # 금지된 키워드들
        self.forbidden_keywords = {
            'import os', 'import sys', 'import subprocess',
            'exec(', 'eval(', 'open(', '__import__',
            'file', 'input(', 'raw_input('
        }
    
    def validate_code(self, code: str) -> Tuple[bool, List[str]]:
        """코드 보안 검증"""
        issues = []
        
        # 1. 금지된 키워드 검사
        code_lower = code.lower()
        for keyword in self.forbidden_keywords:
            if keyword in code_lower:
                issues.append(f"보안상 금지된 키워드 사용: {keyword}")
        
        # 2. AST를 통한 구문 분석
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                # Import 문 검사
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        if alias.name in self.forbidden_imports:
                            issues.append(f"금지된 모듈 import: {alias.name}")
                
                elif isinstance(node, ast.ImportFrom):
                    if node.module in self.forbidden_imports:
                        issues.append(f"금지된 모듈 import: {node.module}")
                
                # 함수 호출 검사
                elif isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name):
                        if node.func.id in self.forbidden_imports:
                            issues.append(f"금지된 함수 호출: {node.func.id}")
        
        except SyntaxError as e:
            issues.append(f"구문 오류: {str(e)}")
        
        return len(issues) == 0, issues
    
    def sanitize_code(self, code: str) -> str:
        """코드 정리 및 안전화"""
        # 주석 제거하지 않고 유지
        # 불필요한 공백 정리
        lines = code.split('\n')
        cleaned_lines = []
        
        for line in lines:
            # 빈 줄이 아닌 경우에만 처리
            if line.strip():
                cleaned_lines.append(line.rstrip())
            else:
                cleaned_lines.append('')
        
        return '\n'.join(cleaned_lines)


class CodeExecutor:
    """Python 코드 실행기"""
    
    def __init__(self):
        self.security_validator = SecurityValidator()
        self.execution_timeout = 10  # 10초 제한
        self.max_output_length = 5000  # 최대 출력 길이
    
    def execute_code(self, code: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Python 코드 실행"""
        start_time = time.time()
        
        # 1. 보안 검증
        is_safe, security_issues = self.security_validator.validate_code(code)
        if not is_safe:
            return {
                'success': False,
                'error': 'Security validation failed',
                'security_issues': security_issues,
                'output': '',
                'execution_time': 0
            }
        
        # 2. 코드 정리
        clean_code = self.security_validator.sanitize_code(code)
        
        # 3. 실행 환경 준비
        if context is None:
            context = {}
        
        # 안전한 내장 함수들만 포함
        safe_builtins = {
            'print': print,
            'len': len,
            'range': range,
            'enumerate': enumerate,
            'zip': zip,
            'map': map,
            'filter': filter,
            'sum': sum,
            'min': min,
            'max': max,
            'abs': abs,
            'round': round,
            'sorted': sorted,
            'reversed': reversed,
            'int': int,
            'float': float,
            'str': str,
            'bool': bool,
            'list': list,
            'dict': dict,
            'tuple': tuple,
            'set': set,
            'type': type,
            'isinstance': isinstance,
            'issubclass': issubclass,
        }
        
        # 실행 컨텍스트 설정
        exec_globals = {
            '__builtins__': safe_builtins,
            **context
        }
        exec_locals = {}
        
        # 4. 출력 캡처 준비
        output_buffer = io.StringIO()
        error_buffer = io.StringIO()
        
        try:
            # stdout, stderr 리다이렉션
            with contextlib.redirect_stdout(output_buffer), \
                 contextlib.redirect_stderr(error_buffer):
                
                # 코드 실행
                exec(clean_code, exec_globals, exec_locals)
            
            # 실행 결과 수집
            output = output_buffer.getvalue()
            error_output = error_buffer.getvalue()
            
            # 출력 길이 제한
            if len(output) > self.max_output_length:
                output = output[:self.max_output_length] + "\n... (출력이 너무 길어 잘렸습니다)"
            
            execution_time = time.time() - start_time
            
            # 성공적인 실행
            result = {
                'success': True,
                'output': output,
                'error': error_output if error_output else None,
                'execution_time': round(execution_time, 3),
                'variables': self._extract_variables(exec_locals),
                'code': clean_code
            }
            
            return result
            
        except Exception as e:
            execution_time = time.time() - start_time
            error_message = str(e)
            error_type = type(e).__name__
            
            # 상세한 오류 정보
            tb = traceback.format_exc()
            
            return {
                'success': False,
                'error': error_message,
                'error_type': error_type,
                'traceback': tb,
                'output': output_buffer.getvalue(),
                'execution_time': round(execution_time, 3),
                'code': clean_code
            }
    
    def _extract_variables(self, locals_dict: Dict[str, Any]) -> Dict[str, Any]:
        """실행 후 변수들 추출"""
        variables = {}
        
        for name, value in locals_dict.items():
            if not name.startswith('_'):
                try:
                    # 직렬화 가능한 값들만 포함
                    if isinstance(value, (int, float, str, bool, list, dict, tuple)):
                        variables[name] = value
                    elif hasattr(value, '__str__'):
                        variables[name] = str(value)
                except:
                    variables[name] = f"<{type(value).__name__} object>"
        
        return variables
    
    def execute_with_imports(self, code: str) -> Dict[str, Any]:
        """필요한 라이브러리를 자동으로 import하여 실행"""
        # 일반적인 데이터 분석 라이브러리들을 미리 import
        setup_code = """
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import math
import statistics
from collections import Counter
"""
        
        full_code = setup_code + "\n" + code
        return self.execute_code(full_code)


class BrowserCodeExecutor:
    """브라우저 기반 Python 코드 실행기"""
    
    def __init__(self):
        self.executor = CodeExecutor()
        self.execution_queue = queue.Queue()
        self.result_cache = {}
        self.max_cache_size = 100
        
    def execute_async(self, code: str, session_id: str = "default") -> str:
        """비동기 코드 실행"""
        execution_id = f"{session_id}_{int(time.time() * 1000)}"
        
        # 실행 작업을 큐에 추가
        self.execution_queue.put({
            'execution_id': execution_id,
            'code': code,
            'session_id': session_id,
            'timestamp': datetime.now().isoformat()
        })
        
        # 별도 스레드에서 실행
        thread = threading.Thread(
            target=self._execute_in_thread,
            args=(execution_id, code, session_id)
        )
        thread.daemon = True
        thread.start()
        
        return execution_id
    
    def _execute_in_thread(self, execution_id: str, code: str, session_id: str):
        """스레드에서 코드 실행"""
        try:
            result = self.executor.execute_with_imports(code)
            result['execution_id'] = execution_id
            result['timestamp'] = datetime.now().isoformat()
            
            # 결과 캐시에 저장
            self._cache_result(execution_id, result)
            
        except Exception as e:
            error_result = {
                'success': False,
                'error': str(e),
                'execution_id': execution_id,
                'timestamp': datetime.now().isoformat()
            }
            self._cache_result(execution_id, error_result)
    
    def get_result(self, execution_id: str) -> Optional[Dict[str, Any]]:
        """실행 결과 조회"""
        return self.result_cache.get(execution_id)
    
    def _cache_result(self, execution_id: str, result: Dict[str, Any]):
        """결과 캐시 저장"""
        if len(self.result_cache) >= self.max_cache_size:
            # 가장 오래된 결과 제거
            oldest_key = min(self.result_cache.keys())
            del self.result_cache[oldest_key]
        
        self.result_cache[execution_id] = result
    
    def get_execution_status(self, execution_id: str) -> str:
        """실행 상태 확인"""
        if execution_id in self.result_cache:
            return "completed"
        else:
            return "running"


class InlineCodeRunner:
    """인라인 코드 실행기 - 웹 인터페이스용"""
    
    def __init__(self):
        self.executor = CodeExecutor()
        self.browser_executor = BrowserCodeExecutor()
        self.session_context = {}  # 세션별 컨텍스트 저장
        self.execution_history = {}  # 실행 기록
    
    def run_code_block(self, code: str, session_id: str = "default", 
                      async_execution: bool = False) -> Dict[str, Any]:
        """코드 블록 실행"""
        # 실행 기록 저장
        self._add_to_history(session_id, code)
        
        if async_execution:
            # 비동기 실행
            execution_id = self.browser_executor.execute_async(code, session_id)
            return {
                'async': True,
                'execution_id': execution_id,
                'status': 'running',
                'session_id': session_id
            }
        else:
            # 동기 실행
            return self._run_sync(code, session_id)
    
    def _run_sync(self, code: str, session_id: str) -> Dict[str, Any]:
        """동기 코드 실행"""
        # 세션 컨텍스트 가져오기
        if session_id not in self.session_context:
            self.session_context[session_id] = {}
        
        context = self.session_context[session_id]
        
        # 코드 실행
        result = self.executor.execute_with_imports(code)
        
        # 성공한 경우 컨텍스트 업데이트
        if result['success'] and 'variables' in result:
            context.update(result['variables'])
            self.session_context[session_id] = context
        
        # 세션 정보 추가
        result['session_id'] = session_id
        result['session_variables'] = list(context.keys())
        result['async'] = False
        
        return result
    
    def get_async_result(self, execution_id: str) -> Optional[Dict[str, Any]]:
        """비동기 실행 결과 조회"""
        return self.browser_executor.get_result(execution_id)
    
    def get_execution_status(self, execution_id: str) -> str:
        """실행 상태 확인"""
        return self.browser_executor.get_execution_status(execution_id)
    
    def _add_to_history(self, session_id: str, code: str):
        """실행 기록 추가"""
        if session_id not in self.execution_history:
            self.execution_history[session_id] = []
        
        self.execution_history[session_id].append({
            'code': code,
            'timestamp': datetime.now().isoformat()
        })
        
        # 최대 50개 기록만 유지
        if len(self.execution_history[session_id]) > 50:
            self.execution_history[session_id] = self.execution_history[session_id][-50:]
    
    def get_execution_history(self, session_id: str = "default") -> List[Dict[str, Any]]:
        """실행 기록 조회"""
        return self.execution_history.get(session_id, [])
    
    def clear_session(self, session_id: str = "default"):
        """세션 컨텍스트 초기화"""
        if session_id in self.session_context:
            del self.session_context[session_id]
        if session_id in self.execution_history:
            del self.execution_history[session_id]
    
    def get_session_info(self, session_id: str = "default") -> Dict[str, Any]:
        """세션 정보 조회"""
        context = self.session_context.get(session_id, {})
        history = self.execution_history.get(session_id, [])
        
        return {
            'session_id': session_id,
            'variables': context,
            'variable_count': len(context),
            'execution_count': len(history),
            'last_execution': history[-1]['timestamp'] if history else None
        }
    
    def export_session(self, session_id: str = "default") -> str:
        """세션 내보내기 (JSON)"""
        session_data = {
            'session_id': session_id,
            'variables': self.session_context.get(session_id, {}),
            'history': self.execution_history.get(session_id, []),
            'export_timestamp': datetime.now().isoformat()
        }
        
        return json.dumps(session_data, ensure_ascii=False, indent=2)
    
    def import_session(self, session_data: str, session_id: str = "default") -> bool:
        """세션 가져오기"""
        try:
            data = json.loads(session_data)
            
            if 'variables' in data:
                self.session_context[session_id] = data['variables']
            
            if 'history' in data:
                self.execution_history[session_id] = data['history']
            
            return True
        except Exception:
            return False


class WebCodeInterface:
    """웹 인터페이스용 코드 실행 API"""
    
    def __init__(self):
        self.runner = InlineCodeRunner()
    
    def execute_code_api(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """웹 API용 코드 실행"""
        try:
            code = request_data.get('code', '')
            session_id = request_data.get('session_id', 'default')
            async_execution = request_data.get('async', False)
            
            if not code.strip():
                return {
                    'success': False,
                    'error': '실행할 코드가 없습니다.',
                    'error_type': 'EmptyCode'
                }
            
            result = self.runner.run_code_block(code, session_id, async_execution)
            
            # 웹 응답용 포맷팅
            if result.get('async'):
                return {
                    'success': True,
                    'async': True,
                    'execution_id': result['execution_id'],
                    'status': 'running',
                    'message': '코드가 백그라운드에서 실행 중입니다.'
                }
            else:
                return self._format_sync_response(result)
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'error_type': type(e).__name__
            }
    
    def get_result_api(self, execution_id: str) -> Dict[str, Any]:
        """비동기 실행 결과 조회 API"""
        try:
            status = self.runner.get_execution_status(execution_id)
            
            if status == 'running':
                return {
                    'success': True,
                    'status': 'running',
                    'message': '코드가 아직 실행 중입니다.'
                }
            
            result = self.runner.get_async_result(execution_id)
            if result:
                return self._format_sync_response(result)
            else:
                return {
                    'success': False,
                    'error': '실행 결과를 찾을 수 없습니다.',
                    'status': 'not_found'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'error_type': type(e).__name__
            }
    
    def _format_sync_response(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """동기 실행 결과 포맷팅"""
        if result['success']:
            return {
                'success': True,
                'output': result.get('output', ''),
                'variables': result.get('variables', {}),
                'execution_time': result.get('execution_time', 0),
                'session_info': {
                    'session_id': result.get('session_id'),
                    'variable_count': len(result.get('session_variables', []))
                }
            }
        else:
            return {
                'success': False,
                'error': result.get('error', '알 수 없는 오류'),
                'error_type': result.get('error_type', 'UnknownError'),
                'output': result.get('output', ''),
                'suggestions': self._get_error_suggestions(result)
            }
    
    def _get_error_suggestions(self, result: Dict[str, Any]) -> List[str]:
        """오류 해결 제안"""
        suggestions = []
        error_type = result.get('error_type', '')
        error_message = result.get('error', '').lower()
        
        if 'syntaxerror' in error_type.lower():
            suggestions.extend([
                "문법 오류를 확인하세요 (괄호, 콜론, 들여쓰기)",
                "Python 문법 가이드를 참고하세요"
            ])
        
        elif 'nameerror' in error_type.lower():
            suggestions.extend([
                "변수나 함수 이름을 확인하세요",
                "필요한 라이브러리를 import했는지 확인하세요"
            ])
        
        elif 'typeerror' in error_type.lower():
            suggestions.extend([
                "데이터 타입을 확인하세요",
                "함수의 매개변수 개수와 타입을 확인하세요"
            ])
        
        elif 'indexerror' in error_type.lower():
            suggestions.extend([
                "리스트나 배열의 인덱스 범위를 확인하세요",
                "len() 함수로 크기를 먼저 확인해보세요"
            ])
        
        elif 'keyerror' in error_type.lower():
            suggestions.extend([
                "딕셔너리의 키가 존재하는지 확인하세요",
                "get() 메서드 사용을 고려해보세요"
            ])
        
        if 'security' in error_message:
            suggestions.append("보안상 제한된 기능입니다. 허용된 라이브러리만 사용하세요")
        
        return suggestions
    
    def get_session_api(self, session_id: str = "default") -> Dict[str, Any]:
        """세션 정보 조회 API"""
        try:
            session_info = self.runner.get_session_info(session_id)
            history = self.runner.get_execution_history(session_id)
            
            return {
                'success': True,
                'session_info': session_info,
                'recent_history': history[-5:] if history else []  # 최근 5개만
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def clear_session_api(self, session_id: str = "default") -> Dict[str, Any]:
        """세션 초기화 API"""
        try:
            self.runner.clear_session(session_id)
            return {
                'success': True,
                'message': f'세션 {session_id}이 초기화되었습니다.'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }


# 테스트용 함수
def test_code_executor():
    """코드 실행기 테스트"""
    executor = CodeExecutor()
    
    # 테스트 코드들
    test_codes = [
        # 1. 기본 계산
        """
x = 10
y = 20
result = x + y
print(f"결과: {result}")
""",
        
        # 2. 데이터 분석 예제
        """
import pandas as pd
import numpy as np

data = [1, 2, 3, 4, 5]
mean_val = np.mean(data)
print(f"평균: {mean_val}")
""",
        
        # 3. 보안 위반 코드 (실행되지 않아야 함)
        """
import os
os.system("ls")
""",
        
        # 4. 구문 오류 코드
        """
x = 10
y = 
print(x + y)
"""
    ]
    
    for i, code in enumerate(test_codes, 1):
        print(f"\n=== 테스트 {i} ===")
        print(f"코드:\n{code}")
        
        result = executor.execute_code(code)
        print(f"성공: {result['success']}")
        
        if result['success']:
            print(f"출력: {result['output']}")
            print(f"실행 시간: {result['execution_time']}초")
            if result.get('variables'):
                print(f"변수: {result['variables']}")
        else:
            print(f"오류: {result['error']}")
            if 'security_issues' in result:
                print(f"보안 문제: {result['security_issues']}")


if __name__ == "__main__":
    test_code_executor()