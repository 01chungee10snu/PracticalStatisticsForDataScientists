#!/usr/bin/env python3
"""
의존성 없는 간단한 웹 인터페이스
- 기본 Python만 사용
- HTTP 서버 기본 모듈 활용
- 실제 브라우저에서 접근 가능
"""

import json
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
from standalone_demo import SimpleLearningSystem

# 전역 학습 시스템 인스턴스
learning_system = SimpleLearningSystem()

class LearningSystemHandler(BaseHTTPRequestHandler):
    """학습 시스템 HTTP 핸들러"""
    
    def do_GET(self):
        """GET 요청 처리"""
        if self.path == '/':
            self.serve_main_page()
        elif self.path == '/api/content':
            self.serve_content_api()
        elif self.path == '/api/analytics':
            self.serve_analytics_api()
        elif self.path == '/api/stats':
            self.serve_stats_api()
        else:
            self.send_error(404, "페이지를 찾을 수 없습니다")
    
    def do_POST(self):
        """POST 요청 처리"""
        if self.path == '/api/register':
            self.handle_register()
        elif self.path == '/api/answer':
            self.handle_answer()
        else:
            self.send_error(404, "API를 찾을 수 없습니다")
    
    def serve_main_page(self):
        """메인 페이지 서빙"""
        html_content = """
        <!DOCTYPE html>
        <html lang="ko">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>적응형 학습 시스템</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; line-height: 1.6; background: #f5f5f5; }
                .container { max-width: 1000px; margin: 0 auto; }
                .card { border: 1px solid #ddd; padding: 20px; margin: 10px 0; border-radius: 8px; background: white; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
                .button { background: #007bff; color: white; padding: 12px 24px; border: none; border-radius: 6px; cursor: pointer; font-size: 14px; transition: all 0.3s; }
                .button:hover { background: #0056b3; transform: translateY(-1px); }
                .success { color: #28a745; font-weight: bold; }
                .error { color: #dc3545; font-weight: bold; }
                .question { background: #f8f9fa; padding: 20px; margin: 15px 0; border-radius: 8px; border-left: 4px solid #007bff; }
                .option { margin: 8px 0; padding: 5px; }
                .option input { margin-right: 10px; }
                .option:hover { background: #e9ecef; border-radius: 4px; }
                .hidden { display: none; }
                .stats { background: #e9ecef; padding: 15px; border-radius: 8px; margin: 15px 0; }
                
                /* Enhanced styling for new content sections */
                .learning-path { background: #e7f3ff; padding: 15px; margin: 15px 0; border-radius: 8px; border-left: 4px solid #007bff; }
                .objectives { background: #fff3cd; padding: 15px; margin: 15px 0; border-radius: 8px; border-left: 4px solid #ffc107; }
                .detailed-explanation { background: #f8f9fa; padding: 15px; margin: 15px 0; border-radius: 8px; }
                .concept-box { background: white; padding: 10px; margin: 8px 0; border-radius: 4px; border: 1px solid #dee2e6; }
                .examples { background: #d1ecf1; padding: 15px; margin: 15px 0; border-radius: 8px; border-left: 4px solid #17a2b8; }
                .study-tips { background: #d4edda; padding: 15px; margin: 15px 0; border-radius: 8px; border-left: 4px solid #28a745; }
                .practice-section { background: #fff; padding: 20px; margin: 20px 0; border-radius: 8px; border: 2px solid #007bff; }
                .next-topics { background: #e2e3e5; padding: 15px; margin: 15px 0; border-radius: 8px; border-left: 4px solid #6c757d; }
                
                /* Typography improvements */
                h1 { color: #2c3e50; text-align: center; margin-bottom: 30px; }
                h2 { color: #34495e; border-bottom: 2px solid #3498db; padding-bottom: 10px; }
                h4 { color: #2c3e50; margin-bottom: 10px; }
                h5 { color: #495057; margin-bottom: 8px; }
                
                /* List styling */
                ul, ol { padding-left: 20px; }
                li { margin-bottom: 5px; }
                
                /* Responsive design */
                @media (max-width: 768px) {
                    .container { max-width: 95%; margin: 10px auto; }
                    .card { padding: 15px; margin: 5px 0; }
                    .button { padding: 10px 20px; font-size: 12px; }
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🎓 적응형 학습 시스템</h1>
                <p>의존성 없이 실제로 동작하는 개인화된 학습 시스템입니다!</p>
                
                <!-- 학습자 등록 -->
                <div class="card">
                    <h2>학습자 등록</h2>
                    <input type="text" id="username" placeholder="사용자 이름" style="width: 200px; padding: 5px;">
                    <button class="button" onclick="registerUser()">등록</button>
                    <div id="register-result"></div>
                </div>
                
                <!-- 개인화된 콘텐츠 -->
                <div class="card">
                    <h2>📚 개인화된 학습 콘텐츠</h2>
                    <button class="button" onclick="getPersonalizedContent()">콘텐츠 추천 받기</button>
                    <div id="content-area"></div>
                </div>
                
                <!-- 학습 분석 -->
                <div class="card">
                    <h2>📈 학습 분석</h2>
                    <button class="button" onclick="getAnalytics()">분석 보기</button>
                    <div id="analytics-area"></div>
                </div>
                
                <!-- 시스템 통계 -->
                <div class="card">
                    <h2>📊 시스템 통계</h2>
                    <button class="button" onclick="getStats()">통계 보기</button>
                    <div id="stats-area"></div>
                </div>
            </div>
            
            <script>
                let currentUser = null;
                let currentContent = null;
                
                function registerUser() {
                    const username = document.getElementById('username').value;
                    if (!username) {
                        alert('사용자 이름을 입력하세요');
                        return;
                    }
                    
                    fetch('/api/register', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({
                            user_id: username,
                            profile: {name: username, difficulty: 5, pace: 'medium'}
                        })
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.status === 'success') {
                            currentUser = username;
                            document.getElementById('register-result').innerHTML = 
                                '<span class="success">✓ ' + data.message + '</span>';
                        } else {
                            document.getElementById('register-result').innerHTML = 
                                '<span class="error">❌ 등록 실패</span>';
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        document.getElementById('register-result').innerHTML = 
                            '<span class="error">❌ 네트워크 오류</span>';
                    });
                }
                
                function getPersonalizedContent() {
                    if (!currentUser) {
                        alert('먼저 학습자를 등록하세요');
                        return;
                    }
                    
                    fetch('/api/content?user_id=' + currentUser)
                    .then(response => response.json())
                    .then(data => {
                        if (data.error) {
                            document.getElementById('content-area').innerHTML = 
                                '<span class="error">❌ ' + data.error + '</span>';
                            return;
                        }
                        
                        currentContent = data;
                        let html = '<h3>' + data.content.title + '</h3>';
                        html += '<p><strong>내용:</strong> ' + data.content.content + '</p>';
                        html += '<p><strong>예상 시간:</strong> ' + data.estimated_time + '</p>';
                        html += '<p><strong>추천 이유:</strong> ' + data.recommendation_reason + '</p>';
                        
                        // 학습 경로 표시
                        if (data.content.learning_path) {
                            html += '<div class="learning-path">';
                            html += '<h4>📚 학습 경로</h4>';
                            html += '<ol>';
                            data.content.learning_path.forEach(step => {
                                html += '<li>' + step + '</li>';
                            });
                            html += '</ol>';
                            html += '</div>';
                        }
                        
                        // 학습 목표 표시
                        if (data.content.learning_objectives) {
                            html += '<div class="objectives">';
                            html += '<h4>🎯 학습 목표</h4>';
                            html += '<ul>';
                            data.content.learning_objectives.forEach(objective => {
                                html += '<li>' + objective + '</li>';
                            });
                            html += '</ul>';
                            html += '</div>';
                        }
                        
                        // 상세 설명 표시
                        if (data.content.detailed_explanation) {
                            html += '<div class="detailed-explanation">';
                            html += '<h4>📖 핵심 개념</h4>';
                            for (const [concept, explanation] of Object.entries(data.content.detailed_explanation)) {
                                html += '<div class="concept-box">';
                                html += '<strong>' + concept + ':</strong> ' + explanation;
                                html += '</div>';
                            }
                            html += '</div>';
                        }
                        
                        // 실생활 예시 표시
                        if (data.content.real_world_examples) {
                            html += '<div class="examples">';
                            html += '<h4>🌍 실생활 예시</h4>';
                            html += '<ul>';
                            data.content.real_world_examples.forEach(example => {
                                html += '<li>' + example + '</li>';
                            });
                            html += '</ul>';
                            html += '</div>';
                        }
                        
                        // 학습 팁 표시
                        if (data.study_tips) {
                            html += '<div class="study-tips">';
                            html += '<h4>💡 학습 팁</h4>';
                            html += '<ul>';
                            data.study_tips.forEach(tip => {
                                html += '<li>' + tip + '</li>';
                            });
                            html += '</ul>';
                            html += '</div>';
                        }
                        
                        // 문제 표시
                        html += '<div class="practice-section">';
                        html += '<h4>🧠 연습 문제</h4>';
                        data.content.questions.forEach((question, index) => {
                            html += '<div class="question">';
                            html += '<h5>문제 ' + (index + 1) + ' (' + question.concept + ')</h5>';
                            html += '<p><strong>난이도:</strong> ' + '★'.repeat(question.difficulty || 3) + '</p>';
                            html += '<p>' + question.q + '</p>';
                            question.options.forEach((option, optIndex) => {
                                html += '<div class="option">';
                                html += '<input type="radio" name="q' + index + '" value="' + optIndex + '" id="q' + index + '_' + optIndex + '">';
                                html += '<label for="q' + index + '_' + optIndex + '">' + option + '</label>';
                                html += '</div>';
                            });
                            html += '<button class="button" onclick="submitAnswer(' + index + ')">답안 제출</button>';
                            html += '<div id="result-' + index + '"></div>';
                            html += '</div>';
                        });
                        html += '</div>';
                        
                        // 다음 학습 주제 제안
                        if (data.next_topics && data.next_topics.length > 0) {
                            html += '<div class="next-topics">';
                            html += '<h4>➡️ 다음 학습 주제</h4>';
                            html += '<ul>';
                            data.next_topics.forEach(topic => {
                                html += '<li>' + topic + '</li>';
                            });
                            html += '</ul>';
                            html += '</div>';
                        }
                        
                        document.getElementById('content-area').innerHTML = html;
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        document.getElementById('content-area').innerHTML = 
                            '<span class="error">❌ 콘텐츠 로딩 실패</span>';
                    });
                }
                
                function submitAnswer(questionIndex) {
                    const selectedOption = document.querySelector('input[name="q' + questionIndex + '"]:checked');
                    if (!selectedOption) {
                        alert('답을 선택하세요');
                        return;
                    }
                    
                    fetch('/api/answer', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({
                            user_id: currentUser,
                            content_id: currentContent.content_id,
                            question_idx: questionIndex,
                            selected_option: parseInt(selectedOption.value)
                        })
                    })
                    .then(response => response.json())
                    .then(data => {
                        let html = '';
                        if (data.correct) {
                            html = '<span class="success">✅ 정답입니다!</span>';
                        } else {
                            html = '<span class="error">❌ 틀렸습니다. 정답: ' + data.correct_answer + '</span>';
                        }
                        html += '<p><strong>해설:</strong> ' + data.explanation + '</p>';
                        html += '<p><strong>성과:</strong> ' + data.performance_summary.success_rate + '% 성공률</p>';
                        
                        if (data.level_up) {
                            html += '<p class="success">🎉 축하합니다! ' + data.new_level + ' 레벨로 승급했습니다!</p>';
                        }
                        
                        document.getElementById('result-' + questionIndex).innerHTML = html;
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        document.getElementById('result-' + questionIndex).innerHTML = 
                            '<span class="error">❌ 답안 제출 실패</span>';
                    });
                }
                
                function getAnalytics() {
                    if (!currentUser) {
                        alert('먼저 학습자를 등록하세요');
                        return;
                    }
                    
                    fetch('/api/analytics?user_id=' + currentUser)
                    .then(response => response.json())
                    .then(data => {
                        if (data.error) {
                            document.getElementById('analytics-area').innerHTML = 
                                '<span class="error">❌ ' + data.error + '</span>';
                            return;
                        }
                        
                        if (data.message) {
                            document.getElementById('analytics-area').innerHTML = 
                                '<p>' + data.message + '</p>';
                            return;
                        }
                        
                        let html = '<div class="stats">';
                        html += '<h4>전체 성과</h4>';
                        html += '<p>총 시도: ' + data.overall_stats.total_attempts + '회</p>';
                        html += '<p>정답률: ' + data.overall_stats.success_rate + '%</p>';
                        html += '<p>현재 레벨: ' + data.overall_stats.current_level + '</p>';
                        html += '<p>학습 상태: ' + data.learning_state + '</p>';
                        html += '<p>추천사항: ' + data.recommendation + '</p>';
                        html += '</div>';
                        
                        document.getElementById('analytics-area').innerHTML = html;
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        document.getElementById('analytics-area').innerHTML = 
                            '<span class="error">❌ 분석 데이터 로딩 실패</span>';
                    });
                }
                
                function getStats() {
                    fetch('/api/stats')
                    .then(response => response.json())
                    .then(data => {
                        if (data.message) {
                            document.getElementById('stats-area').innerHTML = 
                                '<p>' + data.message + '</p>';
                            return;
                        }
                        
                        let html = '<div class="stats">';
                        html += '<h4>시스템 통계</h4>';
                        html += '<p>총 학습자: ' + data.total_learners + '명</p>';
                        html += '<p>총 상호작용: ' + data.total_interactions + '회</p>';
                        html += '<p>전체 성공률: ' + data.overall_success_rate + '%</p>';
                        html += '<p>콘텐츠 수: ' + data.content_library_size + '개</p>';
                        html += '<p>레벨별 분포: ' + JSON.stringify(data.level_distribution) + '</p>';
                        html += '</div>';
                        
                        document.getElementById('stats-area').innerHTML = html;
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        document.getElementById('stats-area').innerHTML = 
                            '<span class="error">❌ 통계 데이터 로딩 실패</span>';
                    });
                }
            </script>
        </body>
        </html>
        """
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html_content.encode('utf-8'))
    
    def serve_content_api(self):
        """콘텐츠 API 서빙"""
        query = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        user_id = query.get('user_id', [None])[0]
        
        if not user_id:
            self.send_json_response({'error': '사용자 ID가 필요합니다'}, 400)
            return
        
        content = learning_system.get_personalized_content(user_id)
        self.send_json_response(content)
    
    def serve_analytics_api(self):
        """분석 API 서빙"""
        query = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        user_id = query.get('user_id', [None])[0]
        
        if not user_id:
            self.send_json_response({'error': '사용자 ID가 필요합니다'}, 400)
            return
        
        analytics = learning_system.get_learning_analytics(user_id)
        self.send_json_response(analytics)
    
    def serve_stats_api(self):
        """통계 API 서빙"""
        stats = learning_system.get_system_stats()
        self.send_json_response(stats)
    
    def handle_register(self):
        """학습자 등록 처리"""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
            user_id = data.get('user_id')
            profile = data.get('profile', {})
            
            if not user_id:
                self.send_json_response({'error': '사용자 ID가 필요합니다'}, 400)
                return
            
            result = learning_system.register_learner(user_id, profile)
            self.send_json_response(result)
            
        except json.JSONDecodeError:
            self.send_json_response({'error': '잘못된 JSON 형식'}, 400)
    
    def handle_answer(self):
        """답안 제출 처리"""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
            user_id = data.get('user_id')
            content_id = data.get('content_id')
            question_idx = data.get('question_idx')
            selected_option = data.get('selected_option')
            
            if not all([user_id, content_id is not None, question_idx is not None, selected_option is not None]):
                self.send_json_response({'error': '필수 파라미터가 누락되었습니다'}, 400)
                return
            
            result = learning_system.submit_answer(user_id, content_id, question_idx, selected_option)
            self.send_json_response(result)
            
        except json.JSONDecodeError:
            self.send_json_response({'error': '잘못된 JSON 형식'}, 400)
    
    def send_json_response(self, data, status_code=200):
        """JSON 응답 전송"""
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.end_headers()
        json_data = json.dumps(data, ensure_ascii=False)
        self.wfile.write(json_data.encode('utf-8'))
    
    def log_message(self, format, *args):
        """로그 메시지 (출력 제어)"""
        return  # 로그 출력 비활성화


def run_server(port=8000):
    """웹 서버 실행"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, LearningSystemHandler)
    
    print(f"🌐 적응형 학습 시스템 웹 서버 시작")
    print(f"📍 주소: http://localhost:{port}")
    print(f"🚀 브라우저에서 위 주소로 접속하세요!")
    print(f"⏹️  서버 중지: Ctrl+C")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n👋 서버를 종료합니다.")
        httpd.server_close()


if __name__ == "__main__":
    run_server()