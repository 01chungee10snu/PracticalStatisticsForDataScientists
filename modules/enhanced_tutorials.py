#!/usr/bin/env python3
"""
상세 설명 및 튜토리얼 모듈
- 단계별 학습 가이드
- 개념 설명과 예시
- 인터랙티브 학습 경험
"""

from typing import Dict, List, Any, Optional
import json
import random


class DetailedExplanationEngine:
    """상세 설명 엔진"""
    
    def __init__(self):
        self.explanation_templates = self._load_explanation_templates()
        self.example_database = self._create_example_database()
        self.misconception_database = self._create_misconception_database()
    
    def _load_explanation_templates(self) -> Dict[str, Dict[str, str]]:
        """설명 템플릿 로드"""
        return {
            "concept_introduction": {
                "template": "📚 {concept_name}는 {basic_definition}입니다.\n\n🎯 핵심 포인트:\n{key_points}\n\n💡 왜 중요한가요?\n{importance}",
                "example": "평균은 모든 데이터 값의 합을 개수로 나눈 값입니다."
            },
            "step_by_step": {
                "template": "📋 {concept_name} 계산 단계:\n\n{steps}\n\n✅ 확인사항:\n{checkpoints}",
                "example": "1단계: 모든 값을 더합니다\n2단계: 값의 개수를 셉니다\n3단계: 합을 개수로 나눕니다"
            },
            "comparison": {
                "template": "🔍 {concept1} vs {concept2}\n\n📊 공통점:\n{similarities}\n\n⚡ 차이점:\n{differences}\n\n🎯 언제 사용하나요?\n{usage_guide}",
                "example": "평균과 중앙값 모두 중심경향성을 나타내지만, 이상치에 대한 민감도가 다릅니다."
            },
            "practical_application": {
                "template": "🌍 실생활 적용: {scenario}\n\n📈 문제 상황:\n{problem}\n\n🔧 해결 과정:\n{solution_steps}\n\n📊 결과 해석:\n{interpretation}",
                "example": "학급 성적 분석에서 평균점수가 중앙값보다 낮다면 저점자들이 평균을 끌어내린 것입니다."
            }
        }
    
    def _create_example_database(self) -> Dict[str, List[Dict[str, Any]]]:
        """예시 데이터베이스 생성"""
        return {
            "descriptive_statistics": [
                {
                    "title": "학급 시험 점수 분석",
                    "scenario": "30명 학급의 수학 시험 점수를 분석해보겠습니다.",
                    "data": [85, 92, 78, 95, 88, 76, 91, 84, 87, 93, 82, 89, 77, 96, 83],
                    "analysis": {
                        "mean": "평균 = 1416 ÷ 15 = 94.4점",
                        "median": "중앙값 = 87점 (8번째 값)",
                        "interpretation": "평균이 중앙값보다 높아 상위권 학생들이 평균을 끌어올렸습니다."
                    },
                    "lessons": [
                        "이상치의 영향을 확인할 수 있습니다",
                        "분포의 치우침을 파악할 수 있습니다",
                        "적절한 대표값 선택의 중요성을 이해할 수 있습니다"
                    ]
                },
                {
                    "title": "직원 연봉 분포 분석",
                    "scenario": "회사 직원들의 연봉 분포를 분석해보겠습니다.",
                    "data": [3000, 3200, 3500, 3800, 4000, 4200, 4500, 8000],
                    "analysis": {
                        "mean": "평균 = 34200 ÷ 8 = 4275만원",
                        "median": "중앙값 = (3800 + 4000) ÷ 2 = 3900만원",
                        "interpretation": "CEO의 고연봉(8000만원)이 평균을 크게 끌어올렸습니다."
                    },
                    "lessons": [
                        "이상치가 평균에 미치는 영향",
                        "중앙값이 더 적절한 대표값인 경우",
                        "분포의 치우침 해석 방법"
                    ]
                }
            ],
            "probability_theory": [
                {
                    "title": "날씨 예보의 확률",
                    "scenario": "내일 비가 올 확률이 70%라는 일기예보의 의미를 알아보겠습니다.",
                    "explanation": "100일 중 비슷한 기상 조건에서 70일 정도 비가 왔다는 의미입니다.",
                    "misconception": "내일 70% 정도만 비가 온다는 뜻이 아닙니다.",
                    "lessons": [
                        "확률은 불확실성의 정도를 나타냅니다",
                        "과거 데이터에 기반한 예측입니다",
                        "100% 확실한 예측은 불가능합니다"
                    ]
                },
                {
                    "title": "복권 당첨 확률",
                    "scenario": "로또 1등 당첨 확률 1/8,145,060의 의미를 이해해보겠습니다.",
                    "visualization": "814만번 중 1번 당첨 = 0.000012%",
                    "comparison": "번개에 맞을 확률(1/100만)보다도 낮습니다",
                    "lessons": [
                        "매우 작은 확률의 의미",
                        "확률과 기댓값의 차이",
                        "확률론적 사고의 중요성"
                    ]
                }
            ],
            "inferential_statistics": [
                {
                    "title": "신약 효과 검증",
                    "scenario": "새로운 감기약의 효과를 검증하는 임상시험을 설계해보겠습니다.",
                    "hypothesis": {
                        "null": "H₀: 신약과 기존약의 효과가 같다",
                        "alternative": "H₁: 신약이 기존약보다 효과가 좋다"
                    },
                    "process": [
                        "환자 100명을 무작위로 두 그룹으로 나눕니다",
                        "한 그룹은 신약, 다른 그룹은 기존약을 복용합니다",
                        "치료 효과를 측정하고 통계적으로 비교합니다",
                        "유의수준 5%에서 가설을 검정합니다"
                    ],
                    "interpretation": "p값이 0.05보다 작으면 신약이 효과적이라고 결론짓습니다",
                    "lessons": [
                        "과학적 의사결정 과정",
                        "통계적 유의성의 의미",
                        "1종/2종 오류의 실제 영향"
                    ]
                }
            ]
        }
    
    def _create_misconception_database(self) -> Dict[str, List[Dict[str, str]]]:
        """흔한 오해 데이터베이스"""
        return {
            "descriptive_statistics": [
                {
                    "misconception": "평균이 항상 가장 좋은 대표값이다",
                    "reality": "이상치가 있을 때는 중앙값이 더 적절할 수 있습니다",
                    "example": "억만장자가 포함된 소득 조사에서는 중앙값이 더 현실적입니다"
                },
                {
                    "misconception": "표준편차가 클수록 나쁜 것이다",
                    "reality": "표준편차는 단순히 분산의 정도를 나타낼 뿐입니다",
                    "example": "투자 수익률의 표준편차가 크면 위험하지만 기회도 클 수 있습니다"
                }
            ],
            "probability_theory": [
                {
                    "misconception": "확률 50%는 절반만 일어난다는 뜻이다",
                    "reality": "장기적으로 50% 정도의 빈도로 일어난다는 의미입니다",
                    "example": "동전 던지기에서 앞면이 연속 5번 나와도 다음에 뒷면이 나올 확률은 여전히 50%입니다"
                },
                {
                    "misconception": "확률이 높으면 반드시 일어난다",
                    "reality": "확률은 가능성의 정도를 나타낼 뿐 확실성을 보장하지 않습니다",
                    "example": "90% 확률의 비 예보에도 비가 안 올 수 있습니다"
                }
            ],
            "inferential_statistics": [
                {
                    "misconception": "p값이 가설이 참일 확률이다",
                    "reality": "p값은 귀무가설이 참일 때 현재 결과가 나올 확률입니다",
                    "example": "p=0.05는 귀무가설이 참이라면 이런 결과가 나올 확률이 5%라는 뜻입니다"
                },
                {
                    "misconception": "통계적 유의성이 실질적 중요성을 의미한다",
                    "reality": "통계적으로 유의해도 실제로는 중요하지 않을 수 있습니다",
                    "example": "약효가 0.1% 증가해도 표본이 크면 통계적으로 유의할 수 있습니다"
                }
            ]
        }
    
    def generate_detailed_explanation(self, concept: str, level: str = "basic") -> Dict[str, Any]:
        """상세 설명 생성"""
        explanation = {
            "concept": concept,
            "level": level,
            "sections": []
        }
        
        # 기본 개념 소개
        explanation["sections"].append(self._create_introduction_section(concept))
        
        # 단계별 설명
        if level in ["intermediate", "advanced"]:
            explanation["sections"].append(self._create_stepby_step_section(concept))
        
        # 실생활 예시
        explanation["sections"].append(self._create_examples_section(concept))
        
        # 흔한 오해
        explanation["sections"].append(self._create_misconceptions_section(concept))
        
        # 고급 단계에서는 비교 분석 추가
        if level == "advanced":
            explanation["sections"].append(self._create_comparison_section(concept))
        
        return explanation
    
    def _create_introduction_section(self, concept: str) -> Dict[str, Any]:
        """개념 소개 섹션"""
        concept_definitions = {
            "평균": {
                "definition": "모든 데이터 값의 합을 데이터 개수로 나눈 값",
                "importance": "데이터의 중심을 나타내는 가장 기본적인 통계량으로, 데이터의 전반적인 수준을 파악할 수 있습니다.",
                "key_points": [
                    "모든 데이터 값이 계산에 사용됩니다",
                    "이상치에 민감하게 반응합니다",
                    "가장 널리 사용되는 중심경향성 지표입니다"
                ]
            },
            "중앙값": {
                "definition": "데이터를 크기 순으로 정렬했을 때 중간에 위치하는 값",
                "importance": "이상치의 영향을 받지 않아 왜곡된 분포에서 더 안정적인 중심값을 제공합니다.",
                "key_points": [
                    "전체 데이터의 50%가 이 값보다 작습니다",
                    "이상치에 영향받지 않습니다",
                    "순서 통계량의 대표적인 예입니다"
                ]
            },
            "확률": {
                "definition": "어떤 사건이 일어날 가능성을 0과 1 사이의 수로 나타낸 것",
                "importance": "불확실한 상황에서 의사결정을 하기 위한 수학적 도구로, 예측과 위험 평가의 기초가 됩니다.",
                "key_points": [
                    "0 이상 1 이하의 값을 가집니다",
                    "모든 가능한 사건의 확률 합은 1입니다",
                    "상대빈도의 극한으로 해석할 수 있습니다"
                ]
            }
        }
        
        concept_info = concept_definitions.get(concept, {
            "definition": f"{concept}의 정의를 학습합니다",
            "importance": f"{concept}는 통계학의 중요한 개념입니다",
            "key_points": [f"{concept}의 핵심을 이해해보세요"]
        })
        
        return {
            "type": "introduction",
            "title": f"📚 {concept} 개념 소개",
            "content": {
                "definition": concept_info["definition"],
                "importance": concept_info["importance"],
                "key_points": concept_info["key_points"]
            }
        }
    
    def _create_stepby_step_section(self, concept: str) -> Dict[str, Any]:
        """단계별 설명 섹션"""
        step_guides = {
            "평균": [
                {"step": 1, "action": "모든 데이터 값을 더합니다", "detail": "누락된 값이 없는지 확인하세요"},
                {"step": 2, "action": "데이터의 개수를 셉니다", "detail": "N = 전체 데이터 포인트 수"},
                {"step": 3, "action": "합을 개수로 나눕니다", "detail": "평균 = 합계 ÷ N"},
                {"step": 4, "action": "결과를 해석합니다", "detail": "이상치나 분포의 치우침을 고려하세요"}
            ],
            "확률": [
                {"step": 1, "action": "전체 가능한 경우의 수를 파악합니다", "detail": "표본공간 S의 크기"},
                {"step": 2, "action": "관심 있는 사건의 경우의 수를 셉니다", "detail": "사건 A에 포함된 원소의 개수"},
                {"step": 3, "action": "확률을 계산합니다", "detail": "P(A) = |A| / |S|"},
                {"step": 4, "action": "결과가 합리적인지 확인합니다", "detail": "0 ≤ P(A) ≤ 1 인지 검증"}
            ]
        }
        
        steps = step_guides.get(concept, [
            {"step": 1, "action": f"{concept} 학습 시작", "detail": "기본 개념부터 차근차근"}
        ])
        
        return {
            "type": "step_by_step",
            "title": f"📋 {concept} 계산 단계",
            "content": {
                "steps": steps,
                "tips": [
                    "각 단계를 차근차근 따라해보세요",
                    "계산 과정을 기록해두면 나중에 검토하기 쉽습니다",
                    "실수가 생기기 쉬운 단계에 특히 주의하세요"
                ]
            }
        }
    
    def _create_examples_section(self, concept: str) -> Dict[str, Any]:
        """실생활 예시 섹션"""
        category_mapping = {
            "평균": "descriptive_statistics",
            "중앙값": "descriptive_statistics", 
            "표준편차": "descriptive_statistics",
            "확률": "probability_theory",
            "가설검정": "inferential_statistics"
        }
        
        category = category_mapping.get(concept, "descriptive_statistics")
        examples = self.example_database.get(category, [])
        
        if examples:
            selected_example = random.choice(examples)
        else:
            selected_example = {
                "title": f"{concept} 활용 예시",
                "scenario": f"{concept}를 실생활에 적용해보겠습니다.",
                "lessons": [f"{concept}의 실용성을 이해할 수 있습니다"]
            }
        
        return {
            "type": "examples",
            "title": f"🌍 {concept} 실생활 예시",
            "content": selected_example
        }
    
    def _create_misconceptions_section(self, concept: str) -> Dict[str, Any]:
        """흔한 오해 섹션"""
        category_mapping = {
            "평균": "descriptive_statistics",
            "중앙값": "descriptive_statistics",
            "표준편차": "descriptive_statistics", 
            "확률": "probability_theory",
            "가설검정": "inferential_statistics"
        }
        
        category = category_mapping.get(concept, "descriptive_statistics")
        misconceptions = self.misconception_database.get(category, [])
        
        return {
            "type": "misconceptions",
            "title": f"⚠️ {concept} 관련 흔한 오해",
            "content": {
                "misconceptions": misconceptions,
                "advice": [
                    "개념을 정확히 이해하는 것이 중요합니다",
                    "다양한 예시를 통해 개념을 확인해보세요",
                    "의심스러울 때는 정의로 돌아가세요"
                ]
            }
        }
    
    def _create_comparison_section(self, concept: str) -> Dict[str, Any]:
        """비교 분석 섹션"""
        comparisons = {
            "평균": {
                "compare_with": "중앙값",
                "similarities": [
                    "둘 다 중심경향성을 나타내는 지표입니다",
                    "데이터의 대표값으로 사용됩니다",
                    "분포의 중심을 파악하는 데 도움이 됩니다"
                ],
                "differences": [
                    "평균은 모든 값을 사용하지만, 중앙값은 순서만 중요합니다",
                    "평균은 이상치에 민감하지만, 중앙값은 강건합니다",
                    "평균은 수치연산이 가능하지만, 중앙값은 순서연산만 가능합니다"
                ],
                "when_to_use": {
                    "평균": "정규분포나 대칭분포에서, 이상치가 없을 때",
                    "중앙값": "치우친 분포에서, 이상치가 있을 때"
                }
            }
        }
        
        comparison_data = comparisons.get(concept)
        if not comparison_data:
            return {
                "type": "comparison",
                "title": f"🔍 {concept} 비교 분석",
                "content": {"message": f"{concept}에 대한 비교 분석을 준비 중입니다."}
            }
        
        return {
            "type": "comparison", 
            "title": f"🔍 {concept} vs {comparison_data['compare_with']}",
            "content": comparison_data
        }


class InteractiveTutorialEngine:
    """인터랙티브 튜토리얼 엔진"""
    
    def __init__(self):
        self.explanation_engine = DetailedExplanationEngine()
        self.tutorial_templates = self._create_tutorial_templates()
    
    def _create_tutorial_templates(self) -> Dict[str, Any]:
        """튜토리얼 템플릿 생성"""
        return {
            "guided_discovery": {
                "name": "안내된 발견 학습",
                "description": "질문을 통해 스스로 개념을 발견하도록 유도",
                "structure": ["motivation", "exploration", "formalization", "application", "reflection"]
            },
            "worked_examples": {
                "name": "단계별 예시 학습",
                "description": "전문가의 문제 해결 과정을 단계별로 따라하기",
                "structure": ["problem_setup", "solution_planning", "step_execution", "verification", "generalization"]
            },
            "conceptual_change": {
                "name": "개념 변화 학습",
                "description": "기존 오개념을 수정하고 올바른 개념 형성",
                "structure": ["misconception_elicitation", "cognitive_conflict", "concept_reconstruction", "reinforcement"]
            }
        }
    
    def create_interactive_tutorial(self, content_id: str, user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """맞춤형 인터랙티브 튜토리얼 생성"""
        tutorial = {
            "tutorial_id": f"interactive_{content_id}_{user_profile.get('user_id', 'anonymous')}",
            "title": f"🎯 {content_id} 완전 정복 튜토리얼",
            "personalization": self._analyze_user_needs(user_profile),
            "modules": []
        }
        
        # 사용자 프로필에 따른 튜토리얼 구성
        if user_profile.get("experience_level", "beginner") == "beginner":
            tutorial["modules"].extend(self._create_beginner_modules(content_id))
        elif user_profile.get("experience_level") == "intermediate":
            tutorial["modules"].extend(self._create_intermediate_modules(content_id))
        else:
            tutorial["modules"].extend(self._create_advanced_modules(content_id))
        
        # 공통 모듈 추가
        tutorial["modules"].extend(self._create_common_modules(content_id))
        
        return tutorial
    
    def _analyze_user_needs(self, user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """사용자 요구 분석"""
        return {
            "learning_style": user_profile.get("learning_style", "visual"),
            "difficulty_preference": user_profile.get("difficulty_preference", 5),
            "time_availability": user_profile.get("time_availability", "medium"),
            "goals": user_profile.get("goals", ["기본 이해"]),
            "recommended_approach": self._recommend_approach(user_profile)
        }
    
    def _recommend_approach(self, user_profile: Dict[str, Any]) -> str:
        """학습 접근법 추천"""
        style = user_profile.get("learning_style", "visual")
        experience = user_profile.get("experience_level", "beginner")
        
        if style == "kinesthetic" and experience == "beginner":
            return "hands_on_exploration"
        elif style == "visual":
            return "diagram_based_learning"
        elif experience == "advanced":
            return "problem_solving_focus"
        else:
            return "step_by_step_guidance"
    
    def _create_beginner_modules(self, content_id: str) -> List[Dict[str, Any]]:
        """초보자용 모듈"""
        return [
            {
                "module_id": "foundation_building",
                "title": "🏗️ 기초 다지기",
                "type": "conceptual_introduction",
                "estimated_time": "10-15분",
                "activities": [
                    {
                        "type": "warm_up",
                        "title": "생각해보기",
                        "content": "일상생활에서 이 개념을 어떻게 사용하고 있을까요?",
                        "interaction": "reflection_questions"
                    },
                    {
                        "type": "concept_introduction",
                        "title": "개념 만나기",
                        "content": "핵심 개념을 쉬운 언어로 소개합니다",
                        "interaction": "guided_reading"
                    }
                ]
            },
            {
                "module_id": "gentle_practice",
                "title": "🚶 천천히 연습하기",
                "type": "guided_practice",
                "estimated_time": "15-20분",
                "activities": [
                    {
                        "type": "worked_example",
                        "title": "함께 풀어보기",
                        "content": "단계별로 함께 문제를 해결해봅시다",
                        "interaction": "step_by_step_guidance"
                    },
                    {
                        "type": "simple_practice",
                        "title": "혼자 해보기",
                        "content": "비슷한 문제를 스스로 풀어보세요",
                        "interaction": "immediate_feedback"
                    }
                ]
            }
        ]
    
    def _create_intermediate_modules(self, content_id: str) -> List[Dict[str, Any]]:
        """중급자용 모듈"""
        return [
            {
                "module_id": "concept_deepening",
                "title": "🔍 개념 심화",
                "type": "analytical_thinking",
                "estimated_time": "15-20분",
                "activities": [
                    {
                        "type": "case_analysis",
                        "title": "사례 분석",
                        "content": "실제 사례를 통해 개념의 적용을 이해합니다",
                        "interaction": "critical_thinking"
                    },
                    {
                        "type": "pattern_recognition",
                        "title": "패턴 찾기",
                        "content": "다양한 상황에서 공통 패턴을 발견해보세요",
                        "interaction": "pattern_matching"
                    }
                ]
            },
            {
                "module_id": "application_practice",
                "title": "🎯 응용 연습",
                "type": "problem_solving",
                "estimated_time": "20-25분",
                "activities": [
                    {
                        "type": "scenario_solving",
                        "title": "상황별 문제 해결",
                        "content": "다양한 시나리오에서 개념을 적용해보세요",
                        "interaction": "scenario_based_learning"
                    }
                ]
            }
        ]
    
    def _create_advanced_modules(self, content_id: str) -> List[Dict[str, Any]]:
        """고급자용 모듈"""
        return [
            {
                "module_id": "theoretical_exploration",
                "title": "📚 이론적 탐구",
                "type": "theoretical_understanding",
                "estimated_time": "20-30분",
                "activities": [
                    {
                        "type": "derivation_understanding",
                        "title": "원리 이해",
                        "content": "수학적/이론적 배경을 깊이 있게 탐구합니다",
                        "interaction": "mathematical_reasoning"
                    },
                    {
                        "type": "connection_mapping",
                        "title": "개념 연결",
                        "content": "다른 개념들과의 연관성을 파악해보세요",
                        "interaction": "concept_mapping"
                    }
                ]
            },
            {
                "module_id": "expert_challenges",
                "title": "🏆 전문가 도전",
                "type": "advanced_problem_solving",
                "estimated_time": "25-35분",
                "activities": [
                    {
                        "type": "complex_scenarios",
                        "title": "복합 문제 해결",
                        "content": "여러 개념을 통합하여 복잡한 문제를 해결합니다",
                        "interaction": "multi_step_reasoning"
                    }
                ]
            }
        ]
    
    def _create_common_modules(self, content_id: str) -> List[Dict[str, Any]]:
        """공통 모듈"""
        return [
            {
                "module_id": "misconception_check",
                "title": "⚠️ 오개념 점검",
                "type": "error_correction",
                "estimated_time": "10분",
                "activities": [
                    {
                        "type": "misconception_quiz",
                        "title": "흔한 실수 확인",
                        "content": "자주 발생하는 오해를 점검해보세요",
                        "interaction": "diagnostic_assessment"
                    }
                ]
            },
            {
                "module_id": "synthesis_reflection",
                "title": "🎭 종합 및 성찰",
                "type": "metacognitive_reflection",
                "estimated_time": "10-15분",
                "activities": [
                    {
                        "type": "learning_synthesis",
                        "title": "학습 정리",
                        "content": "오늘 배운 내용을 자신만의 언어로 정리해보세요",
                        "interaction": "self_explanation"
                    },
                    {
                        "type": "future_application",
                        "title": "활용 계획",
                        "content": "앞으로 이 지식을 어떻게 활용할지 계획해보세요",
                        "interaction": "goal_setting"
                    }
                ]
            }
        ]
    
    def generate_interactive_activity(self, activity_type: str, content: str, user_level: str = "intermediate") -> Dict[str, Any]:
        """인터랙티브 활동 생성"""
        activities = {
            "concept_mapping": self._create_concept_mapping_activity,
            "case_study": self._create_case_study_activity,
            "simulation": self._create_simulation_activity,
            "problem_solving": self._create_problem_solving_activity,
            "reflection": self._create_reflection_activity
        }
        
        activity_creator = activities.get(activity_type, self._create_default_activity)
        return activity_creator(content, user_level)
    
    def _create_concept_mapping_activity(self, content: str, user_level: str) -> Dict[str, Any]:
        """개념 지도 활동"""
        return {
            "activity_type": "concept_mapping",
            "title": "🗺️ 개념 연결하기",
            "instructions": f"{content}와 관련된 개념들 사이의 관계를 파악해보세요",
            "materials": {
                "central_concept": content,
                "related_concepts": self._get_related_concepts(content),
                "relationship_types": ["원인-결과", "상위-하위", "대조", "유사"]
            },
            "interaction_type": "drag_and_drop",
            "assessment": "peer_review",
            "time_estimate": "15-20분"
        }
    
    def _create_case_study_activity(self, content: str, user_level: str) -> Dict[str, Any]:
        """사례 연구 활동"""
        return {
            "activity_type": "case_study",
            "title": "🔍 실제 사례 분석",
            "scenario": self._generate_realistic_scenario(content),
            "questions": self._generate_analysis_questions(content, user_level),
            "interaction_type": "guided_analysis",
            "assessment": "rubric_based",
            "time_estimate": "20-30분"
        }
    
    def _get_related_concepts(self, content: str) -> List[str]:
        """관련 개념 목록 반환"""
        concept_networks = {
            "평균": ["중앙값", "최빈값", "표준편차", "분산", "이상치"],
            "확률": ["표본공간", "사건", "조건부확률", "독립성", "베이즈정리"],
            "가설검정": ["귀무가설", "대립가설", "유의수준", "p값", "신뢰구간"]
        }
        return concept_networks.get(content, [])
    
    def _generate_realistic_scenario(self, content: str) -> str:
        """현실적인 시나리오 생성"""
        scenarios = {
            "평균": "한 회사의 인사팀에서 신입사원 채용을 위해 지원자들의 평가 점수를 분석하고 있습니다.",
            "확률": "보험회사에서 새로운 상품의 위험도를 평가하기 위해 과거 데이터를 분석하고 있습니다.",
            "가설검정": "제약회사에서 새로운 치료제의 효과를 검증하기 위한 임상시험을 설계하고 있습니다."
        }
        return scenarios.get(content, f"{content}를 실제 상황에 적용하는 사례입니다.")
    
    def _generate_analysis_questions(self, content: str, user_level: str) -> List[str]:
        """분석 질문 생성"""
        if user_level == "beginner":
            return [
                f"이 상황에서 {content}는 어떤 역할을 하나요?",
                "어떤 점이 주목할 만한가요?",
                "다른 방법도 가능할까요?"
            ]
        elif user_level == "intermediate":
            return [
                f"{content}를 적용할 때 고려해야 할 요소는 무엇인가요?",
                "이 방법의 장단점은 무엇인가요?",
                "다른 상황에서는 어떻게 달라질까요?"
            ]
        else:
            return [
                f"{content}의 이론적 가정이 현실에서 성립하나요?",
                "한계점과 개선 방안은 무엇인가요?",
                "대안적 접근법의 가능성은 어떤가요?"
            ]
    
    def _create_simulation_activity(self, content: str, user_level: str) -> Dict[str, Any]:
        """시뮬레이션 활동"""
        return {
            "activity_type": "simulation",
            "title": "🎮 가상 실험",
            "description": f"{content} 개념을 가상 환경에서 실험해보세요",
            "parameters": self._get_simulation_parameters(content),
            "interaction_type": "parameter_adjustment",
            "assessment": "experimentation_log",
            "time_estimate": "25-35분"
        }
    
    def _get_simulation_parameters(self, content: str) -> Dict[str, Any]:
        """시뮬레이션 매개변수"""
        parameters = {
            "평균": {
                "variables": ["데이터 크기", "이상치 포함 여부", "분포 타입"],
                "outputs": ["평균값", "중앙값과의 차이", "안정성"]
            },
            "확률": {
                "variables": ["시행 횟수", "성공 확률", "독립성 조건"],
                "outputs": ["관찰된 빈도", "이론적 확률과의 차이", "신뢰구간"]
            }
        }
        return parameters.get(content, {"variables": [], "outputs": []})
    
    def _create_problem_solving_activity(self, content: str, user_level: str) -> Dict[str, Any]:
        """문제 해결 활동"""
        return {
            "activity_type": "problem_solving",
            "title": "🧩 문제 해결 도전",
            "problem_set": self._generate_problem_set(content, user_level),
            "scaffolding": self._get_problem_scaffolding(user_level),
            "interaction_type": "step_by_step_solution",
            "assessment": "solution_quality",
            "time_estimate": "20-30분"
        }
    
    def _generate_problem_set(self, content: str, user_level: str) -> List[Dict[str, Any]]:
        """문제 세트 생성"""
        # 실제 구현에서는 더 정교한 문제 생성 로직 필요
        difficulty_levels = {
            "beginner": [1, 2, 3],
            "intermediate": [3, 4, 5],
            "advanced": [5, 6, 7]
        }
        
        levels = difficulty_levels.get(user_level, [3, 4, 5])
        
        return [
            {
                "problem_id": f"{content}_problem_{i}",
                "difficulty": level,
                "content": f"난이도 {level}의 {content} 문제",
                "hints": [f"힌트 1", f"힌트 2"],
                "solution_steps": []
            }
            for i, level in enumerate(levels, 1)
        ]
    
    def _get_problem_scaffolding(self, user_level: str) -> Dict[str, Any]:
        """문제 해결 지원"""
        scaffolding = {
            "beginner": {
                "hints_available": 3,
                "step_guidance": True,
                "immediate_feedback": True,
                "retry_unlimited": True
            },
            "intermediate": {
                "hints_available": 2,
                "step_guidance": False,
                "immediate_feedback": True,
                "retry_unlimited": True
            },
            "advanced": {
                "hints_available": 1,
                "step_guidance": False,
                "immediate_feedback": False,
                "retry_unlimited": False
            }
        }
        return scaffolding.get(user_level, scaffolding["intermediate"])
    
    def _create_reflection_activity(self, content: str, user_level: str) -> Dict[str, Any]:
        """성찰 활동"""
        return {
            "activity_type": "reflection",
            "title": "🤔 학습 성찰",
            "prompts": self._get_reflection_prompts(content, user_level),
            "interaction_type": "written_response",
            "assessment": "self_assessment",
            "time_estimate": "10-15분"
        }
    
    def _get_reflection_prompts(self, content: str, user_level: str) -> List[str]:
        """성찰 질문"""
        return [
            f"{content}에 대해 새롭게 알게 된 점은 무엇인가요?",
            "가장 어려웠던 부분은 무엇이고, 어떻게 극복했나요?",
            "이 지식을 실생활에서 어떻게 활용할 수 있을까요?",
            "다음에 더 배우고 싶은 관련 주제는 무엇인가요?"
        ]
    
    def _create_default_activity(self, content: str, user_level: str) -> Dict[str, Any]:
        """기본 활동"""
        return {
            "activity_type": "default",
            "title": f"📚 {content} 학습 활동",
            "description": f"{content}에 대한 기본 학습 활동입니다",
            "interaction_type": "reading_comprehension",
            "time_estimate": "15분"
        }


# 전역 인스턴스
explanation_engine = DetailedExplanationEngine()
tutorial_engine = InteractiveTutorialEngine()