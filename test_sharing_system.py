"""
결과 저장 및 공유 시스템 테스트
"""

import sys
sys.path.append('modules')

try:
    from modules.result_sharing_system import ResultSharingSystem, demo_result_sharing_system
    print("모듈 import 성공")
    
    # 데모 실행
    demo_result_sharing_system()
    
except Exception as e:
    print(f"오류 발생: {e}")
    import traceback
    traceback.print_exc()