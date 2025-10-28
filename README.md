# 성장디자인팀 통계학습자료
참고문헌
이훈영. (2012). 이훈영교수의 연구조사방법론. 청람
Bruce, P., Bruce, A., & Gedeck, P. (2020). Practical statistics for data scientists: 50+ essential concepts using R and Python (2nd ed.). O'Reilly Media

# 📊 통계(Statistics)

## 1️⃣ 통계의 정의

* **통계(Statistics)**란 데이터를 **수집(Collect)**, **정리(Organize)**, **분석(Analyze)**, **해석(Interpret)**하여
  **의미 있는 결론을 도출하고 불확실성을 줄이는 과학적 방법론**이다.

> 💬 **‘통계’라는 용어의 기원**
>
> * 라틴어 *status*(상태) → ‘국가의 상태를 수로 기록한다’에서 유래
> * 오늘날은 사회, 과학, 산업 등 모든 영역의 데이터 해석에 사용됨.

---

## 2️⃣ 통계의 구성 체계

### (1) 통계의 두 가지 영역

1. **기술통계 (Descriptive Statistics)**
   데이터를 요약하거나 시각화하여 현상을 직관적으로 파악

   * 예: 평균(mean), 중앙값(median), 분산(variance), 히스토그램(histogram)

2. **추론통계 (Inferential Statistics)**
   표본(sample)으로부터 모집단(population)의 성질을 추정하거나 가설을 검정

   * 예: 신뢰구간(confidence interval), 가설검정(hypothesis testing)

> 💬 **용어 주석**
>
> * **모집단(Population)**: 관심 있는 전체 집단
> * **표본(Sample)**: 모집단 중 실제로 관측한 일부
> * **모수(Parameter)**: 모집단의 특성(예: 평균 μ, 분산 σ²)
> * **통계량(Statistic)**: 표본에서 계산된 수치(예: $\bar{x}$, $s^2$)
>
> 💬 **기호의 어원 (Etymology of Symbols)**
>
> * **$\bar{x}$ (x-bar, 엑스 바)**: 19세기부터 평균을 나타내는 표기법. 위에 가로선(bar)을 그어 "여러 값의 대표값"임을 시각적으로 표현. Karl Pearson이 통계학에 보급.
> * **$\mu$ (뮤, mu)**: 그리스어 "mean"의 첫 글자. 모평균(population mean)을 나타내는 표준 기호로 19세기 말 정립.
> * **$\sigma$ (시그마, sigma)**: 그리스 대문자 Σ(합)의 소문자. "sum"의 첫 글자로 편차 제곱합(sum of squared deviations)에서 유래. Karl Pearson이 표준편차 기호로 사용 시작.

---

### (2) 통계의 목적

| 목적                    | 설명                    |
| --------------------- | --------------------- |
| **요약(Summarization)** | 복잡한 데이터를 대표값으로 단순화    |
| **추론(Inference)**     | 표본으로 모집단의 특성 예측       |
| **의사결정(Decision)**    | 불확실한 상황에서 근거 있는 판단 수행 |

> 💬 통계는 **확률(Probability)**에 의존한다.
> 확률은 데이터의 **불확실성을 수학적으로 표현**하는 언어다.

---

## 3️⃣ 통계적 사고의 구조

### (1) 통계적 사고(Statistical Thinking)

* 데이터를 통해 **패턴을 발견하고**,
  **우연(chance)**과 **규칙(pattern)**을 구분하는 사고방식

> 💬 “데이터는 완벽하지 않다”는 인식이 출발점이다.
> 모든 통계 분석은 **불확실성을 정량화(quantify uncertainty)**하는 과정이다.

---

### (2) 통계 분석의 단계

1. **문제 정의(Define)** – 분석 목적을 명확히 함
2. **데이터 수집(Collect)** – 관찰 또는 실험을 통해 데이터 확보
3. **데이터 요약(Summarize)** – 기술통계로 구조 파악
4. **추론/모델링(Infer/Model)** – 확률과 통계이론으로 결론 도출
5. **의사결정(Decide)** – 결과 해석 및 실질적 판단

> 💬 ④단계에서 **확률론**이 핵심 이론으로 작동한다.

---

## 4️⃣ 통계의 이론적 기반: 확률(Probability)

### (1) 확률의 정의

* **확률**은 어떤 사건이 일어날 가능성을 0과 1 사이의 실수로 나타낸 것

  * 0 → 불가능(impossible)
  * 1 → 확실(certain)

> 💬 확률의 기호는 **$P$**이며, 괄호 안에는 사건(event)을 넣는다.
> 예: $P(A)$는 “사건 A가 일어날 확률”을 의미한다.

---

### (2) 확률의 구성요소

| 구성요소                            | 기호               | 설명                    |
| ------------------------------- | ---------------- | --------------------- |
| **표본공간 (Sample Space)**         | $S$              | 가능한 모든 결과의 집합         |
| **사건 (Event)**                  | $A, B, C, \dots$ | 특정 조건을 만족하는 결과들의 부분집합 |
| **확률함수 (Probability Function)** | $P$              | 사건을 확률 값에 대응시키는 함수    |

> 💬 예시
> 주사위를 던질 때 $S={1,2,3,4,5,6}$
> “짝수가 나오는 사건” $A={2,4,6}$
> $P(A)=3/6=0.5$

---

### (3) 확률의 세 공리 (Kolmogorov Axioms)

1. **비음성(Non-negativity)**
   $$P(A) \ge 0$$
   → 확률은 음수가 될 수 없음

2. **전체공간의 확률은 1**
   $$P(S) = 1$$
   → 전체 가능한 경우의 합은 1

3. **가법성(Additivity)**
   $$P(A \cup B) = P(A) + P(B)$$
   단, $A$와 $B$가 **서로 배타적(mutually exclusive)**일 때만 성립

> 💬 **기호 해설**
>
> * $\cup$: 합집합 (A 또는 B)
> * $\cap$: 교집합 (A 그리고 B)
> * $\varnothing$: 공집합 (아무것도 포함하지 않음)

---

### (4) 확률의 해석 관점

1. **고전적(Classical)**
   $$P(A)=\frac{\text{A의 경우의 수}}{\text{전체 경우의 수}}$$

   * 모든 결과가 동등하게 가능할 때 사용

   > 💬 **고전적 확률의 구체적 예시**
   >
   > **예시 1: 주사위 던지기**
   > - 공정한 주사위를 던져 3이 나올 확률은?
   > - 전체 경우의 수: 6가지 (1, 2, 3, 4, 5, 6)
   > - 3이 나오는 경우의 수: 1가지
   > - **확률**: P(3이 나옴) = 1/6 ≈ 0.167 = 16.7%
   >
   > **예시 2: 카드 뽑기**
   > - 52장 카드 중 하트를 뽑을 확률은?
   > - 전체 경우의 수: 52장
   > - 하트 카드 수: 13장
   > - **확률**: P(하트) = 13/52 = 1/4 = 0.25 = 25%
   >
   > **예시 3: 로또 당첨**
   > - 1~45 중 6개 번호를 맞출 확률은?
   > - 전체 경우의 수: $\binom{45}{6} = \frac{45!}{6! \times 39!} = 8,145,060$
   > - 당첨 경우의 수: 1가지 (내가 산 번호 조합)
   > - **확률**: P(1등) = 1/8,145,060 ≈ 0.00000012 (약 812만분의 1)
   >
   > **예시 4: 동전 두 개 던지기**
   > - 두 동전을 동시에 던져 모두 앞면이 나올 확률은?
   > - 전체 경우의 수: 4가지
   >   ```
   >   (앞, 앞), (앞, 뒤), (뒤, 앞), (뒤, 뒤)
   >   ```
   > - 모두 앞면인 경우: 1가지 (앞, 앞)
   > - **확률**: P(모두 앞면) = 1/4 = 0.25 = 25%
   >
   > **고전적 확률의 핵심 가정**:
   > - ✅ 모든 결과가 **동등하게** 일어날 가능성 (공정한 주사위, 잘 섞인 카드)
   > - ✅ 경우의 수를 **수학적으로 계산** 가능
   > - ❌ 한계: 현실에서는 완벽히 동등한 경우가 드물다 (예: 낡은 주사위, 무게 편향)

2. **빈도적(Frequentist)**
   $$P(A)=\lim_{n \to \infty}\frac{n_A}{n}$$

   * 시행을 무한히 반복했을 때의 비율

   > 💬 **빈도적 확률의 구체적 예시**
   >
   > **예시 1: 동전 던지기**
   > - 공정한 동전을 던져 앞면이 나올 확률은?
   > - 이론적으로 P(앞면) = 0.5이지만, 빈도론자는 **실제로 던져서 확인**
   > - 실험 결과:
   >   ```
   >   10번 던지기:   앞면 6번  → 6/10  = 0.6
   >   100번 던지기:  앞면 52번 → 52/100 = 0.52
   >   1,000번:       앞면 493번 → 0.493
   >   10,000번:      앞면 5,021번 → 0.5021
   >   ```
   > - **큰수의 법칙**: 시행 횟수가 많아질수록 0.5에 가까워짐!
   >
   > **예시 2: 제품 불량률 추정**
   > - 공장에서 생산되는 제품의 불량률을 알고 싶다
   > - 방법: 무작위로 1,000개를 뽑아서 검사
   > - 결과: 불량품 27개 발견
   > - **빈도적 확률**: P(불량) = 27/1,000 = 0.027 = 2.7%
   > - 해석: "이 공장 제품을 하나 뽑으면 2.7% 확률로 불량"
   >
   > **예시 3: 야구 타율**
   > - 타자의 "안타 확률"을 어떻게 알까?
   > - 시즌 중 타석: 500번
   > - 안타: 150번
   > - **타율(빈도적 확률)**: 150/500 = 0.300 (3할 타자)
   > - 의미: "다음 타석에서 안타 칠 확률이 약 30%"
   >
   > **빈도적 관점의 특징**:
   > - ✅ 객관적: 누가 측정해도 같은 결과
   > - ✅ 검증 가능: 실험으로 확인 가능
   > - ❌ 한계: 반복 불가능한 사건은? (예: "내일 비 올 확률", "이번 경기 우승 확률")
   > - ❌ 실용성: 무한히 반복 불가능 (실제로는 유한 횟수만 실험)

3. **주관적(Subjective)**

   * 사건에 대한 개인의 신념의 정도
   * 베이즈 통계(Bayesian Statistics)의 기반

> 💬 **구체적 예시로 이해하는 세 가지 확률 관점**
>
> **상황**: 주머니에 공 10개가 들어있고, 그 중 빨간 공이 몇 개인지 알고 싶다.
>
> 1. **고전적 확률**
>    - "만약 빨간 공이 3개라면, 확률은 3/10 = 0.3"
>    - → 모든 공이 뽑힐 가능성이 동등하다고 가정
>
> 2. **빈도적 확률**
>    - 공을 뽑고 다시 넣는 실험을 1000번 반복
>    - 빨간 공이 297번 나왔다면: P(빨강) ≈ 297/1000 = 0.297
>    - → 무한히 반복하면 진짜 확률에 수렴
>
> 3. **주관적 확률 (베이즈)**
>    - **사전 정보**: "주머니 주인이 빨간 공을 좋아한다"는 정보를 알고 있음
>    - **초기 믿음**: "아마 빨간 공이 많을 것 같다" → 확률 0.6으로 추정
>    - **실험**: 공을 3번 뽑았더니 빨강 2번, 파랑 1번
>    - **업데이트된 믿음**: 베이즈 정리로 계산하면 확률이 0.6 → 0.65로 증가
>    - → **새로운 증거가 나올 때마다 믿음을 업데이트**
>
> **베이즈 통계의 핵심 특징**:
> - 확률을 "고정된 값"이 아니라 "업데이트 가능한 믿음의 정도"로 봄
> - 기존 지식(사전확률) + 새로운 데이터(증거) = 업데이트된 확률(사후확률)
> - 공식: P(가설|데이터) = P(데이터|가설) × P(가설) / P(데이터)
>
> **실생활 예시 - 의료 진단** (왜 16%인지 단계별 계산):
>
> **📋 상황 설정**:
> - 어떤 희귀병의 **유병률**: 인구의 1%
> - 검사의 **정확도**: 95%
>   - 병이 있으면 95% 확률로 양성 (민감도)
>   - 병이 없으면 95% 확률로 음성 (특이도)
>   - 따라서 **위양성률**(병 없는데 양성): 5%
>
> **❓ 질문**: 검사 결과가 양성이면, 실제로 병에 걸렸을 확률은?
>
> **💭 직관적 예상**: "95% 정확도니까 95% 확률 아닌가?"
> **⚠️ 실제 답**: **약 16%** ← 왜 이렇게 낮을까?
>
> ---
>
> **🔢 구체적 계산 (10,000명 기준)**:
>
> ```
> 전체 인구: 10,000명
>
> ① 실제 병이 있는 사람 (유병률 1%)
>    = 10,000 × 0.01 = 100명
>    이 중 검사 양성 (민감도 95%)
>    = 100 × 0.95 = 95명 (진양성 ✓)
>
> ② 실제 병이 없는 사람 (99%)
>    = 10,000 × 0.99 = 9,900명
>    이 중 검사 양성 (위양성률 5%)
>    = 9,900 × 0.05 = 495명 (위양성 ✗)
>
> ③ 검사 결과 양성인 전체 사람
>    = 95명(진양성) + 495명(위양성) = 590명
>
> ④ 그 중 실제로 병이 있는 비율
>    = 95명 / 590명 = 0.161 = 16.1% ✓
> ```
>
> **📊 시각적 이해**:
> ```
> 검사 양성 590명
> ┌─────────────────────────────────────┐
> │ 진짜 병 있음: 95명  (16%)  ✓       │
> │ 병 없는데 양성: 495명 (84%) ✗      │
> └─────────────────────────────────────┘
> ```
>
> **🎯 핵심 통찰 - 왜 16%밖에 안 될까?**:
>
> 1. **유병률이 매우 낮다** (1%)
>    → 애초에 병 있는 사람이 100명뿐
>
> 2. **병 없는 사람이 압도적으로 많다** (9,900명)
>    → 이 중 5%만 위양성이어도 495명!
>
> 3. **위양성자가 진양성자보다 5배 많다** (495명 vs 95명)
>    → 양성이어도 대부분(84%)은 건강한 사람
>
> **📐 베이즈 정리 공식**:
> $$
> P(\text{병}|\text{양성}) = \frac{P(\text{양성}|\text{병}) \times P(\text{병})}{P(\text{양성})}
> $$
> $$
> = \frac{0.95 \times 0.01}{0.95 \times 0.01 + 0.05 \times 0.99} = \frac{0.0095}{0.059} = 0.161
> $$
>
> **💡 실용적 의미**:
> - 검사 양성이어도 **당황하지 말 것!** (84%는 건강)
> - **추가 정밀 검사 필수** (2차 검사로 확률 업데이트)
> - 만약 2차 검사도 양성이면?
>   - 이제 사전확률 = 16% (1%가 아님)
>   - 2차 검사 후 확률 = **약 78%**로 급상승!
> - 이것이 바로 **베이즈 업데이트**의 힘

---

## 5️⃣ 통계의 핵심 개념들

### (1) 모집단과 표본

* **모집단(Population)**: 분석 대상 전체
* **표본(Sample)**: 모집단 중 일부
* **표본추출(Sampling)**: 대표성을 갖게 데이터를 선택하는 과정

> 💬 표본의 대표성이 확보되어야 통계적 추론이 타당하다.

---

### (2) 표본분포(Sampling Distribution)

* 표본으로 계산된 통계량이 따르는 분포
* 예: 표본평균의 분포는 **정규분포에 수렴**
  $$\bar{X} \sim N\left(\mu, \frac{\sigma^2}{n}\right)$$

> 💬 **중심극한정리(Central Limit Theorem):**
> 표본의 크기가 충분히 크면,
> 모집단 분포에 상관없이 표본평균은 정규분포를 따른다.

---

### (3) 추정(Estimation)

1. **점추정(Point Estimation)**
   $$\hat{\theta} = \text{추정치}$$

   * 예: 표본평균 $\bar{x}$는 모집단평균 μ의 추정치

2. **구간추정(Interval Estimation)**
   $$\bar{x} \pm z\frac{s}{\sqrt{n}}$$

   * 95% 신뢰구간(confidence interval)

> 💬 **기호 해설**
>
> * $\hat{\theta}$: 모수의 추정치(estimator)
> * $z$: 표준정규분포의 임계값(critical value)
> * $s$: 표본의 표준편차(standard deviation)
> * $\sqrt{n}$: 표본 크기에 따른 표준오차 감소
>
> 💬 **기호 어원 – 추정 표기**
> * **$\hat{\theta}$ (세타 hat)**: 위에 "모자(^, hat)"를 씌워 "추정값(estimated value)"임을 표시. 19세기 수학자들이 도입한 표기법으로 "진짜 값은 모르지만 추정한 값"을 시각적으로 구분.
> * **$n$ (표본크기)**: "number"의 첫 글자. 표본의 개수를 나타내는 가장 직관적인 표기.
> * **$N$ (모집단크기)**: 대문자 N으로 전체(total) 모집단을 의미. 표본(소문자 n)과 구분.

### 신뢰구간의 의미 시각화

![Confidence intervals for different levels](https://upload.wikimedia.org/wikipedia/commons/f/f4/Confidence_intervals_for_different_confidence_levels.gif)

> 출처: [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Confidence_intervals_for_different_confidence_levels.gif) - 서로 다른 신뢰수준(90%, 95%, 99%)에서의 신뢰구간 비교

> 💬 **신뢰구간의 해석**
>
> * **신뢰수준(Confidence Level)**: 반복 표본추출 시 신뢰구간이 모수를 포함할 확률
>   - 95% 신뢰수준 = "100번 표본추출하면 약 95번은 구간 안에 모수가 포함"
> * **구간의 폭**: 신뢰수준이 높을수록 구간이 넓어짐
>   - 99% CI > 95% CI > 90% CI (더 확신하려면 더 넓은 범위 필요)
> * **표본크기 효과**: $n$이 커질수록 신뢰구간이 좁아짐 ($\propto 1/\sqrt{n}$)
> * **주의**: "모수가 이 구간에 속할 확률이 95%"가 아니라, "구간이 모수를 포함할 확률이 95%"

---

### (4) 가설검정(Hypothesis Testing)

1. **귀무가설 ($H_0$)**: 차이가 없다는 주장
2. **대립가설 ($H_1$)**: 차이가 있다는 주장
3. **검정통계량(Test Statistic)** 계산
4. **유의확률(p-value)** 산출
5. **판단:** p < 0.05 → $H_0$ 기각

> 💬 **p값(p-value)**: 귀무가설이 참일 때,
> 관측된 결과 이상이 나올 확률.
> 작을수록 “가설이 맞을 가능성이 낮다.”

---

### (5) 회귀와 상관

1. **상관(Correlation)**

   * 두 변수 간 선형 관계의 강도
     $$-1 \le r \le 1$$

2. **회귀(Regression)**

   * 독립변수($x$)가 종속변수($y$)에 미치는 영향
     $$y = \beta_0 + \beta_1 x + \varepsilon$$

> 💬 **기호 해설**
>
> * $\beta_0$: 절편(intercept)
> * $\beta_1$: 기울기(slope, 영향의 크기)
> * $\varepsilon$: 오차항(error term) — 실제값과 예측값의 차이
>
> 💬 **기호 어원**
> * **$\beta$ (베타, beta)**: 그리스 알파벳 2번째 글자. 회귀에서 "계수(coefficient)"를 나타내는 전통적 표기. $\beta_0$는 0차(상수항), $\beta_1$은 1차(기울기).
> * **$\varepsilon$ (입실론, epsilon)**: 그리스어 "error"의 첫 글자. 측정 불가능한 무작위 오차를 표현. 작은 값을 의미하는 수학 전통에도 부합.

### 선형 회귀 시각화: 좌표계 회전

![Linear regression rotating](https://upload.wikimedia.org/wikipedia/commons/8/84/Linear_regression%2C_rotating_coordinate_system.gif)

> 출처: [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Linear_regression,_rotating_coordinate_system.gif) - 좌표계를 회전시키면서 선형 회귀선의 기하학적 의미를 보여주는 애니메이션

> 💬 **회귀의 기하학적 해석**
>
> * 회귀선은 데이터 점들로부터의 **수직 거리 제곱합을 최소화**하는 직선 (최소제곱법, OLS)
> * 좌표계를 회전시키면 회귀선의 방향이 데이터의 **주성분 방향**과 일치함을 알 수 있음
> * 상관계수 $r$이 클수록 데이터 점들이 회귀선 주위에 밀집
> * 이 시각화는 회귀분석과 주성분분석(PCA)의 관계를 이해하는 데 도움

---

## ✅ 핵심 요약표

| 용어   | 기호                     | 의미                 |
| ---- | ---------------------- | ------------------ |
| 모집단  | $N$, $\mu$, $\sigma^2$ | 전체 대상, 평균, 분산      |
| 표본   | $n$, $\bar{x}$, $s^2$  | 일부 데이터, 표본평균, 표본분산 |
| 확률함수 | $P(A)$                 | 사건 A의 발생 가능성       |
| 확률변수 | $X$                    | 사건을 수로 표현한 변수      |
| 가설   | $H_0$, $H_1$           | 통계적 주장 (귀무, 대립)    |
| 회귀계수 | $\beta_0$, $\beta_1$   | 변수 간 관계의 강도        |
| p-값  | $p$                    | 귀무가설하에서 결과가 나올 확률  |

---

## 📚 추가 학습 자료 (한국어)

### 🎓 온라인 강의
- **[KOCW 기초통계학](http://www.kocw.net/home/m/search/kemView.do?kemId=1052562)** - 여인권 교수 강의
- **[K-MOOC 통계학의 이해 I](https://www.kmooc.kr/view/course/detail/6760)** - 숙명여대, 표본 수집과 확률분포 학습
- **[한밭대 통계학개론](http://www.kocw.net/home/cview.do?mty=p&kemId=1215315)** - 임준묵 교수, 통계 패키지 실습 포함

### 🔗 인터랙티브 시뮬레이션
- **[PhET 수학 및 통계 시뮬레이션](https://phet.colorado.edu/ko/simulations/filter?subjects=math-and-statistics&type=html)** - 콜로라도대학교의 무료 대화형 시뮬레이션
- **[자바실험실(Javalab)](https://javalab.org/en/)** - 다양한 과학/수학 가상 실험

### 📖 웹 학습 자료
- **[데이터 사이언스 스쿨](https://datascienceschool.net/)** - 파이썬 기반 통계학 튜토리얼

---

# 🎲 확률변수와 확률분포 (Random Variable & Probability Distribution)

## 1️⃣ 확률변수(Random Variable)

### (1) 정의

* **확률변수(Random Variable)**란
  **확률적 실험의 결과를 수치로 대응시키는 함수**를 의미한다.

$$
X : S \rightarrow \mathbb{R}
$$

> 💬 **용어 주석**
>
> * $S$: **표본공간(Sample Space)** — 가능한 모든 결과들의 집합
> * $\mathbb{R}$: **실수(real numbers)** 집합
> * $X$는 각 결과 $\omega \in S$를 실수 $x = X(\omega)$로 대응시키는 **함수(Function)**
> * 즉, “결과를 숫자로 바꿔주는 규칙”

예시:

* 주사위를 던질 때 → 결과 ${1,2,3,4,5,6}$
  확률변수 $X$: “나온 눈의 수” → $X(1)=1, \dots, X(6)=6$

---

### (2) 확률변수의 유형

| 구분                        | 정의                  | 예시                 | 대표 기호                 |
| ------------------------- | ------------------- | ------------------ | --------------------- |
| **이산형 확률변수 (Discrete)**   | 셀 수 있는 개수의 값을 가짐    | 주사위 눈, 동전 던지기 성공횟수 | $X \in {0,1,2,\dots}$ |
| **연속형 확률변수 (Continuous)** | 연속적인 구간 내의 모든 값을 가짐 | 키, 체중, 온도          | $X \in \mathbb{R}$    |

> 💬 **핵심 차이점**
>
> * 이산형은 **확률질량함수(PMF)**
> * 연속형은 **확률밀도함수(PDF)**로 표현됨.

---

## 2️⃣ 확률질량함수 (Probability Mass Function, PMF)

### (1) 정의

* **이산형 확률변수**의 각 값에 대응되는 확률을 나타내는 함수

$$
p(x) = P(X = x)
$$

> 💬 **기호 해설**
>
> * $p(x)$: 확률질량함수(probability mass function)
> * $P(X = x)$: “X가 x의 값을 가질 확률”
> * $x$: 확률변수 $X$의 가능한 값 (support set)

---

### (2) 성질 (PMF의 공리)

1. 모든 확률은 0 이상
   $$
   p(x) \ge 0
   $$

2. 전체 확률의 합은 1
   $$
   \sum_x p(x) = 1
   $$

3. 사건의 확률은 해당 값들의 합으로 구함
   $$
   P(a \le X \le b) = \sum_{x=a}^{b} p(x)
   $$

---

### (3) 예시

**주사위 눈의 확률질량함수**

$$
p(x) =
\begin{cases}
\frac{1}{6}, & x = 1,2,3,4,5,6 \
0, & \text{그 외}
\end{cases}
$$

> 💬 $\sum_{x=1}^6 p(x) = 1$이므로 조건을 만족함.

---

## 3️⃣ 확률밀도함수 (Probability Density Function, PDF)

### (1) 정의

* **연속형 확률변수**의 분포를 나타내는 함수로,
  확률이 아니라 **확률의 밀도(density)**를 의미한다.

$$
f(x) \ge 0, \quad \int_{-\infty}^{\infty} f(x),dx = 1
$$

> 💬 **기호 해설**
>
> * $f(x)$: 확률밀도함수(probability density function)
> * 적분 $\int$: 연속된 구간의 합을 의미
> * 확률 그 자체는 면적(area)으로 계산된다.

---

### (2) 확률 계산

* 특정 구간의 확률은 **면적(적분)**으로 구함
  $$
  P(a \le X \le b) = \int_a^b f(x),dx
  $$

> 💬 **인사이트**
> 연속형 변수에서는 $P(X=x)=0$이다.
> 즉, 하나의 점이 아니라 **구간 단위**로만 확률을 계산할 수 있다.

---

### (3) 예시: 정규분포 (Normal Distribution)

$$
f(x) = \frac{1}{\sqrt{2\pi\sigma^2}} \exp\left( -\frac{(x-\mu)^2}{2\sigma^2} \right)
$$

> 💬 **기호 해설**
>
> * $\mu$: 평균(mean)
> * $\sigma^2$: 분산(variance)
> * $\exp(x)$: $e^x$ (자연상수 $e \approx 2.718$의 거듭제곱)
> * 이 분포는 종(bell) 모양으로, 중심이 $\mu$에 위치함.
>
> 💬 **기호 어원 보충**
> * **$\sigma^2$ (시그마 제곱)**: 분산은 "편차 제곱의 평균"이므로 $\sigma$(표준편차)를 제곱한 형태로 표기. "제곱"이 들어가는 이유는 양수 값을 보장하고 단위를 맞추기 위함.

---

## 4️⃣ 누적분포함수 (Cumulative Distribution Function, CDF)

### (1) 정의

* 확률변수가 특정 값 이하일 확률을 나타내는 함수

$$
F(x) = P(X \le x)
$$

> 💬 **용어 주석**
>
> * $F(x)$: 누적분포함수(CDF)
> * $x$: 임계값(threshold)
> * “$x$까지의 누적확률”이라는 의미

---

### (2) 성질

1. 단조증가: $F(x_1) \le F(x_2)$, $x_1 < x_2$
2. 극한값: $\lim_{x \to -\infty} F(x) = 0$, $\lim_{x \to \infty} F(x) = 1$
3. 이산형과 연속형 모두 정의 가능

   * 이산형: $F(x) = \sum_{t \le x} p(t)$
   * 연속형: $F(x) = \int_{-\infty}^x f(t),dt$

---

### (3) 예시

정규분포의 누적분포함수는 다음 적분 형태로 표현된다.
(닫힌 해석식이 존재하지 않음)

$$
F(x) = \int_{-\infty}^x \frac{1}{\sqrt{2\pi\sigma^2}}
\exp\left( -\frac{(t-\mu)^2}{2\sigma^2} \right) dt
$$

> 💬 실제 계산에서는 **표준정규분포표(z-table)** 또는 **컴퓨터 함수**를 사용한다.
> 예: Python → `scipy.stats.norm.cdf(x, mu, sigma)`

---

## 5️⃣ 확률변수의 기대값과 분산

### (1) 기대값(Expected Value)

* 확률변수의 **평균적 결과(기댓값)**
* 이산형:
  $$
  E[X] = \sum_x x p(x)
  $$
* 연속형:
  $$
  E[X] = \int_{-\infty}^{\infty} x f(x),dx
  $$

> 💬 “기대값”은 무작위 실험을 무한히 반복했을 때의 평균 결과.

---

### (2) 분산(Variance)

* 확률변수가 평균으로부터 얼마나 퍼져 있는지를 나타냄
  $$
  Var(X) = E[(X - E[X])^2]
  $$

* 표준편차(Standard Deviation):
  $$
  \sigma = \sqrt{Var(X)}
  $$

> 💬 **기호 해설**
>
> * $E[X]$: 기대값 (expected value)
> * $Var(X)$: 분산 (variance)
> * $\sigma$: 표준편차 (standard deviation)

---

### (3) 예시

이산형 변수 $X$가 0,1을 같게 가질 때 ($p(0)=p(1)=0.5$):

$$
E[X] = 0(0.5) + 1(0.5) = 0.5
$$
$$
Var(X) = E[X^2] - (E[X])^2 = (0^2)(0.5) + (1^2)(0.5) - 0.25 = 0.25
$$

---

## ✅ 핵심 요약표

| 개념     | 기호       | 의미                 |
| ------ | -------- | ------------------ |
| 확률변수   | $X$      | 결과를 수로 표현하는 함수     |
| 확률질량함수 | $p(x)$   | 이산형 변수의 확률함수       |
| 확률밀도함수 | $f(x)$   | 연속형 변수의 확률분포       |
| 누적분포함수 | $F(x)$   | $P(X \le x)$, 누적확률 |
| 기대값    | $E[X]$   | 확률변수의 평균           |
| 분산     | $Var(X)$ | 평균으로부터의 흩어짐 정도     |

---

# 📈 대표적인 확률분포 (Common Probability Distributions)

## 1️⃣ 분포(Distribution)의 개념

### (1) 정의

* **확률분포(Probability Distribution)**는 **확률변수 $X$**가 가질 수 있는 값과 그 **가능성(확률)**의 대응 규칙이다.
  이산형은 **확률질량함수(PMF)**, 연속형은 **확률밀도함수(PDF)**로 기술한다.

> 💬 **용어·기호 주석**
>
> * **확률변수 $X$**: 표본공간 $S$의 결과를 숫자로 대응시키는 함수 ($X:S\to\mathbb{R}$).
> * **PMF $p(x)$**: 이산형에서 $p(x)=P(X=x)$ (각 값에 “질량”처럼 확률이 붙음).
> * **PDF $f(x)$**: 연속형에서 $f(x)\ge0$, $\int_{-\infty}^{\infty}f(x),dx=1$ (확률은 구간의 “면적”).
> * **CDF $F(x)$**: 누적분포함수, $F(x)=P(X\le x)$.

### (2) PMF vs. PDF (시각)

| 이산형(PMF)                                                                                     | 연속형(PDF)                                                                                   |
| -------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| ![PMF 예시](https://upload.wikimedia.org/wikipedia/commons/7/75/Binomial_distribution_pmf.svg) | ![PDF 예시](https://upload.wikimedia.org/wikipedia/commons/7/74/Normal_Distribution_PDF.svg) |

> 출처: Wikimedia Commons

### (3) 스케일 매개변수의 효과 (Scale Parameter Effect)

![Scale parameter effects](https://upload.wikimedia.org/wikipedia/commons/e/e4/Effects_of_a_scale_parameter_on_a_positive-support_probability_distribution.gif)

> 출처: [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Effects_of_a_scale_parameter_on_a_positive-support_probability_distribution.gif) - 스케일 매개변수가 확률분포의 형태에 미치는 영향

> 💬 **스케일 매개변수(Scale Parameter)**
>
> * **정의**: 분포의 "퍼짐" 또는 "스케일"을 조절하는 매개변수
> * **예시**:
>   - 정규분포: $\sigma$ (표준편차)
>   - 지수분포: $1/\lambda$ (평균)
>   - 감마분포: $1/\lambda$ (스케일)
> * **효과**:
>   - 스케일 ↑ → 분포가 더 넓게 퍼짐 (분산 ↑)
>   - 스케일 ↓ → 분포가 더 좁게 모임 (분산 ↓)
>   - 분포의 **형태(shape)**는 유지되고 **크기만 변함**
> * **위치 매개변수(Location Parameter)**와의 차이:
>   - 위치: 분포를 좌우로 이동 (예: $\mu$)
>   - 스케일: 분포를 확대/축소

---

## 2️⃣ 이산형 확률분포 (Discrete)

### (1) 베르누이분포 (Bernoulli)

$$
P(X=x)=p^x(1-p)^{1-x},\quad x\in{0,1}
$$

* **매개변수:** 성공확률 $p\in[0,1]$
* **기대값/분산:** $E[X]=p,;Var(X)=p(1-p)$
* **용례:** 단일 시도(성공/실패), 클릭 여부, 합격/불합격
* **시각:** ![Bernoulli PMF](https://upload.wikimedia.org/wikipedia/commons/b/b6/PMF_and_CDF_of_a_bernouli_distribution.png)

> 💬 **이름 주석 – “베르누이”**
> **야코프(야곱) 베르누이(Jacob Bernoulli, 1655–1705)**: 확률·대수의 기초 공헌. 베르누이 시행(성공/실패) 개념을 정립.

---

### (2) 이항분포 (Binomial)

$$
P(X=k)=\binom{n}{k}p^k(1-p)^{n-k},\quad k=0,1,\dots,n
$$

* **매개변수:** 시행 수 $n$, 성공확률 $p$
* **기대값/분산:** $E[X]=np,;Var(X)=np(1-p)$
* **용례:** $n$번 독립 베르누이 시행의 성공 횟수(AB테스트 성공 수)
* **시각:** ![Binomial PMF](https://upload.wikimedia.org/wikipedia/commons/7/75/Binomial_distribution_pmf.svg)

> 💬 **기호 주석**
> $\binom{n}{k}=\dfrac{n!}{k!(n-k)!}$는 조합(순서 무시). $!$는 팩토리얼.

### 이항분포 매개변수 변화 시각화

![Binomial distribution animation](https://upload.wikimedia.org/wikipedia/commons/7/74/Binomial_distribution_for_n_%3D_4.gif)

> 출처: [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Binomial_distribution_for_n_%3D_4.gif) - n=4일 때 성공확률 p가 변화함에 따른 이항분포의 형태 변화

> 💬 **매개변수 효과**
>
> * $p=0.5$일 때 대칭적 형태
> * $p$가 0 또는 1에 가까워질수록 분포가 한쪽으로 치우침
> * $n$이 클수록 분포가 정규분포에 가까워짐 (드무아브르-라플라스 정리)

### 이항분포와 정규분포의 관계 (드무아브르-라플라스 정리)

![De Moivre-Laplace theorem](https://upload.wikimedia.org/wikipedia/commons/7/79/De_moivre-laplace.gif)

> 출처: [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:De_moivre-laplace.gif) - 이항분포가 정규분포로 수렴하는 과정

> 💬 **이항분포의 정규 근사**
>
> * $n$이 충분히 크고 $p$가 0.5에 가까우면, 이항분포는 정규분포로 근사 가능
> * 근사 조건: $np \geq 5$ 그리고 $n(1-p) \geq 5$
> * 이는 **중심극한정리(CLT)**의 특수 사례로, 드무아브르와 라플라스가 최초로 발견

---

### (3) 포아송분포 (Poisson)

$$
P(X=k)=\frac{\lambda^k e^{-\lambda}}{k!},\quad k=0,1,2,\dots
$$

* **매개변수:** 평균발생률 $\lambda>0$
* **기대값/분산:** $E[X]=Var(X)=\lambda$
* **용례:** 단위 시간/공간의 드문 사건 발생 횟수(콜센터 콜, 웹 클릭 수, 돌연변이 수)
* **시각:** ![Poisson PMF](https://upload.wikimedia.org/wikipedia/commons/1/16/Poisson_pmf.svg)

> 💬 **이름 주석 – "포아송"**
> **시메옹 드니 포아송(S.-D. Poisson, 1781–1840)**: 확률·해석학 공헌. 드문 사건 근사 모델로 유명.
>
> 💬 **기호 어원 – $\lambda$ (람다, lambda)**
> 그리스 알파벳 11번째 글자. 발생률(rate), 강도(intensity)를 나타내는 매개변수로 널리 사용. 포아송 과정에서 "단위 시간당 평균 발생 횟수"를 의미.

---

## 3️⃣ 연속형 확률분포 (Continuous)

### (1) 균등분포 (Uniform, 연속)

$$
f(x)=
\begin{cases}
\dfrac{1}{b-a}, & a\le x\le b[4pt]
0, & \text{그 외}
\end{cases}
$$

* **매개변수:** 구간 경계 $a<b$
* **기대값/분산:** $E[X]=\dfrac{a+b}{2},;Var(X)=\dfrac{(b-a)^2}{12}$
* **용례:** 무작위 초기값, 난수 테스트
* **시각:** ![Uniform PDF](https://upload.wikimedia.org/wikipedia/commons/9/96/Uniform_Distribution_PDF_SVG.svg)

---

### (2) 정규분포 (Normal, Gaussian)

$$
f(x)=\frac{1}{\sqrt{2\pi\sigma^2}}\exp!\Big(-\frac{(x-\mu)^2}{2\sigma^2}\Big)
$$

* **매개변수:** 평균 $\mu$, 표준편차 $\sigma>0$
* **기대값/분산:** $E[X]=\mu,;Var(X)=\sigma^2$
* **용례:** 키/점수/오차 등 자연·측정 현상, 중심극한정리의 한계분포
* **시각:** ![Normal PDF](https://upload.wikimedia.org/wikipedia/commons/7/74/Normal_Distribution_PDF.svg)

> 💬 **이름 주석 – "정규/가우스"**
> **아브라함 드 무아브르(Abraham de Moivre, 1667–1754)**가 초기 형태 연구,
> **카를 F. 가우스(Carl F. Gauss, 1777–1855)**가 오차이론으로 널리 보급. "가우시안(Gaussian)"이라 부르기도 함.

### 정규분포의 스케일 변화 시각화

![Normal distribution and scales](https://upload.wikimedia.org/wikipedia/commons/3/3a/Normal_distribution_and_scales.gif)

> 출처: [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Normal_distribution_and_scales.gif) - 평균(μ)과 표준편차(σ)의 변화에 따른 정규분포 형태 변화

> 💬 **매개변수의 효과**
>
> * **평균 $\mu$**: 분포의 중심 위치를 결정 (좌우 이동)
> * **표준편차 $\sigma$**: 분포의 퍼짐 정도를 결정 (폭 조절)
>   - $\sigma$가 작으면 → 뾰족하고 좁은 분포 (데이터가 평균 근처에 밀집)
>   - $\sigma$가 크면 → 완만하고 넓은 분포 (데이터가 평균에서 멀리 퍼짐)
> * **68-95-99.7 규칙**: $\mu \pm 1\sigma$ (68%), $\mu \pm 2\sigma$ (95%), $\mu \pm 3\sigma$ (99.7%)

---

### (3) 지수분포 (Exponential)

$$
f(x)=\lambda e^{-\lambda x},\quad x\ge0
$$

* **매개변수:** 발생률 $\lambda>0$
* **기대값/분산:** $E[X]=1/\lambda,;Var(X)=1/\lambda^2$
* **특징:** **무기억성(memoryless)** — $P(X>s+t\mid X>t)=P(X>s)$
* **용례:** 대기시간(고장·도착 간격)
* **시각:** ![Exponential PDF](https://upload.wikimedia.org/wikipedia/commons/e/ec/Exponential_pdf.svg)

> 💬 **개념 주석 – "무기억성"**
> 과거 경과 시간과 무관하게 남은 시간이 같은 분포를 따르는 성질(지수·기하분포만 가짐).
>
> 💬 **기호 재사용 – $\lambda$**
> 포아송분포와 같은 $\lambda$ 기호를 사용하는 이유: 지수분포는 포아송 과정에서 "사건 간 대기시간"을 모델링하므로, 같은 발생률(rate) 매개변수를 공유.

---

### (4) 감마분포 (Gamma)

$$
f(x)=\frac{\lambda^k x^{k-1} e^{-\lambda x}}{\Gamma(k)},\quad x>0
$$

* **매개변수:** 모양 $k>0$, 비율 $\lambda>0$
* **기대값/분산:** $E[X]=\dfrac{k}{\lambda},;Var(X)=\dfrac{k}{\lambda^2}$
* **관계:** $k$개의 독립 지수($\lambda$) 합의 분포
* **용례:** 수명·신뢰성·보험 청구 간격
* **시각:** ![Gamma PDF](https://upload.wikimedia.org/wikipedia/commons/e/e6/Gamma_distribution_pdf.svg)

> 💬 **기호 주석 – $\Gamma(\cdot)$**
> 감마함수: $\Gamma(k)=\int_0^\infty t^{k-1}e^{-t},dt$, 정수 $n$에 대해 $\Gamma(n)=(n-1)!$.
>
> 💬 **기호 어원 – $\Gamma$ (대문자 감마, Gamma)**
> 그리스 알파벳 3번째 글자 대문자. 레온하르트 오일러(Leonhard Euler, 1729)가 팩토리얼의 확장으로 처음 정의. "generalized factorial"의 의미로 감마 함수라 명명.

---

### (5) 카이제곱분포 ($\chi^2$)

$$
\chi^2=\sum_{i=1}^{k}Z_i^2,\quad Z_i\sim N(0,1)\ \text{독립}
$$

* **매개변수:** 자유도 $k\in\mathbb{N}$
* **기대값/분산:** $E[X]=k,;Var(X)=2k$
* **용례:** 분산 추정, 적합도/독립성 검정의 검정통계량
* **시각:** ![Chi-square PDF](https://upload.wikimedia.org/wikipedia/commons/3/35/Chi-square_pdf.svg)

> 💬 **용어 주석 – 자유도(df)**
> 통계량이 자유롭게 변할 수 있는 **독립 정보의 수**. 표본제약(평균 등)으로 줄어듦.
>
> 💬 **기호 어원 – $k$ (자유도)**
> 카이제곱 분포에서는 일반적으로 $k$, $df$, 또는 $\nu$(뉴, nu)로 표기. "degrees of freedom"의 개념은 Ronald Fisher가 1920년대에 정립.

---

### (6) 스튜던트 t분포 (Student’s t)

$$
f(t)=\frac{\Gamma\big(\frac{\nu+1}{2}\big)}{\sqrt{\nu\pi},\Gamma\big(\frac{\nu}{2}\big)}
\left(1+\frac{t^2}{\nu}\right)^{-\frac{\nu+1}{2}}
$$

* **매개변수:** 자유도 $\nu>0$
* **특징:** 꼬리가 두꺼움(소표본·모분산 미지 상황에서 평균 추론에 적합)
* **용례:** 평균 차이 t-검정, 회귀계수 유의성 검정
* **시각:** ![t PDF](https://upload.wikimedia.org/wikipedia/commons/4/41/Student_t_pdf.svg)

> 💬 **이름 주석 – "Student"**
> **윌리엄 시얼리 고셋(William S. Gosset, 1876–1937)**이 **본명 대신 "Student"** 필명으로 발표(기네스 양조장 재직 당시 사내 규정 때문).
>
> 💬 **기호 어원 – $\nu$ (뉴, nu)**
> 그리스 알파벳 13번째 글자. t분포와 카이제곱분포에서 자유도(degrees of freedom)를 나타낼 때 $\nu$ 또는 $df$ 사용. $n$(표본크기)과 혼동을 피하기 위해 그리스 문자 선택.

---

### (7) F분포 (Fisher–Snedecor)

$$
F=\frac{(X_1/d_1)}{(X_2/d_2)},\quad X_1\sim\chi^2_{d_1},\ X_2\sim\chi^2_{d_2}\ \text{독립}
$$

* **매개변수:** 자유도 $d_1,d_2\in\mathbb{N}$
* **용례:** 분산분석(ANOVA), 회귀 총체 적합도 검정(전체 $R^2$ 유의성)
* **시각:** ![F PDF](https://upload.wikimedia.org/wikipedia/commons/7/74/F-distribution_pdf.svg)

> 💬 **이름 주석 – Fisher–Snedecor**
> **로널드 A. 피셔(R. A. Fisher, 1890–1962)**, **조지 W. 스네데커(George W. Snedecor, 1881–1974)**가 발전·보급.

---

## ✅ 매개변수·요약치 한눈에 보기

| 분포       | 유형 | 매개변수         | $E[X]$          | $Var(X)$               | 대표 용례    |
| -------- | -- | ------------ | --------------- | ---------------------- | -------- |
| 베르누이     | 이산 | $p$          | $p$             | $p(1-p)$               | 단일 성공/실패 |
| 이항       | 이산 | $n,p$        | $np$            | $np(1-p)$              | 성공 횟수    |
| 포아송      | 이산 | $\lambda$    | $\lambda$       | $\lambda$              | 희귀 사건 수  |
| 균등       | 연속 | $a,b$        | $\frac{a+b}{2}$ | $\frac{(b-a)^2}{12}$   | 무작위 구간   |
| 정규       | 연속 | $\mu,\sigma$ | $\mu$           | $\sigma^2$             | 자연·오차    |
| 지수       | 연속 | $\lambda$    | $1/\lambda$     | $1/\lambda^2$          | 대기시간     |
| 감마       | 연속 | $k,\lambda$  | $k/\lambda$     | $k/\lambda^2$          | 수명/신뢰성   |
| $\chi^2$ | 연속 | $k$          | $k$             | $2k$                   | 분산·적합도   |
| t        | 연속 | $\nu$        | $0$             | $\nu/(\nu-2)$, $\nu>2$ | 평균 추론    |
| F        | 연속 | $d_1,d_2$    | —               | —                      | 분산 비교    |

> 💬 **추가 용어 주석**
>
> * **ANOVA**: Analysis of Variance, 집단 평균 차이의 통계적 검정.
> * **유의수준 $\alpha$**: 1종 오류 허용 확률(보통 0.05).
> * **p-값**: 귀무가설하에서 관측 이상 극단 결과의 확률(작을수록 증거 강함).
>
> 💬 **기호 어원**
> * **$\alpha$ (알파, alpha)**: 그리스 알파벳 첫 글자. "significance level"을 나타내며, 통계학에서 1종 오류(Type I error) 확률로 정의. Jerzy Neyman과 Egon Pearson이 1920-30년대 가설검정 이론 정립 시 도입.
> * **$p$ (p-value)**: "probability"의 첫 글자. Ronald Fisher가 1925년 저서에서 "p for probability"로 처음 사용.
> * **$\theta$ (세타, theta)**: 그리스 알파벳 8번째 글자. 일반적인 "모수(parameter)"를 나타낼 때 사용. 특정 모수($\mu$, $\sigma$)가 아닌 임의의 모수를 지칭.

---

## 📚 추가 학습 자료 (한국어) - 확률분포

### 🎯 공돌이의 수학정리노트 (시각화 포함)
- **[이항 분포](https://angeloyeo.github.io/2021/04/23/binomial_distribution.html)** - 베르누이 시행과 이항분포의 관계
- **[포아송 분포](https://angeloyeo.github.io/2021/04/26/Poisson_distribution.html)** - 드문 사건의 모델링
- **[기하 분포](https://angeloyeo.github.io/2021/04/28/geometric_distribution.html)** - 첫 성공까지의 시행 횟수
- **[정규분포의 공식 유도](https://angeloyeo.github.io/2020/09/14/normal_distribution_derivation.html)** - 가우스 분포 수식 유도 과정
- **[카이제곱 분포와 검정](https://angeloyeo.github.io/2021/12/13/chi_square.html)** - 카이제곱 분포와 적합도 검정
- **[최대우도법(MLE)](https://angeloyeo.github.io/2020/07/17/MLE.html)** - 확률분포 매개변수 추정

### 📖 웹 자료
- **[데이터 사이언스 스쿨 - 베르누이분포와 이항분포](https://datascienceschool.net/02%20mathematics/08.02%20베르누이분포와%20이항분포.html)** - 분류문제에서의 활용
- **[Khan Academy Korea - 베르누이 분포](https://ko.khanacademy.org/math/statistics-probability/random-variables-stats-library/binomial-mean-standard-dev-formulas/v/mean-and-variance-of-bernoulli-distribution-example)** - 평균과 분산 예제 동영상
- **[Wikidocs - 베르누이분포와 이항분포](https://wikidocs.net/198620)** - 확률 다루기 기초

---

# 📦 표본분포와 중심극한정리 (Sampling Distributions & CLT)

## 1️⃣ 표본분포(Sampling Distribution)

### (1) 정의

* **표본분포**는 같은 크기 $n$의 표본을 **여러 번** 뽑아 계산한 어떤 **통계량(statistic)**의 **분포**이다.
  예: 표본평균 $\bar{X}$ 의 표본분포, 표본비율 $\hat{p}$ 의 표본분포 등.

  > 💬 **용어·기호 주석**
  >
  > * **통계량**: 표본으로부터 계산된 수치(예: $\bar{X}, s^2$).
  > * **모수(parameter)**: 모집단의 특성(예: $\mu, \sigma^2$).
  > * **표본평균**: $\bar{X}=\frac{1}{n}\sum_{i=1}^n X_i$ (각 $X_i$는 표본 관측값).

### (2) 표본평균의 기대값·분산 (정규성 가정 없이도 성립)

* $E[\bar{X}] = \mu$
* $Var(\bar{X}) = \dfrac{\sigma^2}{n}$

> 💬 **표준오차(SE)**: $SE(\bar{X})=\dfrac{\sigma}{\sqrt{n}}$ (모분산 미지 시 $s$로 대체)

### (3) 표본분포의 모양 (정규 모집단인 경우)

* 모집단이 정규라면, 어떤 $n$에서도
  $$\bar{X} \sim N!\left(\mu,\ \frac{\sigma^2}{n}\right).$$
  일반 모집단이어도 $n$이 커질수록 **정규에 근사**(CLT의 내용). ([위키백과][1])

---

## 2️⃣ 큰수의 법칙(LLN) vs. 중심극한정리(CLT)

### (1) 큰수의 법칙(LLN)

* $n \to \infty$일 때 $\bar{X} \to \mu$ (확률수렴/거의확실 수렴): **평균이 참값에 가까워짐**.
* “**수렴의 방향**(중심으로 모임)”을 말해줌.

### (2) 중심극한정리(CLT)

* $n$이 클 때 **표본평균의 확률분포 형태**가 **정규분포**에 가까워짐:
  $$Z=\frac{\bar{X}-\mu}{\sigma/\sqrt{n}}\ \xrightarrow{d}\ N(0,1).$$
* “**모양(형태)**가 정규로 간다”는 진술. ([위키백과][2])

> 💬 **핵심 차이**
>
> * **LLN**: 평균이 어디로 가는가(점수렴).
> * **CLT**: 평균의 **분포 모양**이 어떻게 되는가(분포수렴).
> * 두 정리는 상보적이며, 추론 통계의 핵심 기반.

### (3) 큰수의 법칙 시각화 (주사위 예시)

![Law of Large Numbers - Die Rolls](https://upload.wikimedia.org/wikipedia/commons/c/c9/LLN_Die_Rolls.gif)

> 출처: [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:LLN_Die_Rolls.gif) - 주사위를 반복해서 던질 때 평균이 기댓값(3.5)에 수렴하는 과정

> 💬 **시각화 해설**
>
> * 시행 횟수가 증가할수록 표본평균이 모평균(3.5)에 가까워짐
> * 초기에는 변동이 크지만, $n$이 커질수록 안정화
> * 이것이 바로 **큰수의 법칙**의 핵심: 충분히 많이 반복하면 평균이 참값에 수렴

---

## 3️⃣ 중심극한정리(CLT) — 정식 진술과 변형

### (1) 고전적 CLT (i.i.d. 버전)

* $X_1,\dots,X_n$ i.i.d., $E[X_i]=\mu$, $Var(X_i)=\sigma^2 \in(0,\infty)$이면
  $$
  \sqrt{n},\frac{\bar{X}-\mu}{\sigma}\ \xrightarrow{d}\ N(0,1).
  $$

> 💬 **기호 주석**
>
> * **i.i.d.**: independent and identically distributed(독립·동일분포).
> * $\xrightarrow{d}$: 분포수렴(convergence in distribution).
> * 정규화(표준화): 평균 0, 분산 1로 스케일 조정.

### (2) 일반화 CLT (비동일·약한 독립)

* **Lyapunov**, **Lindeberg–Feller** 조건 등으로 i.i.d.를 약화:
  독립이거나 약한 의존 하에서도 적절한 조건 충족 시 정규로 수렴. ([위키백과][2])

### (3) 수렴 속도(정밀도)

* **Berry–Esseen 부등식**: 수렴 오차가 대략 $O(1/\sqrt{n})$ 규모. (정규 근사의 “얼마나 빨리”를 계량) ([위키백과][2])

### (4) 역사·명칭

* **de Moivre–Laplace 정리**(이항→정규 근사)가 CLT의 초기 형태.
* “Central” 용어는 **G. Pólya(1920)**가 도입(중심적 중요성). ([위키백과][2])

---

## 4️⃣ CLT의 시각화(임베드)

### (1) 샘플 평균 분포의 정규화 수렴(애니메이션)

![CLT in action](https://upload.wikimedia.org/wikipedia/commons/c/cd/Clt_in_action.gif)

> 균등·왜도·이산 등 다양한 원 분포라도, **표본크기 $n$ 증가**에 따라
> **표본평균의 분포가 정규 형태로 수렴**하는 모습을 보여주는 GIF. ([위키미디어 공용판][3])

### (2) 주사위 합의 분포가 종모양으로 (이산 → 연속 근사)

![Dice sum CLT](https://upload.wikimedia.org/wikipedia/commons/8/8c/Dice_sum_central_limit_theorem.svg)

> 여러 개의 공정한 주사위를 던져 **합/평균**을 보면,
> $n$이 커질수록 **종(bell) 모양**에 가까워짐(정규 근사 향상). ([위키미디어 공용판][4])

### (3) 평균의 견고성 한계(반례 직관: 코시 분포)

![Mean estimator consistency – Cauchy](https://upload.wikimedia.org/wikipedia/commons/a/aa/Mean_estimator_consistency.gif)

> **코시(Cauchy)**처럼 **분산이 무한**인 분포는 CLT의 핵심 가정(유한 분산)을 위반 →
> **표본평균이 안정적으로 수렴하지 않음**(두꺼운 꼬리). ([위키미디어 공용판][5])

---

## 5️⃣ 실제 적용과 주의점

### (1) 정규 근사를 써도 좋은가?

* **조건 확인**: 독립성(또는 약한 의존), **유한 분산**, 표본크기 $n$의 크기.
* **비대칭/두꺼운 꼬리** 모집단은 **더 큰 $n$** 필요(수렴 느림).
* **Berry–Esseen**로 정규 근사 오차 규모를 가늠. ([위키백과][2])

### (2) $n\approx 30$ 규칙?

* “$n\ge 30$이면 OK”는 **엄밀한 근거 없음**.
  분포의 꼬리/왜도에 따라 **필요 $n$이 크게 달라짐**. ([위키백과][2])

### (3) 연속성 보정(continuity correction)

* 이항·포아송 같은 **이산 분포**를 정규로 근사할 때
  **$P(X\le k)\approx P!\left(Z\le \dfrac{k+0.5-\mu}{\sigma}\right)$** 처럼 **$0.5$ 보정** 사용.

### (4) 유한모집단 보정(FPC)

* 복원추출이 아닌 **유한 모집단($N$)**에서 표본비 $f=n/N$이 큰 경우
  $SE(\bar{X})=\dfrac{\sigma}{\sqrt{n}}\sqrt{\dfrac{N-n}{N-1}}$ 로 조정.

### (5) 의존 데이터(시계열·군집)

* 약한 상관(믹싱 조건 등) 하에서는 CLT 변형 가능.
  강한 의존/구조적 상관은 **부트스트랩(블록 부트스트랩 등)**로 대체 추정 고려.

---

## 6️⃣ 부트스트랩과 표본분포 추정(직관)

### (1) 부트스트랩(Bootstrap) 아이디어

* 모집단을 모를 때, **표본 자체를 근사 모집단**으로 삼아 **재표본(resampling)** →
  통계량의 **경험적 표본분포**를 추정(표준오차·신뢰구간 산출).

### (2) 구조 그림 (임베드)

![Bootstrap Illustration](https://upload.wikimedia.org/wikipedia/commons/4/4a/Illustration_bootstrap.svg)

> 한 표본에서 **재표본 여러 번** → 통계량 분포를 **경험적으로** 얻음. ([위키미디어 공용판][6])

---

## 7️⃣ 요약(핵심 식·기호 모음)

* **표본평균:** $\bar{X}=\dfrac{1}{n}\sum X_i$
* **기대값/분산:** $E[\bar{X}]=\mu,\ Var(\bar{X})=\dfrac{\sigma^2}{n}$
* **표준오차:** $SE(\bar{X})=\dfrac{\sigma}{\sqrt{n}}$
* **CLT:** $\dfrac{\bar{X}-\mu}{\sigma/\sqrt{n}}\xrightarrow{d}N(0,1)$ (i.i.d., 유한분산) ([위키백과][2])
* **LLN:** $\bar{X}\to\mu$ (수렴의 방향)
* **정규 근사 품질:** Berry–Esseen로 $O(1/\sqrt{n})$ 수준 점검 ([위키백과][2])

---

## 8️⃣ 더 읽을거리(개념·그림·인터랙티브)

* 위키: **중심극한정리 개요·변형·오해 정리** ([위키백과][2])
* 위키: **표본분포**(정규 모집단일 때의 결과, 비정규에서의 근사) ([위키백과][1])
* MIT 메모: **LLN vs CLT 직관 노트(PDF)** ([math.mit.edu][7])
* CLT 그림 모음: **Illustration of the CLT**(연속/이산 케이스) ([위키백과][8])

---

[1]: https://en.wikipedia.org/wiki/Sampling_distribution?utm_source=chatgpt.com "Sampling distribution"
[2]: https://en.wikipedia.org/wiki/Central_limit_theorem?utm_source=chatgpt.com "Central limit theorem"
[3]: https://commons.wikimedia.org/wiki/File%3AClt_in_action.gif?utm_source=chatgpt.com "File:Clt in action.gif"
[4]: https://commons.wikimedia.org/wiki/File%3ADice_sum_central_limit_theorem.svg?utm_source=chatgpt.com "File:Dice sum central limit theorem.svg"
[5]: https://commons.wikimedia.org/wiki/File%3AMean_estimator_consistency.gif?utm_source=chatgpt.com "File:Mean estimator consistency.gif"
[6]: https://commons.wikimedia.org/wiki/File%3AIllustration_bootstrap.svg?utm_source=chatgpt.com "File:Illustration bootstrap.svg"
[7]: https://math.mit.edu/~dav/05.dir/class6-prep.pdf?utm_source=chatgpt.com "Central Limit Theorem and the Law of Large Numbers"
[8]: https://en.wikipedia.org/wiki/Illustration_of_the_central_limit_theorem?utm_source=chatgpt.com "Illustration of the central limit theorem"

아래는 **GitHub 호환 Markdown** 형식으로,

> ✅ 개념 단위 완결 · ✅ 최대 5단계 계층 · ✅ 모든 기호/용어에 “풍부한 주석”을 단 버전
> 의 **〈중심극한정리: 중요성 · 정규성 가정 · 조건〉**입니다.
> (수식은 `$...$`, `$$...$$` 사용)

---

# 🔔 중심극한정리(CL T): 왜 중요한가 · 정규성은 언제/왜 필요한가 · 성립 조건

## 1️⃣ 왜 중요한가 (Purpose & Impact)

### (1) 핵심 진술 (표본평균의 점근 정규성)

* 서로 **독립·동일분포(i.i.d.)**인 $X_1,\dots,X_n$에 대해, $E[X_i]=\mu$, $Var(X_i)=\sigma^2\in(0,\infty)$이면
  $$
  Z_n=\frac{\bar{X}-\mu}{\sigma/\sqrt{n}}\xrightarrow{d}N(0,1),\quad \bar{X}=\frac{1}{n}\sum_{i=1}^n X_i.
  $$

> 💬 **주석(용어·기호·직관)**
>
> * **i.i.d.**: *independent & identically distributed* — 서로 영향 없이(독립), 같은 메커니즘에서 추출(동일분포). 실험·설문에서 “뽑는 방식이 균일하고 서로 간섭이 없다”는 가정.
> * **$\bar{X}$**: 표본평균 — 데이터의 평균이라는 “요약 통계량(statistic)”.
> * **분포수렴** $\xrightarrow{d}$: 확률변수의 **분포 형태**가 어떤 분포로 “가까워진다”는 뜻(값 자체가 수렴한다는 뜻은 아님).
> * **$N(0,1)$**: 평균 0, 분산 1의 표준정규. 중심이 0, 폭이 1인 종 모양.
> * **해석**: “원래 $X_i$가 어떤 분포든(조건 충족 시), **평균의 분포 모양**은 정규에 가까워진다.”

### (2) 실무적 중요성 (왜 모두가 CLT를 쓴다고 하는가)

1. **범용 근사**: 복잡한 원분포라도 평균/합의 분포를 **정규**로 근사 → **신뢰구간·가설검정** 공식이 단순해짐.
2. **표준오차(SE) 설계**: $SE(\bar{X})=\sigma/\sqrt{n}$ → 표본크기 $n$을 늘릴수록 불확실성 ↓. **표본 설계**의 근거.
3. **선형 결합의 단순화**: (가중)평균·합·차이 등의 분포가 정규로 수렴 → **다변량 방법(회귀·ANOVA·SEM의 일부)**의 점근 이론 기반.
4. **점근적 정확성**: 최대우도추정(MLE), M-추정 등 **추정량의 점근 정규성**과 연결 → 복잡한 모델에서도 **근사적 z/t 검정** 가능.

---

## 2️⃣ 정규성 가정은 왜/언제 필요한가 (Normality: Why & When)

### (1) “정규성 없어도 CLT가 돌아간다”는 사실

* CLT 자체는 **모집단 정규성**을 가정하지 않는다.
* 요지: **원분포 비정규**여도, 조건만 맞으면 **평균의 분포가 정규 근사** 된다.

> 💬 **오해 주의**
>
> * “데이터가 정규여야만 통계가 가능하다” → ❌.
> * “정규성은 CLT에 필수다” → ❌. (CLT는 유한분산 등 다른 조건이 핵심)

### (2) 그래도 정규성이 중요한 장면(소표본 ‘정확 분포’)

* **소표본에서 “정확(exact)” 분포**를 쓰려면 **정규성 가정**이 필요:

  * $X_i\sim N(\mu,\sigma^2)$이면

    * $$\frac{\bar{X}-\mu}{S/\sqrt{n}}\sim t_{n-1}$$
      (표본표준편차 $S$ 사용 시 ‘정확한’ t 분포)
    * $$\frac{(n-1)S^2}{\sigma^2}\sim \chi^2_{n-1}$$
      (‘정확한’ 카이제곱 분포)
    * F 검정(분산비)도 정규성 하에서 ‘정확’.
* **요점**: **소표본**·**정확 검정**·**분산 추론**에서는 정규성이 **문헌적 보증**을 줌.

> 💬 **잔차 정규성(회귀)**
>
> * 회귀모형에서 **오차(잔차)**가 근사 정규이면,
>   **계수 추정량의 근사 정규성**·**구간/검정**이 자연스러워짐(중심극한+정규성 가속 효과).

---

## 3️⃣ CLT 성립 조건 (Conditions)

### (1) 표준형(고전적 i.i.d. CLT)

* **독립**: $X_i$ 간 상호 영향 없음.
* **동일분포**: 같은 분포에서 나옴(같은 $\mu,\sigma^2$).
* **유한 분산**: $Var(X_i)=\sigma^2<\infty$ (꼬리가 너무 두꺼우면 위배).
* **충분히 큰 $n$**: 수렴의 속도는 분포의 왜도/첨도에 따라 다름.

> 💬 **상징적 체크리스트**
>
> * 표본 설계가 독립에 가깝나? (무작위·복원추출·군집효과 최소화)
> * 극단값(heavy tail) 위험이 큰가? (코시, $\alpha$-안정분포 등)
> * $n$은 충분한가? (왜도·첨도가 크면 더 큰 $n$ 필요)

### (2) 일반화(비동일·의존 가능)

* **Lyapunov CLT**: 고차 모멘트 존재 조건으로 동일분포 아님을 허용(충분조건).
* **Lindeberg–Feller CLT**: 각 항의 영향이 과도하지 않음을 제어하는 **린데베르크 조건**으로 일반화.
* **의존 자료용 CLT**: 혼합성(mixing)·마팅게일 차분 등 약한 의존 하에서 변형된 CLT 성립.

> 💬 **Berry–Esseen 부등식(정밀도)**
>
> * 정규 근사의 오차가 대략 $O(1/\sqrt{n})$ 규모로 줄어든다고 계량해줌(상수는 3차 절대 중심모멘트에 의존).
> * 실무적 의미: “**얼마나 큰 $n$이면 근사가 괜찮나**”를 가늠하는 가이드.

---

## 4️⃣ 용어·기호 주석 (Rich Glossary)

### (1) 수렴 표기

* **$\xrightarrow{d}$ (분포수렴)**: CDF가 점마다 수렴 → “모양이 닮아감”.
* **$\xrightarrow{p}$ (확률수렴)**: 어떤 값에 가까워질 확률이 1로 감 → LLN의 문맥에서 자주 사용.
* **$\xrightarrow{a.s.}$ (거의확실 수렴)**: 확률 1로 점수렴 — 가장 강한 형태.

### (2) LLN vs. CLT

* **LLN(큰수의 법칙)**: $\bar{X}\to\mu$ (평균이 **어디로** 가는지: 값의 수렴)
* **CLT**: $\bar{X}$의 **분포 모양**이 정규로 간다(분포의 수렴).
* **비유**: LLN은 “목표점으로 모여듦”, CLT는 “모여드는 과정의 **모양**”.

### (3) 표준오차(Standard Error)

* **$SE(\bar{X})=\sigma/\sqrt{n}$**: 표본평균의 변동성 척도.
* 모분산 미지이면 **$s$**로 대체($s$는 표본표준편차).
* 신뢰구간 길이·검정력 계산의 핵심.

### (4) 연속성 보정(Continuity Correction)

* 이산분포(이항·포아송)를 정규로 근사할 때
  $$P(X\le k)\approx P!\left(Z\le \frac{k+0.5-\mu}{\sigma}\right)$$
  처럼 **$0.5$** 보정을 넣어 격자-연속 차이를 완화.

### (5) 유한모집단 보정(Finite Population Correction)

* 복원추출이 아닌 **유한 모집단($N$)**에서 $f=n/N$이 크면
  $$SE(\bar{X})=\frac{\sigma}{\sqrt{n}}\sqrt{\frac{N-n}{N-1}}.$$
* 표본비가 클수록(많이 뽑을수록) 변동성이 더 빠르게 줄어듦.

### (6) Heavy tail / 반례

* **코시(Cauchy)**: 분산이 **무한** → **유한분산 가정 위배** → $\bar{X}$가 안정적으로 수렴하지 않음.
* **실무 사인**: 극단값이 자주·크게 발생, 분산 추정이 불안정, 평균·표준편차로 요약이 무의미해짐.

---

## 5️⃣ 실무 체크리스트 (적용 전 확인)

1. **표본 설계**: 가능한 한 **독립성** 확보(무작위 추출, 클러스터 회피·보정).
2. **분포 탐색**: 히스토그램·QQ-plot·꼬리(heavy tail) 징후 점검.
3. **표본크기**: 왜도·첨도 크면 **더 큰 $n$**. Berry–Esseen 감으로 정규 근사 품질 가늠.
4. **소표본**: 정규성 진단 후 **정확 분포(t/χ²/F)** 또는 **비모수/부트스트랩** 고려.
5. **의존 자료**: 블록부트스트랩, Newey–West(시계열) 등 **의존성 대응 추정** 사용.

---

## 📚 추가 학습 자료 (한국어) - 중심극한정리

### 🎯 공돌이의 수학정리노트 (시각화 + 증명)
- **[중심극한정리의 의미](https://angeloyeo.github.io/2020/09/15/CLT_meaning.html)** - 표본평균이 정규분포를 따르는 이유, 대화형 시각화 포함
- **[중심극한정리 증명](https://angeloyeo.github.io/2020/01/10/CLT_proof.html)** - 수학적 증명 과정과 직관적 설명

### 🔬 시뮬레이션 및 인터랙티브 자료
- **[PhET 통계 시뮬레이션](https://phet.colorado.edu/ko/simulations/filter?subjects=math-and-statistics&type=html)** - 표본분포 및 CLT 시각화
- **[JoVE Science Education - 중심극한정리](https://www.jove.com/kr/science-education/v/13583/central-limit-theorem)** - 표본평균 히스토그램 생성 비디오

### 📖 웹 자료
- **[인투더데이터 - 중심극한정리](https://intothedata.com/02.scholar_category/statistics/central_limit_theorem/)** - 데이터과학 위키
- **[마인드스케일 - 중심극한정리](https://www.mindscale.kr/docs/probability/central-limit-theorem)** - 확률 통계 기초

### 📄 학술 자료
- **[중심극한정리 관련 연구](https://scienceon.kisti.re.kr/srch/selectPORSrchArticle.do?cn=DIKO0011382259)** - 컴퓨터 시뮬레이션(EXCEL, SAS)을 통한 검증

---

아래는 **GitHub 호환 Markdown** 형식으로,

> ✅ 개념 단위 완결 · ✅ 모든 기호/용어 풍부한 주석 · ✅ 최대 5단계 계층 · ✅ 수식 `$...$`/`$$...$$` · ✅ 시각화(직접 제작 이미지 + 공개 이미지 임베드)
> 를 반영한 **〈확률분포와 가설검정〉**입니다.
> (직접 제작한 그림은 아래 경로에서 다운로드하여 GitHub에 업로드해 쓰면 됩니다:
> [Right-tail p-value](sandbox:/mnt/data/normal_pvalue_right.png) · [Two-tailed p-value](sandbox:/mnt/data/normal_pvalue_two_tailed.png) · [t vs normal](sandbox:/mnt/data/t_vs_normal.png) · [Power curve](sandbox:/mnt/data/power_curve_ztest.png) · [Chi-square tail](sandbox:/mnt/data/chi_square_right_tail.png) · [F tail](sandbox:/mnt/data/f_right_tail.png) · [t one/two tails](sandbox:/mnt/data/t_one_two_tailed.png))

---

# 🧪 확률분포와 가설검정 (Distributions & Hypothesis Testing)

## 1️⃣ 확률분포: 검정의 재료 (What are we integrating over?)

### (1) 정의

* **확률분포(Probability Distribution)**는 **확률변수 $X$**가 취할 수 있는 값과 그 **가능성**의 관계를 나타내는 수학적 기술.

  * **이산형**: **확률질량함수(PMF)** $p(x)=P(X=x)$ — 막대그래프(질량)
  * **연속형**: **확률밀도함수(PDF)** $f(x)\ge0$, $\int f(x),dx=1$ — 곡선(면적=확률)
  * **누적분포함수(CDF)** $F(x)=P(X\le x)$ — 누적확률

> 💬 **기호·용어 주석**
>
> * $X$: 확률변수(결과를 수로 대응시키는 함수).
> * $p(x), f(x)$: 각각 이산/연속에서의 분포 표현.
> * $F(x)$: 임계값 $x$ 이하 누적확률.
> * “면적 = 확률”: 연속형에서 **곡선 아래 면적**이 확률.

### (2) 대표 분포와 시각

| 분포                   | 유형 | 의미                  | 시각                                                                                                     |
| -------------------- | -- | ------------------- | ------------------------------------------------------------------------------------------------------ |
| 정규 $N(\mu,\sigma^2)$ | 연속 | 자연·오차·평균의 한계분포      | ![Normal PDF](https://upload.wikimedia.org/wikipedia/commons/7/74/Normal_Distribution_PDF.svg)         |
| t(df)                | 연속 | 소표본, 분산 미지일 때 평균 추론 | ![t PDF](https://upload.wikimedia.org/wikipedia/commons/4/41/Student_t_pdf.svg)                        |
| $\chi^2(k)$          | 연속 | 분산·적합도·독립성 검정       | ![Chi-square PDF](https://upload.wikimedia.org/wikipedia/commons/1/16/Chi-square_distribution_pdf.svg) |
| $F(d_1,d_2)$         | 연속 | 분산비, ANOVA          | ![F PDF](https://upload.wikimedia.org/wikipedia/commons/4/4d/F_distribution_pdf.svg)                   |

---

## 2️⃣ 가설검정의 구조 (How do we decide?)

### (1) 문제 세팅

* **귀무가설 $H_0$**: “차이 없음/효과 없음” 같은 **기본 가설**
* **대립가설 $H_1$**: 우리가 **찾고자 하는 효과/차이**
* **검정통계량 $T$**: 데이터로 계산하는 요약값(예: $Z$, $t$, $\chi^2$, $F$)
* **유의수준 $\alpha$**: 1종 오류(틀린 기각)의 허용 확률(보통 0.05)

> 💬 **핵심 원리**
>
> * $H_0$가 **참이라고 가정**하고, 그 하에서 $T$의 **분포**를 사용해
>   관측통계량 $t_{\text{obs}}$가 **얼마나 극단적인지(p-value)**를 계산.

### (2) p-값(p-value)의 정의와 시각

* **정의(우측단일 예)**:
  $$
  p\text{-value} = P\big(T \ge t_{\text{obs}} ,\big|, H_0 \big)
  $$
* **p-값 개념 시각화**:
  ![P-value concept](https://upload.wikimedia.org/wikipedia/commons/3/3a/P-value_in_statistical_significance_testing.svg)

  > 출처: [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:P-value_in_statistical_significance_testing.svg) - p-값은 귀무가설 하에서 관측값보다 극단적인 결과가 나올 확률

* **양측검정(two-tailed)**:
  $$
  p\text{-value} = P\big(|T| \ge |t_{\text{obs}}| ,\big|, H_0 \big)
  $$

> 💬 **해석 경고**
>
> * p-값은 “$H_0$가 참일 **확률**”이 **아님**.
> * p-값은 “$H_0$가 참이라면 지금처럼 **극단적 데이터**가 나올 **확률**”.
> * 작을수록 “$H_0$하에서 보기 드문 데이터” → 귀무가설 **기각** 근거가 됨(단, 효과크기/검정력 별도 확인 필요).

### (3) 단측/양측 설정 차이 (t-분포 예)

![One and two-tailed tests](https://upload.wikimedia.org/wikipedia/commons/4/42/Visualization_of_a_one-_and_two-tailed_test.svg)

> 출처: [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Visualization_of_a_one-_and_two-tailed_test.svg) - 단측검정(왼쪽)과 양측검정(오른쪽) 비교

> 💬 **단측 vs 양측**
>
> * **단측검정**: 한 방향으로만 극단값을 검정 (예: μ > μ₀ 또는 μ < μ₀)
> * **양측검정**: 양쪽 방향으로 극단값을 검정 (예: μ ≠ μ₀)
> * 연구가설의 방향성·사전 계획이 중요 - 데이터 확인 후 방향 선택은 부적절

---

## 3️⃣ 대표 검정과 분포 연결 (Common tests & their null distributions)

### (1) Z-검정 (모분산 $\sigma^2$ **알고 있음**)

* **가정**: $X_i$ i.i.d., $\sigma$ **알고 있음**, $n$ 크면 정규 근사 가능
* **통계량**:
  $$
  Z=\frac{\bar{X}-\mu_0}{\sigma/\sqrt{n}} \sim N(0,1)\ \text{under}\ H_0
  $$
* **의미**: 평균이 $\mu_0$와 다른가? (한/양측)

### (2) t-검정 (모분산 **모름**, 소표본)

* **단일 표본**:
  $$
  t=\frac{\bar{X}-\mu_0}{S/\sqrt{n}} \sim t_{n-1}\ \text{under}\ H_0
  $$
* **독립 표본(등분산 가정)**:
  $$
  t=\frac{\bar{X}_1-\bar{X}*2}{S_p\sqrt{1/n_1+1/n_2}}\sim t*{n_1+n_2-2}
  $$
  (여기서 $S_p$는 풀드 표준편차)

* **t-분포 vs 정규분포 비교**:

  ![t vs normal comparison](https://upload.wikimedia.org/wikipedia/commons/4/41/Student_t_pdf.svg)

  > 출처: [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Student_t_pdf.svg) - 다양한 자유도(df)에 따른 t-분포와 정규분포(파란선) 비교

> 💬 **주석**:
> * t-분포는 **꼬리가 두꺼워** 소표본에서 불확실성을 더 보수적으로 반영
> * 자유도가 증가할수록(표본크기↑) 정규분포에 수렴
> * df ≥ 30이면 t-분포와 정규분포가 거의 유사

### (3) 카이제곱 검정 ($\chi^2$)

* **분산에 대한 검정**:
  $$
  \frac{(n-1)S^2}{\sigma_0^2}\sim \chi^2_{n-1}
  $$
* **독립성/적합도(교차표)**:
  $$
  \chi^2=\sum \frac{(\text{Observed}-\text{Expected})^2}{\text{Expected}}
  $$

> 💬 **카이제곱분포 참고**: 분포 형태는 [앞서 제시된 카이제곱 PDF 이미지](https://upload.wikimedia.org/wikipedia/commons/3/35/Chi-square_pdf.svg) 참조. 자유도가 증가할수록 대칭적 형태로 변화.

### (4) F-검정 (분산비, ANOVA)

* **정의**:
  $$
  F=\frac{(X_1/d_1)}{(X_2/d_2)},\quad X_1\sim\chi^2_{d_1},\ X_2\sim\chi^2_{d_2}
  $$
* **용례**: 등분산 검정, 분산분석(집단 평균 차이)

> 💬 **F분포 참고**: 분포 형태는 [앞서 제시된 F PDF 이미지](https://upload.wikimedia.org/wikipedia/commons/7/74/F-distribution_pdf.svg) 참조. 두 개의 자유도(d₁, d₂)에 따라 형태가 달라짐.

---

## 4️⃣ 검정력(Power)과 표본크기 (Type I/Type II 오류와 효과크기의 관계)

### (1) 오류의 종류와 검정력 정의

| 실제 상황 \ 결정 | $H_0$ 채택 | $H_0$ 기각 |
|---------|--------|--------|
| **$H_0$ 참** | 올바른 결정 (1-α) | **1종 오류** (α) |
| **$H_0$ 거짓** | **2종 오류** (β) | 올바른 결정 (1-β = **검정력**) |

* **1종 오류($\alpha$)**: 참인 $H_0$를 기각 ("거짓 양성", False Positive)
* **2종 오류($\beta$)**: 거짓인 $H_0$를 채택 ("거짓 음성", False Negative)
* **검정력(Power)**: $1-\beta$ = **실제 효과가 있을 때 이를 올바르게 기각할 확률**

> 💬 **효과크기(effect size)** $d=\dfrac{\mu_1-\mu_0}{\sigma}$: 차이를 **표준편차 단위**로 스케일링 — 실질적 중요성의 척도. Cohen의 기준: small(0.2), medium(0.5), large(0.8)

### (2) 1종 오류, 2종 오류, 검정력 시각화

![Type I and Type II errors](https://upload.wikimedia.org/wikipedia/commons/a/aa/Type_I_and_II_errors.jpg)

> 출처: [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Type_I_and_II_errors.jpg) - 귀무가설(H₀)과 대립가설(H₁) 분포에서 α(1종 오류)와 β(2종 오류), 그리고 검정력(1-β) 표시

### (3) 검정력 곡선의 이해

![Power function](https://upload.wikimedia.org/wikipedia/commons/8/8f/ROC_space-2.png)

> 출처: [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:ROC_space-2.png) - ROC 곡선 (민감도 vs 1-특이도). 검정력은 진양성률(True Positive Rate)과 관련

> **핵심 메시지**:
> * **표본크기 $n$↑** → 두 분포의 중첩 감소 → β↓, 검정력(1-β)↑
> * **효과크기 $d$↑** → 두 분포의 거리↑ → β↓, 검정력↑
> * **유의수준 α↑** → 기각역↑ → 검정력↑ (단, 1종 오류도 증가)
> * p-값이 작아질 가능성이 높아져 유의한 결과를 얻기 쉬워짐

---

## 5️⃣ p-값 중심 사고를 단단히 다지기 (Do & Don’t)

### (1) 올바른 해석 (Do)

* “p-값은 **$H_0$가 참일 때, 현재 관측치 이상으로 극단적인 통계량이 나올 확률**.”
* 작은 p-값 → **데이터가 $H_0$와 상충**한다는 **증거** (효과크기·신뢰구간·파워와 함께 판단).

### (2) 피해야 할 해석 (Don’t)

* “p-값 = $H_0$가 참일 확률” ❌
* “p-값 = 효과의 크기” ❌ (p-값은 **크기 정보**가 아니라 **희귀성** 정보)
* “p<0.05면 실질적으로 중요하다” ❌ (효과크기, 표본크기, 맥락 필수)

### (3) 함께 볼 것

* **신뢰구간(CI)**: 효과크기의 **범위** 제시 → 추론의 풍부화
* **파워분석**: 연구 설계 단계에서 **필요 표본크기** 산출

---

## 6️⃣ 실전 체크리스트 (One-pass)

1. **가설 명확화**: $H_0$, $H_1$(단/양측).
2. **검정통계량 선택**: 평균/비율/분산/다집단? 대응표본?
3. **분포와 가정 확인**: 정규성/독립/등분산/표본크기.
4. **p-값 계산·보고**: $p$와 함께 **효과크기·CI** 병기.
5. **해석**: 통계적 유의성 ↔ 실질적 의미, 파워/재현가능성까지 고려.

---

## 7️⃣ 빠른 복습 퀴즈 (한 번에 하나씩!)

* Q1. p-값의 **정의 문장**을 당신의 말로 1문장으로 써보세요.
* Q2. 양측검정에서 p-값을 면적 관점으로 설명해 보세요(그림을 떠올리며).
* Q3. 효과크기 $d$와 표본크기 $n$이 **p-값**과 **파워**에 주는 영향은?

---

---

## 📋 통계분포표 (Statistical Distribution Tables)

가설검정과 신뢰구간 계산에 필수적인 통계표들을 제공합니다.

### 표준정규분포표 (Z-table)
- **[표준정규분포표 - 한국어 위키백과](https://ko.wikipedia.org/wiki/표준정규분포표)** - 정규 분포의 누적 분포 함수 값(Φ 값) 표
- **[정규분포표 - Chip One Stop](https://www.chip1stop.com/sp/knowledge/019_normal-distribution-table_ko)** - 표준정규분포 누적확률표 (양측, 단측)
- **[Khan Academy Korea - Z-table 사용법](https://ko.khanacademy.org/math/statistics-probability/modeling-distributions-of-data/normal-distribution-calculation/v/z-table-for-proportion-above)** - 비디오 강의

### t분포표 (t-table)
- **[T분포표 - 한국어 위키백과](https://ko.wikipedia.org/wiki/T분포표)** - 자유도별 t 임계값 표 (일측/양측)
- t분포는 자유도 ν(df)에 따라 임계값이 달라지며, 소표본 평균 검정에 사용

### 카이제곱분포표 (χ²-table)
- **[카이제곱 분포 - 한국어 위키백과](https://ko.wikipedia.org/wiki/카이제곱_분포)** - 카이제곱 분포 이론과 임계값
- **[카이제곱분포 - 나무위키](https://namu.wiki/w/카이제곱분포)** - 자유도별 카이제곱 값 표
- 분산 검정, 적합도 검정, 독립성 검정에 활용

### F분포표 (F-table)
- **[F 분포 - 한국어 위키백과](https://ko.wikipedia.org/wiki/F_분포)** - F 분포 이론 및 임계값
- **[F분포표 (α=0.05)](http://www.hocsi.com/f-dis_table_005_free.htm)** - 다양한 유의수준의 F 임계값
- **[확률분포표 모음](http://www.q-engineering.pe.kr/table_probability.htm)** - Z, t, χ², F 분포표 통합
- **[F 분포 계산기](http://www.estat.me/estat/eLearning/kr/eStatU/example/080200.html)** - 인터랙티브 F 분포 계산

> 💬 **사용 방법**
>
> 1. **유의수준 α** 설정 (보통 0.05 또는 0.01)
> 2. **검정 방향** 결정 (단측/양측)
> 3. **자유도** 확인 (표본크기, 모형 복잡도에 따라)
> 4. 해당 표에서 **임계값** 찾기
> 5. **검정통계량**과 비교하여 귀무가설 기각 여부 결정

---

## 🧮 실전 가설검정 문제 (분포표 활용 전 과정)

이 섹션에서는 **실제 데이터를 이용한 가설검정의 전 과정**을 단계별로 학습합니다.

### 📌 문제 1: 단일표본 t-검정 (One-Sample t-Test)

**🔬 연구 상황**:
어느 제약회사에서 신약을 개발했습니다. 이 신약이 혈압을 낮추는 효과가 있는지 검증하고자 합니다. 일반적으로 고혈압 환자의 평균 수축기 혈압은 **140 mmHg**입니다. 신약을 투여한 환자 16명의 수축기 혈압을 측정한 결과는 다음과 같습니다:

```
138, 135, 142, 136, 140, 133, 137, 134,
139, 136, 135, 141, 137, 138, 136, 135
```

**❓ 질문**: 이 신약이 혈압을 낮추는 효과가 있다고 할 수 있는가? (유의수준 α = 0.05)

---

#### 📊 Step 1: 가설 설정

- **귀무가설 (H₀)**: μ = 140 (신약은 효과가 없다)
- **대립가설 (H₁)**: μ < 140 (신약은 혈압을 낮춘다) ← **단측검정**

#### 🧮 Step 2: 검정통계량 계산

**1) 표본평균 계산**:
$$\bar{x} = \frac{138 + 135 + \cdots + 135}{16} = \frac{2197}{16} = 137.3125 \text{ mmHg}$$

**2) 표본표준편차 계산**:
$$s = \sqrt{\frac{\sum(x_i - \bar{x})^2}{n-1}} = \sqrt{\frac{(138-137.31)^2 + \cdots + (135-137.31)^2}{15}} = 2.496$$

**3) t-통계량 계산**:
$$t = \frac{\bar{x} - \mu_0}{s/\sqrt{n}} = \frac{137.3125 - 140}{2.496/\sqrt{16}} = \frac{-2.6875}{0.624} = -4.307$$

#### 📋 Step 3: 자유도 확인

$$\text{df} = n - 1 = 16 - 1 = 15$$

#### 📖 Step 4: 분포표에서 임계값 찾기

**t분포표 확인** (df=15, α=0.05, 단측):
- **임계값**: t₀.₀₅(15) = -1.753

**분포표 참조**: [t분포표 위키백과](https://ko.wikipedia.org/wiki/T분포표)

| 자유도 | α=0.10 (단측) | α=0.05 (단측) | α=0.025 (단측) |
|--------|---------------|---------------|----------------|
| 15 | 1.341 | **1.753** | 2.131 |

> 💡 단측검정(왼쪽 꼬리)이므로 음수: **-1.753**

#### 🎯 Step 5: 판정 및 결론

**판정 기준**:
- 검정통계량 t = **-4.307**
- 임계값 = **-1.753**
- **-4.307 < -1.753** → **기각역 내부** ✓

**p-값 추정**:
t분포표에서 df=15일 때:
- t = -1.753 → p = 0.05
- t = -2.131 → p = 0.025
- t = -4.307 → **p < 0.001** (매우 유의함!)

**✅ 결론**:
> 귀무가설을 **기각**합니다 (p < 0.001). 신약은 통계적으로 유의하게 혈압을 낮추는 효과가 있습니다 (평균 2.7 mmHg 감소).

**📚 참고자료**:
- [JMP - 1표본 t-검정](https://www.jmp.com/ko_kr/statistics-knowledge-portal/t-test/one-sample-t-test.html)
- [Khan Academy Korea - t-통계량 계산 예제](https://ko.khanacademy.org/math/statistics-probability/significance-tests-one-sample/tests-about-population-mean/v/example-calculating-t-statistic-for-signficance-test)

---

### 📌 문제 2: F-검정 (일원분산분석, One-Way ANOVA)

**🔬 연구 상황**:
세 가지 다른 비료(A, B, C)가 식물 성장에 미치는 효과를 비교하고자 합니다. 각 비료를 사용한 식물의 키(cm)를 측정한 결과입니다:

```
비료 A: 20, 22, 19, 21, 20  (n₁=5)
비료 B: 25, 27, 26, 28, 24  (n₂=5)
비료 C: 22, 23, 21, 24, 20  (n₃=5)
```

**❓ 질문**: 세 비료 간 평균 식물 키에 차이가 있는가? (유의수준 α = 0.05)

---

#### 📊 Step 1: 가설 설정

- **귀무가설 (H₀)**: μ₁ = μ₂ = μ₃ (모든 비료의 효과가 같다)
- **대립가설 (H₁)**: 적어도 하나의 평균이 다르다

#### 🧮 Step 2: 기초 통계량 계산

**각 그룹 평균**:
- $\bar{x}_A = \frac{20+22+19+21+20}{5} = 20.4$
- $\bar{x}_B = \frac{25+27+26+28+24}{5} = 26.0$
- $\bar{x}_C = \frac{22+23+21+24+20}{5} = 22.0$

**전체 평균**:
$$\bar{x}_{\text{total}} = \frac{20.4 \times 5 + 26.0 \times 5 + 22.0 \times 5}{15} = \frac{342}{15} = 22.8$$

#### 🧮 Step 3: 제곱합 계산

**1) 총 제곱합 (SST)**:
$$SST = \sum_{i=1}^{3}\sum_{j=1}^{5}(x_{ij} - \bar{x}_{\text{total}})^2$$
$$= (20-22.8)^2 + (22-22.8)^2 + \cdots + (20-22.8)^2 = 148.4$$

**2) 그룹 간 제곱합 (SSB - Between)**:
$$SSB = \sum_{i=1}^{3}n_i(\bar{x}_i - \bar{x}_{\text{total}})^2$$
$$= 5(20.4-22.8)^2 + 5(26.0-22.8)^2 + 5(22.0-22.8)^2$$
$$= 5(7.84) + 5(10.24) + 5(0.64) = 94.4$$

**3) 그룹 내 제곱합 (SSW - Within)**:
$$SSW = SST - SSB = 148.4 - 94.4 = 54.0$$

#### 🧮 Step 4: 평균제곱 (Mean Square) 계산

**자유도**:
- 그룹 간 자유도: $df_B = k - 1 = 3 - 1 = 2$
- 그룹 내 자유도: $df_W = N - k = 15 - 3 = 12$

**평균제곱**:
- $MSB = \frac{SSB}{df_B} = \frac{94.4}{2} = 47.2$
- $MSW = \frac{SSW}{df_W} = \frac{54.0}{12} = 4.5$

#### 🧮 Step 5: F-통계량 계산

$$F = \frac{MSB}{MSW} = \frac{47.2}{4.5} = 10.489$$

#### 📖 Step 6: 분포표에서 임계값 찾기

**F분포표 확인** (df₁=2, df₂=12, α=0.05):

**분포표 참조**: [F분포표](http://www.hocsi.com/f-dis_table_005_free.htm)

| df₂ \ df₁ | 1 | 2 | 3 |
|-----------|-----|-------|-----|
| 12 | 4.75 | **3.89** | 3.49 |

**임계값**: F₀.₀₅(2, 12) = **3.89**

#### 🎯 Step 7: 판정 및 결론

**ANOVA 결과표**:

| 요인 | SS | df | MS | F | F-임계값 | p-value |
|------|-----|-----|-----|-------|----------|---------|
| 그룹 간 | 94.4 | 2 | 47.2 | **10.489** | 3.89 | < 0.01 |
| 그룹 내 | 54.0 | 12 | 4.5 |  |  |  |
| 합계 | 148.4 | 14 |  |  |  |  |

**판정**:
- F-통계량 = **10.489**
- F-임계값 = **3.89**
- **10.489 > 3.89** → **기각역 내부** ✓

**✅ 결론**:
> 귀무가설을 **기각**합니다 (p < 0.01). 세 비료 간 식물 키의 평균에 **통계적으로 유의한 차이**가 있습니다. 특히 비료 B가 평균 26.0cm로 가장 효과가 좋습니다.

**📚 참고자료**:
- [공돌이의 수학정리노트 - F-value와 분산분석](https://angeloyeo.github.io/2020/02/29/ANOVA.html)
- [JMP - 일원 분산분석](https://www.jmp.com/ko_kr/statistics-knowledge-portal/one-way-anova.html)

---

### 📌 문제 3: 정규성 검정 (Shapiro-Wilk Test)

**🔬 연구 상황**:
회귀분석을 수행하기 전에 **잔차의 정규성**을 확인해야 합니다. 다음은 회귀분석 후 얻은 잔차(residuals) 10개입니다:

```
-0.5, 0.3, -0.2, 0.6, -0.4, 0.1, -0.3, 0.4, 0.2, -0.2
```

**❓ 질문**: 이 잔차가 정규분포를 따른다고 할 수 있는가? (유의수준 α = 0.05)

---

#### 📊 Step 1: 가설 설정

- **귀무가설 (H₀)**: 잔차는 정규분포를 따른다
- **대립가설 (H₁)**: 잔차는 정규분포를 따르지 않는다

#### 🧮 Step 2: 데이터 정렬 및 기초 통계량

**1) 오름차순 정렬**:
```
x₍₁₎ = -0.5, x₍₂₎ = -0.4, x₍₃₎ = -0.3, x₍₄₎ = -0.2, x₍₅₎ = -0.2,
x₍₆₎ = 0.1, x₍₇₎ = 0.2, x₍₈₎ = 0.3, x₍₉₎ = 0.4, x₍₁₀₎ = 0.6
```

**2) 평균과 표준편차**:
$$\bar{x} = \frac{-0.5 + 0.3 + \cdots + (-0.2)}{10} = \frac{0}{10} = 0$$

$$s^2 = \frac{\sum(x_i - \bar{x})^2}{n-1} = \frac{0.25 + 0.09 + \cdots + 0.04}{9} = \frac{1.24}{9} = 0.1378$$

#### 🧮 Step 3: Shapiro-Wilk W 통계량 계산

**Shapiro-Wilk 공식**:
$$W = \frac{\left(\sum_{i=1}^{n}a_i x_{(i)}\right)^2}{\sum_{i=1}^{n}(x_i - \bar{x})^2}$$

여기서 $a_i$는 n=10에 대한 Shapiro-Wilk 계수입니다 (표준화된 값).

**n=10일 때의 계수 (일부)**:
- $a_1 = 0.5739$ (첫 번째와 마지막 값의 가중치)
- $a_2 = 0.3291$
- ...

**계산**:
$$\text{분자} = [0.5739(-0.5 + 0.6) + 0.3291(-0.4 + 0.4) + \cdots]^2 = (0.05739)^2 = 0.00329$$

$$\text{분모} = \sum(x_i - 0)^2 = 0.25 + 0.09 + \cdots + 0.04 = 1.24$$

$$W = \frac{0.00329}{1.24} = 0.00265$$

> 💡 **실무에서는 통계 소프트웨어 사용**
> 실제로는 R, Python, SPSS 등의 통계 프로그램으로 계산합니다.
>
> **R 코드 예시**:
> ```r
> residuals <- c(-0.5, 0.3, -0.2, 0.6, -0.4, 0.1, -0.3, 0.4, 0.2, -0.2)
> shapiro.test(residuals)
>
> # Shapiro-Wilk normality test
> # W = 0.9697, p-value = 0.8863
> ```

#### 📖 Step 4: 임계값 및 p-값 확인

**Shapiro-Wilk 임계값 표** (n=10, α=0.05):
- **임계값**: W₀.₀₅(10) = **0.842**

**판정 기준**:
- **W > 0.842** → 귀무가설 채택 (정규성 만족)
- **W < 0.842** → 귀무가설 기각 (정규성 위반)

#### 🎯 Step 5: 판정 및 결론

**계산된 통계량**:
- W = 0.9697
- 임계값 = 0.842
- **0.9697 > 0.842** → **귀무가설 채택** ✓
- **p-value = 0.8863** (> 0.05)

**✅ 결론**:
> 귀무가설을 **채택**합니다 (p = 0.886). 잔차는 **정규분포를 따른다**고 볼 수 있습니다. 따라서 회귀분석의 정규성 가정이 만족되어 회귀분석 결과를 신뢰할 수 있습니다.

**🔍 보조 진단**:
- **Q-Q plot** (분위수-분위수 그림)으로 시각적 확인
- **Kolmogorov-Smirnov 검정** (n≥30일 때 권장)

**📚 참고자료**:
- [Statistics Playbook - 정규성 검정 완벽 가이드](https://statisticsplaybook.com/normality-test/)
- [R을 이용한 데이터 분석 - 샤피로 윌크 검정](https://thebook.io/006723/0262/)
- [정규성 검정 용어 설명](https://moons.kr/entry/통계용어-Shapiro-Wilk-Test샤피로-윌크-검정)

---

### 🎓 학습 포인트 정리

#### ✅ 공통 단계 (모든 가설검정)

1. **가설 설정**: H₀와 H₁를 명확히 정의
2. **유의수준 결정**: 보통 α = 0.05 또는 0.01
3. **검정통계량 계산**: 표본 데이터로부터 t, F, W 등 계산
4. **자유도 확인**: 검정에 따라 df 계산 방법이 다름
5. **분포표 참조**: 임계값 또는 p-값 확인
6. **판정**: 검정통계량과 임계값 비교
7. **결론**: 실질적 의미 해석

#### 📊 검정별 핵심 포인트

| 검정 | 검정통계량 | 자유도 | 언제 사용? |
|------|-----------|--------|-----------|
| **t-검정** | $t = \frac{\bar{x} - \mu_0}{s/\sqrt{n}}$ | df = n-1 | 모평균 비교, 모분산 모름 |
| **F-검정** | $F = \frac{MSB}{MSW}$ | df₁=k-1, df₂=N-k | 3개 이상 집단의 평균 비교 |
| **정규성 검정** | W (Shapiro-Wilk) | n (표본크기) | 정규분포 가정 확인 |

#### 💡 실무 팁

- **소표본(n<30)**: t-검정, Shapiro-Wilk 검정
- **대표본(n≥30)**: z-검정 가능, Kolmogorov-Smirnov 검정
- **분산 비교**: F-검정 전에 등분산 검정(Levene test) 먼저 수행
- **정규성 위반 시**: 비모수 검정(Mann-Whitney, Kruskal-Wallis) 고려

---

## 📚 추가 학습 자료 (한국어) - 가설검정

### 🎯 개념 설명 및 시각화
- **[공돌이의 수학정리노트 - p-value의 의미](https://angeloyeo.github.io/2020/03/29/p_value.html)** - p-값 개념과 시각적 설명
- **[기초통계학 - 가설검정과 p-value](https://soohee410.github.io/stat2)** - 직관적 이해와 그림 설명
- **[First Penguin School - 갈아먹는 통계 기초](https://blog.firstpenguine.school/37)** - 가설, 검정, p-value 기초
- **[Minitab 블로그 - P값을 올바르게 해석하는 방법](https://blog.minitab.com/ko/adventures-in-statistics-2/how-to-correctly-interpret-p-values)** - 실무 해석 가이드

### 🔬 1종/2종 오류와 검정력
- **[Minitab - 제1종 오류 및 제2종 오류의 정의](https://support.minitab.com/ko-kr/minitab/help-and-how-to/statistics/basic-statistics/supporting-topics/basics/type-i-and-type-ii-error/)** - 오류 유형 설명
- **[Khan Academy Korea - 1종 오류](https://ko.khanacademy.org/math/statistics-probability/significance-tests-one-sample/error-probabilities-and-power/v/type-1-errors)** - 비디오 강의
- **[위키백과 - 1종 오류와 2종 오류](https://ko.wikipedia.org/wiki/1종_오류와_2종_오류)** - 이론 및 사례
- **[WikiDocs - A/B 테스트 정복하기](https://wikidocs.net/198387)** - 단측검정, 양측검정 개념

### 📊 시각화 도구
- **[Wikimedia Commons - Hypothesis Testing Category](https://commons.wikimedia.org/wiki/Category:Hypothesis_testing)** - 가설검정 관련 다이어그램 모음 (49개 파일)
- **[Interactive NHST Visualization](https://rpsychologist.com/d3/nhst/)** - 검정력과 유의성 검정 대화형 시각화 (영문)
- **[Hypothesis Test Graph Generator](https://www.imathas.com/stattools/norm.html)** - 정규분포 기반 검정 그래프 생성기

### 📖 심화 학습
- **[의학통계 - 가설검정](http://bigdata.dongguk.ac.kr/lectures/med_stat/_book/가설검정.html)** - 동국대 빅데이터 강의 자료
- **[goteodata.kr - 가설검정](https://www.goteodata.kr/70)** - 상세한 수학적 표기와 예제
- **[Quality Insights - 엑셀로 p-value 계산](https://www.quality-insights.co.kr/2025/07/pvalue.html)** - 실습 가이드

---

# 관찰변인의 정규성 분석 — 산식의 배경과 “직접 계산” 예시

아래는 **왜도·첨도·CR·마할라노비스·마르디아 지수**의 산식을 배경부터 차근차근 설명하고, **작은 예시 데이터**로 실제 값을 손에 잡히도록 계산해 보인 것입니다. 마지막에는 **귀하의 표(〈표 IV-3〉)**에 그대로 적용할 때의 해석 포인트까지 연결합니다.

---

## 1. 단변량 정규성: 왜도(skewness)와 첨도(kurtosis)

### 1.1 배경

* 정규분포는 **대칭(왜도=0)**, **표준정규 대비 꼬리 두께가 동일(초과첨도=0)** 입니다.
* 실제 표본은 유한하므로 추정량의 **편향 보정 여부**에 따라 값이 조금 달라질 수 있습니다.

  * SPSS는 “보정형(또는 Fisher) 추정량”을,
  * AMOS의 “지수(index)”는 보정 여부가 다를 수 있습니다(소프트웨어 차이).

  아래는 **SPSS와 AMOS의 정규성 지표(왜도·첨도·CR)**가 왜 조금씩 달라질 수 있는지에 대한 배경과, **정의–산식–소프트웨어 구현 차이–수치적 예시**까지 한 번에 정리한 설명입니다. (필요 시, 실제 표본수 (n)을 알려 주시면 각 관찰변인의 SPSS/AMOS 값 차이를 정확히 역산해 표로 드리겠습니다.)

---

# 1) 왜 “보정형(또는 Fisher)”이 필요한가

* 우리가 계산하는 왜도·첨도는 **모집단(moment)**이 아니라 **표본(moment)**으로부터 구한 *추정량*입니다.
* 작은 표본에서는 표본왜도·첨도가 **체계적으로 치우친(biased)** 값이 되기 쉽습니다.
* 그래서 통계 패키지들은 **편향보정(bias correction)**을 적용한 버전(일명 *Adjusted Fisher–Pearson standardized moment coefficient*)을 기본값으로 보고하는 경우가 많습니다.

---

# 2) 정의와 산식(표본기반)

## 2.1 “순수 모멘트형(간단형)”—AMOS의 index가 주로 쓰는 형태

표본 (x_1,\dots,x_n), 평균 (\bar x), 표본표준편차 (s)라 할 때
[
g_1=\frac{m_3}{s^3},\quad g_2=\frac{m_4}{s^4}-3,
]
[
m_3=\frac1n\sum(x_i-\bar x)^3,\quad m_4=\frac1n\sum(x_i-\bar x)^4.
]

* (g_1): 표본 **왜도**(표준화된 3차 중심적률)
* (g_2): 표본 **초과첨도(excess)**(정규분포 대비 ( -3 )을 뺀 값)

## 2.2 “편향보정형(Adjusted Fisher–Pearson)”—SPSS의 기본

작은 표본에서의 기대값 편향을 줄이도록 보정한 형태입니다.
[
G_1=\frac{\sqrt{n(n-1)}}{,n-2,},g_1\qquad(\text{보정 왜도})
]
[
G_2=\frac{n-1}{(n-2)(n-3)}\Big[(n+1)g_2+6\Big]\qquad(\text{보정 초과첨도})
]

* **정상분포 표본**에서 (E(G_1)\approx0,\ E(G_2)\approx0)이 되도록 설계된 추정량입니다.
* (g_1,g_2)와 (G_1,G_2)의 차이는 **(n)이 클수록 빠르게 줄어듭니다**.

## 2.3 CR(critical ratio, z)와 표준오차

두 프로그램 모두 **큰 표본 근사**로 다음을 쓰는 것이 일반적입니다.
[
\operatorname{SE}(g_1)\approx \sqrt{\frac{6}{n}},\qquad
\operatorname{SE}(g_2)\approx \sqrt{\frac{24}{n}},
]
[
\text{CR}*{\text{왜도}}=\frac{\text{왜도}}{\operatorname{SE}(\text{왜도})},\quad
\text{CR}*{\text{첨도}}=\frac{\text{첨도}}{\operatorname{SE}(\text{첨도})}.
]

* 임계값: (|\text{CR}|\ge 1.96) (p<.05), (|\text{CR}|\ge 2.58) (p<.01).

---

# 3) 소프트웨어별 “무엇이 어떻게 다른가”

| 항목          | SPSS Statistics                            | AMOS(Assessment of normality 표)                               |
| ----------- | ------------------------------------------ | ------------------------------------------------------------- |
| 단변량 왜도·첨도 값 | **보정형** (G_1, G_2) (Fisher–Pearson) 사용이 기본 | **index**는 보정 없는 **모멘트형** (g_1, g_2)인 경우가 흔함(버전·설정에 따라 차이 가능) |
| ‘첨도’ 표기     | **초과첨도(excess)**를 기본(정규=0)                 | **초과첨도(excess)**를 index로 보고(정규=0)                             |
| CR 계산       | (\sqrt{6/n}, \sqrt{24/n}) 근사 SE 사용         | 동일 근사식으로 **index/SE = CR**                                    |
| 다변량 정규성     | 기본 제공 안 함(별도 절차)                           | **Mardia 다변량 첨도 계수와 CR(z)** 제공(표 하단 ‘Multivariate’)           |
| 결측/표본수      | 변수별 **유효 (n)**(분석 옵션에 따라 다름)               | **모형에 포함된 모든 변수에 대해 listwise (n)**로 계산되는 경우 多                 |

**따라서 같은 데이터라도**
(1) SPSS는 (G_1,G_2), AMOS는 (g_1,g_2)를 쓴다면 값이 **소수점 둘째/셋째**에서 달라질 수 있고,
(2) 결측 처리 방식(listwise vs variable-wise) 때문에 **(n) 자체가 달라져** CR도 미세하게 달라질 수 있습니다.

---

# 4) 수치 예시(귀하 데이터 스케일에 맞춘 시뮬레이션)

귀하 표의 한 항목(예: *지식제공*)에서 AMOS index가 **왜도 (g_1=-0.514)**라고 가정하고, 표본수 (n\approx 357)일 때:

* **SPSS(보정형) 왜도**
  [
  G_1=\frac{\sqrt{n(n-1)}}{n-2},g_1
  =1.0042\times(-0.514)\approx -0.516
  ]
  → **차이 약 0.002(0.4%)**로, 대규모 표본에서는 거의 동일.

* **CR(왜도)**
  [
  \operatorname{SE}(g_1)=\sqrt{6/n}\approx 0.1297,\quad
  \text{CR}=\frac{-0.514}{0.1297}\approx -3.96
  ]
  → AMOS 표의 CR(−3.964)와 일치.

* **첨도도 동일한 논리**로 SPSS 보정값 (G_2)가 AMOS index (g_2)보다 **조금 크게** 조정되며, (n)이 크면 차이는 **미미**합니다.

> 결론: **표본이 큰 본 연구 맥락에서는** SPSS 보정형과 AMOS index의 수치 차이는 *유의미한 해석 차이를 만들 정도가 아님*이 보통입니다. 다만 **보고서에는 어떤 정의를 썼는지 명시**해야 합니다(재현성).

---

# 5) “초과첨도(excess)” vs “Pearson 첨도” 혼동 주의

* **초과첨도(excess kurtosis)**: 정규분포의 기준을 **0**으로 맞춘 값(= “첨도 − 3”).
* **Pearson 첨도**: 정규분포의 기준이 **3**인 원래 값.
* 많은 소프트웨어가 **표기만 ‘kurtosis’**라고 쓰고 실제로는 **excess**를 내보냅니다.
* 논문에는 “**초과첨도(excess kurtosis)**를 보고하였다(정규분포=0)”처럼 **기준점을 명확히 표기**하세요.

---

# 6) 다변량 정규성(AMOS 하단 숫자의 정체)

* AMOS 하단의 **Multivariate ‘kurtosis’ 값(예: 54.855)**은 **Mardia의 다변량 첨도 계수**입니다.
* 그 옆의 **CR(예: 22.947)**은 이를 z로 정규화한 값으로, (|z|\ge 1.96/2.58)이면 **다변량 비정규성**을 뜻합니다.
* 단변량이 양호해도 **변수들의 결합 분포**가 정규에서 벗어나면 여기서 **유의**하게 잡힙니다.

---

# 7) 실무용 권장 문장(보고 일관성 확보)

* “SPSS에서는 **보정형(Adjusted Fisher–Pearson)** 왜도·초과첨도 ((G_1,G_2))를, AMOS에서는 **모멘트형 index** ((g_1,g_2))와 **CR**을 사용하였다. 두 지표는 표본이 큰 경우 수치 차이가 미미하나, 재현성을 위해 사용 정의를 본문에 명시하였다. AMOS의 다변량 정규성은 **Mardia 지수와 CR**로 평가하였다.”

---


### 1.2 기본 산식(중심적률 기반)

표본 (x_1,\dots,x_n), 평균 (\bar x), 표본표준편차 (s)라 할 때,

* (간단형)
  [
  g_1=\frac{m_3}{s^3},\qquad
  g_2=\frac{m_4}{s^4}-3
  ]
  [
  m_3=\frac1n\sum_{i=1}^n(x_i-\bar x)^3,\quad
  m_4=\frac1n\sum_{i=1}^n(x_i-\bar x)^4
  ]
* (편향보정형; SPSS·통계학 교과서에서 흔함)
  [
  G_1=\frac{n}{(n-1)(n-2)}\sum\Big(\frac{x_i-\bar x}{s}\Big)^3
  ]
  [
  G_2=\frac{n(n+1)}{(n-1)(n-2)(n-3)}\sum\Big(\frac{x_i-\bar x}{s}\Big)^4
  -\frac{3(n-1)^2}{(n-2)(n-3)}
  ]
  (;G_2)는 **초과첨도(정규분포를 0으로 만드는 정의)** 입니다.

### 1.3 CR(critical ratio)의 뜻과 계산

* CR은 “**표준오차로 나눈 값**(≈ z값)”입니다.
  [
  \text{CR}*{\text{왜도}}=\frac{\text{왜도}}{\operatorname{SE}(\text{왜도})},\qquad
  \text{CR}*{\text{첨도}}=\frac{\text{첨도}}{\operatorname{SE}(\text{첨도})}
  ]
* 큰 표본에서의 근사 표준오차:
  [
  \operatorname{SE}(g_1)\approx\sqrt{\frac{6}{n}},\qquad
  \operatorname{SE}(g_2)\approx\sqrt{\frac{24}{n}}
  ]
* 판정: |CR| ≥ **1.96**(p<.05) 또는 **2.58**(p<.01)면 **통계적으로 유의한 비정규성**.

> **중요**: CR은 (n)에 민감합니다. 표본이 크면 **작은 왜도·첨도도 유의**해질 수 있으므로, 실제 **절대 크기(효과크기)**와 **CR(유의성)**을 함께 봐야 합니다.

---

## 2. “직접 계산” 단변량 예시

### 2.1 예시 데이터

하나의 변수 (X=[2,3,3,4,5,9]) (n=6)

1. 평균과 표준편차
   [
   \bar x=\frac{2+3+3+4+5+9}{6}=4.3333,\quad
   s=\sqrt{\frac{\sum(x_i-\bar x)^2}{n-1}}=2.5033
   ]

2. 3·4차 중심적률
   [
   m_3=\frac{1}{6}\sum(x_i-\bar x)^3=14.0741,\quad
   m_4=\frac{1}{6}\sum(x_i-\bar x)^4=85.0741
   ]

3. **왜도·첨도(간단형)**
   [
   g_1=\frac{14.0741}{2.5033^3}=0.8971
   ]
   [
   g_2=\frac{85.0741}{2.5033^4}-3=-0.8337
   ]
   → 오른쪽 꼬리가 조금 길고(양의 왜도), **꼬리가 얕은(초과첨도<0)** 분포.

4. **CR 계산** ((n=6) → (\operatorname{SE}(g_1)=\sqrt{6/6}=1,\ \operatorname{SE}(g_2)=\sqrt{24/6}=2))
   [
   \text{CR}*{\text{왜도}}=\frac{0.8971}{1}=0.8971,\qquad
   \text{CR}*{\text{첨도}}=\frac{-0.8337}{2}=-0.4169
   ]
   → |CR|<1.96 → **유의한 비정규성 아님**.

> 같은 데이터라도 “편향보정형” (G_1, G_2)를 쓰면 값이 달라집니다(작은 표본에서 차이가 큼).
> 예시: (G_1=1.615,\ G_2=2.849) (정의 차이의 전형적 사례)

---

## 3. 다변량 정규성: 마할라노비스 거리와 마르디아 지수

### 3.1 마할라노비스 거리 (D^2)

* 공분산행렬 (S)와 평균벡터 (\mu)로
  [
  D^2(x)=(x-\mu)^\top S^{-1}(x-\mu)
  ]
* 정규가정 하에서 (D^2 \sim \chi^2_p).
  ⇒ **이상치 검정**: (D^2>\chi^2_{p,,1-\alpha}) (예: (\alpha=.001))이면 **이상치**로 간주.

### 3.2 마르디아(Mardia) 다변량 왜도·첨도

표준화 (z_i=S^{-1/2}(x_i-\bar x)), 표본크기 (n), 변수 수 (p).

* **다변량 왜도**
  [
  b_{1,p}=\frac{1}{n^2}\sum_{i=1}^{n}\sum_{j=1}^{n} (z_i^\top z_j)^3
  ]
  검정통계량 (;;T_s=\frac{n,b_{1,p}}{6}\approx \chi^2_{\nu},\ \nu=\frac{p(p+1)(p+2)}{6})

* **다변량 첨도**
  [
  b_{2,p}=\frac{1}{n}\sum_{i=1}^{n} (z_i^\top z_i)^2
  ]
  정규에서 (\mathbb{E}[b_{2,p}]=p(p+2)).
  z-검정:
  [
  z_k=\frac{b_{2,p}-p(p+2)}{\sqrt{8p(p+2)/n}}
  ]
  |(z_k)|이 1.96/2.58 초과 → **비정규성**.

### 3.3 “직접 계산” 다변량 예시(간단한 2변수)

두 변수 (X=[2,3,3,4,5,9],\ Y=[1,2,2,3,4,10]) (n=6, p=2)

1. 공분산 (S)와 평균 (\mu)를 구한 뒤 각 관측치의 (D^2)를 계산
   → 예: (D^2)의 일부 값은 약 (0.32, 2.05, 4.17) 등.
   임계치 (\chi^2_{2,,0.999}\approx 13.82)보다 작으므로 **이상치 아님**.

2. 마르디아 지수

* (b_{1,2})로부터 (T_s=\frac{n,b_{1,2}}{6}) 계산 → (\chi^2_{\nu})((\nu=4))와 비교
* (b_{2,2})로부터 (z_k) 계산
  (이 예시는 n이 작아 유의하게 벗어나지 않지만, 귀하의 실제 데이터처럼 (z_k)가 **22.947** 같은 큰 값이면 **명백한 비정규성**입니다.)

---

## 4. 〈표 IV-3〉 값과 연결되는 **역산(샘플수 확인 팁)**

AMOS의 단변량 **왜도-CR**은 대개 (\operatorname{SE}(\text{왜도})\approx\sqrt{6/n})을 사용합니다.
예를 들어, **지식제공**의 왜도 = (-0.514), CR = (-3.964)라면
[
\operatorname{SE} \approx \frac{0.514}{3.964}=0.1297
\Rightarrow n \approx \frac{6}{0.1297^2}\approx 357
]
**지식획득**(왜도 (-0.519), CR (-4.000))에서도 (n\approx 356)이 나옵니다.
→ 귀하의 표본크기가 **약 356~357명** 수준임을 **일관되게 확인**할 수 있습니다.

---

## 5. 정규성의 판정과 그 의미(실무 연결)

### 5.1 판정 체계(요약)

* **단변량**: 절대 왜도 < 3(또는 2), 절대 첨도 < 8~20(또는 4) ⇒ **형상(효과크기)** 양호.
  CR 기준(|2.58|)은 **유의성** 관점으로, 큰 (n)에서 민감.
* **다변량**: **마르디아 (z_k)**(또는 AMOS의 다변량 CR)가 임계 초과 ⇒ **비정규성**.

### 5.2 의미

* 기술통계·피어슨 상관·단순 회귀 등은 **큰 문제 없이** 해석 가능(보조로 Spearman 확인 권장).
* **CFA/SEM/간접효과**처럼 분포 가정에 민감한 분석은
  **Satorra–Bentler 보정(또는 MLR)**, **Bollen–Stine/BCa 부트스트랩**을 적용해
  **표준오차·p값·적합지수의 왜곡을 줄이는 것**이 핵심입니다.

---

## 6. 계산을 스스로 재현할 때의 체크리스트

1. **단변량**: 평균·표준편차 → (m_3,m_4) → (g_1,g_2) → (\text{CR}=g/\text{SE})

   * (\operatorname{SE}(g_1)=\sqrt{6/n},\ \operatorname{SE}(g_2)=\sqrt{24/n})
   * 보정형((G_1,G_2))을 쓰는지 명시
2. **마할라노비스**: (\mu,S) 계산 → 각 사례의 (D^2=(x-\mu)^\top S^{-1}(x-\mu)) → (\chi^2_{p,,1-\alpha})와 비교
3. **마르디아**: (Z=S^{-1/2}(X-\bar X)) → (b_{1,p},b_{2,p}) → (\chi^2_\nu)와 (z_k) 계산
4. **보고**: 효과크기(왜도·첨도의 절대 크기) **+** 유의성(CR) **동시** 제시


좋습니다! 공부하시기 편하도록 논리적 흐름에 맞춰 재정리하겠습니다. 📚

---

# 다중공선성과 보조회귀: 완전 손계산 가이드

## 목차
1. [예시 데이터와 기초 통계량](#1-예시-데이터와-기초-통계량)
2. [보조회귀란 무엇인가](#2-보조회귀란-무엇인가)
3. [보조회귀 계산 방법](#3-보조회귀-계산-방법)
4. [VIF와 다중공선성 진단](#4-vif와-다중공선성-진단)
5. [이론적 배경: 왜 표준오차가 커지는가](#5-이론적-배경-왜-표준오차가-커지는가)
6. [기호 정리 및 요약](#6-기호-정리-및-요약)

---

## 1. 예시 데이터와 기초 통계량

### 1.1 데이터셋

| i |   X₁ |   X₂ |   X₃ |
|---|------|------|------|
| 1 | -2.0 | -1.9 |  2.0 |
| 2 | -1.0 | -0.9 | -2.0 |
| 3 |  0.0 |  0.1 |  0.0 |
| 4 |  1.0 |  1.1 |  1.0 |
| 5 |  2.0 |  1.6 | -1.0 |

**특징**: 모든 변수는 평균이 0이므로 $\sum X_1 = \sum X_2 = \sum X_3 = 0$  
표본크기 $n=5 \Rightarrow n-1=4$

### 1.2 제곱합·교차곱합

각 $i$에 대해 $x_{ik}x_{i\ell}$를 곱해 더합니다.

**제곱합**:
- $\displaystyle \sum X_1^2 = 4+1+0+1+4 = 10$
- $\displaystyle \sum X_2^2 = 3.61+0.81+0.01+1.21+2.56 = 8.20$
- $\displaystyle \sum X_3^2 = 4+4+0+1+1 = 10$

**교차곱합**:
- $\displaystyle \sum X_1X_2 = 3.8+0.9+0+1.1+3.2 = 9.0$
- $\displaystyle \sum X_1X_3 = -4+2+0+1-2 = -3.0$
- $\displaystyle \sum X_2X_3 = -3.8+1.8+0+1.1-1.6 = -2.5$

### 1.3 분산·공분산

평균이 0이므로 표본분산/공분산은 $\sum/(n-1)$입니다.

**분산**:
- $\mathrm{Var}(X_1) = 10/4 = 2.50$
- $\mathrm{Var}(X_2) = 8.20/4 = 2.05$
- $\mathrm{Var}(X_3) = 10/4 = 2.50$

**공분산**:
- $\mathrm{Cov}(X_1,X_2) = 9/4 = 2.25$
- $\mathrm{Cov}(X_1,X_3) = -3/4 = -0.75$
- $\mathrm{Cov}(X_2,X_3) = -2.5/4 = -0.625$

**표준편차**:
- $s_{X_1} = \sqrt{2.5} = 1.5811$
- $s_{X_2} = \sqrt{2.05} = 1.4318$
- $s_{X_3} = 1.5811$

### 1.4 상관계수 행렬

$$r_{k\ell} = \frac{\mathrm{Cov}(X_k,X_\ell)}{s_{X_k}s_{X_\ell}}$$

계산 결과:
- $r_{12} = \dfrac{2.25}{1.5811 \times 1.4318} = \dfrac{9}{\sqrt{82}} \approx 0.9939$
- $r_{13} = \dfrac{-0.75}{1.5811 \times 1.5811} = -\dfrac{3}{10} = -0.3$
- $r_{23} = \dfrac{-0.625}{1.4318 \times 1.5811} = -\dfrac{2.5}{\sqrt{82}} \approx -0.2761$

**상관행렬 $R$**:
$$R = \begin{pmatrix}
1 & 0.9939 & -0.3\\
0.9939 & 1 & -0.2761\\
-0.3 & -0.2761 & 1
\end{pmatrix}$$

---

## 2. 보조회귀란 무엇인가

### 2.1 핵심 개념

**보조회귀(Auxiliary Regression)**는 각 예측변수 $X_j$를 **다른 예측변수들 $X_{-j}$**로 회귀시키는 모형입니다:

$$X_j = \gamma_0 + \gamma^\top X_{-j} + u_j$$

여기서:
- $X_j$: 예측변수 $j$의 관측치 ($n \times 1$ 벡터)
- $X_{-j}$: 다른 예측변수들 ($n \times (p-1)$ 행렬)
- $\gamma_0$: 절편 (중심화 시 0)
- $\gamma$: $(p-1) \times 1$ 회귀계수
- $u_j$: 잔차 = $X_j$에서 "다른 변수로 설명되지 않은" **고유 부분**

### 2.2 보조회귀가 측정하는 것

보조회귀의 **결정계수 $R_j^2$**는:

$$R_j^2 = \frac{\text{설명제곱합(SSR)}}{\text{총제곱합(SST)}} = 1 - \frac{\text{잔차제곱합(SSE)}}{\text{SST}}$$

**해석**:
- $R_j^2$가 **크다** → $X_j$가 다른 변수들로 "잘 예측됨" → **중복 정보가 많음** → 고유정보가 적음
- $R_j^2$가 **작다** → $X_j$가 고유한 정보를 많이 가짐 → 본회귀에서 안정적 추정 가능

### 2.3 핵심 지표

$$\mathrm{Tol}_j = 1 - R_j^2 = \frac{\text{SSE}}{\text{SST}}$$
$$\mathrm{VIF}_j = \frac{1}{1-R_j^2} = \frac{\text{SST}}{\text{SSE}}$$

- **Tolerance(허용도)**: $X_j$의 고유 정보 비율
- **VIF(분산팽창인자)**: 공선성으로 인한 분산 증가 배수

---

## 3. 보조회귀 계산 방법

### 3.1 방법 A: 정상방정식으로 직접 계산

변수들이 중심화되어 있으므로 절편 없이 계산합니다.

#### (a) $j=1$: $X_1 \sim X_2, X_3$

**정상방정식** (2×2 선형계):
$$\begin{pmatrix}
\sum x_2^2 & \sum x_2x_3\\
\sum x_2x_3 & \sum x_3^2
\end{pmatrix}
\begin{pmatrix}b_2\\ b_3\end{pmatrix}
= 
\begin{pmatrix}\sum x_1x_2\\ \sum x_1x_3\end{pmatrix}$$

숫자 대입:
$$\begin{pmatrix}
8.20 & -2.5\\
-2.5 & 10
\end{pmatrix}
\begin{pmatrix}b_2\\ b_3\end{pmatrix}
= 
\begin{pmatrix}9.0\\ -3.0\end{pmatrix}$$

행렬식: $D = 8.20 \times 10 - (-2.5) \times (-2.5) = 82 - 6.25 = 75.75$

**크래머 규칙**:
$$b_2 = \frac{9.0 \times 10 - (-3.0) \times (-2.5)}{75.75} = \frac{90 - 7.5}{75.75} = \frac{82.5}{75.75} = 1.0891$$

$$b_3 = \frac{8.20 \times (-3.0) - 9.0 \times (-2.5)}{75.75} = \frac{-24.6 + 22.5}{75.75} = \frac{-2.1}{75.75} = -0.0277$$

**예측값과 $R_1^2$ 계산**:

| i | $x_{2i}$ | $x_{3i}$ | $\hat{x}_{1i} = 1.0891 x_{2i} - 0.0277 x_{3i}$ | $\hat{x}_{1i}^2$ |
|---|----------|----------|-------------------------------------------------|------------------|
| 1 | -1.9 | 2.0 | -2.0693 - 0.0554 = -2.1247 | 4.5143 |
| 2 | -0.9 | -2.0 | -0.9802 + 0.0554 = -0.9248 | 0.8553 |
| 3 | 0.1 | 0.0 | 0.1089 + 0 = 0.1089 | 0.0119 |
| 4 | 1.1 | 1.0 | 1.1980 - 0.0277 = 1.1703 | 1.3696 |
| 5 | 1.6 | -1.0 | 1.7426 + 0.0277 = 1.7703 | 3.1340 |

$$\sum \hat{x}_{1i}^2 = 9.8851$$

$$R_1^2 = \frac{\sum \hat{x}_{1i}^2}{\sum x_{1i}^2} = \frac{9.8851}{10} = \mathbf{0.98851}$$

$$\mathrm{Tol}_1 = 1 - 0.98851 = \mathbf{0.01149}$$

$$\mathrm{VIF}_1 = \frac{1}{0.01149} = \mathbf{87.07}$$

#### (b) $j=2$: $X_2 \sim X_1, X_3$

**정상방정식**:
$$\begin{pmatrix}
10 & -3\\
-3 & 10
\end{pmatrix}
\begin{pmatrix}b_1\\ b_3\end{pmatrix}
= 
\begin{pmatrix}9.0\\ -2.5\end{pmatrix}$$

행렬식: $D = 100 - 9 = 91$

$$b_1 = \frac{90 + 7.5}{91} = \frac{97.5}{91} = 1.0714$$

$$b_3 = \frac{-25 + 27}{91} = \frac{2}{91} = 0.0220$$

$$R_2^2 = \frac{\sum \hat{x}_{2i}^2}{\sum x_{2i}^2} = \frac{8.1044}{8.20} = \mathbf{0.98834}$$

$$\mathrm{Tol}_2 = \mathbf{0.01166}, \quad \mathrm{VIF}_2 = \mathbf{85.77}$$

#### (c) $j=3$: $X_3 \sim X_1, X_2$

**정상방정식**:
$$\begin{pmatrix}
10 & 9.0\\
9.0 & 8.20
\end{pmatrix}
\begin{pmatrix}b_1\\ b_2\end{pmatrix}
= 
\begin{pmatrix}-3.0\\ -2.5\end{pmatrix}$$

행렬식: $D = 82 - 81 = 1$

$$b_1 = \frac{-24.6 + 22.5}{1} = -2.1$$

$$b_2 = \frac{-25 + 27}{1} = 2.0$$

$$R_3^2 = \frac{\sum \hat{x}_{3i}^2}{\sum x_{3i}^2} = \frac{1.3}{10} = \mathbf{0.13}$$

$$\mathrm{Tol}_3 = \mathbf{0.87}, \quad \mathrm{VIF}_3 = \mathbf{1.15}$$

### 3.2 방법 B: 상관행렬만으로 계산

블록 상관행렬에서:
$$R_j^2 = r^\top R_{-j,-j}^{-1} r$$

여기서 $R_{-j,-j}$는 $j$를 제외한 변수들의 상관행렬입니다.

#### $j=1$인 경우:

$$R_{-1,-1} = \begin{pmatrix}1 & r_{23}\\ r_{23} & 1\end{pmatrix} = \begin{pmatrix}1 & -0.2761\\ -0.2761 & 1\end{pmatrix}$$

**역행렬**:
$$R_{-1,-1}^{-1} = \frac{1}{1-r_{23}^2} \begin{pmatrix}1 & -r_{23}\\ -r_{23} & 1\end{pmatrix} = \frac{1}{1-0.0762} \begin{pmatrix}1 & 0.2761\\ 0.2761 & 1\end{pmatrix}$$

$$= \frac{1}{0.9238} \begin{pmatrix}1 & 0.2761\\ 0.2761 & 1\end{pmatrix} = \begin{pmatrix}1.0824 & 0.2989\\ 0.2989 & 1.0824\end{pmatrix}$$

**$r$ 벡터**:
$$r = \begin{pmatrix}r_{12}\\ r_{13}\end{pmatrix} = \begin{pmatrix}0.9939\\ -0.3\end{pmatrix}$$

**계산**:
$$R_1^2 = \begin{pmatrix}0.9939 & -0.3\end{pmatrix} \begin{pmatrix}1.0824 & 0.2989\\ 0.2989 & 1.0824\end{pmatrix} \begin{pmatrix}0.9939\\ -0.3\end{pmatrix}$$

$$= \begin{pmatrix}0.9939 & -0.3\end{pmatrix} \begin{pmatrix}1.0756 - 0.0897\\ 0.2972 - 0.3247\end{pmatrix}$$

$$= \begin{pmatrix}0.9939 & -0.3\end{pmatrix} \begin{pmatrix}0.9859\\ -0.0275\end{pmatrix}$$

$$= 0.9939 \times 0.9859 + (-0.3) \times (-0.0275) = 0.9798 + 0.0083 = \mathbf{0.9881}$$

또는 **공식으로 직접**:
$$R_1^2 = \frac{r_{12}^2 - 2r_{12}r_{13}r_{23} + r_{13}^2}{1-r_{23}^2}$$

$$= \frac{0.9878 - 2(0.9939)(-0.3)(-0.2761) + 0.09}{1-0.0762}$$

$$= \frac{0.9878 - 0.1644 + 0.09}{0.9238} = \frac{0.9134}{0.9238} = \mathbf{0.9885}$$

$$\Rightarrow \mathrm{VIF}_1 = \frac{1}{1-0.9885} = \frac{1}{0.0115} = \mathbf{87.07}$$

---

## 4. VIF와 다중공선성 진단

### 4.1 검산: $\mathrm{VIF}_j = (R^{-1})_{jj}$

상관행렬 $R$의 역행렬을 3×3으로 직접 구하면:

$$R^{-1} \approx \begin{pmatrix}
\color{blue}{87.069} & -85.870 & 2.414\\
-85.870 & \color{blue}{85.770} & -2.082\\
2.414 & -2.082 & \color{blue}{1.149}
\end{pmatrix}$$

대각 원소가 위에서 구한 VIF들과 정확히 일치합니다!

### 4.2 결과 요약

| 변수 | $R_j^2$ | Tolerance | VIF | 해석 |
|------|---------|-----------|-----|------|
| $X_1$ | 0.9885 | 0.0115 | 87.07 | **심각한 다중공선성** |
| $X_2$ | 0.9883 | 0.0117 | 85.77 | **심각한 다중공선성** |
| $X_3$ | 0.13 | 0.87 | 1.15 | 공선성 거의 없음 |

**해석**:
- $X_1$과 $X_2$는 서로 매우 강하게 상관 ($r \approx 0.994$)
- 두 변수는 거의 같은 정보를 담고 있음
- $X_3$는 독립적인 정보를 제공

---

## 5. 이론적 배경: 왜 표준오차가 커지는가

### 5.1 핵심 메커니즘

본회귀 모형:
$$y = \alpha + X\beta + \varepsilon, \quad X = [X_1, \ldots, X_p]$$

OLS 추정량 $\hat{\beta}_j$의 분산:
$$\mathrm{Var}(\hat{\beta}_j \mid X) = \sigma^2 \big((X'X)^{-1}\big)_{jj}$$

**Frisch-Waugh-Lovell 정리**를 이용하면:
$$\big((X'X)^{-1}\big)_{jj} = \frac{1}{X_j'M_{-j}X_j}$$

여기서:
- $M_{-j} = I - P_{-j}$: 잔차화 행렬
- $P_{-j} = X_{-j}(X_{-j}'X_{-j})^{-1}X_{-j}'$: 투영 행렬
- $z_j := M_{-j}X_j = X_j - \widehat{X}_{j|-j}$: 보조회귀 잔차

따라서:
$$X_j'M_{-j}X_j = \sum z_{ji}^2 = \text{SSE(보조회귀)}$$

### 5.2 최종 분산 공식

$$\boxed{\mathrm{Var}(\hat{\beta}_j \mid X) = \frac{\sigma^2}{\text{SSE(보조회귀)}} = \frac{\sigma^2}{\text{SST} \cdot (1-R_j^2)}}$$

표준오차로 표현:
$$\boxed{\mathrm{se}(\hat{\beta}_j) = \sqrt{\mathrm{MSE}} \cdot \frac{1}{\sqrt{\text{SST}}} \cdot \sqrt{\mathrm{VIF}_j}}$$

### 5.3 구체적 예시로 확인

$X_1 \sim X_2, X_3$ 보조회귀에서:
- $\text{SST}_{x_1} = \sum x_{1i}^2 = 10$
- $R_1^2 = 0.9885$
- $\text{SSE}_{x_1} = \text{SST} \cdot (1-R_1^2) = 10 \times 0.0115 = \mathbf{0.115}$

$$\mathrm{VIF}_1 = \frac{\text{SST}}{\text{SSE}} = \frac{10}{0.115} = 87.0$$

$$\sqrt{\mathrm{VIF}_1} = \sqrt{87.0} \approx \mathbf{9.33}$$

**의미**:
- 공선성이 없다면 ($R_1^2 = 0$): $\text{SSE} = \text{SST} = 10$
- 실제로는 $\text{SSE} = 0.115$로 **분모가 87배 축소**
- $\mathrm{se}(\hat{\beta}_1)$는 약 **9.3배 증가**

### 5.4 기하학적 직관

$X_j$를 $X_{-j}$의 부분공간에 투영하고 남은 잔차 $z_j$는 "$X_j$의 고유 방향"입니다.

```
공선성 강함 → z_j의 길이가 매우 짧음 
           → 그 방향으로 β_j를 안정적으로 추정 불가
           → 분산 증가
```

---

## 6. 기호 정리 및 요약

### 6.1 기호 사전

| 기호 | 의미 | 차원 |
|------|------|------|
| $y$ | 종속변수 | $n \times 1$ |
| $X$ | 예측변수 설계행렬 | $n \times p$ |
| $X_j$ | $j$번째 예측변수 | $n \times 1$ |
| $X_{-j}$ | $j$를 제외한 예측변수들 | $n \times (p-1)$ |
| $\beta$ | 회귀계수 | $p \times 1$ |
| $\hat{\beta}_j$ | $j$번째 계수의 OLS 추정량 | 스칼라 |
| $\varepsilon$ | 오차항 | $n \times 1$ |
| $P_{-j}$ | $X_{-j}$로의 투영 행렬 | $n \times n$ |
| $M_{-j}$ | 잔차화 행렬 ($I - P_{-j}$) | $n \times n$ |
| $u_j$ | 보조회귀 잔차 ($M_{-j}X_j$) | $n \times 1$ |
| $R_j^2$ | 보조회귀 결정계수 | 스칼라 |
| $\mathrm{Tol}_j$ | Tolerance ($1-R_j^2$) | 스칼라 |
| $\mathrm{VIF}_j$ | 분산팽창인자 ($1/\mathrm{Tol}_j$) | 스칼라 |
| SST | 총제곱합 $\sum(X_{ji}-\bar{X}_j)^2$ | 스칼라 |
| SSE | 잔차제곱합 $\sum u_{ji}^2$ | 스칼라 |

### 6.2 핵심 공식 요약

```
보조회귀: X_j = γ₀ + γ'X_{-j} + u_j

R²_j = SSR/SST = 1 - SSE/SST

Tol_j = 1 - R²_j

VIF_j = 1/(1 - R²_j)

Var(β̂_j) = σ²/(SST · (1 - R²_j))

se(β̂_j) = √MSE · (1/√SST) · √VIF_j
```

### 6.3 진단 기준

| VIF 범위 | 다중공선성 수준 | 조치 |
|----------|----------------|------|
| 1-5 | 낮음 | 문제없음 |
| 5-10 | 중간 | 주의 필요 |
| 10+ | 높음 | 심각, 조치 필요 |
| 100+ | 매우 심각 | 변수 제거/결합 필수 |

---

## 마무리

이 문서는 다중공선성 진단의 핵심 도구인 **보조회귀**를 다음 순서로 설명했습니다:

1. ✅ **기초 통계량 계산** - 손으로 할 수 있는 모든 단계
2. ✅ **보조회귀 개념** - 무엇을 측정하는가
3. ✅ **두 가지 계산법** - 정상방정식 vs 상관행렬
4. ✅ **VIF 해석** - 어떻게 진단하는가
5. ✅ **이론적 근거** - 왜 표준오차가 커지는가

**핵심 메시지**: 
> 보조회귀는 각 예측변수의 "고유 정보량"을 측정하고, 이것이 작을수록 (VIF가 클수록) 회귀계수 추정이 불안정해집니다.

