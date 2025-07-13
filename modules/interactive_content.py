"""
상호작용형 콘텐츠 전달 시스템
- 멀티미디어 통합 학습 콘텐츠
- 실시간 상호작용 및 피드백
- 개인화된 학습 경로
- 게임화 요소 통합
"""

import json
import numpy as np
import matplotlib
matplotlib.use('Agg')  # GUI 백엔드 비활성화
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from io import BytesIO
import base64
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import uuid
from dataclasses import dataclass, asdict
from enum import Enum

class ContentType(Enum):
    """콘텐츠 유형"""
    TEXT = "text"
    VIDEO = "video"
    INTERACTIVE_SIMULATION = "interactive_simulation"
    QUIZ = "quiz"
    CODING_EXERCISE = "coding_exercise"
    CASE_STUDY = "case_study"
    GAMIFIED_CHALLENGE = "gamified_challenge"
    VIRTUAL_LAB = "virtual_lab"

class InteractionLevel(Enum):
    """상호작용 수준"""
    PASSIVE = 1      # 읽기만
    GUIDED = 2       # 가이드된 상호작용
    EXPLORATORY = 3  # 탐색적 상호작용
    CREATIVE = 4     # 창작적 상호작용

@dataclass
class MultimediaContent:
    """멀티미디어 콘텐츠"""
    id: str
    title: str
    content_type: ContentType
    interaction_level: InteractionLevel
    estimated_time: int  # 분
    difficulty_level: int  # 1-5
    learning_objectives: List[str]
    prerequisites: List[str]
    content_data: Dict[str, Any]
    metadata: Dict[str, Any]

class InteractiveContentEngine:
    """상호작용형 콘텐츠 엔진"""
    
    def __init__(self):
        self.content_library: Dict[str, MultimediaContent] = {}
        self.user_interactions: Dict[str, List[Dict]] = {}
        self.gamification_engine = GamificationEngine()
        self.simulation_engine = SimulationEngine()
        self._initialize_content_library()
    
    def _initialize_content_library(self):
        """콘텐츠 라이브러리 초기화"""
        self._create_interactive_statistics_content()
        self._create_simulation_content()
        self._create_gamified_content()
    
    def _create_interactive_statistics_content(self):
        """상호작용형 통계 콘텐츠 생성"""
        
        # 1. 분포 시각화 시뮬레이션
        distribution_sim = MultimediaContent(
            id="dist_simulation_001",
            title="확률분포 인터랙티브 시뮬레이션",
            content_type=ContentType.INTERACTIVE_SIMULATION,
            interaction_level=InteractionLevel.EXPLORATORY,
            estimated_time=15,
            difficulty_level=3,
            learning_objectives=[
                "정규분포의 특성 이해",
                "모수 변화가 분포에 미치는 영향 관찰",
                "중심극한정리 직관적 이해"
            ],
            prerequisites=["basic_probability", "descriptive_statistics"],
            content_data={
                "simulation_type": "probability_distributions",
                "parameters": {
                    "distributions": ["normal", "binomial", "poisson", "exponential"],
                    "interactive_params": ["mean", "std", "sample_size"],
                    "visualization_types": ["histogram", "pdf", "cdf"]
                },
                "interactive_elements": [
                    {
                        "type": "slider",
                        "parameter": "mean",
                        "range": [-5, 5],
                        "default": 0,
                        "step": 0.1
                    },
                    {
                        "type": "slider",
                        "parameter": "std",
                        "range": [0.1, 3],
                        "default": 1,
                        "step": 0.1
                    },
                    {
                        "type": "slider",
                        "parameter": "sample_size",
                        "range": [10, 1000],
                        "default": 100,
                        "step": 10
                    }
                ]
            },
            metadata={
                "tags": ["probability", "distributions", "simulation"],
                "created_at": datetime.now().isoformat(),
                "version": "1.0"
            }
        )
        self.content_library[distribution_sim.id] = distribution_sim
        
        # 2. 가설검정 가상 실험실
        hypothesis_lab = MultimediaContent(
            id="hypothesis_lab_001",
            title="가설검정 가상 실험실",
            content_type=ContentType.VIRTUAL_LAB,
            interaction_level=InteractionLevel.CREATIVE,
            estimated_time=25,
            difficulty_level=4,
            learning_objectives=[
                "가설검정의 전체 과정 경험",
                "Type I, Type II 오류 이해",
                "p-value의 의미 체험적 학습"
            ],
            prerequisites=["hypothesis_testing_basics", "statistical_inference"],
            content_data={
                "lab_type": "hypothesis_testing",
                "experiments": [
                    {
                        "name": "t-검정 실험",
                        "description": "두 그룹의 평균 차이 검정",
                        "steps": [
                            "가설 설정",
                            "데이터 수집",
                            "검정통계량 계산",
                            "p-value 계산",
                            "결론 도출"
                        ]
                    },
                    {
                        "name": "카이제곱 독립성 검정",
                        "description": "범주형 변수 간 독립성 검정",
                        "steps": [
                            "교차표 작성",
                            "기댓값 계산",
                            "카이제곱 통계량 계산",
                            "자유도 결정",
                            "결론 해석"
                        ]
                    }
                ],
                "interactive_tools": [
                    "data_generator",
                    "visualization_panel",
                    "calculation_assistant",
                    "interpretation_guide"
                ]
            },
            metadata={
                "tags": ["hypothesis_testing", "lab", "experiential_learning"],
                "difficulty_adaptable": True,
                "assessment_integrated": True
            }
        )
        self.content_library[hypothesis_lab.id] = hypothesis_lab
        
        # 3. 회귀분석 인터랙티브 튜토리얼
        regression_tutorial = MultimediaContent(
            id="regression_tutorial_001",
            title="회귀분석 마스터 클래스",
            content_type=ContentType.CODING_EXERCISE,
            interaction_level=InteractionLevel.GUIDED,
            estimated_time=30,
            difficulty_level=4,
            learning_objectives=[
                "선형회귀 모델 구축 및 해석",
                "잔차 분석을 통한 모델 진단",
                "다중공선성 문제 해결"
            ],
            prerequisites=["linear_algebra_basics", "statistics_intermediate"],
            content_data={
                "coding_language": "python",
                "libraries": ["pandas", "numpy", "scikit-learn", "matplotlib"],
                "exercises": [
                    {
                        "title": "단순선형회귀 구현",
                        "description": "최소제곱법을 이용한 회귀선 찾기",
                        "starter_code": """
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# 데이터 생성
np.random.seed(42)
X = np.random.randn(100, 1)
y = 2 * X.flatten() + 1 + np.random.randn(100) * 0.5

# TODO: 회귀모델을 훈련하고 시각화하세요
""",
                        "hints": [
                            "LinearRegression() 객체를 생성하세요",
                            "fit() 메서드로 모델을 훈련하세요",
                            "predict() 메서드로 예측값을 구하세요"
                        ],
                        "solution": """
# 모델 생성 및 훈련
model = LinearRegression()
model.fit(X, y)

# 예측
y_pred = model.predict(X)

# 시각화
plt.scatter(X, y, alpha=0.7, label='실제 데이터')
plt.plot(X, y_pred, color='red', label='회귀선')
plt.xlabel('X')
plt.ylabel('y')
plt.legend()
plt.title('단순선형회귀')
plt.show()

print(f'기울기: {model.coef_[0]:.2f}')
print(f'절편: {model.intercept_:.2f}')
"""
                    }
                ]
            },
            metadata={
                "tags": ["regression", "coding", "python", "scikit-learn"],
                "auto_grading": True,
                "code_execution": True
            }
        )
        self.content_library[regression_tutorial.id] = regression_tutorial
    
    def _create_simulation_content(self):
        """시뮬레이션 콘텐츠 생성"""
        
        # 중심극한정리 시뮬레이션
        clt_simulation = MultimediaContent(
            id="clt_simulation_001",
            title="중심극한정리 체험 시뮬레이션",
            content_type=ContentType.INTERACTIVE_SIMULATION,
            interaction_level=InteractionLevel.EXPLORATORY,
            estimated_time=20,
            difficulty_level=3,
            learning_objectives=[
                "중심극한정리의 직관적 이해",
                "표본크기가 표본평균 분포에 미치는 영향",
                "다양한 모집단 분포에서의 CLT 확인"
            ],
            prerequisites=["sampling", "probability_distributions"],
            content_data={
                "simulation_type": "central_limit_theorem",
                "population_distributions": [
                    {"name": "정규분포", "type": "normal", "params": {"mu": 0, "sigma": 1}},
                    {"name": "균등분포", "type": "uniform", "params": {"a": 0, "b": 1}},
                    {"name": "지수분포", "type": "exponential", "params": {"scale": 1}},
                    {"name": "베르누이분포", "type": "bernoulli", "params": {"p": 0.3}}
                ],
                "interactive_controls": {
                    "sample_sizes": [5, 10, 20, 50, 100, 500],
                    "num_samples": [100, 500, 1000, 5000],
                    "animation_speed": ["slow", "medium", "fast"]
                },
                "visualizations": [
                    "population_distribution",
                    "sampling_animation",
                    "sample_means_histogram",
                    "theoretical_normal_overlay"
                ]
            },
            metadata={
                "tags": ["central_limit_theorem", "sampling", "animation"],
                "interactive_features": ["real_time_plotting", "parameter_adjustment"]
            }
        )
        self.content_library[clt_simulation.id] = clt_simulation
    
    def _create_gamified_content(self):
        """게임화된 콘텐츠 생성"""
        
        # 통계 탐정 게임
        stats_detective = MultimediaContent(
            id="stats_detective_001",
            title="통계 탐정: 데이터 미스터리 해결",
            content_type=ContentType.GAMIFIED_CHALLENGE,
            interaction_level=InteractionLevel.CREATIVE,
            estimated_time=45,
            difficulty_level=4,
            learning_objectives=[
                "실제 데이터 분석 문제 해결",
                "통계적 추론을 통한 결론 도출",
                "데이터 시각화를 통한 패턴 발견"
            ],
            prerequisites=["descriptive_statistics", "data_visualization", "hypothesis_testing"],
            content_data={
                "game_type": "mystery_solving",
                "scenario": {
                    "title": "수상한 판매 데이터",
                    "description": "한 회사의 분기별 판매 데이터에서 이상한 패턴이 발견되었습니다. 당신은 통계 탐정이 되어 이 미스터리를 해결해야 합니다.",
                    "setting": "corporate_sales_analysis"
                },
                "missions": [
                    {
                        "id": "mission_1",
                        "title": "첫 번째 단서: 기술통계 분석",
                        "description": "판매 데이터의 기본 통계량을 계산하여 이상값을 찾아내세요.",
                        "tools": ["descriptive_stats", "boxplot", "histogram"],
                        "clues": ["outlier_detection", "distribution_analysis"],
                        "points": 100
                    },
                    {
                        "id": "mission_2", 
                        "title": "두 번째 단서: 시계열 패턴 분석",
                        "description": "시간에 따른 판매 트렌드를 분석하여 의심스러운 패턴을 찾으세요.",
                        "tools": ["time_series_plot", "trend_analysis", "seasonality_check"],
                        "clues": ["trend_break", "seasonal_anomaly"],
                        "points": 150
                    },
                    {
                        "id": "mission_3",
                        "title": "최종 미션: 가설검정으로 범인 찾기",
                        "description": "통계적 가설검정을 통해 데이터 조작의 증거를 찾아내세요.",
                        "tools": ["t_test", "chi_square_test", "correlation_analysis"],
                        "clues": ["statistical_significance", "effect_size"],
                        "points": 200
                    }
                ],
                "scoring": {
                    "max_points": 450,
                    "time_bonus": True,
                    "accuracy_bonus": True,
                    "creativity_bonus": True
                },
                "achievements": [
                    {"name": "데이터 탐정", "condition": "complete_all_missions"},
                    {"name": "스피드 러너", "condition": "complete_under_30_minutes"},
                    {"name": "완벽주의자", "condition": "100_percent_accuracy"}
                ]
            },
            metadata={
                "tags": ["gamification", "data_analysis", "mystery", "problem_solving"],
                "multiplayer": False,
                "adaptive_difficulty": True
            }
        )
        self.content_library[stats_detective.id] = stats_detective
    
    def generate_interactive_content(
        self, 
        content_id: str, 
        user_id: str,
        personalization_params: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """개인화된 상호작용 콘텐츠 생성"""
        
        if content_id not in self.content_library:
            return {"error": "콘텐츠를 찾을 수 없습니다"}
        
        content = self.content_library[content_id]
        
        # 사용자 맞춤형 콘텐츠 생성
        personalized_content = self._personalize_content(content, user_id, personalization_params)
        
        # 상호작용 요소 추가
        interactive_elements = self._generate_interactive_elements(content)
        
        # 실시간 피드백 시스템 설정
        feedback_system = self._setup_feedback_system(content, user_id)
        
        return {
            "content_id": content_id,
            "content": personalized_content,
            "interactive_elements": interactive_elements,
            "feedback_system": feedback_system,
            "session_id": str(uuid.uuid4()),
            "estimated_time": content.estimated_time,
            "learning_objectives": content.learning_objectives
        }
    
    def _personalize_content(
        self, 
        content: MultimediaContent, 
        user_id: str,
        personalization_params: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """콘텐츠 개인화"""
        
        # 기본 개인화 매개변수
        if not personalization_params:
            personalization_params = {
                "difficulty_preference": 3,
                "learning_style": "visual",
                "pace": "medium",
                "prior_knowledge": []
            }
        
        personalized = content.content_data.copy()
        
        # 난이도 조정
        if personalization_params.get("difficulty_preference"):
            difficulty_multiplier = personalization_params["difficulty_preference"] / content.difficulty_level
            personalized["adjusted_difficulty"] = difficulty_multiplier
        
        # 학습 스타일 반영
        learning_style = personalization_params.get("learning_style", "visual")
        if learning_style == "visual":
            personalized["emphasis"] = "visualizations"
        elif learning_style == "kinesthetic":
            personalized["emphasis"] = "interactive_exercises"
        elif learning_style == "auditory":
            personalized["emphasis"] = "explanations"
        
        # 속도 조정
        pace = personalization_params.get("pace", "medium")
        pace_multipliers = {"slow": 1.5, "medium": 1.0, "fast": 0.7}
        personalized["time_multiplier"] = pace_multipliers.get(pace, 1.0)
        
        return personalized
    
    def _generate_interactive_elements(self, content: MultimediaContent) -> List[Dict[str, Any]]:
        """상호작용 요소 생성"""
        
        elements = []
        
        if content.content_type == ContentType.INTERACTIVE_SIMULATION:
            elements.extend(self._create_simulation_elements(content))
        elif content.content_type == ContentType.VIRTUAL_LAB:
            elements.extend(self._create_lab_elements(content))
        elif content.content_type == ContentType.CODING_EXERCISE:
            elements.extend(self._create_coding_elements(content))
        elif content.content_type == ContentType.GAMIFIED_CHALLENGE:
            elements.extend(self._create_game_elements(content))
        
        # 공통 상호작용 요소
        elements.extend([
            {
                "type": "progress_tracker",
                "description": "학습 진도 추적",
                "real_time": True
            },
            {
                "type": "hint_system",
                "description": "단계별 힌트 제공",
                "adaptive": True
            },
            {
                "type": "peer_comparison",
                "description": "다른 학습자와 성과 비교",
                "anonymous": True
            }
        ])
        
        return elements
    
    def _create_simulation_elements(self, content: MultimediaContent) -> List[Dict[str, Any]]:
        """시뮬레이션 요소 생성"""
        return [
            {
                "type": "parameter_sliders",
                "description": "실시간 매개변수 조정",
                "parameters": content.content_data.get("interactive_elements", [])
            },
            {
                "type": "real_time_visualization",
                "description": "실시간 그래프 업데이트",
                "chart_types": ["line", "histogram", "scatter"]
            },
            {
                "type": "experiment_designer",
                "description": "사용자 정의 실험 설계",
                "customizable": True
            }
        ]
    
    def _create_lab_elements(self, content: MultimediaContent) -> List[Dict[str, Any]]:
        """가상 실험실 요소 생성"""
        return [
            {
                "type": "data_generator",
                "description": "실험 데이터 생성 도구",
                "distributions": ["normal", "uniform", "exponential"]
            },
            {
                "type": "statistical_calculator",
                "description": "통계량 계산 도구",
                "functions": ["mean", "std", "correlation", "regression"]
            },
            {
                "type": "hypothesis_tester",
                "description": "가설검정 도구",
                "tests": ["t_test", "chi_square", "anova"]
            }
        ]
    
    def _create_coding_elements(self, content: MultimediaContent) -> List[Dict[str, Any]]:
        """코딩 연습 요소 생성"""
        return [
            {
                "type": "code_editor",
                "description": "실시간 코드 편집기",
                "language": content.content_data.get("coding_language", "python"),
                "syntax_highlighting": True,
                "auto_completion": True
            },
            {
                "type": "code_execution",
                "description": "코드 실행 및 결과 확인",
                "sandbox": True,
                "real_time": True
            },
            {
                "type": "auto_grader",
                "description": "자동 채점 시스템",
                "partial_credit": True,
                "detailed_feedback": True
            }
        ]
    
    def _create_game_elements(self, content: MultimediaContent) -> List[Dict[str, Any]]:
        """게임화 요소 생성"""
        return [
            {
                "type": "mission_tracker",
                "description": "미션 진행 상황 추적",
                "visual_progress": True
            },
            {
                "type": "point_system",
                "description": "포인트 및 보상 시스템",
                "achievements": True,
                "leaderboard": True
            },
            {
                "type": "narrative_engine",
                "description": "스토리텔링 요소",
                "branching_story": True,
                "character_interaction": True
            }
        ]
    
    def _setup_feedback_system(self, content: MultimediaContent, user_id: str) -> Dict[str, Any]:
        """실시간 피드백 시스템 설정"""
        return {
            "real_time_feedback": True,
            "feedback_types": [
                "immediate_correctness",
                "explanatory_feedback",
                "adaptive_hints",
                "progress_feedback",
                "motivational_messages"
            ],
            "personalization": {
                "user_id": user_id,
                "learning_style_adapted": True,
                "difficulty_adjusted": True
            },
            "analytics": {
                "interaction_tracking": True,
                "performance_analysis": True,
                "engagement_metrics": True
            }
        }
    
    def process_user_interaction(
        self, 
        session_id: str, 
        user_id: str,
        interaction_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """사용자 상호작용 처리"""
        
        # 상호작용 데이터 저장
        if user_id not in self.user_interactions:
            self.user_interactions[user_id] = []
        
        interaction_record = {
            "session_id": session_id,
            "timestamp": datetime.now().isoformat(),
            "interaction_type": interaction_data.get("type"),
            "data": interaction_data,
            "response_time": interaction_data.get("response_time", 0)
        }
        
        self.user_interactions[user_id].append(interaction_record)
        
        # 실시간 피드백 생성
        feedback = self._generate_real_time_feedback(user_id, interaction_data)
        
        # 적응형 조정
        adaptations = self._calculate_adaptations(user_id, interaction_data)
        
        return {
            "feedback": feedback,
            "adaptations": adaptations,
            "next_suggestions": self._get_next_suggestions(user_id),
            "engagement_score": self._calculate_engagement_score(user_id)
        }
    
    def _generate_real_time_feedback(self, user_id: str, interaction_data: Dict) -> Dict[str, Any]:
        """실시간 피드백 생성"""
        
        interaction_type = interaction_data.get("type")
        is_correct = interaction_data.get("is_correct", None)
        
        feedback = {
            "type": "immediate",
            "timestamp": datetime.now().isoformat()
        }
        
        if interaction_type == "quiz_answer":
            if is_correct:
                feedback.update({
                    "message": "정답입니다! 훌륭해요! 🎉",
                    "tone": "positive",
                    "next_action": "continue"
                })
            else:
                feedback.update({
                    "message": "다시 한번 생각해보세요. 힌트가 필요하신가요?",
                    "tone": "encouraging",
                    "next_action": "retry",
                    "hint_available": True
                })
        
        elif interaction_type == "simulation_parameter":
            feedback.update({
                "message": f"매개변수 변경이 결과에 어떤 영향을 주는지 관찰해보세요",
                "tone": "exploratory",
                "next_action": "observe"
            })
        
        elif interaction_type == "code_execution":
            if interaction_data.get("execution_success"):
                feedback.update({
                    "message": "코드가 성공적으로 실행되었습니다! 결과를 분석해보세요",
                    "tone": "positive",
                    "next_action": "analyze"
                })
            else:
                feedback.update({
                    "message": "코드에 오류가 있습니다. 디버깅 도움이 필요하신가요?",
                    "tone": "supportive",
                    "next_action": "debug",
                    "debugging_help": True
                })
        
        return feedback
    
    def _calculate_adaptations(self, user_id: str, interaction_data: Dict) -> Dict[str, Any]:
        """적응형 조정 계산"""
        
        user_history = self.user_interactions.get(user_id, [])
        recent_interactions = user_history[-10:]  # 최근 10개 상호작용
        
        # 성과 분석
        correct_rate = sum(1 for i in recent_interactions 
                          if i.get("data", {}).get("is_correct")) / max(len(recent_interactions), 1)
        
        avg_response_time = np.mean([i.get("data", {}).get("response_time", 30) 
                                   for i in recent_interactions]) if recent_interactions else 30
        
        adaptations = {}
        
        # 난이도 조정
        if correct_rate > 0.8:
            adaptations["difficulty"] = "increase"
            adaptations["reason"] = "높은 정답률로 인한 난이도 상향"
        elif correct_rate < 0.4:
            adaptations["difficulty"] = "decrease" 
            adaptations["reason"] = "낮은 정답률로 인한 난이도 하향"
        
        # 속도 조정
        if avg_response_time > 60:
            adaptations["pace"] = "slower"
            adaptations["content_amount"] = "reduce"
        elif avg_response_time < 10:
            adaptations["pace"] = "faster"
            adaptations["content_amount"] = "increase"
        
        # 개입 수준 조정
        if correct_rate < 0.5:
            adaptations["intervention"] = "increase_guidance"
            adaptations["hint_frequency"] = "more_frequent"
        
        return adaptations
    
    def _get_next_suggestions(self, user_id: str) -> List[Dict[str, Any]]:
        """다음 학습 제안"""
        
        # 사용자 성과 기반 추천
        suggestions = [
            {
                "type": "content",
                "title": "회귀분석 심화",
                "reason": "현재 진도와 연계된 다음 단계",
                "estimated_time": 20,
                "difficulty": 4
            },
            {
                "type": "practice",
                "title": "추가 연습 문제",
                "reason": "개념 정착을 위한 반복 학습",
                "estimated_time": 15,
                "difficulty": 3
            },
            {
                "type": "review",
                "title": "이전 개념 복습",
                "reason": "기초 개념 보강 필요",
                "estimated_time": 10,
                "difficulty": 2
            }
        ]
        
        return suggestions
    
    def _calculate_engagement_score(self, user_id: str) -> float:
        """참여도 점수 계산"""
        
        user_history = self.user_interactions.get(user_id, [])
        
        if not user_history:
            return 0.5
        
        # 최근 세션 분석
        recent_session = [i for i in user_history[-20:]]
        
        # 참여도 지표
        interaction_variety = len(set(i.get("interaction_type") for i in recent_session))
        session_duration = len(recent_session)
        response_quality = sum(1 for i in recent_session 
                             if i.get("data", {}).get("is_correct")) / max(len(recent_session), 1)
        
        # 가중 평균으로 참여도 계산
        engagement = (
            0.3 * min(interaction_variety / 5, 1.0) +  # 상호작용 다양성
            0.3 * min(session_duration / 20, 1.0) +   # 세션 지속성
            0.4 * response_quality                     # 응답 품질
        )
        
        return min(max(engagement, 0.0), 1.0)

class GamificationEngine:
    """게임화 엔진"""
    
    def __init__(self):
        self.user_profiles = {}
        self.achievements = self._define_achievements()
        self.leaderboards = {}
    
    def _define_achievements(self) -> Dict[str, Dict]:
        """성취 시스템 정의"""
        return {
            "first_lesson": {
                "name": "첫 걸음",
                "description": "첫 번째 학습 완료",
                "icon": "🎯",
                "points": 50
            },
            "streak_7": {
                "name": "일주일 챌린지",
                "description": "7일 연속 학습",
                "icon": "🔥",
                "points": 200
            },
            "perfect_score": {
                "name": "완벽주의자",
                "description": "100% 점수 달성",
                "icon": "⭐",
                "points": 100
            },
            "speed_learner": {
                "name": "스피드 러너",
                "description": "평균보다 2배 빠른 완료",
                "icon": "⚡",
                "points": 150
            },
            "helper": {
                "name": "도움의 손길",
                "description": "다른 학습자 도움",
                "icon": "🤝",
                "points": 300
            }
        }
    
    def award_points(self, user_id: str, points: int, reason: str) -> Dict:
        """포인트 지급"""
        if user_id not in self.user_profiles:
            self.user_profiles[user_id] = {
                "total_points": 0,
                "level": 1,
                "achievements": [],
                "streak": 0
            }
        
        profile = self.user_profiles[user_id]
        profile["total_points"] += points
        
        # 레벨 계산
        new_level = 1 + profile["total_points"] // 1000
        level_up = new_level > profile["level"]
        profile["level"] = new_level
        
        return {
            "points_awarded": points,
            "total_points": profile["total_points"],
            "current_level": profile["level"],
            "level_up": level_up,
            "reason": reason
        }

class SimulationEngine:
    """시뮬레이션 엔진"""
    
    def __init__(self):
        plt.style.use('default')
    
    def create_distribution_simulation(self, dist_type: str, params: Dict) -> str:
        """분포 시뮬레이션 생성"""
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # 매개변수 설정
        if dist_type == "normal":
            mu = params.get("mean", 0)
            sigma = params.get("std", 1)
            x = np.linspace(mu - 4*sigma, mu + 4*sigma, 1000)
            y = (1/(sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mu) / sigma) ** 2)
            
            ax1.plot(x, y, 'b-', linewidth=2, label=f'정규분포 (μ={mu}, σ={sigma})')
            ax1.fill_between(x, y, alpha=0.3)
            ax1.set_title('확률밀도함수')
            
            # 샘플 생성 및 히스토그램
            sample_size = params.get("sample_size", 1000)
            samples = np.random.normal(mu, sigma, sample_size)
            ax2.hist(samples, bins=30, density=True, alpha=0.7, color='skyblue', edgecolor='black')
            ax2.plot(x, y, 'r-', linewidth=2, label='이론적 분포')
            ax2.set_title(f'샘플 히스토그램 (n={sample_size})')
            ax2.legend()
        
        ax1.grid(True, alpha=0.3)
        ax2.grid(True, alpha=0.3)
        plt.tight_layout()
        
        # 이미지를 base64로 인코딩
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        
        return image_base64
    
    def create_hypothesis_testing_simulation(self, test_type: str, data: Dict) -> Dict:
        """가설검정 시뮬레이션"""
        
        if test_type == "t_test":
            group1 = np.array(data.get("group1", []))
            group2 = np.array(data.get("group2", []))
            
            # t-검정 수행
            from scipy.stats import ttest_ind
            t_stat, p_value = ttest_ind(group1, group2)
            
            # 시각화
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
            
            # 박스플롯
            ax1.boxplot([group1, group2], labels=['그룹 1', '그룹 2'])
            ax1.set_title('그룹별 데이터 분포')
            ax1.grid(True, alpha=0.3)
            
            # t-분포와 검정통계량
            df = len(group1) + len(group2) - 2
            x = np.linspace(-4, 4, 1000)
            from scipy.stats import t
            y = t.pdf(x, df)
            
            ax2.plot(x, y, 'b-', linewidth=2, label='t-분포')
            ax2.axvline(t_stat, color='red', linestyle='--', linewidth=2, label=f't-통계량 = {t_stat:.3f}')
            ax2.axvline(-t_stat, color='red', linestyle='--', linewidth=2)
            ax2.fill_between(x[x >= abs(t_stat)], y[x >= abs(t_stat)], alpha=0.3, color='red', label=f'p-value = {p_value:.4f}')
            ax2.fill_between(x[x <= -abs(t_stat)], y[x <= -abs(t_stat)], alpha=0.3, color='red')
            ax2.set_title('t-검정 결과')
            ax2.legend()
            ax2.grid(True, alpha=0.3)
            
            plt.tight_layout()
            
            # 이미지 인코딩
            buffer = BytesIO()
            plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.getvalue()).decode()
            plt.close()
            
            return {
                "image": image_base64,
                "statistics": {
                    "t_statistic": t_stat,
                    "p_value": p_value,
                    "degrees_of_freedom": df,
                    "significant": p_value < 0.05
                },
                "interpretation": self._interpret_t_test(t_stat, p_value)
            }
    
    def _interpret_t_test(self, t_stat: float, p_value: float) -> str:
        """t-검정 결과 해석"""
        alpha = 0.05
        
        if p_value < alpha:
            return f"p-value ({p_value:.4f}) < α ({alpha})이므로 귀무가설을 기각합니다. 두 그룹 간에 통계적으로 유의한 차이가 있습니다."
        else:
            return f"p-value ({p_value:.4f}) ≥ α ({alpha})이므로 귀무가설을 기각할 수 없습니다. 두 그룹 간에 통계적으로 유의한 차이가 없습니다."

# 전역 인스턴스
interactive_content_engine = InteractiveContentEngine()