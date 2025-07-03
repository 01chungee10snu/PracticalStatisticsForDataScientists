from flask import Flask, render_template
import markdown
import os
import re
from docs.docs_index import book_structure
from modules import data_processing


COLORS = {
    'setosa': 'rgba(255,99,132,0.6)',
    'versicolor': 'rgba(54,162,235,0.6)',
    'virginica': 'rgba(75,192,192,0.6)'
}

app = Flask(__name__)
THEME = os.getenv('BOOTSWATCH_THEME', 'cosmo')


def slugify(text):
    """단순 슬러그 생성"""
    return re.sub(r'[^a-zA-Z0-9]+', '-', text).strip('-').lower()


def load_markdown(path):
    """마크다운 파일을 읽어 HTML과 코드 블록을 반환"""
    with open(os.path.join('docs', path), 'r', encoding='utf-8') as f:
        text = f.read()
    code = ""
    if "```" in text:
        parts = text.split("```")
        if len(parts) >= 2:
            code = parts[1].strip()
    html = markdown.markdown(text, extensions=['fenced_code'])
    return html, code


@app.route('/')
def index():
    books = {}
    public_df = data_processing.load_public_dataset()
    feature_pairs = [
        ('sepal_length', 'sepal_width'),
        ('petal_length', 'petal_width'),
        ('sepal_length', 'petal_length'),
        ('sepal_width', 'petal_width'),
    ]

    pair_idx = 0
    for key, sections in book_structure.items():
        books[key] = []
        for sec in sections:
            html, code = load_markdown(sec['file'])
            x_col, y_col = feature_pairs[pair_idx % len(feature_pairs)]
            pair_idx += 1
            datasets = data_processing.prepare_scatter_datasets(
                public_df, x_col, y_col, COLORS
            )
            image_query = slugify(sec['title'])
            books[key].append({
                'title': sec['title'],
                'content': html,
                'code': code,
                'chart': datasets,
                'x': x_col,
                'y': y_col,
                'image_url': f"https://source.unsplash.com/featured/?{image_query}"
            })

    return render_template('index.html', books=books, theme=THEME)


if __name__ == '__main__':
    app.run(debug=True)

