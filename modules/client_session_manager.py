"""
클라이언트 사이드 세션 관리 시스템
- GitHub Pages 호환 (localStorage 사용)
- 세션 생성, 진행, 완료 관리
- 단계별 상태 추적 및 진행률 계산
"""

import json
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional, Union

class ClientSessionManager:
    """
    클라이언트 사이드 세션 관리 시스템
    localStorage를 사용하여 브라우저에서 세션 데이터를 관리합니다.
    """
    
    def __init__(self):
        """초기화"""
        self.storage_key = "learning_sessions"
        self.current_session_key = "current_session"
        
    def create_session(self, concept_id: str, user_id: str = "anonymous") -> Dict[str, Any]:
        """
        새 실습 세션 생성
        
        Args:
            concept_id (str): 학습 개념 ID
            user_id (str): 사용자 ID
            
        Returns:
            dict: 생성된 세션 정보
        """
        session_id = str(uuid.uuid4())
        now = datetime.now().isoformat()
        
        # 개념에 따른 단계 가져오기
        steps = self._get_steps_for_concept(concept_id)
        
        session_data = {
            "session_id": session_id,
            "concept_id": concept_id,
            "user_id": user_id,
            "created_at": now,
            "updated_at": now,
            "completed_at": None,
            "steps": steps,
            "current_step": 0,
            "progress": 0.0,
            "status": "in_progress",
            "history": []
        }
        
        # 세션 저장
        self._save_session(session_data)
        self._set_current_session(session_id)
        
        return session_data
    
    def get_session(self, session_id: str = None) -> Optional[Dict[str, Any]]:
        """
        세션 정보 조회
        
        Args:
            session_id (str, optional): 세션 ID (없으면 현재 세션)
            
        Returns:
            dict or None: 세션 정보
        """
        if session_id is None:
            session_id = self._get_current_session_id()
            
        if not session_id:
            return None
            
        sessions = self._load_all_sessions()
        return sessions.get(session_id)
    
    def get_current_step(self, session_id: str = None) -> Optional[Dict[str, Any]]:
        """현재 단계 정보 조회"""
        session_data = self.get_session(session_id)
        if not session_data:
            return None
        
        current_step_idx = session_data["current_step"]
        if current_step_idx >= len(session_data["steps"]):
            return None
        
        return session_data["steps"][current_step_idx]  
  
    def submit_step(self, code: str, output: str, session_id: str = None) -> Dict[str, Any]:
        """
        단계 제출 및 검증
        
        Args:
            code (str): 제출한 코드
            output (str): 코드 실행 결과
            session_id (str, optional): 세션 ID
            
        Returns:
            dict: 검증 결과
        """
        session_data = self.get_session(session_id)
        if not session_data:
            return {"success": False, "error": "세션을 찾을 수 없습니다."}
        
        current_step_idx = session_data["current_step"]
        if current_step_idx >= len(session_data["steps"]):
            return {"success": False, "error": "모든 단계를 완료했습니다."}
        
        current_step = session_data["steps"][current_step_idx]
        
        # 제출 기록
        submission = {
            "step_id": current_step["step_id"],
            "code": code,
            "output": output,
            "timestamp": datetime.now().isoformat()
        }
        
        # 검증
        verification_result = self._verify_step(current_step, code, output)
        submission.update(verification_result)
        
        # 히스토리에 추가
        session_data["history"].append(submission)
        
        # 성공 시 다음 단계로 이동
        if verification_result["success"]:
            current_step["status"] = "completed"
            current_step["completed_at"] = datetime.now().isoformat()
            
            # 다음 단계가 있으면 이동
            if current_step_idx + 1 < len(session_data["steps"]):
                session_data["current_step"] = current_step_idx + 1
                session_data["steps"][current_step_idx + 1]["status"] = "in_progress"
            else:
                # 모든 단계 완료
                session_data["status"] = "completed"
                session_data["completed_at"] = datetime.now().isoformat()
        
        # 진행률 업데이트
        completed_steps = sum(1 for step in session_data["steps"] if step["status"] == "completed")
        session_data["progress"] = (completed_steps / len(session_data["steps"])) * 100
        
        # 세션 업데이트 시간
        session_data["updated_at"] = datetime.now().isoformat()
        
        # 세션 저장
        self._save_session(session_data)
        
        return verification_result
    
    def get_session_progress(self, session_id: str = None) -> Optional[Dict[str, Any]]:
        """세션 진행률 조회"""
        session_data = self.get_session(session_id)
        if not session_data:
            return None
        
        completed_steps = sum(1 for step in session_data["steps"] if step["status"] == "completed")
        total_steps = len(session_data["steps"])
        progress_percentage = (completed_steps / total_steps * 100) if total_steps > 0 else 0
        
        return {
            "session_id": session_data["session_id"],
            "total_steps": total_steps,
            "completed_steps": completed_steps,
            "current_step": session_data["current_step"] + 1,  # 1-based for display
            "progress_percentage": round(progress_percentage, 1),
            "status": session_data["status"]
        }
    
    def get_hint(self, session_id: str = None) -> Dict[str, Any]:
        """현재 단계의 힌트 제공"""
        session_data = self.get_session(session_id)
        if not session_data:
            return {"success": False, "error": "세션을 찾을 수 없습니다."}
        
        current_step_idx = session_data["current_step"]
        if current_step_idx >= len(session_data["steps"]):
            return {"success": False, "error": "모든 단계를 완료했습니다."}
        
        current_step = session_data["steps"][current_step_idx]
        hints = current_step.get("hints", [])
        
        if not hints:
            return {"success": False, "message": "이 단계에는 힌트가 없습니다."}
        
        # 힌트 사용 기록
        hint_usage = {
            "step_id": current_step["step_id"],
            "timestamp": datetime.now().isoformat(),
            "action": "hint_requested"
        }
        session_data["history"].append(hint_usage)
        session_data["updated_at"] = datetime.now().isoformat()
        
        self._save_session(session_data)
        
        return {"success": True, "hints": hints}
    
    def reset_session(self, session_id: str = None) -> Dict[str, Any]:
        """세션 초기화"""
        session_data = self.get_session(session_id)
        if not session_data:
            return {"success": False, "error": "세션을 찾을 수 없습니다."}
        
        # 세션 상태 초기화
        session_data["current_step"] = 0
        session_data["progress"] = 0.0
        session_data["status"] = "in_progress"
        session_data["completed_at"] = None
        session_data["updated_at"] = datetime.now().isoformat()
        
        # 모든 단계 상태 초기화
        for i, step in enumerate(session_data["steps"]):
            if i == 0:
                step["status"] = "in_progress"
            else:
                step["status"] = "not_started"
            if "completed_at" in step:
                del step["completed_at"]
        
        self._save_session(session_data)
        
        return {"success": True, "message": "세션이 초기화되었습니다."}
    
    def export_session(self, session_id: str = None, format: str = "json") -> Dict[str, Any]:
        """세션 데이터 내보내기"""
        session_data = self.get_session(session_id)
        if not session_data:
            return {"success": False, "error": "세션을 찾을 수 없습니다."}
        
        if format == "json":
            return {
                "success": True,
                "data": session_data,
                "format": "json"
            }
        elif format == "summary":
            return {
                "success": True,
                "data": self._generate_session_summary(session_data),
                "format": "summary"
            }
        else:
            return {"success": False, "error": f"지원하지 않는 형식입니다: {format}"}    
  
  def _get_steps_for_concept(self, concept_id: str) -> List[Dict[str, Any]]:
        """개념에 따른 단계 정보 가져오기"""
        concept_steps = {
            "descriptive_stats": [
                {
                    "step_id": "data_preparation",
                    "title": "데이터 준비",
                    "description": "분석할 데이터를 준비합니다.",
                    "code_template": """# 데이터 준비
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
                    "expected_output": ["생성된 데이터 개수: 50", "처음 10개 데이터:"],
                    "hints": [
                        "numpy의 random.normal() 함수를 사용하여 정규분포 데이터를 생성할 수 있습니다.",
                        "np.random.seed()를 사용하면 매번 같은 난수를 생성할 수 있습니다.",
                        "print() 함수를 사용하여 데이터를 확인해보세요."
                    ],
                    "status": "in_progress"
                },
                {
                    "step_id": "central_tendency",
                    "title": "중심경향성 분석",
                    "description": "데이터의 중심경향성(평균, 중앙값, 최빈값)을 계산하고 비교합니다.",
                    "code_template": """# 중심경향성 분석
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
                    "expected_output": ["평균:", "중앙값:", "최빈값:"],
                    "hints": [
                        "numpy의 mean()과 median() 함수를 사용하여 평균과 중앙값을 계산할 수 있습니다.",
                        "scipy.stats의 mode() 함수를 사용하여 최빈값을 계산할 수 있습니다.",
                        "평균과 중앙값의 차이는 데이터의 치우침을 나타냅니다."
                    ],
                    "status": "not_started"
                },
                {
                    "step_id": "dispersion",
                    "title": "산포도 분석",
                    "description": "데이터의 산포도(범위, 분산, 표준편차, 사분위수 범위)를 계산하고 해석합니다.",
                    "code_template": """# 산포도 분석
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
}""",
                    "expected_output": ["범위:", "분산:", "표준편차:", "사분위수 범위(IQR):", "변동계수(CV):"],
                    "hints": [
                        "numpy의 var()와 std() 함수를 사용하여 분산과 표준편차를 계산할 수 있습니다.",
                        "numpy의 percentile() 함수를 사용하여 사분위수를 계산할 수 있습니다.",
                        "이상치는 일반적으로 Q1 - 1.5 * IQR보다 작거나 Q3 + 1.5 * IQR보다 큰 값으로 정의됩니다."
                    ],
                    "status": "not_started"
                },
                {
                    "step_id": "visualization",
                    "title": "데이터 시각화",
                    "description": "히스토그램과 박스플롯을 사용하여 데이터 분포를 시각화합니다.",
                    "code_template": """# 데이터 시각화
import numpy as np
import matplotlib.pyplot as plt

# 이전 단계에서 생성한 점수 데이터
np.random.seed(42)
scores = np.random.normal(loc=70, scale=15, size=50)

# 그래프 설정
plt.figure(figsize=(12, 5))

# 히스토그램
plt.subplot(1, 2, 1)
plt.hist(scores, bins=10, color='skyblue', edgecolor='black', alpha=0.7)
plt.axvline(np.mean(scores), color='red', linestyle='--', linewidth=2, label=f'평균: {np.mean(scores):.2f}')
plt.axvline(np.median(scores), color='green', linestyle='-.', linewidth=2, label=f'중앙값: {np.median(scores):.2f}')
plt.title('점수 분포 히스토그램')
plt.xlabel('점수')
plt.ylabel('빈도')
plt.legend()
plt.grid(alpha=0.3)

# 박스플롯
plt.subplot(1, 2, 2)
plt.boxplot(scores, vert=False, patch_artist=True, 
           boxprops=dict(facecolor='lightblue', color='black'),
           whiskerprops=dict(color='black'),
           medianprops=dict(color='red', linewidth=2))
plt.title('점수 분포 박스플롯')
plt.xlabel('점수')
plt.grid(alpha=0.3)

# 레이아웃 조정
plt.tight_layout()
plt.show()

# 결과 출력
print("데이터 시각화 완료!")
print(f"평균: {np.mean(scores):.2f}")
print(f"중앙값: {np.median(scores):.2f}")
print(f"표준편차: {np.std(scores):.2f}")

# 결과 반환
{
    'mean': np.mean(scores),
    'median': np.median(scores),
    'std_dev': np.std(scores)
}""",
                    "expected_output": ["데이터 시각화 완료!", "평균:", "중앙값:", "표준편차:"],
                    "hints": [
                        "matplotlib의 hist() 함수를 사용하여 히스토그램을 그릴 수 있습니다.",
                        "matplotlib의 boxplot() 함수를 사용하여 박스플롯을 그릴 수 있습니다.",
                        "plt.subplot()을 사용하여 여러 그래프를 한 화면에 표시할 수 있습니다."
                    ],
                    "status": "not_started"
                },
                {
                    "step_id": "interpretation",
                    "title": "결과 해석",
                    "description": "지금까지 분석한 결과를 종합하여 데이터의 특성을 해석합니다.",
                    "code_template": """# 결과 해석
import numpy as np
from scipy import stats

# 이전 단계에서 생성한 점수 데이터
np.random.seed(42)
scores = np.random.normal(loc=70, scale=15, size=50)

# 기술통계량 계산
mean = np.mean(scores)
median = np.median(scores)
std_dev = np.std(scores)
min_val = np.min(scores)
max_val = np.max(scores)
q1, q3 = np.percentile(scores, [25, 75])
iqr = q3 - q1

# 정규성 검정
shapiro_test = stats.shapiro(scores)
normal_p_value = shapiro_test[1]

# 종합 결과 출력
print("📊 데이터 분석 종합 결과")
print("=" * 40)
print(f"데이터 개수: {len(scores)}")
print(f"\\n🔸 중심경향성:")
print(f"   • 평균: {mean:.2f}")
print(f"   • 중앙값: {median:.2f}")
print(f"\\n🔸 산포도:")
print(f"   • 표준편차: {std_dev:.2f}")
print(f"   • 범위: {min_val:.2f} ~ {max_val:.2f}")
print(f"   • 사분위수 범위: {q1:.2f} ~ {q3:.2f}")
print(f"\\n🔸 분포 특성:")
print(f"   • 치우침: {'우측' if mean > median else '좌측' if mean < median else '없음'}")
print(f"   • 정규성 검정 p-값: {normal_p_value:.4f} ({'정규분포에 가까움' if normal_p_value > 0.05 else '정규분포가 아닐 수 있음'})")

# 해석 및 결론
print("\\n📝 해석 및 결론:")
if normal_p_value > 0.05:
    print("1. 이 데이터는 정규분포를 따르는 것으로 보입니다.")
    print("2. 평균과 표준편차를 사용하여 데이터를 요약하는 것이 적절합니다.")
    print(f"3. 약 68%의 데이터가 {mean - std_dev:.2f}~{mean + std_dev:.2f} 범위에 있을 것으로 예상됩니다.")
    print(f"4. 약 95%의 데이터가 {mean - 2*std_dev:.2f}~{mean + 2*std_dev:.2f} 범위에 있을 것으로 예상됩니다.")
else:
    print("1. 이 데이터는 정규분포를 따르지 않을 수 있습니다.")
    print("2. 중앙값과 사분위수를 사용하여 데이터를 요약하는 것이 더 적절할 수 있습니다.")
    print(f"3. 데이터의 50%가 {q1:.2f}~{q3:.2f} 범위에 있습니다.")

# 결과 반환
{
    'mean': mean,
    'median': median,
    'std_dev': std_dev,
    'normal_p_value': normal_p_value,
    'is_normal': normal_p_value > 0.05
}""",
                    "expected_output": ["📊 데이터 분석 종합 결과", "중심경향성:", "산포도:", "분포 특성:", "해석 및 결론:"],
                    "hints": [
                        "scipy.stats의 shapiro() 함수를 사용하여 정규성 검정을 수행할 수 있습니다.",
                        "정규분포에서는 평균 ± 1 표준편차 범위에 약 68%의 데이터가 포함됩니다.",
                        "정규분포에서는 평균 ± 2 표준편차 범위에 약 95%의 데이터가 포함됩니다."
                    ],
                    "status": "not_started"
                }
            ]
        }
        
        return concept_steps.get(concept_id, [])
    
    def _verify_step(self, step: Dict[str, Any], code: str, output: str) -> Dict[str, Any]:
        """단계 검증"""
        result = {
            "success": False,
            "message": "검증에 실패했습니다.",
            "details": []
        }
        
        # 예상 출력 확인
        expected_outputs = step.get("expected_output", [])
        output_check = all(expected in output for expected in expected_outputs)
        
        if output_check:
            result["success"] = True
            result["message"] = "단계를 성공적으로 완료했습니다!"
            result["details"].append("출력 확인: 성공")
        else:
            result["details"].append("출력 확인: 실패 (예상 출력이 포함되지 않음)")
        
        return result
    
    def _save_session(self, session_data: Dict[str, Any]):
        """세션 저장 (localStorage 시뮬레이션)"""
        sessions = self._load_all_sessions()
        sessions[session_data["session_id"]] = session_data
        # 실제 구현에서는 localStorage에 저장
        # localStorage.setItem(self.storage_key, JSON.stringify(sessions))
    
    def _load_all_sessions(self) -> Dict[str, Dict[str, Any]]:
        """모든 세션 로드 (localStorage 시뮬레이션)"""
        # 실제 구현에서는 localStorage에서 로드
        # return JSON.parse(localStorage.getItem(self.storage_key) || '{}')
        return {}
    
    def _set_current_session(self, session_id: str):
        """현재 세션 설정"""
        # localStorage.setItem(self.current_session_key, session_id)
        pass
    
    def _get_current_session_id(self) -> Optional[str]:
        """현재 세션 ID 가져오기"""
        # return localStorage.getItem(self.current_session_key)
        return None
    
    def _generate_session_summary(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """세션 요약 생성"""
        completed_steps = sum(1 for step in session_data["steps"] if step["status"] == "completed")
        total_steps = len(session_data["steps"])
        
        return {
            "session_id": session_data["session_id"],
            "concept_id": session_data["concept_id"],
            "user_id": session_data["user_id"],
            "created_at": session_data["created_at"],
            "status": session_data["status"],
            "progress": {
                "completed_steps": completed_steps,
                "total_steps": total_steps,
                "percentage": round((completed_steps / total_steps * 100) if total_steps > 0 else 0, 1)
            },
            "steps_summary": [
                {
                    "step_id": step["step_id"],
                    "title": step["title"],
                    "status": step["status"]
                }
                for step in session_data["steps"]
            ]
        }

# 클라이언트 세션 관리자 인스턴스 생성
client_session_manager = ClientSessionManager()