/**
 * 메인 애플리케이션 로직
 * UI 상호작용 및 전체 시스템 조율
 */

// 전역 변수
let currentSection = 'home';
let currentDemoTab = 'stats';
let currentContentLevel = 'foundation';

// DOM 로드 완료 시 초기화
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

/**
 * 애플리케이션 초기화
 */
function initializeApp() {
    // 네비게이션 이벤트 리스너 설정
    setupNavigation();
    
    // 기본 데모 차트 생성
    setupDemoCharts();
    
    // 사용자 데이터 복원
    if (learningSystem.currentUser) {
        showUserInfo(learningSystem.currentUser);
    }
    
    // 시뮬레이션 초기화
    updateSimulation();
    
    console.log('✅ 적응형 학습 시스템이 초기화되었습니다!');
}

/**
 * 네비게이션 설정
 */
function setupNavigation() {
    // 네비게이션 링크 클릭 이벤트
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const section = link.getAttribute('href').substring(1);
            showSection(section);
        });
    });
}

/**
 * 섹션 표시
 */
function showSection(sectionName) {
    // 모든 섹션 숨기기
    document.querySelectorAll('.section').forEach(section => {
        section.style.display = 'none';
    });
    
    // 선택된 섹션 표시
    const targetSection = document.getElementById(sectionName);
    if (targetSection) {
        targetSection.style.display = 'block';
        currentSection = sectionName;
        
        // 네비게이션 활성화 상태 업데이트
        document.querySelectorAll('.nav-link').forEach(link => {
            link.classList.remove('active');
        });
        document.querySelector(`[href="#${sectionName}"]`).classList.add('active');
        
        // 섹션별 초기화 로직
        if (sectionName === 'learn') {
            initializeLearningSection();
        } else if (sectionName === 'demo') {
            refreshDemoContent();
        }
    }
}

/**
 * 학습자 등록
 */
function registerLearner() {
    const nameInput = document.getElementById('learner-name');
    const name = nameInput.value.trim();
    
    if (!name) {
        alert('이름을 입력해주세요!');
        return;
    }
    
    const result = learningSystem.registerLearner(name, {
        name: name,
        difficulty: 5,
        pace: 'medium'
    });
    
    if (result.status === 'success') {
        showUserInfo(name);
        nameInput.value = '';
        
        // 성공 애니메이션
        showNotification('환영합니다! 개인 맞춤형 학습을 시작해보세요! 🎉', 'success');
    } else {
        alert('등록에 실패했습니다. 다시 시도해주세요.');
    }
}

/**
 * 사용자 정보 표시
 */
function showUserInfo(userId) {
    const loginForm = document.getElementById('login-form');
    const userInfo = document.getElementById('user-info');
    const learningArea = document.getElementById('learning-area');
    
    if (loginForm && userInfo && learningArea) {
        loginForm.style.display = 'none';
        userInfo.style.display = 'block';
        learningArea.style.display = 'block';
        
        // 사용자 이름 표시
        document.getElementById('username').textContent = userId;
        
        // 학습 통계 업데이트
        updateUserStats(userId);
        
        // 추천 콘텐츠 로드
        loadRecommendedContent(userId);
        
        // 콘텐츠 라이브러리 표시
        showContentLevel(currentContentLevel);
    }
}

/**
 * 사용자 통계 업데이트
 */
function updateUserStats(userId) {
    const analytics = learningSystem.getLearningAnalytics(userId);
    
    if (analytics && !analytics.error) {
        const userLevel = document.getElementById('user-level');
        const successRate = document.getElementById('user-success-rate');
        const completedContent = document.getElementById('completed-content');
        
        if (userLevel) userLevel.textContent = analytics.overallStats.currentLevel;
        if (successRate) successRate.textContent = `${analytics.overallStats.successRate}%`;
        if (completedContent) {
            // 완료한 콘텐츠 수 계산
            const learner = learningSystem.learners[userId];
            const completedCount = Object.keys(learner.performance).length;
            completedContent.textContent = completedCount;
        }
    }
}

/**
 * 추천 콘텐츠 로드
 */
function loadRecommendedContent(userId) {
    const content = learningSystem.getPersonalizedContent(userId);
    const container = document.getElementById('recommended-content');
    
    if (!container) return;
    
    if (content.error) {
        container.innerHTML = `<p class="error">❌ ${content.error}</p>`;
        return;
    }
    
    if (content.message) {
        container.innerHTML = `<p class="info">📝 ${content.message}</p>`;
        return;
    }
    
    // 추천 콘텐츠 카드 생성
    const html = `
        <div class="recommended-content-card">
            <h4 class="content-title">${content.content.title}</h4>
            <p class="content-description">${content.content.content}</p>
            
            <div class="content-details">
                <div class="detail-item">
                    <span class="detail-label">⏱️ 예상 시간:</span>
                    <span class="detail-value">${content.estimatedTime}</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label">💡 추천 이유:</span>
                    <span class="detail-value">${content.recommendationReason}</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label">📊 현재 레벨:</span>
                    <span class="detail-value">${content.userLevel}</span>
                </div>
            </div>
            
            ${content.content.learningObjectives ? `
                <div class="learning-objectives">
                    <h5>🎯 학습 목표</h5>
                    <ul>
                        ${content.content.learningObjectives.map(obj => `<li>${obj}</li>`).join('')}
                    </ul>
                </div>
            ` : ''}
            
            <div class="content-actions">
                <button class="btn btn-primary" onclick="startContent('${content.contentId}', '${userId}')">
                    🚀 학습 시작하기
                </button>
                <button class="btn btn-secondary" onclick="showContentDetails('${content.contentId}')">
                    📖 상세 보기
                </button>
            </div>
        </div>
    `;
    
    container.innerHTML = html;
}

/**
 * 콘텐츠 시작
 */
function startContent(contentId, userId) {
    const content = learningSystem.getPersonalizedContent(userId);
    if (!content.content) return;
    
    // 학습 모달 또는 새 페이지로 이동
    showContentModal(content, userId);
}

/**
 * 콘텐츠 모달 표시
 */
function showContentModal(content, userId) {
    // 모달 HTML 생성
    const modalHtml = `
        <div class="modal-overlay" id="content-modal" onclick="closeModal()">
            <div class="modal-content" onclick="event.stopPropagation()">
                <div class="modal-header">
                    <h3>${content.content.title}</h3>
                    <button class="modal-close" onclick="closeModal()">×</button>
                </div>
                
                <div class="modal-body">
                    <div class="content-explanation">
                        <p>${content.content.content}</p>
                        
                        ${content.content.detailedExplanation ? `
                            <div class="detailed-explanation">
                                <h4>📖 핵심 개념</h4>
                                ${Object.entries(content.content.detailedExplanation).map(([key, value]) => `
                                    <div class="concept-item">
                                        <strong>${key}:</strong> ${value}
                                    </div>
                                `).join('')}
                            </div>
                        ` : ''}
                        
                        ${content.content.realWorldExamples ? `
                            <div class="real-world-examples">
                                <h4>🌍 실생활 예시</h4>
                                <ul>
                                    ${content.content.realWorldExamples.map(example => `<li>${example}</li>`).join('')}
                                </ul>
                            </div>
                        ` : ''}
                    </div>
                    
                    <div class="questions-section">
                        <h4>🧠 연습 문제</h4>
                        <div id="questions-container">
                            ${content.content.questions.map((question, index) => `
                                <div class="question-card" id="question-${index}">
                                    <div class="question-header">
                                        <h5>문제 ${index + 1}</h5>
                                        <span class="difficulty-badge">난이도: ${'★'.repeat(question.difficulty || 3)}</span>
                                    </div>
                                    <div class="question-text">${question.q}</div>
                                    <div class="question-options">
                                        ${question.options.map((option, optIndex) => `
                                            <label class="option-label">
                                                <input type="radio" name="question-${index}" value="${optIndex}">
                                                <span class="option-text">${option}</span>
                                            </label>
                                        `).join('')}
                                    </div>
                                    <button class="btn btn-primary" onclick="submitQuestionAnswer(${index}, '${content.contentId}', '${userId}')">
                                        답안 제출
                                    </button>
                                    <div class="answer-result" id="result-${index}"></div>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // 모달을 body에 추가
    document.body.insertAdjacentHTML('beforeend', modalHtml);
}

/**
 * 문제 답안 제출
 */
function submitQuestionAnswer(questionIndex, contentId, userId) {
    const selectedOption = document.querySelector(`input[name="question-${questionIndex}"]:checked`);
    
    if (!selectedOption) {
        alert('답을 선택해주세요!');
        return;
    }
    
    const answer = parseInt(selectedOption.value);
    const result = learningSystem.submitAnswer(userId, contentId, questionIndex, answer);
    
    // 결과 표시
    const resultContainer = document.getElementById(`result-${questionIndex}`);
    if (resultContainer) {
        const html = `
            <div class="answer-feedback ${result.correct ? 'correct' : 'incorrect'}">
                <div class="feedback-header">
                    ${result.correct ? '✅ 정답입니다!' : '❌ 틀렸습니다.'}
                </div>
                <div class="feedback-content">
                    <p><strong>선택한 답:</strong> ${result.yourAnswer}</p>
                    <p><strong>정답:</strong> ${result.correctAnswer}</p>
                    <p><strong>해설:</strong> ${result.explanation}</p>
                    <p><strong>성과:</strong> ${result.performanceSummary.successRate}% 성공률 (${result.performanceSummary.attempts}회 시도)</p>
                    ${result.levelUp ? `<p class="level-up">🎉 축하합니다! ${result.newLevel} 레벨로 승급했습니다!</p>` : ''}
                </div>
            </div>
        `;
        resultContainer.innerHTML = html;
        
        // 사용자 통계 업데이트
        updateUserStats(userId);
    }
    
    // 성공/실패에 따른 알림
    if (result.correct) {
        showNotification('정답입니다! 🎉', 'success');
    } else {
        showNotification('다시 한번 생각해보세요! 💪', 'info');
    }
}

/**
 * 모달 닫기
 */
function closeModal() {
    const modal = document.getElementById('content-modal');
    if (modal) {
        modal.remove();
    }
}

/**
 * 콘텐츠 레벨 표시
 */
function showContentLevel(level) {
    currentContentLevel = level;
    
    // 탭 활성화 상태 업데이트
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    document.querySelector(`[onclick="showContentLevel('${level}')"]`).classList.add('active');
    
    // 콘텐츠 목록 생성
    const contentList = learningSystem.contentLibrary[level] || {};
    const container = document.getElementById('content-list');
    
    if (!container) return;
    
    const html = Object.entries(contentList).map(([contentId, content]) => `
        <div class="content-item" onclick="showContentDetails('${contentId}')">
            <div class="content-title">${content.title}</div>
            <div class="content-description">${content.content}</div>
            <div class="content-meta">
                <div class="difficulty-indicator">
                    ${Array.from({length: 10}, (_, i) => 
                        `<div class="difficulty-dot ${i < content.difficulty ? 'active' : ''}"></div>`
                    ).join('')}
                </div>
                <div class="content-category">${content.category}</div>
            </div>
            ${content.prerequisites && content.prerequisites.length > 0 ? 
                `<div class="prerequisites">전제조건: ${content.prerequisites.join(', ')}</div>` : ''
            }
        </div>
    `).join('');
    
    container.innerHTML = html || '<p>이 레벨에는 아직 콘텐츠가 없습니다.</p>';
}

/**
 * 학습 섹션 초기화
 */
function initializeLearningSection() {
    if (learningSystem.currentUser) {
        updateUserStats(learningSystem.currentUser);
        loadRecommendedContent(learningSystem.currentUser);
    }
    showContentLevel(currentContentLevel);
}

/**
 * 데모 탭 표시
 */
function showDemo(demoType) {
    currentDemoTab = demoType;
    
    // 탭 활성화 상태 업데이트
    document.querySelectorAll('.demo-tab').forEach(tab => {
        tab.classList.remove('active');
    });
    document.querySelector(`[onclick="showDemo('${demoType}')"]`).classList.add('active');
    
    // 패널 표시
    document.querySelectorAll('.demo-panel').forEach(panel => {
        panel.classList.remove('active');
    });
    document.getElementById(`demo-${demoType}`).classList.add('active');
    
    // 데모 타입별 초기화
    if (demoType === 'charts') {
        setupDemoCharts();
    } else if (demoType === 'interactive') {
        updateSimulation();
    }
}

/**
 * 데모 차트 설정
 */
function setupDemoCharts() {
    // 막대 차트 예시
    const barData = [85, 92, 78, 88, 95];
    const barLabels = ['A팀', 'B팀', 'C팀', 'D팀', 'E팀'];
    
    setTimeout(() => {
        const barCanvas = document.createElement('canvas');
        barCanvas.id = 'demo-bar-chart';
        const barContainer = document.getElementById('bar-chart-demo');
        if (barContainer) {
            barContainer.innerHTML = '<h4>📊 팀별 성과</h4>';
            barContainer.appendChild(barCanvas);
            visualization.createBarChart('demo-bar-chart', barLabels, barData, {
                title: '팀별 성과 비교',
                yLabel: '점수'
            });
        }
    }, 100);
    
    // 라인 차트 예시
    setTimeout(() => {
        const lineData = [65, 72, 78, 85, 88, 92, 89];
        const lineLabels = ['1월', '2월', '3월', '4월', '5월', '6월', '7월'];
        
        const lineCanvas = document.createElement('canvas');
        lineCanvas.id = 'demo-line-chart';
        const lineContainer = document.getElementById('line-chart-demo');
        if (lineContainer) {
            lineContainer.innerHTML = '<h4>📈 월별 진도</h4>';
            lineContainer.appendChild(lineCanvas);
            visualization.createLineChart('demo-line-chart', lineLabels, lineData, {
                title: '월별 학습 진도',
                yLabel: '완료율 (%)'
            });
        }
    }, 200);
    
    // 산점도 예시
    setTimeout(() => {
        const xData = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
        const yData = [2.1, 3.9, 6.2, 7.8, 10.1, 12.2, 13.8, 16.1, 18.0, 19.9];
        
        const scatterCanvas = document.createElement('canvas');
        scatterCanvas.id = 'demo-scatter-plot';
        const scatterContainer = document.getElementById('scatter-plot-demo');
        if (scatterContainer) {
            scatterContainer.innerHTML = '<h4>📊 상관관계</h4>';
            scatterContainer.appendChild(scatterCanvas);
            visualization.createScatterPlot('demo-scatter-plot', xData, yData, {
                title: '학습시간 vs 성과',
                xLabel: '학습시간 (시간)',
                yLabel: '성과 점수'
            });
        }
    }, 300);
}

/**
 * 샘플 데이터 생성
 */
function generateSampleData(type) {
    let data;
    let title;
    
    switch (type) {
        case 'normal':
            data = visualization.simulateNormalDistribution(50, 10, 100);
            title = '정규분포 (평균=50, 표준편차=10)';
            break;
        case 'skewed':
            data = visualization.simulateSkewedDistribution(0.1, 100);
            title = '치우친분포 (지수분포)';
            break;
        case 'uniform':
            data = visualization.simulateUniformDistribution(0, 100, 100);
            title = '균등분포 (0~100)';
            break;
        default:
            return;
    }
    
    // 통계 표시
    visualization.generateStatsText(data, 'stats-visualization');
    
    // 히스토그램 생성
    const canvas = document.createElement('canvas');
    canvas.id = 'stats-histogram';
    canvas.width = 600;
    canvas.height = 400;
    
    const container = document.getElementById('stats-visualization');
    const existingCanvas = container.querySelector('canvas');
    if (existingCanvas) {
        existingCanvas.remove();
    }
    container.appendChild(canvas);
    
    visualization.createHistogram('stats-histogram', data, {
        title: title,
        bins: 15
    });
}

/**
 * 상관분석 실행
 */
function calculateCorrelation() {
    const xInput = document.getElementById('var-x').value.trim();
    const yInput = document.getElementById('var-y').value.trim();
    
    if (!xInput || !yInput) {
        alert('두 변수의 데이터를 모두 입력해주세요!');
        return;
    }
    
    try {
        const xData = xInput.split(',').map(x => parseFloat(x.trim())).filter(x => !isNaN(x));
        const yData = yInput.split(',').map(y => parseFloat(y.trim())).filter(y => !isNaN(y));
        
        if (xData.length !== yData.length || xData.length < 2) {
            alert('두 변수의 데이터 개수가 같아야 하며, 최소 2개 이상이어야 합니다!');
            return;
        }
        
        const correlation = visualization.calculateCorrelation(xData, yData);
        
        // 결과 표시
        visualization.generateCorrelationText(correlation, 'correlation-result');
        
        // 산점도 생성
        const canvas = document.createElement('canvas');
        canvas.id = 'correlation-scatter';
        
        const resultContainer = document.getElementById('correlation-result');
        const existingCanvas = resultContainer.querySelector('canvas');
        if (existingCanvas) {
            existingCanvas.remove();
        }
        resultContainer.appendChild(canvas);
        
        visualization.createScatterPlot('correlation-scatter', xData, yData, {
            title: `상관분석 결과 (r = ${correlation.toFixed(4)})`,
            xLabel: 'X 변수',
            yLabel: 'Y 변수'
        });
        
    } catch (error) {
        alert('데이터 형식이 올바르지 않습니다. 쉼표로 구분된 숫자를 입력해주세요.');
    }
}

/**
 * 시뮬레이션 업데이트
 */
function updateSimulation() {
    const sampleSize = parseInt(document.getElementById('sample-size').value);
    const mean = parseInt(document.getElementById('mean-value').value);
    const stdDev = parseInt(document.getElementById('std-value').value);
    
    // 값 표시 업데이트
    document.getElementById('sample-size-value').textContent = sampleSize;
    document.getElementById('mean-value-display').textContent = mean;
    document.getElementById('std-value-display').textContent = stdDev;
    
    // 데이터 생성
    const data = visualization.simulateNormalDistribution(mean, stdDev, sampleSize);
    
    // 통계 및 히스토그램 표시
    const container = document.getElementById('simulation-result');
    
    // 통계 텍스트 생성
    const stats = visualization.calculateBasicStats(data);
    const statsHtml = `
        <div class="simulation-stats">
            <h4>📊 시뮬레이션 결과</h4>
            <div class="stats-grid">
                <div class="stat-item">
                    <span class="stat-label">표본 크기:</span>
                    <span class="stat-value">${stats.count}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">표본 평균:</span>
                    <span class="stat-value">${stats.mean.toFixed(2)}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">표본 표준편차:</span>
                    <span class="stat-value">${stats.stdDev.toFixed(2)}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">이론적 평균:</span>
                    <span class="stat-value">${mean}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">이론적 표준편차:</span>
                    <span class="stat-value">${stdDev}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">평균 오차:</span>
                    <span class="stat-value">${Math.abs(stats.mean - mean).toFixed(2)}</span>
                </div>
            </div>
        </div>
        <canvas id="simulation-histogram"></canvas>
    `;
    
    container.innerHTML = statsHtml;
    
    // 히스토그램 생성
    setTimeout(() => {
        visualization.createHistogram('simulation-histogram', data, {
            title: `정규분포 시뮬레이션 (μ=${mean}, σ=${stdDev})`,
            bins: Math.min(20, Math.ceil(Math.sqrt(sampleSize)))
        });
    }, 100);
}

/**
 * 데모 콘텐츠 새로고침
 */
function refreshDemoContent() {
    if (currentDemoTab === 'charts') {
        setupDemoCharts();
    } else if (currentDemoTab === 'interactive') {
        updateSimulation();
    }
}

/**
 * 알림 표시
 */
function showNotification(message, type = 'info') {
    // 기존 알림 제거
    const existingNotification = document.querySelector('.notification');
    if (existingNotification) {
        existingNotification.remove();
    }
    
    // 새 알림 생성
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <span class="notification-message">${message}</span>
            <button class="notification-close" onclick="this.parentElement.parentElement.remove()">×</button>
        </div>
    `;
    
    // 스타일 적용
    notification.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        z-index: 10000;
        max-width: 400px;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.15);
        animation: slideInRight 0.3s ease-out;
        ${type === 'success' ? 'background: #d4edda; border-left: 4px solid #28a745; color: #155724;' : ''}
        ${type === 'error' ? 'background: #f8d7da; border-left: 4px solid #dc3545; color: #721c24;' : ''}
        ${type === 'info' ? 'background: #d1ecf1; border-left: 4px solid #17a2b8; color: #0c5460;' : ''}
        ${type === 'warning' ? 'background: #fff3cd; border-left: 4px solid #ffc107; color: #856404;' : ''}
    `;
    
    document.body.appendChild(notification);
    
    // 3초 후 자동 제거
    setTimeout(() => {
        if (notification.parentElement) {
            notification.style.animation = 'slideOutRight 0.3s ease-in';
            setTimeout(() => notification.remove(), 300);
        }
    }, 3000);
}

/**
 * 콘텐츠 상세 정보 표시
 */
function showContentDetails(contentId) {
    // 콘텐츠 찾기
    let content = null;
    for (const levelContent of Object.values(learningSystem.contentLibrary)) {
        if (levelContent[contentId]) {
            content = levelContent[contentId];
            break;
        }
    }
    
    if (!content) {
        alert('콘텐츠를 찾을 수 없습니다.');
        return;
    }
    
    // 상세 정보 모달 표시
    const modalHtml = `
        <div class="modal-overlay" onclick="closeModal()">
            <div class="modal-content content-details-modal" onclick="event.stopPropagation()">
                <div class="modal-header">
                    <h3>${content.title}</h3>
                    <button class="modal-close" onclick="closeModal()">×</button>
                </div>
                
                <div class="modal-body">
                    <div class="content-overview">
                        <p class="content-description">${content.content}</p>
                        
                        <div class="content-metadata">
                            <div class="meta-item">
                                <span class="meta-label">난이도:</span>
                                <span class="meta-value">${'★'.repeat(content.difficulty)} (${content.difficulty}/10)</span>
                            </div>
                            <div class="meta-item">
                                <span class="meta-label">카테고리:</span>
                                <span class="meta-value">${content.category}</span>
                            </div>
                            ${content.prerequisites && content.prerequisites.length > 0 ? `
                                <div class="meta-item">
                                    <span class="meta-label">전제조건:</span>
                                    <span class="meta-value">${content.prerequisites.join(', ')}</span>
                                </div>
                            ` : ''}
                        </div>
                    </div>
                    
                    ${content.learningObjectives ? `
                        <div class="learning-objectives">
                            <h4>🎯 학습 목표</h4>
                            <ul>
                                ${content.learningObjectives.map(obj => `<li>${obj}</li>`).join('')}
                            </ul>
                        </div>
                    ` : ''}
                    
                    ${content.detailedExplanation ? `
                        <div class="detailed-explanation">
                            <h4>📖 핵심 개념</h4>
                            ${Object.entries(content.detailedExplanation).map(([key, value]) => `
                                <div class="concept-item">
                                    <strong>${key}:</strong> ${value}
                                </div>
                            `).join('')}
                        </div>
                    ` : ''}
                    
                    ${content.realWorldExamples ? `
                        <div class="real-world-examples">
                            <h4>🌍 실생활 예시</h4>
                            <ul>
                                ${content.realWorldExamples.map(example => `<li>${example}</li>`).join('')}
                            </ul>
                        </div>
                    ` : ''}
                    
                    <div class="questions-preview">
                        <h4>📝 연습 문제 미리보기</h4>
                        <p>총 ${content.questions.length}개의 문제가 준비되어 있습니다.</p>
                        <div class="question-concepts">
                            ${[...new Set(content.questions.map(q => q.concept))].map(concept => 
                                `<span class="concept-tag">${concept}</span>`
                            ).join('')}
                        </div>
                    </div>
                    
                    ${learningSystem.currentUser ? `
                        <div class="action-buttons">
                            <button class="btn btn-primary" onclick="closeModal(); startContent('${contentId}', '${learningSystem.currentUser}')">
                                🚀 학습 시작하기
                            </button>
                        </div>
                    ` : `
                        <div class="login-prompt">
                            <p>학습을 시작하려면 먼저 이름을 등록해주세요!</p>
                            <button class="btn btn-primary" onclick="closeModal(); showSection('learn')">
                                👤 학습자 등록하기
                            </button>
                        </div>
                    `}
                </div>
            </div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', modalHtml);
}

// CSS 애니메이션 추가
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideOutRight {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
    
    .modal-overlay {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.7);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 10000;
        animation: fadeIn 0.3s ease-out;
    }
    
    .modal-content {
        background: white;
        border-radius: 15px;
        max-width: 800px;
        max-height: 90vh;
        overflow-y: auto;
        margin: 20px;
        animation: slideInUp 0.3s ease-out;
    }
    
    .modal-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 2rem 2rem 1rem;
        border-bottom: 1px solid #eee;
    }
    
    .modal-close {
        background: none;
        border: none;
        font-size: 2rem;
        cursor: pointer;
        color: #666;
        padding: 0;
        width: 40px;
        height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 50%;
        transition: background 0.3s;
    }
    
    .modal-close:hover {
        background: #f0f0f0;
    }
    
    .modal-body {
        padding: 2rem;
    }
    
    .question-card {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        border-left: 4px solid #4c51bf;
    }
    
    .question-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
    }
    
    .difficulty-badge {
        background: #4c51bf;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-size: 0.8rem;
    }
    
    .question-options {
        margin: 1rem 0;
    }
    
    .option-label {
        display: block;
        margin: 0.5rem 0;
        padding: 0.8rem;
        background: white;
        border-radius: 8px;
        cursor: pointer;
        transition: background 0.3s;
    }
    
    .option-label:hover {
        background: #e6e8ff;
    }
    
    .answer-feedback {
        margin-top: 1rem;
        padding: 1rem;
        border-radius: 8px;
    }
    
    .answer-feedback.correct {
        background: #d4edda;
        border-left: 4px solid #28a745;
        color: #155724;
    }
    
    .answer-feedback.incorrect {
        background: #f8d7da;
        border-left: 4px solid #dc3545;
        color: #721c24;
    }
    
    .level-up {
        color: #e83e8c;
        font-weight: bold;
        font-size: 1.1rem;
    }
    
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 1rem 0;
    }
    
    .stat-item {
        display: flex;
        justify-content: space-between;
        padding: 0.5rem;
        background: #f8f9fa;
        border-radius: 5px;
    }
    
    .concept-tag {
        background: #4c51bf;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-size: 0.8rem;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
        display: inline-block;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes slideInUp {
        from { transform: translateY(50px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
`;
document.head.appendChild(style);