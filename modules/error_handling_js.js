/**
 * 오류 처리 시스템 (JavaScript 버전)
 * 코드 실행 오류를 사용자 친화적으로 처리하고 해결 방법을 제안합니다.
 */

class ErrorHandlingSystem {
    constructor() {
        // 일반적인 오류 패턴 및 설명
        this.errorPatterns = {
            // 문법 오류
            "SyntaxError": {
                "description": "Python 코드 문법에 문제가 있습니다.",
                "commonCauses": [
                    "괄호, 따옴표, 콜론이 올바르게 짝을 이루지 않음",
                    "들여쓰기 불일치",
                    "예약어 잘못 사용",
                    "문자열 내 따옴표 처리 오류"
                ],
                "solutions": [
                    "코드의 괄호, 따옴표, 콜론이 올바르게 짝을 이루는지 확인하세요.",
                    "들여쓰기가 일관되게 되어있는지 확인하세요.",
                    "문자열 안에 따옴표를 사용할 때는 이스케이프(\\) 또는 다른 종류의 따옴표를 사용하세요."
                ]
            },
            // 이름 오류
            "NameError": {
                "description": "정의되지 않은 변수나 함수를 사용하려고 했습니다.",
                "commonCauses": [
                    "변수나 함수를 정의하기 전에 사용",
                    "변수명 오타",
                    "필요한 라이브러리 미포함",
                    "대소문자 구분 오류"
                ],
                "solutions": [
                    "변수명이 올바르게 입력되었는지 확인하세요 (대소문자 구분).",
                    "필요한 라이브러리를 import 했는지 확인하세요.",
                    "변수를 먼저 선언했는지 확인하세요."
                ]
            },
            // 타입 오류
            "TypeError": {
                "description": "데이터 타입이 맞지 않는 연산이나 함수 호출을 시도했습니다.",
                "commonCauses": [
                    "함수에 잘못된 타입의 인자 전달",
                    "문자열과 숫자 간 연산 시도",
                    "리스트, 딕셔너리 등의 자료구조 잘못 사용",
                    "메서드 호출 시 필수 인자 누락"
                ],
                "solutions": [
                    "함수에 전달된 인자의 타입이 올바른지 확인하세요.",
                    "문자열과 숫자를 연산할 때는 적절한 변환이 필요합니다 (str(), int(), float()).",
                    "리스트, 딕셔너리 등의 자료구조를 올바르게 사용하고 있는지 확인하세요."
                ]
            },
            // 인덱스 오류
            "IndexError": {
                "description": "리스트나 배열의 범위를 벗어난 인덱스에 접근하려고 했습니다.",
                "commonCauses": [
                    "리스트 길이보다 큰 인덱스 사용",
                    "빈 리스트에 접근 시도",
                    "음수 인덱스 잘못 사용"
                ],
                "solutions": [
                    "리스트의 길이를 확인하세요 (len(리스트)).",
                    "인덱스는 0부터 시작합니다 (리스트[0]이 첫 번째 요소).",
                    "음수 인덱스는 뒤에서부터 접근합니다 (리스트[-1]이 마지막 요소)."
                ]
            },
            // 키 오류
            "KeyError": {
                "description": "딕셔너리나 DataFrame에 존재하지 않는 키로 접근하려고 했습니다.",
                "commonCauses": [
                    "존재하지 않는 키 사용",
                    "키 이름 오타",
                    "대소문자 구분 오류"
                ],
                "solutions": [
                    "키 이름이 올바른지 확인하세요 (대소문자 구분).",
                    "딕셔너리의 모든 키를 확인하려면 dict.keys()를 사용하세요.",
                    "DataFrame의 열 이름을 확인하려면 df.columns를 사용하세요."
                ]
            }
        };
        
        // 특정 오류 패턴 정규식
        this.specificPatterns = {
            "undefined_variable": /NameError: name '(.+)' is not defined/,
            "key_error": /KeyError: '?(.+?)'?[,\)]/,
            "index_out_of_range": /IndexError: list index out of range/,
            "missing_parenthesis": /SyntaxError: unexpected EOF while parsing/,
            "invalid_syntax": /SyntaxError: invalid syntax/,
            "missing_module": /ModuleNotFoundError: No module named '(.+)'/,
            "attribute_error": /AttributeError: '(.+)' object has no attribute '(.+)'/,
            "type_error_concat": /TypeError: can only concatenate (.+) \(not "(.+)"\) to (.+)/,
            "zero_division": /ZeroDivisionError: division by zero/
        };
    } 
   /**
     * 코드 실행 오류 처리
     * @param {Error} error - 발생한 오류
     * @param {string} code - 실행된 코드
     * @returns {object} 오류 처리 결과
     */
    handleCodeExecutionError(error, code = null) {
        const errorType = error.name || "Error";
        const errorMessage = error.message || "알 수 없는 오류가 발생했습니다.";
        
        const result = {
            success: false,
            errorType: errorType,
            errorMessage: errorMessage,
            userMessage: this._generateUserMessage(errorType, errorMessage),
            suggestions: this._generateSuggestions(errorType, errorMessage, code),
            codeAnalysis: code ? this._analyzeCodeForErrors(code, errorType, errorMessage) : null
        };
        
        return result;
    }
    
    /**
     * 사용자 친화적인 오류 메시지 생성
     * @private
     */
    _generateUserMessage(errorType, errorMessage) {
        // 기본 메시지
        let userMessage = `코드 실행 중 오류가 발생했습니다: ${errorType}`;
        
        // 오류 유형별 메시지
        if (errorType in this.errorPatterns) {
            userMessage = `${this.errorPatterns[errorType].description} (${errorType})`;
        }
        
        // 특정 오류 패턴에 대한 더 구체적인 메시지
        for (const [patternName, pattern] of Object.entries(this.specificPatterns)) {
            const match = errorMessage.match(pattern);
            if (match) {
                if (patternName === "undefined_variable") {
                    const varName = match[1];
                    userMessage = `변수 '${varName}'이(가) 정의되지 않았습니다. 변수를 먼저 선언했는지 확인하세요.`;
                }
                
                else if (patternName === "key_error") {
                    const keyName = match[1];
                    userMessage = `키 '${keyName}'이(가) 딕셔너리나 DataFrame에 존재하지 않습니다.`;
                }
                
                else if (patternName === "index_out_of_range") {
                    userMessage = "리스트 인덱스가 범위를 벗어났습니다. 리스트 길이를 확인하세요.";
                }
                
                else if (patternName === "missing_parenthesis") {
                    userMessage = "괄호가 올바르게 닫히지 않았습니다. 괄호의 짝을 확인하세요.";
                }
                
                else if (patternName === "invalid_syntax") {
                    userMessage = "Python 문법에 오류가 있습니다. 구문을 확인하세요.";
                }
                
                else if (patternName === "missing_module") {
                    const moduleName = match[1];
                    userMessage = `모듈 '${moduleName}'을(를) 찾을 수 없습니다. 설치가 필요할 수 있습니다.`;
                }
                
                else if (patternName === "attribute_error") {
                    const objType = match[1];
                    const attrName = match[2];
                    userMessage = `'${objType}' 객체에 '${attrName}' 속성이나 메서드가 없습니다.`;
                }
                
                else if (patternName === "type_error_concat") {
                    const type1 = match[1];
                    const type2 = match[2];
                    userMessage = `${type1} 타입과 ${type2} 타입은 서로 연결할 수 없습니다. 타입 변환이 필요합니다.`;
                }
                
                else if (patternName === "zero_division") {
                    userMessage = "0으로 나누려고 했습니다. 나누는 값이 0이 아닌지 확인하세요.";
                }
                
                break;
            }
        }
        
        return userMessage;
    }
    
    /**
     * 오류 해결 제안 생성
     * @private
     */
    _generateSuggestions(errorType, errorMessage, code = null) {
        let suggestions = [];
        
        // 오류 유형별 기본 제안
        if (errorType in this.errorPatterns) {
            suggestions = [...this.errorPatterns[errorType].solutions];
        }
        
        // 특정 오류 패턴에 대한 더 구체적인 제안
        for (const [patternName, pattern] of Object.entries(this.specificPatterns)) {
            const match = errorMessage.match(pattern);
            if (match) {
                if (patternName === "undefined_variable") {
                    const varName = match[1];
                    suggestions = [
                        `변수 '${varName}'을(를) 사용하기 전에 정의했는지 확인하세요.`,
                        `변수명에 오타가 없는지 확인하세요 (대소문자 구분).`,
                        `필요한 라이브러리를 import 했는지 확인하세요.`
                    ];
                    
                    // 코드 분석을 통한 추가 제안
                    if (code) {
                        // 비슷한 변수명 찾기
                        const similarVars = this._findSimilarVariables(code, varName);
                        if (similarVars.length > 0) {
                            suggestions.push(`유사한 변수명이 발견되었습니다: ${similarVars.join(', ')}. 오타가 있는지 확인하세요.`);
                        }
                    }
                }
                
                else if (patternName === "key_error") {
                    const keyName = match[1];
                    suggestions = [
                        `키 '${keyName}'이(가) 딕셔너리나 DataFrame에 존재하는지 확인하세요.`,
                        "딕셔너리의 모든 키를 확인하려면 dict.keys()를 사용하세요.",
                        "DataFrame의 열 이름을 확인하려면 df.columns를 사용하세요."
                    ];
                    
                    // 코드 분석을 통한 추가 제안
                    if (code) {
                        // 비슷한 키 찾기
                        const similarKeys = this._findSimilarKeys(code, keyName);
                        if (similarKeys.length > 0) {
                            suggestions.push(`유사한 키가 발견되었습니다: ${similarKeys.join(', ')}. 오타가 있는지 확인하세요.`);
                        }
                    }
                }
                
                else if (patternName === "index_out_of_range") {
                    suggestions = [
                        "리스트의 길이를 확인하세요 (len(리스트)).",
                        "인덱스는 0부터 시작하고, 마지막 인덱스는 (길이 - 1)입니다.",
                        "리스트가 비어있는지 확인하세요.",
                        "인덱싱 전에 리스트 길이를 확인하는 조건문을 추가하세요."
                    ];
                }
                
                else if (patternName === "missing_parenthesis") {
                    suggestions = [
                        "괄호의 짝이 맞는지 확인하세요. 여는 괄호와 닫는 괄호의 수가 같아야 합니다.",
                        "중첩된 괄호를 사용할 때는 들여쓰기로 구조를 명확히 하세요.",
                        "문자열 내에서 괄호를 사용할 때는 이스케이프(\\)를 사용하거나 다른 종류의 따옴표를 사용하세요."
                    ];
                }
                
                else if (patternName === "invalid_syntax") {
                    suggestions = [
                        "Python 문법 규칙을 확인하세요.",
                        "괄호, 따옴표, 콜론이 올바르게 사용되었는지 확인하세요.",
                        "들여쓰기가 일관되게 되어있는지 확인하세요.",
                        "예약어(if, for, while 등)를 변수명으로 사용하지 않았는지 확인하세요."
                    ];
                }
                
                else if (patternName === "missing_module") {
                    const moduleName = match[1];
                    suggestions = [
                        `모듈 '${moduleName}'을(를) 설치해야 할 수 있습니다. 'pip install ${moduleName}'을 실행해보세요.`,
                        `모듈 이름에 오타가 없는지 확인하세요.`,
                        "가상 환경을 사용 중이라면 해당 환경에 모듈이 설치되었는지 확인하세요."
                    ];
                }
                
                else if (patternName === "attribute_error") {
                    const objType = match[1];
                    const attrName = match[2];
                    suggestions = [
                        `'${objType}' 객체에 '${attrName}' 속성이나 메서드가 있는지 확인하세요.`,
                        `메서드나 속성 이름에 오타가 없는지 확인하세요.`,
                        `객체의 타입을 확인하세요 (type(객체)).`,
                        "필요한 라이브러리를 import 했는지 확인하세요."
                    ];
                    
                    // 코드 분석을 통한 추가 제안
                    if (code) {
                        // 비슷한 속성/메서드 찾기
                        const similarAttrs = this._findSimilarAttributes(code, attrName);
                        if (similarAttrs.length > 0) {
                            suggestions.push(`유사한 속성/메서드가 발견되었습니다: ${similarAttrs.join(', ')}. 오타가 있는지 확인하세요.`);
                        }
                    }
                }
                
                else if (patternName === "type_error_concat") {
                    const type1 = match[1];
                    const type2 = match[2];
                    suggestions = [
                        `${type1} 타입과 ${type2} 타입은 서로 연결할 수 없습니다.`,
                        `${type2} 타입을 ${type1} 타입으로 변환해보세요. 예: str(변수) 또는 int(변수)`,
                        "변수의 타입을 확인하세요 (type(변수)).",
                        "문자열 포맷팅을 사용해보세요. 예: f'{숫자} 텍스트'"
                    ];
                }
                
                else if (patternName === "zero_division") {
                    suggestions = [
                        "나누는 값이 0이 아닌지 확인하세요.",
                        "나누기 전에 조건문으로 0인지 확인하는 방어 코드를 추가하세요. 예: if 분모 != 0: 결과 = 분자 / 분모",
                        "0으로 나누는 경우에 대한 예외 처리를 추가하세요. 예: try-except 블록 사용"
                    ];
                }
                
                break;
            }
        }
        
        // 일반적인 디버깅 팁 추가
        if (suggestions.length === 0) {
            suggestions = [
                "코드를 작은 부분으로 나누어 테스트해보세요.",
                "print() 문을 사용하여 변수 값을 확인해보세요.",
                "복잡한 표현식은 여러 단계로 나누어 작성해보세요."
            ];
        } else {
            suggestions.push("코드를 작은 부분으로 나누어 테스트하면 문제를 더 쉽게 찾을 수 있습니다.");
        }
        
        return suggestions;
    }
    
    /**
     * 코드 분석을 통한 오류 원인 파악
     * @private
     */
    _analyzeCodeForErrors(code, errorType, errorMessage) {
        const analysis = {
            potentialIssues: [],
            lineNumbers: [],
            variables: [],
            suggestions: []
        };
        
        if (!code) {
            return analysis;
        }
        
        // 코드 라인별로 분석
        const lines = code.split('\n');
        for (let i = 0; i < lines.length; i++) {
            const line = lines[i];
            const lineNum = i + 1;
            
            // 구문 오류 가능성 확인
            if (errorType === "SyntaxError") {
                // 괄호 짝 확인
                if ((line.match(/\(/g) || []).length !== (line.match(/\)/g) || []).length) {
                    analysis.potentialIssues.push(`라인 ${lineNum}: 괄호 짝이 맞지 않습니다.`);
                    analysis.lineNumbers.push(lineNum);
                }
                
                // 따옴표 짝 확인
                if ((line.match(/"/g) || []).length % 2 !== 0 && (line.match(/'/g) || []).length % 2 !== 0) {
                    analysis.potentialIssues.push(`라인 ${lineNum}: 따옴표 짝이 맞지 않습니다.`);
                    analysis.lineNumbers.push(lineNum);
                }
                
                // 콜론 누락 확인
                if (/\b(if|for|while|def|class|with|try|except|finally)\b.*[^:]\s*$/.test(line)) {
                    analysis.potentialIssues.push(`라인 ${lineNum}: 콜론(:)이 누락되었을 수 있습니다.`);
                    analysis.lineNumbers.push(lineNum);
                }
            }
            
            // 변수 정의 및 사용 확인
            if (errorType === "NameError") {
                const match = errorMessage.match(this.specificPatterns.undefined_variable);
                if (match) {
                    const varName = match[1];
                    
                    // 변수 사용 확인
                    const varRegex = new RegExp(`\\b${this._escapeRegExp(varName)}\\b`);
                    const assignRegex = new RegExp(`\\b${this._escapeRegExp(varName)}\\s*=`);
                    
                    if (varRegex.test(line) && !assignRegex.test(line)) {
                        analysis.potentialIssues.push(`라인 ${lineNum}: 정의되지 않은 변수 '${varName}'을(를) 사용하고 있습니다.`);
                        analysis.lineNumbers.push(lineNum);
                    }
                    
                    // 비슷한 변수명 찾기
                    const similarVars = this._findSimilarVariables(code, varName);
                    if (similarVars.length > 0) {
                        analysis.variables.push(...similarVars);
                        analysis.suggestions.push(`'${varName}' 대신 다음 중 하나를 사용하려고 했나요? ${similarVars.join(', ')}`);
                    }
                }
            }
            
            // 인덱스 오류 확인
            if (errorType === "IndexError") {
                // 리스트 인덱싱 패턴 확인
                const indexMatches = line.match(/(\w+)\[(\d+)\]/g);
                if (indexMatches) {
                    for (const match of indexMatches) {
                        const parts = match.match(/(\w+)\[(\d+)\]/);
                        if (parts) {
                            const varName = parts[1];
                            const index = parts[2];
                            analysis.variables.push(varName);
                            analysis.suggestions.push(`라인 ${lineNum}: '${varName}'의 길이가 ${index}보다 큰지 확인하세요.`);
                        }
                    }
                }
            }
            
            // 타입 오류 확인
            if (errorType === "TypeError") {
                // 문자열과 숫자 연결 시도 확인
                if (line.includes("+") && !line.includes("'+'") && !line.includes("\"+")) {
                    analysis.potentialIssues.push(`라인 ${lineNum}: 서로 다른 타입을 연결하려고 시도했을 수 있습니다.`);
                    analysis.lineNumbers.push(lineNum);
                    analysis.suggestions.push("문자열과 숫자를 연결할 때는 str() 함수를 사용하여 숫자를 문자열로 변환하세요.");
                }
            }
        }
        
        return analysis;
    }
    
    /**
     * 코드에서 비슷한 변수명 찾기
     * @private
     */
    _findSimilarVariables(code, varName) {
        const similarVars = [];
        
        // 변수 정의 패턴 찾기
        const varDefs = code.match(/\b(\w+)\s*=/g);
        if (!varDefs) return similarVars;
        
        for (const def of varDefs) {
            // 변수명 추출
            const varMatch = def.match(/\b(\w+)\s*=/);
            if (!varMatch) continue;
            
            const var2 = varMatch[1];
            
            // 같은 변수는 제외
            if (var2 === varName) continue;
            
            // 유사도 확인
            if (this._isSimilar(var2, varName)) {
                similarVars.push(var2);
            }
        }
        
        return similarVars;
    }
    
    /**
     * 코드에서 비슷한 키 찾기
     * @private
     */
    _findSimilarKeys(code, keyName) {
        const similarKeys = [];
        
        // 딕셔너리 키 패턴 찾기
        const keyPatterns = [
            /'([\w\s]+)':/g,  // 딕셔너리 정의에서의 키
            /"([\w\s]+)":/g,  // 딕셔너리 정의에서의 키 (쌍따옴표)
            /\['([\w\s]+)'\]/g,  // 딕셔너리 접근에서의 키
            /\["([\w\s]+)"\]/g   // 딕셔너리 접근에서의 키 (쌍따옴표)
        ];
        
        for (const pattern of keyPatterns) {
            const matches = code.matchAll(pattern);
            for (const match of matches) {
                const key = match[1];
                
                // 같은 키는 제외
                if (key === keyName) continue;
                
                // 유사도 확인
                if (this._isSimilar(key, keyName)) {
                    similarKeys.push(key);
                }
            }
        }
        
        return similarKeys;
    }
    
    /**
     * 코드에서 비슷한 속성/메서드 찾기
     * @private
     */
    _findSimilarAttributes(code, attrName) {
        const similarAttrs = [];
        
        // 속성/메서드 접근 패턴 찾기
        const attrPattern = /\.(\w+)/g;
        const matches = code.matchAll(attrPattern);
        
        for (const match of matches) {
            const attr = match[1];
            
            // 같은 속성은 제외
            if (attr === attrName) continue;
            
            // 유사도 확인
            if (this._isSimilar(attr, attrName)) {
                similarAttrs.push(attr);
            }
        }
        
        return similarAttrs;
    }
    
    /**
     * 두 문자열의 유사도 확인
     * @private
     */
    _isSimilar(str1, str2) {
        // 길이 차이가 너무 크면 유사하지 않음
        if (Math.abs(str1.length - str2.length) > 2) {
            return false;
        }
        
        // 첫 글자가 같으면 유사할 가능성 높음
        if (str1[0] === str2[0]) {
            // 레벤슈타인 거리 계산
            const distance = this._levenshteinDistance(str1, str2);
            return distance <= 2;
        }
        
        return false;
    }
    
    /**
     * 레벤슈타인 거리 계산
     * @private
     */
    _levenshteinDistance(str1, str2) {
        if (str1.length < str2.length) {
            return this._levenshteinDistance(str2, str1);
        }
        
        if (str2.length === 0) {
            return str1.length;
        }
        
        let previousRow = Array.from({ length: str2.length + 1 }, (_, i) => i);
        
        for (let i = 0; i < str1.length; i++) {
            const currentRow = [i + 1];
            
            for (let j = 0; j < str2.length; j++) {
                const insertions = previousRow[j + 1] + 1;
                const deletions = currentRow[j] + 1;
                const substitutions = previousRow[j] + (str1[i] !== str2[j] ? 1 : 0);
                
                currentRow.push(Math.min(insertions, deletions, substitutions));
            }
            
            previousRow = currentRow;
        }
        
        return previousRow[str2.length];
    }
    
    /**
     * 정규식 특수문자 이스케이프
     * @private
     */
    _escapeRegExp(string) {
        return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    }
    
    /**
     * 오류 도움말 HTML 생성
     */
    generateErrorHelpHTML(error, code = null) {
        // 오류 처리
        const errorInfo = this.handleCodeExecutionError(error, code);
        
        // HTML 생성
        let html = `
        <div class="error-container" style="margin: 20px 0; border: 1px solid #f44336; border-radius: 4px; overflow: hidden;">
            <div class="error-header" style="background: #ffebee; padding: 10px; border-bottom: 1px solid #f44336;">
                <h3 style="margin: 0; color: #d32f2f;">❌ 오류 발생</h3>
            </div>
            <div class="error-body" style="padding: 15px;">
        `;
        
        // 오류 메시지
        html += `
                <div class="error-message" style="margin-bottom: 15px;">
                    <h4 style="color: #d32f2f; margin-top: 0;">오류 메시지</h4>
                    <p style="background: #f5f5f5; padding: 10px; border-radius: 4px; font-family: monospace;">${errorInfo.errorType}: ${errorInfo.errorMessage}</p>
                </div>
        `;
        
        // 사용자 메시지
        html += `
                <div class="user-message" style="margin-bottom: 15px;">
                    <h4 style="color: #1976d2; margin-top: 0;">무슨 뜻인가요?</h4>
                    <p>${errorInfo.userMessage}</p>
                </div>
        `;
        
        // 해결 방법
        if (errorInfo.suggestions && errorInfo.suggestions.length > 0) {
            html += `
                <div class="suggestions">
                    <h4 style="color: #388e3c; margin-top: 0;">해결 방법</h4>
                    <ul style="padding-left: 20px;">
            `;
            
            for (const suggestion of errorInfo.suggestions) {
                html += `<li>${suggestion}</li>`;
            }
            
            html += `
                    </ul>
                </div>
            `;
        }
        
        // 코드 분석 결과
        if (errorInfo.codeAnalysis && errorInfo.codeAnalysis.potentialIssues && errorInfo.codeAnalysis.potentialIssues.length > 0) {
            html += `
                <div class="code-analysis" style="margin-top: 15px;">
                    <h4 style="color: #f57c00; margin-top: 0;">코드 분석 결과</h4>
                    <ul style="padding-left: 20px;">
            `;
            
            for (const issue of errorInfo.codeAnalysis.potentialIssues) {
                html += `<li>${issue}</li>`;
            }
            
            html += `
                    </ul>
                </div>
            `;
        }
        
        html += `
            </div>
        </div>
        `;
        
        return html;
    }
}

// 오류 처리 시스템 인스턴스 생성
const errorHandler = new ErrorHandlingSystem();

// 모듈 내보내기
function getErrorHelp(errorMessage, code = null) {
    // 오류 객체 생성
    const error = new Error(errorMessage);
    
    // 오류 유형 추출
    const errorTypeMatch = errorMessage.match(/^([A-Za-z]+Error):/);
    if (errorTypeMatch) {
        error.name = errorTypeMatch[1];
    }
    
    return errorHandler.generateErrorHelpHTML(error, code);
}