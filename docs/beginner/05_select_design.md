연구 설계는 사례 연구의 목표와 가용 자원에 따라 결정됩니다. 고유적 사례 연구는 특정 현상 자체를 깊이 있게 다루고, 도구적 사례 연구는 이론 개발을 위해 여러 사례를 비교합니다. 적절한 설계를 선택하면 데이터 수집과 분석 절차를 명확히 정리할 수 있습니다.

### 핵심 포인트
* 단일 사례와 다중 사례 설계의 장단점을 비교합니다.
* 실험적 접근보다는 맥락적 분석에 초점을 맞춥니다.
* 연구자 편향을 줄이기 위한 블라인드 절차를 고려합니다.

### 설계 선택 과정
1. 연구 목적에 부합하는 사례 수를 결정합니다.
2. 자료 수집 방법(관찰, 인터뷰, 문서 등)을 조합해 계획합니다.
3. 데이터 분석 전략을 미리 정의하여 결과 해석을 용이하게 합니다.

### 실무 노하우
* 설계 결정 전, 유사 연구의 방법론 장단점을 분석해 참고합니다.
* 예산과 인력 등 현실적 제약을 반영하여 자료 수집 범위를 조정합니다.

### 추가 학습 내용
* 연구 질문에 따라 사례 경계를 명확히 그리는 연습을 합니다.
* 비교 사례가 존재할 때 다중 사례 설계가 주는 이점을 분석합니다.
* 설계 변경이 필요할 경우 의사결정 기록을 남겨 추후 검토에 대비합니다.

### 논문 수준 보충
* 연구 설계 선택 시 사용 가능한 이론적 모델을 표로 정리합니다.
* 시간적 제약을 고려한 반복 측정 설계의 장단점을 논의합니다.
* 설계 타당성 평가를 위한 체크리스트를 작성해 활용합니다.

### 역사적 배경
* 다양한 사례 연구 설계는 20세기 중반 사회과학에서 분과별 연구 전통을 반영하여 발전했습니다.
## 실습 코드 예시
```python
from modules.data_processing import sample_public_dataset
import itertools

df = sample_public_dataset(5)
pairs = list(itertools.combinations(df.index, 2))
print('가능한 비교 쌍 수:', len(pairs))
```



### 추가 예시
- 실제 연구 사례를 간단히 요약하며 수집 절차를 설명합니다.
더 자세한 통합 요약은 [overview.md](../overview.md)에서 확인할 수 있습니다.

### 연습 문제
1. 단일 사례 연구와 다중 사례 연구의 목적 차이를 비교하세요.
2. 사례 연구 설계 시 블라인드 절차를 도입하는 이유를 서술하세요.
3. 자료 수집 방법을 조합할 때 고려해야 할 사항을 정리하세요.

[정답 보기](../answers.md)

[목차로 돌아가기](../overview.md)
