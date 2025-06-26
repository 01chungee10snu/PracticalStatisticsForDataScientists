## 통계적 기계 학습 요약
- **교차 검증**: 데이터 분할을 통해 모델의 일반화 성능을 평가.
- **앙상블 기법**: 배깅, 랜덤 포레스트, 부스팅을 활용해 예측력을 향상.
- **하이퍼파라미터 튜닝**: 그리드 서치와 랜덤 서치로 최적 파라미터를 찾음.
- **모델 평가 지표**: 정확도 외에도 F1 스코어, ROC 곡선 등 다양한 지표 사용을 권장합니다.
- **특성 공학과 파이프라인**: 스케일링과 인코딩 절차를 자동화하여 재현성을 높입니다.
- **배치 학습 vs 온라인 학습**: 데이터 수집 방식에 따라 학습 전략을 선택하는 방법을 소개합니다.

## 실습 코드 예시
```python
from modules.data_processing import sample_public_dataset
from modules.visualization import plot_iris_example

data = sample_public_dataset(50)
img = plot_iris_example(data)
```


