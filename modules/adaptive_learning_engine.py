"""
적응형 학습 엔진
- 개인별 학습 패턴 분석
- 실시간 난이도 조정
- 개인화된 콘텐츠 추천
- 학습 분석 및 예측
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from enum import Enum
import json
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import pickle
import warnings
warnings.filterwarnings('ignore')


class LearningState(Enum):
    """학습 상태"""
    STRUGGLING = "struggling"
    PROGRESSING = "progressing"
    MASTERED = "mastered"
    BORED = "bored"


class InteractionType(Enum):
    """상호작용 유형"""
    CONTENT_VIEW = "content_view"
    EXERCISE_ATTEMPT = "exercise_attempt"
    ASSESSMENT_SUBMIT = "assessment_submit"
    HELP_REQUEST = "help_request"
    HINT_REQUEST = "hint_request"
    SKIP_CONTENT = "skip_content"
    REPEAT_CONTENT = "repeat_content"


@dataclass
class LearningInteraction:
    """학습 상호작용 데이터"""
    user_id: str
    timestamp: datetime
    interaction_type: InteractionType
    content_id: str
    duration: int  # seconds
    success: Optional[bool]
    difficulty_level: int  # 1-10
    hint_used: bool = False
    attempts: int = 1
    confidence_level: Optional[int] = None  # 1-5


@dataclass
class LearnerProfile:
    """학습자 프로필"""
    user_id: str
    learning_style: str
    prior_knowledge_level: int  # 1-10
    learning_pace: str  # slow, medium, fast
    preferred_difficulty: int  # 1-10
    motivation_level: int  # 1-10
    time_availability: int  # hours per week
    goals: List[str]
    strengths: List[str]
    weaknesses: List[str]
    last_activity: datetime


@dataclass
class ContentRecommendation:
    """콘텐츠 추천"""
    content_id: str
    recommendation_score: float
    reasoning: str
    difficulty_adjustment: int
    estimated_time: int
    success_probability: float


class AdaptiveLearningEngine:
    """적응형 학습 엔진 - ML 강화 버전"""
    
    def __init__(self):
        self.learner_profiles: Dict[str, LearnerProfile] = {}
        self.interaction_history: List[LearningInteraction] = []
        self.content_difficulty_map: Dict[str, int] = {}
        self.learning_objectives_map: Dict[str, List[str]] = {}
        self.adaptation_parameters = self._initialize_adaptation_parameters()
        
        # ML 모델들
        self.success_predictor = None
        self.difficulty_predictor = None
        self.engagement_predictor = None
        self.scaler = StandardScaler()
        
        # 모델 성능 추적
        self.model_performance = {
            'success_predictor': {'accuracy': 0.0, 'last_trained': None},
            'difficulty_predictor': {'accuracy': 0.0, 'last_trained': None},
            'engagement_predictor': {'accuracy': 0.0, 'last_trained': None}
        }
        
        self._initialize_ml_models()
    
    def _initialize_adaptation_parameters(self) -> Dict[str, Any]:
        """적응 매개변수 초기화"""
        return {
            "difficulty_adjustment_threshold": 0.6,  # 성공률 임계값
            "boredom_detection_threshold": 0.9,     # 지루함 감지 임계값
            "struggle_detection_threshold": 0.3,    # 어려움 감지 임계값
            "mastery_threshold": 0.85,              # 숙달 임계값
            "confidence_weight": 0.3,               # 신뢰도 가중치
            "time_weight": 0.2,                     # 시간 가중치
            "attempt_weight": 0.5,                  # 시도 횟수 가중치
            "recent_interaction_window": 10,        # 최근 상호작용 윈도우
            "learning_rate_alpha": 0.1,             # 학습률
            "forgetting_factor": 0.95,              # 망각 계수
            "ml_retrain_threshold": 100,            # ML 모델 재훈련 임계값
            "feature_importance_threshold": 0.05,   # 특성 중요도 임계값
            "ensemble_weights": [0.4, 0.3, 0.3],   # 앙상블 가중치
            "temporal_decay_factor": 0.95           # 시간적 감쇠 계수
        }
    
    def _initialize_ml_models(self):
        """ML 모델 초기화"""
        try:
            # 저장된 모델 로드 시도
            self._load_models()
        except FileNotFoundError:
            # 새 모델 생성
            self.success_predictor = RandomForestClassifier(
                n_estimators=100, random_state=42, max_depth=10
            )
            self.difficulty_predictor = LogisticRegression(
                random_state=42, max_iter=1000
            )
            self.engagement_predictor = RandomForestClassifier(
                n_estimators=50, random_state=42, max_depth=8
            )
    
    def _load_models(self):
        """저장된 모델 로드"""
        with open('models/success_predictor.pkl', 'rb') as f:
            self.success_predictor = pickle.load(f)
        with open('models/difficulty_predictor.pkl', 'rb') as f:
            self.difficulty_predictor = pickle.load(f)
        with open('models/engagement_predictor.pkl', 'rb') as f:
            self.engagement_predictor = pickle.load(f)
        with open('models/scaler.pkl', 'rb') as f:
            self.scaler = pickle.load(f)
    
    def _save_models(self):
        """모델 저장"""
        import os
        os.makedirs('models', exist_ok=True)
        
        with open('models/success_predictor.pkl', 'wb') as f:
            pickle.dump(self.success_predictor, f)
        with open('models/difficulty_predictor.pkl', 'wb') as f:
            pickle.dump(self.difficulty_predictor, f)
        with open('models/engagement_predictor.pkl', 'wb') as f:
            pickle.dump(self.engagement_predictor, f)
        with open('models/scaler.pkl', 'wb') as f:
            pickle.dump(self.scaler, f)
    
    def track_interaction(self, interaction: LearningInteraction):
        """학습 상호작용 추적"""
        self.interaction_history.append(interaction)
        
        # 학습자 프로필 업데이트
        if interaction.user_id in self.learner_profiles:
            self._update_learner_profile(interaction)
        else:
            self._create_initial_profile(interaction)
        
        # 실시간 적응 수행
        self._perform_real_time_adaptation(interaction)
    
    def _update_learner_profile(self, interaction: LearningInteraction):
        """학습자 프로필 업데이트"""
        profile = self.learner_profiles[interaction.user_id]
        profile.last_activity = interaction.timestamp
        
        # 학습 페이스 업데이트
        self._update_learning_pace(profile, interaction)
        
        # 선호 난이도 업데이트
        self._update_preferred_difficulty(profile, interaction)
        
        # 강약점 분석 업데이트
        self._update_strengths_weaknesses(profile, interaction)
    
    def _create_initial_profile(self, interaction: LearningInteraction):
        """초기 학습자 프로필 생성"""
        profile = LearnerProfile(
            user_id=interaction.user_id,
            learning_style="visual",  # 기본값, 추후 분석으로 업데이트
            prior_knowledge_level=5,  # 중간값으로 시작
            learning_pace="medium",
            preferred_difficulty=5,
            motivation_level=7,
            time_availability=5,
            goals=[],
            strengths=[],
            weaknesses=[],
            last_activity=interaction.timestamp
        )
        self.learner_profiles[interaction.user_id] = profile
    
    def _update_learning_pace(self, profile: LearnerProfile, interaction: LearningInteraction):
        """학습 페이스 업데이트"""
        recent_interactions = self._get_recent_interactions(
            interaction.user_id, self.adaptation_parameters["recent_interaction_window"]
        )
        
        avg_duration = np.mean([i.duration for i in recent_interactions])
        expected_duration = self._get_expected_duration(interaction.content_id)
        
        pace_ratio = avg_duration / expected_duration if expected_duration > 0 else 1.0
        
        if pace_ratio > 1.3:
            profile.learning_pace = "slow"
        elif pace_ratio < 0.7:
            profile.learning_pace = "fast"
        else:
            profile.learning_pace = "medium"
    
    def _update_preferred_difficulty(self, profile: LearnerProfile, interaction: LearningInteraction):
        """선호 난이도 업데이트"""
        if interaction.success is not None:
            current_success_rate = self._calculate_success_rate(interaction.user_id)
            
            # 성공률에 따른 난이도 조정
            if current_success_rate > self.adaptation_parameters["boredom_detection_threshold"]:
                profile.preferred_difficulty = min(10, profile.preferred_difficulty + 1)
            elif current_success_rate < self.adaptation_parameters["struggle_detection_threshold"]:
                profile.preferred_difficulty = max(1, profile.preferred_difficulty - 1)
    
    def _update_strengths_weaknesses(self, profile: LearnerProfile, interaction: LearningInteraction):
        """강약점 분석 업데이트"""
        content_topic = self._get_content_topic(interaction.content_id)
        
        if interaction.success is not None:
            topic_success_rate = self._calculate_topic_success_rate(
                interaction.user_id, content_topic
            )
            
            if topic_success_rate > 0.8 and content_topic not in profile.strengths:
                profile.strengths.append(content_topic)
                if content_topic in profile.weaknesses:
                    profile.weaknesses.remove(content_topic)
            elif topic_success_rate < 0.4 and content_topic not in profile.weaknesses:
                profile.weaknesses.append(content_topic)
                if content_topic in profile.strengths:
                    profile.strengths.remove(content_topic)
    
    def _perform_real_time_adaptation(self, interaction: LearningInteraction):
        """실시간 적응 수행"""
        learning_state = self._detect_learning_state(interaction.user_id)
        
        adaptation_actions = {
            LearningState.STRUGGLING: self._handle_struggling_learner,
            LearningState.BORED: self._handle_bored_learner,
            LearningState.PROGRESSING: self._handle_progressing_learner,
            LearningState.MASTERED: self._handle_mastered_learner
        }
        
        if learning_state in adaptation_actions:
            adaptation_actions[learning_state](interaction.user_id)
    
    def _detect_learning_state(self, user_id: str) -> LearningState:
        """학습 상태 감지"""
        recent_interactions = self._get_recent_interactions(user_id, 5)
        
        if not recent_interactions:
            return LearningState.PROGRESSING
        
        success_rate = np.mean([i.success for i in recent_interactions if i.success is not None])
        avg_attempts = np.mean([i.attempts for i in recent_interactions])
        hint_usage_rate = np.mean([i.hint_used for i in recent_interactions])
        
        # 학습 상태 판단 로직
        if success_rate < self.adaptation_parameters["struggle_detection_threshold"]:
            return LearningState.STRUGGLING
        elif success_rate > self.adaptation_parameters["boredom_detection_threshold"] and avg_attempts < 1.5:
            return LearningState.BORED
        elif success_rate > self.adaptation_parameters["mastery_threshold"]:
            return LearningState.MASTERED
        else:
            return LearningState.PROGRESSING
    
    def _handle_struggling_learner(self, user_id: str):
        """어려움을 겪는 학습자 처리"""
        profile = self.learner_profiles[user_id]
        
        # 난이도 하향 조정
        profile.preferred_difficulty = max(1, profile.preferred_difficulty - 1)
        
        # 추가 지원 제공 플래그 설정
        profile.needs_support = True
    
    def _handle_bored_learner(self, user_id: str):
        """지루해하는 학습자 처리"""
        profile = self.learner_profiles[user_id]
        
        # 난이도 상향 조정
        profile.preferred_difficulty = min(10, profile.preferred_difficulty + 1)
        
        # 도전적인 콘텐츠 추천 플래그 설정
        profile.needs_challenge = True
    
    def _handle_progressing_learner(self, user_id: str):
        """정상 진행 중인 학습자 처리"""
        # 현재 설정 유지
        pass
    
    def _handle_mastered_learner(self, user_id: str):
        """숙달된 학습자 처리"""
        profile = self.learner_profiles[user_id]
        
        # 다음 단계로 진행 추천
        profile.ready_for_next_level = True
    
    def generate_content_recommendations(self, user_id: str, 
                                       num_recommendations: int = 5) -> List[ContentRecommendation]:
        """개인화된 콘텐츠 추천 생성"""
        if user_id not in self.learner_profiles:
            return []
        
        profile = self.learner_profiles[user_id]
        
        # 사용 가능한 모든 콘텐츠 가져오기
        available_content = self._get_available_content(user_id)
        
        # 각 콘텐츠에 대한 추천 점수 계산
        recommendations = []
        for content_id in available_content:
            score = self._calculate_recommendation_score(user_id, content_id)
            
            if score > 0.3:  # 최소 임계값
                recommendation = ContentRecommendation(
                    content_id=content_id,
                    recommendation_score=score,
                    reasoning=self._generate_recommendation_reasoning(user_id, content_id),
                    difficulty_adjustment=self._calculate_difficulty_adjustment(user_id, content_id),
                    estimated_time=self._estimate_completion_time(user_id, content_id),
                    success_probability=self._predict_success_probability(user_id, content_id)
                )
                recommendations.append(recommendation)
        
        # 추천 점수 순으로 정렬
        recommendations.sort(key=lambda x: x.recommendation_score, reverse=True)
        
        return recommendations[:num_recommendations]
    
    def _calculate_recommendation_score(self, user_id: str, content_id: str) -> float:
        """추천 점수 계산"""
        profile = self.learner_profiles[user_id]
        
        # 기본 점수 요소들
        difficulty_match = self._calculate_difficulty_match(profile, content_id)
        prerequisite_readiness = self._check_prerequisite_readiness(user_id, content_id)
        learning_style_match = self._calculate_learning_style_match(profile, content_id)
        topic_interest = self._calculate_topic_interest(profile, content_id)
        
        # 가중 평균으로 최종 점수 계산
        score = (
            0.3 * difficulty_match +
            0.3 * prerequisite_readiness +
            0.2 * learning_style_match +
            0.2 * topic_interest
        )
        
        return max(0.0, min(1.0, score))
    
    def _calculate_difficulty_match(self, profile: LearnerProfile, content_id: str) -> float:
        """난이도 일치도 계산"""
        content_difficulty = self.content_difficulty_map.get(content_id, 5)
        difficulty_diff = abs(profile.preferred_difficulty - content_difficulty)
        
        # 차이가 클수록 점수 감소
        return max(0.0, 1.0 - (difficulty_diff / 10.0))
    
    def _check_prerequisite_readiness(self, user_id: str, content_id: str) -> float:
        """전제조건 준비도 확인"""
        prerequisites = self._get_content_prerequisites(content_id)
        
        if not prerequisites:
            return 1.0
        
        mastered_prerequisites = [
            prereq for prereq in prerequisites
            if self._is_content_mastered(user_id, prereq)
        ]
        
        return len(mastered_prerequisites) / len(prerequisites)
    
    def _calculate_learning_style_match(self, profile: LearnerProfile, content_id: str) -> float:
        """학습 스타일 일치도 계산"""
        content_style = self._get_content_learning_style(content_id)
        
        style_compatibility = {
            "visual": {"visual": 1.0, "kinesthetic": 0.7, "auditory": 0.5, "reading": 0.6},
            "auditory": {"auditory": 1.0, "visual": 0.5, "reading": 0.8, "kinesthetic": 0.4},
            "kinesthetic": {"kinesthetic": 1.0, "visual": 0.7, "auditory": 0.4, "reading": 0.3},
            "reading": {"reading": 1.0, "auditory": 0.8, "visual": 0.6, "kinesthetic": 0.3}
        }
        
        return style_compatibility.get(profile.learning_style, {}).get(content_style, 0.5)
    
    def _calculate_topic_interest(self, profile: LearnerProfile, content_id: str) -> float:
        """주제 관심도 계산"""
        content_topic = self._get_content_topic(content_id)
        
        # 강점 영역에 대한 관심도 높음
        if content_topic in profile.strengths:
            return 0.8
        # 약점 영역이지만 목표에 포함된 경우
        elif content_topic in profile.weaknesses and content_topic in profile.goals:
            return 0.9
        # 목표에 포함된 경우
        elif content_topic in profile.goals:
            return 0.7
        else:
            return 0.5
    
    def predict_learning_outcome(self, user_id: str, content_id: str) -> Dict[str, Any]:
        """학습 결과 예측"""
        if user_id not in self.learner_profiles:
            return {"error": "User profile not found"}
        
        profile = self.learner_profiles[user_id]
        
        # 성공 확률 예측
        success_probability = self._predict_success_probability(user_id, content_id)
        
        # 완료 시간 예측
        estimated_time = self._estimate_completion_time(user_id, content_id)
        
        # 필요한 도움 수준 예측
        help_level = self._predict_help_requirement(user_id, content_id)
        
        # 학습 효과 예측
        learning_gain = self._predict_learning_gain(user_id, content_id)
        
        return {
            "success_probability": success_probability,
            "estimated_completion_time": estimated_time,
            "required_help_level": help_level,
            "predicted_learning_gain": learning_gain,
            "confidence_interval": self._calculate_prediction_confidence(user_id, content_id)
        }
    
    def _predict_success_probability(self, user_id: str, content_id: str) -> float:
        """ML 기반 성공 확률 예측"""
        if self.success_predictor is None or user_id not in self.learner_profiles:
            return self._fallback_success_prediction(user_id, content_id)
        
        try:
            # 특성 벡터 생성
            features = self._extract_prediction_features(user_id, content_id)
            features_scaled = self.scaler.transform([features])
            
            # ML 모델 예측
            if hasattr(self.success_predictor, 'predict_proba'):
                prediction = self.success_predictor.predict_proba(features_scaled)[0][1]
            else:
                prediction = self.success_predictor.predict(features_scaled)[0]
            
            # 기존 규칙 기반 예측과 앙상블
            rule_based = self._fallback_success_prediction(user_id, content_id)
            ensemble_prediction = (
                0.7 * prediction + 0.3 * rule_based
            )
            
            return max(0.0, min(1.0, ensemble_prediction))
            
        except Exception as e:
            print(f"ML 예측 오류: {e}, 규칙 기반으로 대체")
            return self._fallback_success_prediction(user_id, content_id)
    
    def _fallback_success_prediction(self, user_id: str, content_id: str) -> float:
        """규칙 기반 성공 확률 예측 (백업)"""
        if user_id not in self.learner_profiles:
            return 0.5
            
        profile = self.learner_profiles[user_id]
        
        # 특성 기반 예측
        difficulty_factor = self._calculate_difficulty_match(profile, content_id)
        prerequisite_factor = self._check_prerequisite_readiness(user_id, content_id)
        
        # 과거 성과 기반 예측
        historical_performance = self._get_historical_performance(user_id)
        
        # 주제별 성과 기반 예측
        topic = self._get_content_topic(content_id)
        topic_performance = self._calculate_topic_success_rate(user_id, topic)
        
        # 종합 예측
        prediction = (
            0.3 * difficulty_factor +
            0.3 * prerequisite_factor +
            0.2 * historical_performance +
            0.2 * topic_performance
        )
        
        return max(0.0, min(1.0, prediction))
    
    def _extract_prediction_features(self, user_id: str, content_id: str) -> List[float]:
        """예측을 위한 특성 벡터 추출"""
        profile = self.learner_profiles[user_id]
        
        features = [
            # 학습자 특성
            profile.prior_knowledge_level / 10.0,
            profile.preferred_difficulty / 10.0,
            profile.motivation_level / 10.0,
            profile.time_availability / 12.0,
            
            # 콘텐츠 특성
            self.content_difficulty_map.get(content_id, 5) / 10.0,
            len(self._get_content_prerequisites(content_id)) / 5.0,
            
            # 학습 스타일 매칭
            self._calculate_learning_style_match(profile, content_id),
            
            # 성과 기록
            self._calculate_success_rate(user_id),
            self._calculate_topic_success_rate(user_id, self._get_content_topic(content_id)),
            
            # 시간적 특성
            self._get_time_since_last_activity(user_id) / (24 * 3600),  # 일 단위
            self._get_session_frequency(user_id),
            
            # 상호작용 패턴
            self._get_avg_attempts(user_id),
            self._get_hint_usage_rate(user_id),
            self._get_avg_completion_time_ratio(user_id)
        ]
        
        return features
    
    def generate_adaptive_feedback(self, user_id: str, 
                                 interaction: LearningInteraction) -> Dict[str, Any]:
        """적응형 피드백 생성"""
        profile = self.learner_profiles[user_id]
        learning_state = self._detect_learning_state(user_id)
        
        feedback = {
            "message": "",
            "encouragement_level": "",
            "next_steps": [],
            "resources": []
        }
        
        if learning_state == LearningState.STRUGGLING:
            feedback.update({
                "message": "개념을 이해하는 데 어려움이 있는 것 같습니다. 기초부터 차근차근 접근해보세요.",
                "encouragement_level": "high",
                "next_steps": [
                    "기본 개념 복습",
                    "간단한 예제부터 시작",
                    "도움 요청하기"
                ],
                "resources": ["기초 자료", "튜터링 세션", "추가 연습 문제"]
            })
        
        elif learning_state == LearningState.BORED:
            feedback.update({
                "message": "훌륭합니다! 더 도전적인 내용을 시도해보세요.",
                "encouragement_level": "motivating",
                "next_steps": [
                    "고급 문제 도전",
                    "실제 프로젝트 적용",
                    "다른 학습자 도움주기"
                ],
                "resources": ["고급 자료", "프로젝트 과제", "멘토링 기회"]
            })
        
        elif learning_state == LearningState.MASTERED:
            feedback.update({
                "message": "완벽하게 이해했습니다! 다음 단계로 진행할 준비가 되었습니다.",
                "encouragement_level": "congratulatory",
                "next_steps": [
                    "다음 레벨 진행",
                    "종합 프로젝트 시작",
                    "지식 응용하기"
                ],
                "resources": ["다음 단계 자료", "종합 프로젝트", "응용 사례"]
            })
        
        else:  # PROGRESSING
            feedback.update({
                "message": "좋은 진전을 보이고 있습니다. 계속 진행해보세요!",
                "encouragement_level": "encouraging",
                "next_steps": [
                    "현재 속도 유지",
                    "추가 연습",
                    "이해도 확인"
                ],
                "resources": ["연습 문제", "개념 정리", "자가 점검 도구"]
            })
        
        return feedback
    
    # 유틸리티 메서드들
    def _get_recent_interactions(self, user_id: str, count: int) -> List[LearningInteraction]:
        """최근 상호작용 가져오기"""
        user_interactions = [i for i in self.interaction_history if i.user_id == user_id]
        return sorted(user_interactions, key=lambda x: x.timestamp, reverse=True)[:count]
    
    def _calculate_success_rate(self, user_id: str, window_size: int = 10) -> float:
        """성공률 계산"""
        recent_interactions = self._get_recent_interactions(user_id, window_size)
        successful_interactions = [i for i in recent_interactions if i.success is True]
        
        if not recent_interactions:
            return 0.5  # 기본값
        
        return len(successful_interactions) / len(recent_interactions)
    
    def _get_content_topic(self, content_id: str) -> str:
        """콘텐츠 주제 가져오기"""
        # 실제 구현에서는 콘텐츠 메타데이터에서 가져옴
        topic_map = {
            "stats_basics": "descriptive_statistics",
            "probability": "probability_theory",
            "hypothesis_testing": "inferential_statistics",
            "regression": "regression_analysis",
            "factor_analysis": "multivariate_analysis"
        }
        return topic_map.get(content_id, "general")
    
    def _calculate_topic_success_rate(self, user_id: str, topic: str) -> float:
        """주제별 성공률 계산"""
        topic_interactions = [
            i for i in self.interaction_history
            if i.user_id == user_id and self._get_content_topic(i.content_id) == topic
        ]
        
        if not topic_interactions:
            return 0.5
        
        successful = [i for i in topic_interactions if i.success is True]
        return len(successful) / len(topic_interactions)
    
    def _get_expected_duration(self, content_id: str) -> int:
        """예상 완료 시간 가져오기"""
        # 실제 구현에서는 콘텐츠 메타데이터에서 가져옴
        duration_map = {
            "stats_basics": 300,  # 5분
            "probability": 600,   # 10분
            "hypothesis_testing": 900,  # 15분
            "regression": 1200,   # 20분
            "factor_analysis": 1800  # 30분
        }
        return duration_map.get(content_id, 600)
    
    # 새로운 ML 기반 메서드들
    def train_ml_models(self):
        """ML 모델 훈련"""
        if len(self.interaction_history) < self.adaptation_parameters["ml_retrain_threshold"]:
            print(f"데이터 부족: {len(self.interaction_history)}개 (최소 {self.adaptation_parameters['ml_retrain_threshold']}개 필요)")
            return False
        
        try:
            # 훈련 데이터 준비
            X, y_success, y_difficulty, y_engagement = self._prepare_training_data()
            
            if len(X) == 0:
                print("훈련 데이터가 없습니다.")
                return False
            
            # 데이터 분할
            X_train, X_test, y_success_train, y_success_test = train_test_split(
                X, y_success, test_size=0.2, random_state=42, stratify=y_success
            )
            
            # 특성 스케일링
            X_train_scaled = self.scaler.fit_transform(X_train)
            X_test_scaled = self.scaler.transform(X_test)
            
            # 성공 예측 모델 훈련
            self.success_predictor.fit(X_train_scaled, y_success_train)
            success_pred = self.success_predictor.predict(X_test_scaled)
            success_accuracy = accuracy_score(y_success_test, success_pred)
            
            # 모델 성능 업데이트
            self.model_performance['success_predictor'].update({
                'accuracy': success_accuracy,
                'last_trained': datetime.now()
            })
            
            # 모델 저장
            self._save_models()
            
            print(f"ML 모델 훈련 완료 - 성공 예측 정확도: {success_accuracy:.3f}")
            return True
            
        except Exception as e:
            print(f"ML 모델 훈련 오류: {e}")
            return False
    
    def _prepare_training_data(self) -> Tuple[List[List[float]], List[int], List[int], List[int]]:
        """훈련 데이터 준비"""
        X = []
        y_success = []
        y_difficulty = []
        y_engagement = []
        
        for interaction in self.interaction_history:
            if interaction.user_id not in self.learner_profiles:
                continue
                
            try:
                features = self._extract_prediction_features(
                    interaction.user_id, interaction.content_id
                )
                X.append(features)
                
                # 성공 여부 레이블
                y_success.append(1 if interaction.success else 0)
                
                # 난이도 레이블 (적절/부적절)
                profile = self.learner_profiles[interaction.user_id]
                content_difficulty = self.content_difficulty_map.get(interaction.content_id, 5)
                difficulty_appropriate = abs(profile.preferred_difficulty - content_difficulty) <= 2
                y_difficulty.append(1 if difficulty_appropriate else 0)
                
                # 참여도 레이블 (시간 기반)
                expected_time = self._get_expected_duration(interaction.content_id)
                engagement_level = 1 if interaction.duration > expected_time * 0.5 else 0
                y_engagement.append(engagement_level)
                
            except Exception as e:
                print(f"특성 추출 오류: {e}")
                continue
        
        return X, y_success, y_difficulty, y_engagement
    
    def get_feature_importance(self) -> Dict[str, float]:
        """특성 중요도 분석"""
        if self.success_predictor is None or not hasattr(self.success_predictor, 'feature_importances_'):
            return {}
        
        feature_names = [
            'prior_knowledge', 'preferred_difficulty', 'motivation', 'time_availability',
            'content_difficulty', 'prerequisites_count', 'learning_style_match',
            'success_rate', 'topic_success_rate', 'time_since_activity',
            'session_frequency', 'avg_attempts', 'hint_usage', 'completion_time_ratio'
        ]
        
        importances = self.success_predictor.feature_importances_
        return dict(zip(feature_names, importances))
    
    def adaptive_difficulty_recommendation(self, user_id: str) -> Dict[str, Any]:
        """적응형 난이도 추천"""
        if user_id not in self.learner_profiles:
            return {"recommended_difficulty": 5, "confidence": 0.5}
        
        profile = self.learner_profiles[user_id]
        recent_performance = self._get_recent_performance_metrics(user_id)
        
        # ML 기반 추천 (있는 경우)
        ml_recommendation = self._get_ml_difficulty_recommendation(user_id)
        
        # 규칙 기반 추천
        rule_recommendation = self._get_rule_based_difficulty_recommendation(user_id)
        
        # 앙상블 결합
        if ml_recommendation['confidence'] > 0.7:
            final_difficulty = int(
                0.7 * ml_recommendation['difficulty'] + 
                0.3 * rule_recommendation['difficulty']
            )
            confidence = (ml_recommendation['confidence'] + rule_recommendation['confidence']) / 2
        else:
            final_difficulty = rule_recommendation['difficulty']
            confidence = rule_recommendation['confidence']
        
        return {
            "recommended_difficulty": max(1, min(10, final_difficulty)),
            "confidence": confidence,
            "reasoning": self._generate_difficulty_reasoning(user_id, final_difficulty),
            "recent_performance": recent_performance
        }
    
    def _get_recent_performance_metrics(self, user_id: str) -> Dict[str, float]:
        """최근 성과 지표 계산"""
        recent_interactions = self._get_recent_interactions(user_id, 20)
        
        if not recent_interactions:
            return {"success_rate": 0.5, "avg_attempts": 1.0, "completion_rate": 0.5}
        
        success_rate = np.mean([i.success for i in recent_interactions if i.success is not None])
        avg_attempts = np.mean([i.attempts for i in recent_interactions])
        
        # 완료율 (스킵하지 않은 비율)
        non_skip_interactions = [i for i in recent_interactions if i.interaction_type != InteractionType.SKIP_CONTENT]
        completion_rate = len(non_skip_interactions) / len(recent_interactions) if recent_interactions else 0.5
        
        return {
            "success_rate": success_rate,
            "avg_attempts": avg_attempts,
            "completion_rate": completion_rate
        }
    
    # 유틸리티 메서드들 추가
    def _get_historical_performance(self, user_id: str) -> float:
        """전체 성과 기록"""
        return self._calculate_success_rate(user_id, window_size=50)
    
    def _get_time_since_last_activity(self, user_id: str) -> float:
        """마지막 활동 이후 시간 (초)"""
        if user_id not in self.learner_profiles:
            return 86400  # 1일
        
        last_activity = self.learner_profiles[user_id].last_activity
        return (datetime.now() - last_activity).total_seconds()
    
    def _get_session_frequency(self, user_id: str) -> float:
        """세션 빈도 (일주일 기준)"""
        week_ago = datetime.now() - timedelta(days=7)
        recent_sessions = [
            i for i in self.interaction_history
            if i.user_id == user_id and i.timestamp > week_ago
        ]
        
        # 날짜별 그룹화
        session_dates = set(i.timestamp.date() for i in recent_sessions)
        return len(session_dates) / 7.0
    
    def _get_avg_attempts(self, user_id: str) -> float:
        """평균 시도 횟수"""
        user_interactions = [i for i in self.interaction_history if i.user_id == user_id]
        if not user_interactions:
            return 1.0
        
        return np.mean([i.attempts for i in user_interactions])
    
    def _get_hint_usage_rate(self, user_id: str) -> float:
        """힌트 사용률"""
        user_interactions = [i for i in self.interaction_history if i.user_id == user_id]
        if not user_interactions:
            return 0.0
        
        hint_used = sum(1 for i in user_interactions if i.hint_used)
        return hint_used / len(user_interactions)
    
    def _get_avg_completion_time_ratio(self, user_id: str) -> float:
        """평균 완료 시간 비율 (예상 시간 대비)"""
        user_interactions = [i for i in self.interaction_history if i.user_id == user_id]
        if not user_interactions:
            return 1.0
        
        ratios = []
        for interaction in user_interactions:
            expected = self._get_expected_duration(interaction.content_id)
            if expected > 0:
                ratios.append(interaction.duration / expected)
        
        return np.mean(ratios) if ratios else 1.0


# 전역 적응형 학습 엔진
adaptive_engine = AdaptiveLearningEngine()