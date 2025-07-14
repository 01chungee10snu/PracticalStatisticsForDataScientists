#!/usr/bin/env python3
"""
의존성 없는 독립 실행 가능한 학습 시스템 데모
- 외부 라이브러리 없이 동작
- 기본 Python만으로 구현
- 실제 동작 가능한 핵심 기능만 포함
"""

import json
import random
import math
from datetime import datetime
from typing import Dict, List, Any, Optional

# 시각화 모듈 임포트
try:
    from .enhanced_visualization import visualizer, create_statistics_visualization
except ImportError:
    # 상대 임포트 실패 시 절대 임포트 시도
    try:
        from enhanced_visualization import visualizer, create_statistics_visualization
    except ImportError:
        # 시각화 기능 없이 동작
        visualizer = None
        def create_statistics_visualization(*args, **kwargs):
            return "시각화 모듈을 사용할 수 없습니다."


class SimpleLearningSystem:
    """의존성 없는 간단한 학습 시스템"""
    
    def __init__(self):
        self.learners = {}
        self.content_library = self._create_content_library()
        self.interaction_log = []
        
    def _create_content_library(self) -> Dict[str, Any]:
        """콘텐츠 라이브러리 생성"""
        return {
            "foundation": {
                "stats_basics": {
                    "title": "📊 기술통계 기초",
                    "category": "descriptive_statistics",
                    "difficulty": 3,
                    "prerequisites": [],
                    "learning_objectives": [
                        "중심경향성 지표(평균, 중앙값, 최빈값) 이해",
                        "분산과 표준편차의 의미 파악",
                        "분포의 치우침과 첨도 개념 학습"
                    ],
                    "content": "데이터를 요약하고 특성을 파악하는 기술통계의 핵심 개념들을 학습합니다. 평균, 중앙값, 최빈값과 같은 중심경향성 지표와 분산, 표준편차 등의 산포도 지표를 이해합니다.",
                    "detailed_explanation": {
                        "평균": "모든 값을 더한 후 개수로 나눈 값으로, 데이터의 대표값을 나타냅니다.",
                        "중앙값": "데이터를 크기 순으로 정렬했을 때 중간에 위치한 값입니다.",
                        "최빈값": "데이터에서 가장 자주 나타나는 값입니다.",
                        "분산": "각 데이터가 평균으로부터 얼마나 떨어져 있는지를 나타내는 지표입니다.",
                        "표준편차": "분산의 제곱근으로, 분산과 같은 단위를 가집니다."
                    },
                    "visual_aids": [
                        "히스토그램과 평균/중앙값 비교",
                        "정규분포와 치우친 분포의 특성",
                        "산포도가 다른 데이터셋 비교"
                    ],
                    "real_world_examples": [
                        "학생들의 시험 점수 분석",
                        "회사 직원들의 연봉 분포",
                        "상품 판매량의 계절적 변동"
                    ],
                    "questions": [
                        {
                            "q": "다음 데이터의 평균은? [1, 2, 3, 4, 5]",
                            "options": ["2", "3", "4", "5"],
                            "correct": 1,
                            "explanation": "평균 = (1+2+3+4+5)/5 = 15/5 = 3. 모든 값을 더하고 개수로 나누어 계산합니다.",
                            "difficulty": 2,
                            "concept": "평균 계산"
                        },
                        {
                            "q": "중앙값이 평균보다 작을 때 분포의 특징은?",
                            "options": ["정규분포", "왼쪽 치우침", "오른쪽 치우침", "균등분포"],
                            "correct": 2,
                            "explanation": "중앙값 < 평균이면 오른쪽으로 치우친 분포입니다. 큰 값들이 평균을 오른쪽으로 끌어당기기 때문입니다.",
                            "difficulty": 4,
                            "concept": "분포의 치우침"
                        },
                        {
                            "q": "표준편차가 클수록 데이터는?",
                            "options": ["더 집중되어 있다", "더 퍼져있다", "평균이 크다", "중앙값이 크다"],
                            "correct": 1,
                            "explanation": "표준편차가 클수록 데이터가 평균으로부터 더 멀리 퍼져있음을 의미합니다.",
                            "difficulty": 3,
                            "concept": "산포도"
                        }
                    ]
                },
                "probability": {
                    "title": "🎲 확률 기초",
                    "category": "probability_theory",
                    "difficulty": 4,
                    "prerequisites": ["stats_basics"],
                    "learning_objectives": [
                        "확률의 기본 개념과 정의 이해",
                        "조건부 확률과 독립성 개념 학습",
                        "베이즈 정리의 기본 원리 파악"
                    ],
                    "content": "불확실한 상황에서의 가능성을 수치로 표현하는 확률의 기본 개념을 학습합니다. 독립사건, 조건부 확률, 베이즈 정리 등의 핵심 개념을 다룹니다.",
                    "detailed_explanation": {
                        "확률": "어떤 사건이 일어날 가능성을 0과 1 사이의 수로 나타낸 것",
                        "독립사건": "한 사건의 결과가 다른 사건의 결과에 영향을 주지 않는 경우",
                        "조건부확률": "특정 조건이 주어졌을 때 사건이 일어날 확률",
                        "베이즈정리": "새로운 정보를 바탕으로 기존 확률을 수정하는 방법"
                    },
                    "visual_aids": [
                        "확률 트리 다이어그램",
                        "벤 다이어그램으로 사건의 교집합과 합집합",
                        "조건부 확률의 시각적 표현"
                    ],
                    "real_world_examples": [
                        "날씨 예보의 확률",
                        "의료 진단의 정확도",
                        "투자 수익률의 불확실성"
                    ],
                    "questions": [
                        {
                            "q": "동전을 두 번 던져서 모두 앞면이 나올 확률은?",
                            "options": ["1/2", "1/3", "1/4", "1/8"],
                            "correct": 2,
                            "explanation": "독립사건이므로 P(첫 번째 앞면) × P(두 번째 앞면) = 1/2 × 1/2 = 1/4",
                            "difficulty": 3,
                            "concept": "독립사건의 확률"
                        },
                        {
                            "q": "주사위를 던져 짝수가 나올 확률은?",
                            "options": ["1/6", "1/3", "1/2", "2/3"],
                            "correct": 2,
                            "explanation": "짝수는 2, 4, 6이므로 3개. 전체 경우의 수는 6개이므로 3/6 = 1/2",
                            "difficulty": 2,
                            "concept": "기본 확률 계산"
                        }
                    ]
                },
                "data_visualization": {
                    "title": "📈 데이터 시각화",
                    "category": "data_presentation",
                    "difficulty": 3,
                    "prerequisites": ["stats_basics"],
                    "learning_objectives": [
                        "적절한 시각화 방법 선택",
                        "그래프 해석 능력 향상",
                        "효과적인 데이터 표현 기법 학습"
                    ],
                    "content": "데이터의 특성에 맞는 시각화 방법을 선택하고 해석하는 능력을 기릅니다.",
                    "detailed_explanation": {
                        "히스토그램": "연속형 데이터의 분포를 보여주는 막대그래프",
                        "산점도": "두 변수 간의 관계를 점으로 표현한 그래프",
                        "상자그림": "데이터의 분포와 이상치를 한눈에 보여주는 그래프"
                    },
                    "questions": [
                        {
                            "q": "두 변수 간의 상관관계를 보기에 가장 적합한 그래프는?",
                            "options": ["히스토그램", "원형차트", "산점도", "막대그래프"],
                            "correct": 2,
                            "explanation": "산점도는 두 연속형 변수 간의 관계와 상관성을 시각적으로 보여주는 데 최적입니다.",
                            "difficulty": 3,
                            "concept": "그래프 선택"
                        }
                    ]
                }
            },
            "developing": {
                "hypothesis_testing": {
                    "title": "🔬 가설검정",
                    "category": "inferential_statistics",
                    "difficulty": 6,
                    "prerequisites": ["probability", "stats_basics"],
                    "learning_objectives": [
                        "가설설정과 검정과정 이해",
                        "1종/2종 오류의 개념 파악",
                        "유의수준과 검정력의 관계 학습"
                    ],
                    "content": "표본 데이터를 이용하여 모집단에 대한 가설을 검정하는 통계적 추론 방법을 학습합니다.",
                    "detailed_explanation": {
                        "귀무가설": "현재 상태나 기존 믿음을 나타내는 가설로, 차이가 없다고 가정",
                        "대립가설": "우리가 증명하고자 하는 가설로, 유의한 차이가 있다고 주장",
                        "1종오류": "참인 귀무가설을 잘못 기각하는 오류 (α)",
                        "2종오류": "거짓인 귀무가설을 기각하지 못하는 오류 (β)",
                        "유의수준": "1종 오류를 범할 확률의 상한선"
                    },
                    "visual_aids": [
                        "가설검정의 단계별 프로세스",
                        "1종/2종 오류의 시각적 표현",
                        "검정통계량의 분포와 기각역"
                    ],
                    "real_world_examples": [
                        "신약의 효과 검증",
                        "새로운 교육방법의 효과성 평가",
                        "품질관리에서의 불량률 검사"
                    ],
                    "questions": [
                        {
                            "q": "1종 오류는 무엇인가?",
                            "options": ["귀무가설이 참인데 기각", "귀무가설이 거짓인데 채택", 
                                      "대립가설이 참인데 기각", "검정통계량 계산 오류"],
                            "correct": 0,
                            "explanation": "1종 오류(α)는 실제로는 참인 귀무가설을 잘못 기각하는 것입니다. 이는 '거짓 양성' 결과를 만들어냅니다.",
                            "difficulty": 4,
                            "concept": "오류의 종류"
                        },
                        {
                            "q": "유의수준 α=0.05의 의미는?",
                            "options": ["95% 확률로 옳다", "5% 확률로 틀리다", "1종 오류 확률이 5%", "2종 오류 확률이 5%"],
                            "correct": 2,
                            "explanation": "유의수준 α=0.05는 1종 오류를 범할 확률을 5% 이하로 제한한다는 의미입니다.",
                            "difficulty": 5,
                            "concept": "유의수준"
                        }
                    ]
                },
                "confidence_intervals": {
                    "title": "📏 신뢰구간",
                    "category": "inferential_statistics", 
                    "difficulty": 5,
                    "prerequisites": ["probability", "stats_basics"],
                    "learning_objectives": [
                        "신뢰구간의 개념과 해석",
                        "신뢰도와 구간의 폭의 관계",
                        "다양한 모수에 대한 신뢰구간 구성"
                    ],
                    "content": "표본통계량을 이용하여 모집단 모수를 추정하는 구간추정 방법을 학습합니다.",
                    "detailed_explanation": {
                        "신뢰구간": "모집단 모수가 포함될 것으로 추정되는 구간",
                        "신뢰도": "구간이 실제 모수를 포함할 확률",
                        "오차한계": "추정값과 실제값 사이의 최대 허용 오차"
                    },
                    "questions": [
                        {
                            "q": "95% 신뢰구간의 의미는?",
                            "options": ["모수가 95% 확률로 구간에 있다", "표본평균이 95% 확률로 구간에 있다", 
                                      "같은 방법으로 100번 구간을 만들면 95번은 모수를 포함한다", "구간의 길이가 95%이다"],
                            "correct": 2,
                            "explanation": "95% 신뢰구간은 같은 방법으로 100번 구간을 만들 때 약 95번은 실제 모수를 포함한다는 의미입니다.",
                            "difficulty": 6,
                            "concept": "신뢰구간 해석"
                        }
                    ]
                }
            },
            "proficient": {
                "regression_analysis": {
                    "title": "📊 회귀분석",
                    "category": "advanced_analysis",
                    "difficulty": 7,
                    "prerequisites": ["hypothesis_testing", "confidence_intervals"],
                    "learning_objectives": [
                        "선형회귀모델의 원리 이해",
                        "회귀계수의 의미와 해석",
                        "모델의 적합도 평가 방법"
                    ],
                    "content": "변수 간의 관계를 수학적 모델로 표현하고 예측에 활용하는 회귀분석을 학습합니다.",
                    "detailed_explanation": {
                        "회귀계수": "독립변수가 1단위 증가할 때 종속변수의 평균 변화량",
                        "결정계수": "회귀모델이 설명하는 분산의 비율",
                        "잔차": "실제값과 예측값의 차이"
                    },
                    "questions": [
                        {
                            "q": "회귀계수 β=2.5의 의미는?",
                            "options": ["상관계수가 2.5", "독립변수 1증가시 종속변수 2.5증가", 
                                      "모델의 정확도가 2.5%", "절편이 2.5"],
                            "correct": 1,
                            "explanation": "회귀계수는 독립변수가 1단위 증가할 때 종속변수의 평균적인 변화량을 나타냅니다.",
                            "difficulty": 5,
                            "concept": "회귀계수 해석"
                        }
                    ]
                }
            },
            "advanced": {
                "machine_learning_basics": {
                    "title": "🤖 머신러닝 기초",
                    "category": "predictive_modeling",
                    "difficulty": 8,
                    "prerequisites": ["regression_analysis"],
                    "learning_objectives": [
                        "지도학습과 비지도학습의 차이점",
                        "과적합과 일반화의 개념",
                        "모델 성능 평가 지표"
                    ],
                    "content": "데이터로부터 패턴을 학습하여 예측이나 분류를 수행하는 머신러닝의 기본 개념을 학습합니다.",
                    "questions": [
                        {
                            "q": "과적합(overfitting)이란?",
                            "options": ["모델이 너무 단순해서 성능이 낮음", "훈련데이터에만 잘 맞고 새 데이터에는 성능이 낮음", 
                                      "데이터가 부족한 상황", "알고리즘이 복잡한 상황"],
                            "correct": 1,
                            "explanation": "과적합은 모델이 훈련 데이터의 잡음까지 학습하여 새로운 데이터에 대한 일반화 성능이 떨어지는 현상입니다.",
                            "difficulty": 6,
                            "concept": "과적합"
                        }
                    ]
                }
            }
        }
    
    def register_learner(self, user_id: str, profile: Dict[str, Any]) -> Dict[str, str]:
        """학습자 등록"""
        self.learners[user_id] = {
            "profile": profile,
            "progress": {},
            "performance": {},
            "current_level": "foundation",
            "adaptive_settings": {
                "difficulty_preference": profile.get("difficulty", 5),
                "learning_pace": profile.get("pace", "medium"),
                "success_rate": 0.5
            },
            "created_at": datetime.now().isoformat()
        }
        return {"status": "success", "message": f"학습자 {user_id} 등록 완료"}
    
    def get_personalized_content(self, user_id: str) -> Dict[str, Any]:
        """개인화된 콘텐츠 추천"""
        if user_id not in self.learners:
            return {"error": "학습자를 찾을 수 없습니다"}
        
        learner = self.learners[user_id]
        current_level = learner["current_level"]
        
        # 현재 레벨의 콘텐츠 가져오기
        level_content = self.content_library.get(current_level, {})
        
        # 전제조건 확인하여 적합한 콘텐츠 필터링
        available_content = self._filter_available_content(user_id, level_content)
        
        if not available_content:
            return {"message": "현재 학습 가능한 콘텐츠가 없습니다"}
        
        # 성과 기반 추천
        success_rate = learner["adaptive_settings"]["success_rate"]
        
        # 적응형 난이도 조정
        if success_rate < 0.4:
            # 어려워하는 경우 - 쉬운 콘텐츠 추천
            recommended = min(available_content.items(), 
                            key=lambda x: x[1]["difficulty"], default=(None, None))
        elif success_rate > 0.8:
            # 잘하는 경우 - 어려운 콘텐츠 추천
            recommended = max(available_content.items(), 
                            key=lambda x: x[1]["difficulty"], default=(None, None))
        else:
            # 보통인 경우 - 중간 난이도
            content_list = list(available_content.items())
            recommended = content_list[len(content_list)//2] if content_list else (None, None)
        
        if recommended[0]:
            content = recommended[1].copy()
            # 학습 목표와 구체적 설명 추가
            content["learning_path"] = self._generate_learning_path(user_id, recommended[0])
            content["study_tips"] = self._generate_study_tips(recommended[1])
            
            return {
                "content_id": recommended[0],
                "content": content,
                "recommendation_reason": self._get_recommendation_reason(success_rate),
                "estimated_time": self._estimate_time(recommended[1]["difficulty"]),
                "user_level": current_level,
                "prerequisites_met": self._check_prerequisites(user_id, recommended[0]),
                "next_topics": self._suggest_next_topics(user_id, recommended[0])
            }
        else:
            return {"message": "추천할 콘텐츠가 없습니다"}
    
    def _get_recommendation_reason(self, success_rate: float) -> str:
        """추천 이유 생성"""
        if success_rate < 0.4:
            return "기초를 탄탄히 하기 위해 쉬운 내용부터 시작하세요"
        elif success_rate > 0.8:
            return "실력이 뛰어나니 더 도전적인 내용을 학습해보세요"
        else:
            return "현재 수준에 적합한 내용으로 단계적으로 학습하세요"
    
    def _estimate_time(self, difficulty: int) -> str:
        """예상 학습 시간 계산"""
        base_time = difficulty * 5  # 기본 5분씩
        return f"{base_time}-{base_time + 10}분"
    
    def _filter_available_content(self, user_id: str, level_content: Dict[str, Any]) -> Dict[str, Any]:
        """전제조건을 만족하는 콘텐츠만 필터링"""
        available = {}
        for content_id, content in level_content.items():
            if self._check_prerequisites(user_id, content_id):
                available[content_id] = content
        return available
    
    def _check_prerequisites(self, user_id: str, content_id: str) -> bool:
        """전제조건 확인"""
        # 현재 레벨의 콘텐츠 찾기
        for level_content in self.content_library.values():
            if content_id in level_content:
                prerequisites = level_content[content_id].get("prerequisites", [])
                for prereq in prerequisites:
                    if not self._is_content_mastered(user_id, prereq):
                        return False
                return True
        return True
    
    def _is_content_mastered(self, user_id: str, content_id: str) -> bool:
        """콘텐츠 숙달 여부 확인"""
        if user_id not in self.learners:
            return False
        
        learner = self.learners[user_id]
        performance = learner["performance"].get(content_id, [])
        
        if not performance:
            return False
        
        # 최근 3번의 시도에서 80% 이상 성공 시 숙달로 판단
        recent_attempts = performance[-3:]
        if len(recent_attempts) < 3:
            return False
        
        success_count = sum(1 for attempt in recent_attempts if attempt["correct"])
        return success_count >= 2  # 3번 중 2번 이상 성공
    
    def _generate_learning_path(self, user_id: str, content_id: str) -> List[str]:
        """개인화된 학습 경로 생성"""
        # 현재 콘텐츠 찾기
        current_content = None
        for level_content in self.content_library.values():
            if content_id in level_content:
                current_content = level_content[content_id]
                break
        
        if not current_content:
            return []
        
        path = []
        # 학습 목표 기반 단계적 경로 생성
        objectives = current_content.get("learning_objectives", [])
        for i, objective in enumerate(objectives, 1):
            path.append(f"단계 {i}: {objective}")
        
        # 실제 예제와 연습 단계 추가
        path.append("단계 {}: 실제 예제로 개념 적용해보기".format(len(path) + 1))
        path.append("단계 {}: 연습 문제로 이해도 확인하기".format(len(path) + 1))
        
        return path
    
    def _generate_study_tips(self, content: Dict[str, Any]) -> List[str]:
        """학습 팁 생성"""
        tips = []
        
        # 난이도별 맞춤 팁
        difficulty = content.get("difficulty", 5)
        if difficulty <= 3:
            tips.extend([
                "기본 개념부터 차근차근 이해해보세요",
                "예제를 따라하며 직접 계산해보세요",
                "개념을 자신만의 언어로 설명해보세요"
            ])
        elif difficulty <= 6:
            tips.extend([
                "전제조건 개념들을 먼저 복습하세요",
                "단계별로 나누어 접근해보세요",
                "실생활 예시와 연결해서 이해해보세요"
            ])
        else:
            tips.extend([
                "관련 이론의 배경과 원리를 깊이 이해하세요",
                "다양한 응용 사례를 찾아보세요",
                "개념 간의 연결고리를 파악해보세요"
            ])
        
        # 카테고리별 특화 팁
        category = content.get("category", "")
        if "statistics" in category:
            tips.append("통계적 사고를 위해 '왜?'라는 질문을 많이 해보세요")
        elif "probability" in category:
            tips.append("확률 문제는 경우의 수를 체계적으로 세어보세요")
        elif "analysis" in category:
            tips.append("분석 결과의 실제 의미를 해석하는 연습을 해보세요")
        
        return tips
    
    def _suggest_next_topics(self, user_id: str, current_content_id: str) -> List[str]:
        """다음 학습 주제 제안"""
        # 현재 콘텐츠의 카테고리와 난이도 파악
        current_content = None
        current_level = None
        
        for level, level_content in self.content_library.items():
            if current_content_id in level_content:
                current_content = level_content[current_content_id]
                current_level = level
                break
        
        if not current_content:
            return []
        
        next_topics = []
        current_category = current_content.get("category", "")
        current_difficulty = current_content.get("difficulty", 5)
        
        # 같은 레벨에서 연관된 주제들
        if current_level:
            level_content = self.content_library[current_level]
            for content_id, content in level_content.items():
                if (content_id != current_content_id and 
                    content.get("category") == current_category and
                    abs(content.get("difficulty", 5) - current_difficulty) <= 2):
                    next_topics.append(content["title"])
        
        # 다음 레벨의 관련 주제들
        level_progression = {
            "foundation": "developing",
            "developing": "proficient", 
            "proficient": "advanced"
        }
        
        if current_level in level_progression:
            next_level = level_progression[current_level]
            if next_level in self.content_library:
                next_level_content = self.content_library[next_level]
                for content_id, content in next_level_content.items():
                    if current_content_id in content.get("prerequisites", []):
                        next_topics.append(f"[다음 단계] {content['title']}")
        
        return next_topics[:3]  # 최대 3개만 반환
    
    def submit_answer(self, user_id: str, content_id: str, question_idx: int, 
                     selected_option: int) -> Dict[str, Any]:
        """답안 제출 및 채점"""
        if user_id not in self.learners:
            return {"error": "학습자를 찾을 수 없습니다"}
        
        learner = self.learners[user_id]
        current_level = learner["current_level"]
        
        # 콘텐츠와 문제 찾기
        content = None
        for level_name, level_content in self.content_library.items():
            if content_id in level_content:
                content = level_content[content_id]
                break
        
        if not content or question_idx >= len(content["questions"]):
            return {"error": "문제를 찾을 수 없습니다"}
        
        question = content["questions"][question_idx]
        is_correct = selected_option == question["correct"]
        
        # 성과 기록
        if content_id not in learner["performance"]:
            learner["performance"][content_id] = []
        
        learner["performance"][content_id].append({
            "question_idx": question_idx,
            "correct": is_correct,
            "timestamp": datetime.now().isoformat()
        })
        
        # 적응형 설정 업데이트
        self._update_adaptive_settings(user_id, is_correct)
        
        # 상호작용 로그 기록
        self.interaction_log.append({
            "user_id": user_id,
            "content_id": content_id,
            "question_idx": question_idx,
            "correct": is_correct,
            "timestamp": datetime.now().isoformat()
        })
        
        result = {
            "correct": is_correct,
            "explanation": question["explanation"],
            "your_answer": question["options"][selected_option],
            "correct_answer": question["options"][question["correct"]],
            "performance_summary": self._get_performance_summary(user_id, content_id)
        }
        
        # 레벨업 체크
        if self._check_level_up(user_id):
            result["level_up"] = True
            result["new_level"] = learner["current_level"]
        
        return result
    
    def _update_adaptive_settings(self, user_id: str, is_correct: bool):
        """적응형 설정 업데이트"""
        learner = self.learners[user_id]
        
        # 성공률 업데이트 (이동평균)
        current_rate = learner["adaptive_settings"]["success_rate"]
        learning_rate = 0.1
        new_rate = current_rate + learning_rate * (1.0 if is_correct else 0.0 - current_rate)
        learner["adaptive_settings"]["success_rate"] = max(0.0, min(1.0, new_rate))
        
        # 난이도 선호도 조정
        if is_correct and current_rate > 0.8:
            learner["adaptive_settings"]["difficulty_preference"] += 0.1
        elif not is_correct and current_rate < 0.4:
            learner["adaptive_settings"]["difficulty_preference"] -= 0.1
        
        learner["adaptive_settings"]["difficulty_preference"] = max(1, min(10, 
            learner["adaptive_settings"]["difficulty_preference"]))
    
    def _get_performance_summary(self, user_id: str, content_id: str) -> Dict[str, Any]:
        """성과 요약 생성"""
        learner = self.learners[user_id]
        performance = learner["performance"].get(content_id, [])
        
        if not performance:
            return {"attempts": 0, "success_rate": 0}
        
        correct_count = sum(1 for p in performance if p["correct"])
        total_count = len(performance)
        
        return {
            "attempts": total_count,
            "correct": correct_count,
            "success_rate": round(correct_count / total_count * 100, 1),
            "last_attempt": performance[-1]["timestamp"]
        }
    
    def _check_level_up(self, user_id: str) -> bool:
        """레벨업 조건 확인"""
        learner = self.learners[user_id]
        current_level = learner["current_level"]
        
        # 현재 레벨의 모든 콘텐츠에서 80% 이상 성공률 달성 시 레벨업
        level_content = self.content_library.get(current_level, {})
        
        for content_id in level_content.keys():
            performance = learner["performance"].get(content_id, [])
            if not performance:
                return False
            
            correct_count = sum(1 for p in performance if p["correct"])
            success_rate = correct_count / len(performance)
            
            if success_rate < 0.8:
                return False
        
        # 모든 조건 만족 시 레벨업
        level_progression = {
            "foundation": "developing",
            "developing": "proficient", 
            "proficient": "advanced"
        }
        
        if current_level in level_progression:
            learner["current_level"] = level_progression[current_level]
            return True
        
        return False
    
    def get_learning_analytics(self, user_id: str) -> Dict[str, Any]:
        """학습 분석 데이터 제공"""
        if user_id not in self.learners:
            return {"error": "학습자를 찾을 수 없습니다"}
        
        learner = self.learners[user_id]
        
        # 전체 성과 분석
        all_performance = []
        for content_performances in learner["performance"].values():
            all_performance.extend(content_performances)
        
        if not all_performance:
            return {"message": "아직 학습 기록이 없습니다"}
        
        total_attempts = len(all_performance)
        correct_attempts = sum(1 for p in all_performance if p["correct"])
        
        # 학습 패턴 분석
        recent_performance = all_performance[-10:] if len(all_performance) >= 10 else all_performance
        recent_success_rate = sum(1 for p in recent_performance if p["correct"]) / len(recent_performance)
        
        # 학습 상태 판단
        if recent_success_rate < 0.3:
            learning_state = "어려움을 겪고 있음"
            recommendation = "기초 내용을 다시 복습하거나 도움을 요청하세요"
        elif recent_success_rate > 0.8:
            learning_state = "매우 잘하고 있음"
            recommendation = "더 도전적인 내용으로 진행하세요"
        else:
            learning_state = "정상적으로 진행 중"
            recommendation = "현재 속도를 유지하며 꾸준히 학습하세요"
        
        return {
            "overall_stats": {
                "total_attempts": total_attempts,
                "correct_attempts": correct_attempts,
                "success_rate": round(correct_attempts / total_attempts * 100, 1),
                "current_level": learner["current_level"]
            },
            "recent_performance": {
                "last_10_attempts": len(recent_performance),
                "recent_success_rate": round(recent_success_rate * 100, 1)
            },
            "learning_state": learning_state,
            "recommendation": recommendation,
            "adaptive_settings": learner["adaptive_settings"]
        }
    
    def get_system_stats(self) -> Dict[str, Any]:
        """시스템 전체 통계"""
        total_learners = len(self.learners)
        total_interactions = len(self.interaction_log)
        
        if total_learners == 0:
            return {"message": "등록된 학습자가 없습니다"}
        
        # 레벨별 분포
        level_distribution = {}
        for learner in self.learners.values():
            level = learner["current_level"]
            level_distribution[level] = level_distribution.get(level, 0) + 1
        
        # 전체 성공률
        correct_interactions = sum(1 for log in self.interaction_log if log["correct"])
        overall_success_rate = (correct_interactions / total_interactions * 100) if total_interactions > 0 else 0
        
        return {
            "total_learners": total_learners,
            "total_interactions": total_interactions,
            "overall_success_rate": round(overall_success_rate, 1),
            "level_distribution": level_distribution,
            "content_library_size": sum(len(level) for level in self.content_library.values())
        }


def run_interactive_demo():
    """인터랙티브 데모 실행"""
    system = SimpleLearningSystem()
    
    print("=== 🎓 간단한 적응형 학습 시스템 데모 ===")
    print("의존성 없이 실제로 동작하는 학습 시스템입니다!\n")
    
    # 데모 학습자 등록
    demo_profile = {
        "name": "데모 학습자",
        "difficulty": 5,
        "pace": "medium",
        "goals": ["기초 통계 학습"]
    }
    
    result = system.register_learner("demo_user", demo_profile)
    print(f"✓ {result['message']}")
    
    while True:
        print("\n" + "="*50)
        print("1. 콘텐츠 학습하기")
        print("2. 문제 풀기")
        print("3. 시스템 통계 보기")
        print("4. 종료")
        
        choice = input("\n선택하세요 (1-4): ").strip()
        
        if choice == "1":
            content = system.get_personalized_content("demo_user")
            if "error" not in content:
                print(f"\n📚 학습 콘텐츠: {content['content']['title']}")
                print(f"📖 내용: {content['content']['content']}")
            else:
                print(f"❌ {content['error']}")
        
        elif choice == "2":
            content = system.get_personalized_content("demo_user")
            if "error" not in content:
                questions = content['content']['questions']
                for i, q in enumerate(questions):
                    print(f"\n❓ 문제 {i+1}: {q['q']}")
                    for j, option in enumerate(q['options']):
                        print(f"  {j+1}. {option}")
                    
                    while True:
                        try:
                            answer = int(input("답을 선택하세요 (1-4): ")) - 1
                            if 0 <= answer <= 3:
                                break
                            print("1-4 사이의 숫자를 입력하세요.")
                        except ValueError:
                            print("숫자를 입력하세요.")
                    
                    result = system.submit_answer("demo_user", content['content_id'], i, answer)
                    
                    if result['correct']:
                        print("✅ 정답입니다!")
                    else:
                        print("❌ 틀렸습니다.")
                        print(f"정답: {result['correct_answer']}")
                    
                    print(f"💬 해설: {result['explanation']}")
                    print(f"📊 이 콘텐츠 성과: {result['performance_summary']['success_rate']}%")
                    
                    if result.get('level_up'):
                        print(f"🎉 축하합니다! {result['new_level']} 레벨로 승급했습니다!")
        
        elif choice == "3":
            stats = system.get_system_stats()
            print(f"\n📊 시스템 통계:")
            print(f"전체 학습자: {stats['total_learners']}명")
            print(f"총 상호작용: {stats['total_interactions']}회")
            print(f"전체 성공률: {stats['overall_success_rate']}%")
            print(f"레벨별 분포: {stats['level_distribution']}")
        
        elif choice == "4":
            print("\n👋 학습 시스템을 종료합니다. 좋은 하루 되세요!")
            break
        
        else:
            print("❌ 잘못된 선택입니다. 1-4 사이의 숫자를 입력하세요.")


if __name__ == "__main__":
    run_interactive_demo()