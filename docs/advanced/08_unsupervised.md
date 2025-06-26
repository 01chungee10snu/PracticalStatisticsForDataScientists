## 비지도 학습 요약
- **주성분 분석(PCA)**: 고차원 데이터를 저차원으로 축소하고 스크리 플롯을 해석.
- **K-평균 군집화**: 엘보우 방법을 사용해 클러스터 수를 결정.
- **계층적 군집화**: 덴드로그램을 이용해 데이터 구조를 시각화.
- **모델 기반 군집화**: 혼합 모형과 BIC로 적절한 군집 수를 추정.
- **스케일링과 범주형 변수**: 스케일 차이를 조정하고 Gower 거리를 활용.
- **밀도 기반 군집화**: DBSCAN을 통해 임의 모양의 클러스터를 찾는 방법을 소개합니다.
- **차원 축소 시각화**: t-SNE와 UMAP을 사용해 고차원 데이터를 2D 공간에서 시각화합니다.
- **군집 평가**: 실루엣 점수 등 지표로 군집 품질을 정량화하는 방식을 설명합니다.

## 실습 코드 예시
```python
from modules.data_processing import sample_public_dataset
from modules.visualization import plot_iris_example

data = sample_public_dataset(50)
img = plot_iris_example(data)
```


