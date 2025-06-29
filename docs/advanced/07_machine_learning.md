## 통계적 기계 학습 요약
- **교차 검증**: 데이터 분할을 통해 모델의 일반화 성능을 평가.
- **앙상블 기법**: 배깅, 랜덤 포레스트, 부스팅을 활용해 예측력을 향상.
- **하이퍼파라미터 튜닝**: 그리드 서치와 랜덤 서치로 최적 파라미터를 찾음.
- **모델 평가 지표**: 정확도 외에도 F1 스코어, ROC 곡선 등 다양한 지표 사용을 권장합니다.
- **특성 공학과 파이프라인**: 스케일링과 인코딩 절차를 자동화하여 재현성을 높입니다.
- **배치 학습 vs 온라인 학습**: 데이터 수집 방식에 따라 학습 전략을 선택하는 방법을 소개합니다.

### 핵심 포인트
* 특성 공학과 모델 선택이 기계 학습 성능을 좌우합니다.
* 과적합 방지를 위해 교차 검증과 규제가 중요합니다.

### 대학원 수준 심화
* 커널 기반 학습 이론을 이해하기 위해 서포트 벡터 머신(SVM)의 커널 트릭을 수식으로 설명합니다.
* 딥러닝 모델이 제공하는 표현 학습(representation learning)의 장점과 한계를 논의합니다.
* 모델 복잡도와 과적합 사이의 균형을 살피기 위해 구조적 위험 최소화(Structural Risk Minimization)의 개념을 소개합니다.

### 추가 학습 내용
* 특성 선택 기법의 결과를 해석해 모델 복잡도를 조절합니다.
* 배치 학습과 온라인 학습 간 메모리 사용량 차이를 실험합니다.
* 파이프라인을 활용해 데이터 전처리부터 평가까지 과정을 자동화합니다.

### 논문 수준 보충
* 신뢰 구간을 포함한 교차 검증 결과를 보고하는 절차를 설명합니다.
* 커널 기법을 적용한 서포트 벡터 머신의 하이퍼파라미터 선택 전략을 제시합니다.
* 학습 곡선(learning curve)을 이용해 데이터 크기에 따른 성능 변화를 분석합니다.

### 역사적 배경
* 1957년 프랭크 로젠블랫의 퍼셉트론이 발표되며 기계 학습 연구가 급격히 발전하기 시작했습니다.
## 실습 코드 예시
```python
from modules.data_processing import sample_public_dataset
from sklearn.model_selection import cross_val_score
from sklearn.svm import SVC

df = sample_public_dataset(100)
X = df[['sepal_length', 'sepal_width', 'petal_length', 'petal_width']]
y = df['species']
scores = cross_val_score(SVC(kernel='rbf', gamma='auto'), X, y, cv=5)
print('교차 검증 평균:', scores.mean())
```



### 추가 예시
- 실무 데이터를 활용해 핵심 개념을 적용하는 연습을 제안합니다.
더 자세한 통합 요약은 [overview.md](../overview.md)에서 확인할 수 있습니다.

### 연습 문제
1. 그리드 서치와 랜덤 서치의 장단점을 비교 설명하세요.
2. 교차 검증 과정에서 데이터 누수를 방지하기 위해 주의할 점을 서술하세요.
3. 모델 평가 지표를 선택할 때 고려해야 할 기준을 사례와 함께 제시하세요.

[정답 보기](../answers.md)

[목차로 돌아가기](../overview.md)
