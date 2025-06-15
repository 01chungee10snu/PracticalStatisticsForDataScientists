from flask import Flask, render_template
import markdown
import os
from docs.docs_index import book_structure
from modules import data_processing, visualization

app = Flask(__name__)


def load_markdown(path):
    with open(os.path.join('docs', path), 'r', encoding='utf-8') as f:
        text = f.read()
    return markdown.markdown(text)


@app.route('/')
def index():
    books = {}
    for key, sections in book_structure.items():
        books[key] = []
        for sec in sections:
            html = load_markdown(sec['file'])
            books[key].append({'title': sec['title'], 'content': html})
    data = data_processing.generate_statistics_data()
    img = visualization.plot_statistics(data)
    return render_template('index.html', books=books, image=img)


if __name__ == '__main__':
    app.run(debug=True)

