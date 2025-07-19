# 실습 보고서: 기술통계량 실습

## 세션 정보
- **세션 ID:** stats_practice_001
- **학습 개념:** 기술통계량 실습
- **실행 횟수:** 1
- **성공률:** 100.0%
- **학습한 개념:** 기술통계량

## 실행 히스토리

### 실행 1

**코드:**
```python
import numpy as np
import pandas as pd

# 학생들의 시험 점수 데이터
scores = [85, 92, 78, 96, 88, 76, 94, 82, 90, 87, 
          79, 93, 86, 91, 84, 77, 95, 89, 83, 80]

# 기본 통계량 계산
mean_score = np.mean(scores)
median_score = np.median(scores)
std_score = np.std(scores)

print(f"평균 점수: {mean_score:.2f}")
print(f"중앙값: {median_score:.2f}")
print(f"표준편차: {std_score:.2f}")

# DataFrame으로 변환하여 더 자세한 통계 확인
df = pd.DataFrame({'scores': scores})
print("\n상세 통계:")
print(df.describe())
```

**결과:** 성공
**출력:**
```
평균 점수: 86.25
중앙값: 86.50
표준편차: 6.10

상세 통계:
          scores
count  20.000000
mean   86.250000
std     6.256575
min    76.000000
25%    81.500000
50%    86.500000
75%    91.250000
max    96.000000

```

**해석:**
- **기술통계량:** 기술통계량은 데이터의 기본적인 특성을 요약해주는 지표들입니다.
        - 평균(mean): 데이터의 중심값
        - 표준편차(std): 데이터의 흩어진 정도
        - 분위수(quartiles): 데이터의 분포 형태
        
        이러한 통계량들을 통해 데이터의 전반적인 특성을 파악할 수 있습니다.
  - 인사이트: 데이터의 중심 경향성을 평균으로 확인했습니다., 표준편차를 통해 데이터의 산포도를 측정했습니다., describe() 함수로 데이터의 전반적인 통계 요약을 확인했습니다.

---

