## 통계적 실험 및 유의성 검정 요약
- **가설 검정**: 귀무가설과 대립가설, p-값 해석, 1종·2종 오류.
- **실험 설계**: 랜덤화, 블록 설계, 교차 실험 등 편향 최소화 전략.
- **효과 크기와 검정력**: 유의성 외에 효과 크기와 검정력을 고려.
- **무작위 할당**: 실험군과 대조군을 무작위로 배정하여 교란 요인을 최소화하는 방법을 설명합니다.
- **다중 비교 문제**: 여러 가설을 동시에 검정할 때 생기는 오류 증가를 보정하는 방법을 다룹니다.
- **A/B 테스트 사례**: 실제 비즈니스 현장에서 활용되는 실험 예시를 제시합니다.

## 실습 코드 예시
```python
from modules.data_processing import sample_public_dataset
from modules.visualization import plot_iris_example

data = sample_public_dataset(50)
img = plot_iris_example(data)
```


