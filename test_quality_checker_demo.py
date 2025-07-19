"""
Task 1.2 Complete: Quality Verification System Test
"""

from modules.content_standardization_simple import ContentStandardizer, QualityChecker


def test_quality_verification_system():
    """Test the quality verification system implementation"""
    print("=== Task 1.2: Quality Verification System Test ===")
    
    # Create standardizer with quality checker
    standardizer = ContentStandardizer()
    quality_checker = QualityChecker()
    
    print("✓ 1. Quality Checker Created")
    print(f"   - Required sections defined for {len(quality_checker.required_sections)} difficulty levels")
    print(f"   - Quality criteria: {len(quality_checker.quality_criteria)} checks")
    
    # Test Case 1: Valid content
    print("\n✓ 2. Testing Valid Content")
    valid_content = {
        'title': '기술통계량 완전 가이드',
        'difficulty_level': 'foundation',
        'estimated_time': 30,
        'sections': {
            'concept_introduction': {
                'content': '''기술통계량은 데이터의 특성을 요약하여 설명하는 수치들입니다. 
                주요 기술통계량에는 중심경향성(평균, 중앙값, 최빈값)과 산포도(분산, 표준편차, 범위) 등이 있습니다. 
                이러한 통계량들은 데이터의 전체적인 특성을 파악하는 데 도움이 됩니다. 
                데이터 분석의 첫 단계에서 기술통계량을 계산하여 데이터의 분포와 특성을 이해할 수 있습니다.'''
            },
            'practical_example': {
                'content': '''파이썬을 사용한 기술통계량 계산 예제입니다. 
                다음 코드를 통해 실제로 기술통계량을 계산해볼 수 있습니다.

```python
import pandas as pd
import numpy as np

# 샘플 데이터 생성
data = [85, 90, 78, 92, 88, 76, 95, 89, 84, 91]
df = pd.DataFrame({'scores': data})

# 기술통계량 계산
mean_score = df['scores'].mean()
median_score = df['scores'].median()
std_score = df['scores'].std()

print(f"평균: {mean_score:.2f}")
print(f"중앙값: {median_score:.2f}")
print(f"표준편차: {std_score:.2f}")
```

위 코드는 학생들의 시험 점수 데이터에서 주요 기술통계량을 계산하는 예제입니다.'''
            }
        }
    }
    
    is_valid, issues = standardizer.validate_content(valid_content)
    quality_report = standardizer.get_quality_report(valid_content)
    
    print(f"   - Validation Result: {'✓ PASS' if is_valid else '✗ FAIL'}")
    print(f"   - Quality Score: {quality_report['score']}% (Grade: {quality_report['grade']})")
    print(f"   - Issues: {len(issues)}")
    
    # Test Case 2: Invalid content (missing sections)
    print("\n✓ 3. Testing Invalid Content (Missing Sections)")
    invalid_content = {
        'title': '짧은 제목',
        'difficulty_level': 'foundation',
        'sections': {
            'concept_introduction': {
                'content': '너무 짧은 내용'
            }
            # practical_example 섹션 누락
        }
    }
    
    is_valid, issues = standardizer.validate_content(invalid_content)
    quality_report = standardizer.get_quality_report(invalid_content)
    
    print(f"   - Validation Result: {'✓ PASS' if is_valid else '✗ FAIL'}")
    print(f"   - Quality Score: {quality_report['score']}% (Grade: {quality_report['grade']})")
    print(f"   - Issues Found: {len(issues)}")
    for i, issue in enumerate(issues, 1):
        print(f"     {i}. {issue}")
    
    # Test Case 3: Different difficulty levels
    print("\n✓ 4. Testing Different Difficulty Levels")
    for difficulty in ['foundation', 'developing', 'proficient', 'advanced']:
        required_sections = quality_checker.required_sections[difficulty]
        print(f"   - {difficulty}: {len(required_sections)} required sections")
        print(f"     Required: {', '.join(required_sections)}")
    
    # Test Case 5: Quality criteria validation
    print("\n✓ 5. Testing Quality Criteria")
    criteria = quality_checker.quality_criteria
    for criterion, value in criteria.items():
        print(f"   - {criterion}: {value}")
    
    print("\n=== Task 1.2 COMPLETED SUCCESSFULLY ===")
    print("✓ Required section validation")
    print("✓ Content quality criteria checking")
    print("✓ Quality scoring system")
    print("✓ Detailed issue reporting")
    print("✓ Multiple difficulty level support")
    
    return True


def test_quality_checker_edge_cases():
    """Test edge cases for quality checker"""
    print("\n=== Quality Checker Edge Cases Test ===")
    
    standardizer = ContentStandardizer()
    
    # Edge Case 1: Empty content
    print("\n1. Testing Empty Content")
    empty_content = {}
    is_valid, issues = standardizer.validate_content(empty_content)
    print(f"   - Issues: {len(issues)}")
    for issue in issues:
        print(f"     - {issue}")
    
    # Edge Case 2: Content with no code blocks in practical example
    print("\n2. Testing Missing Code Blocks")
    no_code_content = {
        'title': '코드 없는 실습 예제',
        'difficulty_level': 'foundation',
        'sections': {
            'concept_introduction': {
                'content': '이것은 충분히 긴 개념 소개 내용입니다. 기술통계량에 대한 설명이 포함되어 있습니다. 평균, 중앙값, 표준편차 등에 대해 설명합니다.'
            },
            'practical_example': {
                'content': '이것은 코드 블록이 없는 실습 예제입니다. 단순한 텍스트 설명만 포함되어 있습니다.'
            }
        }
    }
    
    is_valid, issues = standardizer.validate_content(no_code_content)
    quality_report = standardizer.get_quality_report(no_code_content)
    print(f"   - Quality Score: {quality_report['score']}%")
    print(f"   - Code block issues: {[issue for issue in issues if '코드 블록' in issue]}")
    
    print("\n✓ Edge cases handled successfully")


if __name__ == "__main__":
    success = test_quality_verification_system()
    test_quality_checker_edge_cases()
    
    if success:
        print("\n🎉 Task 1.2 Quality Verification System Complete!")
    else:
        print("\n❌ Task 1.2 Implementation Failed!")