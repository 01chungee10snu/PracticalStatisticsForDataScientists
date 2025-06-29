## 분류 요약
- **로지스틱 회귀**: 이진 결과 예측을 위한 기본 모델.
- **판별 분석**: LDA/QDA를 활용해 그룹 간 차이를 모델링.
- **나이브 베이즈와 K-최근접 이웃**: 단순하지만 실무에서 널리 쓰이는 방법.
- **모델 평가**: 정확도, 정밀도, 재현율, AUC 등 지표로 성능을 측정.
- **결정 트리와 SVM**: 비선형 분류 문제를 해결하기 위한 대표 알고리즘을 설명합니다.
- **앙상블 분류**: 랜덤 포레스트와 부스팅 계열 모델로 예측력을 높이는 방법을 소개합니다.
- **불균형 데이터 대응**: 재샘플링이나 가중치 조정으로 편향을 완화하는 전략을 다룹니다.

### 핵심 포인트
* 분류 모델은 범주형 결과 예측을 목표로 합니다.
* 모델 평가 지표를 통해 예측 정확도를 정량화합니다.

### 추가 학습 내용
* 다중 클래스 문제에서 원-핫 인코딩 기법을 적용해 봅니다.
* 앙상블 모델의 투표 방식 차이를 실험해 성능을 비교합니다.
* 불균형 데이터셋에서 가중치를 조정한 로지스틱 회귀를 구현합니다.

### 논문 수준 보충
* ROC 곡선 아래 면적(AUC)의 추정치를 신뢰구간과 함께 제시합니다.
* 클래스 불균형 완화를 위한 비용 민감 학습(cost-sensitive learning) 방법을 비교합니다.
* 실험 반복을 통해 분류 모델의 분산을 정량화하고 이를 보고합니다.

### 역사적 배경
* 피셔가 1936년 아이리스 데이터를 이용해 선형 판별 분석을 시연한 것이 현대 분류 기법의 초기 사례입니다.
## 실습 코드 예시
```python
from modules.data_processing import sample_public_dataset, sample_titanic_dataset
from sklearn.ensemble import RandomForestClassifier

df = sample_public_dataset(100)
X = df[['sepal_length', 'sepal_width', 'petal_length', 'petal_width']]
y = df['species']
clf = RandomForestClassifier(n_estimators=50).fit(X, y)
print('훈련 정확도:', clf.score(X, y))

# 타이타닉 생존 예측 간단 실습
tdf = sample_titanic_dataset(200).dropna(subset=['age','fare'])
X_t = tdf[['age', 'fare']]
y_t = tdf['survived']
clf = RandomForestClassifier(n_estimators=50).fit(X_t, y_t)
print('타이타닉 훈련 정확도:', clf.score(X_t, y_t))
```



### 추가 예시
- 실무 데이터를 활용해 핵심 개념을 적용하는 연습을 제안합니다.
더 자세한 통합 요약은 [overview.md](../overview.md)에서 확인할 수 있습니다.

### 연습 문제
1. 랜덤 포레스트가 단일 결정 트리보다 성능이 우수한 이유를 설명하세요.
2. 데이터 불균형 문제가 분류 정확도에 미치는 영향을 예시와 함께 서술하세요.
3. 실습 코드에 적용된 피처 엔지니어링 방식이 모델 성능 향상에 어떻게 기여했는지 분석하세요.

[정답 보기](../answers.md)

[목차로 돌아가기](../overview.md)
