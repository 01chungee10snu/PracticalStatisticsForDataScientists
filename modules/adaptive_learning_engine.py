"""
적응형 학습 엔진
- 학습자 수준 자동 감지
- 개인화된 학습 경로 제공
- 실시간 난이도 조절
- 학습 성과 추적 및 분석
"""

import json
import math
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict

@dataclass
class LearnerProfile:
    """학습자 프로필"""
    user_id: str
    current_level: str  # foundation, developing, proficient, advanced
    skill_scores: Dict[str, float]  # 각 스킬별 점수 (0-100)
    learning_pace: float  # 학습 속도 (0.5-2.0)
    preferred_style: str  # visual, auditory, kinesthetic, reading
    completion_rate: float  # 완료율 (0-1)
    last_activity: str
    total_study_time: int  # 분 단위

@dataclass
class LearningSession:
    """학습 세션 데이터"""
    session_id: str
    user_id: str
    topic: str
    start_time: str
    end_time: Optional[str]
    exercises_completed: int
    correct_answers: int
    difficulty_level: float
    engagement_score: float

class AdaptiveLearningEngine:
    def __init__(self):
        self.learner_profiles: Dict[str, LearnerProfile] = {}
        self.learning_sessions: List[LearningSession] = []
        self.skill_taxonomy = {
            'foundation': {
                'descriptive_statistics': ['mean', 'median', 'mode', 'std_dev'],
                'data_visualization': ['histogram', 'boxplot', 'scatter'],
                'probability_basics': ['basic_probability', 'distributions'],
                'python_basics': ['pandas', 'numpy', 'matplotlib']
            },
            'developing': {
                'statistical_inference': ['hypothesis_testing', 'confidence_intervals'],
                'regression_analysis': ['simple_regression', 'correlation'],
                'experimental_design': ['ab_testing', 'sample_size'],
                'advanced_visualization': ['seaborn', 'plotly']
            },
            'proficient': {
                'multiple_regression': ['multivariate', 'model_selection'],
                'classification': ['logistic_regression', 'decision_trees'],
                'time_series': ['trend_analysis', 'forecasting'],
                'machine_learning': ['supervised', 'unsupervised']
            },
            'advanced': {
                'deep_learning': ['neural_networks', 'tensorflow'],
                'big_data': ['spark', 'distributed_computing'],
                'nlp': ['text_mining', 'sentiment_analysis'],
                'advanced_ml': ['ensemble', 'optimization']
            }
        }
    
    def create_learner_profile(self, user_id: str, initial_assessment: Dict[str, Any]) -> LearnerProfile:
        """학습자 프로필 생성"""
        # 초기 평가 결과를 바탕으로 수준 결정
        level = self._determine_initial_level(initial_assessment)
        
        profile = LearnerProfile(
            user_id=user_id,
            current_level=level,
            skill_scores=self._initialize_skill_scores(level),
            learning_pace=1.0,  # 기본 속도
            preferred_style=initial_assessment.get('learning_style', 'visual'),
            completion_rate=0.0,
            last_activity=datetime.now().isoformat(),
            total_study_time=0
        )
        
        self.learner_profiles[user_id] = profile
        return profile
    
    def _determine_initial_level(self, assessment: Dict[str, Any]) -> str:
        """초기 수준 결정"""
        score = assessment.get('total_score', 0)
        
        if score < 30:
            return 'foundation'
        elif score < 60:
            return 'developing'
        elif score < 80:
            return 'proficient'
        else:
            return 'advanced'
    
    def _initialize_skill_scores(self, level: str) -> Dict[str, float]:
        """스킬 점수 초기화"""
        scores = {}
        
        # 현재 레벨과 이전 레벨의 스킬들에 대해 점수 설정
        levels = ['foundation', 'developing', 'proficient', 'advanced']
        current_index = levels.index(level)
        
        for i, lvl in enumerate(levels):
            if i < current_index:
                # 이전 레벨은 높은 점수
                base_score = 80
            elif i == current_index:
                # 현재 레벨은 중간 점수
                base_score = 50
            else:
                # 상위 레벨은 낮은 점수
                base_score = 20
            
            for category, skills in self.skill_taxonomy[lvl].items():
                for skill in skills:
                    scores[skill] = base_score + (math.random() * 20 - 10)  # ±10 변동
        
        return scores
    
    def get_personalized_learning_path(self, user_id: str) -> Dict[str, Any]:
        """개인화된 학습 경로 생성"""
        if user_id not in self.learner_profiles:
            raise ValueError(f"User {user_id} not found")
        
        profile = self.learner_profiles[user_id]
        
        # 약점 스킬 식별
        weak_skills = self._identify_weak_skills(profile)
        
        # 다음 학습 목표 설정
        next_objectives = self._set_learning_objectives(profile, weak_skills)
        
        # 학습 자료 추천
        recommended_materials = self._recommend_materials(profile, next_objectives)
        
        # 예상 학습 시간 계산
        estimated_time = self._estimate_learning_time(profile, next_objectives)
        
        return {
            'user_id': user_id,
            'current_level': profile.current_level,
            'weak_skills': weak_skills,
            'next_objectives': next_objectives,
            'recommended_materials': recommended_materials,
            'estimated_time_minutes': estimated_time,
            'learning_pace_adjustment': self._calculate_pace_adjustment(profile)
        }
    
    def _identify_weak_skills(self, profile: LearnerProfile) -> List[Dict[str, Any]]:
        """약점 스킬 식별"""
        weak_skills = []
        
        for skill, score in profile.skill_scores.items():
            if score < 60:  # 60점 미만을 약점으로 간주
                weak_skills.append({
                    'skill': skill,
                    'score': score,
                    'priority': self._calculate_skill_priority(skill, profile)
                })
        
        # 우선순위 순으로 정렬
        weak_skills.sort(key=lambda x: x['priority'], reverse=True)
        
        return weak_skills[:5]  # 상위 5개만 반환
    
    def _calculate_skill_priority(self, skill: str, profile: LearnerProfile) -> float:
        """스킬 우선순위 계산"""
        # 현재 레벨에 필요한 스킬일수록 높은 우선순위
        current_level_skills = []
        for category, skills in self.skill_taxonomy[profile.current_level].items():
            current_level_skills.extend(skills)
        
        if skill in current_level_skills:
            return 1.0
        
        # 기초 스킬일수록 높은 우선순위
        foundation_skills = []
        for category, skills in self.skill_taxonomy['foundation'].items():
            foundation_skills.extend(skills)
        
        if skill in foundation_skills:
            return 0.8
        
        return 0.5
    
    def _set_learning_objectives(self, profile: LearnerProfile, weak_skills: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """학습 목표 설정"""
        objectives = []
        
        for weak_skill in weak_skills[:3]:  # 상위 3개 약점 스킬
            skill_name = weak_skill['skill']
            current_score = weak_skill['score']
            target_score = min(100, current_score + 30)  # 30점 향상 목표
            
            objectives.append({
                'skill': skill_name,
                'current_score': current_score,
                'target_score': target_score,
                'difficulty_level': self._calculate_optimal_difficulty(profile, skill_name),
                'learning_activities': self._generate_learning_activities(skill_name, profile)
            })
        
        return objectives
    
    def _calculate_optimal_difficulty(self, profile: LearnerProfile, skill: str) -> float:
        """최적 난이도 계산 (Zone of Proximal Development)"""
        current_skill_score = profile.skill_scores.get(skill, 0)
        
        # 현재 실력보다 10-20% 높은 난이도가 최적
        optimal_difficulty = (current_skill_score / 100) + 0.15
        
        # 학습 속도에 따른 조정
        if profile.learning_pace > 1.2:
            optimal_difficulty += 0.05  # 빠른 학습자는 조금 더 어렵게
        elif profile.learning_pace < 0.8:
            optimal_difficulty -= 0.05  # 느린 학습자는 조금 더 쉽게
        
        return max(0.1, min(1.0, optimal_difficulty))
    
    def _generate_learning_activities(self, skill: str, profile: LearnerProfile) -> List[Dict[str, Any]]:
        """학습 활동 생성"""
        activities = []
        
        # 학습 스타일에 따른 활동 추천
        if profile.preferred_style == 'visual':
            activities.extend([
                {'type': 'visualization', 'description': f'{skill} 시각화 실습'},
                {'type': 'diagram', 'description': f'{skill} 개념도 학습'}
            ])
        elif profile.preferred_style == 'kinesthetic':
            activities.extend([
                {'type': 'hands_on', 'description': f'{skill} 실습 프로젝트'},
                {'type': 'interactive', 'description': f'{skill} 인터랙티브 연습'}
            ])
        else:  # auditory, reading
            activities.extend([
                {'type': 'reading', 'description': f'{skill} 이론 학습'},
                {'type': 'explanation', 'description': f'{skill} 개념 설명'}
            ])
        
        # 공통 활동
        activities.extend([
            {'type': 'practice', 'description': f'{skill} 연습 문제'},
            {'type': 'assessment', 'description': f'{skill} 이해도 확인'}
        ])
        
        return activities
    
    def _recommend_materials(self, profile: LearnerProfile, objectives: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """학습 자료 추천"""
        materials = []
        
        for objective in objectives:
            skill = objective['skill']
            difficulty = objective['difficulty_level']
            
            # 난이도에 따른 자료 추천
            if difficulty < 0.3:
                level_tag = "기초"
                materials.append({
                    'skill': skill,
                    'title': f"{skill} {level_tag} 가이드",
                    'type': 'tutorial',
                    'difficulty': difficulty,
                    'estimated_time': 15
                })
            elif difficulty < 0.7:
                level_tag = "중급"
                materials.append({
                    'skill': skill,
                    'title': f"{skill} {level_tag} 실습",
                    'type': 'practice',
                    'difficulty': difficulty,
                    'estimated_time': 30
                })
            else:
                level_tag = "고급"
                materials.append({
                    'skill': skill,
                    'title': f"{skill} {level_tag} 프로젝트",
                    'type': 'project',
                    'difficulty': difficulty,
                    'estimated_time': 60
                })
        
        return materials
    
    def _estimate_learning_time(self, profile: LearnerProfile, objectives: List[Dict[str, Any]]) -> int:
        """학습 시간 예상"""
        base_time = len(objectives) * 45  # 목표당 45분 기본
        
        # 학습 속도에 따른 조정
        adjusted_time = base_time / profile.learning_pace
        
        # 현재 완료율에 따른 조정
        if profile.completion_rate < 0.5:
            adjusted_time *= 1.2  # 완료율이 낮으면 더 많은 시간 필요
        
        return int(adjusted_time)
    
    def _calculate_pace_adjustment(self, profile: LearnerProfile) -> Dict[str, Any]:
        """학습 속도 조정 계산"""
        recent_sessions = [s for s in self.learning_sessions 
                          if s.user_id == profile.user_id][-5:]  # 최근 5세션
        
        if not recent_sessions:
            return {'adjustment': 0, 'reason': 'insufficient_data'}
        
        # 정답률 기반 조정
        avg_accuracy = sum(s.correct_answers / max(s.exercises_completed, 1) 
                          for s in recent_sessions) / len(recent_sessions)
        
        if avg_accuracy > 0.8:
            return {'adjustment': 0.1, 'reason': 'high_accuracy'}
        elif avg_accuracy < 0.5:
            return {'adjustment': -0.1, 'reason': 'low_accuracy'}
        else:
            return {'adjustment': 0, 'reason': 'optimal_pace'}
    
    def update_learner_progress(self, user_id: str, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """학습 진도 업데이트"""
        if user_id not in self.learner_profiles:
            raise ValueError(f"User {user_id} not found")
        
        profile = self.learner_profiles[user_id]
        
        # 세션 데이터 저장
        session = LearningSession(
            session_id=session_data['session_id'],
            user_id=user_id,
            topic=session_data['topic'],
            start_time=session_data['start_time'],
            end_time=session_data.get('end_time'),
            exercises_completed=session_data['exercises_completed'],
            correct_answers=session_data['correct_answers'],
            difficulty_level=session_data['difficulty_level'],
            engagement_score=session_data.get('engagement_score', 0.5)
        )
        
        self.learning_sessions.append(session)
        
        # 프로필 업데이트
        self._update_skill_scores(profile, session)
        self._update_learning_pace(profile, session)
        self._update_completion_rate(profile)
        
        profile.last_activity = datetime.now().isoformat()
        
        # 레벨 승급 확인
        level_change = self._check_level_progression(profile)
        
        return {
            'updated_profile': asdict(profile),
            'level_change': level_change,
            'next_recommendations': self.get_personalized_learning_path(user_id)
        }
    
    def _update_skill_scores(self, profile: LearnerProfile, session: LearningSession):
        """스킬 점수 업데이트"""
        topic = session.topic
        accuracy = session.correct_answers / max(session.exercises_completed, 1)
        
        # 정확도에 따른 점수 조정
        if topic in profile.skill_scores:
            current_score = profile.skill_scores[topic]
            
            if accuracy > 0.8:
                # 높은 정확도: 점수 증가
                score_increase = min(5, (accuracy - 0.8) * 25)
                profile.skill_scores[topic] = min(100, current_score + score_increase)
            elif accuracy < 0.5:
                # 낮은 정확도: 점수 감소
                score_decrease = (0.5 - accuracy) * 10
                profile.skill_scores[topic] = max(0, current_score - score_decrease)
    
    def _update_learning_pace(self, profile: LearnerProfile, session: LearningSession):
        """학습 속도 업데이트"""
        # 참여도와 정확도를 바탕으로 학습 속도 조정
        accuracy = session.correct_answers / max(session.exercises_completed, 1)
        engagement = session.engagement_score
        
        pace_factor = (accuracy + engagement) / 2
        
        if pace_factor > 0.7:
            profile.learning_pace = min(2.0, profile.learning_pace + 0.05)
        elif pace_factor < 0.4:
            profile.learning_pace = max(0.5, profile.learning_pace - 0.05)
    
    def _update_completion_rate(self, profile: LearnerProfile):
        """완료율 업데이트"""
        user_sessions = [s for s in self.learning_sessions if s.user_id == profile.user_id]
        
        if user_sessions:
            completed_sessions = [s for s in user_sessions if s.end_time is not None]
            profile.completion_rate = len(completed_sessions) / len(user_sessions)
    
    def _check_level_progression(self, profile: LearnerProfile) -> Optional[Dict[str, str]]:
        """레벨 승급 확인"""
        current_level = profile.current_level
        current_level_skills = []
        
        for category, skills in self.skill_taxonomy[current_level].items():
            current_level_skills.extend(skills)
        
        # 현재 레벨 스킬들의 평균 점수
        level_scores = [profile.skill_scores.get(skill, 0) for skill in current_level_skills]
        avg_score = sum(level_scores) / len(level_scores) if level_scores else 0
        
        # 80점 이상이면 다음 레벨로 승급
        if avg_score >= 80:
            levels = ['foundation', 'developing', 'proficient', 'advanced']
            current_index = levels.index(current_level)
            
            if current_index < len(levels) - 1:
                new_level = levels[current_index + 1]
                profile.current_level = new_level
                
                # 새 레벨 스킬 점수 초기화
                for category, skills in self.skill_taxonomy[new_level].items():
                    for skill in skills:
                        if skill not in profile.skill_scores:
                            profile.skill_scores[skill] = 30  # 새 스킬은 30점부터 시작
                
                return {
                    'from_level': current_level,
                    'to_level': new_level,
                    'achievement_score': avg_score
                }
        
        return None

# 사용 예제
if __name__ == "__main__":
    engine = AdaptiveLearningEngine()
    
    # 학습자 프로필 생성
    initial_assessment = {
        'total_score': 45,
        'learning_style': 'visual'
    }
    
    profile = engine.create_learner_profile('user123', initial_assessment)
    print(f"생성된 프로필: {profile.current_level} 레벨")
    
    # 개인화된 학습 경로 생성
    learning_path = engine.get_personalized_learning_path('user123')
    print(f"추천 학습 시간: {learning_path['estimated_time_minutes']}분")
    print(f"약점 스킬: {[skill['skill'] for skill in learning_path['weak_skills']]}")