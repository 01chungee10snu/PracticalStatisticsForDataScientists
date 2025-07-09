from flask import Flask, render_template, request, jsonify
import markdown
import os
from docs.docs_index import book_structure
from modules import data_processing, visualization, content_integration


COLORS = {
    'setosa': 'rgba(255,99,132,0.6)',
    'versicolor': 'rgba(54,162,235,0.6)',
    'virginica': 'rgba(75,192,192,0.6)',
    'Control': 'rgba(255,99,132,0.6)',
    'Treatment_A': 'rgba(54,162,235,0.6)',
    'Treatment_B': 'rgba(75,192,192,0.6)',
    'Male': 'rgba(255,159,64,0.6)',
    'Female': 'rgba(153,102,255,0.6)'
}

app = Flask(__name__)


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
    # 통합 데이터셋 생성
    integrator = content_integration.content_integrator
    integrator.generate_unified_dataset()
    
    books = {}
    
    # 레벨별 데이터셋 및 시각화 매핑
    level_mapping = {
        '통합 개요': {'level': 'overview', 'data_func': lambda: integrator.get_level_specific_data('advanced')},
        '연구방법론': {'level': 'beginner', 'data_func': lambda: integrator.get_level_specific_data('beginner')},
        '요인분석 이론': {'level': 'intermediate', 'data_func': lambda: integrator.get_level_specific_data('intermediate')},
        '통계학습': {'level': 'advanced', 'data_func': lambda: integrator.get_level_specific_data('advanced')}
    }
    
    for key, sections in book_structure.items():
        books[key] = []
        level_info = level_mapping.get(key, {'level': 'beginner', 'data_func': lambda: integrator.get_level_specific_data('beginner')})
        level_data = level_info['data_func']()
        
        for sec in sections:
            html, code = load_markdown(sec['file'])
            
            # 레벨별 적절한 시각화 데이터 생성
            if level_info['level'] == 'beginner':
                # 연구방법론: 인구통계 데이터 시각화
                if 'age' in level_data.columns and 'group' in level_data.columns:
                    chart_data = data_processing.prepare_scatter_datasets(
                        level_data, 'age', 'performance_score', COLORS, 'group'
                    )
                    x_col, y_col = 'age', 'performance_score'
                else:
                    chart_data = []
                    x_col, y_col = 'age', 'group'
                    
            elif level_info['level'] == 'intermediate':
                # 요인분석: 측정 항목 간 관계
                numeric_cols = level_data.select_dtypes(include=['number']).columns
                if len(numeric_cols) >= 2:
                    x_col, y_col = numeric_cols[0], numeric_cols[1] if len(numeric_cols) > 1 else numeric_cols[0]
                    chart_data = data_processing.prepare_scatter_datasets(
                        level_data, x_col, y_col, COLORS, None
                    )
                else:
                    chart_data = []
                    x_col, y_col = 'item1', 'item2'
                    
            elif level_info['level'] == 'advanced':
                # 고급 분석: 머신러닝 특성 시각화
                if 'performance_score' in level_data.columns and 'success' in level_data.columns:
                    chart_data = data_processing.prepare_scatter_datasets(
                        level_data, 'performance_score', 'age', COLORS, 'group'
                    )
                    x_col, y_col = 'performance_score', 'age'
                else:
                    chart_data = []
                    x_col, y_col = 'feature1', 'feature2'
                    
            else:
                # 개요: 기본 시각화
                chart_data = []
                x_col, y_col = 'x', 'y'
            
            books[key].append({
                'title': sec['title'],
                'content': html,
                'code': code,
                'chart': chart_data,
                'x': x_col,
                'y': y_col,
                'level': level_info['level']
            })
    
    return render_template('index.html', books=books)


@app.route('/api/data/<level>')
def get_data(level):
    """레벨별 데이터 API"""
    integrator = content_integration.content_integrator
    if integrator.unified_dataset is None:
        integrator.generate_unified_dataset()
    
    data = integrator.get_level_specific_data(level)
    return jsonify({
        'data': data.to_dict(orient='records'),
        'columns': data.columns.tolist(),
        'shape': data.shape
    })


@app.route('/api/visualization/<level>')
def get_visualization(level):
    """레벨별 시각화 API"""
    integrator = content_integration.content_integrator
    if integrator.unified_dataset is None:
        integrator.generate_unified_dataset()
    
    data = integrator.get_level_specific_data(level)
    
    if level == 'beginner':
        viz_b64 = visualization.plot_research_methodology(data)
    elif level == 'intermediate':
        viz_b64 = visualization.plot_factor_analysis(data)
    elif level == 'advanced':
        viz_b64 = visualization.plot_advanced_analytics(data)
    else:
        viz_b64 = visualization.plot_statistics(data)
    
    return jsonify({
        'visualization': viz_b64,
        'level': level
    })


@app.route('/api/bridge/<from_level>/<to_level>')
def get_bridge_content(from_level, to_level):
    """레벨 간 연결 콘텐츠 API"""
    integrator = content_integration.content_integrator
    bridge_content = integrator.create_bridge_content(from_level, to_level)
    return jsonify(bridge_content)


@app.route('/comprehensive')
def comprehensive_example():
    """종합 예시 페이지"""
    integrator = content_integration.content_integrator
    example = integrator.create_comprehensive_example()
    return render_template('comprehensive.html', example=example)


@app.route('/roadmap')
def learning_roadmap():
    """학습 로드맵 페이지"""
    integrator = content_integration.content_integrator
    roadmap = integrator.generate_content_roadmap()
    return render_template('roadmap.html', roadmap=roadmap)


if __name__ == '__main__':
    # 애플리케이션 시작 시 통합 데이터셋 생성
    integrator = content_integration.content_integrator
    integrator.generate_unified_dataset()
    print("통합 데이터셋이 생성되었습니다.")
    
    app.run(debug=True, host='0.0.0.0', port=5000)

