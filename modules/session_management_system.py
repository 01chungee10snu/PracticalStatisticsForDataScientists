"""
실습 세션 관리 시스템
- 세션 생성, 진행, 완료 관리
- 단계별 상태 추적 및 진행률 계산
- 세션 데이터 저장 및 로드
"""

import os
import json
import uuid
import time
from datetime import datetime
from typing import Dict, List, Any, Optional, Union, Tuple

class SessionManagementSystem:
    """
    실습 세션 관리 시스템
    사용자의 학습 세션을 관리하고, 단계별 진행 상황을 추적합니다.
    """
    
    def __init__(self, session_dir: str = "sessions"):
        """
        초기화
        
        Args:
            session_dir (str): 세션 데이터를 저장할 디렉토리
        """
        self.session_dir = session_dir
        self.active_sessions = {}  # 현재 활성화된 세션 (메모리에 유지)
        
        # 세션 디렉토리 생성
        os.makedirs(self.session_dir, exist_ok=True)
    
    def create_session(self, concept_id: str, user_id: str = "anonymous") -> Dict[str, Any]:
        """
        새 실습 세션 생성
        
        Args:
            concept_id (str): 학습 개념 ID
            user_id (str): 사용자 ID (익명 가능)
            
        Returns:
            dict: 생성된 세션 정보
        """
        # 세션 ID 생성
        session_id = str(uuid.uuid4())
        
        # 현재 시간
        now = datetime.now().isoformat()
        
        # 개념에 따른 단계 가져오기
        steps = self._get_steps_for_concept(concept_id)
        
        # 세션 데이터 생성
        session_data = {
            "session_id": session_id,
            "concept_id": concept_id,
            "user_id": user_id,
            "created_at": now,
            "updated_at": now,
            "completed_at": None,
            "steps": steps,
            "current_step": 0,
            "progress": 0.0,  # 0-100%
            "status": "in_progress",  # in_progress, completed, abandoned
            "history": []
        }
        
        # 세션 저장
        self.active_sessions[session_id] = session_data
        self._save_session(session_data)
        
        return session_data
    
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        세션 정보 조회
        
        Args:
            session_id (str): 세션 ID
            
        Returns:
            dict or None: 세션 정보 (없으면 None)
        """
        # 메모리에서 조회
        if session_id in self.active_sessions:
            return self.active_sessions[session_id]
        
        # 파일에서 로드
        session_data = self._load_session(session_id)
        if session_data:
            # 메모리에 캐싱
            self.active_sessions[session_id] = session_data
        
        return session_data
    
    def get_current_step(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        현재 단계 정보 조회
        
        Args:
            session_id (str): 세션 ID
            
        Returns:
            dict or None: 현재 단계 정보 (없으면 None)
        """
        session_data = self.get_session(session_id)
        if not session_data:
            return None
        
        current_step_idx = session_data["current_step"]
        if current_step_idx >= len(session_data["steps"]):
            return None
        
        return session_data["steps"][current_step_idx]
    
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
        
    def skip_step(self, session_id: str) -> Dict[str, Any]:
        """
        현재 단계 건너뛰기
        
        Args:
            session_id (str): 세션 ID
            
        Returns:
            dict: 결과
        """
        session_data = self.get_session(session_id)
        if not session_data:
            return {"success": False, "error": "세션을 찾을 수 없습니다."}
        
        current_step_idx = session_data["current_step"]
        if current_step_idx >= len(session_data["steps"]):
            return {"success": False, "error": "모든 단계를 완료했습니다."}
        
        current_step = session_data["steps"][current_step_idx]
        
        # 현재 단계 건너뛰기
        current_step["status"] = "skipped"
        
        # 다음 단계가 있으면 이동
        if current_step_idx + 1 < len(session_data["steps"]):
            session_data["current_step"] = current_step_idx + 1
            session_data["steps"][current_step_idx + 1]["status"] = "in_progress"
        else:
            # 모든 단계 완료
            session_data["status"] = "completed"
            session_data["completed_at"] = datetime.now().isoformat()
        
        # 진행률 업데이트
        completed_steps = sum(1 for step in session_data["steps"] if step["status"] in ["completed", "skipped"])
        session_data["progress"] = (completed_steps / len(session_data["steps"])) * 100
        
        # 세션 업데이트 시간
        session_data["updated_at"] = datetime.now().isoformat()
        
        # 세션 저장
        self._save_session(session_data)
        
        return {
            "success": True,
            "message": "단계를 건너뛰었습니다.",
            "next_step": self.get_current_step(session_id)
        }
    
    def reset_step(self, session_id: str) -> Dict[str, Any]:
        """
        현재 단계 초기화
        
        Args:
            session_id (str): 세션 ID
            
        Returns:
            dict: 결과
        """
        session_data = self.get_session(session_id)
        if not session_data:
            return {"success": False, "error": "세션을 찾을 수 없습니다."}
        
        current_step_idx = session_data["current_step"]
        if current_step_idx >= len(session_data["steps"]):
            return {"success": False, "error": "모든 단계를 완료했습니다."}
        
        current_step = session_data["steps"][current_step_idx]
        
        # 현재 단계 초기화
        current_step["status"] = "in_progress"
        if "completed_at" in current_step:
            del current_step["completed_at"]
        
        # 세션 업데이트 시간
        session_data["updated_at"] = datetime.now().isoformat()
        
        # 세션 저장
        self._save_session(session_data)
        
        return {
            "success": True,
            "message": "단계를 초기화했습니다.",
            "current_step": current_step
        }
    
    def get_hint(self, session_id: str) -> Dict[str, Any]:
        """
        현재 단계의 힌트 제공
        
        Args:
            session_id (str): 세션 ID
            
        Returns:
            dict: 힌트 정보
        """
        session_data = self.get_session(session_id)
        if not session_data:
            return {"success": False, "error": "세션을 찾을 수 없습니다."}
        
        current_step_idx = session_data["current_step"]
        if current_step_idx >= len(session_data["steps"]):
            return {"success": False, "error": "모든 단계를 완료했습니다."}
        
        current_step = session_data["steps"][current_step_idx]
        
        # 힌트 가져오기
        hints = current_step.get("hints", [])
        if not hints:
            return {
                "success": False,
                "message": "이 단계에는 힌트가 없습니다."
            }
        
        # 힌트 사용 기록
        hint_usage = {
            "step_id": current_step["step_id"],
            "timestamp": datetime.now().isoformat(),
            "action": "hint_requested"
        }
        session_data["history"].append(hint_usage)
        
        # 세션 업데이트 시간
        session_data["updated_at"] = datetime.now().isoformat()
        
        # 세션 저장
        self._save_session(session_data)
        
        return {
            "success": True,
            "hints": hints
        } 
   def get_session_summary(self, session_id: str) -> Dict[str, Any]:
        """
        세션 요약 정보 조회
        
        Args:
            session_id (str): 세션 ID
            
        Returns:
            dict: 세션 요약 정보
        """
        session_data = self.get_session(session_id)
        if not session_data:
            return {"success": False, "error": "세션을 찾을 수 없습니다."}
        
        # 요약 정보 생성
        summary = {
            "session_id": session_data["session_id"],
            "concept_id": session_data["concept_id"],
            "user_id": session_data["user_id"],
            "created_at": session_data["created_at"],
            "updated_at": session_data["updated_at"],
            "completed_at": session_data["completed_at"],
            "status": session_data["status"],
            "progress": session_data["progress"],
            "total_steps": len(session_data["steps"]),
            "current_step": session_data["current_step"] + 1,  # 1-based for display
            "steps_summary": []
        }
        
        # 단계별 요약
        for step in session_data["steps"]:
            step_summary = {
                "step_id": step["step_id"],
                "title": step["title"],
                "status": step["status"]
            }
            summary["steps_summary"].append(step_summary)
        
        return {
            "success": True,
            "summary": summary
        }
    
    def export_session(self, session_id: str, format: str = "json") -> Dict[str, Any]:
        """
        세션 데이터 내보내기
        
        Args:
            session_id (str): 세션 ID
            format (str): 내보내기 형식 (json, html, csv)
            
        Returns:
            dict: 내보내기 결과
        """
        session_data = self.get_session(session_id)
        if not session_data:
            return {"success": False, "error": "세션을 찾을 수 없습니다."}
        
        if format == "json":
            # JSON 형식으로 내보내기
            export_data = session_data
            
            # 파일명 생성
            filename = f"session_{session_data['user_id']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            # 파일 저장
            export_path = os.path.join("exports", filename)
            os.makedirs("exports", exist_ok=True)
            
            with open(export_path, "w", encoding="utf-8") as f:
                json.dump(export_data, f, ensure_ascii=False, indent=2)
            
            return {
                "success": True,
                "format": format,
                "filename": filename,
                "path": export_path
            }
        
        elif format == "html":
            # HTML 형식으로 내보내기
            html_content = self._generate_session_html(session_data)
            
            # 파일명 생성
            filename = f"session_{session_data['user_id']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
            
            # 파일 저장
            export_path = os.path.join("exports", filename)
            os.makedirs("exports", exist_ok=True)
            
            with open(export_path, "w", encoding="utf-8") as f:
                f.write(html_content)
            
            return {
                "success": True,
                "format": format,
                "filename": filename,
                "path": export_path
            }
        
        elif format == "csv":
            # CSV 형식으로 내보내기
            csv_content = self._generate_session_csv(session_data)
            
            # 파일명 생성
            filename = f"session_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
            # 파일 저장
            export_path = os.path.join("exports", filename)
            os.makedirs("exports", exist_ok=True)
            
            with open(export_path, "w", encoding="utf-8") as f:
                f.write(csv_content)
            
            return {
                "success": True,
                "format": format,
                "filename": filename,
                "path": export_path
            }
        
        else:
            return {
                "success": False,
                "error": f"지원하지 않는 형식입니다: {format}"
            } 
   def _get_steps_for_concept(self, concept_id: str) -> List[Dict[str, Any]]:
        """
        개념에 따른 단계 정보 가져오기
        
        Args:
            concept_id (str): 개념 ID
            
        Returns:
            list: 단계 정보 목록
        """
        # 개념별 단계 정의
        concept_steps = {
            "descriptive_stats": [
                {
                    "step_id": "data_preparation",
                    "title": "데이터 준비",
                    "description": "분석할 데이터를 준비합니다.",
                    "code_template": "# 데이터 준비\nimport numpy as np\n\n# 학생 시험 점수 데이터 생성 (평균 70, 표준편차 15인 정규분포)\nnp.random.seed(42)  # 재현성을 위한 시드 설정\nscores = np.random.normal(loc=70, scale=15, size=50)\n\n# 데이터 확인\nprint(f\"생성된 데이터 개수: {len(scores)}\")\nprint(\"처음 10개 데이터:\")\nprint(scores[:10])\n\n# 데이터 반환\nscores",
                    "expected_output": ["생성된 데이터 개수: 50", "처음 10개 데이터:"],
                    "verification_criteria": {
                        "data_length": 50,
                        "data_type": "numpy.ndarray"
                    },
                    "hints": [
                        "numpy의 random.normal() 함수를 사용하여 정규분포 데이터를 생성할 수 있습니다.",
                        "np.random.seed()를 사용하면 매번 같은 난수를 생성할 수 있습니다.",
                        "print() 함수를 사용하여 데이터를 확인해보세요."
                    ],
                    "status": "not_started"
                },
                {
                    "step_id": "central_tendency",
                    "title": "중심경향성 분석",
                    "description": "데이터의 중심경향성(평균, 중앙값, 최빈값)을 계산하고 비교합니다.",
                    "code_template": "# 중심경향성 분석\nimport numpy as np\nfrom scipy import stats\n\n# 이전 단계에서 생성한 점수 데이터\nnp.random.seed(42)\nscores = np.random.normal(loc=70, scale=15, size=50)\n\n# 중심경향성 계산\nmean = np.mean(scores)\nmedian = np.median(scores)\nmode = stats.mode(scores)[0][0]  # scipy의 mode 함수 사용\n\n# 결과 출력\nprint(f\"평균: {mean:.2f}\")\nprint(f\"중앙값: {median:.2f}\")\nprint(f\"최빈값: {mode:.2f}\")\n\n# 평균과 중앙값 비교\nif mean > median:\n    print(\"\\n평균이 중앙값보다 크므로, 데이터가 오른쪽으로 치우쳐 있을 가능성이 있습니다.\")\nelif mean < median:\n    print(\"\\n평균이 중앙값보다 작으므로, 데이터가 왼쪽으로 치우쳐 있을 가능성이 있습니다.\")\nelse:\n    print(\"\\n평균과 중앙값이 같으므로, 데이터가 대칭적일 가능성이 높습니다.\")\n\n# 결과 반환\n{\n    'mean': mean,\n    'median': median,\n    'mode': mode\n}",
                    "expected_output": ["평균:", "중앙값:", "최빈값:"],
                    "verification_criteria": {
                        "has_mean": True,
                        "has_median": True,
                        "has_mode": True
                    },
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
                    "code_template": "# 산포도 분석\nimport numpy as np\n\n# 이전 단계에서 생성한 점수 데이터\nnp.random.seed(42)\nscores = np.random.normal(loc=70, scale=15, size=50)\n\n# 산포도 계산\ndata_range = np.max(scores) - np.min(scores)\nvariance = np.var(scores)\nstd_dev = np.std(scores)\nq1, q3 = np.percentile(scores, [25, 75])\niqr = q3 - q1\n\n# 결과 출력\nprint(f\"범위: {data_range:.2f}\")\nprint(f\"분산: {variance:.2f}\")\nprint(f\"표준편차: {std_dev:.2f}\")\nprint(f\"1사분위수(Q1): {q1:.2f}\")\nprint(f\"3사분위수(Q3): {q3:.2f}\")\nprint(f\"사분위수 범위(IQR): {iqr:.2f}\")\n\n# 변동계수 계산 (표준편차/평균)\ncv = std_dev / np.mean(scores)\nprint(f\"\\n변동계수(CV): {cv:.4f}\")\n\nif cv < 0.1:\n    print(\"변동계수가 0.1보다 작으므로, 데이터의 변동성이 낮습니다.\")\nelif cv > 0.3:\n    print(\"변동계수가 0.3보다 크므로, 데이터의 변동성이 높습니다.\")\nelse:\n    print(\"변동계수가 중간 정도로, 데이터가 적절한 변동성을 가지고 있습니다.\")\n\n# 이상치 탐지\nlower_bound = q1 - 1.5 * iqr\nupper_bound = q3 + 1.5 * iqr\noutliers = scores[(scores < lower_bound) | (scores > upper_bound)]\n\nprint(f\"\\n이상치 경계: {lower_bound:.2f} ~ {upper_bound:.2f}\")\nprint(f\"이상치 개수: {len(outliers)}\")\nif len(outliers) > 0:\n    print(f\"이상치: {outliers}\")\n\n# 결과 반환\n{\n    'range': data_range,\n    'variance': variance,\n    'std_dev': std_dev,\n    'iqr': iqr,\n    'cv': cv,\n    'outliers': outliers\n}",
                    "expected_output": ["범위:", "분산:", "표준편차:", "사분위수 범위(IQR):", "변동계수(CV):"],
                    "verification_criteria": {
                        "has_range": True,
                        "has_variance": True,
                        "has_std_dev": True,
                        "has_iqr": True
                    },
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
                    "code_template": "# 데이터 시각화\nimport numpy as np\nimport matplotlib.pyplot as plt\nfrom io import BytesIO\nimport base64\n\n# 이전 단계에서 생성한 점수 데이터\nnp.random.seed(42)\nscores = np.random.normal(loc=70, scale=15, size=50)\n\n# 그래프 설정\nplt.figure(figsize=(12, 5))\n\n# 히스토그램\nplt.subplot(1, 2, 1)\nplt.hist(scores, bins=10, color='skyblue', edgecolor='black', alpha=0.7)\nplt.axvline(np.mean(scores), color='red', linestyle='--', linewidth=2, label=f'평균: {np.mean(scores):.2f}')\nplt.axvline(np.median(scores), color='green', linestyle='-.', linewidth=2, label=f'중앙값: {np.median(scores):.2f}')\nplt.title('점수 분포 히스토그램')\nplt.xlabel('점수')\nplt.ylabel('빈도')\nplt.legend()\nplt.grid(alpha=0.3)\n\n# 박스플롯\nplt.subplot(1, 2, 2)\nplt.boxplot(scores, vert=False, patch_artist=True, \n           boxprops=dict(facecolor='lightblue', color='black'),\n           whiskerprops=dict(color='black'),\n           medianprops=dict(color='red', linewidth=2))\nplt.title('점수 분포 박스플롯')\nplt.xlabel('점수')\nplt.grid(alpha=0.3)\n\n# 레이아웃 조정\nplt.tight_layout()\n\n# 그래프를 이미지로 변환\nbuffer = BytesIO()\nplt.savefig(buffer, format='png')\nbuffer.seek(0)\nimage_base64 = base64.b64encode(buffer.read()).decode('utf-8')\n\n# HTML에 이미지 표시\nfrom IPython.display import HTML\nHTML(f'<img src=\"data:image/png;base64,{image_base64}\" />')\n\n# 결과 출력\nprint(\"데이터 시각화 완료!\")\nprint(f\"평균: {np.mean(scores):.2f}\")\nprint(f\"중앙값: {np.median(scores):.2f}\")\nprint(f\"표준편차: {np.std(scores):.2f}\")\n\n# 그래프 닫기\nplt.close()\n\n# 결과 반환\n{\n    'mean': np.mean(scores),\n    'median': np.median(scores),\n    'std_dev': np.std(scores)\n}",
                    "expected_output": ["데이터 시각화 완료!", "평균:", "중앙값:", "표준편차:"],
                    "verification_criteria": {
                        "has_visualization": True,
                        "has_histogram": True,
                        "has_boxplot": True
                    },
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
                    "code_template": "# 결과 해석\nimport numpy as np\nimport matplotlib.pyplot as plt\nfrom scipy import stats\n\n# 이전 단계에서 생성한 점수 데이터\nnp.random.seed(42)\nscores = np.random.normal(loc=70, scale=15, size=50)\n\n# 기술통계량 계산\nmean = np.mean(scores)\nmedian = np.median(scores)\nstd_dev = np.std(scores)\nmin_val = np.min(scores)\nmax_val = np.max(scores)\nq1, q3 = np.percentile(scores, [25, 75])\niqr = q3 - q1\n\n# 정규성 검정\nshapiro_test = stats.shapiro(scores)\nnormal_p_value = shapiro_test[1]\n\n# 종합 결과 출력\nprint(\"📊 데이터 분석 종합 결과\")\nprint(\"=\" * 40)\nprint(f\"데이터 개수: {len(scores)}\")\nprint(f\"\\n🔸 중심경향성:\")\nprint(f\"   • 평균: {mean:.2f}\")\nprint(f\"   • 중앙값: {median:.2f}\")\nprint(f\"\\n🔸 산포도:\")\nprint(f\"   • 표준편차: {std_dev:.2f}\")\nprint(f\"   • 범위: {min_val:.2f} ~ {max_val:.2f}\")\nprint(f\"   • 사분위수 범위: {q1:.2f} ~ {q3:.2f}\")\nprint(f\"\\n🔸 분포 특성:\")\nprint(f\"   • 치우침: {'우측' if mean > median else '좌측' if mean < median else '없음'}\")\nprint(f\"   • 정규성 검정 p-값: {normal_p_value:.4f} ({'정규분포에 가까움' if normal_p_value > 0.05 else '정규분포가 아닐 수 있음'})\")\n\n# 해석 및 결론\nprint(\"\\n📝 해석 및 결론:\")\nif normal_p_value > 0.05:\n    print(\"1. 이 데이터는 정규분포를 따르는 것으로 보입니다.\")\n    print(\"2. 평균과 표준편차를 사용하여 데이터를 요약하는 것이 적절합니다.\")\n    print(f\"3. 약 68%의 데이터가 {mean - std_dev:.2f}~{mean + std_dev:.2f} 범위에 있을 것으로 예상됩니다.\")\n    print(f\"4. 약 95%의 데이터가 {mean - 2*std_dev:.2f}~{mean + 2*std_dev:.2f} 범위에 있을 것으로 예상됩니다.\")\nelse:\n    print(\"1. 이 데이터는 정규분포를 따르지 않을 수 있습니다.\")\n    print(\"2. 중앙값과 사분위수를 사용하여 데이터를 요약하는 것이 더 적절할 수 있습니다.\")\n    print(f\"3. 데이터의 50%가 {q1:.2f}~{q3:.2f} 범위에 있습니다.\")\n\n# 실무적 해석 예시 (학생 점수 데이터 가정)\nprint(\"\\n💡 실무적 해석 (학생 점수 데이터 예시):\")\nif mean < 60:\n    print(\"• 전반적인 성적이 낮으므로, 추가 학습 지원이 필요할 수 있습니다.\")\nelif mean > 80:\n    print(\"• 전반적인 성적이 우수하므로, 심화 학습을 제공할 수 있습니다.\")\nelse:\n    print(\"• 전반적인 성적이 보통 수준입니다.\")\n\nif std_dev > 20:\n    print(\"• 점수 편차가 크므로, 학생별 맞춤형 지도가 필요할 수 있습니다.\")\nelse:\n    print(\"• 점수 편차가 적절하므로, 전체 학생을 대상으로 한 교육이 효과적일 수 있습니다.\")\n\n# 결과 반환\n{\n    'mean': mean,\n    'median': median,\n    'std_dev': std_dev,\n    'normal_p_value': normal_p_value,\n    'is_normal': normal_p_value > 0.05\n}",
                    "expected_output": ["📊 데이터 분석 종합 결과", "중심경향성:", "산포도:", "분포 특성:", "해석 및 결론:", "실무적 해석"],
                    "verification_criteria": {
                        "has_summary": True,
                        "has_interpretation": True,
                        "has_normality_test": True
                    },
                    "hints": [
                        "scipy.stats의 shapiro() 함수를 사용하여 정규성 검정을 수행할 수 있습니다.",
                        "정규분포에서는 평균 ± 1 표준편차 범위에 약 68%의 데이터가 포함됩니다.",
                        "정규분포에서는 평균 ± 2 표준편차 범위에 약 95%의 데이터가 포함됩니다."
                    ],
                    "status": "not_started"
                }
            ],
            "probability": [
                # 확률론 관련 단계 정의
            ],
            "hypothesis_testing": [
                # 가설 검정 관련 단계 정의
            ]
        }
        
        # 기본 단계 정의 (개념이 없는 경우)
        default_steps = [
            {
                "step_id": "default_step",
                "title": "기본 단계",
                "description": "기본적인 데이터 분석을 수행합니다.",
                "code_template": "# 기본 데이터 분석\nimport numpy as np\n\n# 데이터 생성\ndata = np.random.normal(0, 1, 100)\n\n# 기본 통계량 계산\nmean = np.mean(data)\nstd = np.std(data)\n\nprint(f\"평균: {mean:.2f}\")\nprint(f\"표준편차: {std:.2f}\")\n\n# 데이터 반환\ndata",
                "expected_output": ["평균:", "표준편차:"],
                "verification_criteria": {
                    "data_length": 100
                },
                "hints": [
                    "numpy를 사용하여 기본 통계량을 계산할 수 있습니다."
                ],
                "status": "not_started"
            }
        ]
        
        # 개념에 따른 단계 반환
        return concept_steps.get(concept_id, default_steps)
    
    def _verify_step(self, step: Dict[str, Any], code: str, output: str) -> Dict[str, Any]:
        """
        단계 검증
        
        Args:
            step (dict): 단계 정보
            code (str): 제출한 코드
            output (str): 코드 실행 결과
            
        Returns:
            dict: 검증 결과
        """
        # 기본 검증 결과
        result = {
            "success": False,
            "message": "검증에 실패했습니다.",
            "details": []
        }
        
        # 예상 출력 확인
        expected_outputs = step.get("expected_output", [])
        output_check = all(expected in output for expected in expected_outputs)
        
        if output_check:
            result["details"].append("출력 확인: 성공")
        else:
            result["details"].append("출력 확인: 실패 (예상 출력이 포함되지 않음)")
        
        # 코드 검증 기준 확인
        criteria = step.get("verification_criteria", {})
        criteria_checks = []
        
        # 데이터 길이 확인
        if "data_length" in criteria:
            if f"데이터 개수: {criteria['data_length']}" in output:
                criteria_checks.append(True)
                result["details"].append(f"데이터 길이 확인: 성공 ({criteria['data_length']})")
            else:
                criteria_checks.append(False)
                result["details"].append(f"데이터 길이 확인: 실패 (예상: {criteria['data_length']})")
        
        # 데이터 타입 확인
        if "data_type" in criteria:
            if criteria["data_type"] in output:
                criteria_checks.append(True)
                result["details"].append(f"데이터 타입 확인: 성공 ({criteria['data_type']})")
            else:
                criteria_checks.append(False)
                result["details"].append(f"데이터 타입 확인: 실패 (예상: {criteria['data_type']})")
        
        # 통계량 포함 여부 확인
        for stat in ["mean", "median", "mode", "range", "variance", "std_dev", "iqr"]:
            key = f"has_{stat}"
            if key in criteria and criteria[key]:
                if stat in output.lower():
                    criteria_checks.append(True)
                    result["details"].append(f"{stat} 포함 확인: 성공")
                else:
                    criteria_checks.append(False)
                    result["details"].append(f"{stat} 포함 확인: 실패")
        
        # 시각화 포함 여부 확인
        if "has_visualization" in criteria and criteria["has_visualization"]:
            if "plt" in code and "savefig" in code:
                criteria_checks.append(True)
                result["details"].append("시각화 포함 확인: 성공")
            else:
                criteria_checks.append(False)
                result["details"].append("시각화 포함 확인: 실패")
        
        # 히스토그램 포함 여부 확인
        if "has_histogram" in criteria and criteria["has_histogram"]:
            if "hist" in code:
                criteria_checks.append(True)
                result["details"].append("히스토그램 포함 확인: 성공")
            else:
                criteria_checks.append(False)
                result["details"].append("히스토그램 포함 확인: 실패")
        
        # 박스플롯 포함 여부 확인
        if "has_boxplot" in criteria and criteria["has_boxplot"]:
            if "boxplot" in code:
                criteria_checks.append(True)
                result["details"].append("박스플롯 포함 확인: 성공")
            else:
                criteria_checks.append(False)
                result["details"].append("박스플롯 포함 확인: 실패")
        
        # 요약 정보 포함 여부 확인
        if "has_summary" in criteria and criteria["has_summary"]:
            if "종합 결과" in output:
                criteria_checks.append(True)
                result["details"].append("요약 정보 포함 확인: 성공")
            else:
                criteria_checks.append(False)
                result["details"].append("요약 정보 포함 확인: 실패")
        
        # 해석 포함 여부 확인
        if "has_interpretation" in criteria and criteria["has_interpretation"]:
            if "해석" in output:
                criteria_checks.append(True)
                result["details"].append("해석 포함 확인: 성공")
            else:
                criteria_checks.append(False)
                result["details"].append("해석 포함 확인: 실패")
        
        # 정규성 검정 포함 여부 확인
        if "has_normality_test" in criteria and criteria["has_normality_test"]:
            if "shapiro" in code:
                criteria_checks.append(True)
                result["details"].append("정규성 검정 포함 확인: 성공")
            else:
                criteria_checks.append(False)
                result["details"].append("정규성 검정 포함 확인: 실패")a_checks.append(False)
                result["details"].append("정규성 검정 포함 확인: 실패")a_checks.append(False)
                result["details"].append("정규성 검정 포함 확인: 실패")
        
        # 최종 검증 결과
        if output_check and (not criteria_checks or all(criteria_checks)):
            result["success"] = True
            result["message"] = "검증에 성공했습니다."
        
        return result    def
 _save_session(self, session_data: Dict[str, Any]) -> bool:
        """
        세션 데이터 저장
        
        Args:
            session_data (dict): 세션 데이터
            
        Returns:
            bool: 저장 성공 여부
        """
        try:
            session_id = session_data["session_id"]
            filename = f"{session_id}.json"
            filepath = os.path.join(self.session_dir, filename)
            
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(session_data, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception as e:
            print(f"세션 저장 오류: {e}")
            return False
    
    def _load_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        세션 데이터 로드
        
        Args:
            session_id (str): 세션 ID
            
        Returns:
            dict or None: 세션 데이터 (없으면 None)
        """
        try:
            filename = f"{session_id}.json"
            filepath = os.path.join(self.session_dir, filename)
            
            if not os.path.exists(filepath):
                return None
            
            with open(filepath, "r", encoding="utf-8") as f:
                session_data = json.load(f)
            
            return session_data
        except Exception as e:
            print(f"세션 로드 오류: {e}")
            return None
    
    def _generate_session_html(self, session_data: Dict[str, Any]) -> str:
        """
        세션 데이터를 HTML로 변환
        
        Args:
            session_data (dict): 세션 데이터
            
        Returns:
            str: HTML 문자열
        """
        # 기본 HTML 템플릿
        html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>학습 세션 결과 - {session_data["concept_id"]}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        h1, h2, h3, h4 {{
            color: #2c3e50;
        }}
        .header {{
            background-color: #3498db;
            color: white;
            padding: 20px;
            border-radius: 5px;
            margin-bottom: 20px;
        }}
        .step {{
            background-color: #f8f9fa;
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 15px;
            margin-bottom: 20px;
        }}
        .step-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid #ddd;
            padding-bottom: 10px;
            margin-bottom: 10px;
        }}
        .step-title {{
            font-size: 1.2rem;
            font-weight: bold;
        }}
        .step-status {{
            padding: 5px 10px;
            border-radius: 3px;
            font-size: 0.8rem;
            font-weight: bold;
        }}
        .status-completed {{
            background-color: #2ecc71;
            color: white;
        }}
        .status-in_progress {{
            background-color: #f39c12;
            color: white;
        }}
        .status-not_started, .status-skipped {{
            background-color: #95a5a6;
            color: white;
        }}
        .code-block {{
            background-color: #f5f5f5;
            border: 1px solid #ddd;
            border-radius: 3px;
            padding: 10px;
            font-family: monospace;
            white-space: pre-wrap;
            overflow-x: auto;
        }}
        .output-block {{
            background-color: #f0f8ff;
            border: 1px solid #b8daff;
            border-radius: 3px;
            padding: 10px;
            font-family: monospace;
            white-space: pre-wrap;
            overflow-x: auto;
        }}
        .summary {{
            background-color: #e8f4f8;
            border: 1px solid #b8daff;
            border-radius: 5px;
            padding: 15px;
            margin-top: 20px;
        }}
        .progress-bar {{
            height: 20px;
            background-color: #ecf0f1;
            border-radius: 10px;
            margin-bottom: 10px;
            overflow: hidden;
        }}
        .progress-fill {{
            height: 100%;
            background-color: #3498db;
            border-radius: 10px;
            width: {session_data["progress"]}%;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>학습 세션 결과</h1>
        <p>개념: {session_data["concept_id"]}</p>
        <p>사용자: {session_data["user_id"]}</p>
        <p>생성일: {session_data["created_at"]}</p>
        <p>상태: {session_data["status"]}</p>
    </div>
    
    <div class="summary">
        <h2>진행 상황</h2>
        <div class="progress-bar">
            <div class="progress-fill"></div>
        </div>
        <p>진행률: {session_data["progress"]:.1f}%</p>
        <p>총 단계: {len(session_data["steps"])}</p>
        <p>현재 단계: {session_data["current_step"] + 1}</p>
    </div>
    
    <h2>단계별 결과</h2>
"""
        
        # 단계별 정보 추가
        for i, step in enumerate(session_data["steps"]):
            status_class = f"status-{step['status']}"
            
            html += f"""
    <div class="step">
        <div class="step-header">
            <div class="step-title">단계 {i+1}: {step["title"]}</div>
            <div class="step-status {status_class}">{step["status"]}</div>
        </div>
        <p>{step["description"]}</p>
"""
            
            # 완료된 단계인 경우 코드와 결과 표시
            if step["status"] == "completed":
                # 히스토리에서 해당 단계의 마지막 제출 찾기
                step_submissions = [h for h in session_data["history"] if h.get("step_id") == step["step_id"] and "code" in h]
                if step_submissions:
                    last_submission = step_submissions[-1]
                    html += f"""
        <h4>코드</h4>
        <div class="code-block">{last_submission["code"]}</div>
        
        <h4>결과</h4>
        <div class="output-block">{last_submission["output"]}</div>
"""
            
            html += """
    </div>
"""
        
        # HTML 마무리
        html += """
</body>
</html>
"""
        
        return html
    
    def _generate_session_csv(self, session_data: Dict[str, Any]) -> str:
        """
        세션 데이터를 CSV로 변환
        
        Args:
            session_data (dict): 세션 데이터
            
        Returns:
            str: CSV 문자열
        """
        # 기본 정보
        csv_lines = [
            "세션 ID,개념 ID,사용자 ID,생성일,상태,진행률",
            f"{session_data['session_id']},{session_data['concept_id']},{session_data['user_id']},{session_data['created_at']},{session_data['status']},{session_data['progress']}"
        ]
        
        # 빈 줄
        csv_lines.append("")
        
        # 단계 정보
        csv_lines.append("단계 번호,단계 ID,제목,설명,상태")
        for i, step in enumerate(session_data["steps"]):
            csv_lines.append(f"{i+1},{step['step_id']},{step['title']},{step['description']},{step['status']}")
        
        # 빈 줄
        csv_lines.append("")
        
        # 히스토리 정보
        csv_lines.append("타임스탬프,단계 ID,액션,성공 여부")
        for entry in session_data["history"]:
            timestamp = entry.get("timestamp", "")
            step_id = entry.get("step_id", "")
            action = "submission" if "code" in entry else entry.get("action", "")
            success = str(entry.get("success", "")).lower()
            
            csv_lines.append(f"{timestamp},{step_id},{action},{success}")
        
        return "\n".join(csv_lines)


# 세션 관리 시스템 인스턴스 생성
session_manager = SessionManagementSystem()