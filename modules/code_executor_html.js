/**
 * 코드 실행기 HTML 생성 모듈
 * GitHub Pages에서 사용할 수 있는 인라인 Python 코드 실행기를 생성합니다.
 */

function generateCodeExecutor(code = "", placeholder = "여기에 Python 코드를 입력하세요...", height = "300px") {
    return `
    <div class="code-executor" style="width: 100%; margin: 20px 0;">
        <div class="code-editor-container" style="border: 1px solid #ccc; border-radius: 4px; overflow: hidden;">
            <div class="toolbar" style="background: #f5f5f5; padding: 8px; border-bottom: 1px solid #ccc;">
                <button id="run-button" class="run-button btn btn-success btn-sm" style="padding: 6px 12px; border-radius: 4px; cursor: pointer;">
                    ▶️ 실행
                </button>
                <button id="clear-button" class="btn btn-danger btn-sm" style="padding: 6px 12px; border-radius: 4px; margin-left: 8px; cursor: pointer;">
                    🗑️ 지우기
                </button>
                <span id="execution-status" style="margin-left: 10px; font-size: 14px;"></span>
            </div>
            <textarea id="code-editor" style="width: 100%; height: ${height}; padding: 10px; font-family: monospace; font-size: 14px; line-height: 1.5; border: none; resize: vertical;" placeholder="${placeholder}">${code}</textarea>
        </div>
        
        <div class="output-container" style="margin-top: 10px; border: 1px solid #ccc; border-radius: 4px; overflow: hidden;">
            <div class="toolbar" style="background: #f5f5f5; padding: 8px; border-bottom: 1px solid #ccc;">
                <span style="font-weight: bold;">실행 결과</span>
                <button id="copy-output" class="btn btn-primary btn-sm" style="float: right; padding: 4px 8px; border-radius: 4px; cursor: pointer;">
                    📋 복사
                </button>
            </div>
            <pre id="output" style="margin: 0; padding: 10px; min-height: 100px; max-height: 300px; overflow-y: auto; background-color: #f8f8f8; font-family: monospace; white-space: pre-wrap;"></pre>
        </div>
        
        <div class="interpretation-container" style="margin-top: 10px; border: 1px solid #ccc; border-radius: 4px; overflow: hidden; display: none;">
            <div class="toolbar" style="background: #f5f5f5; padding: 8px; border-bottom: 1px solid #ccc;">
                <span style="font-weight: bold;">결과 해석</span>
            </div>
            <div id="interpretation" style="padding: 10px;"></div>
        </div>
    </div>

    <script>
    // 코드 실행기 초기화
    (async function() {
        // 상태 변수
        let pyodideReady = false;
        let pyodide = null;
        let outputElement = document.getElementById('output');
        let statusElement = document.getElementById('execution-status');
        let interpretationElement = document.getElementById('interpretation');
        let interpretationContainer = document.querySelector('.interpretation-container');
        
        // 상태 메시지 표시
        statusElement.textContent = "Pyodide 로딩 중...";
        
        try {
            // Pyodide 로드
            pyodide = await loadPyodide();
            await pyodide.loadPackagesFromImports(\`
                import numpy as np
                import pandas as pd
                import matplotlib.pyplot as plt
                from io import StringIO
            \`);
            
            pyodideReady = true;
            statusElement.textContent = "준비 완료";
        } catch (error) {
            statusElement.textContent = "Pyodide 로드 실패";
            outputElement.textContent = "오류: " + error.message;
            console.error("Pyodide 로드 오류:", error);
        }
        
        // 실행 버튼 이벤트 리스너
        document.getElementById('run-button').addEventListener('click', async () => {
            if (!pyodideReady) {
                outputElement.textContent = "Pyodide가 아직 준비되지 않았습니다. 잠시 후 다시 시도해주세요.";
                return;
            }
            
            const code = document.getElementById('code-editor').value;
            if (!code.trim()) {
                outputElement.textContent = "실행할 코드를 입력해주세요.";
                return;
            }
            
            // 실행 상태 업데이트
            statusElement.textContent = "실행 중...";
            outputElement.textContent = "코드 실행 중...";
            interpretationContainer.style.display = 'none';
            
            try {
                // 표준 출력 캡처를 위한 설정
                pyodide.runPython(\`
                    import sys
                    from io import StringIO
                    sys.stdout = StringIO()
                    sys.stderr = StringIO()
                \`);
                
                // 코드 실행
                const result = pyodide.runPython(code);
                
                // 표준 출력 및 오류 가져오기
                const stdout = pyodide.runPython("sys.stdout.getvalue()");
                const stderr = pyodide.runPython("sys.stderr.getvalue()");
                
                // 결과 표시
                let output = "";
                if (stdout) output += stdout;
                if (stderr) output += "\\n오류:\\n" + stderr;
                
                // 반환값이 있으면 추가
                if (result !== undefined && result !== null) {
                    if (output) output += "\\n\\n";
                    output += "반환값: " + String(result);
                    
                    // 결과 해석 시도
                    try {
                        const interpretation = interpretResult(result, code);
                        if (interpretation) {
                            interpretationElement.innerHTML = interpretation;
                            interpretationContainer.style.display = 'block';
                        }
                    } catch (e) {
                        console.error("결과 해석 오류:", e);
                    }
                }
                
                outputElement.textContent = output || "실행 완료 (출력 없음)";
                statusElement.textContent = "실행 완료";
                
            } catch (error) {
                outputElement.textContent = "실행 오류: " + error.message;
                statusElement.textContent = "오류 발생";
                console.error("코드 실행 오류:", error);
                
                // 오류 해석 및 도움말 제공
                try {
                    const errorHelp = getErrorHelp(error.message, code);
                    if (errorHelp) {
                        interpretationElement.innerHTML = errorHelp;
                        interpretationContainer.style.display = 'block';
                    }
                } catch (e) {
                    console.error("오류 해석 실패:", e);
                }
            }
        });
        
        // 지우기 버튼 이벤트 리스너
        document.getElementById('clear-button').addEventListener('click', () => {
            document.getElementById('code-editor').value = '';
            outputElement.textContent = '';
            interpretationContainer.style.display = 'none';
            statusElement.textContent = "준비 완료";
        });
        
        // 출력 복사 버튼 이벤트 리스너
        document.getElementById('copy-output').addEventListener('click', () => {
            const output = outputElement.textContent;
            if (!output) return;
            
            navigator.clipboard.writeText(output).then(() => {
                const originalText = document.getElementById('copy-output').textContent;
                document.getElementById('copy-output').textContent = "✓ 복사됨";
                setTimeout(() => {
                    document.getElementById('copy-output').textContent = originalText;
                }, 2000);
            });
        });
        
        // 결과 해석 함수
        function interpretResult(result, code) {
            // 코드 분석
            const isStatisticalAnalysis = /np\\.mean|np\\.std|np\\.percentile|np\\.median|describe\\(\\)|df\\.mean|df\\.std/.test(code);
            const isVisualization = /plt\\./.test(code);
            const isDataManipulation = /pd\\.DataFrame|pd\\.Series|pd\\.read_|df\\[/.test(code);
            
            let interpretation = "";
            
            // 결과 유형에 따른 해석
            if (result && typeof result === 'object') {
                // 숫자 배열인 경우
                if (result.length !== undefined && result.length > 0 && typeof result[0] === 'number') {
                    const arr = Array.from(result);
                    const mean = arr.reduce((a, b) => a + b, 0) / arr.length;
                    const stdDev = Math.sqrt(arr.map(x => Math.pow(x - mean, 2)).reduce((a, b) => a + b, 0) / arr.length);
                    
                    interpretation += "<h4>📊 데이터 요약</h4>";
                    interpretation += "<ul>";
                    interpretation += \`<li><strong>평균:</strong> \${mean.toFixed(2)}</li>\`;
                    interpretation += \`<li><strong>표준편차:</strong> \${stdDev.toFixed(2)}</li>\`;
                    interpretation += \`<li><strong>최소값:</strong> \${Math.min(...arr).toFixed(2)}</li>\`;
                    interpretation += \`<li><strong>최대값:</strong> \${Math.max(...arr).toFixed(2)}</li>\`;
                    interpretation += \`<li><strong>데이터 개수:</strong> \${arr.length}</li>\`;
                    interpretation += "</ul>";
                    
                    interpretation += "<h4>💡 해석 가이드</h4>";
                    interpretation += "<p>이 데이터는 ";
                    
                    if (stdDev / mean < 0.1) interpretation += "변동성이 낮은 ";
                    else if (stdDev / mean > 0.3) interpretation += "변동성이 높은 ";
                    else interpretation += "중간 정도의 변동성을 가진 ";
                    
                    interpretation += "수치형 데이터입니다.</p>";
                }
                // 기타 객체
                else {
                    interpretation += "<h4>🔍 결과 분석</h4>";
                    interpretation += "<p>객체 유형의 결과가 반환되었습니다.</p>";
                }
            }
            // 숫자인 경우
            else if (typeof result === 'number') {
                interpretation += "<h4>🔢 숫자 결과</h4>";
                interpretation += \`<p>계산된 값: <strong>\${result}</strong></p>\`;
                
                // 통계적 의미 추론
                if (isStatisticalAnalysis) {
                    interpretation += "<h4>📈 통계적 의미</h4>";
                    if (/mean|average/.test(code)) {
                        interpretation += "<p>이 값은 데이터의 <strong>평균</strong>으로, 중심 경향성을 나타냅니다.</p>";
                    } else if (/std|variance/.test(code)) {
                        interpretation += "<p>이 값은 데이터의 <strong>분산 또는 표준편차</strong>로, 데이터의 퍼짐 정도를 나타냅니다.</p>";
                    } else if (/median/.test(code)) {
                        interpretation += "<p>이 값은 데이터의 <strong>중앙값</strong>으로, 이상치에 덜 민감한 중심 경향성 측정값입니다.</p>";
                    }
                }
            }
            // 문자열인 경우
            else if (typeof result === 'string') {
                interpretation += "<h4>📝 텍스트 결과</h4>";
                interpretation += \`<p>반환된 텍스트 길이: <strong>\${result.length}</strong>자</p>\`;
            }
            
            // 코드 유형에 따른 추가 해석
            if (isStatisticalAnalysis) {
                interpretation += "<h4>📊 통계 분석 팁</h4>";
                interpretation += "<ul>";
                interpretation += "<li>데이터의 분포 형태를 시각화하려면 히스토그램을 사용해보세요.</li>";
                interpretation += "<li>이상치가 있는지 확인하려면 박스플롯을 활용하세요.</li>";
                interpretation += "<li>평균과 중앙값의 차이는 데이터의 치우침을 나타냅니다.</li>";
                interpretation += "</ul>";
            }
            else if (isVisualization) {
                interpretation += "<h4>📈 시각화 팁</h4>";
                interpretation += "<ul>";
                interpretation += "<li>제목과 축 레이블을 추가하면 그래프의 의미가 명확해집니다.</li>";
                interpretation += "<li>적절한 색상과 마커를 사용하면 가독성이 향상됩니다.</li>";
                interpretation += "<li>여러 그래프를 비교하려면 subplot을 활용하세요.</li>";
                interpretation += "</ul>";
            }
            else if (isDataManipulation) {
                interpretation += "<h4>🔍 데이터 처리 팁</h4>";
                interpretation += "<ul>";
                interpretation += "<li>결측값 처리는 데이터 분석의 중요한 단계입니다.</li>";
                interpretation += "<li>데이터 요약 통계는 describe() 메서드로 확인할 수 있습니다.</li>";
                interpretation += "<li>그룹별 집계는 groupby() 메서드를 활용하세요.</li>";
                interpretation += "</ul>";
            }
            
            return interpretation;
        }
        
        // 오류 도움말 함수
        function getErrorHelp(errorMessage) {
            let help = "<h4>❌ 오류 도움말</h4>";
            
            // 일반적인 오류 패턴 확인
            if (/NameError: name '(.+)' is not defined/.test(errorMessage)) {
                const varName = errorMessage.match(/NameError: name '(.+)' is not defined/)[1];
                help += \`<p><strong>정의되지 않은 변수/함수:</strong> '\${varName}'이(가) 정의되지 않았습니다.</p>\`;
                help += "<ul>";
                help += "<li>변수명이 올바르게 입력되었는지 확인하세요 (대소문자 구분).</li>";
                help += "<li>필요한 라이브러리를 import 했는지 확인하세요.</li>";
                help += \`<li>변수를 먼저 선언했는지 확인하세요 (예: \${varName} = 값).</li>\`;
                help += "</ul>";
            }
            else if (/SyntaxError: (.+)/.test(errorMessage)) {
                help += "<p><strong>문법 오류:</strong> Python 코드 문법에 문제가 있습니다.</p>";
                help += "<ul>";
                help += "<li>괄호, 따옴표, 콜론이 올바르게 짝을 이루는지 확인하세요.</li>";
                help += "<li>들여쓰기가 일관되게 되어있는지 확인하세요.</li>";
                help += "<li>문자열 안에 따옴표를 사용할 때는 이스케이프(\\) 또는 다른 종류의 따옴표를 사용하세요.</li>";
                help += "</ul>";
            }
            else if (/TypeError: (.+)/.test(errorMessage)) {
                help += "<p><strong>타입 오류:</strong> 데이터 타입이 맞지 않습니다.</p>";
                help += "<ul>";
                help += "<li>함수에 전달된 인자의 타입이 올바른지 확인하세요.</li>";
                help += "<li>문자열과 숫자를 연산할 때는 적절한 변환이 필요합니다 (str(), int(), float()).</li>";
                help += "<li>리스트, 딕셔너리 등의 자료구조를 올바르게 사용하고 있는지 확인하세요.</li>";
                help += "</ul>";
            }
            else if (/IndexError: (.+)/.test(errorMessage)) {
                help += "<p><strong>인덱스 오류:</strong> 리스트나 배열의 범위를 벗어났습니다.</p>";
                help += "<ul>";
                help += "<li>리스트의 길이를 확인하세요 (len(리스트)).</li>";
                help += "<li>인덱스는 0부터 시작합니다 (리스트[0]이 첫 번째 요소).</li>";
                help += "<li>음수 인덱스는 뒤에서부터 접근합니다 (리스트[-1]이 마지막 요소).</li>";
                help += "</ul>";
            }
            else if (/KeyError: (.+)/.test(errorMessage)) {
                const key = errorMessage.match(/KeyError: (.+)/)[1];
                help += \`<p><strong>키 오류:</strong> 딕셔너리나 DataFrame에 '\${key}' 키가 없습니다.</p>\`;
                help += "<ul>";
                help += "<li>키 이름이 올바른지 확인하세요 (대소문자 구분).</li>";
                help += "<li>딕셔너리의 모든 키를 확인하려면 dict.keys()를 사용하세요.</li>";
                help += "<li>DataFrame의 열 이름을 확인하려면 df.columns를 사용하세요.</li>";
                help += "</ul>";
            }
            else if (/AttributeError: (.+)/.test(errorMessage)) {
                help += "<p><strong>속성 오류:</strong> 객체에 존재하지 않는 속성이나 메서드를 호출했습니다.</p>";
                help += "<ul>";
                help += "<li>객체의 타입을 확인하세요 (type(객체)).</li>";
                help += "<li>메서드나 속성 이름이 올바른지 확인하세요.</li>";
                help += "<li>필요한 라이브러리를 import 했는지 확인하세요.</li>";
                help += "</ul>";
            }
            else if (/ValueError: (.+)/.test(errorMessage)) {
                help += "<p><strong>값 오류:</strong> 함수나 연산에 부적절한 값이 전달되었습니다.</p>";
                help += "<ul>";
                help += "<li>함수에 전달된 인자의 값이 허용 범위 내인지 확인하세요.</li>";
                help += "<li>문자열을 숫자로 변환할 때는 유효한 형식인지 확인하세요.</li>";
                help += "<li>리스트나 배열의 차원이 올바른지 확인하세요.</li>";
                help += "</ul>";
            }
            else if (/ZeroDivisionError: (.+)/.test(errorMessage)) {
                help += "<p><strong>0으로 나누기 오류:</strong> 0으로 나누려고 했습니다.</p>";
                help += "<ul>";
                help += "<li>나누는 값이 0이 아닌지 확인하세요.</li>";
                help += "<li>나누기 전에 조건문으로 0인지 확인하는 방어 코드를 추가하세요.</li>";
                help += "</ul>";
            }
            else {
                help += "<p>오류 메시지를 확인하고 코드를 검토해보세요.</p>";
                help += "<p><strong>오류 내용:</strong> " + errorMessage + "</p>";
            }
            
            help += "<h4>🔍 일반적인 디버깅 팁</h4>";
            help += "<ul>";
            help += "<li>코드를 작은 부분으로 나누어 테스트해보세요.</li>";
            help += "<li>print() 문을 사용하여 변수 값을 확인해보세요.</li>";
            help += "<li>복잡한 표현식은 여러 단계로 나누어 작성해보세요.</li>";
            help += "</ul>";
            
            return help;
        }
    })();
    </script>
    `;
}