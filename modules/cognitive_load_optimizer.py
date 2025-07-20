"""
인지 부하 최적화 에이전트
- 학습자의 인지 부하 실시간 모니터링
- 정보 제시 방식 최적화
- 학습 세션 길이 및 휴식 시간 조절
- 멀티태스킹 방지 및 집중도 향상
"""

import json
import math
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum

class CognitiveLoadType(Enum):
    INTRINSIC = "intrinsic"      # 내재적 부하 (학습 내용 자체의 복잡성)
    EXTRANEOUS = "extraneous"    # 외재적 부하 (불필요한 정보나 방해 요소)
    GERMANE = "germane"          # 생성적 부하 (스키마 구성을 위한 부하)

@dataclass
class CognitiveState:
    """학습자의 인지 상태"""
    user_id: str
    timestamp: str
    attention_level: float      # 0-1, 집중도
    working_memory_load: float  # 0-1, 작업 기억 부하
    processing_speed: float     # 0-1, 정보 처리 속도
    fatigue_level: float       # 0-1, 피로도
    stress_level: float        # 0-1, 스트레스 수준
    flow_state: float          # 0-1, 몰입 상태

@dataclass
class ContentComplexity:
    """콘텐츠 복잡도 분석"""
    content_id: str
    intrinsic_complexity: float    # 내재적 복잡도
    extraneous_elements: int       # 외재적 요소 개수
    information_density: float     # 정보 밀도
    cognitive_demand: float        # 인지적 요구도
    recommended_chunk_size: int    # 권장 청크 크기

class CognitiveLoadOptimizer:
    def __init__(self):
        self.cognitive_states: Dict[str, List[CognitiveState]] = {}
        self.content_complexities: Dict[str, ContentComplexity] = {}
        self.optimization_rules = self._initialize_optimization_rules()
        self.session_data: Dict[str, Dict] = {}
        
    def _initialize_optimization_rules(self) -> Dict[str, Any]:
        """최적화 규칙 초기화"""
        return {
            'max_session_duration': 45,  # 최대 세션 시간 (분)
            'optimal_chunk_size': 7,     # 최적 정보 청크 크기 (Miller's 7±2)
            'break_interval': 25,        # 휴식 간격 (분, Pomodoro 기법)
            'attention_threshold': 0.6,   # 집중도 임계값
            'fatigue_threshold': 0.7,     # 피로도 임계값
            'complexity_adjustment': {
                'low': 0.8,    # 낮은 복잡도 콘텐츠 비율
                'medium': 1.0, # 중간 복잡도 콘텐츠 비율
                'high': 1.2    # 높은 복잡도 콘텐츠 비율
            }
        }
    
    def analyze_content_complexity(self, content: str, content_id: str) -> ContentComplexity:
        """콘텐츠 복잡도 분석"""
        # 1. 내재적 복잡도 계산
        intrinsic_complexity = self._calculate_intrinsic_complexity(content)
        
        # 2. 외재적 요소 분석
        extraneous_elements = self._count_extraneous_elements(content)
        
        # 3. 정보 밀도 계산
        information_density = self._calculate_information_density(content)
        
        # 4. 인지적 요구도 계산
        cognitive_demand = self._calculate_cognitive_demand(
            intrinsic_complexity, extraneous_elements, information_density
        )
        
        # 5. 권장 청크 크기 계산
        recommended_chunk_size = self._calculate_optimal_chunk_size(cognitive_demand)
        
        complexity = ContentComplexity(
            content_id=content_id,
            intrinsic_complexity=intrinsic_complexity,
            extraneous_elements=extraneous_elements,
            information_density=information_density,
            cognitive_demand=cognitive_demand,
            recommended_chunk_size=recommended_chunk_size
        )
        
        self.content_complexities[content_id] = complexity
        return complexity
    
    def _calculate_intrinsic_complexity(self, content: str) -> float:
        """내재적 복잡도 계산"""
        # 텍스트 기반 복잡도 지표들
        words = content.split()
        sentences = content.split('.')
        
        # 1. 어휘 복잡도 (긴 단어 비율)
        long_words = [w for w in words if len(w) > 6]
        vocab_complexity = len(long_words) / max(len(words), 1)
        
        # 2. 구문 복잡도 (평균 문장 길이)
        avg_sentence_length = len(words) / max(len(sentences), 1)
        syntax_complexity = min(1.0, avg_sentence_length / 20)  # 20단어를 기준으로 정규화
        
        # 3. 개념 복잡도 (전문 용어 밀도)
        technical_terms = self._count_technical_terms(content)
        concept_complexity = technical_terms / max(len(words), 1) * 10
        
        # 4. 논리적 복잡도 (연결어 사용)
        logical_connectors = self._count_logical_connectors(content)
        logic_complexity = logical_connectors / max(len(sentences), 1)
        
        # 가중 평균으로 최종 복잡도 계산
        intrinsic_complexity = (
            vocab_complexity * 0.25 +
            syntax_complexity * 0.25 +
            concept_complexity * 0.3 +
            logic_complexity * 0.2
        )
        
        return min(1.0, intrinsic_complexity)
    
    def _count_technical_terms(self, content: str) -> int:
        """전문 용어 개수 계산"""
        technical_terms = [
            '통계', '확률', '분포', '가설', '검정', '회귀', '상관',
            '표준편차', '분산', '평균', '중앙값', '최빈값',
            'python', 'pandas', 'numpy', 'matplotlib', 'seaborn',
            '데이터', '분석', '시각화', '모델', '알고리즘'
        ]
        
        content_lower = content.lower()
        count = 0
        for term in technical_terms:
            count += content_lower.count(term)
        
        return count
    
    def _count_logical_connectors(self, content: str) -> int:
        """논리적 연결어 개수 계산"""
        connectors = [
            '그러나', '하지만', '따라서', '그러므로', '또한', '그리고',
            '반면', '한편', '즉', '예를 들어', '특히', '결과적으로'
        ]
        
        count = 0
        for connector in connectors:
            count += content.count(connector)
        
        return count
    
    def _count_extraneous_elements(self, content: str) -> int:
        """외재적 요소 개수 계산"""
        extraneous_count = 0
        
        # 1. 불필요한 장식적 요소
        decorative_elements = ['★', '♦', '◆', '●', '■', '▲']
        for element in decorative_elements:
            extraneous_count += content.count(element)
        
        # 2. 중복된 정보
        sentences = content.split('.')
        unique_sentences = set(sentences)
        extraneous_count += len(sentences) - len(unique_sentences)
        
        # 3. 과도한 강조 표시
        emphasis_marks = content.count('**') + content.count('__') + content.count('*')
        if emphasis_marks > len(content.split()) * 0.1:  # 10% 이상이면 과도함
            extraneous_count += emphasis_marks
        
        return extraneous_count
    
    def _calculate_information_density(self, content: str) -> float:
        """정보 밀도 계산"""
        words = content.split()
        
        # 1. 정보 단위 계산 (명사, 동사, 형용사 등)
        info_words = self._count_information_words(content)
        
        # 2. 밀도 계산 (정보 단위 / 전체 단어)
        density = info_words / max(len(words), 1)
        
        return min(1.0, density)
    
    def _count_information_words(self, content: str) -> int:
        """정보를 담고 있는 단어 개수 계산 (간단한 휴리스틱)"""
        words = content.split()
        
        # 기능어 (조사, 접속사 등) 제외
        function_words = [
            '은', '는', '이', '가', '을', '를', '에', '에서', '로', '으로',
            '와', '과', '의', '도', '만', '부터', '까지', '처럼', '같이',
            '그리고', '또는', '하지만', '그러나', '그래서'
        ]
        
        info_words = [w for w in words if w not in function_words and len(w) > 1]
        return len(info_words)
    
    def _calculate_cognitive_demand(self, intrinsic: float, extraneous: int, density: float) -> float:
        """인지적 요구도 계산"""
        # 내재적 복잡도가 기본, 외재적 요소와 정보 밀도가 추가 부하
        base_demand = intrinsic
        extraneous_penalty = min(0.3, extraneous * 0.05)  # 외재적 요소 페널티
        density_factor = density * 0.2  # 정보 밀도 가중치
        
        total_demand = base_demand + extraneous_penalty + density_factor
        return min(1.0, total_demand)
    
    def _calculate_optimal_chunk_size(self, cognitive_demand: float) -> int:
        """최적 청크 크기 계산"""
        base_chunk_size = self.optimization_rules['optimal_chunk_size']
        
        # 인지적 요구도에 따른 청크 크기 조정
        if cognitive_demand < 0.3:
            return int(base_chunk_size * 1.5)  # 쉬운 내용은 더 큰 청크
        elif cognitive_demand > 0.7:
            return int(base_chunk_size * 0.7)  # 어려운 내용은 더 작은 청크
        else:
            return base_chunk_size
    
    def monitor_cognitive_state(self, user_id: str, interaction_data: Dict[str, Any]) -> CognitiveState:
        """인지 상태 모니터링"""
        # 상호작용 데이터를 바탕으로 인지 상태 추정
        attention_level = self._estimate_attention_level(interaction_data)
        working_memory_load = self._estimate_working_memory_load(interaction_data)
        processing_speed = self._estimate_processing_speed(interaction_data)
        fatigue_level = self._estimate_fatigue_level(user_id, interaction_data)
        stress_level = self._estimate_stress_level(interaction_data)
        flow_state = self._estimate_flow_state(interaction_data)
        
        cognitive_state = CognitiveState(
            user_id=user_id,
            timestamp=datetime.now().isoformat(),
            attention_level=attention_level,
            working_memory_load=working_memory_load,
            processing_speed=processing_speed,
            fatigue_level=fatigue_level,
            stress_level=stress_level,
            flow_state=flow_state
        )
        
        # 상태 기록 저장
        if user_id not in self.cognitive_states:
            self.cognitive_states[user_id] = []
        self.cognitive_states[user_id].append(cognitive_state)
        
        return cognitive_state
    
    def _estimate_attention_level(self, interaction_data: Dict[str, Any]) -> float:
        """집중도 추정"""
        # 마우스 움직임, 클릭 패턴, 스크롤 속도 등을 바탕으로 추정
        mouse_activity = interaction_data.get('mouse_movements', 0)
        click_frequency = interaction_data.get('clicks_per_minute', 0)
        scroll_pattern = interaction_data.get('scroll_consistency', 1.0)
        
        # 적절한 활동량이 높은 집중도를 의미
        if 10 <= mouse_activity <= 50 and 2 <= click_frequency <= 10:
            base_attention = 0.8
        else:
            base_attention = 0.5
        
        # 스크롤 패턴이 일정하면 집중도 높음
        attention_level = base_attention * scroll_pattern
        
        return min(1.0, max(0.0, attention_level))
    
    def _estimate_working_memory_load(self, interaction_data: Dict[str, Any]) -> float:
        """작업 기억 부하 추정"""
        # 동시에 열린 탭 수, 전환 빈도 등
        open_tabs = interaction_data.get('open_tabs', 1)
        tab_switches = interaction_data.get('tab_switches_per_minute', 0)
        
        # 탭이 많고 전환이 빈번하면 작업 기억 부하 증가
        tab_load = min(1.0, open_tabs / 10)  # 10개 탭을 최대로 정규화
        switch_load = min(1.0, tab_switches / 5)  # 분당 5회 전환을 최대로 정규화
        
        working_memory_load = (tab_load + switch_load) / 2
        
        return working_memory_load
    
    def _estimate_processing_speed(self, interaction_data: Dict[str, Any]) -> float:
        """정보 처리 속도 추정"""
        # 읽기 속도, 응답 시간 등
        reading_speed = interaction_data.get('words_per_minute', 200)  # 기본 200wpm
        response_time = interaction_data.get('avg_response_time', 3.0)  # 기본 3초
        
        # 정규화 (200wpm을 기준으로)
        speed_factor = reading_speed / 200
        
        # 응답 시간이 빠를수록 처리 속도 높음
        response_factor = max(0.1, 5.0 / response_time)  # 5초를 기준으로 역수
        
        processing_speed = (speed_factor + response_factor) / 2
        
        return min(1.0, max(0.1, processing_speed))
    
    def _estimate_fatigue_level(self, user_id: str, interaction_data: Dict[str, Any]) -> float:
        """피로도 추정"""
        # 세션 지속 시간, 활동 패턴 변화 등
        session_duration = interaction_data.get('session_duration_minutes', 0)
        activity_decline = interaction_data.get('activity_decline_rate', 0)
        
        # 시간이 길수록 피로도 증가
        time_fatigue = min(1.0, session_duration / 60)  # 60분을 최대로 정규화
        
        # 활동량 감소율이 높을수록 피로도 증가
        activity_fatigue = activity_decline
        
        fatigue_level = (time_fatigue + activity_fatigue) / 2
        
        return fatigue_level
    
    def _estimate_stress_level(self, interaction_data: Dict[str, Any]) -> float:
        """스트레스 수준 추정"""
        # 오류 빈도, 재시도 횟수, 불규칙한 패턴 등
        error_rate = interaction_data.get('error_rate', 0)
        retry_count = interaction_data.get('retry_count', 0)
        pattern_irregularity = interaction_data.get('pattern_irregularity', 0)
        
        stress_indicators = [error_rate, retry_count / 10, pattern_irregularity]
        stress_level = sum(stress_indicators) / len(stress_indicators)
        
        return min(1.0, stress_level)
    
    def _estimate_flow_state(self, interaction_data: Dict[str, Any]) -> float:
        """몰입 상태 추정"""
        # 일정한 활동 패턴, 중단 없는 진행, 적절한 도전 수준
        activity_consistency = interaction_data.get('activity_consistency', 0.5)
        interruption_count = interaction_data.get('interruptions', 0)
        challenge_balance = interaction_data.get('challenge_skill_balance', 0.5)
        
        # 중단이 적고, 활동이 일정하며, 도전과 스킬의 균형이 맞을 때 몰입도 높음
        flow_factors = [
            activity_consistency,
            max(0, 1 - interruption_count / 10),  # 중단 횟수 역수
            challenge_balance
        ]
        
        flow_state = sum(flow_factors) / len(flow_factors)
        
        return flow_state
    
    def optimize_content_presentation(self, user_id: str, content_id: str) -> Dict[str, Any]:
        """콘텐츠 제시 방식 최적화"""
        # 현재 인지 상태 가져오기
        if user_id not in self.cognitive_states or not self.cognitive_states[user_id]:
            # 기본 상태로 가정
            current_state = CognitiveState(
                user_id=user_id,
                timestamp=datetime.now().isoformat(),
                attention_level=0.7,
                working_memory_load=0.5,
                processing_speed=0.7,
                fatigue_level=0.3,
                stress_level=0.3,
                flow_state=0.6
            )
        else:
            current_state = self.cognitive_states[user_id][-1]
        
        # 콘텐츠 복잡도 가져오기
        if content_id not in self.content_complexities:
            raise ValueError(f"Content {content_id} complexity not analyzed")
        
        content_complexity = self.content_complexities[content_id]
        
        # 최적화 전략 결정
        optimization_strategy = self._determine_optimization_strategy(current_state, content_complexity)
        
        return optimization_strategy
    
    def _determine_optimization_strategy(self, state: CognitiveState, complexity: ContentComplexity) -> Dict[str, Any]:
        """최적화 전략 결정"""
        strategy = {
            'content_modifications': [],
            'presentation_adjustments': [],
            'interaction_recommendations': [],
            'break_suggestions': []
        }
        
        # 1. 피로도가 높은 경우
        if state.fatigue_level > self.optimization_rules['fatigue_threshold']:
            strategy['break_suggestions'].append({
                'type': 'mandatory_break',
                'duration_minutes': 10,
                'reason': 'high_fatigue_detected'
            })
        
        # 2. 집중도가 낮은 경우
        if state.attention_level < self.optimization_rules['attention_threshold']:
            strategy['presentation_adjustments'].extend([
                {'type': 'increase_interactivity', 'level': 'high'},
                {'type': 'add_visual_cues', 'frequency': 'every_paragraph'},
                {'type': 'reduce_text_density', 'factor': 0.7}
            ])
        
        # 3. 작업 기억 부하가 높은 경우
        if state.working_memory_load > 0.7:
            strategy['content_modifications'].extend([
                {'type': 'reduce_chunk_size', 'new_size': max(3, complexity.recommended_chunk_size - 2)},
                {'type': 'add_memory_aids', 'aids': ['summaries', 'key_points', 'mnemonics']},
                {'type': 'sequential_presentation', 'overlap': False}
            ])
        
        # 4. 스트레스 수준이 높은 경우
        if state.stress_level > 0.6:
            strategy['interaction_recommendations'].extend([
                {'type': 'provide_hints', 'availability': 'always'},
                {'type': 'allow_retries', 'unlimited': True},
                {'type': 'positive_reinforcement', 'frequency': 'high'}
            ])
        
        # 5. 콘텐츠 복잡도에 따른 조정
        if complexity.cognitive_demand > 0.8:
            strategy['content_modifications'].extend([
                {'type': 'add_scaffolding', 'level': 'extensive'},
                {'type': 'provide_examples', 'count': 3},
                {'type': 'gradual_complexity_increase', 'steps': 5}
            ])
        
        # 6. 몰입 상태 유지/향상
        if state.flow_state > 0.7:
            strategy['presentation_adjustments'].append({
                'type': 'maintain_current_pace',
                'reason': 'optimal_flow_state'
            })
        else:
            strategy['presentation_adjustments'].append({
                'type': 'adjust_challenge_level',
                'target_difficulty': self._calculate_optimal_difficulty(state)
            })
        
        return strategy
    
    def _calculate_optimal_difficulty(self, state: CognitiveState) -> float:
        """최적 난이도 계산"""
        # Csikszentmihalyi의 몰입 이론에 기반
        skill_level = (state.processing_speed + (1 - state.stress_level)) / 2
        
        # 스킬 수준보다 약간 높은 도전 수준이 최적
        optimal_difficulty = skill_level + 0.1
        
        # 피로도와 집중도 고려
        if state.fatigue_level > 0.6:
            optimal_difficulty -= 0.1
        if state.attention_level < 0.5:
            optimal_difficulty -= 0.15
        
        return max(0.1, min(1.0, optimal_difficulty))
    
    def generate_adaptive_break_schedule(self, user_id: str, session_duration_minutes: int) -> List[Dict[str, Any]]:
        """적응형 휴식 스케줄 생성"""
        if user_id not in self.cognitive_states or not self.cognitive_states[user_id]:
            # 기본 스케줄 (Pomodoro 기법)
            return self._generate_default_break_schedule(session_duration_minutes)
        
        recent_states = self.cognitive_states[user_id][-5:]  # 최근 5개 상태
        avg_fatigue = sum(s.fatigue_level for s in recent_states) / len(recent_states)
        avg_attention = sum(s.attention_level for s in recent_states) / len(recent_states)
        
        # 개인화된 휴식 간격 계산
        if avg_fatigue > 0.6 or avg_attention < 0.5:
            break_interval = 20  # 더 자주 휴식
        elif avg_fatigue < 0.3 and avg_attention > 0.8:
            break_interval = 35  # 덜 자주 휴식
        else:
            break_interval = 25  # 기본 간격
        
        breaks = []
        current_time = break_interval
        
        while current_time < session_duration_minutes:
            break_duration = self._calculate_break_duration(avg_fatigue, current_time)
            
            breaks.append({
                'time_minutes': current_time,
                'duration_minutes': break_duration,
                'type': self._determine_break_type(avg_fatigue, avg_attention),
                'activities': self._suggest_break_activities(avg_fatigue, avg_attention)
            })
            
            current_time += break_interval + break_duration
        
        return breaks
    
    def _generate_default_break_schedule(self, session_duration_minutes: int) -> List[Dict[str, Any]]:
        """기본 휴식 스케줄 생성"""
        breaks = []
        break_interval = self.optimization_rules['break_interval']
        current_time = break_interval
        
        while current_time < session_duration_minutes:
            breaks.append({
                'time_minutes': current_time,
                'duration_minutes': 5,
                'type': 'standard',
                'activities': ['stretch', 'hydrate', 'eye_rest']
            })
            current_time += break_interval + 5
        
        return breaks
    
    def _calculate_break_duration(self, fatigue_level: float, elapsed_time: int) -> int:
        """휴식 시간 계산"""
        base_duration = 5
        
        # 피로도에 따른 조정
        if fatigue_level > 0.7:
            base_duration += 5
        elif fatigue_level > 0.5:
            base_duration += 2
        
        # 경과 시간에 따른 조정 (시간이 길수록 더 긴 휴식)
        if elapsed_time > 60:
            base_duration += 3
        elif elapsed_time > 30:
            base_duration += 1
        
        return min(15, base_duration)  # 최대 15분
    
    def _determine_break_type(self, fatigue_level: float, attention_level: float) -> str:
        """휴식 유형 결정"""
        if fatigue_level > 0.7:
            return 'restorative'  # 회복적 휴식
        elif attention_level < 0.5:
            return 'activating'   # 활성화 휴식
        else:
            return 'maintenance'  # 유지 휴식
    
    def _suggest_break_activities(self, fatigue_level: float, attention_level: float) -> List[str]:
        """휴식 활동 제안"""
        activities = ['hydrate', 'eye_rest']  # 기본 활동
        
        if fatigue_level > 0.6:
            activities.extend(['deep_breathing', 'meditation', 'power_nap'])
        
        if attention_level < 0.6:
            activities.extend(['light_exercise', 'stretching', 'fresh_air'])
        
        return activities

# 사용 예제
if __name__ == "__main__":
    optimizer = CognitiveLoadOptimizer()
    
    # 콘텐츠 복잡도 분석
    sample_content = """
    통계학에서 가설검정은 모집단에 대한 가설을 표본 데이터를 사용하여 검증하는 과정입니다.
    귀무가설(H0)과 대립가설(H1)을 설정하고, 유의수준(α)을 정한 후 검정통계량을 계산합니다.
    p-값이 유의수준보다 작으면 귀무가설을 기각하고 대립가설을 채택합니다.
    """
    
    complexity = optimizer.analyze_content_complexity(sample_content, "hypothesis_testing_intro")
    print(f"콘텐츠 복잡도: {complexity.cognitive_demand:.2f}")
    print(f"권장 청크 크기: {complexity.recommended_chunk_size}")
    
    # 인지 상태 모니터링
    interaction_data = {
        'mouse_movements': 25,
        'clicks_per_minute': 5,
        'session_duration_minutes': 30,
        'error_rate': 0.1
    }
    
    cognitive_state = optimizer.monitor_cognitive_state('user123', interaction_data)
    print(f"집중도: {cognitive_state.attention_level:.2f}")
    print(f"피로도: {cognitive_state.fatigue_level:.2f}")
    
    # 최적화 전략 생성
    strategy = optimizer.optimize_content_presentation('user123', 'hypothesis_testing_intro')
    print(f"제안된 최적화 전략: {len(strategy['content_modifications'])}개 수정사항")