"""
콘텐츠 템플릿 엔진 및 품질 검증 시스템
- 표준 콘텐츠 구조 정의 및 템플릿 생성
- 필수 섹션 포함 여부 자동 확인
- 콘텐츠 품질 기준 검증 기능
"""

import json
import re
from typing import Dict, List, Any, Optional
from datetime import datetime
from dataclasses import dataclass, asdict
from .content_quality_agent import ContentQualityAgent

@dataclass
class ContentTemplate:
    """콘텐츠 템플릿 구조"""
    template_id: str
    name: str
    description: str
    required_sections: List[str]
    optional_sections: List[str]
    quality_criteria: Dict[str, Any]
    target_audience: str
    estimated_time: int

@dataclass
class ValidationResult:
    """검증 결과"""
    is_valid: bool
    score: float
    missing_sections: List[str]
    quality_issues: List[str]
    recommendations: List[str]
    validation_time: str

class ContentTemplateEngine:
    def __init__(self):
        self.quality_agent = ContentQualityAgent()
        self.templates = self._initialize_templates()
        self.validation_rules = self._initialize_validation_rules()
    
    def _initialize_templates(self) -> Dict[str, ContentTemplate]:
        """콘텐츠 템플릿 초기화"""
        templates = {}
        
        # 기초 통계 개념 템플릿
        templates['basic_statistics'] = ContentTemplate(
            template_id='basic_statistics',
            name='기초 통계 개념',
            description='통계학 기본 개념을 학습하기 위한 표준 템플릿',
            required_sections=[
                '학습 목표',
                '핵심 개념',
                '실습 예제',
                '연습 문제',
                '요약'
            ],
            optional_sections=[
                '사전 지식',
                '심화 학습',
                '참고 자료',
                'FAQ'
            ],
            quality_criteria={
                'min_word_count': 500,
                'max_word_count': 2000,
                'min_examples': 2,
                'min_exercises': 3,
                'readability_threshold': 70
            },
            target_audience='beginner',
            estimated_time=30
        )
        
        # 실습 가이드 템플릿
        templates['practice_guide'] = ContentTemplate(
            template_id='practice_guide',
            name='실습 가이드',
            description='단계별 실습을 위한 가이드 템플릿',
            required_sections=[
                '실습 개요',
                '준비 사항',
                '단계별 진행',
                '결과 해석',
                '점검 사항'
            ],
            optional_sections=[
                '문제 해결',
                '추가 도전',
                '관련 자료'
            ],
            quality_criteria={
                'min_word_count': 300,
                'max_word_count': 1500,
                'min_steps': 3,
                'max_steps': 7,
                'code_block_required': True
            },
            target_audience='intermediate',
            estimated_time=45
        )
        
        # 평가 문항 템플릿
        templates['assessment'] = ContentTemplate(
            template_id='assessment',
            name='평가 문항',
            description='학습 평가를 위한 문항 템플릿',
            required_sections=[
                '문항 개요',
                '문제',
                '정답',
                '해설',
                '평가 기준'
            ],
            optional_sections=[
                '힌트',
                '관련 개념',
                '난이도 조절'
            ],
            quality_criteria={
                'min_word_count': 200,
                'max_word_count': 800,
                'clear_question': True,
                'detailed_explanation': True
            },
            target_audience='all',
            estimated_time=15
        )
        
        return templates
    
    def _initialize_validation_rules(self) -> Dict[str, Any]:
        """검증 규칙 초기화"""
        return {
            'section_validation': {
                'required_section_penalty': 20,  # 필수 섹션 누락 시 감점
                'empty_section_penalty': 10,     # 빈 섹션 감점
                'min_section_length': 50         # 최소 섹션 길이
            },
            'content_validation': {
                'min_readability_score': 60,     # 최소 가독성 점수
                'max_complexity_ratio': 0.3,     # 최대 복잡도 비율
                'min_engagement_score': 40       # 최소 참여도 점수
            },
            'structure_validation': {
                'min_headers': 3,                # 최소 헤더 개수
                'max_paragraph_length': 200,    # 최대 문단 길이
                'min_examples': 1                # 최소 예제 개수
            }
        }
    
    def generate_content_from_template(self, template_id: str, content_data: Dict[str, Any]) -> str:
        """템플릿을 기반으로 콘텐츠 생성"""
        if template_id not in self.templates:
            raise ValueError(f"Template {template_id} not found")
        
        template = self.templates[template_id]
        
        # 템플릿 구조에 따른 마크다운 생성
        markdown_content = self._build_markdown_structure(template, content_data)
        
        return markdown_content
    
    def _build_markdown_structure(self, template: ContentTemplate, content_data: Dict[str, Any]) -> str:
        """마크다운 구조 생성"""
        markdown_lines = []
        
        # 제목
        title = content_data.get('title', '제목 없음')
        markdown_lines.append(f"# {title}")
        markdown_lines.append("")
        
        # 메타데이터
        markdown_lines.append("## 📋 학습 정보")
        markdown_lines.append(f"- **대상**: {template.target_audience}")
        markdown_lines.append(f"- **예상 시간**: {template.estimated_time}분")
        markdown_lines.append(f"- **난이도**: {content_data.get('difficulty', '기초')}")
        markdown_lines.append("")
        
        # 필수 섹션
        for section in template.required_sections:
            section_content = content_data.get('sections', {}).get(section, '')
            
            if section == '학습 목표':
                markdown_lines.append("## 🎯 학습 목표")
                if section_content:
                    goals = section_content if isinstance(section_content, list) else [section_content]
                    for goal in goals:
                        markdown_lines.append(f"- {goal}")
                else:
                    markdown_lines.append("- 학습 목표를 입력하세요")
                markdown_lines.append("")
            
            elif section == '핵심 개념':
                markdown_lines.append("## 💡 핵심 개념")
                if section_content:
                    markdown_lines.append(section_content)
                else:
                    markdown_lines.append("핵심 개념을 입력하세요.")
                markdown_lines.append("")
            
            elif section == '실습 예제':
                markdown_lines.append("## 🔬 실습 예제")
                if section_content:
                    if isinstance(section_content, list):
                        for i, example in enumerate(section_content, 1):
                            markdown_lines.append(f"### 예제 {i}")
                            markdown_lines.append(example)
                            markdown_lines.append("")
                    else:
                        markdown_lines.append(section_content)
                        markdown_lines.append("")
                else:
                    markdown_lines.append("실습 예제를 입력하세요.")
                    markdown_lines.append("")
            
            elif section == '연습 문제':
                markdown_lines.append("## 📝 연습 문제")
                if section_content:
                    if isinstance(section_content, list):
                        for i, problem in enumerate(section_content, 1):
                            markdown_lines.append(f"{i}. {problem}")
                    else:
                        markdown_lines.append(section_content)
                else:
                    markdown_lines.append("1. 연습 문제를 입력하세요.")
                markdown_lines.append("")
            
            elif section == '요약':
                markdown_lines.append("## 📚 요약")
                if section_content:
                    markdown_lines.append(section_content)
                else:
                    markdown_lines.append("학습 내용을 요약하세요.")
                markdown_lines.append("")
            
            else:
                # 기타 섹션
                section_title = section.replace('_', ' ').title()
                markdown_lines.append(f"## {section_title}")
                if section_content:
                    markdown_lines.append(section_content)
                else:
                    markdown_lines.append(f"{section} 내용을 입력하세요.")
                markdown_lines.append("")
        
        # 선택적 섹션 (내용이 있는 경우만)
        for section in template.optional_sections:
            section_content = content_data.get('sections', {}).get(section, '')
            if section_content:
                section_title = section.replace('_', ' ').title()
                markdown_lines.append(f"## {section_title}")
                markdown_lines.append(section_content)
                markdown_lines.append("")
        
        return '\n'.join(markdown_lines)
    
    def validate_content(self, content: str, template_id: str) -> ValidationResult:
        """콘텐츠 검증"""
        if template_id not in self.templates:
            raise ValueError(f"Template {template_id} not found")
        
        template = self.templates[template_id]
        
        # 1. 섹션 구조 검증
        section_validation = self._validate_sections(content, template)
        
        # 2. 콘텐츠 품질 검증
        quality_analysis = self.quality_agent.analyze_content_quality(content)
        
        # 3. 템플릿별 특수 검증
        template_validation = self._validate_template_specific(content, template)
        
        # 4. 전체 점수 계산
        total_score = self._calculate_validation_score(
            section_validation, quality_analysis, template_validation
        )
        
        # 5. 검증 결과 생성
        validation_result = ValidationResult(
            is_valid=total_score >= 70,  # 70점 이상을 합격으로 설정
            score=total_score,
            missing_sections=section_validation['missing_sections'],
            quality_issues=self._identify_quality_issues(quality_analysis),
            recommendations=self._generate_validation_recommendations(
                section_validation, quality_analysis, template_validation
            ),
            validation_time=datetime.now().isoformat()
        )
        
        return validation_result
    
    def _validate_sections(self, content: str, template: ContentTemplate) -> Dict[str, Any]:
        """섹션 구조 검증"""
        # 헤더 추출
        headers = re.findall(r'^#+\s+(.+)$', content, re.MULTILINE)
        header_texts = [h.strip() for h in headers]
        
        # 필수 섹션 확인
        missing_sections = []
        empty_sections = []
        
        for required_section in template.required_sections:
            # 섹션 키워드 매칭 (유연한 매칭)
            section_found = False
            section_empty = True
            
            for header in header_texts:
                if self._is_section_match(required_section, header):
                    section_found = True
                    # 해당 섹션의 내용 확인
                    section_content = self._extract_section_content(content, header)
                    if len(section_content.strip()) > self.validation_rules['section_validation']['min_section_length']:
                        section_empty = False
                    break
            
            if not section_found:
                missing_sections.append(required_section)
            elif section_empty:
                empty_sections.append(required_section)
        
        return {
            'missing_sections': missing_sections,
            'empty_sections': empty_sections,
            'total_headers': len(headers),
            'section_coverage': (len(template.required_sections) - len(missing_sections)) / len(template.required_sections)
        }
    
    def _is_section_match(self, required_section: str, header: str) -> bool:
        """섹션 매칭 확인"""
        # 키워드 기반 매칭
        section_keywords = {
            '학습 목표': ['목표', '학습목표', 'goal', 'objective'],
            '핵심 개념': ['개념', '핵심', 'concept', 'key'],
            '실습 예제': ['실습', '예제', 'practice', 'example'],
            '연습 문제': ['연습', '문제', 'exercise', 'problem'],
            '요약': ['요약', 'summary', '정리'],
            '실습 개요': ['개요', 'overview', '소개'],
            '준비 사항': ['준비', 'preparation', '사전준비'],
            '단계별 진행': ['단계', 'step', '진행', 'process'],
            '결과 해석': ['결과', '해석', 'result', 'interpretation'],
            '점검 사항': ['점검', 'check', '확인']
        }
        
        keywords = section_keywords.get(required_section, [required_section.lower()])
        header_lower = header.lower()
        
        return any(keyword in header_lower for keyword in keywords)
    
    def _extract_section_content(self, content: str, header: str) -> str:
        """특정 섹션의 내용 추출"""
        lines = content.split('\n')
        section_content = []
        in_section = False
        header_level = 0
        
        for line in lines:
            if line.strip().endswith(header.strip()):
                in_section = True
                header_level = len(line) - len(line.lstrip('#'))
                continue
            
            if in_section:
                # 같은 레벨 이상의 헤더를 만나면 섹션 종료
                if line.startswith('#'):
                    current_level = len(line) - len(line.lstrip('#'))
                    if current_level <= header_level:
                        break
                
                section_content.append(line)
        
        return '\n'.join(section_content)
    
    def _validate_template_specific(self, content: str, template: ContentTemplate) -> Dict[str, Any]:
        """템플릿별 특수 검증"""
        validation_result = {'issues': [], 'score': 100}
        
        # 단어 수 검증
        word_count = len(content.split())
        min_words = template.quality_criteria.get('min_word_count', 0)
        max_words = template.quality_criteria.get('max_word_count', float('inf'))
        
        if word_count < min_words:
            validation_result['issues'].append(f"내용이 너무 짧습니다 (현재: {word_count}단어, 최소: {min_words}단어)")
            validation_result['score'] -= 15
        elif word_count > max_words:
            validation_result['issues'].append(f"내용이 너무 깁니다 (현재: {word_count}단어, 최대: {max_words}단어)")
            validation_result['score'] -= 10
        
        # 예제 개수 검증
        if 'min_examples' in template.quality_criteria:
            example_count = content.lower().count('예제') + content.lower().count('example')
            min_examples = template.quality_criteria['min_examples']
            
            if example_count < min_examples:
                validation_result['issues'].append(f"예제가 부족합니다 (현재: {example_count}개, 최소: {min_examples}개)")
                validation_result['score'] -= 10
        
        # 연습 문제 개수 검증
        if 'min_exercises' in template.quality_criteria:
            exercise_patterns = [r'\d+\.\s', r'문제\s*\d+', r'연습\s*\d+']
            exercise_count = sum(len(re.findall(pattern, content)) for pattern in exercise_patterns)
            min_exercises = template.quality_criteria['min_exercises']
            
            if exercise_count < min_exercises:
                validation_result['issues'].append(f"연습 문제가 부족합니다 (현재: {exercise_count}개, 최소: {min_exercises}개)")
                validation_result['score'] -= 10
        
        # 코드 블록 검증
        if template.quality_criteria.get('code_block_required', False):
            code_blocks = re.findall(r'```[\s\S]*?```', content)
            if not code_blocks:
                validation_result['issues'].append("필수 코드 블록이 없습니다")
                validation_result['score'] -= 15
        
        return validation_result
    
    def _calculate_validation_score(self, section_validation: Dict, quality_analysis: Dict, 
                                  template_validation: Dict) -> float:
        """검증 점수 계산"""
        # 기본 점수
        base_score = 100
        
        # 섹션 검증 점수
        section_score = section_validation['section_coverage'] * 30
        missing_penalty = len(section_validation['missing_sections']) * self.validation_rules['section_validation']['required_section_penalty']
        empty_penalty = len(section_validation['empty_sections']) * self.validation_rules['section_validation']['empty_section_penalty']
        
        # 품질 분석 점수
        quality_score = quality_analysis['overall_score'] * 0.4  # 40점 만점
        
        # 템플릿별 검증 점수
        template_score = template_validation['score'] * 0.3  # 30점 만점
        
        # 최종 점수 계산
        final_score = section_score + quality_score + template_score - missing_penalty - empty_penalty
        
        return max(0, min(100, final_score))
    
    def _identify_quality_issues(self, quality_analysis: Dict) -> List[str]:
        """품질 이슈 식별"""
        issues = []
        
        if quality_analysis['readability']['score'] < self.validation_rules['content_validation']['min_readability_score']:
            issues.append("가독성이 낮습니다. 문장을 더 간단하게 작성해보세요.")
        
        if quality_analysis['structure']['score'] < 50:
            issues.append("구조가 명확하지 않습니다. 헤더와 리스트를 활용해보세요.")
        
        if quality_analysis['engagement']['score'] < self.validation_rules['content_validation']['min_engagement_score']:
            issues.append("참여도가 낮습니다. 실습이나 질문을 더 추가해보세요.")
        
        if quality_analysis['accessibility']['score'] < 80:
            issues.append("접근성을 개선해보세요. 이미지에 대체 텍스트를 추가하고 링크 설명을 명확히 하세요.")
        
        return issues
    
    def _generate_validation_recommendations(self, section_validation: Dict, quality_analysis: Dict, 
                                           template_validation: Dict) -> List[str]:
        """검증 권장사항 생성"""
        recommendations = []
        
        # 섹션 관련 권장사항
        if section_validation['missing_sections']:
            recommendations.append(f"다음 필수 섹션을 추가하세요: {', '.join(section_validation['missing_sections'])}")
        
        if section_validation['empty_sections']:
            recommendations.append(f"다음 섹션에 내용을 추가하세요: {', '.join(section_validation['empty_sections'])}")
        
        # 품질 관련 권장사항
        recommendations.extend(quality_analysis.get('recommendations', []))
        
        # 템플릿별 권장사항
        recommendations.extend(template_validation.get('issues', []))
        
        return recommendations
    
    def get_template_list(self) -> List[Dict[str, Any]]:
        """사용 가능한 템플릿 목록 반환"""
        return [
            {
                'id': template.template_id,
                'name': template.name,
                'description': template.description,
                'target_audience': template.target_audience,
                'estimated_time': template.estimated_time,
                'required_sections': template.required_sections
            }
            for template in self.templates.values()
        ]
    
    def auto_improve_content(self, content: str, template_id: str) -> str:
        """콘텐츠 자동 개선"""
        validation_result = self.validate_content(content, template_id)
        
        if validation_result.score >= 80:
            return content  # 이미 충분히 좋음
        
        # 콘텐츠 품질 에이전트를 통한 개선
        improved_content = self.quality_agent.improve_content_structure(content)
        
        # 누락된 섹션 추가
        if validation_result.missing_sections:
            improved_content = self._add_missing_sections(improved_content, validation_result.missing_sections, template_id)
        
        return improved_content
    
    def _add_missing_sections(self, content: str, missing_sections: List[str], template_id: str) -> str:
        """누락된 섹션 추가"""
        template = self.templates[template_id]
        
        for section in missing_sections:
            if section == '학습 목표':
                content += "\n\n## 🎯 학습 목표\n\n- 학습 목표를 입력하세요\n"
            elif section == '요약':
                content += "\n\n## 📚 요약\n\n학습 내용을 요약하세요.\n"
            elif section == '연습 문제':
                content += "\n\n## 📝 연습 문제\n\n1. 연습 문제를 입력하세요.\n"
            else:
                section_title = section.replace('_', ' ').title()
                content += f"\n\n## {section_title}\n\n{section} 내용을 입력하세요.\n"
        
        return content

# 사용 예제
if __name__ == "__main__":
    # 템플릿 엔진 초기화
    template_engine = ContentTemplateEngine()
    
    # 사용 가능한 템플릿 목록
    templates = template_engine.get_template_list()
    print("사용 가능한 템플릿:")
    for template in templates:
        print(f"- {template['name']}: {template['description']}")
    
    # 샘플 콘텐츠 데이터
    sample_content_data = {
        'title': '기술통계량 이해하기',
        'difficulty': '기초',
        'sections': {
            '학습 목표': [
                '기술통계량의 개념을 이해한다',
                '평균, 중앙값, 최빈값의 차이를 설명할 수 있다',
                'Python을 사용하여 기술통계량을 계산할 수 있다'
            ],
            '핵심 개념': '''
기술통계량은 데이터의 특성을 요약하는 수치들입니다.
주요 기술통계량에는 중심경향성(평균, 중앙값, 최빈값)과 
산포도(분산, 표준편차, 범위) 등이 있습니다.
            ''',
            '실습 예제': [
                '''
### 평균 계산 예제
```python
import numpy as np
data = [1, 2, 3, 4, 5]
mean = np.mean(data)
print(f"평균: {mean}")
```
                ''',
                '''
### 표준편차 계산 예제
```python
std = np.std(data)
print(f"표준편차: {std}")
```
                '''
            ],
            '연습 문제': [
                '다음 데이터의 평균을 계산하세요: [10, 20, 30, 40, 50]',
                '평균과 중앙값이 다른 경우는 언제인가요?',
                'Python을 사용하여 분산을 계산하는 코드를 작성하세요.'
            ]
        }
    }
    
    # 템플릿을 사용하여 콘텐츠 생성
    generated_content = template_engine.generate_content_from_template('basic_statistics', sample_content_data)
    print("\n생성된 콘텐츠:")
    print(generated_content[:500] + "...")
    
    # 콘텐츠 검증
    validation_result = template_engine.validate_content(generated_content, 'basic_statistics')
    print(f"\n검증 결과:")
    print(f"유효성: {'통과' if validation_result.is_valid else '실패'}")
    print(f"점수: {validation_result.score:.1f}")
    print(f"누락된 섹션: {validation_result.missing_sections}")
    print(f"권장사항: {validation_result.recommendations[:2]}")  # 처음 2개만 표시