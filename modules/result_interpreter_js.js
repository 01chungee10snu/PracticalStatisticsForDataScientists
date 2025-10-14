/**
 * 결과 해석 시스템 (JavaScript 버전)
 * 코드 실행 결과의 통계적 의미와 실무적 해석을 제공합니다.
 */

class ResultInterpreter {
    constructor() {
        // 통계 용어 사전
        this.statsTerms = {
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
        };
        
        // 결과 해석 템플릿
        this.interpretationTemplates = {
            "mean": "평균 {value}은(는) 데이터의 중심 경향성을 나타냅니다. 모든 값의 합을 개수로 나눈 값입니다.",
            "median": "중앙값 {value}은(는) 데이터를 크기 순으로 나열했을 때 가운데 위치한 값입니다. 이상치에 덜 민감한 중심 경향성 측정값입니다.",
            "std": "표준편차 {value}은(는) 데이터가 평균으로부터 얼마나 퍼져 있는지를 나타냅니다. 값이 클수록 데이터의 변동성이 큽니다.",
            "correlation": "상관계수 {value}은(는) 두 변수 간의 선형 관계 강도를 나타냅니다. 1에 가까울수록 강한 양의 상관관계, -1에 가까울수록 강한 음의 상관관계를 의미합니다.",
            "p_value": "p-값 {value}은(는) 귀무가설이 참일 때 관측된 결과(또는 더 극단적인 결과)가 나올 확률입니다. 일반적으로 0.05보다 작으면 통계적으로 유의하다고 판단합니다."
        };
    }
    
    /**
     * 결과 해석
     * @param {any} result - 코드 실행 결과
     * @param {string} code - 실행된 코드
     * @param {string} conceptType - 개념 유형 (descriptive_stats, inferential_stats, regression, etc.)
     * @returns {object} 해석 결과
     */
    interpretResult(result, code = null, conceptType = null) {
        const interpretation = {
            statisticalMeaning: [],
            practicalInterpretation: [],
            recommendations: [],
            codeAnalysis: code ? this._analyzeCode(code) : {}
        };
        
        // 결과 유형에 따른 해석
        if (result && typeof result === 'object') {
            // 배열 또는 유사 배열 객체인 경우
            if (result.length !== undefined) {
                Object.assign(interpretation, this._interpretArrayResult(result, conceptType));
            } 
            // 일반 객체인 경우
            else {
                Object.assign(interpretation, this._interpretObjectResult(result, conceptType));
            }
        } 
        // 숫자인 경우
        else if (typeof result === 'number') {
            Object.assign(interpretation, this._interpretNumericResult(result, code, conceptType));
        } 
        // 문자열인 경우
        else if (typeof result === 'string') {
            Object.assign(interpretation, this._interpretStringResult(result, conceptType));
        } 
        // 기타 유형
        else {
            interpretation.statisticalMeaning.push("결과 유형에 대한 통계적 해석을 제공할 수 없습니다.");
            interpretation.practicalInterpretation.push("실행 결과를 확인하고 필요한 추가 분석을 수행하세요.");
        }
        
        // 코드 분석 기반 추가 해석
        if (code) {
            const codeAnalysis = this._analyzeCode(code);
            
            // 통계 분석 코드인 경우
            if (codeAnalysis.isStatisticalAnalysis) {
                const statsFunctions = codeAnalysis.statisticalFunctions || [];
                
                if (statsFunctions.includes('mean')) {
                    interpretation.statisticalMeaning.push("평균은 데이터의 중심 경향성을 나타내는 기본적인 통계량입니다.");
                    interpretation.practicalInterpretation.push("평균은 이상치에 민감하므로, 데이터에 극단값이 있는 경우 중앙값도 함께 확인하는 것이 좋습니다.");
                }
                
                if (statsFunctions.includes('std') || statsFunctions.includes('var')) {
                    interpretation.statisticalMeaning.push("표준편차와 분산은 데이터의 퍼짐 정도를 나타내는 지표입니다.");
                    interpretation.practicalInterpretation.push("표준편차가 클수록 데이터의 변동성이 크며, 작을수록 평균 주변에 데이터가 밀집되어 있음을 의미합니다.");
                }
                
                if (statsFunctions.includes('corr') || statsFunctions.includes('correlation')) {
                    interpretation.statisticalMeaning.push("상관계수는 두 변수 간의 선형 관계 강도를 -1에서 1 사이의 값으로 나타냅니다.");
                    interpretation.practicalInterpretation.push("상관관계가 있다고 해서 반드시 인과관계가 있는 것은 아닙니다. 다른 요인의 영향도 고려해야 합니다.");
                }
            }
            
            // 시각화 코드인 경우
            if (codeAnalysis.isVisualization) {
                const vizTypes = codeAnalysis.visualizationTypes || [];
                
                if (vizTypes.includes('histogram')) {
                    interpretation.statisticalMeaning.push("히스토그램은 데이터의 분포를 시각화하는 도구로, 구간별 빈도를 보여줍니다.");
                    interpretation.practicalInterpretation.push("히스토그램의 모양을 통해 데이터가 정규분포를 따르는지, 치우침이 있는지 등을 파악할 수 있습니다.");
                }
                
                if (vizTypes.includes('scatter')) {
                    interpretation.statisticalMeaning.push("산점도는 두 변수 간의 관계를 시각화하는 도구입니다.");
                    interpretation.practicalInterpretation.push("점들이 일정한 패턴을 보이면 두 변수 간에 관계가 있을 가능성이 높습니다.");
                }
                
                if (vizTypes.includes('boxplot')) {
                    interpretation.statisticalMeaning.push("박스플롯은 데이터의 분포, 중앙값, 사분위수, 이상치 등을 한눈에 보여줍니다.");
                    interpretation.practicalInterpretation.push("박스의 크기(IQR)는 데이터의 산포도를 나타내며, 박스 바깥의 점들은 이상치일 가능성이 있습니다.");
                }
            }
        }
        
        // 추천사항 추가
        if (interpretation.recommendations.length === 0) {
            interpretation.recommendations = this._generateRecommendations(result, code, conceptType);
        }
        
        return interpretation;
    }
    
    /**
     * 배열 결과 해석
     * @private
     */
    _interpretArrayResult(result, conceptType) {
        const interpretation = {
            statisticalMeaning: [],
            practicalInterpretation: []
        };
        
        // 숫자 배열인지 확인
        try {
            // 모든 요소가 숫자인지 확인
            const isNumericArray = Array.from(result).every(item => typeof item === 'number');
            
            if (isNumericArray) {
                const arr = Array.from(result);
                const mean = arr.reduce((a, b) => a + b, 0) / arr.length;
                const variance = arr.reduce((a, b) => a + Math.pow(b - mean, 2), 0) / arr.length;
                const stdDev = Math.sqrt(variance);
                const min = Math.min(...arr);
                const max = Math.max(...arr);
                
                // 중앙값 계산
                const sortedArr = [...arr].sort((a, b) => a - b);
                let median;
                if (sortedArr.length % 2 === 0) {
                    median = (sortedArr[sortedArr.length / 2 - 1] + sortedArr[sortedArr.length / 2]) / 2;
                } else {
                    median = sortedArr[Math.floor(sortedArr.length / 2)];
                }
                
                // 사분위수 계산
                const q1Idx = Math.floor(sortedArr.length * 0.25);
                const q3Idx = Math.floor(sortedArr.length * 0.75);
                const q1 = sortedArr[q1Idx];
                const q3 = sortedArr[q3Idx];
                
                interpretation.statisticalMeaning.push(`데이터 개수: ${arr.length}`);
                interpretation.statisticalMeaning.push(`평균: ${mean.toFixed(2)}`);
                interpretation.statisticalMeaning.push(`중앙값: ${median.toFixed(2)}`);
                interpretation.statisticalMeaning.push(`표준편차: ${stdDev.toFixed(2)}`);
                interpretation.statisticalMeaning.push(`범위: ${min.toFixed(2)} ~ ${max.toFixed(2)}`);
                
                // 분포 특성 해석
                if (mean > median) {
                    interpretation.practicalInterpretation.push(
                        `평균(${mean.toFixed(2)})이 중앙값(${median.toFixed(2)})보다 크므로, 데이터가 오른쪽으로 치우친 분포를 가질 가능성이 있습니다.`
                    );
                } else if (mean < median) {
                    interpretation.practicalInterpretation.push(
                        `평균(${mean.toFixed(2)})이 중앙값(${median.toFixed(2)})보다 작으므로, 데이터가 왼쪽으로 치우친 분포를 가질 가능성이 있습니다.`
                    );
                } else {
                    interpretation.practicalInterpretation.push(
                        `평균(${mean.toFixed(2)})과 중앙값(${median.toFixed(2)})이 같으므로, 데이터가 대칭적인 분포를 가질 가능성이 높습니다.`
                    );
                }
                
                // 변동계수(CV) 계산 및 해석
                if (mean !== 0) {
                    const cv = stdDev / mean;
                    interpretation.statisticalMeaning.push(`변동계수(CV): ${cv.toFixed(2)}`);
                    
                    if (cv < 0.1) {
                        interpretation.practicalInterpretation.push(
                            "변동계수가 0.1보다 작으므로, 데이터의 변동성이 낮습니다. 값들이 평균 주변에 밀집되어 있습니다."
                        );
                    } else if (cv > 0.3) {
                        interpretation.practicalInterpretation.push(
                            "변동계수가 0.3보다 크므로, 데이터의 변동성이 높습니다. 값들이 평균으로부터 넓게 퍼져 있습니다."
                        );
                    } else {
                        interpretation.practicalInterpretation.push(
                            "변동계수가 중간 정도로, 데이터가 적절한 변동성을 가지고 있습니다."
                        );
                    }
                }
            } else {
                interpretation.statisticalMeaning.push(`데이터 개수: ${result.length}`);
                interpretation.practicalInterpretation.push("비숫자 데이터이므로 기술통계량을 계산할 수 없습니다.");
            }
        } catch (error) {
            interpretation.statisticalMeaning.push(`데이터 개수: ${result.length}`);
            interpretation.practicalInterpretation.push("데이터 분석 중 오류가 발생했습니다.");
        }
        
        return interpretation;
    }
    
    /**
     * 객체 결과 해석
     * @private
     */
    _interpretObjectResult(result, conceptType) {
        const interpretation = {
            statisticalMeaning: [],
            practicalInterpretation: []
        };
        
        // 통계 결과 객체인지 확인
        if ('mean' in result || 'median' in result || 'std' in result) {
            interpretation.statisticalMeaning.push("이 결과는 기술통계량을 포함하고 있습니다.");
            
            if ('mean' in result && typeof result.mean === 'number') {
                interpretation.statisticalMeaning.push(
                    this.interpretationTemplates.mean.replace('{value}', result.mean.toFixed(2))
                );
            }
            
            if ('median' in result && typeof result.median === 'number') {
                interpretation.statisticalMeaning.push(
                    this.interpretationTemplates.median.replace('{value}', result.median.toFixed(2))
                );
            }
            
            if ('std' in result && typeof result.std === 'number') {
                interpretation.statisticalMeaning.push(
                    this.interpretationTemplates.std.replace('{value}', result.std.toFixed(2))
                );
            }
            
            // 평균과 중앙값 비교
            if ('mean' in result && 'median' in result) {
                const mean = result.mean;
                const median = result.median;
                
                if (typeof mean === 'number' && typeof median === 'number') {
                    if (mean > median) {
                        interpretation.practicalInterpretation.push(
                            `평균(${mean.toFixed(2)})이 중앙값(${median.toFixed(2)})보다 크므로, 데이터가 오른쪽으로 치우친(right-skewed) 분포를 가질 가능성이 있습니다. 이는 큰 값의 이상치가 있을 수 있음을 의미합니다.`
                        );
                    } else if (mean < median) {
                        interpretation.practicalInterpretation.push(
                            `평균(${mean.toFixed(2)})이 중앙값(${median.toFixed(2)})보다 작으므로, 데이터가 왼쪽으로 치우친(left-skewed) 분포를 가질 가능성이 있습니다. 이는 작은 값의 이상치가 있을 수 있음을 의미합니다.`
                        );
                    } else {
                        interpretation.practicalInterpretation.push(
                            `평균(${mean.toFixed(2)})과 중앙값(${median.toFixed(2)})이 같으므로, 데이터가 대칭적인 분포를 가질 가능성이 높습니다.`
                        );
                    }
                }
            }
        }
        
        // 상관관계 결과인지 확인
        if ('correlation' in result || 'corr' in result) {
            const corrKey = 'correlation' in result ? 'correlation' : 'corr';
            const corrValue = result[corrKey];
            
            if (typeof corrValue === 'number') {
                interpretation.statisticalMeaning.push(
                    this.interpretationTemplates.correlation.replace('{value}', corrValue.toFixed(2))
                );
                
                // 상관관계 강도 해석
                let strength;
                if (Math.abs(corrValue) > 0.7) {
                    strength = "강한";
                } else if (Math.abs(corrValue) > 0.3) {
                    strength = "중간 정도의";
                } else {
                    strength = "약한";
                }
                
                const direction = corrValue > 0 ? "양의" : "음의";
                
                interpretation.practicalInterpretation.push(
                    `상관계수 ${corrValue.toFixed(2)}는 두 변수 간에 ${strength} ${direction} 선형 관계가 있음을 나타냅니다.`
                );
                
                if (Math.abs(corrValue) > 0.7) {
                    interpretation.practicalInterpretation.push(
                        "두 변수가 매우 밀접하게 관련되어 있으므로, 한 변수의 변화가 다른 변수의 변화와 강하게 연관될 가능성이 높습니다."
                    );
                }
            }
        }
        
        // 가설 검정 결과인지 확인
        if ('p_value' in result || 'pvalue' in result) {
            const pKey = 'p_value' in result ? 'p_value' : 'pvalue';
            const pValue = result[pKey];
            
            if (typeof pValue === 'number') {
                interpretation.statisticalMeaning.push(
                    this.interpretationTemplates.p_value.replace('{value}', pValue.toFixed(4))
                );
                
                // p-값 해석
                if (pValue < 0.01) {
                    interpretation.practicalInterpretation.push(
                        `p-값(${pValue.toFixed(4)})이 0.01보다 작으므로, 매우 강한 통계적 유의성을 나타냅니다. 귀무가설을 기각할 충분한 증거가 있습니다.`
                    );
                } else if (pValue < 0.05) {
                    interpretation.practicalInterpretation.push(
                        `p-값(${pValue.toFixed(4)})이 0.05보다 작으므로, 통계적으로 유의합니다. 귀무가설을 기각할 충분한 증거가 있습니다.`
                    );
                } else {
                    interpretation.practicalInterpretation.push(
                        `p-값(${pValue.toFixed(4)})이 0.05보다 크므로, 통계적으로 유의하지 않습니다. 귀무가설을 기각할 충분한 증거가 없습니다.`
                    );
                }
            }
        }
        
        return interpretation;
    }
    
    /**
     * 숫자 결과 해석
     * @private
     */
    _interpretNumericResult(result, code, conceptType) {
        const interpretation = {
            statisticalMeaning: [],
            practicalInterpretation: []
        };
        
        // 코드 분석을 통한 맥락 파악
        if (code) {
            const codeAnalysis = this._analyzeCode(code);
            
            // 평균 계산 결과인지 확인
            if (/mean|average|np\.mean|\.mean\(\)/.test(code)) {
                interpretation.statisticalMeaning.push(
                    this.interpretationTemplates.mean.replace('{value}', result.toFixed(2))
                );
                interpretation.practicalInterpretation.push(
                    "평균은 이상치에 민감하므로, 데이터에 극단값이 있는 경우 중앙값도 함께 확인하는 것이 좋습니다."
                );
            }
            
            // 중앙값 계산 결과인지 확인
            else if (/median|np\.median|\.median\(\)/.test(code)) {
                interpretation.statisticalMeaning.push(
                    this.interpretationTemplates.median.replace('{value}', result.toFixed(2))
                );
                interpretation.practicalInterpretation.push(
                    "중앙값은 이상치에 덜 민감하므로, 치우친 분포나 이상치가 있는 데이터에서 중심 경향성을 파악하는 데 유용합니다."
                );
            }
            
            // 표준편차 계산 결과인지 확인
            else if (/std|standard deviation|np\.std|\.std\(\)/.test(code)) {
                interpretation.statisticalMeaning.push(
                    this.interpretationTemplates.std.replace('{value}', result.toFixed(2))
                );
                interpretation.practicalInterpretation.push(
                    "표준편차가 클수록 데이터의 변동성이 크며, 작을수록 평균 주변에 데이터가 밀집되어 있음을 의미합니다."
                );
            }
            
            // 상관계수 계산 결과인지 확인
            else if (/corr|correlation|np\.corrcoef|\.corr\(\)/.test(code)) {
                interpretation.statisticalMeaning.push(
                    this.interpretationTemplates.correlation.replace('{value}', result.toFixed(2))
                );
                
                // 상관관계 강도 해석
                let strength;
                if (Math.abs(result) > 0.7) {
                    strength = "강한";
                } else if (Math.abs(result) > 0.3) {
                    strength = "중간 정도의";
                } else {
                    strength = "약한";
                }
                
                const direction = result > 0 ? "양의" : "음의";
                
                interpretation.practicalInterpretation.push(
                    `상관계수 ${result.toFixed(2)}는 두 변수 간에 ${strength} ${direction} 선형 관계가 있음을 나타냅니다.`
                );
                
                interpretation.practicalInterpretation.push(
                    "상관관계가 있다고 해서 반드시 인과관계가 있는 것은 아닙니다. 다른 요인의 영향도 고려해야 합니다."
                );
            }
            
            // p-값 계산 결과인지 확인
            else if (/p-value|pvalue|\.pvalue|significance/.test(code)) {
                interpretation.statisticalMeaning.push(
                    this.interpretationTemplates.p_value.replace('{value}', result.toFixed(4))
                );
                
                // p-값 해석
                if (result < 0.01) {
                    interpretation.practicalInterpretation.push(
                        `p-값(${result.toFixed(4)})이 0.01보다 작으므로, 매우 강한 통계적 유의성을 나타냅니다. 귀무가설을 기각할 충분한 증거가 있습니다.`
                    );
                } else if (result < 0.05) {
                    interpretation.practicalInterpretation.push(
                        `p-값(${result.toFixed(4)})이 0.05보다 작으므로, 통계적으로 유의합니다. 귀무가설을 기각할 충분한 증거가 있습니다.`
                    );
                } else {
                    interpretation.practicalInterpretation.push(
                        `p-값(${result.toFixed(4)})이 0.05보다 크므로, 통계적으로 유의하지 않습니다. 귀무가설을 기각할 충분한 증거가 없습니다.`
                    );
                }
            }
            
            // 일반적인 숫자 결과
            else {
                interpretation.statisticalMeaning.push(`계산 결과: ${result.toFixed(2)}`);
                interpretation.practicalInterpretation.push("이 값의 맥락과 의미는 계산 방법과 데이터의 특성에 따라 달라집니다.");
            }
        } else {
            // 코드 정보가 없는 경우
            interpretation.statisticalMeaning.push(`계산 결과: ${result.toFixed(2)}`);
            interpretation.practicalInterpretation.push("이 값의 맥락과 의미는 계산 방법과 데이터의 특성에 따라 달라집니다.");
        }
        
        return interpretation;
    }
    
    /**
     * 문자열 결과 해석
     * @private
     */
    _interpretStringResult(result, conceptType) {
        const interpretation = {
            statisticalMeaning: [],
            practicalInterpretation: []
        };
        
        // 통계 결과가 포함된 문자열인지 확인
        const statsPatterns = {
            "mean": /mean[:\s=]+(\d+\.?\d*)/i,
            "median": /median[:\s=]+(\d+\.?\d*)/i,
            "std": /std|standard deviation[:\s=]+(\d+\.?\d*)/i,
            "correlation": /corr|correlation[:\s=]+([-]?\d+\.?\d*)/i,
            "p_value": /p-?value[:\s=]+([\d\.e\-]+)/i
        };
        
        for (const [stat, pattern] of Object.entries(statsPatterns)) {
            const match = result.match(pattern);
            if (match) {
                try {
                    const value = parseFloat(match[1]);
                    if (stat in this.interpretationTemplates) {
                        interpretation.statisticalMeaning.push(
                            this.interpretationTemplates[stat].replace('{value}', value.toFixed(2))
                        );
                    }
                } catch (e) {
                    // 파싱 오류 무시
                }
            }
        }
        
        // 일반적인 문자열 결과
        if (interpretation.statisticalMeaning.length === 0) {
            interpretation.statisticalMeaning.push("텍스트 결과에서 통계적 의미를 추출할 수 없습니다.");
            interpretation.practicalInterpretation.push("결과를 직접 검토하여 관련 정보를 확인하세요.");
        }
        
        return interpretation;
    }
    
    /**
     * 코드 분석
     * @private
     */
    _analyzeCode(code) {
        if (!code) {
            return {};
        }
        
        const analysis = {
            isStatisticalAnalysis: false,
            isVisualization: false,
            statisticalFunctions: [],
            visualizationTypes: [],
            librariesUsed: []
        };
        
        // 라이브러리 사용 확인
        if (/import\s+numpy|import\s+np|from\s+numpy/.test(code)) {
            analysis.librariesUsed.push("numpy");
        }
        
        if (/import\s+pandas|import\s+pd|from\s+pandas/.test(code)) {
            analysis.librariesUsed.push("pandas");
        }
        
        if (/import\s+matplotlib|import\s+plt|from\s+matplotlib/.test(code)) {
            analysis.librariesUsed.push("matplotlib");
            analysis.isVisualization = true;
        }
        
        if (/import\s+seaborn|import\s+sns|from\s+seaborn/.test(code)) {
            analysis.librariesUsed.push("seaborn");
            analysis.isVisualization = true;
        }
        
        if (/import\s+scipy|from\s+scipy/.test(code)) {
            analysis.librariesUsed.push("scipy");
        }
        
        if (/import\s+statsmodels|from\s+statsmodels/.test(code)) {
            analysis.librariesUsed.push("statsmodels");
        }
        
        // 통계 함수 사용 확인
        const statFunctions = [
            "mean", "median", "mode", "std", "var", "min", "max",
            "quantile", "percentile", "corr", "correlation",
            "ttest", "t-test", "chi2", "chi-square", "anova", "regression"
        ];
        
        for (const func of statFunctions) {
            if (new RegExp(`\\b${func}\\b`, 'i').test(code)) {
                analysis.statisticalFunctions.push(func);
                analysis.isStatisticalAnalysis = true;
            }
        }
        
        // 시각화 유형 확인
        const vizTypes = [
            "histogram", "hist", "bar", "barplot", "scatter", "scatterplot",
            "line", "lineplot", "box", "boxplot", "violin", "violinplot",
            "heatmap", "pie", "piechart"
        ];
        
        for (const viz of vizTypes) {
            if (new RegExp(`\\b${viz}\\b`, 'i').test(code)) {
                analysis.visualizationTypes.push(viz);
                analysis.isVisualization = true;
            }
        }
        
        return analysis;
    }
    
    /**
     * 추천사항 생성
     * @private
     */
    _generateRecommendations(result, code, conceptType) {
        const recommendations = [];
        
        // 코드 분석 기반 추천
        if (code) {
            const codeAnalysis = this._analyzeCode(code);
            
            // 통계 분석 코드인 경우
            if (codeAnalysis.isStatisticalAnalysis) {
                recommendations.push("데이터의 분포를 시각화하여 더 깊은 인사이트를 얻어보세요.");
                recommendations.push("이상치가 있는지 확인하고, 필요한 경우 처리 방법을 고려하세요.");
                
                if (codeAnalysis.statisticalFunctions.includes('mean')) {
                    recommendations.push("평균과 함께 중앙값도 확인하여 데이터의 치우침을 파악하세요.");
                }
                
                if (codeAnalysis.statisticalFunctions.includes('correlation')) {
                    recommendations.push("상관관계가 있다고 해서 인과관계가 있는 것은 아닙니다. 다른 요인의 영향도 고려하세요.");
                }
            }
            
            // 시각화 코드인 경우
            if (codeAnalysis.isVisualization) {
                recommendations.push("그래프에 제목, 축 레이블, 범례를 추가하여 가독성을 높이세요.");
                recommendations.push("색상과 마커를 적절히 사용하여 정보를 효과적으로 전달하세요.");
                
                if (codeAnalysis.visualizationTypes.includes('histogram')) {
                    recommendations.push("히스토그램의 구간(bin) 개수를 조정하여 데이터의 패턴을 더 잘 파악해보세요.");
                }
                
                if (codeAnalysis.visualizationTypes.includes('scatter')) {
                    recommendations.push("산점도에 추세선을 추가하여 관계의 방향과 강도를 시각화해보세요.");
                }
            }
        }
        
        // 결과 유형에 따른 추천
        if (Array.isArray(result)) {
            try {
                const isNumericArray = result.every(item => typeof item === 'number');
                if (isNumericArray) {
                    recommendations.push("데이터의 분포를 히스토그램으로 시각화하여 패턴을 파악해보세요.");
                    recommendations.push("박스플롯을 사용하여 이상치를 확인해보세요.");
                }
            } catch (e) {
                // 오류 무시
            }
        }
        
        // 기본 추천사항
        if (recommendations.length === 0) {
            recommendations.push("결과를 다양한 관점에서 해석하고, 맥락에 맞게 활용하세요.");
            recommendations.push("추가 분석을 통해 더 깊은 인사이트를 얻어보세요.");
        }
        
        return recommendations;
    }
    
    /**
     * 결과 해석 HTML 생성
     */
    generateInterpretationHTML(result, code = null, conceptType = null) {
        // 결과 해석
        const interpretation = this.interpretResult(result, code, conceptType);
        
        // HTML 생성
        let html = `
        <div class="interpretation-container" style="margin: 20px 0; border: 1px solid #ddd; border-radius: 4px; overflow: hidden;">
            <div class="interpretation-header" style="background: #f5f5f5; padding: 10px; border-bottom: 1px solid #ddd;">
                <h3 style="margin: 0; color: #333;">결과 해석</h3>
            </div>
            <div class="interpretation-body" style="padding: 15px;">
        `;
        
        // 통계적 의미
        if (interpretation.statisticalMeaning.length > 0) {
            html += `
                <div class="section">
                    <h4 style="color: #2196F3; margin-top: 0;">📊 통계적 의미</h4>
                    <ul style="padding-left: 20px; margin-bottom: 15px;">
            `;
            
            for (const meaning of interpretation.statisticalMeaning) {
                html += `<li>${meaning}</li>`;
            }
            
            html += `
                    </ul>
                </div>
            `;
        }
        
        // 실무적 해석
        if (interpretation.practicalInterpretation.length > 0) {
            html += `
                <div class="section">
                    <h4 style="color: #4CAF50; margin-top: 0;">💡 실무적 해석</h4>
                    <ul style="padding-left: 20px; margin-bottom: 15px;">
            `;
            
            for (const interp of interpretation.practicalInterpretation) {
                html += `<li>${interp}</li>`;
            }
            
            html += `
                    </ul>
                </div>
            `;
        }
        
        // 추천사항
        if (interpretation.recommendations.length > 0) {
            html += `
                <div class="section">
                    <h4 style="color: #FF9800; margin-top: 0;">🔍 추천사항</h4>
                    <ul style="padding-left: 20px; margin-bottom: 0;">
            `;
            
            for (const rec of interpretation.recommendations) {
                html += `<li>${rec}</li>`;
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

// 결과 해석기 인스턴스 생성
const resultInterpreter = new ResultInterpreter();

// 모듈 내보내기
function interpretResult(result, code = null, conceptType = null) {
    return resultInterpreter.generateInterpretationHTML(result, code, conceptType);
}