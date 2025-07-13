"""
현대적 통계 학습 플랫폼 - Flask 웹 애플리케이션
- RESTful API 아키텍처
- 현대적 프론트엔드 지원
- 사용자 인증 및 세션 관리
- 실시간 학습 분석
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.security import generate_password_hash, check_password_hash
import json
import os
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import secrets
import time

# 로컬 모듈 임포트
from modules.adaptive_learning_engine import adaptive_engine, LearningInteraction, InteractionType
from modules.content_integration import content_integrator
from modules.enhanced_visualization import visualizer
from modules.enhanced_tutorials import tutorial_engine
from modules.cognitive_load_optimizer import cognitive_optimizer
from modules.assessment_system import assessment_engine, certification_manager
from modules.interactive_content import interactive_content_engine

# Flask 앱 설정
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', secrets.token_urlsafe(32))

# 보안 설정
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
    PERMANENT_SESSION_LIFETIME=timedelta(hours=24)
)

# CORS 및 Rate Limiting 설정
CORS(app, origins=['http://localhost:5000', 'https://yourdomain.com'])
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s %(message)s'
)
logger = logging.getLogger(__name__)

# 사용자 데이터 스토어 (실제 환경에서는 데이터베이스 사용)
USERS_DB = {}
SESSIONS_DB = {}

class UserManager:
    """사용자 관리 클래스"""
    
    @staticmethod
    def create_user(username: str, email: str, password: str) -> Dict[str, Any]:
        """새 사용자 생성"""
        if username in USERS_DB:
            return {"success": False, "message": "이미 존재하는 사용자명입니다"}
        
        user_id = f"user_{len(USERS_DB) + 1}"
        hashed_password = generate_password_hash(password)
        
        user_data = {
            "id": user_id,
            "username": username,
            "email": email,
            "password_hash": hashed_password,
            "created_at": datetime.now().isoformat(),
            "profile": {
                "learning_style": "visual",
                "difficulty_preference": 5,
                "goals": [],
                "streak": 0,
                "total_study_time": 0
            },
            "statistics": {
                "lessons_completed": 0,
                "total_score": 0,
                "success_rate": 0.0,
                "last_activity": None
            }
        }
        
        USERS_DB[username] = user_data
        
        # 적응형 학습 엔진에 사용자 등록
        adaptive_engine.register_learner(user_id, user_data["profile"])
        
        return {"success": True, "user_id": user_id}
    
    @staticmethod
    def authenticate_user(username: str, password: str) -> Optional[Dict[str, Any]]:
        """사용자 인증"""
        user = USERS_DB.get(username)
        if user and check_password_hash(user["password_hash"], password):
            return user
        return None
    
    @staticmethod
    def get_user(user_id: str) -> Optional[Dict[str, Any]]:
        """사용자 정보 조회"""
        for user in USERS_DB.values():
            if user["id"] == user_id:
                return user
        return None
    
    @staticmethod
    def update_user_stats(user_id: str, lesson_completed: bool = False, score: int = 0):
        """사용자 통계 업데이트"""
        user = UserManager.get_user(user_id)
        if not user:
            return
        
        stats = user["statistics"]
        
        if lesson_completed:
            stats["lessons_completed"] += 1
        
        if score > 0:
            # 누적 점수 및 성공률 계산
            current_total = stats["total_score"]
            lessons_count = stats["lessons_completed"]
            stats["total_score"] = current_total + score
            stats["success_rate"] = stats["total_score"] / (lessons_count * 100) if lessons_count > 0 else 0
        
        stats["last_activity"] = datetime.now().isoformat()

class AnalyticsManager:
    """학습 분석 관리 클래스"""
    
    @staticmethod
    def get_user_analytics(user_id: str) -> Dict[str, Any]:
        """사용자별 학습 분석 데이터 생성"""
        try:
            # 사용자 기본 정보
            user = UserManager.get_user(user_id)
            if not user:
                return {"error": "사용자를 찾을 수 없습니다"}
            
            # 적응형 학습 엔진에서 데이터 가져오기
            learning_analytics = adaptive_engine.get_learning_analytics(user_id)
            recommendations = adaptive_engine.generate_content_recommendations(user_id, 5)
            
            # 진도 데이터 생성
            progress_data = AnalyticsManager._generate_progress_data(user_id)
            
            # 최근 활동 데이터
            recent_activity = AnalyticsManager._get_recent_activity(user_id)
            
            return {
                "user_stats": user["statistics"],
                "learning_analytics": learning_analytics,
                "recommendations": [
                    {
                        "id": rec.content_id,
                        "title": AnalyticsManager._get_content_title(rec.content_id),
                        "difficulty": rec.difficulty_adjustment,
                        "estimated_time": rec.estimated_time,
                        "match_score": rec.recommendation_score,
                        "reasoning": rec.reasoning
                    }
                    for rec in recommendations
                ],
                "progress_data": progress_data,
                "recent_activity": recent_activity
            }
            
        except Exception as e:
            logger.error(f"Analytics generation error for user {user_id}: {e}")
            return {"error": "분석 데이터 생성 중 오류가 발생했습니다"}
    
    @staticmethod
    def _generate_progress_data(user_id: str) -> List[Dict[str, Any]]:
        """진도 데이터 생성 (최근 30일)"""
        data = []
        now = datetime.now()
        
        for i in range(30, 0, -1):
            date = now - timedelta(days=i)
            # 실제 환경에서는 데이터베이스에서 조회
            progress = min(100, max(0, 50 + (30 - i) * 2 + (i % 3) * 10))
            
            data.append({
                "date": date.strftime("%Y-%m-%d"),
                "progress": progress,
                "lessons_completed": (30 - i) // 3,
                "time_spent": 30 + (i % 5) * 15
            })
        
        return data
    
    @staticmethod
    def _get_recent_activity(user_id: str) -> List[Dict[str, Any]]:
        """최근 활동 데이터 생성"""
        # 실제 환경에서는 데이터베이스에서 조회
        activities = [
            {
                "id": 1,
                "type": "lesson_completed",
                "title": "기술통계학 개념",
                "timestamp": (datetime.now() - timedelta(hours=2)).isoformat(),
                "score": 95
            },
            {
                "id": 2,
                "type": "quiz_attempted",
                "title": "확률분포 퀴즈",
                "timestamp": (datetime.now() - timedelta(hours=4)).isoformat(),
                "score": 88
            },
            {
                "id": 3,
                "type": "tutorial_viewed",
                "title": "회귀분석 기초",
                "timestamp": (datetime.now() - timedelta(days=1)).isoformat(),
                "score": None
            }
        ]
        
        return activities
    
    @staticmethod
    def _get_content_title(content_id: str) -> str:
        """콘텐츠 ID에서 제목 생성"""
        title_map = {
            "stats_basics": "기술통계학 기초",
            "probability": "확률론 개념",
            "hypothesis_testing": "가설검정",
            "regression": "회귀분석",
            "factor_analysis": "요인분석",
            "machine_learning": "머신러닝 입문"
        }
        return title_map.get(content_id, f"콘텐츠 {content_id}")

# 라우트 정의

@app.route('/')
def index():
    """메인 페이지 - 전체 기능 통합 데모"""
    return render_template('showcase_index.html')

@app.route('/dashboard')
def dashboard():
    """대시보드 페이지"""
    return render_template('modern_index.html')

@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def login():
    """로그인 처리"""
    if request.method == 'GET':
        return render_template('auth/login.html')
    
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({"success": False, "message": "사용자명과 비밀번호를 입력해주세요"}), 400
        
        user = UserManager.authenticate_user(username, password)
        if user:
            session['user_id'] = user['id']
            session['username'] = username
            session.permanent = True
            
            logger.info(f"User {username} logged in successfully")
            return jsonify({
                "success": True,
                "user": {
                    "id": user['id'],
                    "username": user['username'],
                    "email": user['email']
                }
            })
        else:
            return jsonify({"success": False, "message": "잘못된 사용자명 또는 비밀번호입니다"}), 401
            
    except Exception as e:
        logger.error(f"Login error: {e}")
        return jsonify({"success": False, "message": "로그인 처리 중 오류가 발생했습니다"}), 500

@app.route('/register', methods=['POST'])
@limiter.limit("3 per minute")
def register():
    """회원가입 처리"""
    try:
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        if not all([username, email, password]):
            return jsonify({"success": False, "message": "모든 필드를 입력해주세요"}), 400
        
        if len(password) < 8:
            return jsonify({"success": False, "message": "비밀번호는 8자 이상이어야 합니다"}), 400
        
        result = UserManager.create_user(username, email, password)
        
        if result["success"]:
            logger.info(f"New user registered: {username}")
            return jsonify(result), 201
        else:
            return jsonify(result), 400
            
    except Exception as e:
        logger.error(f"Registration error: {e}")
        return jsonify({"success": False, "message": "회원가입 처리 중 오류가 발생했습니다"}), 500

@app.route('/logout', methods=['POST'])
def logout():
    """로그아웃 처리"""
    username = session.get('username')
    session.clear()
    
    if username:
        logger.info(f"User {username} logged out")
    
    return jsonify({"success": True, "message": "로그아웃되었습니다"})

# API 라우트

@app.route('/api/v1/user/profile')
def get_user_profile():
    """사용자 프로필 조회"""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "인증이 필요합니다"}), 401
    
    user = UserManager.get_user(user_id)
    if not user:
        return jsonify({"error": "사용자를 찾을 수 없습니다"}), 404
    
    return jsonify({
        "id": user["id"],
        "username": user["username"],
        "email": user["email"],
        "profile": user["profile"],
        "statistics": user["statistics"]
    })

@app.route('/api/v1/analytics/dashboard')
def get_dashboard_analytics():
    """대시보드 분석 데이터"""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "인증이 필요합니다"}), 401
    
    analytics = AnalyticsManager.get_user_analytics(user_id)
    return jsonify(analytics)

@app.route('/api/v1/learning/content/<level>')
def get_learning_content(level):
    """학습 콘텐츠 조회"""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "인증이 필요합니다"}), 401
    
    try:
        # 레벨별 콘텐츠 생성
        content_data = content_integrator.get_level_specific_data(level)
        optimized_content = cognitive_optimizer.optimize_content_presentation(
            user_id, content_data, level
        )
        
        return jsonify({
            "level": level,
            "content": optimized_content,
            "total_items": len(optimized_content) if optimized_content else 0
        })
        
    except Exception as e:
        logger.error(f"Content loading error for level {level}: {e}")
        return jsonify({"error": "콘텐츠를 불러오는 중 오류가 발생했습니다"}), 500

@app.route('/api/v1/learning/interact', methods=['POST'])
@limiter.limit("100 per minute")
def track_learning_interaction():
    """학습 상호작용 추적"""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "인증이 필요합니다"}), 401
    
    try:
        data = request.get_json()
        
        # 상호작용 데이터 생성
        interaction = LearningInteraction(
            user_id=user_id,
            timestamp=datetime.now(),
            interaction_type=InteractionType(data.get('interaction_type', 'content_view')),
            content_id=data.get('content_id', ''),
            duration=data.get('duration', 0),
            success=data.get('success'),
            difficulty_level=data.get('difficulty_level', 5),
            hint_used=data.get('hint_used', False),
            attempts=data.get('attempts', 1),
            confidence_level=data.get('confidence_level')
        )
        
        # 적응형 학습 엔진에 추적
        adaptive_engine.track_interaction(interaction)
        
        # 사용자 통계 업데이트
        if interaction.success is not None:
            score = 100 if interaction.success else 0
            UserManager.update_user_stats(
                user_id, 
                lesson_completed=interaction.success,
                score=score
            )
        
        # 피드백 생성
        feedback = adaptive_engine.generate_adaptive_feedback(user_id, interaction)
        
        return jsonify({
            "success": True,
            "feedback": feedback,
            "next_recommendations": [
                {
                    "content_id": rec.content_id,
                    "reasoning": rec.reasoning,
                    "difficulty": rec.difficulty_adjustment
                }
                for rec in adaptive_engine.generate_content_recommendations(user_id, 3)
            ]
        })
        
    except Exception as e:
        logger.error(f"Interaction tracking error: {e}")
        return jsonify({"error": "상호작용 추적 중 오류가 발생했습니다"}), 500

@app.route('/api/v1/visualization/<chart_type>')
def get_visualization(chart_type):
    """시각화 데이터 생성"""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "인증이 필요합니다"}), 401
    
    try:
        # 시각화 데이터 생성
        viz_data = visualizer.create_adaptive_visualization(
            chart_type, user_id, 
            width=800, height=400
        )
        
        return jsonify({
            "chart_type": chart_type,
            "data": viz_data,
            "generated_at": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Visualization error for {chart_type}: {e}")
        return jsonify({"error": "시각화 생성 중 오류가 발생했습니다"}), 500

@app.route('/api/v1/tutorial/generate', methods=['POST'])
def generate_tutorial():
    """개인화된 튜토리얼 생성"""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "인증이 필요합니다"}), 401
    
    try:
        data = request.get_json()
        topic = data.get('topic', 'statistics_basics')
        difficulty = data.get('difficulty', 'beginner')
        
        # 튜토리얼 생성
        tutorial_content = tutorial_engine.create_personalized_tutorial(
            user_id, topic, difficulty
        )
        
        return jsonify({
            "topic": topic,
            "difficulty": difficulty,
            "tutorial": tutorial_content,
            "estimated_time": len(tutorial_content.get('steps', [])) * 3  # 3분/단계
        })
        
    except Exception as e:
        logger.error(f"Tutorial generation error: {e}")
        return jsonify({"error": "튜토리얼 생성 중 오류가 발생했습니다"}), 500

@app.route('/api/v1/assessment/start', methods=['POST'])
def start_assessment():
    """평가 시작"""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "인증이 필요합니다"}), 401
    
    try:
        data = request.get_json()
        assessment_type = data.get('type', 'formative')
        topic = data.get('topic', 'statistics_basics')
        
        session_id = assessment_engine.start_assessment(
            user_id, assessment_type, topic
        )
        
        return jsonify({
            "success": True,
            "session_id": session_id,
            "message": "평가가 시작되었습니다"
        })
        
    except Exception as e:
        logger.error(f"Assessment start error: {e}")
        return jsonify({"error": "평가 시작 중 오류가 발생했습니다"}), 500

@app.route('/api/v1/assessment/submit', methods=['POST'])
def submit_assessment_answer():
    """평가 답안 제출"""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "인증이 필요합니다"}), 401
    
    try:
        data = request.get_json()
        session_id = data.get('session_id')
        user_answer = data.get('answer')
        time_taken = data.get('time_taken', 30)
        
        result = assessment_engine.submit_response(
            session_id, user_answer, time_taken
        )
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Assessment submission error: {e}")
        return jsonify({"error": "답안 제출 중 오류가 발생했습니다"}), 500

@app.route('/api/v1/interactive/content/<content_id>')
def get_interactive_content(content_id):
    """상호작용형 콘텐츠 조회"""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "인증이 필요합니다"}), 401
    
    try:
        content = interactive_content_engine.generate_interactive_content(
            content_id, user_id
        )
        
        return jsonify(content)
        
    except Exception as e:
        logger.error(f"Interactive content error: {e}")
        return jsonify({"error": "상호작용 콘텐츠 생성 중 오류가 발생했습니다"}), 500

@app.route('/api/v1/interactive/interact', methods=['POST'])
def process_interaction():
    """상호작용 처리"""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "인증이 필요합니다"}), 401
    
    try:
        data = request.get_json()
        session_id = data.get('session_id')
        interaction_data = data.get('interaction')
        
        result = interactive_content_engine.process_user_interaction(
            session_id, user_id, interaction_data
        )
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Interaction processing error: {e}")
        return jsonify({"error": "상호작용 처리 중 오류가 발생했습니다"}), 500

@app.route('/api/v1/certification/issue', methods=['POST'])
def issue_certificate():
    """인증서 발급"""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "인증이 필요합니다"}), 401
    
    try:
        data = request.get_json()
        certificate_type = data.get('type', 'basic_statistics')
        session_id = data.get('session_id')
        
        # 평가 세션 조회
        assessment_session = None
        for session in assessment_engine.completed_sessions:
            if session.session_id == session_id and session.user_id == user_id:
                assessment_session = session
                break
        
        if not assessment_session:
            return jsonify({"error": "유효한 평가 세션을 찾을 수 없습니다"}), 404
        
        certificate = certification_manager.issue_certificate(
            user_id, assessment_session, certificate_type
        )
        
        if certificate:
            return jsonify({
                "success": True,
                "certificate": certificate
            })
        else:
            return jsonify({
                "success": False,
                "message": "인증 요구사항을 충족하지 않습니다"
            }), 400
            
    except Exception as e:
        logger.error(f"Certificate issuance error: {e}")
        return jsonify({"error": "인증서 발급 중 오류가 발생했습니다"}), 500

@app.route('/api/v1/ml/train', methods=['POST'])
@limiter.limit("1 per hour")
def train_ml_models():
    """ML 모델 재훈련 (관리자 전용)"""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "인증이 필요합니다"}), 401
    
    # 실제 환경에서는 관리자 권한 확인 필요
    
    try:
        # 적응형 학습 엔진의 ML 모델 훈련
        training_result = adaptive_engine.train_ml_models()
        
        if training_result:
            return jsonify({
                "success": True,
                "message": "ML 모델이 성공적으로 훈련되었습니다",
                "model_performance": adaptive_engine.model_performance
            })
        else:
            return jsonify({
                "success": False,
                "message": "충분한 훈련 데이터가 없습니다"
            }), 400
            
    except Exception as e:
        logger.error(f"ML training error: {e}")
        return jsonify({"error": "ML 모델 훈련 중 오류가 발생했습니다"}), 500

# 에러 핸들러

@app.errorhandler(404)
def not_found(error):
    """404 에러 처리"""
    return jsonify({"error": "요청한 리소스를 찾을 수 없습니다"}), 404

@app.errorhandler(500)
def internal_error(error):
    """500 에러 처리"""
    logger.error(f"Internal server error: {error}")
    return jsonify({"error": "서버 내부 오류가 발생했습니다"}), 500

@app.errorhandler(429)
def ratelimit_handler(e):
    """Rate limit 에러 처리"""
    return jsonify({"error": "요청 한도를 초과했습니다. 잠시 후 다시 시도해주세요"}), 429

# 헬스 체크

@app.route('/health')
def health_check():
    """서버 상태 확인"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0",
        "users_count": len(USERS_DB),
        "ml_models_trained": any(
            perf['last_trained'] is not None 
            for perf in adaptive_engine.model_performance.values()
        )
    })

if __name__ == '__main__':
    # 개발 서버 실행
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    # 정적 파일 디렉토리 생성
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    os.makedirs('static/images', exist_ok=True)
    
    logger.info(f"Starting modern statistics learning platform on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)