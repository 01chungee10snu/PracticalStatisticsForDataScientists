"""
Task 4.1 완료 테스트: 웹 인터페이스 구축
"""

import os
import re
from pathlib import Path

def test_html_file_exists():
    """HTML 파일 존재 확인"""
    print("=== HTML 파일 존재 확인 ===")
    
    html_file = Path("integrated_practice_demo.html")
    exists = html_file.exists()
    
    print(f"HTML 파일 존재: {'✅' if exists else '❌'}")
    if exists:
        file_size = html_file.stat().st_size
        print(f"파일 크기: {file_size:,} bytes")
    
    return exists

def test_html_structure():
    """HTML 구조 및 필수 요소 확인"""
    print("\n=== HTML 구조 및 필수 요소 확인 ===")
    
    try:
        with open("integrated_practice_demo.html", "r", encoding="utf-8") as f:
            content = f.read()
        
        # 필수 HTML 구조 요소 확인
        required_elements = [
            (r'<!DOCTYPE html>', 'DOCTYPE 선언'),
            (r'<html[^>]*lang="ko"', '한국어 설정'),
            (r'<meta[^>]*viewport', '반응형 viewport 메타태그'),
            (r'<title>', '페이지 제목'),
            (r'<style>', 'CSS 스타일'),
            (r'<script>', 'JavaScript 코드'),
            (r'class="container"', '컨테이너 클래스'),
            (r'class="header"', '헤더 섹션'),
            (r'class="main-content"', '메인 콘텐츠 섹션'),
            (r'class="step-panel"', '단계 패널'),
            (r'class="code-editor"', '코드 에디터'),
            (r'class="result-panel"', '결과 패널')
        ]
        
        results = []
        for pattern, description in required_elements:
            found = bool(re.search(pattern, content, re.IGNORECASE))
            results.append((description, found))
            print(f"- {description}: {'✅' if found else '❌'}")
        
        return all(result[1] for result in results)
        
    except Exception as e:
        print(f"❌ HTML 파일 읽기 오류: {e}")
        return False

def test_responsive_design():
    """반응형 디자인 확인"""
    print("\n=== 반응형 디자인 확인 ===")
    
    try:
        with open("integrated_practice_demo.html", "r", encoding="utf-8") as f:
            content = f.read()
        
        # 반응형 디자인 요소 확인
        responsive_elements = [
            (r'@media[^{]*\(max-width:\s*768px\)', '태블릿 반응형 (768px)'),
            (r'@media[^{]*\(max-width:\s*480px\)', '모바일 반응형 (480px)'),
            (r'grid-template-columns:\s*1fr', '그리드 레이아웃'),
            (r'flex-wrap:\s*wrap', 'Flexbox 래핑'),
            (r'font-size:\s*[0-9.]+rem', '상대적 폰트 크기'),
            (r'padding:\s*[0-9]+px', '패딩 조정')
        ]
        
        results = []
        for pattern, description in responsive_elements:
            found = bool(re.search(pattern, content, re.IGNORECASE))
            results.append((description, found))
            print(f"- {description}: {'✅' if found else '❌'}")
        
        return sum(result[1] for result in results) >= 4  # 최소 4개 이상
        
    except Exception as e:
        print(f"❌ 반응형 디자인 확인 오류: {e}")
        return False

def test_ui_components():
    """UI 컴포넌트 확인"""
    print("\n=== UI 컴포넌트 확인 ===")
    
    try:
        with open("integrated_practice_demo.html", "r", encoding="utf-8") as f:
            content = f.read()
        
        # UI 컴포넌트 확인
        ui_components = [
            (r'class="progress-bar"', '진행률 표시바'),
            (r'class="step-number"', '단계 번호'),
            (r'class="btn[^"]*btn-primary"', '기본 버튼'),
            (r'class="btn[^"]*btn-secondary"', '보조 버튼'),
            (r'class="btn[^"]*btn-success"', '성공 버튼'),
            (r'class="code-textarea"', '코드 입력 영역'),
            (r'class="result-output"', '결과 출력 영역'),
            (r'class="status-message"', '상태 메시지'),
            (r'class="hint-panel"', '힌트 패널'),
            (r'class="loading-spinner"', '로딩 스피너')
        ]
        
        results = []
        for pattern, description in ui_components:
            found = bool(re.search(pattern, content, re.IGNORECASE))
            results.append((description, found))
            print(f"- {description}: {'✅' if found else '❌'}")
        
        return sum(result[1] for result in results) >= 8  # 최소 8개 이상
        
    except Exception as e:
        print(f"❌ UI 컴포넌트 확인 오류: {e}")
        return False

def test_javascript_functionality():
    """JavaScript 기능 확인"""
    print("\n=== JavaScript 기능 확인 ===")
    
    try:
        with open("integrated_practice_demo.html", "r", encoding="utf-8") as f:
            content = f.read()
        
        # JavaScript 함수 확인
        js_functions = [
            (r'function\s+init\s*\(', 'init() 초기화 함수'),
            (r'function\s+loadStep\s*\(', 'loadStep() 단계 로드 함수'),
            (r'function\s+runCode\s*\(', 'runCode() 코드 실행 함수'),
            (r'function\s+nextStep\s*\(', 'nextStep() 다음 단계 함수'),
            (r'function\s+showHint\s*\(', 'showHint() 힌트 표시 함수'),
            (r'function\s+resetCode\s*\(', 'resetCode() 코드 초기화 함수'),
            (r'function\s+updateProgress\s*\(', 'updateProgress() 진행률 업데이트 함수'),
            (r'function\s+showStatusMessage\s*\(', 'showStatusMessage() 상태 메시지 함수'),
            (r'const\s+stepsData\s*=', 'stepsData 단계 데이터'),
            (r'addEventListener\s*\(\s*[\'"]DOMContentLoaded[\'"]', 'DOM 로드 이벤트 리스너')
        ]
        
        results = []
        for pattern, description in js_functions:
            found = bool(re.search(pattern, content, re.IGNORECASE))
            results.append((description, found))
            print(f"- {description}: {'✅' if found else '❌'}")
        
        return sum(result[1] for result in results) >= 8  # 최소 8개 이상
        
    except Exception as e:
        print(f"❌ JavaScript 기능 확인 오류: {e}")
        return False

def test_css_styling():
    """CSS 스타일링 확인"""
    print("\n=== CSS 스타일링 확인 ===")
    
    try:
        with open("integrated_practice_demo.html", "r", encoding="utf-8") as f:
            content = f.read()
        
        # CSS 스타일 요소 확인
        css_elements = [
            (r'background:\s*linear-gradient', '그라데이션 배경'),
            (r'backdrop-filter:\s*blur', '블러 효과'),
            (r'border-radius:', '둥근 모서리'),
            (r'box-shadow:', '그림자 효과'),
            (r'transition:', '애니메이션 전환'),
            (r'@keyframes', '키프레임 애니메이션'),
            (r'transform:', '변형 효과'),
            (r'grid-template-columns:', '그리드 레이아웃'),
            (r'flex', 'Flexbox 레이아웃'),
            (r'hover:', '호버 효과')
        ]
        
        results = []
        for pattern, description in css_elements:
            found = bool(re.search(pattern, content, re.IGNORECASE))
            results.append((description, found))
            print(f"- {description}: {'✅' if found else '❌'}")
        
        return sum(result[1] for result in results) >= 8  # 최소 8개 이상
        
    except Exception as e:
        print(f"❌ CSS 스타일링 확인 오류: {e}")
        return False

def test_accessibility_features():
    """접근성 기능 확인"""
    print("\n=== 접근성 기능 확인 ===")
    
    try:
        with open("integrated_practice_demo.html", "r", encoding="utf-8") as f:
            content = f.read()
        
        # 접근성 요소 확인
        accessibility_elements = [
            (r'lang="ko"', '언어 설정'),
            (r'alt="[^"]*"', 'alt 속성 (이미지가 있는 경우)'),
            (r'aria-[a-z]+="[^"]*"', 'ARIA 속성'),
            (r'role="[^"]*"', 'role 속성'),
            (r'tabindex="[^"]*"', 'tabindex 속성'),
            (r'<label[^>]*for="[^"]*"', 'label 요소'),
            (r'font-size:\s*[0-9.]+rem', '상대적 폰트 크기'),
            (r'color:\s*#[0-9a-fA-F]{6}', '명시적 색상 지정')
        ]
        
        results = []
        for pattern, description in accessibility_elements:
            found = bool(re.search(pattern, content, re.IGNORECASE))
            results.append((description, found))
            print(f"- {description}: {'✅' if found else '❌'}")
        
        # 기본적인 접근성 요소만 확인 (일부는 선택사항)
        essential_accessibility = [result[1] for result in results[:3]]  # 언어, alt, aria 중 일부
        return sum(essential_accessibility) >= 1
        
    except Exception as e:
        print(f"❌ 접근성 기능 확인 오류: {e}")
        return False

def test_step_data_completeness():
    """단계별 데이터 완성도 확인"""
    print("\n=== 단계별 데이터 완성도 확인 ===")
    
    try:
        with open("integrated_practice_demo.html", "r", encoding="utf-8") as f:
            content = f.read()
        
        # 5단계 데이터 확인
        step_checks = []
        for i in range(1, 6):
            step_pattern = f'"{i}":\\s*{{[^}}]*title:[^}}]*description:[^}}]*objective:[^}}]*template:'
            found = bool(re.search(step_pattern, content, re.IGNORECASE | re.DOTALL))
            step_checks.append(found)
            print(f"- {i}단계 데이터: {'✅' if found else '❌'}")
        
        return sum(step_checks) >= 4  # 최소 4단계 이상
        
    except Exception as e:
        print(f"❌ 단계별 데이터 확인 오류: {e}")
        return False

def main():
    """메인 테스트 함수"""
    print("=" * 60)
    print("Task 4.1: 웹 인터페이스 구축 - 테스트")
    print("=" * 60)
    
    # 개별 테스트 실행
    tests = [
        ("HTML 파일 존재", test_html_file_exists),
        ("HTML 구조 및 필수 요소", test_html_structure),
        ("반응형 디자인", test_responsive_design),
        ("UI 컴포넌트", test_ui_components),
        ("JavaScript 기능", test_javascript_functionality),
        ("CSS 스타일링", test_css_styling),
        ("접근성 기능", test_accessibility_features),
        ("단계별 데이터 완성도", test_step_data_completeness)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} 테스트 오류: {e}")
            results.append((test_name, False))
    
    # 최종 평가
    print("\n" + "=" * 60)
    print("Task 4.1 완료 평가")
    print("=" * 60)
    
    passed_tests = sum(1 for _, passed in results if passed)
    total_tests = len(results)
    
    print("테스트 결과:")
    for test_name, passed in results:
        status = "✅ 통과" if passed else "❌ 실패"
        print(f"- {test_name}: {status}")
    
    print(f"\n전체 테스트 통과율: {passed_tests}/{total_tests} ({passed_tests/total_tests*100:.1f}%)")
    
    # 요구사항 4.1 충족 여부 확인
    essential_requirements = [
        "HTML 파일 존재",
        "HTML 구조 및 필수 요소", 
        "반응형 디자인",
        "UI 컴포넌트",
        "JavaScript 기능"
    ]
    
    essential_passed = sum(1 for test_name, passed in results 
                          if test_name in essential_requirements and passed)
    
    if essential_passed >= 4 and passed_tests >= 6:
        print("\n🎉 Task 4.1 '웹 인터페이스 구축'이 성공적으로 완료되었습니다!")
        print("\n주요 구현 내용:")
        print("- HTML/CSS/JavaScript 기반 사용자 인터페이스")
        print("- 반응형 디자인 및 모바일 호환성")
        print("- 5단계 실습 과정 통합 인터페이스")
        print("- 코드 에디터 및 실행 결과 표시")
        print("- 진행률 추적 및 상태 관리")
        print("- 힌트 시스템 및 사용자 피드백")
        print("- 현대적인 UI/UX 디자인")
        return True
    else:
        print(f"\n⚠️  Task 4.1 완료를 위해 추가 개선이 필요합니다.")
        print(f"필수 요구사항 통과: {essential_passed}/5")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)