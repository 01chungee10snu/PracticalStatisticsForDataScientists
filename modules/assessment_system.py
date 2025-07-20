"""
평가 및 피드백 시스템
- 실시간 학습 성과 평가
- 개인화된 피드백 생성
- 학습 목표 달성도 추적
- 적응형 평가 문항 생성
"""

import json
import math
import random
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum

class AssessmentType(Enum):
    DIAGNOSTIC = "diagnostic"      # 진단 평가
    FORMATIVE = "formative"       # 형성 평가
    SUMMATIVE = "summative"       # 총괄 평가
    ADAPTIVE = "adaptive"         # 적응형 평가

class QuestionType(Enum):
    MULTIPLE_CHOICE = "multiple_choice"
    TRUE_FALSE = "true_false"
    SHORT_ANSWER = "short_answer"
    CODE_COMPLETION = "code_completion"
    INTERPRETATION = "interpretation"
    PROBLEM_SOLVING = "problem_solving"

@dataclass
class Question:
    """평가 문항"""
    question_id: str
    type: QuestionType
    content: str
    options: Optional[List[str]]
    correct_answer: str
    explanation: str
    difficulty_level: float  # 0-1
    topic: str
    cognitive_level: str     # remember, understand, apply, analyze, evaluate, create
    estimated_time: int      # 예상 소요 시간 (초)

@dataclass
class Response:
    """학습자 응답"""
    response_id: str
    user_id: str
    question_id: str
    answer: str
    is_correct: bool
    response_time: int       # 응답 시간 (초)
    timestamp: str
    confidence_level: Optional[float]  # 확신도 (0-1)

@dataclass
class AssessmentResult:
    """평가 결과"""
    assessment_id: str
    user_id: str
    assessment_type: AssessmentType
    total_questions: int
    correct_answers: int
    score: float             # 0-100
    completion_time: int     # 완료 시간 (초)
    topic_scores: Dict[str, float]  # 주제별 점수
    cognitive_scores: Dict[str, float]  # 인지 수준별 점수
    strengths: List[str]
    weaknesses: List[str]
    recommendations: List[str]
    timestamp: str

class AssessmentSystem:
    def __init__(self):
        self.questions: Dict[str, Question] = {}
        self.responses: List[Response] = []
        self.assessment_results: Dict[str, AssessmentResult] = {}
        self.user_profiles: Dict[str, Dict] = {}
        self.question_bank = self._initialize_question_bank()
        
    def _initialize_question_bank(self) -> Dict[str, List[Question]]:
        """문항 은행 초기화"""
        return {
            'descriptive_statistics': self._create_descriptive_stats_questions(),
            'probability': self._create_probability_questions(),
            'hypothesis_testing': self._create_hypothesis_testing_questions(),
            'regression': self._create_regression_questions(),
            'python_basics': self._create_python_questions()
        }
    
    def _create_descriptive_stats_questions(self) -> List[Question]:
        """기술통계 문항 생성"""
        questions = []
        
        # 기본 개념 문항
        questions.append(Question(
            question_id="desc_stats_001",
            type=QuestionType.MULTIPLE_CHOICE,
            content="다음 중 중심경향성을 나타내는 통계량이 아닌 것은?",
            options=["평균", "중앙값", "최빈값", "표준편차"],
            correct_answer="표준편차",
            explanation="표준편차는 산포도를 나타내는 통계량입니다. 중심경향성은 평균, 중앙값, 최빈값으로 측정됩니다.",
            difficulty_level=0.3,
            topic="descriptive_statistics",
            cognitive_level="remember",
            estimated_time=30
        ))
        
        # 적용 문항
        questions.append(Question(
            question_id="desc_stats_002",
            type=QuestionType.CODE_COMPLETION,
            content="다음 데이터의 평균을 계산하는 Python 코드를 완성하세요.\ndata = [1, 2, 3, 4, 5]\nmean = ____",
            options=None,
            correct_answer="sum(data) / len(data)",
            explanation="평균은 모든 값의 합을 개수로 나눈 값입니다. Python에서는 sum()과 len() 함수를 사용할 수 있습니다.",
            difficulty_level=0.4,
            topic="descriptive_statistics",
            cognitive_level="apply",
            estimated_time=60
        ))
        
        # 해석 문항
        questions.append(Question(
            question_id="desc_stats_003",
            type=QuestionType.INTERPRETATION,
            content="어떤 데이터의 평균이 50, 중앙값이 45일 때, 이 분포의 특성을 설명하세요.",
            options=None,
            correct_answer="우측으로 치우친 분포 (positive skew)",
            explanation="평균이 중앙값보다 클 때는 우측으로 치우친 분포입니다. 극값이 평균을 끌어올리기 때문입니다.",
            difficulty_level=0.6,
            topic="descriptive_statistics",
            cognitive_level="analyze",
            estimated_time=90
        ))
        
        return questions
    
    def _create_probability_questions(self) -> List[Question]:
        """확률 문항 생성"""
        questions = []
        
        questions.append(Question(
            question_id="prob_001",
            type=QuestionType.MULTIPLE_CHOICE,
            content="동전을 두 번 던질 때, 적어도 한 번은 앞면이 나올 확률은?",
            options=["1/4", "1/2", "3/4", "1"],
            correct_answer="3/4",
            explanation="전체 경우의 수는 4가지(HH, HT, TH, TT)이고, 적어도 한 번 앞면이 나오는 경우는 3가지입니다.",
            difficulty_level=0.5,
            topic="probability",
            cognitive_level="apply",
            estimated_time=45
        ))
        
        return questions
    
    def _create_hypothesis_testing_questions(self) -> List[Question]:
        """가설검정 문항 생성"""
        questions = []
        
        questions.append(Question(
            question_id="hyp_test_001",
            type=QuestionType.TRUE_FALSE,
            content="p-값이 0.05보다 작으면 항상 귀무가설을 기각해야 한다.",
            options=["참", "거짓"],
            correct_answer="거짓",
            explanation="p-값이 유의수준보다 작을 때 귀무가설을 기각하지만, 유의수준은 연구자가 미리 설정해야 하며 항상 0.05일 필요는 없습니다.",
            difficulty_level=0.7,
            topic="hypothesis_testing",
            cognitive_level="evaluate",
            estimated_time=60
        ))
        
        return questions
    
    def _create_regression_questions(self) -> List[Question]:
        """회귀분석 문항 생성"""
        questions = []
        
        questions.append(Question(
            question_id="reg_001",
            type=QuestionType.PROBLEM_SOLVING,
            content="회귀식 y = 2x + 3에서 x가 1 증가할 때 y의 변화량은?",
            options=None,
            correct_answer="2",
            explanation="회귀계수(기울기)는 독립변수가 1단위 증가할 때 종속변수의 변화량을 나타냅니다.",
            difficulty_level=0.4,
            topic="regression",
            cognitive_level="understand",
            estimated_time=30
        ))
        
        return questions
    
    def _create_python_questions(self) -> List[Question]:
        """Python 문항 생성"""
        questions = []
        
        questions.append(Question(
            question_id="python_001",
            type=QuestionType.CODE_COMPLETION,
            content="pandas DataFrame에서 'age' 컬럼의 평균을 구하는 코드를 완성하세요.\ndf.____.mean()",
            options=None,
            correct_answer="['age']",
            explanation="DataFrame에서 특정 컬럼을 선택할 때는 대괄호를 사용합니다. df['age'].mean()이 정답입니다.",
            difficulty_level=0.3,
            topic="python_basics",
            cognitive_level="apply",
            estimated_time=45
        ))
        
        return questions
    
    def create_adaptive_assessment(self, user_id: str, topic: str, target_questions: int = 10) -> List[Question]:
        """적응형 평가 생성"""
        if user_id not in self.user_profiles:
            # 새 사용자는 중간 난이도부터 시작
            estimated_ability = 0.5
        else:
            # 기존 사용자는 이전 성과를 바탕으로 능력 추정
            estimated_ability = self._estimate_user_ability(user_id, topic)
        
        selected_questions = []
        current_ability = estimated_ability
        
        # 첫 번째 문항은 추정 능력 수준에 맞춰 선택
        first_question = self._select_question_by_difficulty(topic, current_ability)
        if first_question:
            selected_questions.append(first_question)
        
        # 나머지 문항들을 적응적으로 선택
        for i in range(1, target_questions):
            if len(selected_questions) == 0:
                break
                
            # 이전 응답을 바탕으로 능력 재추정
            last_question = selected_questions[-1]
            # 실제 구현에서는 사용자의 실제 응답을 사용해야 함
            # 여기서는 시뮬레이션을 위해 임의의 응답 생성
            simulated_correct = random.random() < current_ability
            
            current_ability = self._update_ability_estimate(
                current_ability, last_question.difficulty_level, simulated_correct
            )
            
            # 업데이트된 능력에 맞는 다음 문항 선택
            next_question = self._select_question_by_difficulty(topic, current_ability)
            if next_question and next_question.question_id not in [q.question_id for q in selected_questions]:
                selected_questions.append(next_question)
        
        return selected_questions
    
    def _estimate_user_ability(self, user_id: str, topic: str) -> float:
        """사용자 능력 추정"""
        user_responses = [r for r in self.responses if r.user_id == user_id]
        
        if not user_responses:
            return 0.5  # 기본값
        
        # 해당 주제의 최근 응답들을 분석
        topic_responses = []
        for response in user_responses:
            if response.question_id in self.questions:
                question = self.questions[response.question_id]
                if question.topic == topic:
                    topic_responses.append(response)
        
        if not topic_responses:
            return 0.5
        
        # 최근 10개 응답의 가중평균으로 능력 추정
        recent_responses = topic_responses[-10:]
        total_weight = 0
        weighted_score = 0
        
        for i, response in enumerate(recent_responses):
            weight = i + 1  # 최근 응답일수록 높은 가중치
            question = self.questions[response.question_id]
            
            if response.is_correct:
                score = question.difficulty_level + 0.1  # 정답이면 난이도보다 약간 높게
            else:
                score = question.difficulty_level - 0.1  # 오답이면 난이도보다 약간 낮게
            
            weighted_score += score * weight
            total_weight += weight
        
        estimated_ability = weighted_score / total_weight
        return max(0.1, min(0.9, estimated_ability))
    
    def _select_question_by_difficulty(self, topic: str, target_difficulty: float) -> Optional[Question]:
        """난이도에 맞는 문항 선택"""
        if topic not in self.question_bank:
            return None
        
        available_questions = self.question_bank[topic]
        
        # 목표 난이도와 가장 가까운 문항 찾기
        best_question = None
        min_diff = float('inf')
        
        for question in available_questions:
            diff = abs(question.difficulty_level - target_difficulty)
            if diff < min_diff:
                min_diff = diff
                best_question = question
        
        return best_question
    
    def _update_ability_estimate(self, current_ability: float, question_difficulty: float, is_correct: bool) -> float:
        """능력 추정치 업데이트 (간단한 베이지안 업데이트)"""
        learning_rate = 0.1
        
        if is_correct:
            # 정답이면 능력 추정치를 문항 난이도 방향으로 조정
            if question_difficulty > current_ability:
                new_ability = current_ability + learning_rate * (question_difficulty - current_ability)
            else:
                new_ability = current_ability + learning_rate * 0.05  # 약간 증가
        else:
            # 오답이면 능력 추정치를 낮춤
            if question_difficulty < current_ability:
                new_ability = current_ability - learning_rate * (current_ability - question_difficulty)
            else:
                new_ability = current_ability - learning_rate * 0.05  # 약간 감소
        
        return max(0.1, min(0.9, new_ability))
    
    def evaluate_response(self, user_id: str, question_id: str, user_answer: str, response_time: int) -> Dict[str, Any]:
        """응답 평가"""
        if question_id not in self.questions:
            raise ValueError(f"Question {question_id} not found")
        
        question = self.questions[question_id]
        
        # 정답 여부 판단
        is_correct = self._check_answer_correctness(question, user_answer)
        
        # 응답 기록 생성
        response = Response(
            response_id=f"resp_{user_id}_{question_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            user_id=user_id,
            question_id=question_id,
            answer=user_answer,
            is_correct=is_correct,
            response_time=response_time,
            timestamp=datetime.now().isoformat(),
            confidence_level=None  # 추후 구현
        )
        
        self.responses.append(response)
        
        # 피드백 생성
        feedback = self._generate_feedback(question, user_answer, is_correct, response_time)
        
        return {
            'is_correct': is_correct,
            'feedback': feedback,
            'explanation': question.explanation,
            'response_id': response.response_id
        }
    
    def _check_answer_correctness(self, question: Question, user_answer: str) -> bool:
        """정답 여부 확인"""
        correct_answer = question.correct_answer.strip().lower()
        user_answer = user_answer.strip().lower()
        
        if question.type == QuestionType.MULTIPLE_CHOICE:
            return user_answer == correct_answer
        elif question.type == QuestionType.TRUE_FALSE:
            return user_answer in ['참', '거짓', 'true', 'false'] and user_answer == correct_answer
        elif question.type == QuestionType.CODE_COMPLETION:
            # 코드 답안은 더 유연한 검사 필요
            return self._check_code_answer(correct_answer, user_answer)
        elif question.type == QuestionType.SHORT_ANSWER:
            # 키워드 기반 검사
            return self._check_short_answer(correct_answer, user_answer)
        else:
            return user_answer == correct_answer
    
    def _check_code_answer(self, correct: str, user_answer: str) -> bool:
        """코드 답안 검사"""
        # 공백과 대소문자 무시하고 비교
        correct_normalized = ''.join(correct.split()).lower()
        user_normalized = ''.join(user_answer.split()).lower()
        
        return correct_normalized == user_normalized
    
    def _check_short_answer(self, correct: str, user_answer: str) -> bool:
        """단답형 답안 검사"""
        correct_keywords = set(correct.split())
        user_keywords = set(user_answer.split())
        
        # 키워드의 80% 이상 일치하면 정답으로 인정
        intersection = correct_keywords.intersection(user_keywords)
        return len(intersection) / len(correct_keywords) >= 0.8
    
    def _generate_feedback(self, question: Question, user_answer: str, is_correct: bool, response_time: int) -> Dict[str, Any]:
        """개인화된 피드백 생성"""
        feedback = {
            'correctness': 'correct' if is_correct else 'incorrect',
            'message': '',
            'hints': [],
            'next_steps': [],
            'time_feedback': ''
        }
        
        # 정답/오답에 따른 메시지
        if is_correct:
            feedback['message'] = "정답입니다! 잘하셨습니다."
            
            # 응답 시간에 따른 추가 피드백
            if response_time < question.estimated_time * 0.7:
                feedback['time_feedback'] = "빠르고 정확한 답변이었습니다."
            elif response_time > question.estimated_time * 1.5:
                feedback['time_feedback'] = "정답이지만 시간이 좀 걸렸네요. 연습을 통해 속도를 높여보세요."
        else:
            feedback['message'] = "아쉽게도 틀렸습니다. 다시 한번 생각해보세요."
            
            # 문항 유형별 힌트 제공
            feedback['hints'] = self._generate_hints(question, user_answer)
        
        # 다음 단계 제안
        feedback['next_steps'] = self._suggest_next_steps(question, is_correct)
        
        return feedback
    
    def _generate_hints(self, question: Question, user_answer: str) -> List[str]:
        """힌트 생성"""
        hints = []
        
        if question.type == QuestionType.MULTIPLE_CHOICE:
            hints.append("각 선택지를 다시 한번 검토해보세요.")
            hints.append(f"이 문제는 '{question.topic}' 주제와 관련이 있습니다.")
        
        elif question.type == QuestionType.CODE_COMPLETION:
            hints.append("Python 문법을 다시 확인해보세요.")
            hints.append("함수 이름과 괄호를 정확히 사용했는지 확인하세요.")
        
        elif question.type == QuestionType.INTERPRETATION:
            hints.append("데이터의 특성을 단계별로 분석해보세요.")
            hints.append("수치들 간의 관계를 생각해보세요.")
        
        return hints
    
    def _suggest_next_steps(self, question: Question, is_correct: bool) -> List[str]:
        """다음 단계 제안"""
        next_steps = []
        
        if is_correct:
            if question.difficulty_level < 0.7:
                next_steps.append("더 어려운 문제에 도전해보세요.")
            next_steps.append(f"{question.topic} 관련 심화 학습을 진행해보세요.")
        else:
            next_steps.append(f"{question.topic} 기본 개념을 다시 복습해보세요.")
            if question.difficulty_level > 0.5:
                next_steps.append("더 쉬운 문제부터 차근차근 풀어보세요.")
            next_steps.append("관련 예제를 더 많이 연습해보세요.")
        
        return next_steps
    
    def generate_assessment_report(self, user_id: str, assessment_id: str) -> AssessmentResult:
        """평가 보고서 생성"""
        # 해당 평가의 응답들 수집
        assessment_responses = [r for r in self.responses 
                              if r.user_id == user_id and assessment_id in r.response_id]
        
        if not assessment_responses:
            raise ValueError(f"No responses found for assessment {assessment_id}")
        
        # 기본 통계 계산
        total_questions = len(assessment_responses)
        correct_answers = sum(1 for r in assessment_responses if r.is_correct)
        score = (correct_answers / total_questions) * 100
        
        # 주제별 점수 계산
        topic_scores = self._calculate_topic_scores(assessment_responses)
        
        # 인지 수준별 점수 계산
        cognitive_scores = self._calculate_cognitive_scores(assessment_responses)
        
        # 강점과 약점 분석
        strengths, weaknesses = self._analyze_strengths_weaknesses(topic_scores, cognitive_scores)
        
        # 개선 권장사항 생성
        recommendations = self._generate_recommendations(weaknesses, user_id)
        
        # 완료 시간 계산
        completion_time = sum(r.response_time for r in assessment_responses)
        
        result = AssessmentResult(
            assessment_id=assessment_id,
            user_id=user_id,
            assessment_type=AssessmentType.FORMATIVE,  # 기본값
            total_questions=total_questions,
            correct_answers=correct_answers,
            score=score,
            completion_time=completion_time,
            topic_scores=topic_scores,
            cognitive_scores=cognitive_scores,
            strengths=strengths,
            weaknesses=weaknesses,
            recommendations=recommendations,
            timestamp=datetime.now().isoformat()
        )
        
        self.assessment_results[assessment_id] = result
        return result
    
    def _calculate_topic_scores(self, responses: List[Response]) -> Dict[str, float]:
        """주제별 점수 계산"""
        topic_scores = {}
        topic_counts = {}
        
        for response in responses:
            if response.question_id in self.questions:
                question = self.questions[response.question_id]
                topic = question.topic
                
                if topic not in topic_scores:
                    topic_scores[topic] = 0
                    topic_counts[topic] = 0
                
                if response.is_correct:
                    topic_scores[topic] += 1
                topic_counts[topic] += 1
        
        # 백분율로 변환
        for topic in topic_scores:
            if topic_counts[topic] > 0:
                topic_scores[topic] = (topic_scores[topic] / topic_counts[topic]) * 100
        
        return topic_scores
    
    def _calculate_cognitive_scores(self, responses: List[Response]) -> Dict[str, float]:
        """인지 수준별 점수 계산"""
        cognitive_scores = {}
        cognitive_counts = {}
        
        for response in responses:
            if response.question_id in self.questions:
                question = self.questions[response.question_id]
                cognitive_level = question.cognitive_level
                
                if cognitive_level not in cognitive_scores:
                    cognitive_scores[cognitive_level] = 0
                    cognitive_counts[cognitive_level] = 0
                
                if response.is_correct:
                    cognitive_scores[cognitive_level] += 1
                cognitive_counts[cognitive_level] += 1
        
        # 백분율로 변환
        for level in cognitive_scores:
            if cognitive_counts[level] > 0:
                cognitive_scores[level] = (cognitive_scores[level] / cognitive_counts[level]) * 100
        
        return cognitive_scores
    
    def _analyze_strengths_weaknesses(self, topic_scores: Dict[str, float], 
                                    cognitive_scores: Dict[str, float]) -> Tuple[List[str], List[str]]:
        """강점과 약점 분석"""
        strengths = []
        weaknesses = []
        
        # 주제별 분석
        for topic, score in topic_scores.items():
            if score >= 80:
                strengths.append(f"{topic} 영역에서 우수한 성과")
            elif score < 60:
                weaknesses.append(f"{topic} 영역 보완 필요")
        
        # 인지 수준별 분석
        for level, score in cognitive_scores.items():
            if score >= 80:
                strengths.append(f"{level} 수준의 사고 능력 우수")
            elif score < 60:
                weaknesses.append(f"{level} 수준의 사고 능력 향상 필요")
        
        return strengths, weaknesses
    
    def _generate_recommendations(self, weaknesses: List[str], user_id: str) -> List[str]:
        """개선 권장사항 생성"""
        recommendations = []
        
        for weakness in weaknesses:
            if "descriptive_statistics" in weakness:
                recommendations.append("기술통계량 개념을 다시 학습하고 실습 문제를 더 풀어보세요.")
            elif "probability" in weakness:
                recommendations.append("확률 기초 개념을 복습하고 다양한 예제를 연습하세요.")
            elif "hypothesis_testing" in weakness:
                recommendations.append("가설검정의 단계별 과정을 체계적으로 학습하세요.")
            elif "remember" in weakness:
                recommendations.append("기본 개념과 용어를 암기하는 학습에 집중하세요.")
            elif "apply" in weakness:
                recommendations.append("이론을 실제 문제에 적용하는 연습을 늘리세요.")
            elif "analyze" in weakness:
                recommendations.append("데이터를 분석하고 해석하는 능력을 기르세요.")
        
        # 일반적인 권장사항
        if len(weaknesses) > 3:
            recommendations.append("기초부터 차근차근 다시 학습하는 것을 권장합니다.")
        
        return recommendations

# 사용 예제
if __name__ == "__main__":
    assessment_system = AssessmentSystem()
    
    # 문항을 문항 은행에 등록
    for topic, questions in assessment_system.question_bank.items():
        for question in questions:
            assessment_system.questions[question.question_id] = question
    
    # 적응형 평가 생성
    adaptive_questions = assessment_system.create_adaptive_assessment('user123', 'descriptive_statistics', 5)
    print(f"생성된 적응형 평가 문항 수: {len(adaptive_questions)}")
    
    # 응답 평가 시뮬레이션
    for question in adaptive_questions[:2]:
        result = assessment_system.evaluate_response(
            'user123', 
            question.question_id, 
            question.correct_answer,  # 정답으로 시뮬레이션
            30
        )
        print(f"문항 {question.question_id}: {result['feedback']['message']}")
    
    # 평가 보고서 생성
    try:
        report = assessment_system.generate_assessment_report('user123', 'test_assessment')
        print(f"평가 점수: {report.score:.1f}점")
        print(f"강점: {report.strengths}")
        print(f"약점: {report.weaknesses}")
    except ValueError as e:
        print(f"보고서 생성 실패: {e}")