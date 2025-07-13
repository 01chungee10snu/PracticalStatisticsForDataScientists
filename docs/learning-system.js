/**
 * 적응형 학습 시스템 - JavaScript 구현
 * 콘텐츠를 외부 JSON 파일에서 동적으로 로드합니다.
 */

class AdaptiveLearningSystem {
    constructor() {
        this.learners = {};
        this.currentUser = null;
        this.contentLibrary = {}; // 초기에는 비어있음
        this.interactionLog = [];
        this.storageKey = 'adaptive-learning-data';
    }

    /**
     * 시스템 초기화 (비동기)
     * 콘텐츠를 로드하고 로컬 스토리지에서 데이터를 복원합니다.
     */
    async initialize() {
        try {
            await this.loadContentLibrary();
            this.loadFromStorage();
            console.log('📚 적응형 학습 시스템이 성공적으로 초기화되었습니다.');
            console.log('현재 학습자 데이터:', this.learners);
            console.log('현재 콘텐츠 라이브러리:', this.contentLibrary);
        } catch (error) {
            console.error('학습 시스템 초기화 실패:', error);
        }
    }

    /**
     * 외부 JSON 파일에서 콘텐츠 라이브러리를 로드합니다.
     */
    async loadContentLibrary() {
        const contentPaths = {
            foundation: {
                case_study_intro: 'content/foundation/case_study_intro.json',
                eda: 'content/foundation/eda.json',
                sampling: 'content/foundation/sampling.json'
            },
            developing: {
                case_study_datacollection: 'content/developing/case_study_datacollection.json',
                hypothesis_testing: 'content/developing/hypothesis_testing.json'
            },
            proficient: {
                regression: 'content/proficient/regression.json',
                classification: 'content/proficient/classification.json'
            },
            advanced: {
                machine_learning: 'content/advanced/machine_learning.json',
                unsupervised_learning: 'content/advanced/unsupervised_learning.json'
            }
        };

        const fetchPromises = [];
        for (const level in contentPaths) {
            this.contentLibrary[level] = {};
            for (const topic in contentPaths[level]) {
                const path = contentPaths[level][topic];
                fetchPromises.push(
                    fetch(path)
                        .then(response => {
                            if (!response.ok) {
                                throw new Error(`HTTP error! status: ${response.status} for ${path}`);
                            }
                            return response.json();
                        })
                        .then(data => {
                            this.contentLibrary[level][topic] = data;
                        })
                );
            }
        }

        await Promise.all(fetchPromises);
    }

    /**
     * 학습자 등록
     */
    registerLearner(userId, profile = {}) {
        const learnerData = {
            profile: {
                name: profile.name || userId,
                difficulty: profile.difficulty || 5,
                pace: profile.pace || "medium",
                ...profile
            },
            progress: {},
            performance: {},
            currentLevel: "foundation",
            adaptiveSettings: {
                difficultyPreference: profile.difficulty || 5,
                learningPace: profile.pace || "medium",
                successRate: 0.5
            },
            createdAt: new Date().toISOString()
        };

        this.learners[userId] = learnerData;
        this.currentUser = userId;
        this.saveToStorage();
        
        return {
            status: "success",
            message: `학습자 ${userId} 등록 완료`
        };
    }

    /**
     * 개인화된 콘텐츠 추천
     */
    getPersonalizedContent(userId) {
        if (!this.learners[userId]) {
            return { error: "학습자를 찾을 수 없습니다" };
        }

        const learner = this.learners[userId];
        const currentLevel = learner.currentLevel;
        const levelContent = this.contentLibrary[currentLevel] || {};

        // 전제조건을 만족하는 콘텐츠 필터링
        const availableContent = this.filterAvailableContent(userId, levelContent);

        if (Object.keys(availableContent).length === 0) {
            // 다음 레벨로 넘어갈 수 있는지 확인
            const nextLevel = this.getNextLevel(currentLevel);
            if (nextLevel && this.contentLibrary[nextLevel]) {
                learner.currentLevel = nextLevel;
                this.saveToStorage();
                return this.getPersonalizedContent(userId); // 재귀 호출
            }
            return { message: "모든 학습을 완료하셨습니다! 🎉" };
        }

        // 성과 기반 추천
        const successRate = learner.adaptiveSettings.successRate;
        let recommended;

        if (successRate < 0.4) {
            // 어려워하는 경우 - 쉬운 콘텐츠 추천
            recommended = this.getMinDifficultyContent(availableContent);
        } else if (successRate > 0.8) {
            // 잘하는 경우 - 어려운 콘텐츠 추천
            recommended = this.getMaxDifficultyContent(availableContent);
        } else {
            // 보통인 경우 - 중간 난이도
            recommended = this.getMediumDifficultyContent(availableContent, userId);
        }

        if (recommended) {
            const content = { ...recommended.content };
            return {
                contentId: recommended.id,
                content: content,
                recommendationReason: this.getRecommendationReason(successRate),
                estimatedTime: this.estimateTime(recommended.content.difficulty),
                userLevel: currentLevel
            };
        }

        return { message: "추천할 콘텐츠가 없습니다. 다음 레벨로 이동해보세요." };
    }

    /**
     * 답안 제출 및 채점
     */
    submitAnswer(userId, contentId, questionIdx, selectedOption) {
        if (!this.learners[userId]) {
            return { error: "학습자를 찾을 수 없습니다" };
        }

        const learner = this.learners[userId];

        // 콘텐츠와 문제 찾기
        let content = null;
        for (const levelContent of Object.values(this.contentLibrary)) {
            if (levelContent[contentId]) {
                content = levelContent[contentId];
                break;
            }
        }

        if (!content || questionIdx >= content.questions.length) {
            return { error: "문제를 찾을 수 없습니다" };
        }

        const question = content.questions[questionIdx];
        const isCorrect = selectedOption === question.correct;

        // 성과 기록
        if (!learner.performance[contentId]) {
            learner.performance[contentId] = [];
        }

        learner.performance[contentId].push({
            questionIdx: questionIdx,
            correct: isCorrect,
            timestamp: new Date().toISOString()
        });

        // 적응형 설정 업데이트
        this.updateAdaptiveSettings(userId, isCorrect);

        const result = {
            correct: isCorrect,
            explanation: question.explanation,
            yourAnswer: question.options[selectedOption],
            correctAnswer: question.options[question.correct],
            performanceSummary: this.getPerformanceSummary(userId, contentId)
        };

        // 레벨업 체크
        if (this.checkLevelUp(userId)) {
            result.levelUp = true;
            result.newLevel = learner.currentLevel;
        }

        this.saveToStorage();
        return result;
    }

    // ... (getLearningAnalytics, getSystemStats 등 나머지 메소드는 이전과 거의 동일) ...

    // === 헬퍼 메서드들 ===

    filterAvailableContent(userId, levelContent) {
        const available = {};
        const learner = this.learners[userId];
        for (const [contentId, content] of Object.entries(levelContent)) {
            // 이미 완료한 콘텐츠는 제외
            if (this.isContentMastered(userId, contentId)) continue;

            if (this.checkPrerequisites(userId, contentId)) {
                available[contentId] = content;
            }
        }
        return available;
    }

    checkPrerequisites(userId, contentId) {
        let prerequisites = [];
        for (const levelContent of Object.values(this.contentLibrary)) {
            if (levelContent[contentId]) {
                prerequisites = levelContent[contentId].prerequisites || [];
                break;
            }
        }
        
        for (const prereq of prerequisites) {
            if (!this.isContentMastered(userId, prereq)) {
                return false;
            }
        }
        return true;
    }

    isContentMastered(userId, contentId) {
        if (!this.learners[userId]) return false;

        const performance = this.learners[userId].performance[contentId] || [];
        if (performance.length === 0) return false;

        // 해당 콘텐츠의 모든 문제를 1번 이상 맞췄으면 마스터로 간주
        let content = null;
         for (const levelContent of Object.values(this.contentLibrary)) {
            if (levelContent[contentId]) {
                content = levelContent[contentId];
                break;
            }
        }
        if (!content) return false;

        const correctQuestions = new Set(performance.filter(p => p.correct).map(p => p.questionIdx));
        return correctQuestions.size >= content.questions.length;
    }

    getMinDifficultyContent(contentList) {
        return Object.entries(contentList).reduce((min, [id, content]) => {
            if (!min || content.difficulty < min.content.difficulty) {
                return { id, content };
            }
            return min;
        }, null);
    }

    getMaxDifficultyContent(contentList) {
        return Object.entries(contentList).reduce((max, [id, content]) => {
            if (!max || content.difficulty > max.content.difficulty) {
                return { id, content };
            }
            return max;
        }, null);
    }

    getMediumDifficultyContent(contentList, userId) {
        // 아직 풀지 않은 문제 중 중간 난이도
        const sorted = Object.entries(contentList).sort((a, b) => a[1].difficulty - b[1].difficulty);
        const midIndex = Math.floor(sorted.length / 2);
        const [id, content] = sorted[midIndex];
        return { id, content };
    }

    getNextLevel(currentLevel) {
        const levelProgression = {
            "foundation": "developing",
            "developing": "proficient", 
            "proficient": "advanced"
        };
        return levelProgression[currentLevel] || null;
    }

    checkLevelUp(userId) {
        const learner = this.learners[userId];
        const currentLevel = learner.currentLevel;
        const levelContent = this.contentLibrary[currentLevel] || {};

        for (const contentId of Object.keys(levelContent)) {
            if (!this.isContentMastered(userId, contentId)) {
                return false; // 현재 레벨의 모든 콘텐츠를 마스터해야 함
            }
        }

        const nextLevel = this.getNextLevel(currentLevel);
        if (nextLevel) {
            learner.currentLevel = nextLevel;
            return true;
        }

        return false;
    }

    // ... (이하 다른 헬퍼 메소드 및 데이터 저장/로드 메소드) ...
    // getRecommendationReason, estimateTime, getPerformanceSummary 등은 이전과 동일하게 유지

    getRecommendationReason(successRate) {
        if (successRate < 0.4) {
            return "기초를 탄탄히 하기 위해 쉬운 내용부터 시작하세요";
        } else if (successRate > 0.8) {
            return "실력이 뛰어나니 더 도전적인 내용을 학습해보세요";
        } else {
            return "현재 수준에 적합한 내용으로 단계적으로 학습하세요";
        }
    }

    estimateTime(difficulty) {
        const baseTime = difficulty * 5; // 기본 5분씩
        return `${baseTime}-${baseTime + 10}분`;
    }

    getPerformanceSummary(userId, contentId) {
        const learner = this.learners[userId];
        const performance = learner.performance[contentId] || [];

        if (performance.length === 0) {
            return { attempts: 0, correct: 0, successRate: 0 };
        }

        const correctCount = performance.filter(p => p.correct).length;
        const totalCount = performance.length;

        return {
            attempts: totalCount,
            correct: correctCount,
            successRate: Math.round(correctCount / totalCount * 100 * 10) / 10,
            lastAttempt: performance[performance.length - 1].timestamp
        };
    }

    updateAdaptiveSettings(userId, isCorrect) {
        const learner = this.learners[userId];
        const currentRate = learner.adaptiveSettings.successRate;
        const learningRate = 0.1;
        const newRate = currentRate + learningRate * ((isCorrect ? 1.0 : 0.0) - currentRate);
        learner.adaptiveSettings.successRate = Math.max(0.0, Math.min(1.0, newRate));
    }

    saveToStorage() {
        const data = {
            learners: this.learners,
            currentUser: this.currentUser,
            interactionLog: this.interactionLog
        };
        localStorage.setItem(this.storageKey, JSON.stringify(data));
    }

    loadFromStorage() {
        try {
            const data = localStorage.getItem(this.storageKey);
            if (data) {
                const parsed = JSON.parse(data);
                this.learners = parsed.learners || {};
                this.currentUser = parsed.currentUser || null;
                this.interactionLog = parsed.interactionLog || [];
            }
        } catch (error) {
            console.warn('Failed to load data from storage:', error);
        }
    }
}

// 전역 학습 시스템 인스턴스 생성 및 초기화
window.learningSystem = new AdaptiveLearningSystem();