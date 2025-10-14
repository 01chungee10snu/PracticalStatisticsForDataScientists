"""
기술통계량 실습 과정
- 데이터 준비 → 중심경향성 → 산포도 → 시각화 → 해석 단계 구현
- 각 단계별 학습 목표와 성공 기준 정의
- 단계별 가이드 및 피드백 제공
"""

import os
import json
import uuid
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from typing import Dict, List, Any, Optional, Union, Tuple

from modules.session_management_system import session_manager
from modules.verification_hint_system import verification_system

class DescriptiveStatisticsPractice:
    """
    기술통계량 실습 과정
    단계별로 기술통계량 분석을 학습할 수 있는 실습 과정을 제공합니다.
    """
    
    def __init__(self):
        """초기화"""
        self.concept_id = "descriptive_stats"
        self.title = "기술통계량 분석 실습"
        self.description = "데이터 준비부터 결과 해석까지 단계별로 기술통계량 분석을 학습합니다."
        
        # 단계 정의
        self.steps = [
            {
                "step_id": "data_preparation",
                "title": "데이터 준비",
                "description": "분석할 데이터를 준비합니다.",
                "learning_objectives": [
                    "numpy를 사용하여 정규분포 데이터를 생성할 수 있다.",
                    "데이터의 기본 정보를 확인할 수 있다."
                ],
                "success_criteria": [
                    "numpy 라이브러리를 사용하여 정규분포 데이터를 생성한다.",
                    "생성된 데이터의 개수와 일부를 출력한다."
                ]
            },
            {
                "step_id": "central_tendency",
                "title": "중심경향성 분석",
                "description": "데이터의 중심경향성(평균, 중앙값, 최빈값)을 계산하고 비교합니다.",
                "learning_objectives": [
                    "평균, 중앙값, 최빈값을 계산할 수 있다.",
                    "중심경향성 측도들의 차이점을 이해할 수 있다.",
                    "데이터의 치우침을 판단할 수 있다."
                ],
                "success_criteria": [
                    "numpy와 scipy를 사용하여 평균, 중앙값, 최빈값을 계산한다.",
                    "평균과 중앙값의 차이를 통해 데이터의 치우침을 해석한다."
                ]
            },
            {
                "step_id": "dispersion",
                "title": "산포도 분석",
                "description": "데이터의 산포도(범위, 분산, 표준편차, 사분위수 범위)를 계산하고 해석합니다.",
                "learning_objectives": [
                    "범위, 분산, 표준편차, 사분위수 범위를 계산할 수 있다.",
                    "변동계수를 계산하여 상대적 변동성을 평가할 수 있다.",
                    "이상치를 탐지할 수 있다."
                ],
                "success_criteria": [
                    "numpy를 사용하여 다양한 산포도 측도를 계산한다.",
                    "변동계수를 계산하여 데이터의 변동성을 해석한다.",
                    "사분위수 범위를 사용하여 이상치를 탐지한다."
                ]
            },
            {
                "step_id": "visualization",
                "title": "데이터 시각화",
                "description": "히스토그램과 박스플롯을 사용하여 데이터 분포를 시각화합니다.",
                "learning_objectives": [
                    "matplotlib을 사용하여 히스토그램을 그릴 수 있다.",
                    "matplotlib을 사용하여 박스플롯을 그릴 수 있다.",
                    "시각화를 통해 데이터의 분포 특성을 파악할 수 있다."
                ],
                "success_criteria": [
                    "히스토그램과 박스플롯을 그린다.",
                    "그래프에 제목, 축 레이블, 범례를 추가한다.",
                    "평균과 중앙값을 히스토그램에 표시한다."
                ]
            },
            {
                "step_id": "interpretation",
                "title": "결과 해석",
                "description": "지금까지 분석한 결과를 종합하여 데이터의 특성을 해석합니다.",
                "learning_objectives": [
                    "정규성 검정을 수행할 수 있다.",
                    "기술통계량을 종합하여 데이터의 특성을 해석할 수 있다.",
                    "실무적 관점에서 데이터의 의미를 해석할 수 있다."
                ],
                "success_criteria": [
                    "scipy.stats를 사용하여 정규성 검정을 수행한다.",
                    "기술통계량을 종합하여 데이터의 특성을 해석한다.",
                    "실무적 관점에서 결과를 해석한다."
                ]
            }
        ]
        
        # 코드 템플릿
        self.code_templates = {
            "data_preparation": """# 데이터 준비
import numpy as np

# 학생 시험 점수 데이터 생성 (평균 70, 표준편차 15인 정규분포)
np.random.seed(42)  # 재현성을 위한 시드 설정
scores = np.random.normal(loc=70, scale=15, size=50)

# 데이터 확인
print(f"생성된 데이터 개수: {len(scores)}")
print("처음 10개 데이터:")
print(scores[:10])

# 데이터 반환
scores""",
            "central_tendency": """# 중심경향성 분석
import numpy as np
from scipy import stats

# 이전 단계에서 생성한 점수 데이터
np.random.seed(42)
scores = np.random.normal(loc=70, scale=15, size=50)

# 중심경향성 계산
mean = np.mean(scores)
median = np.median(scores)
mode = stats.mode(scores)[0][0]  # scipy의 mode 함수 사용

# 결과 출력
print(f"평균: {mean:.2f}")
print(f"중앙값: {median:.2f}")
print(f"최빈값: {mode:.2f}")

# 평균과 중앙값 비교
if mean > median:
    print("\\n평균이 중앙값보다 크므로, 데이터가 오른쪽으로 치우쳐 있을 가능성이 있습니다.")
elif mean < median:
    print("\\n평균이 중앙값보다 작으므로, 데이터가 왼쪽으로 치우쳐 있을 가능성이 있습니다.")
else:
    print("\\n평균과 중앙값이 같으므로, 데이터가 대칭적일 가능성이 높습니다.")

# 결과 반환
{
    'mean': mean,
    'median': median,
    'mode': mode
}""",
            "dispersion": """# 산포도 분석
import numpy as np

# 이전 단계에서 생성한 점수 데이터
np.random.seed(42)
scores = np.random.normal(loc=70, scale=15, size=50)

# 산포도 계산
data_range = np.max(scores) - np.min(scores)
variance = np.var(scores)
std_dev = np.std(scores)
q1, q3 = np.percentile(scores, [25, 75])
iqr = q3 - q1

# 결과 출력
print(f"범위: {data_range:.2f}")
print(f"분산: {variance:.2f}")
print(f"표준편차: {std_dev:.2f}")
print(f"1사분위수(Q1): {q1:.2f}")
print(f"3사분위수(Q3): {q3:.2f}")
print(f"사분위수 범위(IQR): {iqr:.2f}")

# 변동계수 계산 (표준편차/평균)
cv = std_dev / np.mean(scores)
print(f"\\n변동계수(CV): {cv:.4f}")

if cv < 0.1:
    print("변동계수가 0.1보다 작으므로, 데이터의 변동성이 낮습니다.")
elif cv > 0.3:
    print("변동계수가 0.3보다 크므로, 데이터의 변동성이 높습니다.")
else:
    print("변동계수가 중간 정도로, 데이터가 적절한 변동성을 가지고 있습니다.")

# 이상치 탐지
lower_bound = q1 - 1.5 * iqr
upper_bound = q3 + 1.5 * iqr
outliers = scores[(scores < lower_bound) | (scores > upper_bound)]

print(f"\\n이상치 경계: {lower_bound:.2f} ~ {upper_bound:.2f}")
print(f"이상치 개수: {len(outliers)}")
if len(outliers) > 0:
    print(f"이상치: {outliers}")

# 결과 반환
{
    'range': data_range,
    'variance': variance,
    'std_dev': std_dev,
    'iqr': iqr,
    'cv': cv,
    'outliers': outliers
}"""
        }
    
    def start_practice(self, user_id: str = "anonymous") -> Dict[str, Any]:
        """
        실습 시작
        
        Args:
            user_id (str): 사용자 ID (익명 가능)
            
        Returns:
            dict: 세션 정보
        """
        # 세션 생성
        session = session_manager.create_session(self.concept_id, user_id)
        
        # 첫 단계 정보 가져오기
        current_step = session_manager.get_current_step(session["session_id"])
        
        # 코드 템플릿 추가
        if current_step and current_step["step_id"] in self.code_templates:
            current_step["code_template"] = self.code_templates[current_step["step_id"]]
        
        return {
            "success": True,
            "session_id": session["session_id"],
            "title": self.title,
            "description": self.description,
            "current_step": current_step,
            "total_steps": len(self.steps),
            "progress": session["progress"]
        }    
def continue_practice(self, session_id: str) -> Dict[str, Any]:
        """
        실습 계속하기
        
        Args:
            session_id (str): 세션 ID
            
        Returns:
            dict: 세션 정보
        """
        # 세션 정보 가져오기
        session = session_manager.get_session(session_id)
        if not session:
            return {
                "success": False,
                "error": "세션을 찾을 수 없습니다."
            }
        
        # 현재 단계 정보 가져오기
        current_step = session_manager.get_current_step(session_id)
        
        # 코드 템플릿 추가
        if current_step and current_step["step_id"] in self.code_templates:
            current_step["code_template"] = self.code_templates[current_step["step_id"]]
        
        return {
            "success": True,
            "session_id": session_id,
            "title": self.title,
            "description": self.description,
            "current_step": current_step,
            "total_steps": len(self.steps),
            "progress": session["progress"]
        }
    
    def submit_step(self, session_id: str, code: str, output: str) -> Dict[str, Any]:
        """
        단계 제출 및 검증
        
        Args:
            session_id (str): 세션 ID
            code (str): 제출한 코드
            output (str): 코드 실행 결과
            
        Returns:
            dict: 검증 결과
        """
        # 세션 정보 가져오기
        session = session_manager.get_session(session_id)
        if not session:
            return {
                "success": False,
                "error": "세션을 찾을 수 없습니다."
            }
        
        # 현재 단계 정보 가져오기
        current_step = session_manager.get_current_step(session_id)
        if not current_step:
            return {
                "success": False,
                "error": "현재 단계를 찾을 수 없습니다."
            }
        
        # 단계 검증
        verification_result = verification_system.verify_step(
            self.concept_id, current_step["step_id"], code, output
        )
        
        # 피드백 생성
        feedback = verification_system.generate_feedback(verification_result)
        verification_result["feedback"] = feedback
        
        # 성공 시 다음 단계로 이동
        if verification_result["success"]:
            session_result = session_manager.submit_step(session_id, code, output)
            
            # 다음 단계 정보 가져오기
            next_step = session_manager.get_current_step(session_id)
            if next_step and next_step["step_id"] in self.code_templates:
                next_step["code_template"] = self.code_templates[next_step["step_id"]]
            
            verification_result["next_step"] = next_step
            
            # 모든 단계 완료 확인
            session = session_manager.get_session(session_id)
            verification_result["progress"] = session["progress"]
            verification_result["completed"] = session["status"] == "completed"
        
        return verification_result
    
    def get_hint(self, session_id: str) -> Dict[str, Any]:
        """
        힌트 제공
        
        Args:
            session_id (str): 세션 ID
            
        Returns:
            dict: 힌트 정보
        """
        # 세션 정보 가져오기
        session = session_manager.get_session(session_id)
        if not session:
            return {
                "success": False,
                "error": "세션을 찾을 수 없습니다."
            }
        
        # 현재 단계 정보 가져오기
        current_step = session_manager.get_current_step(session_id)
        if not current_step:
            return {
                "success": False,
                "error": "현재 단계를 찾을 수 없습니다."
            }
        
        # 힌트 제공
        hint_result = verification_system.provide_hints(self.concept_id, current_step["step_id"])
        
        # 힌트 사용 기록
        session_manager.get_hint(session_id)
        
        return {
            "success": True,
            "step_id": current_step["step_id"],
            "title": current_step["title"],
            "hints": hint_result["hints"],
            "code_suggestions": hint_result.get("code_suggestions", []),
            "resources": hint_result.get("resources", [])
        }
    
    def skip_step(self, session_id: str) -> Dict[str, Any]:
        """
        단계 건너뛰기
        
        Args:
            session_id (str): 세션 ID
            
        Returns:
            dict: 결과
        """
        # 단계 건너뛰기
        result = session_manager.skip_step(session_id)
        
        # 다음 단계 정보 가져오기
        if result["success"] and "next_step" in result:
            next_step = result["next_step"]
            if next_step and next_step["step_id"] in self.code_templates:
                next_step["code_template"] = self.code_templates[next_step["step_id"]]
        
        return result
    
    def reset_step(self, session_id: str) -> Dict[str, Any]:
        """
        단계 초기화
        
        Args:
            session_id (str): 세션 ID
            
        Returns:
            dict: 결과
        """
        # 단계 초기화
        result = session_manager.reset_step(session_id)
        
        # 현재 단계 정보 가져오기
        if result["success"] and "current_step" in result:
            current_step = result["current_step"]
            if current_step and current_step["step_id"] in self.code_templates:
                current_step["code_template"] = self.code_templates[current_step["step_id"]]
        
        return result    def get
_session_summary(self, session_id: str) -> Dict[str, Any]:
        """
        세션 요약 정보 조회
        
        Args:
            session_id (str): 세션 ID
            
        Returns:
            dict: 세션 요약 정보
        """
        return session_manager.get_session_summary(session_id)
    
    def export_session(self, session_id: str, format: str = "json") -> Dict[str, Any]:
        """
        세션 데이터 내보내기
        
        Args:
            session_id (str): 세션 ID
            format (str): 내보내기 형식 (json, html, csv)
            
        Returns:
            dict: 내보내기 결과
        """
        return session_manager.export_session(session_id, format)
    
    def get_learning_objectives(self, step_id: str) -> List[str]:
        """
        단계별 학습 목표 조회
        
        Args:
            step_id (str): 단계 ID
            
        Returns:
            list: 학습 목표 목록
        """
        for step in self.steps:
            if step["step_id"] == step_id:
                return step.get("learning_objectives", [])
        
        return []
    
    def get_success_criteria(self, step_id: str) -> List[str]:
        """
        단계별 성공 기준 조회
        
        Args:
            step_id (str): 단계 ID
            
        Returns:
            list: 성공 기준 목록
        """
        for step in self.steps:
            if step["step_id"] == step_id:
                return step.get("success_criteria", [])
        
        return []
    
    def generate_practice_html(self, session_id: str = None) -> str:
        """
        실습 HTML 생성
        
        Args:
            session_id (str, optional): 세션 ID
            
        Returns:
            str: HTML 문자열
        """
        # 기본 HTML 템플릿
        html = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>기술통계량 분석 실습</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            padding-top: 56px;
        }
        
        .step-indicator {
            display: flex;
            justify-content: space-between;
            margin-bottom: 2rem;
        }
        
        .step {
            flex: 1;
            text-align: center;
            padding: 0.5rem;
            border-bottom: 3px solid #ddd;
            position: relative;
        }
        
        .step.active {
            border-color: #3498db;
            color: #3498db;
            font-weight: 600;
        }
        
        .step.completed {
            border-color: #2ecc71;
            color: #2ecc71;
        }
        
        .code-editor {
            border-radius: 8px;
            overflow: hidden;
            margin-bottom: 1rem;
        }
        
        .code-toolbar {
            background-color: #f5f5f5;
            padding: 0.5rem;
            border-bottom: 1px solid #ddd;
        }
        
        .code-output {
            background-color: #f8f8f8;
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 1rem;
            font-family: monospace;
            white-space: pre-wrap;
            min-height: 100px;
            max-height: 300px;
            overflow-y: auto;
        }
        
        .feedback {
            background-color: #f0f8ff;
            border: 1px solid #b8daff;
            border-radius: 8px;
            padding: 1rem;
            margin-top: 1rem;
        }
        
        .hint-container {
            background-color: #fff3cd;
            border: 1px solid #ffeeba;
            border-radius: 8px;
            padding: 1rem;
            margin-top: 1rem;
        }
        
        .objectives-container {
            background-color: #e8f4f8;
            border: 1px solid #b8daff;
            border-radius: 8px;
            padding: 1rem;
            margin-top: 1rem;
        }
    </style>
</head>
<body>
    <!-- 네비게이션 바 -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark fixed-top">
        <div class="container">
            <a class="navbar-brand" href="#">📊 기술통계량 분석 실습</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="#" id="export-session">결과 내보내기</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <div class="container mt-4">
        <h1 class="mb-4">기술통계량 분석 실습</h1>
        <p class="lead">데이터 준비부터 결과 해석까지 단계별로 기술통계량 분석을 학습합니다.</p>
        
        <!-- 단계 표시기 -->
        <div class="step-indicator mb-4">
            <div class="step" id="step-1">1. 데이터 준비</div>
            <div class="step" id="step-2">2. 중심경향성</div>
            <div class="step" id="step-3">3. 산포도</div>
            <div class="step" id="step-4">4. 시각화</div>
            <div class="step" id="step-5">5. 해석</div>
        </div>
        
        <!-- 현재 단계 -->
        <div id="current-step-container">
            <div class="card mb-4">
                <div class="card-header">
                    <h2 id="step-title">단계 제목</h2>
                </div>
                <div class="card-body">
                    <p id="step-description">단계 설명</p>
                    
                    <!-- 학습 목표 및 성공 기준 -->
                    <div class="objectives-container mb-4">
                        <h4>학습 목표</h4>
                        <ul id="learning-objectives">
                            <!-- 학습 목표 목록 -->
                        </ul>
                        
                        <h4>성공 기준</h4>
                        <ul id="success-criteria">
                            <!-- 성공 기준 목록 -->
                        </ul>
                    </div>
                    
                    <!-- 코드 에디터 -->
                    <div class="code-editor mb-4">
                        <div class="code-toolbar">
                            <button class="btn btn-primary" id="run-code">▶️ 실행</button>
                            <button class="btn btn-secondary" id="reset-code">🔄 초기화</button>
                            <button class="btn btn-warning" id="get-hint">💡 힌트</button>
                            <button class="btn btn-danger" id="skip-step">⏭️ 건너뛰기</button>
                        </div>
                        <textarea id="code-editor" class="form-control" rows="15"></textarea>
                    </div>
                    
                    <!-- 코드 출력 -->
                    <h4>실행 결과</h4>
                    <div class="code-output" id="code-output">
                        <!-- 코드 실행 결과 -->
                    </div>
                    
                    <!-- 피드백 -->
                    <div class="feedback mt-4" id="feedback-container" style="display: none;">
                        <h4>피드백</h4>
                        <div id="feedback-content"></div>
                        
                        <div class="mt-3" id="next-step-container" style="display: none;">
                            <button class="btn btn-success" id="next-step">다음 단계로</button>
                        </div>
                    </div>
                    
                    <!-- 힌트 -->
                    <div class="hint-container mt-4" id="hint-container" style="display: none;">
                        <h4>힌트</h4>
                        <div id="hint-content"></div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- 완료 메시지 -->
        <div id="completion-container" style="display: none;">
            <div class="card">
                <div class="card-body text-center">
                    <h2>🎉 축하합니다!</h2>
                    <p class="lead">기술통계량 분석 실습을 모두 완료했습니다.</p>
                    <button class="btn btn-primary" id="export-result">결과 내보내기</button>
                    <button class="btn btn-success" id="restart-practice">다시 시작하기</button>
                </div>
            </div>
        </div>
    </div>

    <!-- 스크립트 -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        // 실습 세션 관리
        const practiceSession = {
            sessionId: null,
            currentStep: null,
            totalSteps: 5,
            progress: 0
        };
        
        // 페이지 로드 시 실행
        document.addEventListener('DOMContentLoaded', function() {
            // 세션 ID가 있으면 계속하기, 없으면 새로 시작
            const sessionId = localStorage.getItem('practiceSessionId');
            if (sessionId) {
                continuePractice(sessionId);
            } else {
                startPractice();
            }
            
            // 이벤트 리스너 등록
            document.getElementById('run-code').addEventListener('click', runCode);
            document.getElementById('reset-code').addEventListener('click', resetCode);
            document.getElementById('get-hint').addEventListener('click', getHint);
            document.getElementById('skip-step').addEventListener('click', skipStep);
            document.getElementById('export-session').addEventListener('click', exportSession);
            document.getElementById('export-result').addEventListener('click', exportSession);
            document.getElementById('restart-practice').addEventListener('click', restartPractice);
        });
        
        // 실습 시작
        async function startPractice() {
            try {
                const response = await fetch('/api/practice/start', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });
                
                const data = await response.json();
                if (data.success) {
                    practiceSession.sessionId = data.session_id;
                    practiceSession.totalSteps = data.total_steps;
                    practiceSession.progress = data.progress;
                    
                    // 세션 ID 저장
                    localStorage.setItem('practiceSessionId', data.session_id);
                    
                    // 현재 단계 표시
                    updateCurrentStep(data.current_step);
                    updateStepIndicator();
                } else {
                    showError(data.error || '실습을 시작하는 데 문제가 발생했습니다.');
                }
            } catch (error) {
                showError('서버 연결에 실패했습니다.');
                console.error(error);
            }
        }
        
        // 실습 계속하기
        async function continuePractice(sessionId) {
            try {
                const response = await fetch(`/api/practice/continue/${sessionId}`, {
                    method: 'GET'
                });
                
                const data = await response.json();
                if (data.success) {
                    practiceSession.sessionId = data.session_id;
                    practiceSession.totalSteps = data.total_steps;
                    practiceSession.progress = data.progress;
                    
                    // 현재 단계 표시
                    updateCurrentStep(data.current_step);
                    updateStepIndicator();
                    
                    // 모든 단계 완료 확인
                    if (!data.current_step) {
                        showCompletionMessage();
                    }
                } else {
                    showError(data.error || '실습을 계속하는 데 문제가 발생했습니다.');
                    // 세션이 만료되었을 수 있으므로 새로 시작
                    localStorage.removeItem('practiceSessionId');
                    startPractice();
                }
            } catch (error) {
                showError('서버 연결에 실패했습니다.');
                console.error(error);
            }
        }
        
        // 코드 실행
        async function runCode() {
            const code = document.getElementById('code-editor').value;
            if (!code.trim()) {
                showError('실행할 코드를 입력하세요.');
                return;
            }
            
            try {
                // 코드 실행 (실제로는 서버에 요청)
                const output = await executeCode(code);
                
                // 결과 표시
                document.getElementById('code-output').textContent = output;
                
                // 단계 제출
                submitStep(code, output);
            } catch (error) {
                showError('코드 실행에 실패했습니다.');
                console.error(error);
            }
        }
        
        // 코드 실행 (서버에 요청)
        async function executeCode(code) {
            // 실제로는 서버에 요청하여 코드 실행
            // 여기서는 간단히 시뮬레이션
            return `코드 실행 결과:\n${code}\n\n실행 완료`;
        }
        
        // 단계 제출
        async function submitStep(code, output) {
            try {
                const response = await fetch(`/api/practice/submit/${practiceSession.sessionId}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        code: code,
                        output: output
                    })
                });
                
                const data = await response.json();
                
                // 피드백 표시
                document.getElementById('feedback-container').style.display = 'block';
                document.getElementById('feedback-content').innerHTML = data.feedback || '';
                
                // 성공 시 다음 단계 버튼 표시
                if (data.success) {
                    document.getElementById('next-step-container').style.display = 'block';
                    document.getElementById('next-step').addEventListener('click', function() {
                        // 다음 단계로 이동
                        if (data.next_step) {
                            updateCurrentStep(data.next_step);
                        } else {
                            showCompletionMessage();
                        }
                        
                        // 진행 상황 업데이트
                        practiceSession.progress = data.progress;
                        updateStepIndicator();
                        
                        // 피드백 숨기기
                        document.getElementById('feedback-container').style.display = 'none';
                    });
                } else {
                    document.getElementById('next-step-container').style.display = 'none';
                }
            } catch (error) {
                showError('단계 제출에 실패했습니다.');
                console.error(error);
            }
        }
        
        // 코드 초기화
        function resetCode() {
            if (practiceSession.currentStep && practiceSession.currentStep.code_template) {
                document.getElementById('code-editor').value = practiceSession.currentStep.code_template;
            } else {
                document.getElementById('code-editor').value = '';
            }
            
            // 피드백 숨기기
            document.getElementById('feedback-container').style.display = 'none';
            document.getElementById('hint-container').style.display = 'none';
        }
        
        // 힌트 가져오기
        async function getHint() {
            try {
                const response = await fetch(`/api/practice/hint/${practiceSession.sessionId}`, {
                    method: 'GET'
                });
                
                const data = await response.json();
                if (data.success) {
                    // 힌트 표시
                    document.getElementById('hint-container').style.display = 'block';
                    
                    let hintContent = '<ul>';
                    data.hints.forEach(hint => {
                        hintContent += `<li>${hint}</li>`;
                    });
                    hintContent += '</ul>';
                    
                    // 코드 제안이 있으면 추가
                    if (data.code_suggestions && data.code_suggestions.length > 0) {
                        hintContent += '<h5>코드 제안:</h5>';
                        hintContent += '<pre>';
                        data.code_suggestions.forEach(suggestion => {
                            hintContent += suggestion + '\n';
                        });
                        hintContent += '</pre>';
                    }
                    
                    // 참고 자료가 있으면 추가
                    if (data.resources && data.resources.length > 0) {
                        hintContent += '<h5>참고 자료:</h5>';
                        hintContent += '<ul>';
                        data.resources.forEach(resource => {
                            hintContent += `<li><a href="${resource.url}" target="_blank">${resource.title}</a></li>`;
                        });
                        hintContent += '</ul>';
                    }
                    
                    document.getElementById('hint-content').innerHTML = hintContent;
                } else {
                    showError(data.error || '힌트를 가져오는 데 문제가 발생했습니다.');
                }
            } catch (error) {
                showError('서버 연결에 실패했습니다.');
                console.error(error);
            }
        }
        
        // 단계 건너뛰기
        async function skipStep() {
            if (!confirm('정말 이 단계를 건너뛰시겠습니까?')) {
                return;
            }
            
            try {
                const response = await fetch(`/api/practice/skip/${practiceSession.sessionId}`, {
                    method: 'POST'
                });
                
                const data = await response.json();
                if (data.success) {
                    // 다음 단계로 이동
                    if (data.next_step) {
                        updateCurrentStep(data.next_step);
                    } else {
                        showCompletionMessage();
                    }
                    
                    // 진행 상황 업데이트
                    practiceSession.progress = data.progress;
                    updateStepIndicator();
                    
                    // 피드백 숨기기
                    document.getElementById('feedback-container').style.display = 'none';
                    document.getElementById('hint-container').style.display = 'none';
                } else {
                    showError(data.error || '단계를 건너뛰는 데 문제가 발생했습니다.');
                }
            } catch (error) {
                showError('서버 연결에 실패했습니다.');
                console.error(error);
            }
        }
        
        // 세션 내보내기
        async function exportSession() {
            try {
                const response = await fetch(`/api/practice/export/${practiceSession.sessionId}?format=html`, {
                    method: 'GET'
                });
                
                const data = await response.json();
                if (data.success) {
                    // 파일 다운로드
                    const a = document.createElement('a');
                    a.href = `/exports/${data.filename}`;
                    a.download = data.filename;
                    document.body.appendChild(a);
                    a.click();
                    document.body.removeChild(a);
                } else {
                    showError(data.error || '세션을 내보내는 데 문제가 발생했습니다.');
                }
            } catch (error) {
                showError('서버 연결에 실패했습니다.');
                console.error(error);
            }
        }
        
        // 실습 다시 시작
        function restartPractice() {
            if (confirm('정말 처음부터 다시 시작하시겠습니까?')) {
                localStorage.removeItem('practiceSessionId');
                startPractice();
                document.getElementById('completion-container').style.display = 'none';
                document.getElementById('current-step-container').style.display = 'block';
            }
        }
        
        // 현재 단계 업데이트
        function updateCurrentStep(step) {
            if (!step) {
                showCompletionMessage();
                return;
            }
            
            practiceSession.currentStep = step;
            
            // 단계 정보 업데이트
            document.getElementById('step-title').textContent = step.title;
            document.getElementById('step-description').textContent = step.description;
            
            // 코드 에디터 업데이트
            if (step.code_template) {
                document.getElementById('code-editor').value = step.code_template;
            } else {
                document.getElementById('code-editor').value = '';
            }
            
            // 코드 출력 초기화
            document.getElementById('code-output').textContent = '';
            
            // 피드백 숨기기
            document.getElementById('feedback-container').style.display = 'none';
            document.getElementById('hint-container').style.display = 'none';
            
            // 학습 목표 및 성공 기준 업데이트
            updateLearningObjectives(step.step_id);
            updateSuccessCriteria(step.step_id);
            
            // 단계 표시기 업데이트
            updateStepIndicator();
        }
        
        // 학습 목표 업데이트
        async function updateLearningObjectives(stepId) {
            try {
                const response = await fetch(`/api/practice/objectives/${stepId}`, {
                    method: 'GET'
                });
                
                const data = await response.json();
                if (data.success) {
                    const objectivesList = document.getElementById('learning-objectives');
                    objectivesList.innerHTML = '';
                    
                    data.objectives.forEach(objective => {
                        const li = document.createElement('li');
                        li.textContent = objective;
                        objectivesList.appendChild(li);
                    });
                }
            } catch (error) {
                console.error('학습 목표를 가져오는 데 실패했습니다:', error);
            }
        }
        
        // 성공 기준 업데이트
        async function updateSuccessCriteria(stepId) {
            try {
                const response = await fetch(`/api/practice/criteria/${stepId}`, {
                    method: 'GET'
                });
                
                const data = await response.json();
                if (data.success) {
                    const criteriaList = document.getElementById('success-criteria');
                    criteriaList.innerHTML = '';
                    
                    data.criteria.forEach(criterion => {
                        const li = document.createElement('li');
                        li.textContent = criterion;
                        criteriaList.appendChild(li);
                    });
                }
            } catch (error) {
                console.error('성공 기준을 가져오는 데 실패했습니다:', error);
            }
        }
        
        // 단계 표시기 업데이트
        function updateStepIndicator() {
            // 현재 단계 인덱스 (0부터 시작)
            const currentStepIndex = practiceSession.currentStep ? 
                ['data_preparation', 'central_tendency', 'dispersion', 'visualization', 'interpretation']
                .indexOf(practiceSession.currentStep.step_id) : -1;
            
            // 모든 단계 요소
            const stepElements = document.querySelectorAll('.step');
            
            // 각 단계 상태 업데이트
            stepElements.forEach((element, index) => {
                element.classList.remove('active', 'completed');
                
                if (index < currentStepIndex) {
                    element.classList.add('completed');
                } else if (index === currentStepIndex) {
                    element.classList.add('active');
                }
            });
        }
        
        // 완료 메시지 표시
        function showCompletionMessage() {
            document.getElementById('current-step-container').style.display = 'none';
            document.getElementById('completion-container').style.display = 'block';
        }
        
        // 오류 메시지 표시
        function showError(message) {
            alert(message);
        }
    </script>
</body>
</html>
"""
        
        return html


# 기술통계량 실습 인스턴스 생성
descriptive_stats_practice = DescriptiveStatisticsPractice()