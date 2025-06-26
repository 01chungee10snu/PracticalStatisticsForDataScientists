from ipywidgets import interact, IntSlider
from IPython.display import display, HTML
from . import data_processing, visualization


def create_interactive_demo():
    """사용자가 입력한 데이터 크기에 따라 그래프를 업데이트"""

    def update(size):
        data = data_processing.sample_public_dataset(size)
        img = visualization.plot_iris_example(data)
        display(HTML(f'<img src="data:image/png;base64,{img}"/>'))

    interact(update, size=IntSlider(min=10, max=150, step=10, value=50))

