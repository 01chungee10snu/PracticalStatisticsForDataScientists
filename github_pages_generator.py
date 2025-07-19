"""
GitHub Pages 최적화 결과 공유 시스템
정적 파일 기반으로 학습 결과를 GitHub Pages에서 공유할 수 있도록 생성
"""

import json
import datetime
import os
from typing import Dict, Any, List
from dataclasses import dataclass


@dataclass
class GitHubPagesResult:
    """GitHub Pages용 결과 데이터"""
    session_id: str
    title: str
    created_at: str
    completion_percentage: float
    success_rate: float
    total_attempts: int
    achievements: List[str]
    recommendations: List[str]


class GitHubPagesGenerator:
    """GitHub Pages용 정적 파일 생성기"""
    
    def __init__(self, output_dir: str = "docs"):
        self.output_dir = output_dir
        self.results_dir = os.path.join(output_dir, "results")
        
        # 디렉토리 생성
        os.makedirs(self.results_dir, exist_ok=True)
    
    def generate_result_page(self, result_data: GitHubPagesResult) -> str:
        """개별 결과 페이지 생성"""
        html_content = f'''<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{result_data.title} - 학습 결과</title>
    <meta name="description" content="통계학습 교육 플랫폼 학습 결과 리포트">
    <meta property="og:title" content="{result_data.title}">
    <meta property="og:description" content="완료율 {result_data.completion_percentage:.1f}%의 학습 성과를 달성했습니다.">
    <meta property="og:type" content="website">
    
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 900px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #2c3e50, #3498db);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5rem;
            margin-bottom: 10px;
            font-weight: 700;
        }}
        
        .header p {{
            font-size: 1.2rem;
            opacity: 0.9;
            margin-bottom: 5px;
        }}
        
        .header .date {{
            font-size: 1rem;
            opacity: 0.8;
        }}
        
        .content {{
            padding: 40px;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }}
        
        .stat-card {{
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 25px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        }}
        
        .stat-value {{
            font-size: 2.5rem;
            font-weight: bold;
            margin-bottom: 8px;
            display: block;
        }}
        
        .stat-label {{
            font-size: 1rem;
            opacity: 0.9;
        }}
        
        .section {{
            margin-bottom: 35px;
        }}
        
        .section h3 {{
            color: #2c3e50;
            font-size: 1.5rem;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .achievement-list, .recommendation-list {{
            list-style: none;
        }}
        
        .achievement-item {{
            background: #d4edda;
            border-left: 4px solid #28a745;
            padding: 15px;
            margin-bottom: 10px;
            border-radius: 0 8px 8px 0;
            transition: transform 0.2s ease;
        }}
        
        .achievement-item:hover {{
            transform: translateX(5px);
        }}
        
        .recommendation-item {{
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 15px;
            margin-bottom: 10px;
            border-radius: 0 8px 8px 0;
            transition: transform 0.2s ease;
        }}
        
        .recommendation-item:hover {{
            transform: translateX(5px);
        }}
        
        .footer {{
            background: #f8f9fa;
            padding: 30px;
            text-align: center;
            border-top: 1px solid #e9ecef;
        }}
        
        .footer p {{
            color: #6c757d;
            margin-bottom: 10px;
        }}
        
        .footer a {{
            color: #007bff;
            text-decoration: none;
            font-weight: 600;
        }}
        
        .footer a:hover {{
            text-decoration: underline;
        }}
        
        .share-buttons {{
            display: flex;
            justify-content: center;
            gap: 15px;
            margin-top: 20px;
        }}
        
        .share-btn {{
            padding: 10px 20px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 600;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            transition: all 0.3s ease;
        }}
        
        .share-btn.twitter {{
            background: #1da1f2;
            color: white;
        }}
        
        .share-btn.linkedin {{
            background: #0077b5;
            color: white;
        }}
        
        .share-btn.copy {{
            background: #6c757d;
            color: white;
        }}
        
        .share-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        }}
        
        .progress-ring {{
            width: 120px;
            height: 120px;
            margin: 0 auto 20px;
        }}
        
        .progress-ring circle {{
            fill: none;
            stroke-width: 8;
            stroke-linecap: round;
            transform: rotate(-90deg);
            transform-origin: 50% 50%;
        }}
        
        .progress-ring .background {{
            stroke: rgba(255, 255, 255, 0.3);
        }}
        
        .progress-ring .progress {{
            stroke: #fff;
            stroke-dasharray: 283;
            stroke-dashoffset: {283 - (283 * result_data.completion_percentage / 100)};
            transition: stroke-dashoffset 1s ease;
        }}
        
        .progress-text {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 1.5rem;
            font-weight: bold;
            color: white;
        }}
        
        @media (max-width: 768px) {{
            .container {{
                margin: 10px;
            }}
            
            .header {{
                padding: 30px 20px;
            }}
            
            .header h1 {{
                font-size: 2rem;
            }}
            
            .content {{
                padding: 30px 20px;
            }}
            
            .stats-grid {{
                grid-template-columns: repeat(2, 1fr);
            }}
            
            .share-buttons {{
                flex-direction: column;
                align-items: center;
            }}
        }}
        
        @media (max-width: 480px) {{
            .stats-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="progress-ring" style="position: relative; display: inline-block;">
                <svg width="120" height="120">
                    <circle class="background" cx="60" cy="60" r="45"></circle>
                    <circle class="progress" cx="60" cy="60" r="45"></circle>
                </svg>
                <div class="progress-text">{result_data.completion_percentage:.0f}%</div>
            </div>
            <h1>🎓 {result_data.title}</h1>
            <p>학습 완료 결과 리포트</p>
            <p class="date">생성일: {datetime.datetime.fromisoformat(result_data.created_at).strftime("%Y년 %m월 %d일 %H:%M")}</p>
        </div>
        
        <div class="content">
            <div class="stats-grid">
                <div class="stat-card">
                    <span class="stat-value">{result_data.completion_percentage:.1f}%</span>
                    <div class="stat-label">완료율</div>
                </div>
                <div class="stat-card">
                    <span class="stat-value">{result_data.success_rate:.1f}%</span>
                    <div class="stat-label">성공률</div>
                </div>
                <div class="stat-card">
                    <span class="stat-value">{result_data.total_attempts}</span>
                    <div class="stat-label">총 시도</div>
                </div>
                <div class="stat-card">
                    <span class="stat-value">A+</span>
                    <div class="stat-label">학습 등급</div>
                </div>
            </div>
            
            <div class="section">
                <h3>🏆 학습 성취</h3>
                <ul class="achievement-list">
                    {''.join(f'<li class="achievement-item">{achievement}</li>' for achievement in result_data.achievements)}
                </ul>
            </div>
            
            <div class="section">
                <h3>📋 권장사항</h3>
                <ul class="recommendation-list">
                    {''.join(f'<li class="recommendation-item">• {rec}</li>' for rec in result_data.recommendations)}
                </ul>
            </div>
        </div>
        
        <div class="footer">
            <p><strong>🎯 통계학습 교육 플랫폼</strong>으로 생성된 리포트</p>
            <p>세션 ID: {result_data.session_id}</p>
            
            <div class="share-buttons">
                <a href="#" class="share-btn twitter" onclick="shareOnTwitter()">
                    🐦 Twitter 공유
                </a>
                <a href="#" class="share-btn linkedin" onclick="shareOnLinkedIn()">
                    💼 LinkedIn 공유
                </a>
                <a href="#" class="share-btn copy" onclick="copyLink()">
                    🔗 링크 복사
                </a>
            </div>
            
            <p style="margin-top: 20px;">
                <a href="../index.html">🏠 메인으로 돌아가기</a> | 
                <a href="../integrated_practice_demo.html">🚀 새로운 학습 시작</a>
            </p>
        </div>
    </div>

    <script>
        // 페이지 로드 시 애니메이션
        document.addEventListener('DOMContentLoaded', function() {{
            // 통계 카드 애니메이션
            const statCards = document.querySelectorAll('.stat-card');
            statCards.forEach((card, index) => {{
                card.style.opacity = '0';
                card.style.transform = 'translateY(20px)';
                
                setTimeout(() => {{
                    card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
                    card.style.opacity = '1';
                    card.style.transform = 'translateY(0)';
                }}, 200 + (index * 100));
            }});
            
            // 성취 항목 애니메이션
            const achievements = document.querySelectorAll('.achievement-item, .recommendation-item');
            achievements.forEach((item, index) => {{
                item.style.opacity = '0';
                item.style.transform = 'translateX(-20px)';
                
                setTimeout(() => {{
                    item.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
                    item.style.opacity = '1';
                    item.style.transform = 'translateX(0)';
                }}, 800 + (index * 100));
            }});
        }});
        
        // 소셜 공유 기능
        function shareOnTwitter() {{
            const text = `통계학습 교육 플랫폼에서 {result_data.completion_percentage:.0f}% 완료율을 달성했습니다! 🎓`;
            const url = window.location.href;
            window.open(`https://twitter.com/intent/tweet?text=${{encodeURIComponent(text)}}&url=${{encodeURIComponent(url)}}`, '_blank');
        }}
        
        function shareOnLinkedIn() {{
            const url = window.location.href;
            window.open(`https://www.linkedin.com/sharing/share-offsite/?url=${{encodeURIComponent(url)}}`, '_blank');
        }}
        
        function copyLink() {{
            navigator.clipboard.writeText(window.location.href).then(() => {{
                alert('링크가 클립보드에 복사되었습니다!');
            }}).catch(() => {{
                // 폴백: 텍스트 선택
                const textArea = document.createElement('textarea');
                textArea.value = window.location.href;
                document.body.appendChild(textArea);
                textArea.select();
                document.execCommand('copy');
                document.body.removeChild(textArea);
                alert('링크가 클립보드에 복사되었습니다!');
            }});
        }}
    </script>
</body>
</html>'''
        
        return html_content
    
    def generate_results_index(self, results: List[GitHubPagesResult]) -> str:
        """결과 목록 인덱스 페이지 생성"""
        results_html = ""
        
        for result in sorted(results, key=lambda x: x.created_at, reverse=True):
            results_html += f'''
            <div class="result-card">
                <div class="result-header">
                    <h3>{result.title}</h3>
                    <span class="result-date">{datetime.datetime.fromisoformat(result.created_at).strftime("%Y.%m.%d")}</span>
                </div>
                <div class="result-stats">
                    <div class="stat">
                        <span class="stat-value">{result.completion_percentage:.0f}%</span>
                        <span class="stat-label">완료율</span>
                    </div>
                    <div class="stat">
                        <span class="stat-value">{result.success_rate:.0f}%</span>
                        <span class="stat-label">성공률</span>
                    </div>
                    <div class="stat">
                        <span class="stat-value">{result.total_attempts}</span>
                        <span class="stat-label">시도</span>
                    </div>
                </div>
                <a href="results/{result.session_id}.html" class="view-btn">결과 보기</a>
            </div>'''
        
        html_content = f'''<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>학습 결과 모음 - 통계학습 교육 플랫폼</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .header {{
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 40px;
            margin-bottom: 30px;
            text-align: center;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }}
        .results-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 25px;
        }}
        .result-card {{
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease;
        }}
        .result-card:hover {{ transform: translateY(-5px); }}
        .result-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }}
        .result-stats {{
            display: flex;
            justify-content: space-around;
            margin-bottom: 20px;
        }}
        .stat {{ text-align: center; }}
        .stat-value {{ display: block; font-size: 1.5rem; font-weight: bold; color: #2c3e50; }}
        .stat-label {{ font-size: 0.9rem; color: #7f8c8d; }}
        .view-btn {{
            display: block;
            background: linear-gradient(135deg, #3498db, #2980b9);
            color: white;
            padding: 12px;
            border-radius: 8px;
            text-decoration: none;
            text-align: center;
            font-weight: 600;
            transition: all 0.3s ease;
        }}
        .view-btn:hover {{ transform: translateY(-2px); }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 학습 결과 모음</h1>
            <p>완료된 학습 세션들의 결과를 확인해보세요</p>
        </div>
        
        <div class="results-grid">
            {results_html}
        </div>
        
        <div style="text-align: center; margin-top: 30px;">
            <a href="index.html" style="color: white; text-decoration: none; font-size: 1.1rem;">🏠 메인으로 돌아가기</a>
        </div>
    </div>
</body>
</html>'''
        
        return html_content
    
    def save_result_page(self, result_data: GitHubPagesResult) -> str:
        """결과 페이지를 파일로 저장"""
        html_content = self.generate_result_page(result_data)
        file_path = os.path.join(self.results_dir, f"{result_data.session_id}.html")
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return file_path
    
    def save_results_index(self, results: List[GitHubPagesResult]) -> str:
        """결과 인덱스 페이지를 파일로 저장"""
        html_content = self.generate_results_index(results)
        file_path = os.path.join(self.output_dir, "results.html")
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return file_path


def demo_github_pages_generator():
    """GitHub Pages 생성기 데모"""
    print("=== GitHub Pages 생성기 데모 ===\\n")
    
    # 생성기 초기화
    generator = GitHubPagesGenerator()
    
    # 샘플 결과 데이터 생성
    sample_results = [
        GitHubPagesResult(
            session_id="session_demo_user_20250719_171618",
            title="기술통계량 마스터 과정",
            created_at=datetime.datetime.now().isoformat(),
            completion_percentage=85.0,
            success_rate=92.5,
            total_attempts=12,
            achievements=[
                "🧠 모든 단계를 순서대로 완료했습니다!",
                "📊 기술통계량 계산을 정확히 수행했습니다!",
                "🎯 첫 번째 시도에서 성공한 단계가 3개입니다!",
                "💡 힌트 없이 스스로 해결한 문제가 2개입니다!"
            ],
            recommendations=[
                "표준편차와 분산의 개념을 다시 한 번 복습해보세요.",
                "다양한 데이터셋으로 실습을 반복해보세요.",
                "시각화 기법을 활용하여 결과를 더 잘 이해해보세요.",
                "다음 단계인 추론통계학으로 진행해보세요."
            ]
        ),
        GitHubPagesResult(
            session_id="session_advanced_user_20250719_180000",
            title="고급 데이터 분석 실습",
            created_at=(datetime.datetime.now() - datetime.timedelta(hours=2)).isoformat(),
            completion_percentage=95.0,
            success_rate=88.0,
            total_attempts=8,
            achievements=[
                "🏆 완벽한 학습 성과를 달성했습니다!",
                "⚡ 평균보다 빠른 속도로 완료했습니다!",
                "🎯 모든 검증을 통과했습니다!"
            ],
            recommendations=[
                "머신러닝 기초 과정으로 진행해보세요.",
                "실제 프로젝트에 적용해보세요."
            ]
        )
    ]
    
    print(f"샘플 결과 {len(sample_results)}개 생성")
    
    # 개별 결과 페이지 생성
    print("\\n=== 개별 결과 페이지 생성 ===")
    for result in sample_results:
        file_path = generator.save_result_page(result)
        print(f"결과 페이지 생성: {file_path}")
    
    # 결과 인덱스 페이지 생성
    print("\\n=== 결과 인덱스 페이지 생성 ===")
    index_path = generator.save_results_index(sample_results)
    print(f"인덱스 페이지 생성: {index_path}")
    
    print("\\n=== GitHub Pages 배포 준비 완료 ===")
    print("생성된 파일들:")
    print(f"- {index_path}")
    for result in sample_results:
        print(f"- {os.path.join(generator.results_dir, result.session_id + '.html')}")
    
    print("\\n이제 GitHub Pages에서 다음 URL로 접근할 수 있습니다:")
    print("- https://your-username.github.io/your-repo/")
    print("- https://your-username.github.io/your-repo/results.html")
    for result in sample_results:
        print(f"- https://your-username.github.io/your-repo/results/{result.session_id}.html")
    
    return generator


if __name__ == "__main__":
    demo_github_pages_generator()