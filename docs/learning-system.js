/**
 * 적응형 학습 시스템 - JavaScript 구현
 * Python 백엔드를 완전히 대체하는 클라이언트 사이드 시스템
 */

class AdaptiveLearningSystem {
    constructor() {
        this.learners = {};
        this.currentUser = null;
        this.contentLibrary = this.createContentLibrary();
        this.interactionLog = [];
        this.storageKey = 'adaptive-learning-data';
        
        // 로컬 스토리지에서 데이터 로드
        this.loadFromStorage();
    }

    /**
     * 콘텐츠 라이브러리 생성
     */
    createContentLibrary() {
        return {
            foundation: {
                stats_basics: {
                    title: "📊 기술통계 기초",
                    category: "descriptive_statistics",
                    difficulty: 3,
                    prerequisites: [],
                    learningObjectives: [
                        "중심경향성 지표(평균, 중앙값, 최빈값) 이해",
                        "분산과 표준편차의 의미 파악",
                        "분포의 치우침과 첨도 개념 학습"
                    ],
                    content: "데이터를 요약하고 특성을 파악하는 기술통계의 핵심 개념들을 학습합니다. 평균, 중앙값, 최빈값과 같은 중심경향성 지표와 분산, 표준편차 등의 산포도 지표를 이해합니다.",
                    detailedExplanation: {
                        "평균": "모든 값을 더한 후 개수로 나눈 값으로, 데이터의 대표값을 나타냅니다.",
                        "중앙값": "데이터를 크기 순으로 정렬했을 때 중간에 위치한 값입니다.",
                        "최빈값": "데이터에서 가장 자주 나타나는 값입니다.",
                        "분산": "각 데이터가 평균으로부터 얼마나 떨어져 있는지를 나타내는 지표입니다.",
                        "표준편차": "분산의 제곱근으로, 분산과 같은 단위를 가집니다."
                    },
                    realWorldExamples: [
                        "학생들의 시험 점수 분석",
                        "회사 직원들의 연봉 분포",
                        "상품 판매량의 계절적 변동"
                    ],
                    questions: [
                        {
                            q: "다음 데이터의 평균은? [1, 2, 3, 4, 5]",
                            options: ["2", "3", "4", "5"],
                            correct: 1,
                            explanation: "평균 = (1+2+3+4+5)/5 = 15/5 = 3. 모든 값을 더하고 개수로 나누어 계산합니다.",
                            difficulty: 2,
                            concept: "평균 계산"
                        },
                        {
                            q: "중앙값이 평균보다 작을 때 분포의 특징은?",
                            options: ["정규분포", "왼쪽 치우침", "오른쪽 치우침", "균등분포"],
                            correct: 2,
                            explanation: "중앙값 < 평균이면 오른쪽으로 치우친 분포입니다. 큰 값들이 평균을 오른쪽으로 끌어당기기 때문입니다.",
                            difficulty: 4,
                            concept: "분포의 치우침"
                        },
                        {
                            q: "표준편차가 클수록 데이터는?",
                            options: ["더 집중되어 있다", "더 퍼져있다", "평균이 크다", "중앙값이 크다"],
                            correct: 1,
                            explanation: "표준편차가 클수록 데이터가 평균으로부터 더 멀리 퍼져있음을 의미합니다.",
                            difficulty: 3,
                            concept: "산포도"
                        }
                    ]
                },
                probability: {
                    title: "🎲 확률 기초",
                    category: "probability_theory",
                    difficulty: 4,
                    prerequisites: ["stats_basics"],
                    learningObjectives: [
                        "확률의 기본 개념과 정의 이해",
                        "조건부 확률과 독립성 개념 학습",
                        "베이즈 정리의 기본 원리 파악"
                    ],
                    content: "불확실한 상황에서의 가능성을 수치로 표현하는 확률의 기본 개념을 학습합니다. 독립사건, 조건부 확률, 베이즈 정리 등의 핵심 개념을 다룹니다.",
                    questions: [
                        {
                            q: "동전을 두 번 던져서 모두 앞면이 나올 확률은?",
                            options: ["1/2", "1/3", "1/4", "1/8"],
                            correct: 2,
                            explanation: "독립사건이므로 P(첫 번째 앞면) × P(두 번째 앞면) = 1/2 × 1/2 = 1/4",
                            difficulty: 3,
                            concept: "독립사건의 확률"
                        },
                        {
                            q: "주사위를 던져 짝수가 나올 확률은?",
                            options: ["1/6", "1/3", "1/2", "2/3"],
                            correct: 2,
                            explanation: "짝수는 2, 4, 6이므로 3개. 전체 경우의 수는 6개이므로 3/6 = 1/2",
                            difficulty: 2,
                            concept: "기본 확률 계산"
                        }
                    ]
                },
                data_visualization: {
                    title: "📈 데이터 시각화",
                    category: "data_presentation",
                    difficulty: 3,
                    prerequisites: ["stats_basics"],
                    learningObjectives: [
                        "적절한 시각화 방법 선택",
                        "그래프 해석 능력 향상",
                        "효과적인 데이터 표현 기법 학습"
                    ],
                    content: "데이터의 특성에 맞는 시각화 방법을 선택하고 해석하는 능력을 기릅니다.",
                    questions: [
                        {
                            q: "두 변수 간의 상관관계를 보기에 가장 적합한 그래프는?",
                            options: ["히스토그램", "원형차트", "산점도", "막대그래프"],
                            correct: 2,
                            explanation: "산점도는 두 연속형 변수 간의 관계와 상관성을 시각적으로 보여주는 데 최적입니다.",
                            difficulty: 3,
                            concept: "그래프 선택"
                        }
                    ]
                }
            },
            developing: {
                hypothesis_testing: {
                    title: "🔬 가설검정",
                    category: "inferential_statistics",
                    difficulty: 6,
                    prerequisites: ["probability", "stats_basics"],
                    learningObjectives: [
                        "가설설정과 검정과정 이해",
                        "1종/2종 오류의 개념 파악",
                        "유의수준과 검정력의 관계 학습"
                    ],
                    content: "표본 데이터를 이용하여 모집단에 대한 가설을 검정하는 통계적 추론 방법을 학습합니다.",
                    questions: [
                        {
                            q: "1종 오류는 무엇인가?",
                            options: ["귀무가설이 참인데 기각", "귀무가설이 거짓인데 채택", 
                                      "대립가설이 참인데 기각", "검정통계량 계산 오류"],
                            correct: 0,
                            explanation: "1종 오류(α)는 실제로는 참인 귀무가설을 잘못 기각하는 것입니다. 이는 '거짓 양성' 결과를 만들어냅니다.",
                            difficulty: 4,
                            concept: "오류의 종류"
                        },
                        {
                            q: "유의수준 α=0.05의 의미는?",
                            options: ["95% 확률로 옳다", "5% 확률로 틀리다", "1종 오류 확률이 5%", "2종 오류 확률이 5%"],
                            correct: 2,
                            explanation: "유의수준 α=0.05는 1종 오류를 범할 확률을 5% 이하로 제한한다는 의미입니다.",
                            difficulty: 5,
                            concept: "유의수준"
                        }
                    ]
                },
                confidence_intervals: {
                    title: "📏 신뢰구간",
                    category: "inferential_statistics", 
                    difficulty: 5,
                    prerequisites: ["probability", "stats_basics"],
                    learningObjectives: [
                        "신뢰구간의 개념과 해석",
                        "신뢰도와 구간의 폭의 관계",
                        "다양한 모수에 대한 신뢰구간 구성"
                    ],
                    content: "표본통계량을 이용하여 모집단 모수를 추정하는 구간추정 방법을 학습합니다.",
                    questions: [
                        {
                            q: "95% 신뢰구간의 의미는?",
                            options: ["모수가 95% 확률로 구간에 있다", "표본평균이 95% 확률로 구간에 있다", 
                                      "같은 방법으로 100번 구간을 만들면 95번은 모수를 포함한다", "구간의 길이가 95%이다"],
                            correct: 2,
                            explanation: "95% 신뢰구간은 같은 방법으로 100번 구간을 만들 때 약 95번은 실제 모수를 포함한다는 의미입니다.",
                            difficulty: 6,
                            concept: "신뢰구간 해석"
                        }
                    ]
                }
            },
            proficient: {
                regression_analysis: {
                    title: "📊 회귀분석",
                    category: "advanced_analysis",
                    difficulty: 7,
                    prerequisites: ["hypothesis_testing", "confidence_intervals"],
                    learningObjectives: [
                        "선형회귀모델의 원리 이해",
                        "회귀계수의 의미와 해석",
                        "모델의 적합도 평가 방법"
                    ],
                    content: "변수 간의 관계를 수학적 모델로 표현하고 예측에 활용하는 회귀분석을 학습합니다.",
                    questions: [
                        {
                            q: "회귀계수 β=2.5의 의미는?",
                            options: ["상관계수가 2.5", "독립변수 1증가시 종속변수 2.5증가", 
                                      "모델의 정확도가 2.5%", "절편이 2.5"],
                            correct: 1,
                            explanation: "회귀계수는 독립변수가 1단위 증가할 때 종속변수의 평균적인 변화량을 나타냅니다.",
                            difficulty: 5,
                            concept: "회귀계수 해석"
                        }
                    ]
                }
            },
            advanced: {
                machine_learning_basics: {
                    title: "🤖 머신러닝 기초",
                    category: "predictive_modeling",
                    difficulty: 8,
                    prerequisites: ["regression_analysis"],
                    learningObjectives: [
                        "지도학습과 비지도학습의 차이점",
                        "과적합과 일반화의 개념",
                        "모델 성능 평가 지표"
                    ],
                    content: "데이터로부터 패턴을 학습하여 예측이나 분류를 수행하는 머신러닝의 기본 개념을 학습합니다.",
                    questions: [
                        {
                            q: "과적합(overfitting)이란?",
                            options: ["모델이 너무 단순해서 성능이 낮음", "훈련데이터에만 잘 맞고 새 데이터에는 성능이 낮음", 
                                      "데이터가 부족한 상황", "알고리즘이 복잡한 상황"],
                            correct: 1,
                            explanation: "과적합은 모델이 훈련 데이터의 잡음까지 학습하여 새로운 데이터에 대한 일반화 성능이 떨어지는 현상입니다.",
                            difficulty: 6,
                            concept: "과적합"
                        }
                    ]
                }
            }
        };
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
            return { message: "현재 학습 가능한 콘텐츠가 없습니다" };
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
            recommended = this.getMediumDifficultyContent(availableContent);
        }

        if (recommended) {
            const content = { ...recommended.content };
            content.learningPath = this.generateLearningPath(userId, recommended.id);
            content.studyTips = this.generateStudyTips(recommended.content);

            return {
                contentId: recommended.id,
                content: content,
                recommendationReason: this.getRecommendationReason(successRate),
                estimatedTime: this.estimateTime(recommended.content.difficulty),
                userLevel: currentLevel,
                prerequisitesMet: this.checkPrerequisites(userId, recommended.id),
                nextTopics: this.suggestNextTopics(userId, recommended.id)
            };
        }

        return { message: "추천할 콘텐츠가 없습니다" };
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

        // 상호작용 로그 기록
        this.interactionLog.push({
            userId: userId,
            contentId: contentId,
            questionIdx: questionIdx,
            correct: isCorrect,
            timestamp: new Date().toISOString()
        });

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

    /**
     * 학습 분석 데이터 제공
     */
    getLearningAnalytics(userId) {
        if (!this.learners[userId]) {
            return { error: "학습자를 찾을 수 없습니다" };
        }

        const learner = this.learners[userId];

        // 전체 성과 분석
        const allPerformance = [];
        Object.values(learner.performance).forEach(contentPerformances => {
            allPerformance.push(...contentPerformances);
        });

        if (allPerformance.length === 0) {
            return { message: "아직 학습 기록이 없습니다" };
        }

        const totalAttempts = allPerformance.length;
        const correctAttempts = allPerformance.filter(p => p.correct).length;

        // 학습 패턴 분석
        const recentPerformance = allPerformance.slice(-10);
        const recentSuccessRate = recentPerformance.filter(p => p.correct).length / recentPerformance.length;

        // 학습 상태 판단
        let learningState, recommendation;
        if (recentSuccessRate < 0.3) {
            learningState = "어려움을 겪고 있음";
            recommendation = "기초 내용을 다시 복습하거나 도움을 요청하세요";
        } else if (recentSuccessRate > 0.8) {
            learningState = "매우 잘하고 있음";
            recommendation = "더 도전적인 내용으로 진행하세요";
        } else {
            learningState = "정상적으로 진행 중";
            recommendation = "현재 속도를 유지하며 꾸준히 학습하세요";
        }

        return {
            overallStats: {
                totalAttempts: totalAttempts,
                correctAttempts: correctAttempts,
                successRate: Math.round(correctAttempts / totalAttempts * 100 * 10) / 10,
                currentLevel: learner.currentLevel
            },
            recentPerformance: {
                last10Attempts: recentPerformance.length,
                recentSuccessRate: Math.round(recentSuccessRate * 100 * 10) / 10
            },
            learningState: learningState,
            recommendation: recommendation,
            adaptiveSettings: learner.adaptiveSettings
        };
    }

    /**
     * 시스템 전체 통계
     */
    getSystemStats() {
        const totalLearners = Object.keys(this.learners).length;
        const totalInteractions = this.interactionLog.length;

        if (totalLearners === 0) {
            return { message: "등록된 학습자가 없습니다" };
        }

        // 레벨별 분포
        const levelDistribution = {};
        Object.values(this.learners).forEach(learner => {
            const level = learner.currentLevel;
            levelDistribution[level] = (levelDistribution[level] || 0) + 1;
        });

        // 전체 성공률
        const correctInteractions = this.interactionLog.filter(log => log.correct).length;
        const overallSuccessRate = totalInteractions > 0 ? 
            Math.round(correctInteractions / totalInteractions * 100 * 10) / 10 : 0;

        return {
            totalLearners: totalLearners,
            totalInteractions: totalInteractions,
            overallSuccessRate: overallSuccessRate,
            levelDistribution: levelDistribution,
            contentLibrarySize: Object.values(this.contentLibrary).reduce((sum, level) => 
                sum + Object.keys(level).length, 0)
        };
    }

    // === 헬퍼 메서드들 ===

    filterAvailableContent(userId, levelContent) {
        const available = {};
        for (const [contentId, content] of Object.entries(levelContent)) {
            if (this.checkPrerequisites(userId, contentId)) {
                available[contentId] = content;
            }
        }
        return available;
    }

    checkPrerequisites(userId, contentId) {
        // 현재 레벨의 콘텐츠 찾기
        for (const levelContent of Object.values(this.contentLibrary)) {
            if (levelContent[contentId]) {
                const prerequisites = levelContent[contentId].prerequisites || [];
                for (const prereq of prerequisites) {
                    if (!this.isContentMastered(userId, prereq)) {
                        return false;
                    }
                }
                return true;
            }
        }
        return true;
    }

    isContentMastered(userId, contentId) {
        if (!this.learners[userId]) return false;

        const learner = this.learners[userId];
        const performance = learner.performance[contentId] || [];

        if (performance.length < 3) return false;

        // 최근 3번의 시도에서 80% 이상 성공 시 숙달로 판단
        const recentAttempts = performance.slice(-3);
        const successCount = recentAttempts.filter(attempt => attempt.correct).length;
        return successCount >= 2; // 3번 중 2번 이상 성공
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

    getMediumDifficultyContent(contentList) {
        const contentArray = Object.entries(contentList);
        const midIndex = Math.floor(contentArray.length / 2);
        const [id, content] = contentArray[midIndex];
        return { id, content };
    }

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

    generateLearningPath(userId, contentId) {
        // 현재 콘텐츠 찾기
        let currentContent = null;
        for (const levelContent of Object.values(this.contentLibrary)) {
            if (levelContent[contentId]) {
                currentContent = levelContent[contentId];
                break;
            }
        }

        if (!currentContent) return [];

        const path = [];
        const objectives = currentContent.learningObjectives || [];
        objectives.forEach((objective, i) => {
            path.push(`단계 ${i + 1}: ${objective}`);
        });

        // 실제 예제와 연습 단계 추가
        path.push(`단계 ${path.length + 1}: 실제 예제로 개념 적용해보기`);
        path.push(`단계 ${path.length + 1}: 연습 문제로 이해도 확인하기`);

        return path;
    }

    generateStudyTips(content) {
        const tips = [];
        const difficulty = content.difficulty || 5;

        if (difficulty <= 3) {
            tips.push(...[
                "기본 개념부터 차근차근 이해해보세요",
                "예제를 따라하며 직접 계산해보세요",
                "개념을 자신만의 언어로 설명해보세요"
            ]);
        } else if (difficulty <= 6) {
            tips.push(...[
                "전제조건 개념들을 먼저 복습하세요",
                "단계별로 나누어 접근해보세요",
                "실생활 예시와 연결해서 이해해보세요"
            ]);
        } else {
            tips.push(...[
                "관련 이론의 배경과 원리를 깊이 이해하세요",
                "다양한 응용 사례를 찾아보세요",
                "개념 간의 연결고리를 파악해보세요"
            ]);
        }

        const category = content.category || "";
        if (category.includes("statistics")) {
            tips.push("통계적 사고를 위해 '왜?'라는 질문을 많이 해보세요");
        } else if (category.includes("probability")) {
            tips.push("확률 문제는 경우의 수를 체계적으로 세어보세요");
        } else if (category.includes("analysis")) {
            tips.push("분석 결과의 실제 의미를 해석하는 연습을 해보세요");
        }

        return tips;
    }

    suggestNextTopics(userId, currentContentId) {
        // 현재 콘텐츠의 카테고리와 난이도 파악
        let currentContent = null;
        let currentLevel = null;

        for (const [level, levelContent] of Object.entries(this.contentLibrary)) {
            if (levelContent[currentContentId]) {
                currentContent = levelContent[currentContentId];
                currentLevel = level;
                break;
            }
        }

        if (!currentContent) return [];

        const nextTopics = [];
        const currentCategory = currentContent.category || "";
        const currentDifficulty = currentContent.difficulty || 5;

        // 같은 레벨에서 연관된 주제들
        if (currentLevel) {
            const levelContent = this.contentLibrary[currentLevel];
            for (const [contentId, content] of Object.entries(levelContent)) {
                if (contentId !== currentContentId && 
                    content.category === currentCategory &&
                    Math.abs(content.difficulty - currentDifficulty) <= 2) {
                    nextTopics.push(content.title);
                }
            }
        }

        // 다음 레벨의 관련 주제들
        const levelProgression = {
            "foundation": "developing",
            "developing": "proficient", 
            "proficient": "advanced"
        };

        if (currentLevel && levelProgression[currentLevel]) {
            const nextLevel = levelProgression[currentLevel];
            if (this.contentLibrary[nextLevel]) {
                const nextLevelContent = this.contentLibrary[nextLevel];
                for (const [contentId, content] of Object.entries(nextLevelContent)) {
                    const prerequisites = content.prerequisites || [];
                    if (prerequisites.includes(currentContentId)) {
                        nextTopics.push(`[다음 단계] ${content.title}`);
                    }
                }
            }
        }

        return nextTopics.slice(0, 3); // 최대 3개만 반환
    }

    updateAdaptiveSettings(userId, isCorrect) {
        const learner = this.learners[userId];

        // 성공률 업데이트 (이동평균)
        const currentRate = learner.adaptiveSettings.successRate;
        const learningRate = 0.1;
        const newRate = currentRate + learningRate * ((isCorrect ? 1.0 : 0.0) - currentRate);
        learner.adaptiveSettings.successRate = Math.max(0.0, Math.min(1.0, newRate));

        // 난이도 선호도 조정
        if (isCorrect && currentRate > 0.8) {
            learner.adaptiveSettings.difficultyPreference += 0.1;
        } else if (!isCorrect && currentRate < 0.4) {
            learner.adaptiveSettings.difficultyPreference -= 0.1;
        }

        learner.adaptiveSettings.difficultyPreference = Math.max(1, Math.min(10, 
            learner.adaptiveSettings.difficultyPreference));
    }

    getPerformanceSummary(userId, contentId) {
        const learner = this.learners[userId];
        const performance = learner.performance[contentId] || [];

        if (performance.length === 0) {
            return { attempts: 0, successRate: 0 };
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

    checkLevelUp(userId) {
        const learner = this.learners[userId];
        const currentLevel = learner.currentLevel;

        // 현재 레벨의 모든 콘텐츠에서 80% 이상 성공률 달성 시 레벨업
        const levelContent = this.contentLibrary[currentLevel] || {};

        for (const contentId of Object.keys(levelContent)) {
            const performance = learner.performance[contentId] || [];
            if (performance.length === 0) return false;

            const correctCount = performance.filter(p => p.correct).length;
            const successRate = correctCount / performance.length;

            if (successRate < 0.8) return false;
        }

        // 모든 조건 만족 시 레벨업
        const levelProgression = {
            "foundation": "developing",
            "developing": "proficient", 
            "proficient": "advanced"
        };

        if (levelProgression[currentLevel]) {
            learner.currentLevel = levelProgression[currentLevel];
            return true;
        }

        return false;
    }

    // === 데이터 저장/로드 ===

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

    clearStorage() {
        localStorage.removeItem(this.storageKey);
        this.learners = {};
        this.currentUser = null;
        this.interactionLog = [];
    }
}

// 전역 학습 시스템 인스턴스
window.learningSystem = new AdaptiveLearningSystem();