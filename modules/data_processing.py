import pandas as pd


def generate_statistics_data(size=50):
    """평균, 분산, 상관관계를 설명하기 위한 예제 데이터 생성"""
    rng = pd.Series(range(1, size + 1))
    data = pd.DataFrame({
        'x': rng,
        'y': rng.sample(frac=1, random_state=42).reset_index(drop=True)
    })
    return data
