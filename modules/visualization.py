import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64
from . import data_processing

sns.set_theme(style="whitegrid")


def plot_statistics(data):
    """평균, 분산, 상관관계 그래프를 그려 base64 이미지로 반환"""
    fig, axs = plt.subplots(1, 3, figsize=(12, 4))
    axs[0].bar(data.index, data['x'])
    axs[0].set_title('평균')
    axs[0].axhline(data['x'].mean(), color='red', linestyle='--')

    axs[1].hist(data['x'], bins=10, color='skyblue')
    axs[1].set_title('분산')
    axs[1].axvline(data['x'].var(), color='red', linestyle='--')

    sns.scatterplot(x='x', y='y', data=data, ax=axs[2])
    axs[2].set_title('상관관계')

    buf = BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('utf8')


def plot_iris_example(df=None):
    """Iris 데이터셋을 활용한 기본 통계 그래프"""
    if df is None:
        df = data_processing.load_public_dataset()

    fig, axs = plt.subplots(1, 2, figsize=(10, 4))
    sns.histplot(df['sepal_length'], kde=True, ax=axs[0])
    axs[0].set_title('꽃받침 길이 분포')

    sns.scatterplot(x='sepal_length', y='petal_length', hue='species', data=df, ax=axs[1])
    axs[1].set_title('꽃받침 길이와 꽃잎 길이')

    buf = BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('utf8')

