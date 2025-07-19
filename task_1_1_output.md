# 기술통계량 이해하기

**난이도:** foundation
**예상 소요 시간:** 25분

## Concept Introduction

기술통계량은 데이터의 특성을 요약하여 설명하는 수치들입니다.
                주요 기술통계량에는 중심경향성(평균, 중앙값, 최빈값)과 산포도(분산, 표준편차, 범위) 등이 있습니다.
                이러한 통계량들은 데이터의 전체적인 특성을 파악하는 데 도움이 됩니다.

## Practical Example

파이썬을 사용한 기술통계량 계산 예제:

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
