# 파이썬 데이터 분석 기초

**난이도:** foundation
**예상 소요 시간:** 30분
**선수 지식:**
- 파이썬 기초
- 수학 기초

## Concept Introduction

데이터 분석은 현대 사회에서 매우 중요한 기술입니다.

파이썬은 데이터 분석을 위한 강력한 도구들을 제공합니다.

pandas, numpy, matplotlib 등의 라이브러리가 있습니다.

## Practical Example

파이썬으로 간단한 데이터 분석을 해보겠습니다:

```python
import pandas as pd
import numpy as np

# 데이터 생성
data = [1, 2, 3, 4, 5]
mean = np.mean(data)
print("평균:", mean)

# 데이터프레임 생성
df = pd.DataFrame({'values': data})
print(df.describe())
```

위 코드는 기본적인 통계를 계산합니다.

## Common Misconceptions

- 데이터 분석은 복잡한 수학만 필요하다

- 파이썬만 알면 데이터 분석을 완벽하게 할 수 있다
- 모든 데이터는 정확하다

## Visual Explanation

데이터 시각화 예제:

![차트 예제](chart.png)

참고 링크: [파이썬 공식 문서](https://www.python.org)
