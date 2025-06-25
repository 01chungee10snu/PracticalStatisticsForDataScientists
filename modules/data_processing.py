import pandas as pd
import seaborn as sns


def generate_statistics_data(size=50):
    """평균, 분산, 상관관계를 설명하기 위한 예제 데이터 생성"""
    rng = pd.Series(range(1, size + 1))
    data = pd.DataFrame({
        'x': rng,
        'y': rng.sample(frac=1, random_state=42).reset_index(drop=True)
    })
    return data


def load_public_dataset():
    """공개된 Iris 데이터셋을 로드"""
    return sns.load_dataset('iris')


def prepare_scatter_datasets(df, x_col, y_col, color_map):
    """주어진 컬럼 쌍으로 차트용 데이터셋을 준비"""
    datasets = []
    for species, group in df.groupby('species'):
        sample = group[[x_col, y_col]].rename(columns={x_col: 'x', y_col: 'y'})
        datasets.append({
            'label': species,
            'data': sample.to_dict(orient='records'),
            'backgroundColor': color_map.get(species, 'rgba(0,0,0,0.6)')
        })
    return datasets
