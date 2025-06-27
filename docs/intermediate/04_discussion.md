이 장에서는 연구 결과의 함의와 한계를 정리합니다. 직접 요인 분석이 기존 통계 기법과 비교해 가지는 장점과 실용성을 논의하고, 데이터 규모와 요인 수 결정과 같은 향후 연구 과제를 제안합니다. 이러한 논의를 통해 이론적·실무적 적용 가능성을 폭넓게 모색합니다.

### 핵심 포인트
* 직접 요인 분석은 변수 수가 적을 때도 안정적인 결과를 제공합니다.
* 회전 방식의 선택이 요인 해석에 큰 영향을 미친다는 점을 강조합니다.
* 데이터가 크면 추정치가 안정적이지만 계산 비용이 증가합니다.

### 토론 주제
1. 기존 연구와 비교해 직접 요인 분석이 가지는 장점은 무엇인지 분석합니다.
2. 데이터 세트 규모에 따른 적용 한계를 사례별로 검토합니다.
3. 추가 실험 설계를 통해 보완할 수 있는 부분을 정리합니다.

## 실습 코드 예시
```python
from modules.data_processing import sample_public_dataset
from modules.visualization import plot_iris_example

data = sample_public_dataset(50)
img = plot_iris_example(data)
```


