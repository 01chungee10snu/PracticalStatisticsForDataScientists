"""
Content Standardization System - Enhanced Version with Template Engine
"""

import re
import os
from typing import Dict, List, Any, Tuple, Optional
from enum import Enum


class DifficultyLevel(Enum):
    """난이도 수준"""
    FOUNDATION = "foundation"
    DEVELOPING = "developing"
    PROFICIENT = "proficient"
    ADVANCED = "advanced"


class AutoFormatter:
    """자동 포맷팅 도구"""
    
    def __init__(self):
        pass
    
    def format_content(self, content_data: Dict[str, Any]) -> Dict[str, Any]:
        """콘텐츠 데이터 포맷팅"""
        formatted_data = content_data.copy()
        
        if 'sections' in formatted_data:
            for section_name, section_data in formatted_data['sections'].items():
                if isinstance(section_data, dict) and 'content' in section_data:
                    # 마크다운 포맷팅
                    formatted_data['sections'][section_name]['content'] = self._format_markdown(
                        section_data['content']
                    )
                    # 링크 수정
                    formatted_data['sections'][section_name]['content'] = self._fix_links(
                        formatted_data['sections'][section_name]['content']
                    )
        
        return formatted_data
    
    def _format_markdown(self, content: str) -> str:
        """마크다운 포맷팅"""
        lines = content.split('\n')
        formatted_lines = []
        
        for line in lines:
            # 연속된 빈 줄 제거
            if not line.strip():
                if not formatted_lines or formatted_lines[-1].strip():
                    formatted_lines.append('')
            else:
                formatted_lines.append(line)
        
        return '\n'.join(formatted_lines)
    
    def _fix_links(self, content: str) -> str:
        """링크 수정"""
        # 마크다운 링크 찾기
        links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
        
        for text, url in links:
            original = f"[{text}]({url})"
            fixed_url = url.strip()
            
            # https:// 추가
            if not re.match(r'^https?://', fixed_url) and fixed_url.startswith('www.'):
                fixed_url = 'https://' + fixed_url
            
            fixed = f"[{text}]({fixed_url})"
            content = content.replace(original, fixed)
        
        return content


class ContentTemplate:
    """콘텐츠 템플릿"""
    
    def __init__(self, title: str, difficulty_level: str, estimated_time: int, 
                 prerequisites: List[str] = None, sections: Dict[str, Any] = None):
        """초기화"""
        self.title = title
        self.difficulty_level = difficulty_level
        self.estimated_time = estimated_time
        self.prerequisites = prerequisites or []
        self.sections = sections or {}
    
    @classmethod
    def create_default_template(cls, difficulty_level: str) -> 'ContentTemplate':
        """기본 템플릿 생성"""
        # 공통 섹션
        common_sections = {
            "concept_introduction": {
                "required": True,
                "description": "핵심 포인트와 정의",
                "min_words": 100,
            },
            "visual_explanation": {
                "required": True,
                "description": "인터랙티브 시각화",
                "visualization_required": True,
            },
            "practical_example": {
                "required": True,
                "description": "실습 코드와 해석",
                "code_blocks_required": True,
                "min_code_blocks": 1,
            },
            "common_misconceptions": {
                "required": True,
                "description": "흔한 오해와 올바른 이해",
                "min_items": 2,
            },
            "self_assessment": {
                "required": True,
                "description": "자가 점검 문제",
                "min_questions": 3,
            }
        }
        
        # 난이도별 설정
        if difficulty_level == DifficultyLevel.FOUNDATION.value:
            title = "기초 수준 콘텐츠"
            estimated_time = 20
        elif difficulty_level == DifficultyLevel.DEVELOPING.value:
            title = "발전 수준 콘텐츠"
            estimated_time = 30
            common_sections["practical_example"]["min_code_blocks"] = 2
            common_sections["self_assessment"]["min_questions"] = 4
        elif difficulty_level == DifficultyLevel.PROFICIENT.value:
            title = "숙련 수준 콘텐츠"
            estimated_time = 45
            common_sections["practical_example"]["min_code_blocks"] = 3
            common_sections["advanced_concepts"] = {
                "required": True,
                "description": "심화 개념 설명",
                "min_words": 200,
            }
            common_sections["self_assessment"]["min_questions"] = 5
        elif difficulty_level == DifficultyLevel.ADVANCED.value:
            title = "고급 수준 콘텐츠"
            estimated_time = 60
            common_sections["practical_example"]["min_code_blocks"] = 4
            common_sections["advanced_concepts"] = {
                "required": True,
                "description": "심화 개념 설명",
                "min_words": 300,
            }
            common_sections["research_insights"] = {
                "required": True,
                "description": "최신 연구 및 고급 응용",
                "min_words": 200,
            }
            common_sections["self_assessment"]["min_questions"] = 6
        else:
            raise ValueError(f"유효하지 않은 난이도: {difficulty_level}")
        
        return cls(title, difficulty_level, estimated_time, [], common_sections)


class TemplateEngine:
    """템플릿 엔진"""
    
    def __init__(self):
        """초기화"""
        self.templates = {}
        self._load_default_templates()
    
    def _load_default_templates(self):
        """기본 템플릿 로드"""
        for level in DifficultyLevel:
            self.templates[level.value] = ContentTemplate.create_default_template(level.value)
    
    def get_template(self, difficulty_level: str) -> ContentTemplate:
        """템플릿 가져오기"""
        if difficulty_level not in self.templates:
            raise ValueError(f"유효하지 않은 난이도: {difficulty_level}")
        return self.templates[difficulty_level]
    
    def apply_template(self, content_data: Dict[str, Any]) -> Dict[str, Any]:
        """템플릿 적용"""
        if 'difficulty_level' not in content_data:
            raise ValueError("콘텐츠 데이터에 난이도가 지정되지 않았습니다")
        
        difficulty_level = content_data['difficulty_level']
        template = self.get_template(difficulty_level)
        
        # 템플릿 구조 적용
        result = {
            'title': content_data.get('title', template.title),
            'difficulty_level': difficulty_level,
            'estimated_time': content_data.get('estimated_time', template.estimated_time),
            'prerequisites': content_data.get('prerequisites', template.prerequisites),
            'sections': {}
        }
        
        # 필수 섹션 확인
        for section_name, section_config in template.sections.items():
            if section_config.get('required', False):
                if section_name not in content_data.get('sections', {}):
                    result['sections'][section_name] = {
                        'content': f"[TODO: {section_config['description']}]",
                        'template_config': section_config
                    }
                else:
                    result['sections'][section_name] = {
                        'content': content_data['sections'][section_name].get('content', ''),
                        'template_config': section_config
                    }
        
        # 추가 섹션 포함
        for section_name, section_data in content_data.get('sections', {}).items():
            if section_name not in result['sections']:
                result['sections'][section_name] = {
                    'content': section_data.get('content', ''),
                    'template_config': {'required': False, 'description': '사용자 정의 섹션'}
                }
        
        return result
    
    def validate_against_template(self, content_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """템플릿 기준 검증"""
        issues = []
        
        if 'difficulty_level' not in content_data:
            issues.append("난이도가 지정되지 않았습니다")
            return False, issues
        
        try:
            template = self.get_template(content_data['difficulty_level'])
        except ValueError as e:
            issues.append(str(e))
            return False, issues
        
        # 필수 섹션 검사
        for section_name, section_config in template.sections.items():
            if section_config.get('required', False):
                if section_name not in content_data.get('sections', {}):
                    issues.append(f"필수 섹션 누락: {section_name}")
                else:
                    section = content_data['sections'][section_name]
                    
                    # 최소 단어 수 검사
                    if 'min_words' in section_config and 'content' in section:
                        word_count = len(section['content'].split())
                        if word_count < section_config['min_words']:
                            issues.append(
                                f"섹션 '{section_name}'의 단어 수가 {word_count}개로, "
                                f"최소 요구사항인 {section_config['min_words']}개보다 적습니다"
                            )
                    
                    # 코드 블록 검사
                    if section_config.get('code_blocks_required', False):
                        code_blocks = re.findall(r'```[\w]*\n[\s\S]*?\n```', section.get('content', ''))
                        if not code_blocks:
                            issues.append(f"섹션 '{section_name}'에 코드 블록이 필요합니다")
                        elif 'min_code_blocks' in section_config and len(code_blocks) < section_config['min_code_blocks']:
                            issues.append(
                                f"섹션 '{section_name}'의 코드 블록이 {len(code_blocks)}개로, "
                                f"최소 요구사항인 {section_config['min_code_blocks']}개보다 적습니다"
                            )
                    
                    # 최소 항목 수 검사
                    if 'min_items' in section_config:
                        items = re.findall(r'^\s*[-*]\s+', section.get('content', ''), re.MULTILINE)
                        if len(items) < section_config['min_items']:
                            issues.append(
                                f"섹션 '{section_name}'의 항목이 {len(items)}개로, "
                                f"최소 요구사항인 {section_config['min_items']}개보다 적습니다"
                            )
                    
                    # 최소 질문 수 검사
                    if 'min_questions' in section_config:
                        questions = re.findall(r'^\s*\d+\.\s+', section.get('content', ''), re.MULTILINE)
                        if len(questions) < section_config['min_questions']:
                            issues.append(
                                f"섹션 '{section_name}'의 질문이 {len(questions)}개로, "
                                f"최소 요구사항인 {section_config['min_questions']}개보다 적습니다"
                            )
        
        return len(issues) == 0, issues


class ContentStandardizer:
    """콘텐츠 표준화 도구 - 템플릿 엔진 통합"""
    
    def __init__(self):
        self.formatter = AutoFormatter()
        self.template_engine = TemplateEngine()
    
    def standardize_content(self, content_data: Dict[str, Any]) -> Dict[str, Any]:
        """콘텐츠 표준화 - 템플릿 적용 및 포맷팅"""
        # 1. 템플릿 적용 (난이도가 지정된 경우)
        if 'difficulty_level' in content_data:
            try:
                content_data = self.template_engine.apply_template(content_data)
            except ValueError as e:
                print(f"템플릿 적용 실패: {e}")
        
        # 2. 포맷팅 적용
        return self.formatter.format_content(content_data)
    
    def validate_content(self, content_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """콘텐츠 검증"""
        return self.template_engine.validate_against_template(content_data)
    
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
        
        if content_data.get('prerequisites'):
            md_lines.append("**선수 지식:**")
            for prereq in content_data['prerequisites']:
                md_lines.append(f"- {prereq}")
        
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


# 테스트용 함수
def test_formatter():
    """포맷터 테스트"""
    formatter = AutoFormatter()
    
    test_content = {
        'title': '테스트 콘텐츠',
        'difficulty_level': 'foundation',
        'estimated_time': 30,
        'prerequisites': ['기초 지식'],
        'sections': {
            'concept_introduction': {
                'content': '''이것은 테스트입니다.


여러 줄의 내용이 있습니다.

[링크 테스트](www.example.com)'''
            },
            'practical_example': {
                'content': '''코드 예제:

```python
print("Hello World")
```

설명입니다.'''
            }
        }
    }
    
    formatted = formatter.format_content(test_content)
    return formatted


if __name__ == "__main__":
    result = test_formatter()
    print("포맷팅 테스트 완료")
    print(f"제목: {result['title']}")
    print(f"섹션 수: {len(result['sections'])}")