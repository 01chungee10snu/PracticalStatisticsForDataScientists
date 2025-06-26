## 분류 요약
- **로지스틱 회귀**: 이진 결과 예측을 위한 기본 모델.
- **판별 분석**: LDA/QDA를 활용해 그룹 간 차이를 모델링.
- **나이브 베이즈와 K-최근접 이웃**: 단순하지만 실무에서 널리 쓰이는 방법.
- **모델 평가**: 정확도, 정밀도, 재현율, AUC 등 지표로 성능을 측정.
- **결정 트리와 SVM**: 비선형 분류 문제를 해결하기 위한 대표 알고리즘을 설명합니다.
- **앙상블 분류**: 랜덤 포레스트와 부스팅 계열 모델로 예측력을 높이는 방법을 소개합니다.
- **불균형 데이터 대응**: 재샘플링이나 가중치 조정으로 편향을 완화하는 전략을 다룹니다.

## 실습 코드 예시
```python
from modules.data_processing import sample_public_dataset
from modules.visualization import plot_iris_example

data = sample_public_dataset(50)
img = plot_iris_example(data)
```


