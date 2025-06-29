이 장에서는 소규모 심리 척도 데이터를 활용하여 직접 요인 분석의 절차를 단계별로 보여 줍니다. 예제 데이터의 상관 행렬을 계산하고 행렬 분해를 통해 요인 부하량을 추정한 뒤, 각 요인이 설명하는 분산 비율을 해석합니다. 실습을 통해 직접 요인 분석의 핵심 개념을 체감할 수 있습니다.

### 핵심 포인트
* 직접 요인 분석은 상관 행렬을 바로 분해해 요인을 추정합니다.
* 공통성 추정을 위해 최대 우도법이나 주축 요인법을 사용할 수 있습니다.
* 요인 수 결정 시 카이제르 기준과 스크리 플롯을 함께 검토합니다.

### 분석 절차
1. 데이터의 적합성을 확인하기 위해 KMO와 Bartlett 검정을 수행합니다.
2. 상관 행렬을 분해해 초기 요인 부하량을 계산합니다.
3. 필요하면 요인 회전을 적용해 해석의 명료성을 높입니다.

## 실습 코드 예시
```python
from modules.data_processing import sample_public_dataset
from modules.visualization import plot_iris_example

data = sample_public_dataset(50)
img = plot_iris_example(data)
```

### 간단한 분석 코드 예시
```python
import pandas as pd
from sklearn.decomposition import FactorAnalysis

df = sample_public_dataset(100)
fa = FactorAnalysis(n_components=2, random_state=42)
factors = fa.fit_transform(df[['sepal_length', 'sepal_width', 'petal_length', 'petal_width']])
loadings = pd.DataFrame(fa.components_.T, columns=['Factor1', 'Factor2'])
```
`loadings`에는 각 요인이 변수에 미치는 영향을 나타내는 부하량이 저장됩니다. 이를 통해 어떤 변수들이 공통된 요인으로 묶이는지 해석할 수 있습니다.


