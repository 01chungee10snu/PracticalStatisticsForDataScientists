"""
결과 저장 및 공유 시스템
- 학습 과정 및 결과 저장 기능
- 완성된 데모 페이지 생성 및 공유
- GitHub Pages 호환 (클라이언트 사이드)
"""

import json
import base64
from datetime import datetime
from typing import Dict, List, Any, Optional, Union
from urllib.parse import quote

class ResultSharingSystem:
    """
    결과 저장 및 공유 시스템
    학습 과정과 결과를 저장하고 공유할 수 있는 기능을 제공합니다.
    """
    
    def __init__(self):
        """초기화"""
        self.storage_key = "learning_results"
        self.shared_results_key = "shared_results"
        
    def save_learning_result(self, session_data: Dict[str, Any], 
                           execution_results: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        학습 결과 저장
        
        Args:
            session_data (dict): 세션 데이터
            execution_results (list, optional): 코드 실행 결과들
            
        Returns:
            dict: 저장 결과
        """
        try:
            result_id = self._generate_result_id()
            timestamp = datetime.now().isoformat()
            
            learning_result = {
                "result_id": result_id,
                "timestamp": timestamp,
                "session_data": session_data,
                "execution_results": execution_results or [],
                "summary": self._generate_result_summary(session_data, execution_results),
                "metadata": {
                    "concept_id": session_data.get("concept_id", "unknown"),
                    "user_id": session_data.get("user_id", "anonymous"),
                    "completion_status": session_data.get("status", "unknown"),
                    "total_steps": len(session_data.get("steps", [])),
                    "completed_steps": sum(1 for step in session_data.get("steps", []) 
                                         if step.get("status") == "completed")
                }
            }
            
            # 로컬 저장소에 저장
            self._save_to_local_storage(result_id, learning_result)
            
            return {
                "success": True,
                "result_id": result_id,
                "message": "학습 결과가 성공적으로 저장되었습니다.",
                "timestamp": timestamp
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "학습 결과 저장 중 오류가 발생했습니다."
            }
    
    def get_saved_results(self, user_id: str = None) -> Dict[str, Any]:
        """
        저장된 결과 목록 조회
        
        Args:
            user_id (str, optional): 사용자 ID
            
        Returns:
            dict: 저장된 결과 목록
        """
        try:
            all_results = self._load_from_local_storage()
            
            if user_id:
                filtered_results = {
                    result_id: result for result_id, result in all_results.items()
                    if result.get("metadata", {}).get("user_id") == user_id
                }
            else:
                filtered_results = all_results
            
            # 요약 정보만 반환 (전체 데이터는 너무 클 수 있음)
            summary_results = {}
            for result_id, result in filtered_results.items():
                summary_results[result_id] = {
                    "result_id": result_id,
                    "timestamp": result.get("timestamp"),
                    "summary": result.get("summary"),
                    "metadata": result.get("metadata")
                }
            
            return {
                "success": True,
                "results": summary_results,
                "count": len(summary_results)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "results": {},
                "count": 0
            }
    
    def get_result_detail(self, result_id: str) -> Dict[str, Any]:
        """
        특정 결과의 상세 정보 조회
        
        Args:
            result_id (str): 결과 ID
            
        Returns:
            dict: 결과 상세 정보
        """
        try:
            all_results = self._load_from_local_storage()
            
            if result_id not in all_results:
                return {
                    "success": False,
                    "error": "결과를 찾을 수 없습니다.",
                    "result": None
                }
            
            return {
                "success": True,
                "result": all_results[result_id]
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "result": None
            }
    
    def generate_shareable_link(self, result_id: str) -> Dict[str, Any]:
        """
        공유 가능한 링크 생성
        
        Args:
            result_id (str): 결과 ID
            
        Returns:
            dict: 공유 링크 정보
        """
        try:
            result_detail = self.get_result_detail(result_id)
            
            if not result_detail["success"]:
                return result_detail
            
            result_data = result_detail["result"]
            
            # 결과 데이터를 압축하여 URL 파라미터로 사용
            compressed_data = self._compress_result_data(result_data)
            
            # 현재 페이지 URL을 기반으로 공유 링크 생성
            base_url = self._get_current_page_url()
            share_url = f"{base_url}?shared_result={compressed_data}"
            
            # 공유 정보 저장
            share_info = {
                "share_id": self._generate_share_id(),
                "result_id": result_id,
                "created_at": datetime.now().isoformat(),
                "share_url": share_url,
                "access_count": 0
            }
            
            self._save_share_info(share_info)
            
            return {
                "success": True,
                "share_url": share_url,
                "share_id": share_info["share_id"],
                "message": "공유 링크가 생성되었습니다."
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "공유 링크 생성 중 오류가 발생했습니다."
            }
    
    def load_shared_result(self, compressed_data: str) -> Dict[str, Any]:
        """
        공유된 결과 로드
        
        Args:
            compressed_data (str): 압축된 결과 데이터
            
        Returns:
            dict: 로드된 결과 데이터
        """
        try:
            result_data = self._decompress_result_data(compressed_data)
            
            return {
                "success": True,
                "result": result_data,
                "message": "공유된 결과를 성공적으로 로드했습니다."
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "공유된 결과 로드 중 오류가 발생했습니다."
            }
    
    def export_result(self, result_id: str, format: str = "html") -> Dict[str, Any]:
        """
        결과 내보내기
        
        Args:
            result_id (str): 결과 ID
            format (str): 내보내기 형식 (html, json, markdown)
            
        Returns:
            dict: 내보내기 결과
        """
        try:
            result_detail = self.get_result_detail(result_id)
            
            if not result_detail["success"]:
                return result_detail
            
            result_data = result_detail["result"]
            
            if format == "html":
                exported_content = self._generate_html_report(result_data)
                filename = f"learning_result_{result_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
            elif format == "json":
                exported_content = json.dumps(result_data, indent=2, ensure_ascii=False)
                filename = f"learning_result_{result_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            elif format == "markdown":
                exported_content = self._generate_markdown_report(result_data)
                filename = f"learning_result_{result_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
            else:
                return {
                    "success": False,
                    "error": f"지원하지 않는 형식입니다: {format}"
                }
            
            return {
                "success": True,
                "content": exported_content,
                "filename": filename,
                "format": format,
                "message": f"{format.upper()} 형식으로 내보내기가 완료되었습니다."
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "결과 내보내기 중 오류가 발생했습니다."
            }
    
    def delete_result(self, result_id: str) -> Dict[str, Any]:
        """
        저장된 결과 삭제
        
        Args:
            result_id (str): 결과 ID
            
        Returns:
            dict: 삭제 결과
        """
        try:
            all_results = self._load_from_local_storage()
            
            if result_id not in all_results:
                return {
                    "success": False,
                    "error": "삭제할 결과를 찾을 수 없습니다."
                }
            
            del all_results[result_id]
            self._save_all_to_local_storage(all_results)
            
            return {
                "success": True,
                "message": "결과가 성공적으로 삭제되었습니다."
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "결과 삭제 중 오류가 발생했습니다."
            }