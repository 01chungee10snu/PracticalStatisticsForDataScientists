import pandas as pd
import seaborn as sns
import numpy as np
from sklearn.datasets import make_classification, make_regression
from sklearn.preprocessing import StandardScaler


def generate_statistics_data(size=50):
    """평균, 분산, 상관관계를 설명하기 위한 예제 데이터 생성"""
    rng = pd.Series(range(1, size + 1))
    data = pd.DataFrame({
        'x': rng,
        'y': rng.sample(frac=1, random_state=42).reset_index(drop=True)
    })
    return data


def generate_research_dataset(n_subjects=200, random_state=42):
    """연구 방법론 교육용 종합 데이터셋 생성"""
    np.random.seed(random_state)
    
    # 기본 인구통계 정보
    ages = np.random.normal(35, 12, n_subjects).astype(int)
    ages = np.clip(ages, 18, 80)
    
    gender = np.random.choice(['Male', 'Female'], n_subjects)
    education = np.random.choice(['High School', 'Bachelor', 'Master', 'PhD'], 
                               n_subjects, p=[0.3, 0.4, 0.2, 0.1])
    
    # 심리측정 변수 (요인분석용)
    # 5개 요인, 각각 3개 문항
    factor_data = np.random.multivariate_normal(
        mean=[0, 0, 0, 0, 0],
        cov=[[1, 0.3, 0.2, 0.1, 0.1],
             [0.3, 1, 0.1, 0.2, 0.1],
             [0.2, 0.1, 1, 0.1, 0.3],
             [0.1, 0.2, 0.1, 1, 0.2],
             [0.1, 0.1, 0.3, 0.2, 1]],
        size=n_subjects
    )
    
    # 리커트 척도로 변환 (1-7)
    items = {}
    for i in range(5):
        for j in range(3):
            item_name = f'Q{i+1}_{j+1}'
            items[item_name] = np.clip(
                np.round(factor_data[:, i] * 1.5 + 4), 1, 7
            ).astype(int)
    
    # 연속형 결과 변수
    performance = (
        0.3 * factor_data[:, 0] + 
        0.2 * factor_data[:, 1] + 
        0.1 * (ages - 35) / 12 +
        np.random.normal(0, 0.5, n_subjects)
    )
    
    # 범주형 결과 변수
    success_prob = 1 / (1 + np.exp(-performance))
    success = np.random.binomial(1, success_prob, n_subjects)
    
    # 그룹 변수 (실험 조건)
    group = np.random.choice(['Control', 'Treatment_A', 'Treatment_B'], 
                           n_subjects, p=[0.4, 0.3, 0.3])
    
    # 데이터프레임 생성
    data = pd.DataFrame({
        'subject_id': range(1, n_subjects + 1),
        'age': ages,
        'gender': gender,
        'education': education,
        'group': group,
        'performance_score': performance,
        'success': success,
        **items
    })
    
    return data


def generate_factor_analysis_data(n_subjects=300, n_factors=4, random_state=42):
    """요인분석 교육용 데이터셋 생성"""
    np.random.seed(random_state)
    
    # 요인 점수 생성
    factor_scores = np.random.multivariate_normal(
        mean=np.zeros(n_factors),
        cov=np.eye(n_factors),
        size=n_subjects
    )
    
    # 요인 로딩 행렬 (각 요인당 4개 문항)
    loadings = np.array([
        [0.8, 0.1, 0.1, 0.1],  # Factor 1 items
        [0.7, 0.2, 0.1, 0.1],
        [0.6, 0.1, 0.2, 0.1],
        [0.8, 0.1, 0.1, 0.2],
        [0.1, 0.8, 0.1, 0.1],  # Factor 2 items
        [0.2, 0.7, 0.1, 0.1],
        [0.1, 0.6, 0.2, 0.1],
        [0.1, 0.8, 0.1, 0.1],
        [0.1, 0.1, 0.8, 0.1],  # Factor 3 items
        [0.1, 0.2, 0.7, 0.1],
        [0.2, 0.1, 0.6, 0.1],
        [0.1, 0.1, 0.8, 0.2],
        [0.1, 0.1, 0.1, 0.8],  # Factor 4 items
        [0.1, 0.1, 0.2, 0.7],
        [0.1, 0.2, 0.1, 0.6],
        [0.2, 0.1, 0.1, 0.8],
    ])
    
    # 관찰 변수 생성
    observed_scores = factor_scores @ loadings.T
    
    # 오차 추가
    error = np.random.normal(0, 0.5, observed_scores.shape)
    observed_scores += error
    
    # 리커트 척도로 변환
    observed_scores = np.clip(
        np.round(observed_scores * 1.5 + 4), 1, 7
    ).astype(int)
    
    # 데이터프레임 생성
    item_names = [f'Item_{i+1:02d}' for i in range(16)]
    data = pd.DataFrame(observed_scores, columns=item_names)
    
    # 요인 정보 추가
    factor_info = pd.DataFrame(factor_scores, columns=[f'Factor_{i+1}' for i in range(n_factors)])
    
    return data, factor_info, loadings


def generate_ml_dataset(n_samples=1000, n_features=10, task='classification', random_state=42):
    """머신러닝 교육용 데이터셋 생성"""
    if task == 'classification':
        X, y = make_classification(
            n_samples=n_samples,
            n_features=n_features,
            n_informative=n_features//2,
            n_redundant=n_features//4,
            n_classes=3,
            random_state=random_state
        )
        target_names = ['Class_A', 'Class_B', 'Class_C']
        y = [target_names[i] for i in y]
    else:
        X, y = make_regression(
            n_samples=n_samples,
            n_features=n_features,
            noise=0.1,
            random_state=random_state
        )
    
    # 특성 이름 생성
    feature_names = [f'Feature_{i+1:02d}' for i in range(n_features)]
    
    # 데이터프레임 생성
    data = pd.DataFrame(X, columns=feature_names)
    data['target'] = y
    
    return data


def load_public_dataset():
    """공개된 Iris 데이터셋을 로드"""
    return sns.load_dataset('iris')


def sample_public_dataset(size=50):
    """Iris 데이터셋에서 일부 행을 무작위로 샘플링"""
    df = load_public_dataset()
    size = min(size, len(df))
    return df.sample(n=size, random_state=42).reset_index(drop=True)


def load_titanic_dataset():
    """Seaborn의 타이타닉 데이터셋 로드"""
    return sns.load_dataset('titanic')


def sample_titanic_dataset(size=50):
    """타이타닉 데이터셋에서 일부 행을 무작위로 샘플링"""
    df = load_titanic_dataset()
    size = min(size, len(df))
    return df.sample(n=size, random_state=42).reset_index(drop=True)


def prepare_scatter_datasets(df, x_col, y_col, color_map, group_col='species'):
    """주어진 컬럼 쌍으로 차트용 데이터셋을 준비"""
    datasets = []
    if group_col in df.columns:
        for group_name, group in df.groupby(group_col):
            sample = group[[x_col, y_col]].rename(columns={x_col: 'x', y_col: 'y'})
            datasets.append({
                'label': str(group_name),
                'data': sample.to_dict(orient='records'),
                'backgroundColor': color_map.get(group_name, 'rgba(0,0,0,0.6)')
            })
    else:
        # 그룹 컬럼이 없을 경우 전체 데이터 사용
        sample = df[[x_col, y_col]].rename(columns={x_col: 'x', y_col: 'y'})
        datasets.append({
            'label': 'Data',
            'data': sample.to_dict(orient='records'),
            'backgroundColor': 'rgba(54,162,235,0.6)'
        })
    return datasets


def get_unified_dataset(level='all', size=None):
    """모든 레벨에서 사용할 수 있는 통합 데이터셋 반환"""
    research_data = generate_research_dataset(n_subjects=200)
    
    if level == 'beginner':
        # 질적 연구용 - 인구통계와 그룹 정보 중심
        return research_data[['subject_id', 'age', 'gender', 'education', 'group', 'success']]
    
    elif level == 'intermediate':
        # 요인분석용 - 심리측정 문항들
        factor_cols = [col for col in research_data.columns if col.startswith('Q')]
        return research_data[['subject_id'] + factor_cols]
    
    elif level == 'advanced':
        # 머신러닝용 - 전체 데이터
        return research_data
    
    else:
        return research_data


def prepare_visualization_data(df, chart_type='scatter', x_col=None, y_col=None, group_col=None):
    """시각화를 위한 데이터 준비"""
    if chart_type == 'scatter':
        if x_col and y_col:
            return prepare_scatter_datasets(df, x_col, y_col, 
                                          {'Control': 'rgba(255,99,132,0.6)',
                                           'Treatment_A': 'rgba(54,162,235,0.6)',
                                           'Treatment_B': 'rgba(75,192,192,0.6)',
                                           'Male': 'rgba(255,159,64,0.6)',
                                           'Female': 'rgba(153,102,255,0.6)'},
                                          group_col or 'group')
    
    elif chart_type == 'histogram':
        if x_col:
            return {
                'data': df[x_col].tolist(),
                'labels': df[x_col].value_counts().index.tolist(),
                'counts': df[x_col].value_counts().tolist()
            }
    
    elif chart_type == 'correlation':
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        corr_matrix = df[numeric_cols].corr()
        return {
            'labels': corr_matrix.columns.tolist(),
            'data': corr_matrix.values.tolist()
        }
    
    return None
