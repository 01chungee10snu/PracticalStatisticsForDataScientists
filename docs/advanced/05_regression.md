## 회귀 및 예측 요약
- **단순 선형 회귀**: 종속 변수와 독립 변수 간 선형 관계 모델링, 잔차 분석.
- **다중 회귀**: 여러 독립 변수가 존재할 때의 모델과 다중공선성 문제.
- **정규화**: 릿지 회귀(L2)와 라쏘(L1)로 과적합을 방지.
- **비선형 회귀와 일반화 모델**: 로지스틱 회귀 등 다양한 모델로 확장.
- **회귀 진단**: 잔차의 정규성, 등분산성, 영향 관측치를 확인하는 방법을 소개합니다.
- **변수 선택**: 단계별 선택법과 규제 기반 방법을 사용해 중요한 변수를 찾는 절차를 설명합니다.
- **예측 오차 측정**: RMSE와 MAE 같은 지표로 모델의 예측 성능을 평가합니다.

### 핵심 포인트
* 회귀 분석은 변수 간 관계 모델링과 예측에 활용됩니다.
* 정규화와 변수 선택은 과적합을 방지하고 해석력을 높입니다.

### 대학원 수준 심화
* 정규화 경로(regularization path)를 추적하여 모델 계수의 변화를 시각화합니다.
* 일반화 가법 모형(GAM)을 사용해 비선형 관계를 유연하게 포착하는 방법을 설명합니다.
* 교차 검증을 활용한 하이퍼파라미터 최적화 과정을 체계적으로 기술합니다.

### 추가 학습 내용
* 상호작용 항(term)을 포함해 모델이 복잡해질 때 계수 해석을 연습합니다.
* 잔차 플롯을 이용해 비선형 패턴을 진단하는 방법을 실습합니다.
* 스플라인(spline)이나 다항식 변환을 사용해 예측 성능 변화를 비교합니다.

* 앙상블 기반 회귀(랜덤 포레스트, 그래디언트 부스팅)와 전통적 선형 모델 결과를 비교합니다.
* 부트스트랩을 통한 신뢰구간 추정으로 예측 불확실성을 정량화합니다.

### 단계별 실습 절차
1. 데이터 분할 전 샘플의 균형 여부를 확인하고 필요하면 층화 추출을 적용합니다.
2. 훈련 세트에서 교차 검증을 실시해 모델 복잡도와 규제 강도를 조정합니다.
3. 검증 결과가 안정되면 전체 훈련 데이터를 사용해 최종 모델을 학습합니다.
4. 테스트 세트로 예측력을 평가하고, 잔차 분석을 통해 개선점을 찾습니다.
### 논문 수준 보충

* 회귀 모형의 가정 위반 시 사용하는 진단 통계량을 수식과 함께 정리합니다.
* 변수 선택 절차를 단계별로 기술하며 AIC와 BIC 비교를 추가합니다.
* 연속형 변수의 스케일 차이를 줄이기 위한 정규화 기법을 표로 정리합니다.

### 역사적 배경
* 회귀 분석이라는 용어는 프랜시스 갈튼이 키 유전 연구를 하며 19세기 후반에 처음 사용한 것으로 알려져 있습니다.
## 실습 코드 예시
```python
from modules.data_processing import sample_public_dataset
from sklearn.linear_model import LinearRegression

df = sample_public_dataset(80)
X = df[['sepal_length']]
y = df['petal_length']
model = LinearRegression().fit(X, y)
print('회귀 계수:', model.coef_[0])
```



### 추가 예시
- 실무 데이터를 활용해 핵심 개념을 적용하는 연습을 제안합니다.
더 자세한 통합 요약은 [overview.md](../overview.md)에서 확인할 수 있습니다.

### 연습 문제
1. 다중공선성 문제가 발생했을 때 릿지 회귀와 라쏘 회귀의 차이를 설명하세요.
2. 회귀 진단 과정에서 잔차 분석이 왜 중요한지 구체적으로 서술하세요.
3. 교차 검증을 활용한 하이퍼파라미터 조정 절차를 간단히 정리하세요.

[정답 보기](../answers.md)

[목차로 돌아가기](../overview.md)
