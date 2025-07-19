"""
Simple Content Standardization System for Testing
"""

from typing import Dict, List, Any, Tuple
from enum import Enum


class DifficultyLevel(Enum):
    """난이도 수준"""
    FOUNDATION = "foundation"
    DEVELOPING = "developing"
    PROFICIENT = "proficient"
    ADVANCED = "advanced"


class QualityChecker:
    """콘텐츠 품질 검증 도구"""
    
    def __init__(self):
        # 난이도별 필수 섹션 정의
        self.required_sections = {
            'foundation': [
                'concept_introduction',
                'practical_example'
            ],
            'developing': [
                'concept_introduction',
                'practical_example',
                'common_misconceptions'
            ],
            'proficient': [
                'concept_introduction',
                'practical_example',
                'common_misconceptions',
                'advanced_concepts'
            ],
            'advanced': [
                'concept_introduction',
                'practical_example',
                'common_misconceptions',
                'advanced_concepts',
                'research_insights'
            ]
        }
        
        # 품질 기준 정의
        self.quality_criteria = {
            'min_title_length': 5,
            'min_section_content_length': 50,
            'min_code_blocks_for_practical': 1,
            'min_words_concept_introduction': 30
        }
    
    def validate_content(self, content_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """콘텐츠 품질 검증"""
        issues = []
        
        # 1. 기본 구조 검증
        if not content_data.get('title'):
            issues.append("제목이 누락되었습니다")
        elif len(content_data['title']) < self.quality_criteria['min_title_length']:
            issues.append(f"제목이 너무 짧습니다 (최소 {self.quality_criteria['min_title_length']}자)")
        
        # 2. 난이도별 필수 섹션 검증
        difficulty = content_data.get('difficulty_level', 'foundation')
        if difficulty in self.required_sections:
            required = self.required_sections[difficulty]
            sections = content_data.get('sections', {})
            
            for required_section in required:
                if required_section not in sections:
                    issues.append(f"필수 섹션 누락: {required_section}")
                else:
                    # 섹션 내용 품질 검증
                    section_content = sections[required_section]
                    if isinstance(section_content, dict):
                        content = section_content.get('content', '')
                    else:
                        content = str(section_content)
                    
                    if len(content.strip()) < self.quality_criteria['min_section_content_length']:
                        issues.append(f"섹션 '{required_section}'의 내용이 너무 짧습니다")
        
        # 3. 특정 섹션 품질 검증
        sections = content_data.get('sections', {})
        
        # concept_introduction 단어 수 검증
        if 'concept_introduction' in sections:
            content = sections['concept_introduction']
            if isinstance(content, dict):
                text = content.get('content', '')
            else:
                text = str(content)
            
            word_count = len(text.split())
            if word_count < self.quality_criteria['min_words_concept_introduction']:
                issues.append(f"개념 소개 섹션의 단어 수가 부족합니다 ({word_count}/{self.quality_criteria['min_words_concept_introduction']})")
        
        # practical_example 코드 블록 검증
        if 'practical_example' in sections:
            content = sections['practical_example']
            if isinstance(content, dict):
                text = content.get('content', '')
            else:
                text = str(content)
            
            import re
            code_blocks = re.findall(r'```[\w]*\n[\s\S]*?\n```', text)
            if len(code_blocks) < self.quality_criteria['min_code_blocks_for_practical']:
                issues.append(f"실습 예제 섹션에 코드 블록이 부족합니다 ({len(code_blocks)}/{self.quality_criteria['min_code_blocks_for_practical']})")
        
        return len(issues) == 0, issues
    
    def get_quality_score(self, content_data: Dict[str, Any]) -> Dict[str, Any]:
        """콘텐츠 품질 점수 계산"""
        is_valid, issues = self.validate_content(content_data)
        
        # 기본 점수 계산
        total_checks = 10
        failed_checks = len(issues)
        score = max(0, (total_checks - failed_checks) / total_checks * 100)
        
        return {
            'score': round(score, 1),
            'is_valid': is_valid,
            'issues_count': failed_checks,
            'issues': issues,
            'grade': self._get_grade(score)
        }
    
    def _get_grade(self, score: float) -> str:
        """점수에 따른 등급 반환"""
        if score >= 90:
            return 'A'
        elif score >= 80:
            return 'B'
        elif score >= 70:
            return 'C'
        elif score >= 60:
            return 'D'
        else:
            return 'F'


class ContentStandardizer:
    """콘텐츠 표준화 도구"""
    
    def __init__(self):
        self.quality_checker = QualityChecker()
    
    def standardize_content(self, content_data: Dict[str, Any]) -> Dict[str, Any]:
        """콘텐츠 표준화"""
        return content_data
    
    def validate_content(self, content_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """콘텐츠 검증"""
        return self.quality_checker.validate_content(content_data)
    
    def get_quality_report(self, content_data: Dict[str, Any]) -> Dict[str, Any]:
        """품질 보고서 생성"""
        return self.quality_checker.get_quality_score(content_data)
    
    def generate_markdown(self, content_data: Dict[str, Any]) -> str:
        """마크다운 생성"""
        md_lines = []
        
        # 제목
        md_lines.append(f"# {content_data.get('title', 'Untitled')}")
        md_lines.append("")
        
        # 메타데이터
        if 'difficulty_level' in content_data:
            md_lines.append(f"**난이도:** {content_data['difficulty_level']}")
        if 'estimated_time' in content_data:
            md_lines.append(f"**예상 소요 시간:** {content_data['estimated_time']}분")
        
        md_lines.append("")
        
        # 섹션
        if 'sections' in content_data:
            for section_name, section_data in content_data['sections'].items():
                # 섹션 제목
                section_title = ' '.join(word.capitalize() for word in section_name.split('_'))
                md_lines.append(f"## {section_title}")
                md_lines.append("")
                
                # 섹션 내용
                if isinstance(section_data, dict):
                    content = section_data.get('content', '')
                else:
                    content = str(section_data)
                
                md_lines.append(content)
                md_lines.append("")
        
        return '\n'.join(md_lines)


if __name__ == "__main__":
    print("Simple Content Standardizer Test")
    standardizer = ContentStandardizer()
    
    test_data = {
        'title': 'Test Content',
        'difficulty_level': 'foundation',
        'estimated_time': 30,
        'sections': {
            'concept_introduction': {
                'content': 'This is a test content.'
            }
        }
    }
    
    result = standardizer.standardize_content(test_data)
    markdown = standardizer.generate_markdown(result)
    print("Generated Markdown:")
    print(markdown)