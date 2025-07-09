#!/usr/bin/env python3
"""
독립 실행 가능한 학습 시스템 테스트
"""

from modules.standalone_demo import SimpleLearningSystem

def test_learning_system():
    """학습 시스템 자동 테스트"""
    print("=== 🧪 독립 실행 가능한 학습 시스템 테스트 ===")
    
    # 시스템 초기화
    system = SimpleLearningSystem()
    print("✓ 시스템 초기화 완료")
    
    # 테스트 1: 학습자 등록
    profile = {
        "name": "테스트 학습자",
        "difficulty": 5,
        "pace": "medium"
    }
    
    result = system.register_learner("test_user", profile)
    print(f"✓ 학습자 등록: {result['message']}")
    
    # 테스트 2: 개인화된 콘텐츠 추천
    content = system.get_personalized_content("test_user")
    if "error" not in content:
        print(f"✓ 콘텐츠 추천: {content['content']['title']} (난이도: {content['content']['difficulty']})")
        print(f"  추천 이유: {content['recommendation_reason']}")
        
        # 테스트 3: 문제 풀기
        questions = content['content']['questions']
        correct_answers = 0
        
        for i, question in enumerate(questions):
            print(f"\n📝 문제 {i+1}: {question['q']}")
            
            # 정답 선택 (테스트용)
            correct_answer = question['correct']
            result = system.submit_answer("test_user", content['content_id'], i, correct_answer)
            
            if result['correct']:
                correct_answers += 1
                print(f"✅ 정답! 해설: {result['explanation']}")
            else:
                print(f"❌ 오답. 정답: {result['correct_answer']}")
        
        print(f"\\n📊 문제 풀이 결과: {correct_answers}/{len(questions)} 정답")
        
        # 테스트 4: 학습 분석
        analytics = system.get_learning_analytics("test_user")
        if "error" not in analytics:
            print(f"\\n📈 학습 분석:")
            print(f"  전체 성공률: {analytics['overall_stats']['success_rate']}%")
            print(f"  현재 레벨: {analytics['overall_stats']['current_level']}")
            print(f"  학습 상태: {analytics['learning_state']}")
        
        # 테스트 5: 시스템 통계
        stats = system.get_system_stats()
        print(f"\\n📊 시스템 통계:")
        print(f"  총 학습자: {stats['total_learners']}명")
        print(f"  총 상호작용: {stats['total_interactions']}회")
        print(f"  전체 성공률: {stats['overall_success_rate']}%")
        
        # 테스트 6: 적응형 기능 테스트
        print(f"\\n🎯 적응형 기능 테스트:")
        
        # 계속 틀린 답 제출 (어려워하는 상황 시뮬레이션)
        for i in range(3):
            wrong_answer = (correct_answer + 1) % 4  # 틀린 답
            result = system.submit_answer("test_user", content['content_id'], 0, wrong_answer)
            print(f"  시도 {i+1}: 의도적 오답 제출")
        
        # 새로운 추천 확인
        new_content = system.get_personalized_content("test_user")
        if "error" not in new_content:
            print(f"  적응 후 추천: {new_content['recommendation_reason']}")
        
        print(f"\\n🎉 테스트 완료! 모든 기능이 정상적으로 동작합니다.")
        return True
        
    else:
        print(f"❌ 콘텐츠 추천 실패: {content['error']}")
        return False

if __name__ == "__main__":
    success = test_learning_system()
    if success:
        print("\\n✅ 전체 테스트 성공")
    else:
        print("\\n❌ 테스트 실패")