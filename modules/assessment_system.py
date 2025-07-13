"""
전문 평가 및 인증 시스템
- 적응형 평가 알고리즘
- 실시간 난이도 조정
- 종합적인 학습 진단
- 전문 인증서 발급
"""

import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import numpy as np
from pathlib import Path
import hashlib
import base64

class QuestionType(Enum):
    """문제 유형"""
    MULTIPLE_CHOICE = "multiple_choice"
    TRUE_FALSE = "true_false"
    FILL_BLANK = "fill_blank"
    CALCULATION = "calculation"
    INTERPRETATION = "interpretation"
    CODE_COMPLETION = "code_completion"
    CASE_STUDY = "case_study"

class DifficultyLevel(Enum):
    """난이도 레벨"""
    FOUNDATION = 1      # 기초
    DEVELOPING = 2      # 발전
    PROFICIENT = 3      # 숙련
    ADVANCED = 4        # 고급
    EXPERT = 5          # 전문가

class AssessmentType(Enum):
    """평가 유형"""
    FORMATIVE = "formative"        # 형성평가 (학습 중)
    SUMMATIVE = "summative"        # 총괄평가 (단원 마무리)
    DIAGNOSTIC = "diagnostic"      # 진단평가 (사전 지식 확인)
    CERTIFICATION = "certification" # 인증평가 (자격증)

@dataclass
class Question:
    """문제 데이터 구조"""
    id: str
    type: QuestionType
    difficulty: DifficultyLevel
    topic: str
    subtopic: str
    question_text: str
    options: List[str]
    correct_answer: str
    explanation: str
    hints: List[str]
    tags: List[str]
    estimated_time: int  # 예상 소요 시간 (초)
    cognitive_level: str  # bloom's taxonomy level
    prerequisite_concepts: List[str]
    
class QuestionBank:
    """문제 은행 관리"""
    
    def __init__(self):
        self.questions: Dict[str, Question] = {}
        self.question_statistics: Dict[str, Dict] = {}
        self._load_question_bank()
    
    def _load_question_bank(self):
        """문제 은행 데이터 로드"""
        # 실제 환경에서는 데이터베이스에서 로드
        self._generate_sample_questions()
    
    def _generate_sample_questions(self):
        """샘플 문제 생성"""
        sample_questions = [
            {
                "id": "stats_basic_001",
                "type": QuestionType.MULTIPLE_CHOICE,
                "difficulty": DifficultyLevel.FOUNDATION,
                "topic": "descriptive_statistics",
                "subtopic": "measures_of_central_tendency",
                "question_text": "다음 데이터의 평균은 얼마입니까? [2, 4, 6, 8, 10]",
                "options": ["5", "6", "7", "8"],
                "correct_answer": "6",
                "explanation": "평균 = (2+4+6+8+10) ÷ 5 = 30 ÷ 5 = 6",
                "hints": ["모든 값을 더한 후 개수로 나누세요", "2+4+6+8+10 = 30"],
                "tags": ["mean", "average", "basic_calculation"],
                "estimated_time": 60,
                "cognitive_level": "application",
                "prerequisite_concepts": ["basic_arithmetic"]
            },
            {
                "id": "stats_inter_001",
                "type": QuestionType.INTERPRETATION,
                "difficulty": DifficultyLevel.PROFICIENT,
                "topic": "hypothesis_testing",
                "subtopic": "p_value_interpretation",
                "question_text": "p-value가 0.03일 때, 유의수준 α=0.05에서 어떤 결론을 내릴 수 있습니까?",
                "options": [
                    "귀무가설을 기각한다",
                    "귀무가설을 채택한다", 
                    "대립가설을 기각한다",
                    "결론을 내릴 수 없다"
                ],
                "correct_answer": "귀무가설을 기각한다",
                "explanation": "p-value(0.03) < α(0.05)이므로 귀무가설을 기각하고 대립가설을 채택합니다.",
                "hints": ["p-value와 유의수준을 비교하세요", "p < α일 때의 의미를 생각해보세요"],
                "tags": ["hypothesis_testing", "p_value", "statistical_inference"],
                "estimated_time": 120,
                "cognitive_level": "analysis",
                "prerequisite_concepts": ["hypothesis_testing_basics", "significance_level"]
            },
            {
                "id": "stats_adv_001",
                "type": QuestionType.CALCULATION,
                "difficulty": DifficultyLevel.ADVANCED,
                "topic": "regression_analysis",
                "subtopic": "linear_regression",
                "question_text": "다음 회귀식에서 R² = 0.85가 의미하는 바를 설명하고, 이 모델의 설명력을 평가하세요.",
                "options": [],
                "correct_answer": "독립변수가 종속변수 변동의 85%를 설명함. 높은 설명력을 가진 모델임.",
                "explanation": "R²는 결정계수로, 독립변수가 종속변수의 변동을 얼마나 설명하는지 나타냅니다. 0.85는 85%의 변동을 설명함을 의미하며, 일반적으로 높은 설명력으로 평가됩니다.",
                "hints": ["R²의 정의를 생각해보세요", "0.85는 퍼센트로 어떻게 해석됩니까?"],
                "tags": ["regression", "r_squared", "model_evaluation"],
                "estimated_time": 180,
                "cognitive_level": "evaluation",
                "prerequisite_concepts": ["correlation", "regression_basics", "variance"]
            }
        ]
        
        for q_data in sample_questions:
            question = Question(**q_data)
            self.questions[question.id] = question
            self.question_statistics[question.id] = {
                "attempts": 0,
                "correct_attempts": 0,
                "average_time": 0,
                "difficulty_rating": question.difficulty.value
            }
    
    def get_questions_by_criteria(
        self, 
        topic: Optional[str] = None,
        difficulty: Optional[DifficultyLevel] = None,
        question_type: Optional[QuestionType] = None,
        tags: Optional[List[str]] = None,
        limit: int = 10
    ) -> List[Question]:
        """조건에 맞는 문제 검색"""
        filtered_questions = []
        
        for question in self.questions.values():
            # 토픽 필터
            if topic and question.topic != topic:
                continue
            
            # 난이도 필터
            if difficulty and question.difficulty != difficulty:
                continue
            
            # 문제 유형 필터
            if question_type and question.type != question_type:
                continue
            
            # 태그 필터
            if tags and not any(tag in question.tags for tag in tags):
                continue
            
            filtered_questions.append(question)
        
        # 난이도와 통계 기반 정렬
        filtered_questions.sort(key=lambda q: (
            q.difficulty.value,
            self.question_statistics[q.id]["difficulty_rating"]
        ))
        
        return filtered_questions[:limit]
    
    def update_question_statistics(self, question_id: str, correct: bool, time_taken: int):
        """문제 통계 업데이트"""
        if question_id not in self.question_statistics:
            return
        
        stats = self.question_statistics[question_id]
        stats["attempts"] += 1
        
        if correct:
            stats["correct_attempts"] += 1
        
        # 평균 시간 업데이트
        current_avg = stats["average_time"]
        stats["average_time"] = (current_avg * (stats["attempts"] - 1) + time_taken) / stats["attempts"]
        
        # 난이도 재계산 (정답률 기반)
        success_rate = stats["correct_attempts"] / stats["attempts"]
        if success_rate > 0.8:
            stats["difficulty_rating"] = max(1, stats["difficulty_rating"] - 0.1)
        elif success_rate < 0.4:
            stats["difficulty_rating"] = min(5, stats["difficulty_rating"] + 0.1)

@dataclass
class AssessmentResponse:
    """평가 응답"""
    question_id: str
    user_answer: str
    is_correct: bool
    time_taken: int
    hints_used: int
    confidence_level: int  # 1-5
    timestamp: datetime

@dataclass
class AssessmentSession:
    """평가 세션"""
    session_id: str
    user_id: str
    assessment_type: AssessmentType
    topic: str
    start_time: datetime
    end_time: Optional[datetime]
    questions: List[str]  # question IDs
    responses: List[AssessmentResponse]
    current_question_index: int
    score: float
    max_score: float
    is_completed: bool
    adaptive_parameters: Dict[str, Any]

class AdaptiveAssessmentEngine:
    """적응형 평가 엔진"""
    
    def __init__(self, question_bank: QuestionBank):
        self.question_bank = question_bank
        self.active_sessions: Dict[str, AssessmentSession] = {}
        self.completed_sessions: List[AssessmentSession] = []
        
        # CAT (Computer Adaptive Testing) 매개변수
        self.cat_parameters = {
            "initial_difficulty": 3,        # 초기 난이도
            "difficulty_adjustment": 0.5,   # 난이도 조정 폭
            "min_questions": 5,             # 최소 문제 수
            "max_questions": 20,            # 최대 문제 수
            "precision_threshold": 0.3,     # 정밀도 임계값
            "confidence_interval": 0.95     # 신뢰구간
        }
    
    def start_assessment(
        self, 
        user_id: str, 
        assessment_type: AssessmentType,
        topic: str,
        initial_difficulty: Optional[int] = None
    ) -> str:
        """평가 시작"""
        session_id = str(uuid.uuid4())
        
        # 초기 난이도 설정
        if initial_difficulty is None:
            initial_difficulty = self._estimate_user_ability(user_id, topic)
        
        # 첫 번째 문제 선택
        first_question = self._select_next_question(
            topic, 
            DifficultyLevel(initial_difficulty),
            []  # 이미 출제된 문제 없음
        )
        
        session = AssessmentSession(
            session_id=session_id,
            user_id=user_id,
            assessment_type=assessment_type,
            topic=topic,
            start_time=datetime.now(),
            end_time=None,
            questions=[first_question.id] if first_question else [],
            responses=[],
            current_question_index=0,
            score=0.0,
            max_score=0.0,
            is_completed=False,
            adaptive_parameters={
                "current_difficulty": initial_difficulty,
                "ability_estimate": initial_difficulty,
                "ability_precision": 1.0,
                "question_count": 0
            }
        )
        
        self.active_sessions[session_id] = session
        return session_id
    
    def submit_response(
        self, 
        session_id: str, 
        user_answer: str,
        time_taken: int,
        hints_used: int = 0,
        confidence_level: int = 3
    ) -> Dict[str, Any]:
        """답안 제출 및 다음 문제 선택"""
        if session_id not in self.active_sessions:
            return {"error": "세션을 찾을 수 없습니다"}
        
        session = self.active_sessions[session_id]
        
        if session.current_question_index >= len(session.questions):
            return {"error": "더 이상 문제가 없습니다"}
        
        current_question_id = session.questions[session.current_question_index]
        question = self.question_bank.questions[current_question_id]
        
        # 정답 확인
        is_correct = self._check_answer(question, user_answer)
        
        # 응답 기록
        response = AssessmentResponse(
            question_id=current_question_id,
            user_answer=user_answer,
            is_correct=is_correct,
            time_taken=time_taken,
            hints_used=hints_used,
            confidence_level=confidence_level,
            timestamp=datetime.now()
        )
        session.responses.append(response)
        
        # 점수 업데이트
        question_score = self._calculate_question_score(question, response)
        session.score += question_score
        session.max_score += 100  # 각 문제 만점
        
        # 문제 통계 업데이트
        self.question_bank.update_question_statistics(
            current_question_id, is_correct, time_taken
        )
        
        # 능력 추정치 업데이트 (CAT)
        self._update_ability_estimate(session, response)
        
        # 다음 문제 결정
        next_question = None
        session_complete = False
        
        if self._should_continue_assessment(session):
            next_question = self._select_next_question(
                session.topic,
                DifficultyLevel(int(session.adaptive_parameters["current_difficulty"])),
                session.questions
            )
            
            if next_question:
                session.questions.append(next_question.id)
            else:
                session_complete = True
        else:
            session_complete = True
        
        if session_complete:
            session.is_completed = True
            session.end_time = datetime.now()
            self.completed_sessions.append(session)
            del self.active_sessions[session_id]
        else:
            session.current_question_index += 1
        
        # 응답 생성
        result = {
            "correct": is_correct,
            "explanation": question.explanation,
            "score": question_score,
            "total_score": session.score,
            "progress": (session.current_question_index + 1) / len(session.questions),
            "session_complete": session_complete
        }
        
        if next_question and not session_complete:
            result["next_question"] = {
                "id": next_question.id,
                "type": next_question.type.value,
                "question_text": next_question.question_text,
                "options": next_question.options,
                "estimated_time": next_question.estimated_time
            }
        
        if session_complete:
            result["final_results"] = self._generate_final_results(session)
        
        return result
    
    def _estimate_user_ability(self, user_id: str, topic: str) -> int:
        """사용자 능력 추정"""
        # 실제 환경에서는 과거 성과 데이터 분석
        # 여기서는 중간 난이도로 시작
        return self.cat_parameters["initial_difficulty"]
    
    def _select_next_question(
        self, 
        topic: str, 
        target_difficulty: DifficultyLevel,
        used_questions: List[str]
    ) -> Optional[Question]:
        """다음 문제 선택 (CAT 알고리즘)"""
        available_questions = self.question_bank.get_questions_by_criteria(
            topic=topic,
            difficulty=target_difficulty,
            limit=50
        )
        
        # 이미 사용된 문제 제외
        available_questions = [
            q for q in available_questions if q.id not in used_questions
        ]
        
        if not available_questions:
            # 다른 난이도에서 문제 찾기
            for diff in DifficultyLevel:
                if diff == target_difficulty:
                    continue
                
                backup_questions = self.question_bank.get_questions_by_criteria(
                    topic=topic,
                    difficulty=diff,
                    limit=10
                )
                
                backup_questions = [
                    q for q in backup_questions if q.id not in used_questions
                ]
                
                if backup_questions:
                    available_questions = backup_questions
                    break
        
        if not available_questions:
            return None
        
        # 정보량이 최대인 문제 선택 (IRT 기반)
        best_question = self._select_most_informative_question(available_questions)
        return best_question
    
    def _select_most_informative_question(self, questions: List[Question]) -> Question:
        """가장 정보량이 많은 문제 선택"""
        # 단순화된 구현: 난이도와 통계를 고려한 선택
        scored_questions = []
        
        for question in questions:
            stats = self.question_bank.question_statistics[question.id]
            
            # 정보량 계산 (단순화된 버전)
            discrimination = 1.0  # 실제로는 IRT 매개변수 사용
            information = discrimination ** 2 * 0.25  # Fisher Information
            
            # 문제 다양성 보너스
            diversity_bonus = 1.0 / (stats["attempts"] + 1)
            
            total_score = information + diversity_bonus
            scored_questions.append((question, total_score))
        
        # 가장 높은 점수의 문제 선택
        scored_questions.sort(key=lambda x: x[1], reverse=True)
        return scored_questions[0][0]
    
    def _check_answer(self, question: Question, user_answer: str) -> bool:
        """답안 확인"""
        if question.type == QuestionType.MULTIPLE_CHOICE:
            return user_answer.strip().lower() == question.correct_answer.strip().lower()
        elif question.type == QuestionType.TRUE_FALSE:
            return user_answer.strip().lower() in ['true', 'false'] and \
                   user_answer.strip().lower() == question.correct_answer.strip().lower()
        elif question.type == QuestionType.CALCULATION:
            # 숫자 답안의 경우 허용 오차 범위 내 정답 인정
            try:
                user_num = float(user_answer.strip())
                correct_num = float(question.correct_answer.strip())
                return abs(user_num - correct_num) < 0.01
            except ValueError:
                return False
        else:
            # 기타 유형은 키워드 기반 채점 (실제로는 더 정교한 NLP 필요)
            user_keywords = set(user_answer.lower().split())
            correct_keywords = set(question.correct_answer.lower().split())
            overlap = len(user_keywords.intersection(correct_keywords))
            return overlap / len(correct_keywords) > 0.7
    
    def _calculate_question_score(self, question: Question, response: AssessmentResponse) -> float:
        """문제별 점수 계산"""
        base_score = 100 if response.is_correct else 0
        
        # 난이도 보너스
        difficulty_multiplier = 1.0 + (question.difficulty.value - 1) * 0.2
        
        # 시간 보너스/페널티
        expected_time = question.estimated_time
        time_ratio = response.time_taken / expected_time
        
        if time_ratio < 0.5:  # 매우 빠른 답변
            time_multiplier = 1.2
        elif time_ratio < 1.0:  # 적절한 시간
            time_multiplier = 1.1
        elif time_ratio < 2.0:  # 조금 느린 답변
            time_multiplier = 1.0
        else:  # 매우 느린 답변
            time_multiplier = 0.9
        
        # 힌트 사용 페널티
        hint_penalty = 1.0 - (response.hints_used * 0.1)
        
        final_score = base_score * difficulty_multiplier * time_multiplier * hint_penalty
        return max(0, min(100, final_score))
    
    def _update_ability_estimate(self, session: AssessmentSession, response: AssessmentResponse):
        """능력 추정치 업데이트 (CAT)"""
        # 단순화된 능력 추정 업데이트
        current_ability = session.adaptive_parameters["ability_estimate"]
        
        if response.is_correct:
            # 정답인 경우 능력 추정치 상향 조정
            adjustment = self.cat_parameters["difficulty_adjustment"]
            new_ability = min(5, current_ability + adjustment)
        else:
            # 오답인 경우 능력 추정치 하향 조정
            adjustment = self.cat_parameters["difficulty_adjustment"]
            new_ability = max(1, current_ability - adjustment)
        
        session.adaptive_parameters["ability_estimate"] = new_ability
        session.adaptive_parameters["current_difficulty"] = int(round(new_ability))
        session.adaptive_parameters["question_count"] += 1
        
        # 정밀도 개선 (더 많은 문제를 풀수록 정밀도 향상)
        precision_improvement = 0.1
        current_precision = session.adaptive_parameters["ability_precision"]
        session.adaptive_parameters["ability_precision"] = max(
            self.cat_parameters["precision_threshold"],
            current_precision - precision_improvement
        )
    
    def _should_continue_assessment(self, session: AssessmentSession) -> bool:
        """평가 계속 여부 결정"""
        question_count = session.adaptive_parameters["question_count"]
        precision = session.adaptive_parameters["ability_precision"]
        
        # 최소 문제 수 미달
        if question_count < self.cat_parameters["min_questions"]:
            return True
        
        # 최대 문제 수 도달
        if question_count >= self.cat_parameters["max_questions"]:
            return False
        
        # 정밀도 기준 달성
        if precision <= self.cat_parameters["precision_threshold"]:
            return False
        
        return True
    
    def _generate_final_results(self, session: AssessmentSession) -> Dict[str, Any]:
        """최종 결과 생성"""
        total_questions = len(session.responses)
        correct_answers = sum(1 for r in session.responses if r.is_correct)
        
        accuracy = correct_answers / total_questions if total_questions > 0 else 0
        avg_time = np.mean([r.time_taken for r in session.responses]) if session.responses else 0
        
        # 능력 수준 판정
        ability_estimate = session.adaptive_parameters["ability_estimate"]
        if ability_estimate >= 4.5:
            ability_level = "전문가"
        elif ability_estimate >= 3.5:
            ability_level = "고급"
        elif ability_estimate >= 2.5:
            ability_level = "중급"
        elif ability_estimate >= 1.5:
            ability_level = "초급"
        else:
            ability_level = "기초"
        
        # 강약점 분석
        topic_performance = self._analyze_topic_performance(session)
        
        # 학습 권장사항
        recommendations = self._generate_recommendations(session)
        
        return {
            "session_id": session.session_id,
            "total_score": session.score,
            "max_possible_score": session.max_score,
            "percentage": (session.score / session.max_score * 100) if session.max_score > 0 else 0,
            "accuracy": accuracy * 100,
            "total_questions": total_questions,
            "correct_answers": correct_answers,
            "average_time": avg_time,
            "ability_level": ability_level,
            "ability_estimate": ability_estimate,
            "topic_performance": topic_performance,
            "recommendations": recommendations,
            "completion_time": (session.end_time - session.start_time).total_seconds() / 60,
            "certification_eligible": self._check_certification_eligibility(session)
        }
    
    def _analyze_topic_performance(self, session: AssessmentSession) -> Dict[str, Any]:
        """주제별 성과 분석"""
        topic_stats = {}
        
        for response in session.responses:
            question = self.question_bank.questions[response.question_id]
            subtopic = question.subtopic
            
            if subtopic not in topic_stats:
                topic_stats[subtopic] = {
                    "total": 0,
                    "correct": 0,
                    "avg_time": 0,
                    "times": []
                }
            
            topic_stats[subtopic]["total"] += 1
            if response.is_correct:
                topic_stats[subtopic]["correct"] += 1
            topic_stats[subtopic]["times"].append(response.time_taken)
        
        # 평균 시간 계산
        for subtopic in topic_stats:
            times = topic_stats[subtopic]["times"]
            topic_stats[subtopic]["avg_time"] = np.mean(times) if times else 0
            topic_stats[subtopic]["accuracy"] = (
                topic_stats[subtopic]["correct"] / topic_stats[subtopic]["total"] * 100
            ) if topic_stats[subtopic]["total"] > 0 else 0
            del topic_stats[subtopic]["times"]  # 불필요한 데이터 제거
        
        return topic_stats
    
    def _generate_recommendations(self, session: AssessmentSession) -> List[str]:
        """학습 권장사항 생성"""
        recommendations = []
        ability = session.adaptive_parameters["ability_estimate"]
        topic_performance = self._analyze_topic_performance(session)
        
        # 능력 수준 기반 권장사항
        if ability < 2.0:
            recommendations.append("기초 개념 학습에 더 많은 시간을 투자하세요")
            recommendations.append("단계별 튜토리얼을 활용하여 기초를 다지세요")
        elif ability < 3.0:
            recommendations.append("중급 수준의 연습문제를 통해 실력을 향상시키세요")
            recommendations.append("개념 간의 연결고리를 이해하는 데 집중하세요")
        elif ability < 4.0:
            recommendations.append("고급 주제에 도전해보세요")
            recommendations.append("실제 데이터를 활용한 프로젝트를 시도해보세요")
        else:
            recommendations.append("전문가 수준의 고급 과제에 도전하세요")
            recommendations.append("다른 학습자들을 멘토링해보세요")
        
        # 주제별 성과 기반 권장사항
        weak_topics = [
            topic for topic, stats in topic_performance.items()
            if stats["accuracy"] < 60
        ]
        
        if weak_topics:
            recommendations.append(f"다음 주제들을 집중적으로 학습하세요: {', '.join(weak_topics)}")
        
        return recommendations
    
    def _check_certification_eligibility(self, session: AssessmentSession) -> bool:
        """인증 자격 확인"""
        if session.assessment_type != AssessmentType.CERTIFICATION:
            return False
        
        # 인증 기준: 80% 이상 정확도 + 평균 이상 능력 추정치
        accuracy = sum(1 for r in session.responses if r.is_correct) / len(session.responses)
        ability = session.adaptive_parameters["ability_estimate"]
        
        return accuracy >= 0.8 and ability >= 3.0

class CertificationManager:
    """인증 관리 시스템"""
    
    def __init__(self):
        self.certificates: Dict[str, Dict] = {}
        self.certificate_templates = self._load_certificate_templates()
    
    def _load_certificate_templates(self) -> Dict[str, Dict]:
        """인증서 템플릿 로드"""
        return {
            "basic_statistics": {
                "name": "기초 통계학 인증",
                "description": "기초 통계 개념과 기술통계학 숙달 인증",
                "requirements": {"min_score": 80, "min_ability": 2.0},
                "validity_days": 365
            },
            "advanced_statistics": {
                "name": "고급 통계학 인증",
                "description": "고급 통계 분석 및 추론통계학 전문성 인증",
                "requirements": {"min_score": 85, "min_ability": 4.0},
                "validity_days": 730
            },
            "data_science": {
                "name": "데이터 사이언스 인증",
                "description": "종합적인 데이터 분석 및 머신러닝 역량 인증",
                "requirements": {"min_score": 90, "min_ability": 4.5},
                "validity_days": 730
            }
        }
    
    def issue_certificate(
        self, 
        user_id: str, 
        session: AssessmentSession,
        certificate_type: str
    ) -> Optional[Dict[str, Any]]:
        """인증서 발급"""
        if not session.is_completed or certificate_type not in self.certificate_templates:
            return None
        
        template = self.certificate_templates[certificate_type]
        requirements = template["requirements"]
        
        # 요구사항 확인
        final_results = session  # 실제로는 final_results를 별도 계산
        score_percentage = (session.score / session.max_score * 100) if session.max_score > 0 else 0
        ability = session.adaptive_parameters["ability_estimate"]
        
        if (score_percentage >= requirements["min_score"] and 
            ability >= requirements["min_ability"]):
            
            # 인증서 생성
            certificate_id = self._generate_certificate_id(user_id, certificate_type)
            issue_date = datetime.now()
            expiry_date = issue_date + timedelta(days=template["validity_days"])
            
            certificate = {
                "id": certificate_id,
                "user_id": user_id,
                "certificate_type": certificate_type,
                "name": template["name"],
                "description": template["description"],
                "issue_date": issue_date.isoformat(),
                "expiry_date": expiry_date.isoformat(),
                "score": score_percentage,
                "ability_level": ability,
                "session_id": session.session_id,
                "verification_hash": self._generate_verification_hash(certificate_id, user_id),
                "is_valid": True
            }
            
            self.certificates[certificate_id] = certificate
            return certificate
        
        return None
    
    def _generate_certificate_id(self, user_id: str, certificate_type: str) -> str:
        """인증서 ID 생성"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"CERT_{certificate_type.upper()}_{user_id}_{timestamp}"
    
    def _generate_verification_hash(self, certificate_id: str, user_id: str) -> str:
        """검증 해시 생성"""
        data = f"{certificate_id}_{user_id}_{datetime.now().isoformat()}"
        hash_object = hashlib.sha256(data.encode())
        return base64.urlsafe_b64encode(hash_object.digest()).decode()[:16]
    
    def verify_certificate(self, certificate_id: str) -> Optional[Dict[str, Any]]:
        """인증서 검증"""
        certificate = self.certificates.get(certificate_id)
        
        if not certificate:
            return None
        
        # 만료일 확인
        expiry_date = datetime.fromisoformat(certificate["expiry_date"])
        is_expired = datetime.now() > expiry_date
        
        return {
            "certificate": certificate,
            "is_valid": certificate["is_valid"] and not is_expired,
            "is_expired": is_expired,
            "verification_time": datetime.now().isoformat()
        }

# 전역 인스턴스
question_bank = QuestionBank()
assessment_engine = AdaptiveAssessmentEngine(question_bank)
certification_manager = CertificationManager()