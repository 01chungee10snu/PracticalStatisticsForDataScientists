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

2. **빈도적(Frequentist)**
   $$P(A)=\lim_{n \to \infty}\frac{n_A}{n}$$

   * 시행을 무한히 반복했을 때의 비율

3. **주관적(Subjective)**

   * 사건에 대한 개인의 신념의 정도
   * 베이즈 통계(Bayesian Statistics)의 기반

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
| ![PMF 예시](https://upload.wikimedia.org/wikipedia/commons/1/1a/Binomial_distribution_pmf.svg) | ![PDF 예시](https://upload.wikimedia.org/wikipedia/commons/7/74/Normal_Distribution_PDF.svg) |

> 출처: Wikimedia Commons

---

## 2️⃣ 이산형 확률분포 (Discrete)

### (1) 베르누이분포 (Bernoulli)

$$
P(X=x)=p^x(1-p)^{1-x},\quad x\in{0,1}
$$

* **매개변수:** 성공확률 $p\in[0,1]$
* **기대값/분산:** $E[X]=p,;Var(X)=p(1-p)$
* **용례:** 단일 시도(성공/실패), 클릭 여부, 합격/불합격
* **시각:** ![Bernoulli PMF](https://upload.wikimedia.org/wikipedia/commons/f/fd/Bernoulli_pmf.svg)

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
* **시각:** ![Binomial PMF](https://upload.wikimedia.org/wikipedia/commons/1/1a/Binomial_distribution_pmf.svg)

> 💬 **기호 주석**
> $\binom{n}{k}=\dfrac{n!}{k!(n-k)!}$는 조합(순서 무시). $!$는 팩토리얼.

---

### (3) 포아송분포 (Poisson)

$$
P(X=k)=\frac{\lambda^k e^{-\lambda}}{k!},\quad k=0,1,2,\dots
$$

* **매개변수:** 평균발생률 $\lambda>0$
* **기대값/분산:** $E[X]=Var(X)=\lambda$
* **용례:** 단위 시간/공간의 드문 사건 발생 횟수(콜센터 콜, 웹 클릭 수, 돌연변이 수)
* **시각:** ![Poisson PMF](https://upload.wikimedia.org/wikipedia/commons/1/16/Poisson_pmf.svg)

> 💬 **이름 주석 – “포아송”**
> **시메옹 드니 포아송(S.-D. Poisson, 1781–1840)**: 확률·해석학 공헌. 드문 사건 근사 모델로 유명.

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
* **시각:** ![Uniform PDF](https://upload.wikimedia.org/wikipedia/commons/9/96/Uniform_distribution_PDF.svg)

---

### (2) 정규분포 (Normal, Gaussian)

$$
f(x)=\frac{1}{\sqrt{2\pi\sigma^2}}\exp!\Big(-\frac{(x-\mu)^2}{2\sigma^2}\Big)
$$

* **매개변수:** 평균 $\mu$, 표준편차 $\sigma>0$
* **기대값/분산:** $E[X]=\mu,;Var(X)=\sigma^2$
* **용례:** 키/점수/오차 등 자연·측정 현상, 중심극한정리의 한계분포
* **시각:** ![Normal PDF](https://upload.wikimedia.org/wikipedia/commons/7/74/Normal_Distribution_PDF.svg)

> 💬 **이름 주석 – “정규/가우스”**
> **아브라함 드 무아브르(Abraham de Moivre, 1667–1754)**가 초기 형태 연구,
> **카를 F. 가우스(Carl F. Gauss, 1777–1855)**가 오차이론으로 널리 보급. “가우시안(Gaussian)”이라 부르기도 함.

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

> 💬 **개념 주석 – “무기억성”**
> 과거 경과 시간과 무관하게 남은 시간이 같은 분포를 따르는 성질(지수·기하분포만 가짐).

---

### (4) 감마분포 (Gamma)

$$
f(x)=\frac{\lambda^k x^{k-1} e^{-\lambda x}}{\Gamma(k)},\quad x>0
$$

* **매개변수:** 모양 $k>0$, 비율 $\lambda>0$
* **기대값/분산:** $E[X]=\dfrac{k}{\lambda},;Var(X)=\dfrac{k}{\lambda^2}$
* **관계:** $k$개의 독립 지수($\lambda$) 합의 분포
* **용례:** 수명·신뢰성·보험 청구 간격
* **시각:** ![Gamma PDF](https://upload.wikimedia.org/wikipedia/commons/f/f3/Gamma_distribution_pdf.svg)

> 💬 **기호 주석 – $\Gamma(\cdot)$**
> 감마함수: $\Gamma(k)=\int_0^\infty t^{k-1}e^{-t},dt$, 정수 $n$에 대해 $\Gamma(n)=(n-1)!$.

---

### (5) 카이제곱분포 ($\chi^2$)

$$
\chi^2=\sum_{i=1}^{k}Z_i^2,\quad Z_i\sim N(0,1)\ \text{독립}
$$

* **매개변수:** 자유도 $k\in\mathbb{N}$
* **기대값/분산:** $E[X]=k,;Var(X)=2k$
* **용례:** 분산 추정, 적합도/독립성 검정의 검정통계량
* **시각:** ![Chi-square PDF](https://upload.wikimedia.org/wikipedia/commons/1/16/Chi-square_distribution_pdf.svg)

> 💬 **용어 주석 – 자유도(df)**
> 통계량이 자유롭게 변할 수 있는 **독립 정보의 수**. 표본제약(평균 등)으로 줄어듦.

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

> 💬 **이름 주석 – “Student”**
> **윌리엄 시얼리 고셋(William S. Gosset, 1876–1937)**이 **본명 대신 “Student”** 필명으로 발표(기네스 양조장 재직 당시 사내 규정 때문).

---

### (7) F분포 (Fisher–Snedecor)

$$
F=\frac{(X_1/d_1)}{(X_2/d_2)},\quad X_1\sim\chi^2_{d_1},\ X_2\sim\chi^2_{d_2}\ \text{독립}
$$

* **매개변수:** 자유도 $d_1,d_2\in\mathbb{N}$
* **용례:** 분산분석(ANOVA), 회귀 총체 적합도 검정(전체 $R^2$ 유의성)
* **시각:** ![F PDF](https://upload.wikimedia.org/wikipedia/commons/4/4d/F_distribution_pdf.svg)

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

![CLT in action](https://upload.wikimedia.org/wikipedia/commons/0/05/Clt_in_action.gif)

> 균등·왜도·이산 등 다양한 원 분포라도, **표본크기 $n$ 증가**에 따라
> **표본평균의 분포가 정규 형태로 수렴**하는 모습을 보여주는 GIF. ([위키미디어 공용판][3])

### (2) 주사위 합의 분포가 종모양으로 (이산 → 연속 근사)

![Dice sum CLT](https://upload.wikimedia.org/wikipedia/commons/2/2b/Dice_sum_central_limit_theorem.svg)

> 여러 개의 공정한 주사위를 던져 **합/평균**을 보면,
> $n$이 커질수록 **종(bell) 모양**에 가까워짐(정규 근사 향상). ([위키미디어 공용판][4])

### (3) 평균의 견고성 한계(반례 직관: 코시 분포)

![Mean estimator consistency – Cauchy](https://upload.wikimedia.org/wikipedia/commons/5/52/Mean_estimator_consistency.gif)

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

![Bootstrap Illustration](https://upload.wikimedia.org/wikipedia/commons/9/98/Illustration_bootstrap.svg)

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

