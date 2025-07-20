"""
콘텐츠 품질 개선 에이전트
- 콘텐츠 가독성 분석 및 개선
- 정보 구조 최적화
- 학습 효과 극대화를 위한 콘텐츠 재구성
"""

import re
import json
from typing import Dict, List, Any
from datetime import datetime

class ContentQualityAgent:
    def __init__(self):
        self.quality_metrics = {
            'readability_score': 0,
            'structure_score': 0,
            'engagement_score': 0,
            'accessibility_score': 0
        }
        
    def analyze_content_quality(self, content: str) -> Dict[str, Any]:
        """콘텐츠 품질 종합 분석"""
        analysis = {
            'timestamp': datetime.now().isoformat(),
            'content_length': len(content),
            'readability': self._analyze_readability(content),
            'structure': self._analyze_structure(content),
            'engagement': self._analyze_engagement(content),
            'accessibility': self._analyze_accessibility(content),
            'recommendations': []
        }
        
        # 개선 권장사항 생성
        analysis['recommendations'] = self._generate_recommendations(analysis)
        analysis['overall_score'] = self._calculate_overall_score(analysis)
        
        return analysis
    
    def _analyze_readability(self, content: str) -> Dict[str, Any]:
        """가독성 분석"""
        sentences = content.split('.')
        words = content.split()
        
        avg_sentence_length = len(words) / max(len(sentences), 1)
        
        # 복잡한 단어 비율 (5글자 이상)
        complex_words = [w for w in words if len(w) > 5]
        complex_ratio = len(complex_words) / max(len(words), 1)
        
        # 가독성 점수 계산 (0-100)
        readability_score = max(0, 100 - (avg_sentence_length * 2) - (complex_ratio * 50))
        
        return {
            'score': readability_score,
            'avg_sentence_length': avg_sentence_length,
            'complex_word_ratio': complex_ratio,
            'total_words': len(words),
            'total_sentences': len(sentences)
        }
    
    def _analyze_structure(self, content: str) -> Dict[str, Any]:
        """정보 구조 분석"""
        # 헤더 구조 분석
        headers = re.findall(r'^#+\s+(.+)$', content, re.MULTILINE)
        
        # 리스트 구조 분석
        lists = re.findall(r'^\s*[-*+]\s+(.+)$', content, re.MULTILINE)
        
        # 코드 블록 분석
        code_blocks = re.findall(r'```[\s\S]*?```', content)
        
        # 구조 점수 계산
        structure_score = min(100, len(headers) * 10 + len(lists) * 2 + len(code_blocks) * 5)
        
        return {
            'score': structure_score,
            'header_count': len(headers),
            'list_count': len(lists),
            'code_block_count': len(code_blocks),
            'has_clear_hierarchy': len(headers) >= 3
        }
    
    def _analyze_engagement(self, content: str) -> Dict[str, Any]:
        """참여도 분석"""
        # 인터랙티브 요소 검색
        interactive_elements = [
            r'실습', r'예제', r'연습', r'문제', r'퀴즈',
            r'클릭', r'실행', r'테스트', r'확인'
        ]
        
        engagement_count = 0
        for pattern in interactive_elements:
            engagement_count += len(re.findall(pattern, content, re.IGNORECASE))
        
        # 질문 형태 문장 분석
        questions = re.findall(r'[?？]', content)
        
        engagement_score = min(100, engagement_count * 5 + len(questions) * 3)
        
        return {
            'score': engagement_score,
            'interactive_elements': engagement_count,
            'question_count': len(questions),
            'has_call_to_action': engagement_count > 0
        }
    
    def _analyze_accessibility(self, content: str) -> Dict[str, Any]:
        """접근성 분석"""
        # 이미지 alt 텍스트 확인
        images = re.findall(r'!\[([^\]]*)\]', content)
        images_with_alt = [img for img in images if img.strip()]
        
        # 링크 텍스트 분석
        links = re.findall(r'\[([^\]]+)\]', content)
        descriptive_links = [link for link in links if len(link) > 3]
        
        # 색상 의존성 확인 (기본적인 패턴)
        color_references = re.findall(r'(빨간|파란|초록|노란|색깔)', content)
        
        accessibility_score = 100
        if images and len(images_with_alt) / len(images) < 0.8:
            accessibility_score -= 20
        if links and len(descriptive_links) / len(links) < 0.7:
            accessibility_score -= 15
        if color_references:
            accessibility_score -= 10
        
        return {
            'score': max(0, accessibility_score),
            'image_alt_ratio': len(images_with_alt) / max(len(images), 1),
            'descriptive_link_ratio': len(descriptive_links) / max(len(links), 1),
            'color_dependency_issues': len(color_references)
        }
    
    def _generate_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """개선 권장사항 생성"""
        recommendations = []
        
        # 가독성 개선
        if analysis['readability']['score'] < 70:
            recommendations.append("문장 길이를 줄이고 복잡한 단어를 간단하게 바꿔보세요")
        
        # 구조 개선
        if analysis['structure']['header_count'] < 3:
            recommendations.append("명확한 섹션 구분을 위해 헤더를 더 추가하세요")
        
        # 참여도 개선
        if analysis['engagement']['score'] < 50:
            recommendations.append("실습 예제나 인터랙티브 요소를 더 추가하세요")
        
        # 접근성 개선
        if analysis['accessibility']['score'] < 80:
            recommendations.append("이미지에 대체 텍스트를 추가하고 링크 설명을 개선하세요")
        
        return recommendations
    
    def _calculate_overall_score(self, analysis: Dict[str, Any]) -> float:
        """전체 품질 점수 계산"""
        scores = [
            analysis['readability']['score'],
            analysis['structure']['score'],
            analysis['engagement']['score'],
            analysis['accessibility']['score']
        ]
        return sum(scores) / len(scores)
    
    def improve_content_structure(self, content: str) -> str:
        """콘텐츠 구조 자동 개선"""
        improved_content = content
        
        # 1. 중요 정보를 상단으로 이동
        improved_content = self._move_key_info_to_top(improved_content)
        
        # 2. 섹션 구분 명확화
        improved_content = self._improve_section_structure(improved_content)
        
        # 3. 가독성 향상
        improved_content = self._enhance_readability(improved_content)
        
        return improved_content
    
    def _move_key_info_to_top(self, content: str) -> str:
        """핵심 정보를 상단으로 이동"""
        # 학습 목표나 핵심 개념을 찾아서 상단으로 이동
        key_patterns = [
            r'(학습 목표[:\s]*[^\n]+)',
            r'(핵심 개념[:\s]*[^\n]+)',
            r'(주요 내용[:\s]*[^\n]+)'
        ]
        
        key_info = []
        for pattern in key_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            key_info.extend(matches)
        
        if key_info:
            # 기존 내용에서 핵심 정보 제거
            for info in key_info:
                content = content.replace(info, '')
            
            # 상단에 핵심 정보 추가
            key_section = "## 🎯 핵심 포인트\n\n" + "\n".join(f"- {info}" for info in key_info) + "\n\n"
            content = key_section + content
        
        return content
    
    def _improve_section_structure(self, content: str) -> str:
        """섹션 구조 개선"""
        # 긴 문단을 소제목으로 나누기
        paragraphs = content.split('\n\n')
        improved_paragraphs = []
        
        for i, paragraph in enumerate(paragraphs):
            if len(paragraph) > 500 and not paragraph.startswith('#'):
                # 긴 문단을 두 부분으로 나누고 소제목 추가
                mid_point = len(paragraph) // 2
                sentences = paragraph.split('.')
                
                if len(sentences) > 3:
                    mid_sentence = len(sentences) // 2
                    first_part = '.'.join(sentences[:mid_sentence]) + '.'
                    second_part = '.'.join(sentences[mid_sentence:])
                    
                    improved_paragraphs.append(first_part)
                    improved_paragraphs.append(f"### 📋 세부 내용")
                    improved_paragraphs.append(second_part)
                else:
                    improved_paragraphs.append(paragraph)
            else:
                improved_paragraphs.append(paragraph)
        
        return '\n\n'.join(improved_paragraphs)
    
    def _enhance_readability(self, content: str) -> str:
        """가독성 향상"""
        # 1. 긴 문장 분리
        content = re.sub(r'([.!?])\s*([가-힣A-Za-z])', r'\1\n\2', content)
        
        # 2. 리스트 형태로 변환 가능한 내용 찾기
        content = re.sub(r'(\d+)\.\s*([^.\n]+)', r'- \2', content)
        
        # 3. 강조 표시 추가
        emphasis_words = ['중요', '핵심', '주의', '필수']
        for word in emphasis_words:
            content = re.sub(f'({word})', r'**\1**', content)
        
        return content

# 사용 예제
if __name__ == "__main__":
    agent = ContentQualityAgent()
    
    sample_content = """
    통계학은 데이터를 수집하고 분석하여 의미 있는 정보를 추출하는 학문입니다. 
    이 과정에서 우리는 다양한 통계적 기법을 사용하게 됩니다.
    
    기술통계량은 데이터의 특성을 요약하는 수치들입니다.
    """
    
    # 품질 분석
    analysis = agent.analyze_content_quality(sample_content)
    print("콘텐츠 품질 분석 결과:")
    print(f"전체 점수: {analysis['overall_score']:.1f}")
    print("권장사항:", analysis['recommendations'])
    
    # 콘텐츠 개선
    improved = agent.improve_content_structure(sample_content)
    print("\n개선된 콘텐츠:")
    print(improved)