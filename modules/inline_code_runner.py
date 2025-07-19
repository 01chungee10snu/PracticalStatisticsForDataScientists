"""
Inline Code Runner - Browser-based Python Code Execution
"""

import sys
import io
import contextlib
import traceback
import time
from typing import Dict, Any, List, Optional, Tuple
import re
import json


class SafeCodeExecutor:
    """안전한 코드 실행기"""
    
    def __init__(self):
        self.execution_timeout = 10
        self.max_output_length = 5000
        
        # 미리 import된 라이브러리들
        self.available_modules = {}
        self._setup_safe_environment()
    
    def _setup_safe_environment(self):
        """안전한 실행 환경 설정"""
        try:
            import pandas as pd
            self.available_modules['pd'] = pd
            self.available_modules['pandas'] = pd
        except ImportError:
            pass
        
        try:
            import numpy as np
            self.available_modules['np'] = np
            self.available_modules['numpy'] = np
        except ImportError:
            pass
        
        try:
            import matplotlib.pyplot as plt
            self.available_modules['plt'] = plt
            self.available_modules['matplotlib'] = plt
        except ImportError:
            pass
        
        try:
            import seaborn as sns
            self.available_modules['sns'] = sns
            self.available_modules['seaborn'] = sns
        except ImportError:
            pass
        
        # 기본 모듈들
        import math
        import statistics
        import random
        from collections import Counter
        
        self.available_modules.update({
            'math': math,
            'statistics': statistics,
            'random': random,
            'Counter': Counter
        })
    
    def execute_code(self, code: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """코드 실행"""
        start_time = time.time()
        
        # 1. 기본 보안 검사
        if self._has_security_issues(code):
            return {
                'success': False,
                'error': '보안상 위험한 코드가 감지되었습니다.',
                'output': '',
                'execution_time': 0
            }
        
        # 2. 실행 환경 준비
        if context is None:
            context = {}
        
        # 안전한 내장 함수들
        safe_builtins = {
            'print': print, 'len': len, 'range': range, 'enumerate': enumerate,
            'zip': zip, 'map': map, 'filter': filter, 'sum': sum,
            'min': min, 'max': max, 'abs': abs, 'round': round,
            'sorted': sorted, 'reversed': reversed,
            'int': int, 'float': float, 'str': str, 'bool': bool,
            'list': list, 'dict': dict, 'tuple': tuple, 'set': set,
            'type': type, 'isinstance': isinstance
        }
        
        # 실행 컨텍스트 설정
        exec_globals = {
            '__builtins__': safe_builtins,
            **self.available_modules,
            **context
        }
        exec_locals = {}
        
        # 3. 출력 캡처
        output_buffer = io.StringIO()
        error_buffer = io.StringIO()
        
        try:
            with contextlib.redirect_stdout(output_buffer), \
                 contextlib.redirect_stderr(error_buffer):
                
                # 코드 실행
                exec(code, exec_globals, exec_locals)
            
            # 결과 수집
            output = output_buffer.getvalue()
            error_output = error_buffer.getvalue()
            
            if len(output) > self.max_output_length:
                output = output[:self.max_output_length] + "\n... (출력이 너무 길어 잘렸습니다)"
            
            execution_time = time.time() - start_time
            
            return {
                'success': True,
                'output': output,
                'error': error_output if error_output else None,
                'execution_time': round(execution_time, 3),
                'variables': self._extract_variables(exec_locals),
                'code': code
            }
            
        except Exception as e:
            execution_time = time.time() - start_time
            
            return {
                'success': False,
                'error': str(e),
                'error_type': type(e).__name__,
                'traceback': traceback.format_exc(),
                'output': output_buffer.getvalue(),
                'execution_time': round(execution_time, 3),
                'code': code
            }
    
    def _has_security_issues(self, code: str) -> bool:
        """기본 보안 검사"""
        dangerous_patterns = [
            'import os', 'import sys', 'import subprocess',
            'exec(', 'eval(', 'open(', '__import__',
            'file(', 'input(', 'raw_input('
        ]
        
        code_lower = code.lower()
        for pattern in dangerous_patterns:
            if pattern in code_lower:
                return True
        
        return False
    
    def _extract_variables(self, locals_dict: Dict[str, Any]) -> Dict[str, Any]:
        """변수 추출"""
        variables = {}
        
        for name, value in locals_dict.items():
            if not name.startswith('_'):
                try:
                    if isinstance(value, (int, float, str, bool, list, dict, tuple)):
                        variables[name] = value
                    else:
                        variables[name] = str(value)[:100]  # 긴 출력 제한
                except:
                    variables[name] = f"<{type(value).__name__}>"
        
        return variables


class InlineCodeRunner:
    """인라인 코드 실행기"""
    
    def __init__(self):
        self.executor = SafeCodeExecutor()
        self.sessions = {}  # 세션별 컨텍스트
    
    def run_code(self, code: str, session_id: str = "default") -> Dict[str, Any]:
        """코드 실행"""
        # 세션 컨텍스트 가져오기
        if session_id not in self.sessions:
            self.sessions[session_id] = {}
        
        context = self.sessions[session_id]
        
        # 코드 실행
        result = self.executor.execute_code(code, context)
        
        # 성공한 경우 컨텍스트 업데이트
        if result['success'] and 'variables' in result:
            context.update(result['variables'])
            self.sessions[session_id] = context
        
        # 추가 정보
        result['session_id'] = session_id
        result['available_modules'] = list(self.executor.available_modules.keys())
        
        return result
    
    def get_session_variables(self, session_id: str = "default") -> Dict[str, Any]:
        """세션 변수 조회"""
        return self.sessions.get(session_id, {})
    
    def clear_session(self, session_id: str = "default"):
        """세션 초기화"""
        if session_id in self.sessions:
            del self.sessions[session_id]
    
    def create_html_interface(self) -> str:
        """HTML 인터페이스 생성"""
        html = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Python 코드 실행기</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background: white;
            border-radius: 10px;
            padding: 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            text-align: center;
            margin-bottom: 30px;
        }
        .code-section {
            margin-bottom: 20px;
        }
        textarea {
            width: 100%;
            height: 200px;
            font-family: 'Courier New', monospace;
            font-size: 14px;
            padding: 15px;
            border: 2px solid #ddd;
            border-radius: 5px;
            resize: vertical;
        }
        .button-group {
            margin: 15px 0;
            text-align: center;
        }
        button {
            background: #007bff;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            margin: 0 10px;
        }
        button:hover {
            background: #0056b3;
        }
        .clear-btn {
            background: #dc3545;
        }
        .clear-btn:hover {
            background: #c82333;
        }
        .output {
            background: #f8f9fa;
            border: 2px solid #e9ecef;
            border-radius: 5px;
            padding: 15px;
            margin-top: 20px;
            font-family: 'Courier New', monospace;
            white-space: pre-wrap;
            max-height: 400px;
            overflow-y: auto;
        }
        .success {
            border-color: #28a745;
            background: #d4edda;
        }
        .error {
            border-color: #dc3545;
            background: #f8d7da;
            color: #721c24;
        }
        .info {
            background: #e3f2fd;
            border: 1px solid #2196f3;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        .variables {
            background: #fff3cd;
            border: 1px solid #ffc107;
            padding: 10px;
            border-radius: 5px;
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🐍 Python 코드 실행기</h1>
        
        <div class="info">
            <strong>사용 가능한 라이브러리:</strong> pandas (pd), numpy (np), matplotlib.pyplot (plt), seaborn (sns), math, statistics, random
        </div>
        
        <div class="code-section">
            <textarea id="codeInput" placeholder="여기에 Python 코드를 입력하세요...">
# 예제: 기술통계량 계산
import pandas as pd
import numpy as np

# 샘플 데이터
data = [85, 90, 78, 92, 88, 76, 95, 89, 84, 91]
df = pd.DataFrame({'scores': data})

# 기술통계량 계산
print("=== 기술통계량 ===")
print(f"평균: {df['scores'].mean():.2f}")
print(f"중앙값: {df['scores'].median():.2f}")
print(f"표준편차: {df['scores'].std():.2f}")
print(f"최솟값: {df['scores'].min()}")
print(f"최댓값: {df['scores'].max()}")
            </textarea>
        </div>
        
        <div class="button-group">
            <button onclick="runCode()">▶️ 코드 실행</button>
            <button onclick="clearOutput()">🗑️ 출력 지우기</button>
            <button class="clear-btn" onclick="clearSession()">🔄 세션 초기화</button>
        </div>
        
        <div id="output" class="output" style="display: none;"></div>
        <div id="variables" class="variables" style="display: none;"></div>
    </div>

    <script>
        let sessionId = 'web-session-' + Date.now();
        
        function runCode() {
            const code = document.getElementById('codeInput').value;
            const outputDiv = document.getElementById('output');
            const variablesDiv = document.getElementById('variables');
            
            if (!code.trim()) {
                alert('코드를 입력해주세요.');
                return;
            }
            
            outputDiv.style.display = 'block';
            outputDiv.innerHTML = '실행 중...';
            outputDiv.className = 'output';
            
            // 실제 구현에서는 서버로 요청을 보내야 합니다
            // 여기서는 시뮬레이션
            setTimeout(() => {
                try {
                    // 시뮬레이션된 결과
                    const result = simulateCodeExecution(code);
                    displayResult(result);
                } catch (error) {
                    displayError(error.message);
                }
            }, 500);
        }
        
        function simulateCodeExecution(code) {
            // 실제로는 서버에서 처리
            return {
                success: true,
                output: "=== 기술통계량 ===\\n평균: 86.80\\n중앙값: 88.50\\n표준편차: 5.94\\n최솟값: 76\\n최댓값: 95",
                execution_time: 0.023,
                variables: {
                    'data': '[85, 90, 78, 92, 88, 76, 95, 89, 84, 91]',
                    'df': 'DataFrame(10 rows x 1 columns)'
                }
            };
        }
        
        function displayResult(result) {
            const outputDiv = document.getElementById('output');
            const variablesDiv = document.getElementById('variables');
            
            if (result.success) {
                outputDiv.className = 'output success';
                outputDiv.innerHTML = result.output + `\\n\\n실행 시간: ${result.execution_time}초`;
                
                if (result.variables && Object.keys(result.variables).length > 0) {
                    variablesDiv.style.display = 'block';
                    variablesDiv.innerHTML = '<strong>생성된 변수들:</strong><br>' + 
                        Object.entries(result.variables)
                            .map(([key, value]) => `${key}: ${value}`)
                            .join('<br>');
                }
            } else {
                outputDiv.className = 'output error';
                outputDiv.innerHTML = `오류: ${result.error}\\n\\n${result.traceback || ''}`;
                variablesDiv.style.display = 'none';
            }
        }
        
        function displayError(message) {
            const outputDiv = document.getElementById('output');
            outputDiv.className = 'output error';
            outputDiv.innerHTML = `오류: ${message}`;
        }
        
        function clearOutput() {
            document.getElementById('output').style.display = 'none';
            document.getElementById('variables').style.display = 'none';
        }
        
        function clearSession() {
            sessionId = 'web-session-' + Date.now();
            clearOutput();
            alert('세션이 초기화되었습니다.');
        }
    </script>
</body>
</html>
        """
        return html


def test_inline_code_runner():
    """인라인 코드 실행기 테스트"""
    runner = InlineCodeRunner()
    
    print("=== 인라인 코드 실행기 테스트 ===")
    
    # 테스트 1: 기본 계산
    print("\n1. 기본 계산 테스트")
    code1 = """
x = 10
y = 20
result = x + y
print(f"x + y = {result}")
"""
    result1 = runner.run_code(code1)
    print(f"성공: {result1['success']}")
    print(f"출력: {result1['output']}")
    print(f"변수: {result1.get('variables', {})}")
    
    # 테스트 2: 데이터 분석 (pandas 사용)
    print("\n2. 데이터 분석 테스트")
    code2 = """
import pandas as pd
import numpy as np

data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
df = pd.DataFrame({'numbers': data})

mean_val = df['numbers'].mean()
std_val = df['numbers'].std()

print(f"데이터: {data}")
print(f"평균: {mean_val}")
print(f"표준편차: {std_val:.2f}")
"""
    result2 = runner.run_code(code2)
    print(f"성공: {result2['success']}")
    if result2['success']:
        print(f"출력: {result2['output']}")
    else:
        print(f"오류: {result2['error']}")
    
    # 테스트 3: 세션 지속성
    print("\n3. 세션 지속성 테스트")
    code3 = """
# 이전에 정의된 변수 사용
print(f"이전 결과 재사용: {result}")
new_calc = result * 2
print(f"새로운 계산: {new_calc}")
"""
    result3 = runner.run_code(code3)
    print(f"성공: {result3['success']}")
    if result3['success']:
        print(f"출력: {result3['output']}")
    else:
        print(f"오류: {result3['error']}")
    
    print(f"\n사용 가능한 모듈: {result1.get('available_modules', [])}")


if __name__ == "__main__":
    test_inline_code_runner()