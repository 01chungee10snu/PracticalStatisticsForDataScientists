/**
 * 데이터 시각화 엔진 - JavaScript 구현
 * Chart.js 기반 인터랙티브 차트와 통계 계산
 */

class DataVisualization {
    constructor() {
        this.charts = {};
        this.colors = {
            primary: '#4c51bf',
            secondary: '#667eea',
            success: '#48bb78',
            warning: '#ed8936',
            error: '#f56565',
            info: '#38b2ac'
        };
    }

    /**
     * 기본 통계량 계산
     */
    calculateBasicStats(data) {
        if (!data || data.length === 0) return null;

        const sorted = [...data].sort((a, b) => a - b);
        const n = data.length;
        
        // 기본 통계량
        const sum = data.reduce((acc, val) => acc + val, 0);
        const mean = sum / n;
        
        // 중앙값
        const median = n % 2 === 1 ? 
            sorted[Math.floor(n / 2)] : 
            (sorted[n / 2 - 1] + sorted[n / 2]) / 2;
        
        // 분산과 표준편차
        const variance = data.reduce((acc, val) => acc + Math.pow(val - mean, 2), 0) / n;
        const stdDev = Math.sqrt(variance);
        
        // 사분위수
        const q1 = this.getPercentile(sorted, 25);
        const q3 = this.getPercentile(sorted, 75);
        const iqr = q3 - q1;
        
        return {
            count: n,
            sum: sum,
            mean: mean,
            median: median,
            mode: this.getMode(data),
            variance: variance,
            stdDev: stdDev,
            min: Math.min(...data),
            max: Math.max(...data),
            range: Math.max(...data) - Math.min(...data),
            q1: q1,
            q3: q3,
            iqr: iqr,
            skewness: this.calculateSkewness(data, mean, stdDev),
            kurtosis: this.calculateKurtosis(data, mean, stdDev)
        };
    }

    /**
     * 백분위수 계산
     */
    getPercentile(sortedData, percentile) {
        const index = (percentile / 100) * (sortedData.length - 1);
        const lower = Math.floor(index);
        const upper = Math.ceil(index);
        const weight = index % 1;
        
        if (lower === upper) {
            return sortedData[lower];
        }
        
        return sortedData[lower] * (1 - weight) + sortedData[upper] * weight;
    }

    /**
     * 최빈값 계산
     */
    getMode(data) {
        const frequency = {};
        let maxFreq = 0;
        let modes = [];
        
        data.forEach(value => {
            frequency[value] = (frequency[value] || 0) + 1;
            if (frequency[value] > maxFreq) {
                maxFreq = frequency[value];
                modes = [value];
            } else if (frequency[value] === maxFreq && !modes.includes(value)) {
                modes.push(value);
            }
        });
        
        return modes.length === data.length ? null : modes;
    }

    /**
     * 비대칭도(왜도) 계산
     */
    calculateSkewness(data, mean, stdDev) {
        if (stdDev === 0) return 0;
        
        const n = data.length;
        const skewness = data.reduce((acc, val) => {
            return acc + Math.pow((val - mean) / stdDev, 3);
        }, 0) / n;
        
        return skewness;
    }

    /**
     * 첨도 계산
     */
    calculateKurtosis(data, mean, stdDev) {
        if (stdDev === 0) return 0;
        
        const n = data.length;
        const kurtosis = data.reduce((acc, val) => {
            return acc + Math.pow((val - mean) / stdDev, 4);
        }, 0) / n;
        
        return kurtosis - 3; // 정규분포의 첨도는 3이므로 excess kurtosis
    }

    /**
     * 상관계수 계산
     */
    calculateCorrelation(x, y) {
        if (x.length !== y.length || x.length === 0) return null;
        
        const n = x.length;
        const meanX = x.reduce((a, b) => a + b) / n;
        const meanY = y.reduce((a, b) => a + b) / n;
        
        let numerator = 0;
        let sumSqX = 0;
        let sumSqY = 0;
        
        for (let i = 0; i < n; i++) {
            const devX = x[i] - meanX;
            const devY = y[i] - meanY;
            numerator += devX * devY;
            sumSqX += devX * devX;
            sumSqY += devY * devY;
        }
        
        const denominator = Math.sqrt(sumSqX * sumSqY);
        return denominator === 0 ? 0 : numerator / denominator;
    }

    /**
     * 히스토그램 생성
     */
    createHistogram(canvasId, data, options = {}) {
        const canvas = document.getElementById(canvasId);
        if (!canvas) return null;

        const stats = this.calculateBasicStats(data);
        if (!stats) return null;

        // 빈도 계산
        const bins = options.bins || Math.ceil(Math.sqrt(data.length));
        const binWidth = (stats.max - stats.min) / bins;
        const frequency = new Array(bins).fill(0);
        const labels = [];

        for (let i = 0; i < bins; i++) {
            const binStart = stats.min + i * binWidth;
            const binEnd = binStart + binWidth;
            labels.push(`${binStart.toFixed(1)}-${binEnd.toFixed(1)}`);
        }

        data.forEach(value => {
            const binIndex = Math.min(Math.floor((value - stats.min) / binWidth), bins - 1);
            frequency[binIndex]++;
        });

        // Chart.js로 히스토그램 생성
        if (this.charts[canvasId]) {
            this.charts[canvasId].destroy();
        }

        this.charts[canvasId] = new Chart(canvas, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: '빈도',
                    data: frequency,
                    backgroundColor: this.colors.primary + '80',
                    borderColor: this.colors.primary,
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: options.title || '히스토그램'
                    },
                    legend: {
                        display: false
                    }
                },
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: options.xLabel || '값'
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            text: '빈도'
                        },
                        beginAtZero: true
                    }
                }
            }
        });

        return this.charts[canvasId];
    }

    /**
     * 막대 차트 생성
     */
    createBarChart(canvasId, categories, values, options = {}) {
        const canvas = document.getElementById(canvasId);
        if (!canvas) return null;

        if (this.charts[canvasId]) {
            this.charts[canvasId].destroy();
        }

        this.charts[canvasId] = new Chart(canvas, {
            type: 'bar',
            data: {
                labels: categories,
                datasets: [{
                    label: options.label || '값',
                    data: values,
                    backgroundColor: this.colors.secondary + '80',
                    borderColor: this.colors.secondary,
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: options.title || '막대 차트'
                    },
                    legend: {
                        display: false
                    }
                },
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: options.xLabel || '카테고리'
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            text: options.yLabel || '값'
                        },
                        beginAtZero: true
                    }
                }
            }
        });

        return this.charts[canvasId];
    }

    /**
     * 산점도 생성
     */
    createScatterPlot(canvasId, xData, yData, options = {}) {
        const canvas = document.getElementById(canvasId);
        if (!canvas) return null;

        if (xData.length !== yData.length) return null;

        const scatterData = xData.map((x, i) => ({ x: x, y: yData[i] }));

        if (this.charts[canvasId]) {
            this.charts[canvasId].destroy();
        }

        this.charts[canvasId] = new Chart(canvas, {
            type: 'scatter',
            data: {
                datasets: [{
                    label: options.label || '데이터 포인트',
                    data: scatterData,
                    backgroundColor: this.colors.info + '80',
                    borderColor: this.colors.info,
                    borderWidth: 2,
                    pointRadius: 5
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: options.title || '산점도'
                    }
                },
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: options.xLabel || 'X 값'
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            text: options.yLabel || 'Y 값'
                        }
                    }
                }
            }
        });

        return this.charts[canvasId];
    }

    /**
     * 라인 차트 생성
     */
    createLineChart(canvasId, xData, yData, options = {}) {
        const canvas = document.getElementById(canvasId);
        if (!canvas) return null;

        if (this.charts[canvasId]) {
            this.charts[canvasId].destroy();
        }

        this.charts[canvasId] = new Chart(canvas, {
            type: 'line',
            data: {
                labels: xData,
                datasets: [{
                    label: options.label || '값',
                    data: yData,
                    backgroundColor: this.colors.success + '20',
                    borderColor: this.colors.success,
                    borderWidth: 2,
                    fill: options.fill || false,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: options.title || '라인 차트'
                    }
                },
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: options.xLabel || 'X 값'
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            text: options.yLabel || 'Y 값'
                        }
                    }
                }
            }
        });

        return this.charts[canvasId];
    }

    /**
     * 박스플롯 생성 (Chart.js 플러그인 필요하지만 간단한 버전으로 대체)
     */
    createBoxPlot(canvasId, data, options = {}) {
        const canvas = document.getElementById(canvasId);
        if (!canvas) return null;

        const stats = this.calculateBasicStats(data);
        if (!stats) return null;

        // 박스플롯 데이터 준비
        const boxData = [
            { label: 'Min', value: stats.min },
            { label: 'Q1', value: stats.q1 },
            { label: 'Median', value: stats.median },
            { label: 'Q3', value: stats.q3 },
            { label: 'Max', value: stats.max }
        ];

        if (this.charts[canvasId]) {
            this.charts[canvasId].destroy();
        }

        this.charts[canvasId] = new Chart(canvas, {
            type: 'bar',
            data: {
                labels: boxData.map(d => d.label),
                datasets: [{
                    label: '값',
                    data: boxData.map(d => d.value),
                    backgroundColor: [
                        this.colors.primary + '40',
                        this.colors.secondary + '60',
                        this.colors.warning + '80',
                        this.colors.secondary + '60',
                        this.colors.primary + '40'
                    ],
                    borderColor: this.colors.primary,
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: options.title || 'Box Plot (5-Number Summary)'
                    }
                },
                scales: {
                    y: {
                        title: {
                            display: true,
                            text: options.yLabel || '값'
                        }
                    }
                }
            }
        });

        return this.charts[canvasId];
    }

    /**
     * 확률분포 시뮬레이션
     */
    simulateNormalDistribution(mean = 0, stdDev = 1, size = 1000) {
        const data = [];
        for (let i = 0; i < size; i++) {
            // Box-Muller 변환을 사용한 정규분포 생성
            const u1 = Math.random();
            const u2 = Math.random();
            const z0 = Math.sqrt(-2 * Math.log(u1)) * Math.cos(2 * Math.PI * u2);
            data.push(z0 * stdDev + mean);
        }
        return data;
    }

    /**
     * 균등분포 시뮬레이션
     */
    simulateUniformDistribution(min = 0, max = 1, size = 1000) {
        const data = [];
        for (let i = 0; i < size; i++) {
            data.push(Math.random() * (max - min) + min);
        }
        return data;
    }

    /**
     * 치우친 분포 시뮬레이션 (지수분포)
     */
    simulateSkewedDistribution(lambda = 1, size = 1000) {
        const data = [];
        for (let i = 0; i < size; i++) {
            const u = Math.random();
            const x = -Math.log(1 - u) / lambda;
            data.push(x);
        }
        return data;
    }

    /**
     * 통계 텍스트 생성
     */
    generateStatsText(data, containerId) {
        const container = document.getElementById(containerId);
        if (!container) return;

        const stats = this.calculateBasicStats(data);
        if (!stats) {
            container.innerHTML = '<p>유효한 데이터가 없습니다.</p>';
            return;
        }

        const html = `
            <div class="stats-summary">
                <h4>📊 기술통계 요약</h4>
                <div class="stats-grid">
                    <div class="stat-item">
                        <span class="stat-label">개수:</span>
                        <span class="stat-value">${stats.count}</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-label">평균:</span>
                        <span class="stat-value">${stats.mean.toFixed(2)}</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-label">중앙값:</span>
                        <span class="stat-value">${stats.median.toFixed(2)}</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-label">표준편차:</span>
                        <span class="stat-value">${stats.stdDev.toFixed(2)}</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-label">최솟값:</span>
                        <span class="stat-value">${stats.min.toFixed(2)}</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-label">최댓값:</span>
                        <span class="stat-value">${stats.max.toFixed(2)}</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-label">1사분위수:</span>
                        <span class="stat-value">${stats.q1.toFixed(2)}</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-label">3사분위수:</span>
                        <span class="stat-value">${stats.q3.toFixed(2)}</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-label">비대칭도:</span>
                        <span class="stat-value">${stats.skewness.toFixed(3)}</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-label">첨도:</span>
                        <span class="stat-value">${stats.kurtosis.toFixed(3)}</span>
                    </div>
                </div>
                
                <div class="distribution-analysis">
                    <h5>📈 분포 특성</h5>
                    <ul>
                        <li><strong>중심경향성:</strong> 평균 ${stats.mean.toFixed(2)}, 중앙값 ${stats.median.toFixed(2)}</li>
                        <li><strong>산포도:</strong> 표준편차 ${stats.stdDev.toFixed(2)}, 범위 ${stats.range.toFixed(2)}</li>
                        <li><strong>분포 형태:</strong> ${this.interpretSkewness(stats.skewness)}</li>
                        <li><strong>첨도:</strong> ${this.interpretKurtosis(stats.kurtosis)}</li>
                    </ul>
                </div>
            </div>
        `;

        container.innerHTML = html;
    }

    /**
     * 비대칭도 해석
     */
    interpretSkewness(skewness) {
        if (Math.abs(skewness) < 0.5) {
            return "대칭에 가까운 분포";
        } else if (skewness > 0.5) {
            return "오른쪽으로 치우친 분포 (양의 비대칭)";
        } else {
            return "왼쪽으로 치우친 분포 (음의 비대칭)";
        }
    }

    /**
     * 첨도 해석
     */
    interpretKurtosis(kurtosis) {
        if (Math.abs(kurtosis) < 0.5) {
            return "정규분포와 유사한 첨도";
        } else if (kurtosis > 0.5) {
            return "뾰족한 분포 (정규분포보다 첨도가 높음)";
        } else {
            return "납작한 분포 (정규분포보다 첨도가 낮음)";
        }
    }

    /**
     * 상관분석 결과 텍스트 생성
     */
    generateCorrelationText(correlation, containerId) {
        const container = document.getElementById(containerId);
        if (!container) return;

        if (correlation === null) {
            container.innerHTML = '<p>상관계수를 계산할 수 없습니다.</p>';
            return;
        }

        let strength, direction, interpretation;

        // 방향
        direction = correlation >= 0 ? "양의" : "음의";

        // 강도
        const absCorr = Math.abs(correlation);
        if (absCorr >= 0.8) {
            strength = "매우 강한";
        } else if (absCorr >= 0.6) {
            strength = "강한";
        } else if (absCorr >= 0.4) {
            strength = "중간";
        } else if (absCorr >= 0.2) {
            strength = "약한";
        } else {
            strength = "매우 약한";
        }

        // 해석
        if (absCorr >= 0.7) {
            interpretation = "두 변수는 강한 선형 관계를 보입니다.";
        } else if (absCorr >= 0.3) {
            interpretation = "두 변수 간에 어느 정도의 선형 관계가 있습니다.";
        } else {
            interpretation = "두 변수 간의 선형 관계는 미약합니다.";
        }

        const html = `
            <div class="correlation-result">
                <h4>🔗 상관분석 결과</h4>
                <div class="correlation-value">
                    <span class="correlation-number">${correlation.toFixed(4)}</span>
                </div>
                <div class="correlation-interpretation">
                    <p><strong>관계의 성격:</strong> ${strength} ${direction} 상관관계</p>
                    <p><strong>해석:</strong> ${interpretation}</p>
                    <p><strong>설명력:</strong> 결정계수(R²) = ${(correlation * correlation).toFixed(4)} 
                       (약 ${(correlation * correlation * 100).toFixed(1)}%의 분산 설명)</p>
                </div>
                
                <div class="correlation-guide">
                    <h5>📚 상관계수 해석 가이드</h5>
                    <ul>
                        <li><strong>±0.8 이상:</strong> 매우 강한 상관관계</li>
                        <li><strong>±0.6~0.8:</strong> 강한 상관관계</li>
                        <li><strong>±0.4~0.6:</strong> 중간 정도의 상관관계</li>
                        <li><strong>±0.2~0.4:</strong> 약한 상관관계</li>
                        <li><strong>±0.2 미만:</strong> 매우 약한 상관관계</li>
                    </ul>
                    <p><em>※ 상관관계가 있다고 해서 반드시 인과관계가 있는 것은 아닙니다.</em></p>
                </div>
            </div>
        `;

        container.innerHTML = html;
    }

    /**
     * 모든 차트 정리
     */
    destroyAllCharts() {
        Object.values(this.charts).forEach(chart => {
            chart.destroy();
        });
        this.charts = {};
    }
}

// 전역 시각화 인스턴스
window.visualization = new DataVisualization();