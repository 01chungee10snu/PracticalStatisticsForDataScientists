## 회귀 및 예측 요약
- **단순 선형 회귀**: 종속 변수와 독립 변수 간 선형 관계 모델링, 잔차 분석.
- **다중 회귀**: 여러 독립 변수가 존재할 때의 모델과 다중공선성 문제.
- **정규화**: 릿지 회귀(L2)와 라쏘(L1)로 과적합을 방지.
- **비선형 회귀와 일반화 모델**: 로지스틱 회귀 등 다양한 모델로 확장.
- **회귀 진단**: 잔차의 정규성, 등분산성, 영향 관측치를 확인하는 방법을 소개합니다.
- **변수 선택**: 단계별 선택법과 규제 기반 방법을 사용해 중요한 변수를 찾는 절차를 설명합니다.
- **예측 오차 측정**: RMSE와 MAE 같은 지표로 모델의 예측 성능을 평가합니다.

## 실습 코드 예시
```python
from modules.data_processing import sample_public_dataset
from modules.visualization import plot_iris_example

data = sample_public_dataset(50)
img = plot_iris_example(data)
```


