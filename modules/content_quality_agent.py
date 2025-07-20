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
        self.quality_standards = self._initialize_quality_standards()
        self.validation_rules = self._initialize_validation_rules()
    
    def _initialize_quality_standards(self) -> Dict[str, Any]:
        """품질 기준 초기화"""
        return {
            'required_sections': [
                '학습 목표', '핵심 개념', '실습 예제', '요약'
            ],
            'min_readability_score': 70,
            'min_structure_score': 60,
            'min_engagement_score': 50,
            'min_accessibility_score': 80,
            'max_paragraph_length': 300,
            'max_sentence_length': 50,
            'min_examples': 2,
            'required_elements': {
                'headers': 3,
                'code_blocks': 1,
                'lists': 2
            }
        }
    
    def _initialize_validation_rules(self) -> List[Dict[str, Any]]:
        """검증 규칙 초기화"""
        return [
            {
                'rule_id': 'required_sections',
                'description': '필수 섹션 포함 여부 확인',
                'severity': 'error',
                'check_function': self._check_required_sections
            },
            {
                'rule_id': 'readability',
                'description': '가독성 기준 충족 여부',
                'severity': 'warning',
                'check_function': self._check_readability_standards
            },
            {
                'rule_id': 'structure',
                'description': '구조적 완성도 확인',
                'severity': 'warning',
                'check_function': self._check_structure_standards
            },
            {
                'rule_id': 'accessibility',
                'description': '접근성 기준 충족 여부',
                'severity': 'error',
                'check_function': self._check_accessibility_standards
            },
            {
                'rule_id': 'content_completeness',
                'description': '콘텐츠 완성도 확인',
                'severity': 'warning',
                'check_function': self._check_content_completeness
            }
        ]
        
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
    
    def validate_content(self, content: str) -> Dict[str, Any]:
        """콘텐츠 품질 검증"""
        validation_result = {
            'is_valid': True,
            'errors': [],
            'warnings': [],
            'suggestions': [],
            'validation_score': 0,
            'detailed_results': {}
        }
        
        # 각 검증 규칙 실행
        for rule in self.validation_rules:
            try:
                rule_result = rule['check_function'](content)
                validation_result['detailed_results'][rule['rule_id']] = rule_result
                
                if not rule_result['passed']:
                    if rule['severity'] == 'error':
                        validation_result['errors'].extend(rule_result['messages'])
                        validation_result['is_valid'] = False
                    elif rule['severity'] == 'warning':
                        validation_result['warnings'].extend(rule_result['messages'])
                
                # 제안사항 추가
                if 'suggestions' in rule_result:
                    validation_result['suggestions'].extend(rule_result['suggestions'])
                    
            except Exception as e:
                validation_result['errors'].append(f"검증 규칙 '{rule['rule_id']}' 실행 중 오류: {str(e)}")
                validation_result['is_valid'] = False
        
        # 검증 점수 계산
        validation_result['validation_score'] = self._calculate_validation_score(validation_result)
        
        return validation_result
    
    def _check_required_sections(self, content: str) -> Dict[str, Any]:
        """필수 섹션 포함 여부 확인"""
        required_sections = self.quality_standards['required_sections']
        found_sections = []
        missing_sections = []
        
        for section in required_sections:
            # 헤더나 강조된 텍스트로 섹션 찾기
            pattern = rf'(#{1,6}\s*{section}|^\s*\*\*{section}\*\*|\b{section}\b.*:)'
            if re.search(pattern, content, re.IGNORECASE | re.MULTILINE):
                found_sections.append(section)
            else:
                missing_sections.append(section)
        
        passed = len(missing_sections) == 0
        messages = []
        suggestions = []
        
        if not passed:
            messages.append(f"필수 섹션이 누락되었습니다: {', '.join(missing_sections)}")
            suggestions.extend([f"'{section}' 섹션을 추가하세요" for section in missing_sections])
        
        return {
            'passed': passed,
            'messages': messages,
            'suggestions': suggestions,
            'found_sections': found_sections,
            'missing_sections': missing_sections
        }
    
    def _check_readability_standards(self, content: str) -> Dict[str, Any]:
        """가독성 기준 충족 여부 확인"""
        readability_analysis = self._analyze_readability(content)
        min_score = self.quality_standards['min_readability_score']
        
        passed = readability_analysis['score'] >= min_score
        messages = []
        suggestions = []
        
        if not passed:
            messages.append(f"가독성 점수가 기준({min_score})보다 낮습니다: {readability_analysis['score']:.1f}")
            
            if readability_analysis['avg_sentence_length'] > self.quality_standards['max_sentence_length']:
                suggestions.append("문장 길이를 줄여보세요")
            
            if readability_analysis['complex_word_ratio'] > 0.3:
                suggestions.append("복잡한 단어를 간단한 단어로 바꿔보세요")
        
        return {
            'passed': passed,
            'messages': messages,
            'suggestions': suggestions,
            'readability_score': readability_analysis['score']
        }
    
    def _check_structure_standards(self, content: str) -> Dict[str, Any]:
        """구조적 완성도 확인"""
        structure_analysis = self._analyze_structure(content)
        min_score = self.quality_standards['min_structure_score']
        required_elements = self.quality_standards['required_elements']
        
        passed = structure_analysis['score'] >= min_score
        messages = []
        suggestions = []
        
        if not passed:
            messages.append(f"구조 점수가 기준({min_score})보다 낮습니다: {structure_analysis['score']:.1f}")
        
        # 필수 요소 확인
        if structure_analysis['header_count'] < required_elements['headers']:
            suggestions.append(f"헤더를 더 추가하세요 (현재: {structure_analysis['header_count']}, 필요: {required_elements['headers']})")
        
        if structure_analysis['code_block_count'] < required_elements['code_blocks']:
            suggestions.append(f"코드 블록을 추가하세요 (현재: {structure_analysis['code_block_count']}, 필요: {required_elements['code_blocks']})")
        
        if structure_analysis['list_count'] < required_elements['lists']:
            suggestions.append(f"리스트를 더 추가하세요 (현재: {structure_analysis['list_count']}, 필요: {required_elements['lists']})")
        
        return {
            'passed': passed,
            'messages': messages,
            'suggestions': suggestions,
            'structure_score': structure_analysis['score']
        }
    
    def _check_accessibility_standards(self, content: str) -> Dict[str, Any]:
        """접근성 기준 충족 여부 확인"""
        accessibility_analysis = self._analyze_accessibility(content)
        min_score = self.quality_standards['min_accessibility_score']
        
        passed = accessibility_analysis['score'] >= min_score
        messages = []
        suggestions = []
        
        if not passed:
            messages.append(f"접근성 점수가 기준({min_score})보다 낮습니다: {accessibility_analysis['score']:.1f}")
            
            if accessibility_analysis['image_alt_ratio'] < 0.8:
                suggestions.append("이미지에 대체 텍스트(alt text)를 추가하세요")
            
            if accessibility_analysis['descriptive_link_ratio'] < 0.7:
                suggestions.append("링크에 설명적인 텍스트를 사용하세요")
            
            if accessibility_analysis['color_dependency_issues'] > 0:
                suggestions.append("색상에만 의존하지 말고 추가적인 시각적 단서를 제공하세요")
        
        return {
            'passed': passed,
            'messages': messages,
            'suggestions': suggestions,
            'accessibility_score': accessibility_analysis['score']
        }
    
    def _check_content_completeness(self, content: str) -> Dict[str, Any]:
        """콘텐츠 완성도 확인"""
        min_examples = self.quality_standards['min_examples']
        max_paragraph_length = self.quality_standards['max_paragraph_length']
        
        # 예제 개수 확인
        examples = re.findall(r'예제|example', content, re.IGNORECASE)
        
        # 긴 문단 확인
        paragraphs = content.split('\n\n')
        long_paragraphs = [p for p in paragraphs if len(p) > max_paragraph_length and not p.startswith('#')]
        
        # 빈 섹션 확인
        empty_sections = re.findall(r'#{1,6}\s+[^\n]+\n\s*\n\s*#{1,6}', content)
        
        passed = True
        messages = []
        suggestions = []
        
        if len(examples) < min_examples:
            passed = False
            messages.append(f"예제가 부족합니다 (현재: {len(examples)}, 필요: {min_examples})")
            suggestions.append("실습 예제를 더 추가하세요")
        
        if long_paragraphs:
            messages.append(f"너무 긴 문단이 {len(long_paragraphs)}개 있습니다")
            suggestions.append("긴 문단을 여러 개의 짧은 문단으로 나누세요")
        
        if empty_sections:
            passed = False
            messages.append(f"내용이 없는 섹션이 {len(empty_sections)}개 있습니다")
            suggestions.append("모든 섹션에 적절한 내용을 추가하세요")
        
        return {
            'passed': passed,
            'messages': messages,
            'suggestions': suggestions,
            'example_count': len(examples),
            'long_paragraph_count': len(long_paragraphs),
            'empty_section_count': len(empty_sections)
        }
    
    def _calculate_validation_score(self, validation_result: Dict[str, Any]) -> float:
        """검증 점수 계산"""
        total_rules = len(self.validation_rules)
        passed_rules = 0
        
        for rule_result in validation_result['detailed_results'].values():
            if rule_result['passed']:
                passed_rules += 1
        
        # 기본 점수 (통과한 규칙 비율)
        base_score = (passed_rules / total_rules) * 100
        
        # 오류와 경고에 따른 점수 차감
        error_penalty = len(validation_result['errors']) * 10
        warning_penalty = len(validation_result['warnings']) * 5
        
        final_score = max(0, base_score - error_penalty - warning_penalty)
        
        return final_score
    
    def generate_quality_report(self, content: str) -> Dict[str, Any]:
        """종합 품질 보고서 생성"""
        # 품질 분석
        quality_analysis = self.analyze_content_quality(content)
        
        # 품질 검증
        validation_result = self.validate_content(content)
        
        # 종합 보고서
        report = {
            'timestamp': datetime.now().isoformat(),
            'content_length': len(content),
            'quality_analysis': quality_analysis,
            'validation_result': validation_result,
            'overall_assessment': self._generate_overall_assessment(quality_analysis, validation_result),
            'improvement_plan': self._generate_improvement_plan(quality_analysis, validation_result)
        }
        
        return report
    
    def _generate_overall_assessment(self, quality_analysis: Dict[str, Any], 
                                   validation_result: Dict[str, Any]) -> Dict[str, Any]:
        """전체 평가 생성"""
        overall_score = (quality_analysis['overall_score'] + validation_result['validation_score']) / 2
        
        if overall_score >= 90:
            grade = 'A'
            status = 'excellent'
        elif overall_score >= 80:
            grade = 'B'
            status = 'good'
        elif overall_score >= 70:
            grade = 'C'
            status = 'satisfactory'
        elif overall_score >= 60:
            grade = 'D'
            status = 'needs_improvement'
        else:
            grade = 'F'
            status = 'requires_major_revision'
        
        return {
            'overall_score': overall_score,
            'grade': grade,
            'status': status,
            'is_ready_for_publication': validation_result['is_valid'] and overall_score >= 70
        }
    
    def _generate_improvement_plan(self, quality_analysis: Dict[str, Any], 
                                 validation_result: Dict[str, Any]) -> List[Dict[str, Any]]:
        """개선 계획 생성"""
        improvement_tasks = []
        
        # 검증 오류 해결 (최우선)
        for error in validation_result['errors']:
            improvement_tasks.append({
                'priority': 'high',
                'category': 'validation_error',
                'description': error,
                'estimated_time': 15
            })
        
        # 품질 개선 권장사항
        for recommendation in quality_analysis['recommendations']:
            improvement_tasks.append({
                'priority': 'medium',
                'category': 'quality_improvement',
                'description': recommendation,
                'estimated_time': 10
            })
        
        # 검증 제안사항
        for suggestion in validation_result['suggestions']:
            improvement_tasks.append({
                'priority': 'low',
                'category': 'enhancement',
                'description': suggestion,
                'estimated_time': 5
            })
        
        # 우선순위별 정렬
        priority_order = {'high': 1, 'medium': 2, 'low': 3}
        improvement_tasks.sort(key=lambda x: priority_order[x['priority']])
        
        return improvement_tasks

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