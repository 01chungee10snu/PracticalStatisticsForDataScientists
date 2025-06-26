### 2. "David Robertson Saunders - Practical Methods in the Direct Factor Analysis of Psychological Score Matrices (1950)"

이 박사 학위 논문은 심리학적 점수 행렬의 직접 요인 분석을 위한 실용적인 절차에 대해 논의하며, 특히 상관 행렬(R)이 정의되지 않는 경우에 중점을 둡니다. 직접 요인 분석 이론을 통일된 전체로 제시하고, 그 가정이 기존 방법론과 어떻게 다른지 대조합니다.

**서론 (I Introduction)**

*   **문제 진술 (Statement of the problem)**: 논문에서 다루는 연구 문제를 제시합니다.
*   **요약 (Summary)**: 논문의 주요 내용을 간략하게 요약합니다.

**II. 직접 요인 분석 이론 (II The theory of direct factor analysis)**
이 섹션에서는 직접 요인 분석의 이론적 기반을 자세히 설명합니다.

*   **기본 가정 (Fundamental Assumptions)**
    *   **내용 개요:** 요인 분석의 궁극적인 목적과 심리 측정학자들이 행동을 연구하는 접근 방식을 설명합니다.
    *   **세부 내용:**
        *   요인 분석의 궁극적인 목적은 관찰 가능한 행동을 성공적으로 예측하는 것임을 밝힙니다.
        *   Burt의 제안에 따라 방정식이 테일러 급수(Taylor's Series)로 확장되거나 직교 함수(orthogonal functions)의 계열로 확장될 수 있음을 언급합니다.
        *   행렬 표기법 S = AB를 도입하며, 개인의 점수가 "개인 요인(person-factors)"의 곱의 합으로 간주됨을 설명합니다.
        *   행렬 R = S'S로 정의되며, S의 점수가 표준화되면 R이 곱-모멘트 상관 계수(product-moment correlation coefficients)의 행렬이 됨을 설명합니다.
        *   B(요인 부하량)를 추정하는 두 가지 접근 방식, 즉 S를 직접 AB로 분해하거나 R을 B'B로 분해하는 방식이 동일한 B 솔루션을 산출하며, 이는 회전에 대해서만 불변하다는 것을 지적합니다.

*   **점수 행렬의 최적 요인화 (Optimal Factorization of the Score Matrix)**
    *   **내용 개요:** 점수 행렬을 직접 AB로 요인화하는 최적 절차에 대해 논의합니다.
    *   **세부 내용:**
        *   Young의 연구를 인용하며, R의 모든 주요 구성 요소를 포함하는 요인 행렬 B0와 AQBQ = S일 때, A0와 B0가 S에 대한 모든 원하는 솔루션의 핵심이라고 설명합니다.
        *   최적의 H 행렬을 미리 확인하여 다이버전스를 우연 수준으로 줄이는 데 필요한 구성 요소의 수가 달라질 수 있음을 제시합니다.
        *   Lawley의 최대 우도법(maximum likelihood method)에 의해 얻어진 R-요인화의 최대 우도 공통성(communalities)과 S-요인화에서 Dn 요소 간의 관계를 수식으로 표현합니다.
        *   점수 행렬의 요인 분석이 분산 분석(analysis of variance)과 밀접하게 관련되어 있음을 Burt의 예시를 통해 설명합니다. 점수를 원시 형식에서 표준 형식으로 줄이는 것이 분산 분석표에서 주효과(main effect)와 열 효과(column effects)를 빼는 것과 동일함을 관찰합니다.
        *   계산된 통계량(분산 대 자유도 비율)을 F-표 값과 비교하여 상호작용 분산(interaction variance) 추정치의 유의성을 결정하는 방법을 설명합니다.

*   **3-방향 점수 행렬 (Three-way Score Matrices)**
    *   **내용 개요:** 요인이 3-선형 점수 함수를 통해 작동한다고 가정하는 경우를 다룹니다.
    *   **세부 내용:**

## 실습 코드 예시

```python
from modules.data_processing import sample_public_dataset
from modules.visualization import plot_iris_example

data = sample_public_dataset(50)
img = plot_iris_example(data)
```

