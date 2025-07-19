"""
Enhanced Content Standardization System Test
"""

from modules.content_standardization import ContentStandardizer, DifficultyLevel
import json


def test_enhanced_content_standardizer():
    """Enhanced content standardizer test"""
    print("=== Enhanced Content Standardization System Test ===")
    
    # Create standardizer
    standardizer = ContentStandardizer()
    
    # Test content data
    test_content = {
        'title': '기술통계량 이해하기',
        'difficulty_level': 'foundation',
        'estimated_time': 25,
        'prerequisites': ['기초 통계학', '파이썬 기초'],
        'sections': {
            'concept_introduction': {
                'content': '''기술통계량은 데이터의 특성을 요약하여 설명하는 수치들입니다.
                주요 기술통계량에는 중심경향성(평균, 중앙값, 최빈값)과 산포도(분산, 표준편차, 범위) 등이 있습니다.
                이러한 통계량들은 데이터의 전체적인 특성을 파악하는 데 도움이 됩니다.
                데이터 분석의 첫 단계에서 기술통계량을 계산하여 데이터의 분포와 특성을 이해할 수 있습니다.
                올바른 기술통계량 선택은 데이터의 유형과 분포에 따라 달라집니다.'''
            },
            'practical_example': {
                'content': '''파이썬을 사용한 기술통계량 계산 예제:

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
    
    print("1. Original Content:")
    print(f"Title: {test_content['title']}")
    print(f"Sections: {list(test_content['sections'].keys())}")
    
    # Apply standardization (includes template application)
    print("\n2. Applying Standardization (with Template):")
    standardized_content = standardizer.standardize_content(test_content)
    
    print(f"Standardized Title: {standardized_content['title']}")
    print(f"Difficulty Level: {standardized_content['difficulty_level']}")
    print(f"Estimated Time: {standardized_content['estimated_time']} minutes")
    print(f"Total Sections: {len(standardized_content['sections'])}")
    print("All Sections:")
    for section_name in standardized_content['sections'].keys():
        print(f"  - {section_name}")
    
    # Validate content
    print("\n3. Content Validation:")
    is_valid, issues = standardizer.validate_content(test_content)
    print(f"Validation Result: {'Valid' if is_valid else 'Invalid'}")
    if not is_valid:
        print("Issues found:")
        for issue in issues:
            print(f"  - {issue}")
    
    # Generate markdown
    print("\n4. Markdown Generation:")
    markdown = standardizer.generate_markdown(standardized_content)
    print("Generated Markdown (first 500 chars):")
    print(markdown[:500] + "..." if len(markdown) > 500 else markdown)
    
    # Save to file
    with open('test_output_enhanced.md', 'w', encoding='utf-8') as f:
        f.write(markdown)
    print("\nMarkdown saved to: test_output_enhanced.md")
    
    print("\n=== Test Complete ===")


def test_different_difficulty_levels():
    """Test different difficulty levels"""
    print("\n=== Testing Different Difficulty Levels ===")
    
    standardizer = ContentStandardizer()
    
    base_content = {
        'title': '통계 개념 학습',
        'prerequisites': ['수학 기초'],
        'sections': {
            'concept_introduction': {
                'content': '''통계학은 데이터를 수집, 분석, 해석하는 학문입니다.
                현대 사회에서 데이터의 중요성이 증가하면서 통계학의 역할도 커지고 있습니다.
                통계학을 통해 우리는 불확실성 속에서 합리적인 의사결정을 할 수 있습니다.
                기초적인 통계 개념부터 고급 분석 기법까지 다양한 도구들이 있습니다.
                실무에서는 이러한 통계적 사고가 문제 해결의 핵심이 됩니다.'''
            }
        }
    }
    
    for level in DifficultyLevel:
        print(f"\n--- {level.value.upper()} Level ---")
        
        # Create content for this difficulty level
        content = base_content.copy()
        content['difficulty_level'] = level.value
        
        # Apply standardization
        standardized = standardizer.standardize_content(content)
        
        print(f"Estimated Time: {standardized['estimated_time']} minutes")
        print(f"Required Sections: {len(standardized['sections'])}")
        
        # Validate
        is_valid, issues = standardizer.validate_content(content)
        print(f"Validation: {'✓' if is_valid else '✗'} ({len(issues)} issues)")


if __name__ == "__main__":
    test_enhanced_content_standardizer()
    test_different_difficulty_levels()