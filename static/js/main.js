/**
 * Main Application JavaScript
 * Modern Statistics Learning Platform
 */

// Application State
const AppState = {
    currentUser: null,
    currentSection: 'dashboard',
    theme: localStorage.getItem('theme') || 'light',
    learningProgress: {},
    notifications: []
};

// Configuration
const CONFIG = {
    API_BASE_URL: '/api/v1',
    REFRESH_INTERVAL: 30000, // 30 seconds
    CHART_COLORS: {
        primary: 'hsl(250, 70%, 55%)',
        success: 'hsl(142, 76%, 36%)',
        warning: 'hsl(38, 92%, 50%)',
        error: 'hsl(0, 84%, 60%)',
        info: 'hsl(217, 91%, 60%)'
    }
};

// Utility Functions
const Utils = {
    // Debounce function for performance
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },

    // Format numbers with Korean locale
    formatNumber(num) {
        return new Intl.NumberFormat('ko-KR').format(num);
    },

    // Format dates with Korean locale
    formatDate(date) {
        return new Intl.DateTimeFormat('ko-KR', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        }).format(new Date(date));
    },

    // Generate unique IDs
    generateId() {
        return Math.random().toString(36).substr(2, 9);
    },

    // Smooth scroll to element
    scrollTo(element) {
        element.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }
};

// Theme Management
const ThemeManager = {
    init() {
        this.setTheme(AppState.theme);
        this.bindEvents();
    },

    setTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        AppState.theme = theme;
        localStorage.setItem('theme', theme);
    },

    toggle() {
        const newTheme = AppState.theme === 'light' ? 'dark' : 'light';
        this.setTheme(newTheme);
        this.announceThemeChange(newTheme);
    },

    announceThemeChange(theme) {
        const message = theme === 'dark' ? '다크 모드가 활성화되었습니다' : '라이트 모드가 활성화되었습니다';
        ToastManager.show(message, 'info');
    },

    bindEvents() {
        const themeToggle = document.getElementById('theme-toggle');
        if (themeToggle) {
            themeToggle.addEventListener('click', () => this.toggle());
        }
    }
};

// Navigation Management
const NavigationManager = {
    init() {
        this.bindEvents();
        this.setActiveSection(AppState.currentSection);
    },

    bindEvents() {
        // Navigation links
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const section = link.dataset.section;
                if (section) {
                    this.navigateToSection(section);
                }
            });
        });

        // User menu
        const userMenuButton = document.getElementById('user-menu-button');
        const userMenu = document.getElementById('user-menu');
        
        if (userMenuButton && userMenu) {
            userMenuButton.addEventListener('click', () => {
                this.toggleUserMenu();
            });

            // Close menu when clicking outside
            document.addEventListener('click', (e) => {
                if (!userMenuButton.contains(e.target) && !userMenu.contains(e.target)) {
                    this.closeUserMenu();
                }
            });
        }
    },

    navigateToSection(section) {
        // Update state
        AppState.currentSection = section;
        
        // Update URL without reload
        history.pushState({ section }, '', `#${section}`);
        
        // Update UI
        this.setActiveSection(section);
        
        // Load section content
        this.loadSectionContent(section);
    },

    setActiveSection(section) {
        // Update navigation
        document.querySelectorAll('.nav-link').forEach(link => {
            link.classList.toggle('active', link.dataset.section === section);
        });

        // Update content sections
        document.querySelectorAll('.content-section').forEach(contentSection => {
            contentSection.classList.toggle('active', contentSection.id === section);
        });
    },

    async loadSectionContent(section) {
        try {
            switch (section) {
                case 'dashboard':
                    await DashboardManager.loadContent();
                    break;
                case 'learning':
                    await LearningManager.loadContent();
                    break;
                case 'progress':
                    await ProgressManager.loadContent();
                    break;
                case 'community':
                    await CommunityManager.loadContent();
                    break;
            }
        } catch (error) {
            console.error(`Error loading ${section} content:`, error);
            ToastManager.show('콘텐츠를 불러오는 중 오류가 발생했습니다', 'error');
        }
    },

    toggleUserMenu() {
        const userMenu = document.getElementById('user-menu');
        const button = document.getElementById('user-menu-button');
        
        if (userMenu && button) {
            const isOpen = userMenu.classList.contains('show');
            userMenu.classList.toggle('show');
            button.setAttribute('aria-expanded', !isOpen);
        }
    },

    closeUserMenu() {
        const userMenu = document.getElementById('user-menu');
        const button = document.getElementById('user-menu-button');
        
        if (userMenu && button) {
            userMenu.classList.remove('show');
            button.setAttribute('aria-expanded', 'false');
        }
    }
};

// Toast Notification Manager
const ToastManager = {
    show(message, type = 'info', duration = 5000) {
        const toast = this.createToast(message, type);
        const container = document.getElementById('toast-container');
        
        if (container) {
            container.appendChild(toast);
            
            // Auto remove
            setTimeout(() => {
                this.remove(toast);
            }, duration);
        }
    },

    createToast(message, type) {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.setAttribute('role', 'alert');
        toast.setAttribute('aria-live', 'polite');
        
        const icon = this.getIcon(type);
        
        toast.innerHTML = `
            ${icon}
            <span class="toast-message">${message}</span>
            <button class="toast-close" aria-label="알림 닫기">
                <svg viewBox="0 0 24 24" fill="currentColor">
                    <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
                </svg>
            </button>
        `;
        
        // Bind close event
        const closeButton = toast.querySelector('.toast-close');
        if (closeButton) {
            closeButton.addEventListener('click', () => this.remove(toast));
        }
        
        return toast;
    },

    getIcon(type) {
        const icons = {
            success: '<svg class="toast-icon" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/></svg>',
            error: '<svg class="toast-icon" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/></svg>',
            warning: '<svg class="toast-icon" viewBox="0 0 24 24" fill="currentColor"><path d="M1 21h22L12 2 1 21zm12-3h-2v-2h2v2zm0-4h-2v-4h2v4z"/></svg>',
            info: '<svg class="toast-icon" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"/></svg>'
        };
        return icons[type] || icons.info;
    },

    remove(toast) {
        if (toast && toast.parentNode) {
            toast.style.animation = 'slideOut 300ms ease-in-out forwards';
            setTimeout(() => {
                toast.parentNode.removeChild(toast);
            }, 300);
        }
    }
};

// Dashboard Manager
const DashboardManager = {
    charts: {},

    async loadContent() {
        try {
            const [statsData, progressData, recommendations, recentActivity] = await Promise.all([
                this.fetchStats(),
                this.fetchProgressData(),
                this.fetchRecommendations(),
                this.fetchRecentActivity()
            ]);

            this.updateStats(statsData);
            this.updateProgressChart(progressData);
            this.updateRecommendations(recommendations);
            this.updateRecentActivity(recentActivity);

        } catch (error) {
            console.error('Dashboard loading error:', error);
            ToastManager.show('대시보드 데이터를 불러오는 중 오류가 발생했습니다', 'error');
        }
    },

    async fetchStats() {
        // Mock data - replace with actual API call
        return {
            overallProgress: 85,
            completedLessons: 24,
            successRate: 92,
            studyStreak: 12
        };
    },

    async fetchProgressData() {
        // Mock data - replace with actual API call
        const now = new Date();
        const data = [];
        
        for (let i = 30; i >= 0; i--) {
            const date = new Date(now);
            date.setDate(date.getDate() - i);
            data.push({
                date: date.toISOString().split('T')[0],
                progress: Math.random() * 100,
                timeSpent: Math.random() * 120 + 30
            });
        }
        
        return data;
    },

    async fetchRecommendations() {
        // Mock data - replace with actual API call
        return [
            {
                id: 1,
                title: '회귀분석 기초',
                description: '선형회귀와 다중회귀 분석 방법',
                difficulty: 'intermediate',
                estimatedTime: 45,
                matchScore: 0.92
            },
            {
                id: 2,
                title: '가설검정 심화',
                description: 't-검정과 카이제곱 검정 실습',
                difficulty: 'advanced',
                estimatedTime: 60,
                matchScore: 0.87
            }
        ];
    },

    async fetchRecentActivity() {
        // Mock data - replace with actual API call
        return [
            {
                id: 1,
                type: 'lesson_completed',
                title: '기술통계학 개념',
                timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
                score: 95
            },
            {
                id: 2,
                type: 'quiz_attempted',
                title: '확률분포 퀴즈',
                timestamp: new Date(Date.now() - 4 * 60 * 60 * 1000).toISOString(),
                score: 88
            }
        ];
    },

    updateStats(stats) {
        document.getElementById('overall-progress').textContent = `${stats.overallProgress}%`;
        document.getElementById('completed-lessons').textContent = Utils.formatNumber(stats.completedLessons);
        document.getElementById('success-rate').textContent = `${stats.successRate}%`;
        document.getElementById('study-streak').textContent = Utils.formatNumber(stats.studyStreak);
    },

    updateProgressChart(data) {
        const canvas = document.getElementById('progress-chart');
        if (!canvas) return;

        const ctx = canvas.getContext('2d');
        
        // Destroy existing chart
        if (this.charts.progress) {
            this.charts.progress.destroy();
        }

        this.charts.progress = new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.map(d => Utils.formatDate(d.date)),
                datasets: [{
                    label: '학습 진도',
                    data: data.map(d => d.progress),
                    borderColor: CONFIG.CHART_COLORS.primary,
                    backgroundColor: CONFIG.CHART_COLORS.primary + '20',
                    tension: 0.4,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        ticks: {
                            callback: function(value) {
                                return value + '%';
                            }
                        }
                    }
                }
            }
        });
    },

    updateRecommendations(recommendations) {
        const container = document.getElementById('recommendations');
        if (!container) return;

        container.innerHTML = recommendations.map(rec => `
            <div class="recommendation-item" data-id="${rec.id}">
                <div class="recommendation-header">
                    <h4 class="recommendation-title">${rec.title}</h4>
                    <span class="difficulty-badge ${rec.difficulty}">${this.getDifficultyText(rec.difficulty)}</span>
                </div>
                <p class="recommendation-description">${rec.description}</p>
                <div class="recommendation-meta">
                    <span class="time-estimate">${rec.estimatedTime}분</span>
                    <span class="match-score">매칭도: ${Math.round(rec.matchScore * 100)}%</span>
                </div>
                <button class="btn-primary btn-sm" onclick="LearningManager.startLesson(${rec.id})">
                    시작하기
                </button>
            </div>
        `).join('');
    },

    updateRecentActivity(activities) {
        const container = document.getElementById('recent-activity');
        if (!container) return;

        container.innerHTML = activities.map(activity => `
            <div class="activity-item">
                <div class="activity-icon ${activity.type}">
                    ${this.getActivityIcon(activity.type)}
                </div>
                <div class="activity-content">
                    <h4 class="activity-title">${activity.title}</h4>
                    <p class="activity-time">${this.getRelativeTime(activity.timestamp)}</p>
                    ${activity.score ? `<span class="activity-score">${activity.score}점</span>` : ''}
                </div>
            </div>
        `).join('');
    },

    getDifficultyText(difficulty) {
        const texts = {
            beginner: '기초',
            intermediate: '중급',
            advanced: '고급'
        };
        return texts[difficulty] || difficulty;
    },

    getActivityIcon(type) {
        const icons = {
            lesson_completed: '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/></svg>',
            quiz_attempted: '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/></svg>'
        };
        return icons[type] || icons.lesson_completed;
    },

    getRelativeTime(timestamp) {
        const now = new Date();
        const time = new Date(timestamp);
        const diffInHours = Math.floor((now - time) / (1000 * 60 * 60));
        
        if (diffInHours < 1) return '방금 전';
        if (diffInHours < 24) return `${diffInHours}시간 전`;
        
        const diffInDays = Math.floor(diffInHours / 24);
        return `${diffInDays}일 전`;
    }
};

// Learning Manager
const LearningManager = {
    currentLesson: null,

    async loadContent() {
        try {
            const learningPath = await this.fetchLearningPath();
            this.updateLearningPath(learningPath);
        } catch (error) {
            console.error('Learning content loading error:', error);
        }
    },

    async fetchLearningPath() {
        // Mock data - replace with actual API call
        return [
            {
                id: 'beginner',
                title: '연구방법론',
                description: '질적 연구의 기초부터 사례연구까지',
                progress: 100,
                status: 'completed'
            },
            {
                id: 'intermediate',
                title: '요인분석 이론',
                description: '다변량 분석과 통계적 추론',
                progress: 65,
                status: 'current'
            },
            {
                id: 'advanced',
                title: '통계학습',
                description: '머신러닝과 고급 통계 기법',
                progress: 0,
                status: 'locked'
            }
        ];
    },

    updateLearningPath(path) {
        // Update path steps in the UI
        path.forEach((step, index) => {
            const stepElement = document.querySelector(`[data-level="${step.id}"]`);
            if (stepElement) {
                const progressFill = stepElement.querySelector('.progress-fill');
                const progressText = stepElement.querySelector('.progress-text');
                
                if (progressFill) {
                    progressFill.style.width = `${step.progress}%`;
                }
                
                if (progressText) {
                    if (step.status === 'completed') {
                        progressText.textContent = '100% 완료';
                    } else if (step.status === 'locked') {
                        progressText.textContent = '잠금됨';
                    } else {
                        progressText.textContent = `${step.progress}% 완료`;
                    }
                }
                
                // Update classes
                stepElement.className = `path-step ${step.status}`;
            }
        });
    },

    async startLesson(lessonId) {
        try {
            // Navigate to learning section if not already there
            if (AppState.currentSection !== 'learning') {
                NavigationManager.navigateToSection('learning');
            }
            
            // Load lesson content
            const lesson = await this.fetchLesson(lessonId);
            this.displayLesson(lesson);
            
            ToastManager.show('학습을 시작합니다', 'success');
        } catch (error) {
            console.error('Error starting lesson:', error);
            ToastManager.show('학습을 시작하는 중 오류가 발생했습니다', 'error');
        }
    },

    async fetchLesson(lessonId) {
        // Mock lesson data - replace with actual API call
        return {
            id: lessonId,
            title: '샘플 강의',
            content: '여기에 강의 내용이 표시됩니다.',
            questions: []
        };
    },

    displayLesson(lesson) {
        const container = document.getElementById('learning-content');
        if (container) {
            container.innerHTML = `
                <div class="lesson-container">
                    <h2>${lesson.title}</h2>
                    <div class="lesson-content">${lesson.content}</div>
                </div>
            `;
        }
    }
};

// Progress Manager
const ProgressManager = {
    async loadContent() {
        try {
            const progressData = await this.fetchDetailedProgress();
            this.displayProgress(progressData);
        } catch (error) {
            console.error('Progress loading error:', error);
        }
    },

    async fetchDetailedProgress() {
        // Mock data - replace with actual API call
        return {
            overall: 85,
            subjects: [
                { name: '기술통계', progress: 95, score: 92 },
                { name: '확률론', progress: 80, score: 88 },
                { name: '추리통계', progress: 70, score: 85 }
            ]
        };
    },

    displayProgress(data) {
        const container = document.querySelector('#progress .progress-grid');
        if (container) {
            container.innerHTML = `
                <div class="progress-overview">
                    <h3>전체 진도: ${data.overall}%</h3>
                    <div class="subject-progress">
                        ${data.subjects.map(subject => `
                            <div class="subject-item">
                                <span>${subject.name}</span>
                                <div class="progress-bar">
                                    <div class="progress-fill" style="width: ${subject.progress}%"></div>
                                </div>
                                <span>${subject.score}점</span>
                            </div>
                        `).join('')}
                    </div>
                </div>
            `;
        }
    }
};

// Community Manager
const CommunityManager = {
    async loadContent() {
        try {
            const communityData = await this.fetchCommunityData();
            this.displayCommunity(communityData);
        } catch (error) {
            console.error('Community loading error:', error);
        }
    },

    async fetchCommunityData() {
        // Mock data - replace with actual API call
        return {
            discussions: [
                {
                    id: 1,
                    title: '회귀분석 질문',
                    author: '학습자A',
                    replies: 5,
                    timestamp: new Date()
                }
            ]
        };
    },

    displayCommunity(data) {
        const container = document.querySelector('#community .community-grid');
        if (container) {
            container.innerHTML = `
                <div class="community-overview">
                    <h3>최근 토론</h3>
                    ${data.discussions.map(discussion => `
                        <div class="discussion-item">
                            <h4>${discussion.title}</h4>
                            <p>작성자: ${discussion.author} | 답글: ${discussion.replies}개</p>
                        </div>
                    `).join('')}
                </div>
            `;
        }
    }
};

// Loading Manager
const LoadingManager = {
    show() {
        const loadingScreen = document.getElementById('loading-screen');
        if (loadingScreen) {
            loadingScreen.classList.remove('fade-out');
        }
    },

    hide() {
        const loadingScreen = document.getElementById('loading-screen');
        if (loadingScreen) {
            loadingScreen.classList.add('fade-out');
            setTimeout(() => {
                loadingScreen.style.display = 'none';
            }, 300);
        }
    }
};

// Application Initialization
class App {
    constructor() {
        this.initialized = false;
    }

    async init() {
        if (this.initialized) return;

        try {
            // Show loading screen
            LoadingManager.show();

            // Initialize managers
            ThemeManager.init();
            NavigationManager.init();
            
            // Handle browser navigation
            window.addEventListener('popstate', (e) => {
                const section = e.state?.section || 'dashboard';
                NavigationManager.setActiveSection(section);
                NavigationManager.loadSectionContent(section);
            });

            // Initialize help button
            this.initHelpButton();

            // Load initial content
            await NavigationManager.loadSectionContent(AppState.currentSection);

            // Setup periodic refresh
            this.setupPeriodicRefresh();

            this.initialized = true;
            
            // Hide loading screen
            LoadingManager.hide();

            // Show welcome message
            ToastManager.show('통계 학습 플랫폼에 오신 것을 환영합니다!', 'success');

        } catch (error) {
            console.error('App initialization error:', error);
            LoadingManager.hide();
            ToastManager.show('애플리케이션 초기화 중 오류가 발생했습니다', 'error');
        }
    }

    initHelpButton() {
        const helpButton = document.getElementById('help-fab');
        if (helpButton) {
            helpButton.addEventListener('click', () => {
                ToastManager.show('도움말 기능이 곧 제공될 예정입니다', 'info');
            });
        }
    }

    setupPeriodicRefresh() {
        setInterval(async () => {
            try {
                if (AppState.currentSection === 'dashboard') {
                    await DashboardManager.loadContent();
                }
            } catch (error) {
                console.error('Periodic refresh error:', error);
            }
        }, CONFIG.REFRESH_INTERVAL);
    }
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    const app = new App();
    app.init();
});

// Global error handler
window.addEventListener('error', (event) => {
    console.error('Global error:', event.error);
    ToastManager.show('예기치 않은 오류가 발생했습니다', 'error');
});

// Export for use in other modules
window.App = {
    state: AppState,
    utils: Utils,
    navigation: NavigationManager,
    dashboard: DashboardManager,
    learning: LearningManager,
    progress: ProgressManager,
    community: CommunityManager,
    toast: ToastManager,
    theme: ThemeManager
};