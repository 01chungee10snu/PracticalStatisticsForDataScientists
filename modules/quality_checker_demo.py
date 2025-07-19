"""
Quality Checker Demo - Comprehensive Content Validation System
"""

from content_standardization_simple import ContentStandardizer, QualityChecker
import json


def create_sample_contents():
    """Create sample content for testing"""
    return {
        'excellent_content': {
            'title': '파이썬 데이터 분석을 위한 기술통계량 완전 가이드',
            'difficulty_level': 'developing',
            'estimated_time': 45,
            'prerequisites': ['파이썬 기초', '기초 통계학'],
            'sections': {
                'concept_introduction': {
                    'content': '''기술통계량(Descriptive Statistics)은 수집된 데이터의 특성을 요약하고 설명하는 수치적 지표들입니다. 
                    이는 데이터 분석의 첫 번째 단계로, 데이터의 전체적인 패턴과 특성을 파악하는 데 필수적입니다.
                    
                    주요 기술통계량은 크게 두 가지 범주로 나뉩니다:
                    1. 중심경향성(Central Tendency): 평균(Mean), 중앙값(Median), 최빈값(Mode)
                    2. 산포도(Dispersion): 분산(Variance), 표준편차(Standard Deviation), 범위(Range), 사분위수(Quartiles)
                    
                    이러한 통계량들을 통해 데이터의 분포 형태, 중심 위치, 퍼짐 정도를 한눈에 파악할 수 있습니다.'''
                },
                'practical_example': {
                    'content': '''실제 데이터를 사용하여 기술통계량을 계산해보겠습니다. 
                    다음은 학생들의 수학 시험 점수 데이터를 분석하는 예제입니다.

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 샘플 데이터 생성 (학생 100명의 수학 점수)
np.random.seed(42)
scores = np.random.normal(75, 12, 100)  # 평균 75, 표준편차 12
df = pd.DataFrame({'math_scores': scores})

# 기본 기술통계량 계산
print("=== 기술통계량 요약 ===")
print(f"평균 (Mean): {df['math_scores'].mean():.2f}")
print(f"중앙값 (Median): {df['math_scores'].median():.2f}")
print(f"표준편차 (Std Dev): {df['math_scores'].std():.2f}")
print(f"분산 (Variance): {df['math_scores'].var():.2f}")
print(f"최솟값 (Min): {df['math_scores'].min():.2f}")
print(f"최댓값 (Max): {df['math_scores'].max():.2f}")

# 사분위수 계산
Q1 = df['math_scores'].quantile(0.25)
Q3 = df['math_scores'].quantile(0.75)
IQR = Q3 - Q1

print(f"\\n=== 사분위수 정보 ===")
print(f"1사분위수 (Q1): {Q1:.2f}")
print(f"3사분위수 (Q3): {Q3:.2f}")
print(f"사분위수 범위 (IQR): {IQR:.2f}")
```

```python
# 히스토그램으로 분포 시각화
plt.figure(figsize=(10, 6))
plt.hist(df['math_scores'], bins=20, alpha=0.7, color='skyblue', edgecolor='black')
plt.axvline(df['math_scores'].mean(), color='red', linestyle='--', label=f'평균: {df["math_scores"].mean():.1f}')
plt.axvline(df['math_scores'].median(), color='green', linestyle='--', label=f'중앙값: {df["math_scores"].median():.1f}')
plt.xlabel('수학 점수')
plt.ylabel('빈도')
plt.title('학생 수학 점수 분포')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
```

이 예제를 통해 데이터의 중심 위치와 퍼짐 정도를 시각적으로 확인할 수 있습니다.'''
                },
                'common_misconceptions': {
                    'content': '''기술통계량을 해석할 때 자주 발생하는 오해들을 정리했습니다:

- **평균이 항상 대표값이다**: 이상치가 있는 경우 평균은 데이터를 잘못 대표할 수 있습니다. 이때는 중앙값이 더 적절합니다.
- **표준편차가 클수록 나쁘다**: 표준편차의 크기는 상대적입니다. 데이터의 특성과 맥락을 고려해야 합니다.
- **정규분포가 아니면 평균을 사용할 수 없다**: 평균은 모든 분포에서 계산 가능하지만, 해석 시 분포의 형태를 고려해야 합니다.'''
                }
            }
        },
        'poor_content': {
            'title': '통계',
            'difficulty_level': 'foundation',
            'sections': {
                'concept_introduction': {
                    'content': '통계는 중요합니다.'
                }
                # practical_example 누락
            }
        },
        'medium_content': {
            'title': '기초 통계학 개념 정리',
            'difficulty_level': 'foundation',
            'sections': {
                'concept_introduction': {
                    'content': '''통계학은 데이터를 수집하고 분석하여 의미 있는 정보를 추출하는 학문입니다. 
                    기술통계량은 이러한 통계학의 기본 도구로, 데이터의 특성을 숫자로 요약해줍니다.
                    평균, 중앙값, 표준편차 등이 대표적인 기술통계량입니다.'''
                },
                'practical_example': {
                    'content': '''간단한 예제를 살펴보겠습니다.
                    
                    데이터: [1, 2, 3, 4, 5]
                    평균: 3
                    중앙값: 3
                    
                    이처럼 기술통계량을 통해 데이터의 특성을 파악할 수 있습니다.'''
                }
            }
        }
    }


def analyze_content_quality(content_name: str, content_data: dict, standardizer: ContentStandardizer):
    """Analyze and display content quality"""
    print(f"\n{'='*60}")
    print(f"📊 {content_name.upper()} 분석 결과")
    print(f"{'='*60}")
    
    # 기본 정보
    print(f"제목: {content_data.get('title', 'N/A')}")
    print(f"난이도: {content_data.get('difficulty_level', 'N/A')}")
    print(f"섹션 수: {len(content_data.get('sections', {}))}")
    
    # 품질 검증
    is_valid, issues = standardizer.validate_content(content_data)
    quality_report = standardizer.get_quality_report(content_data)
    
    print(f"\n📈 품질 점수: {quality_report['score']}% (등급: {quality_report['grade']})")
    print(f"✅ 검증 결과: {'통과' if is_valid else '실패'}")
    print(f"🔍 발견된 문제: {len(issues)}개")
    
    if issues:
        print("\n❌ 문제점 상세:")
        for i, issue in enumerate(issues, 1):
            print(f"   {i}. {issue}")
    else:
        print("\n✅ 모든 품질 기준을 만족합니다!")
    
    # 섹션별 분석
    sections = content_data.get('sections', {})
    if sections:
        print(f"\n📝 섹션별 분석:")
        for section_name, section_data in sections.items():
            if isinstance(section_data, dict):
                content = section_data.get('content', '')
            else:
                content = str(section_data)
            
            word_count = len(content.split())
            char_count = len(content)
            
            print(f"   • {section_name}:")
            print(f"     - 단어 수: {word_count}")
            print(f"     - 문자 수: {char_count}")
            
            # 코드 블록 검사
            import re
            code_blocks = re.findall(r'```[\w]*\n[\s\S]*?\n```', content)
            if code_blocks:
                print(f"     - 코드 블록: {len(code_blocks)}개")


def main():
    """Main demo function"""
    print("🔍 콘텐츠 품질 검증 시스템 데모")
    print("=" * 80)
    
    # 시스템 초기화
    standardizer = ContentStandardizer()
    quality_checker = QualityChecker()
    
    print(f"✅ 품질 검증 시스템 초기화 완료")
    print(f"   - 지원 난이도: {list(quality_checker.required_sections.keys())}")
    print(f"   - 품질 기준: {len(quality_checker.quality_criteria)}개")
    
    # 샘플 콘텐츠 생성
    sample_contents = create_sample_contents()
    
    # 각 콘텐츠 분석
    for content_name, content_data in sample_contents.items():
        analyze_content_quality(content_name, content_data, standardizer)
    
    # 전체 요약
    print(f"\n{'='*80}")
    print("📊 전체 분석 요약")
    print(f"{'='*80}")
    
    total_contents = len(sample_contents)
    valid_contents = 0
    quality_scores = []
    
    for content_name, content_data in sample_contents.items():
        is_valid, _ = standardizer.validate_content(content_data)
        quality_report = standardizer.get_quality_report(content_data)
        
        if is_valid:
            valid_contents += 1
        quality_scores.append(quality_report['score'])
    
    avg_quality = sum(quality_scores) / len(quality_scores)
    
    print(f"📈 분석된 콘텐츠: {total_contents}개")
    print(f"✅ 품질 기준 통과: {valid_contents}개 ({valid_contents/total_contents*100:.1f}%)")
    print(f"📊 평균 품질 점수: {avg_quality:.1f}%")
    print(f"🏆 최고 점수: {max(quality_scores):.1f}%")
    print(f"⚠️  최저 점수: {min(quality_scores):.1f}%")
    
    print(f"\n🎉 Task 1.2 품질 검증 시스템 데모 완료!")


if __name__ == "__main__":
    main()