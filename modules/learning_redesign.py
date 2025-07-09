"""
학습 콘텐츠 재설계 모듈
- 교육학적 원리 기반 콘텐츠 구조화
- 인지부하 이론 적용
- 점진적 복잡성 증가
- 적응형 학습 경로 제공
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum


class LearningStyle(Enum):
    """학습 스타일 분류"""
    VISUAL = "visual"
    AUDITORY = "auditory"
    KINESTHETIC = "kinesthetic"
    READING = "reading"


class DifficultyLevel(Enum):
    """난이도 단계"""
    FOUNDATION = "foundation"      # 기초
    DEVELOPING = "developing"      # 발전
    PROFICIENT = "proficient"      # 숙련
    ADVANCED = "advanced"          # 고급


@dataclass
class LearningObjective:
    """학습 목표 정의"""
    id: str
    title: str
    description: str
    level: DifficultyLevel
    prerequisites: List[str]
    bloom_level: str  # remember, understand, apply, analyze, evaluate, create
    estimated_time: int  # minutes
    assessment_type: str


@dataclass
class ConceptModule:
    """개념 모듈 정의"""
    id: str
    title: str
    objectives: List[LearningObjective]
    content_types: List[str]  # text, video, interactive, exercise
    scaffolding_elements: List[str]
    prerequisite_concepts: List[str]
    cognitive_load_score: int  # 1-10


class LearningPathRedesigner:
    """학습 경로 재설계 클래스"""
    
    def __init__(self):
        self.redesigned_structure = self._create_optimal_structure()
        self.assessment_framework = self._create_assessment_framework()
        self.scaffolding_system = self._create_scaffolding_system()
    
    def _create_optimal_structure(self) -> Dict[str, Any]:
        """최적화된 학습 구조 생성"""
        return {
            "foundation": {
                "title": "통계학 기초",
                "duration": "6주",
                "description": "데이터 과학을 위한 필수 통계 개념",
                "modules": [
                    ConceptModule(
                        id="stats_basics",
                        title="기술통계와 데이터 탐색",
                        objectives=[
                            LearningObjective(
                                id="desc_stats_1",
                                title="중심경향성 이해",
                                description="평균, 중앙값, 최빈값의 개념과 활용",
                                level=DifficultyLevel.FOUNDATION,
                                prerequisites=[],
                                bloom_level="understand",
                                estimated_time=30,
                                assessment_type="interactive_quiz"
                            ),
                            LearningObjective(
                                id="desc_stats_2",
                                title="산포도 측정",
                                description="분산, 표준편차, 범위의 해석",
                                level=DifficultyLevel.FOUNDATION,
                                prerequisites=["desc_stats_1"],
                                bloom_level="apply",
                                estimated_time=45,
                                assessment_type="hands_on_exercise"
                            )
                        ],
                        content_types=["interactive_visualization", "guided_practice"],
                        scaffolding_elements=["concept_map", "worked_examples", "immediate_feedback"],
                        prerequisite_concepts=[],
                        cognitive_load_score=3
                    ),
                    ConceptModule(
                        id="probability_basics",
                        title="확률의 기초",
                        objectives=[
                            LearningObjective(
                                id="prob_1",
                                title="확률 개념 이해",
                                description="확률의 정의와 기본 법칙",
                                level=DifficultyLevel.FOUNDATION,
                                prerequisites=["desc_stats_2"],
                                bloom_level="understand",
                                estimated_time=40,
                                assessment_type="conceptual_questions"
                            )
                        ],
                        content_types=["simulation", "interactive_examples"],
                        scaffolding_elements=["visual_analogies", "step_by_step_guide"],
                        prerequisite_concepts=["stats_basics"],
                        cognitive_load_score=4
                    )
                ]
            },
            "developing": {
                "title": "추론통계와 실험설계",
                "duration": "8주",
                "description": "통계적 추론과 연구방법론",
                "modules": [
                    ConceptModule(
                        id="sampling_distributions",
                        title="표본분포와 추정",
                        objectives=[
                            LearningObjective(
                                id="sampling_1",
                                title="중심극한정리 이해",
                                description="표본평균의 분포와 중심극한정리",
                                level=DifficultyLevel.DEVELOPING,
                                prerequisites=["prob_1"],
                                bloom_level="analyze",
                                estimated_time=60,
                                assessment_type="simulation_exercise"
                            )
                        ],
                        content_types=["interactive_simulation", "guided_discovery"],
                        scaffolding_elements=["parameter_manipulation", "visual_feedback"],
                        prerequisite_concepts=["probability_basics"],
                        cognitive_load_score=6
                    ),
                    ConceptModule(
                        id="hypothesis_testing",
                        title="가설검정",
                        objectives=[
                            LearningObjective(
                                id="hyp_test_1",
                                title="가설검정 절차",
                                description="귀무가설과 대립가설 설정 및 검정",
                                level=DifficultyLevel.DEVELOPING,
                                prerequisites=["sampling_1"],
                                bloom_level="apply",
                                estimated_time=75,
                                assessment_type="problem_solving"
                            )
                        ],
                        content_types=["case_study", "interactive_decision_tree"],
                        scaffolding_elements=["decision_flowchart", "error_analysis"],
                        prerequisite_concepts=["sampling_distributions"],
                        cognitive_load_score=7
                    )
                ]
            },
            "proficient": {
                "title": "다변량 분석과 모델링",
                "duration": "10주",
                "description": "회귀분석, 분류, 요인분석",
                "modules": [
                    ConceptModule(
                        id="regression_analysis",
                        title="회귀분석",
                        objectives=[
                            LearningObjective(
                                id="regression_1",
                                title="단순선형회귀",
                                description="두 변수 간의 선형관계 모델링",
                                level=DifficultyLevel.PROFICIENT,
                                prerequisites=["hyp_test_1"],
                                bloom_level="apply",
                                estimated_time=90,
                                assessment_type="data_analysis_project"
                            )
                        ],
                        content_types=["real_data_analysis", "interpretation_practice"],
                        scaffolding_elements=["assumption_checker", "result_interpreter"],
                        prerequisite_concepts=["hypothesis_testing"],
                        cognitive_load_score=8
                    ),
                    ConceptModule(
                        id="factor_analysis",
                        title="요인분석과 차원축소",
                        objectives=[
                            LearningObjective(
                                id="factor_1",
                                title="주성분분석",
                                description="차원축소와 주성분분석의 원리",
                                level=DifficultyLevel.PROFICIENT,
                                prerequisites=["regression_1"],
                                bloom_level="analyze",
                                estimated_time=120,
                                assessment_type="interpretation_exercise"
                            )
                        ],
                        content_types=["mathematical_intuition", "practical_application"],
                        scaffolding_elements=["mathematical_scaffolds", "conceptual_bridges"],
                        prerequisite_concepts=["regression_analysis"],
                        cognitive_load_score=9
                    )
                ]
            },
            "advanced": {
                "title": "머신러닝과 예측모델링",
                "duration": "12주",
                "description": "현대적 예측 모델링과 머신러닝",
                "modules": [
                    ConceptModule(
                        id="classification_methods",
                        title="분류 알고리즘",
                        objectives=[
                            LearningObjective(
                                id="classification_1",
                                title="의사결정나무와 랜덤포레스트",
                                description="트리 기반 분류 알고리즘의 이해와 적용",
                                level=DifficultyLevel.ADVANCED,
                                prerequisites=["factor_1"],
                                bloom_level="create",
                                estimated_time=150,
                                assessment_type="model_development_project"
                            )
                        ],
                        content_types=["hands_on_coding", "model_comparison"],
                        scaffolding_elements=["code_templates", "performance_evaluation"],
                        prerequisite_concepts=["factor_analysis"],
                        cognitive_load_score=9
                    )
                ]
            }
        }
    
    def _create_assessment_framework(self) -> Dict[str, Any]:
        """종합적 평가 체계 생성"""
        return {
            "formative_assessment": {
                "frequency": "매 개념 후",
                "types": [
                    "immediate_feedback_quiz",
                    "interactive_concept_check",
                    "peer_explanation_exercise",
                    "misconception_identification"
                ],
                "adaptive_features": [
                    "difficulty_adjustment",
                    "hint_provision",
                    "alternative_explanations"
                ]
            },
            "summative_assessment": {
                "frequency": "모듈 완료 시",
                "types": [
                    "comprehensive_case_study",
                    "data_analysis_project",
                    "peer_review_assignment",
                    "reflective_portfolio"
                ],
                "criteria": [
                    "conceptual_understanding",
                    "practical_application",
                    "critical_thinking",
                    "communication_skills"
                ]
            },
            "diagnostic_assessment": {
                "timing": "학습 시작 전/진행 중",
                "purpose": [
                    "prerequisite_knowledge_check",
                    "learning_style_identification",
                    "misconception_detection",
                    "progress_monitoring"
                ]
            }
        }
    
    def _create_scaffolding_system(self) -> Dict[str, Any]:
        """학습 지원 체계 생성"""
        return {
            "cognitive_scaffolds": {
                "concept_maps": "개념 간 관계 시각화",
                "worked_examples": "단계별 해결 과정 제시",
                "thinking_aloud": "전문가 사고 과정 모델링",
                "analogies": "친숙한 개념과의 연결"
            },
            "metacognitive_scaffolds": {
                "learning_strategies": "효과적 학습 방법 안내",
                "self_monitoring": "학습 진도 자가 점검",
                "reflection_prompts": "학습 과정 성찰 유도",
                "goal_setting": "개인 학습 목표 설정"
            },
            "social_scaffolds": {
                "peer_collaboration": "동료 학습 기회 제공",
                "expert_mentoring": "전문가 피드백 시스템",
                "community_support": "학습 커뮤니티 참여",
                "discussion_forums": "개념 토론 플랫폼"
            },
            "technological_scaffolds": {
                "adaptive_hints": "상황별 힌트 제공",
                "progress_tracking": "학습 진도 시각화",
                "personalized_feedback": "개인화된 피드백",
                "interactive_simulations": "개념 조작 도구"
            }
        }
    
    def generate_adaptive_pathway(self, student_profile: Dict[str, Any]) -> Dict[str, Any]:
        """학습자 프로필 기반 적응형 경로 생성"""
        learning_style = student_profile.get('learning_style', LearningStyle.VISUAL)
        prior_knowledge = student_profile.get('prior_knowledge', 'none')
        available_time = student_profile.get('weekly_hours', 5)
        goals = student_profile.get('goals', ['basic_understanding'])
        
        # 개인화된 학습 경로 생성
        pathway = {
            "recommended_sequence": self._determine_sequence(prior_knowledge, goals),
            "content_adaptations": self._adapt_content(learning_style),
            "time_allocation": self._allocate_time(available_time),
            "assessment_schedule": self._schedule_assessments(available_time),
            "support_resources": self._select_resources(learning_style, prior_knowledge)
        }
        
        return pathway
    
    def _determine_sequence(self, prior_knowledge: str, goals: List[str]) -> List[str]:
        """사전 지식과 목표에 따른 학습 순서 결정"""
        if prior_knowledge == 'none':
            return ["foundation", "developing", "proficient", "advanced"]
        elif prior_knowledge == 'basic_stats':
            return ["developing", "proficient", "advanced"]
        elif prior_knowledge == 'intermediate_stats':
            return ["proficient", "advanced"]
        else:
            return ["advanced"]
    
    def _adapt_content(self, learning_style: LearningStyle) -> Dict[str, str]:
        """학습 스타일에 따른 콘텐츠 적응"""
        adaptations = {
            LearningStyle.VISUAL: {
                "primary_format": "interactive_visualizations",
                "secondary_format": "infographics",
                "assessment_style": "visual_problem_solving"
            },
            LearningStyle.AUDITORY: {
                "primary_format": "narrated_explanations",
                "secondary_format": "discussion_forums",
                "assessment_style": "oral_presentations"
            },
            LearningStyle.KINESTHETIC: {
                "primary_format": "hands_on_simulations",
                "secondary_format": "interactive_exercises",
                "assessment_style": "practical_projects"
            },
            LearningStyle.READING: {
                "primary_format": "detailed_text_explanations",
                "secondary_format": "case_studies",
                "assessment_style": "written_analysis"
            }
        }
        return adaptations.get(learning_style, adaptations[LearningStyle.VISUAL])
    
    def _allocate_time(self, weekly_hours: int) -> Dict[str, int]:
        """주당 학습 시간에 따른 시간 배분"""
        if weekly_hours <= 3:
            return {"foundation": 3, "developing": 4, "proficient": 5, "advanced": 6}
        elif weekly_hours <= 6:
            return {"foundation": 2, "developing": 3, "proficient": 4, "advanced": 5}
        else:
            return {"foundation": 1.5, "developing": 2, "proficient": 3, "advanced": 4}
    
    def _schedule_assessments(self, weekly_hours: int) -> Dict[str, str]:
        """학습 시간에 따른 평가 일정"""
        if weekly_hours <= 3:
            return {
                "formative": "주 1회",
                "summative": "모듈당 1회",
                "diagnostic": "2주마다"
            }
        else:
            return {
                "formative": "주 2회",
                "summative": "모듈당 1회",
                "diagnostic": "주마다"
            }
    
    def _select_resources(self, learning_style: LearningStyle, prior_knowledge: str) -> List[str]:
        """학습 스타일과 사전 지식에 따른 지원 자료 선택"""
        base_resources = ["concept_glossary", "progress_tracker", "help_forum"]
        
        style_resources = {
            LearningStyle.VISUAL: ["interactive_charts", "concept_maps", "video_tutorials"],
            LearningStyle.AUDITORY: ["audio_explanations", "discussion_groups", "podcast_links"],
            LearningStyle.KINESTHETIC: ["simulation_tools", "practice_datasets", "lab_exercises"],
            LearningStyle.READING: ["detailed_notes", "research_papers", "textbook_references"]
        }
        
        knowledge_resources = {
            'none': ["math_refresher", "basic_terminology"],
            'basic_stats': ["intermediate_bridge", "application_examples"],
            'intermediate_stats': ["advanced_applications", "research_connections"]
        }
        
        return (base_resources + 
                style_resources.get(learning_style, []) + 
                knowledge_resources.get(prior_knowledge, []))
    
    def create_interactive_content(self, module_id: str) -> Dict[str, Any]:
        """모듈별 인터랙티브 콘텐츠 생성"""
        content_templates = {
            "stats_basics": {
                "simulations": [
                    {
                        "name": "central_tendency_explorer",
                        "description": "평균, 중앙값, 최빈값의 변화 탐색",
                        "parameters": ["dataset_size", "distribution_shape", "outliers"],
                        "learning_objectives": ["중심경향성 이해", "이상치 영향 파악"]
                    }
                ],
                "interactive_exercises": [
                    {
                        "name": "descriptive_stats_calculator",
                        "description": "기술통계량 직접 계산 연습",
                        "difficulty_levels": ["guided", "partially_guided", "independent"],
                        "feedback_types": ["immediate", "explanatory", "corrective"]
                    }
                ]
            },
            "probability_basics": {
                "simulations": [
                    {
                        "name": "probability_visualizer",
                        "description": "확률 개념의 시각적 이해",
                        "parameters": ["event_type", "sample_size", "repetitions"],
                        "learning_objectives": ["확률의 직관적 이해", "큰 수의 법칙"]
                    }
                ]
            }
        }
        
        return content_templates.get(module_id, {})
    
    def generate_assessment_items(self, objective_id: str, difficulty: str = "medium") -> List[Dict[str, Any]]:
        """학습 목표별 평가 문항 생성"""
        assessment_bank = {
            "desc_stats_1": [
                {
                    "type": "multiple_choice",
                    "difficulty": "easy",
                    "question": "다음 데이터셋 [1, 2, 3, 4, 100]에서 가장 적절한 중심경향성 측도는?",
                    "options": ["평균", "중앙값", "최빈값", "범위"],
                    "correct": "중앙값",
                    "explanation": "이상치(100)가 있을 때는 중앙값이 더 대표적인 값을 나타냅니다.",
                    "learning_objective": "중심경향성 측도의 적절한 선택"
                },
                {
                    "type": "interactive_problem",
                    "difficulty": "medium",
                    "question": "주어진 데이터의 평균을 계산하고, 이상치를 제거했을 때의 변화를 관찰하세요.",
                    "dataset": "interactive_dataset",
                    "required_actions": ["calculate_mean", "identify_outliers", "recalculate"],
                    "feedback": "contextual_hints"
                }
            ]
        }
        
        items = assessment_bank.get(objective_id, [])
        return [item for item in items if item.get('difficulty') == difficulty]


# 전역 재설계 시스템 인스턴스
learning_redesigner = LearningPathRedesigner()