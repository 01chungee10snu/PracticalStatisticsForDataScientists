## 데이터 및 표본 분포 요약
- **표본 추출**: 단순 임의 추출, 층화 추출 등 다양한 방법 소개.
- **중심 극한 정리**: 표본 평균이 정규 분포에 수렴하는 원리 설명.
- **통계적 추정**: 모수 추정과 신뢰 구간 설정 방법 기술.
- **복원추출과 비복원추출**: 표본을 다시 모집단에 넣는지 여부에 따른 차이를 설명하고, 상황에 맞게 선택하는 방법을 제시합니다.
- **샘플 크기와 정확도**: 샘플 수가 늘어날수록 추정의 분산이 줄어드는 원리를 소개합니다.
- **샘플링 편향 방지**: 실무에서 발생하기 쉬운 편향을 줄이기 위한 설계 전략을 설명합니다.

## 실습 코드 예시
```python
from modules.data_processing import sample_public_dataset
from modules.visualization import plot_iris_example

data = sample_public_dataset(50)
img = plot_iris_example(data)
```


