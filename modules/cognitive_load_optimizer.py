"""
인지부하 최적화 모듈
- 인지부하 이론 기반 콘텐츠 설계
- 점진적 복잡성 증가
- 멀티미디어 학습 원리 적용
- 작업기억 용량 고려
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass
from enum import Enum


class CognitiveLoadType(Enum):
    """인지부하 유형"""
    INTRINSIC = "intrinsic"      # 내재적 부하 (개념 자체의 복잡성)
    EXTRANEOUS = "extraneous"    # 외재적 부하 (불필요한 인지 자원 소모)
    GERMANE = "germane"          # 관련적 부하 (스키마 형성을 위한 처리)


@dataclass
class ContentElement:
    """콘텐츠 요소 정의"""
    id: str
    type: str  # text, image, video, interactive, formula
    complexity_score: int  # 1-10
    cognitive_load_type: CognitiveLoadType
    processing_time: int  # seconds
    prerequisite_elements: List[str]
    cognitive_demands: Dict[str, int]  # visual, auditory, spatial, verbal


class CognitiveLoadOptimizer:
    """인지부하 최적화 클래스"""
    
    def __init__(self):
        self.working_memory_capacity = 7  # Miller의 마법의 숫자
        self.max_processing_time = 300  # 5분 단위
        self.multimedia_principles = self._setup_multimedia_principles()
        self.complexity_thresholds = self._setup_complexity_thresholds()
    
    def _setup_multimedia_principles(self) -> Dict[str, str]:
        """멀티미디어 학습 원리 설정"""
        return {
            "coherence": "불필요한 자료 제거",
            "signaling": "중요한 내용 강조",
            "redundancy": "시각-청각 정보 중복 방지", 
            "spatial_contiguity": "관련 정보 공간적 인접 배치",
            "temporal_contiguity": "관련 정보 시간적 동시 제시",
            "modality": "시각-청각 채널 균형 활용",
            "multimedia": "텍스트와 그래픽 조합",
            "personalization": "대화체 사용",
            "voice": "인간 음성 선호",
            "image": "사실적 이미지보다 단순한 그래픽"
        }
    
    def _setup_complexity_thresholds(self) -> Dict[str, Dict[str, int]]:
        """복잡성 임계값 설정"""
        return {
            "foundation": {
                "max_elements_per_screen": 5,
                "max_complexity_score": 15,
                "max_new_concepts": 2,
                "max_processing_time": 180
            },
            "developing": {
                "max_elements_per_screen": 7,
                "max_complexity_score": 25,
                "max_new_concepts": 3,
                "max_processing_time": 240
            },
            "proficient": {
                "max_elements_per_screen": 9,
                "max_complexity_score": 35,
                "max_new_concepts": 4,
                "max_processing_time": 300
            },
            "advanced": {
                "max_elements_per_screen": 12,
                "max_complexity_score": 45,
                "max_new_concepts": 5,
                "max_processing_time": 360
            }
        }
    
    def analyze_cognitive_load(self, content_elements: List[ContentElement], 
                             level: str) -> Dict[str, Any]:
        """콘텐츠의 인지부하 분석"""
        
        # 총 복잡성 점수 계산
        total_complexity = sum(element.complexity_score for element in content_elements)
        
        # 동시 처리 요소 수 계산
        simultaneous_elements = len([e for e in content_elements 
                                   if e.processing_time > 0])
        
        # 인지부하 유형별 분석
        load_by_type = {
            load_type.value: sum(e.complexity_score for e in content_elements 
                               if e.cognitive_load_type == load_type)
            for load_type in CognitiveLoadType
        }
        
        # 채널별 부하 분석
        channel_loads = {
            'visual': sum(e.cognitive_demands.get('visual', 0) for e in content_elements),
            'auditory': sum(e.cognitive_demands.get('auditory', 0) for e in content_elements),
            'spatial': sum(e.cognitive_demands.get('spatial', 0) for e in content_elements),
            'verbal': sum(e.cognitive_demands.get('verbal', 0) for e in content_elements)
        }
        
        # 임계값과 비교
        thresholds = self.complexity_thresholds[level]
        
        analysis = {
            "total_complexity": total_complexity,
            "simultaneous_elements": simultaneous_elements,
            "load_by_type": load_by_type,
            "channel_loads": channel_loads,
            "threshold_violations": self._check_threshold_violations(
                total_complexity, simultaneous_elements, thresholds
            ),
            "recommendations": self._generate_load_recommendations(
                content_elements, total_complexity, simultaneous_elements, thresholds
            )
        }
        
        return analysis
    
    def _check_threshold_violations(self, total_complexity: int, 
                                  simultaneous_elements: int,
                                  thresholds: Dict[str, int]) -> List[str]:
        """임계값 위반 사항 확인"""
        violations = []
        
        if total_complexity > thresholds["max_complexity_score"]:
            violations.append(f"총 복잡성 초과 ({total_complexity} > {thresholds['max_complexity_score']})")
        
        if simultaneous_elements > thresholds["max_elements_per_screen"]:
            violations.append(f"동시 처리 요소 초과 ({simultaneous_elements} > {thresholds['max_elements_per_screen']})")
        
        return violations
    
    def _generate_load_recommendations(self, content_elements: List[ContentElement],
                                     total_complexity: int, simultaneous_elements: int,
                                     thresholds: Dict[str, int]) -> List[str]:
        """인지부하 감소 권장사항 생성"""
        recommendations = []
        
        # 복잡성 감소 권장사항
        if total_complexity > thresholds["max_complexity_score"]:
            recommendations.extend([
                "콘텐츠를 더 작은 단위로 분할하세요",
                "비핵심 정보를 제거하거나 별도 섹션으로 이동하세요",
                "점진적 공개(progressive disclosure) 기법을 사용하세요"
            ])
        
        # 동시 처리 요소 감소 권장사항
        if simultaneous_elements > thresholds["max_elements_per_screen"]:
            recommendations.extend([
                "순차적 정보 제시를 고려하세요",
                "관련 정보를 그룹화하여 청킹(chunking)하세요",
                "중요도에 따라 정보를 계층화하세요"
            ])
        
        # 외재적 부하 감소 권장사항
        extraneous_load = sum(e.complexity_score for e in content_elements 
                            if e.cognitive_load_type == CognitiveLoadType.EXTRANEOUS)
        if extraneous_load > 5:
            recommendations.extend([
                "장식적 요소를 제거하세요",
                "일관된 디자인 패턴을 사용하세요",
                "내비게이션을 단순화하세요"
            ])
        
        return recommendations
    
    def optimize_content_sequence(self, content_elements: List[ContentElement]) -> List[ContentElement]:
        """콘텐츠 순서 최적화"""
        
        # 전제조건 기반 위상정렬
        sorted_elements = self._topological_sort(content_elements)
        
        # 인지부하 균형 조정
        balanced_sequence = self._balance_cognitive_load(sorted_elements)
        
        return balanced_sequence
    
    def _topological_sort(self, elements: List[ContentElement]) -> List[ContentElement]:
        """전제조건 기반 위상정렬"""
        # 간단한 위상정렬 구현
        result = []
        remaining = elements.copy()
        
        while remaining:
            # 전제조건이 모두 충족된 요소 찾기
            ready_elements = [
                elem for elem in remaining
                if all(prereq in [r.id for r in result] for prereq in elem.prerequisite_elements)
            ]
            
            if not ready_elements:
                # 순환 의존성이 있을 경우 임의로 하나 선택
                ready_elements = [remaining[0]]
            
            # 복잡성이 낮은 순서로 정렬
            ready_elements.sort(key=lambda x: x.complexity_score)
            
            selected = ready_elements[0]
            result.append(selected)
            remaining.remove(selected)
        
        return result
    
    def _balance_cognitive_load(self, elements: List[ContentElement]) -> List[ContentElement]:
        """인지부하 균형 조정"""
        balanced = []
        current_load = 0
        current_group = []
        
        for element in elements:
            # 현재 그룹에 추가했을 때의 부하 계산
            potential_load = current_load + element.complexity_score
            
            if potential_load <= self.working_memory_capacity and len(current_group) < 5:
                current_group.append(element)
                current_load = potential_load
            else:
                # 현재 그룹 완료 및 새 그룹 시작
                if current_group:
                    balanced.extend(current_group)
                current_group = [element]
                current_load = element.complexity_score
        
        # 마지막 그룹 추가
        if current_group:
            balanced.extend(current_group)
        
        return balanced
    
    def create_scaffolded_content(self, complex_concept: str, 
                                target_level: str) -> Dict[str, Any]:
        """복잡한 개념을 위한 스캐폴딩된 콘텐츠 생성"""
        
        scaffolding_strategies = {
            "conceptual_scaffolds": [
                "analogy_introduction",
                "visual_metaphor",
                "concrete_example",
                "abstract_principle"
            ],
            "procedural_scaffolds": [
                "worked_example",
                "guided_practice",
                "independent_practice",
                "transfer_application"
            ],
            "metacognitive_scaffolds": [
                "strategy_explanation",
                "self_monitoring_prompts",
                "reflection_questions",
                "error_analysis"
            ]
        }
        
        # 레벨별 스캐폴딩 강도 조정
        scaffolding_intensity = {
            "foundation": {"high": 4, "medium": 2, "low": 1},
            "developing": {"high": 3, "medium": 3, "low": 2},
            "proficient": {"high": 2, "medium": 3, "low": 3},
            "advanced": {"high": 1, "medium": 2, "low": 4}
        }
        
        intensity = scaffolding_intensity[target_level]
        
        scaffolded_content = {
            "concept": complex_concept,
            "level": target_level,
            "scaffolding_sequence": self._generate_scaffolding_sequence(
                complex_concept, scaffolding_strategies, intensity
            ),
            "assessment_checkpoints": self._create_assessment_checkpoints(complex_concept),
            "fade_out_schedule": self._create_fade_out_schedule(intensity)
        }
        
        return scaffolded_content
    
    def _generate_scaffolding_sequence(self, concept: str, 
                                     strategies: Dict[str, List[str]],
                                     intensity: Dict[str, int]) -> List[Dict[str, Any]]:
        """스캐폴딩 순서 생성"""
        sequence = []
        
        # 개념적 스캐폴딩
        for i in range(intensity["high"]):
            sequence.append({
                "type": "conceptual",
                "strategy": strategies["conceptual_scaffolds"][i % len(strategies["conceptual_scaffolds"])],
                "support_level": "high",
                "duration": "10-15분"
            })
        
        # 절차적 스캐폴딩
        for i in range(intensity["medium"]):
            sequence.append({
                "type": "procedural",
                "strategy": strategies["procedural_scaffolds"][i % len(strategies["procedural_scaffolds"])],
                "support_level": "medium",
                "duration": "15-20분"
            })
        
        # 메타인지적 스캐폴딩
        for i in range(intensity["low"]):
            sequence.append({
                "type": "metacognitive",
                "strategy": strategies["metacognitive_scaffolds"][i % len(strategies["metacognitive_scaffolds"])],
                "support_level": "low",
                "duration": "5-10분"
            })
        
        return sequence
    
    def _create_assessment_checkpoints(self, concept: str) -> List[Dict[str, str]]:
        """평가 체크포인트 생성"""
        return [
            {
                "checkpoint": "이해도 확인",
                "type": "conceptual_question",
                "timing": "개념 설명 후",
                "purpose": "기본 이해도 점검"
            },
            {
                "checkpoint": "적용 연습",
                "type": "guided_practice",
                "timing": "예제 학습 후",
                "purpose": "절차 숙련도 점검"
            },
            {
                "checkpoint": "전이 평가",
                "type": "novel_problem",
                "timing": "독립 연습 후",
                "purpose": "전이 능력 평가"
            }
        ]
    
    def _create_fade_out_schedule(self, intensity: Dict[str, int]) -> Dict[str, str]:
        """스캐폴딩 제거 일정"""
        return {
            "phase_1": "높은 지원 (첫 50% 진행)",
            "phase_2": "중간 지원 (다음 30% 진행)",
            "phase_3": "낮은 지원 (마지막 20% 진행)",
            "criteria": "학습자 성공률 80% 이상 시 다음 단계 진행"
        }
    
    def evaluate_multimedia_design(self, content_design: Dict[str, Any]) -> Dict[str, Any]:
        """멀티미디어 설계 평가"""
        
        evaluation = {
            "principle_compliance": {},
            "recommendations": [],
            "overall_score": 0
        }
        
        # 각 원리별 준수도 평가
        for principle, description in self.multimedia_principles.items():
            compliance_score = self._evaluate_principle_compliance(
                principle, content_design
            )
            evaluation["principle_compliance"][principle] = {
                "score": compliance_score,
                "description": description
            }
        
        # 전체 점수 계산
        total_score = sum(
            score["score"] for score in evaluation["principle_compliance"].values()
        )
        evaluation["overall_score"] = total_score / len(self.multimedia_principles)
        
        # 개선 권장사항 생성
        evaluation["recommendations"] = self._generate_multimedia_recommendations(
            evaluation["principle_compliance"]
        )
        
        return evaluation
    
    def _evaluate_principle_compliance(self, principle: str, 
                                     design: Dict[str, Any]) -> float:
        """개별 원리 준수도 평가"""
        # 간단한 휴리스틱 기반 평가
        # 실제 구현에서는 더 정교한 평가 알고리즘 필요
        
        compliance_checks = {
            "coherence": lambda d: 0.8 if d.get("extraneous_elements", 0) < 3 else 0.4,
            "signaling": lambda d: 0.9 if d.get("highlighting_used", False) else 0.3,
            "redundancy": lambda d: 0.7 if not d.get("text_audio_redundancy", True) else 0.2,
            "spatial_contiguity": lambda d: 0.8 if d.get("related_items_adjacent", True) else 0.4,
            "temporal_contiguity": lambda d: 0.9 if d.get("synchronized_presentation", True) else 0.3,
            "modality": lambda d: 0.8 if d.get("balanced_channels", True) else 0.5,
            "multimedia": lambda d: 0.9 if d.get("text_graphic_combination", True) else 0.6,
            "personalization": lambda d: 0.7 if d.get("conversational_style", False) else 0.8,
            "voice": lambda d: 0.8 if d.get("human_voice", True) else 0.6,
            "image": lambda d: 0.7 if d.get("simple_graphics", True) else 0.5
        }
        
        return compliance_checks.get(principle, lambda d: 0.5)(design)
    
    def _generate_multimedia_recommendations(self, compliance: Dict[str, Dict[str, float]]) -> List[str]:
        """멀티미디어 개선 권장사항 생성"""
        recommendations = []
        
        for principle, data in compliance.items():
            if data["score"] < 0.6:
                recommendations.append(f"{principle} 원리 개선 필요: {data['description']}")
        
        return recommendations


# 전역 인지부하 최적화 시스템
cognitive_optimizer = CognitiveLoadOptimizer()