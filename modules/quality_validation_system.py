"""
품질 검증 시스템 (Quality Validation System)
- 필수 섹션 포함 여부 자동 확인
- 콘텐츠 품질 기준 검증 기능
- 요구사항 1.2 구현
"""

import re
import json
from typing import Dict, List, Any, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class ValidationLevel(Enum):
    """검증 수준"""
    BASIC = "basic"
    STANDARD = "standard"
    COMPREHENSIVE = "comprehensive"


class QualityGrade(Enum):
    """품질 등급"""
    EXCELLENT = "A+"  # 90-100
    GOOD = "A"        # 80-89
    SATISFACTORY = "B"  # 70-79
    NEEDS_IMPROVEMENT = "C"  # 60-69
    POOR = "D"        # 50-59
    FAIL = "F"        # 0-49


@dataclass
class ValidationRule:
    """검증 규칙"""
    name: str
    description: str
    weight: float
    min_threshold: float
    max_threshold: Optional[float] = None
    is_required: bool = True


@dataclass
class ValidationResult:
    """검증 결과"""
    rule_name: str
    passed: bool
    score: float
    message: str
    suggestions: List[str]


@dataclass
class QualityReport:
    """품질 보고서"""
    overall_score: float
    grade: str
    passed_rules: int
    total_rules: int
    validation_results: List[ValidationResult]
    missing_sections: List[str]
    recommendations: List[str]
    validation_time: str


class QualityValidator:
    """품질 검증기"""
    
    def __init__(self):
        self.validation_rules = self._initialize_validation_rules()
        self.required_sections = self._initialize_required_sections()
        self.quality_thresholds = self._initialize_quality_thresholds()
    
    def _initialize_validation_rules(self) -> Dict[str, ValidationRule]:
        """검증 규칙 초기화"""
        return {
            'content_length': ValidationRule(
                name='콘텐츠 길이',
                description='적절한 콘텐츠 분량 확인',
                weight=0.15,
                min_threshold=200,  # 최소 200단어
                max_threshold=3000,  # 최대 3000단어
                is_required=True
            ),
            'section_completeness': ValidationRule(
                name='섹션 완성도',
                description='필수 섹션 포함 여부',
                weight=0.25,
                min_threshold=0.8,  # 80% 이상 필수 섹션 포함
                is_required=True
            ),
            'content_depth': ValidationRule(
                name='콘텐츠 깊이',
                description='각 섹션의 내용 충실도',
                weight=0.20,
                min_threshold=50,  # 섹션당 최소 50단어
                is_required=True
            ),
            'code_quality': ValidationRule(
                name='코드 품질',
                description='코드 블록의 품질과 설명',
                weight=0.15,
                min_threshold=1,  # 최소 1개 코드 블록
                is_required=False
            ),
            'readability': ValidationRule(
                name='가독성',
                description='텍스트의 읽기 쉬움 정도',
                weight=0.15,
                min_threshold=60,  # 가독성 점수 60 이상
                is_required=True
            ),
            'structure_quality': ValidationRule(
                name='구조 품질',
                description='헤더, 리스트 등 구조적 요소',
                weight=0.10,
                min_threshold=3,  # 최소 3개 헤더
                is_required=True
            )
        }
    
    def _initialize_required_sections(self) -> Dict[str, List[str]]:
        """난이도별 필수 섹션 정의"""
        return {
            'foundation': [
                'concept_introduction',
                'practical_example',
                'self_assessment'
            ],
            'developing': [
                'concept_introduction',
                'visual_explanation',
                'practical_example',
                'common_misconceptions',
                'self_assessment'
            ],
            'proficient': [
                'concept_introduction',
                'visual_explanation',
                'practical_example',
                'common_misconceptions',
                'advanced_concepts',
                'self_assessment'
            ],
            'advanced': [
                'concept_introduction',
                'visual_explanation',
                'practical_example',
                'common_misconceptions',
                'advanced_concepts',
                'research_insights',
                'self_assessment'
            ]
        }
    
    def _initialize_quality_thresholds(self) -> Dict[str, float]:
        """품질 임계값 설정"""
        return {
            'excellent': 90.0,
            'good': 80.0,
            'satisfactory': 70.0,
            'needs_improvement': 60.0,
            'poor': 50.0
        }
    
    def validate_content(self, content_data: Dict[str, Any], 
                        validation_level: ValidationLevel = ValidationLevel.STANDARD) -> QualityReport:
        """콘텐츠 품질 검증"""
        validation_results = []
        
        # 1. 섹션 완성도 검증
        section_result = self._validate_section_completeness(content_data)
        validation_results.append(section_result)
        
        # 2. 콘텐츠 길이 검증
        length_result = self._validate_content_length(content_data)
        validation_results.append(length_result)
        
        # 3. 콘텐츠 깊이 검증
        depth_result = self._validate_content_depth(content_data)
        validation_results.append(depth_result)
        
        # 4. 구조 품질 검증
        structure_result = self._validate_structure_quality(content_data)
        validation_results.append(structure_result)
        
        # 5. 가독성 검증
        readability_result = self._validate_readability(content_data)
        validation_results.append(readability_result)
        
        # 6. 코드 품질 검증 (선택적)
        if self._has_code_content(content_data):
            code_result = self._validate_code_quality(content_data)
            validation_results.append(code_result)
        
        # 전체 점수 계산
        overall_score = self._calculate_overall_score(validation_results)
        
        # 등급 결정
        grade = self._determine_grade(overall_score)
        
        # 누락된 섹션 확인
        missing_sections = self._find_missing_sections(content_data)
        
        # 권장사항 생성
        recommendations = self._generate_recommendations(validation_results, missing_sections)
        
        # 통과한 규칙 수 계산
        passed_rules = sum(1 for result in validation_results if result.passed)
        
        return QualityReport(
            overall_score=overall_score,
            grade=grade,
            passed_rules=passed_rules,
            total_rules=len(validation_results),
            validation_results=validation_results,
            missing_sections=missing_sections,
            recommendations=recommendations,
            validation_time=datetime.now().isoformat()
        )
    
    def _validate_section_completeness(self, content_data: Dict[str, Any]) -> ValidationResult:
        """섹션 완성도 검증"""
        difficulty_level = content_data.get('difficulty_level', 'foundation')
        required_sections = self.required_sections.get(difficulty_level, [])
        
        if not required_sections:
            return ValidationResult(
                rule_name='section_completeness',
                passed=True,
                score=100.0,
                message="필수 섹션 요구사항이 없습니다.",
                suggestions=[]
            )
        
        existing_sections = set(content_data.get('sections', {}).keys())
        required_sections_set = set(required_sections)
        
        # 포함된 필수 섹션 비율 계산
        included_sections = existing_sections.intersection(required_sections_set)
        completeness_ratio = len(included_sections) / len(required_sections_set)
        
        rule = self.validation_rules['section_completeness']
        passed = completeness_ratio >= rule.min_threshold
        score = completeness_ratio * 100
        
        missing_sections = required_sections_set - existing_sections
        
        if passed:
            message = f"필수 섹션 {len(included_sections)}/{len(required_sections_set)}개 포함됨"
            suggestions = []
        else:
            message = f"필수 섹션 부족: {len(included_sections)}/{len(required_sections_set)}개만 포함됨"
            suggestions = [f"다음 섹션을 추가하세요: {', '.join(missing_sections)}"]
        
        return ValidationResult(
            rule_name='section_completeness',
            passed=passed,
            score=score,
            message=message,
            suggestions=suggestions
        )
    
    def _validate_content_length(self, content_data: Dict[str, Any]) -> ValidationResult:
        """콘텐츠 길이 검증"""
        total_words = 0
        sections = content_data.get('sections', {})
        
        for section_data in sections.values():
            if isinstance(section_data, dict):
                content = section_data.get('content', '')
            else:
                content = str(section_data)
            total_words += len(content.split())
        
        rule = self.validation_rules['content_length']
        
        if total_words < rule.min_threshold:
            passed = False
            score = (total_words / rule.min_threshold) * 100
            message = f"콘텐츠가 너무 짧습니다 ({total_words}단어, 최소 {rule.min_threshold}단어 필요)"
            suggestions = ["더 자세한 설명과 예제를 추가하세요"]
        elif rule.max_threshold and total_words > rule.max_threshold:
            passed = False
            score = max(0, 100 - ((total_words - rule.max_threshold) / rule.max_threshold) * 50)
            message = f"콘텐츠가 너무 깁니다 ({total_words}단어, 최대 {rule.max_threshold}단어 권장)"
            suggestions = ["핵심 내용으로 요약하거나 섹션을 나누어 보세요"]
        else:
            passed = True
            score = 100.0
            message = f"적절한 콘텐츠 길이입니다 ({total_words}단어)"
            suggestions = []
        
        return ValidationResult(
            rule_name='content_length',
            passed=passed,
            score=score,
            message=message,
            suggestions=suggestions
        )
    
    def _validate_content_depth(self, content_data: Dict[str, Any]) -> ValidationResult:
        """콘텐츠 깊이 검증"""
        sections = content_data.get('sections', {})
        rule = self.validation_rules['content_depth']
        
        if not sections:
            return ValidationResult(
                rule_name='content_depth',
                passed=False,
                score=0.0,
                message="섹션이 없습니다",
                suggestions=["콘텐츠 섹션을 추가하세요"]
            )
        
        section_scores = []
        shallow_sections = []
        
        for section_name, section_data in sections.items():
            if isinstance(section_data, dict):
                content = section_data.get('content', '')
            else:
                content = str(section_data)
            
            word_count = len(content.split())
            
            if word_count >= rule.min_threshold:
                section_scores.append(100)
            else:
                section_scores.append((word_count / rule.min_threshold) * 100)
                shallow_sections.append(section_name)
        
        average_score = sum(section_scores) / len(section_scores)
        passed = average_score >= 70  # 평균 70점 이상
        
        if passed:
            message = f"콘텐츠 깊이가 충분합니다 (평균 {average_score:.1f}점)"
            suggestions = []
        else:
            message = f"일부 섹션의 내용이 부족합니다 (평균 {average_score:.1f}점)"
            suggestions = [f"다음 섹션의 내용을 보강하세요: {', '.join(shallow_sections)}"]
        
        return ValidationResult(
            rule_name='content_depth',
            passed=passed,
            score=average_score,
            message=message,
            suggestions=suggestions
        )
    
    def _validate_structure_quality(self, content_data: Dict[str, Any]) -> ValidationResult:
        """구조 품질 검증"""
        sections = content_data.get('sections', {})
        rule = self.validation_rules['structure_quality']
        
        total_headers = 0
        total_lists = 0
        total_code_blocks = 0
        
        for section_data in sections.values():
            if isinstance(section_data, dict):
                content = section_data.get('content', '')
            else:
                content = str(section_data)
            
            # 헤더 개수
            headers = re.findall(r'^#+\s+', content, re.MULTILINE)
            total_headers += len(headers)
            
            # 리스트 개수
            lists = re.findall(r'^\s*[-*+]\s+', content, re.MULTILINE)
            total_lists += len(lists)
            
            # 코드 블록 개수
            code_blocks = re.findall(r'```[\s\S]*?```', content)
            total_code_blocks += len(code_blocks)
        
        # 구조 점수 계산
        structure_score = 0
        
        # 헤더 점수 (40점)
        if total_headers >= rule.min_threshold:
            structure_score += 40
        else:
            structure_score += (total_headers / rule.min_threshold) * 40
        
        # 리스트 점수 (30점)
        if total_lists >= 2:
            structure_score += 30
        else:
            structure_score += (total_lists / 2) * 30
        
        # 코드 블록 점수 (30점)
        if total_code_blocks >= 1:
            structure_score += 30
        else:
            structure_score += total_code_blocks * 30
        
        passed = structure_score >= 70
        
        suggestions = []
        if total_headers < rule.min_threshold:
            suggestions.append(f"헤더를 더 추가하세요 (현재 {total_headers}개, 권장 {rule.min_threshold}개 이상)")
        if total_lists < 2:
            suggestions.append("리스트를 사용하여 내용을 정리하세요")
        if total_code_blocks < 1:
            suggestions.append("실습 코드나 예제를 추가하세요")
        
        message = f"구조 품질 점수: {structure_score:.1f}점 (헤더 {total_headers}개, 리스트 {total_lists}개, 코드블록 {total_code_blocks}개)"
        
        return ValidationResult(
            rule_name='structure_quality',
            passed=passed,
            score=structure_score,
            message=message,
            suggestions=suggestions
        )
    
    def _validate_readability(self, content_data: Dict[str, Any]) -> ValidationResult:
        """가독성 검증"""
        sections = content_data.get('sections', {})
        
        if not sections:
            return ValidationResult(
                rule_name='readability',
                passed=False,
                score=0.0,
                message="검증할 콘텐츠가 없습니다",
                suggestions=["콘텐츠를 추가하세요"]
            )
        
        total_sentences = 0
        total_words = 0
        long_sentences = 0
        
        for section_data in sections.values():
            if isinstance(section_data, dict):
                content = section_data.get('content', '')
            else:
                content = str(section_data)
            
            # 문장 분리 (간단한 방법)
            sentences = re.split(r'[.!?]+', content)
            sentences = [s.strip() for s in sentences if s.strip()]
            
            total_sentences += len(sentences)
            
            for sentence in sentences:
                words = sentence.split()
                total_words += len(words)
                
                # 긴 문장 체크 (20단어 이상)
                if len(words) > 20:
                    long_sentences += 1
        
        # 가독성 점수 계산 (간단한 공식)
        if total_sentences > 0:
            avg_words_per_sentence = total_words / total_sentences
            long_sentence_ratio = long_sentences / total_sentences
            
            # 점수 계산 (평균 문장 길이와 긴 문장 비율 고려)
            readability_score = max(0, 100 - (avg_words_per_sentence - 10) * 2 - long_sentence_ratio * 30)
        else:
            readability_score = 0
        
        rule = self.validation_rules['readability']
        passed = readability_score >= rule.min_threshold
        
        suggestions = []
        if avg_words_per_sentence > 15:
            suggestions.append("문장을 더 짧게 나누어 보세요")
        if long_sentence_ratio > 0.3:
            suggestions.append("긴 문장을 줄이고 간결하게 작성하세요")
        if not passed:
            suggestions.append("더 읽기 쉽게 작성하세요")
        
        message = f"가독성 점수: {readability_score:.1f}점 (평균 문장길이: {avg_words_per_sentence:.1f}단어)"
        
        return ValidationResult(
            rule_name='readability',
            passed=passed,
            score=readability_score,
            message=message,
            suggestions=suggestions
        )
    
    def _validate_code_quality(self, content_data: Dict[str, Any]) -> ValidationResult:
        """코드 품질 검증"""
        sections = content_data.get('sections', {})
        
        total_code_blocks = 0
        code_with_comments = 0
        code_with_explanation = 0
        
        for section_data in sections.values():
            if isinstance(section_data, dict):
                content = section_data.get('content', '')
            else:
                content = str(section_data)
            
            # 코드 블록 찾기
            code_blocks = re.findall(r'```[\w]*\n([\s\S]*?)\n```', content)
            total_code_blocks += len(code_blocks)
            
            for code_block in code_blocks:
                # 주석이 있는지 확인
                if '#' in code_block:
                    code_with_comments += 1
                
                # 코드 블록 앞뒤에 설명이 있는지 확인 (간단한 체크)
                code_start = content.find('```')
                if code_start > 0:
                    before_code = content[:code_start].strip()
                    if before_code and len(before_code.split()) >= 5:
                        code_with_explanation += 1
        
        rule = self.validation_rules['code_quality']
        
        if total_code_blocks == 0:
            return ValidationResult(
                rule_name='code_quality',
                passed=True,  # 코드가 없어도 통과 (선택적 규칙)
                score=100.0,
                message="코드 블록이 없습니다",
                suggestions=[]
            )
        
        # 코드 품질 점수 계산
        comment_ratio = code_with_comments / total_code_blocks
        explanation_ratio = code_with_explanation / total_code_blocks
        
        code_quality_score = (comment_ratio * 50) + (explanation_ratio * 50)
        passed = code_quality_score >= 60
        
        suggestions = []
        if comment_ratio < 0.5:
            suggestions.append("코드에 주석을 더 추가하세요")
        if explanation_ratio < 0.5:
            suggestions.append("코드 블록에 대한 설명을 추가하세요")
        
        message = f"코드 품질 점수: {code_quality_score:.1f}점 (코드블록 {total_code_blocks}개, 주석 {code_with_comments}개)"
        
        return ValidationResult(
            rule_name='code_quality',
            passed=passed,
            score=code_quality_score,
            message=message,
            suggestions=suggestions
        )
    
    def _has_code_content(self, content_data: Dict[str, Any]) -> bool:
        """코드 콘텐츠 포함 여부 확인"""
        sections = content_data.get('sections', {})
        
        for section_data in sections.values():
            if isinstance(section_data, dict):
                content = section_data.get('content', '')
            else:
                content = str(section_data)
            
            if '```' in content:
                return True
        
        return False
    
    def _calculate_overall_score(self, validation_results: List[ValidationResult]) -> float:
        """전체 점수 계산"""
        weighted_score = 0.0
        total_weight = 0.0
        
        for result in validation_results:
            rule = self.validation_rules.get(result.rule_name)
            if rule:
                weighted_score += result.score * rule.weight
                total_weight += rule.weight
        
        if total_weight > 0:
            return weighted_score / total_weight
        else:
            return 0.0
    
    def _determine_grade(self, score: float) -> str:
        """점수에 따른 등급 결정"""
        if score >= self.quality_thresholds['excellent']:
            return QualityGrade.EXCELLENT.value
        elif score >= self.quality_thresholds['good']:
            return QualityGrade.GOOD.value
        elif score >= self.quality_thresholds['satisfactory']:
            return QualityGrade.SATISFACTORY.value
        elif score >= self.quality_thresholds['needs_improvement']:
            return QualityGrade.NEEDS_IMPROVEMENT.value
        elif score >= self.quality_thresholds['poor']:
            return QualityGrade.POOR.value
        else:
            return QualityGrade.FAIL.value
    
    def _find_missing_sections(self, content_data: Dict[str, Any]) -> List[str]:
        """누락된 필수 섹션 찾기"""
        difficulty_level = content_data.get('difficulty_level', 'foundation')
        required_sections = self.required_sections.get(difficulty_level, [])
        existing_sections = set(content_data.get('sections', {}).keys())
        
        return list(set(required_sections) - existing_sections)
    
    def _generate_recommendations(self, validation_results: List[ValidationResult], 
                                missing_sections: List[str]) -> List[str]:
        """권장사항 생성"""
        recommendations = []
        
        # 누락된 섹션 권장사항
        if missing_sections:
            recommendations.append(f"다음 필수 섹션을 추가하세요: {', '.join(missing_sections)}")
        
        # 검증 결과별 권장사항
        for result in validation_results:
            if not result.passed and result.suggestions:
                recommendations.extend(result.suggestions)
        
        # 중복 제거
        return list(set(recommendations))


# 테스트 및 데모 함수
def test_quality_validator():
    """품질 검증기 테스트"""
    validator = QualityValidator()
    
    # 테스트 콘텐츠
    test_content = {
        'title': '기술통계량 이해하기',
        'difficulty_level': 'developing',
        'estimated_time': 45,
        'sections': {
            'concept_introduction': {
                'content': '''기술통계량은 데이터의 특성을 요약하는 수치들입니다. 
                주요 기술통계량에는 중심경향성과 산포도가 있습니다.
                중심경향성은 데이터의 중심 위치를 나타내며, 평균, 중앙값, 최빈값이 있습니다.
                산포도는 데이터의 퍼짐 정도를 나타내며, 분산, 표준편차, 범위 등이 있습니다.'''
            },
            'practical_example': {
                'content': '''실제 예제를 통해 기술통계량을 계산해보겠습니다.

```python
import numpy as np
data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# 평균 계산
mean = np.mean(data)
print(f"평균: {mean}")

# 표준편차 계산
std = np.std(data)
print(f"표준편차: {std}")
```

이 코드는 간단한 데이터셋의 평균과 표준편차를 계산합니다.'''
            },
            'self_assessment': {
                'content': '''다음 문제를 풀어보세요:
                
1. 데이터 [2, 4, 6, 8, 10]의 평균을 계산하세요.
2. 평균과 중앙값의 차이점을 설명하세요.
3. 표준편차가 클 때와 작을 때의 의미를 설명하세요.'''
            }
        }
    }
    
    # 검증 실행
    report = validator.validate_content(test_content)
    
    return report


if __name__ == "__main__":
    report = test_quality_validator()
    print(f"품질 점수: {report.overall_score:.1f}점")
    print(f"등급: {report.grade}")
    print(f"통과한 규칙: {report.passed_rules}/{report.total_rules}")
    
    if report.missing_sections:
        print(f"누락된 섹션: {report.missing_sections}")
    
    if report.recommendations:
        print("권장사항:")
        for rec in report.recommendations:
            print(f"- {rec}")