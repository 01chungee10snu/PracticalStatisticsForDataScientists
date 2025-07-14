#!/usr/bin/env python3
"""
🎓 실무 통계학 학습 시스템 - 메인 진입점
- 다양한 실행 모드 제공
- 사용자 친화적인 인터페이스
- 완전한 학습 경로 안내
"""

import os
import sys
import json
import time
from datetime import datetime
from typing import Dict, List, Any, Optional

# 현재 디렉토리를 Python 경로에 추가
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 로컬 모듈 임포트
try:
    from modules.standalone_demo import SimpleLearningSystem
    from modules.simple_webapp import run_server
    from modules.enhanced_visualization import visualizer, create_statistics_visualization
    from modules.enhanced_tutorials import explanation_engine, tutorial_engine
except ImportError as e:
    # 모듈을 개별적으로 임포트 시도
    try:
        import sys
        sys.path.append('./modules')
        from standalone_demo import SimpleLearningSystem
        from simple_webapp import run_server
        from enhanced_visualization import visualizer, create_statistics_visualization
        from enhanced_tutorials import explanation_engine, tutorial_engine
    except ImportError as e2:
        print(f"❌ 모듈 임포트 오류: {e2}")
        print("📁 현재 디렉토리에서 실행해주세요.")
        print("🔍 modules/ 디렉토리가 존재하는지 확인해주세요.")
        sys.exit(1)


class LearningSystemLauncher:
    """학습 시스템 런처"""
    
    def __init__(self):
        self.system = SimpleLearningSystem()
        self.user_data_file = "user_data.json"
        self.session_log_file = "session_log.json"
        self.visualization_engine = visualizer
        self.explanation_engine = explanation_engine
        self.tutorial_engine = tutorial_engine
        
    def show_welcome(self):
        """환영 메시지 표시"""
        print("\n" + "="*70)
        print("🎓 실무 통계학 학습 시스템 v2.0".center(70))
        print("="*70)
        print("""
📚 학습 내용:
   • 기초 통계학 (기술통계, 확률)
   • 추론 통계학 (가설검정, 신뢰구간)
   • 고급 분석 (회귀, 분류, 군집)
   
✨ 주요 기능:
   • 개인화된 학습 경로
   • 적응형 난이도 조절
   • 실시간 성과 분석
   • 인터랙티브 문제 해결
   
🎯 학습 목표:
   • 통계적 사고력 향상
   • 실무 적용 능력 배양
   • 데이터 분석 기초 확립
        """)
    
    def show_main_menu(self):
        """메인 메뉴 표시"""
        print("\n" + "="*50)
        print("🎮 학습 모드 선택")
        print("="*50)
        print("1. 🖥️  웹 인터페이스 모드 (추천)")
        print("2. 💻 터미널 대화형 모드")
        print("3. 🔧 시스템 설정")
        print("4. 📖 학습 가이드")
        print("5. 🧪 데모 모드")
        print("6. 📊 시각화 데모")
        print("7. 🎓 인터랙티브 튜토리얼")
        print("8. 🚪 종료")
        print("="*50)
    
    def run_web_interface(self):
        """웹 인터페이스 실행"""
        print("\n🌐 웹 인터페이스를 시작합니다...")
        print("📍 주소: http://localhost:8000")
        print("🔗 브라우저에서 자동으로 열립니다")
        print("⏹️  종료: Ctrl+C")
        
        # 운영체제별 브라우저 열기
        try:
            import webbrowser
            webbrowser.open('http://localhost:8000')
        except:
            print("🔍 브라우저를 수동으로 열어주세요")
        
        # 웹 서버 실행
        try:
            run_server(port=8000)
        except KeyboardInterrupt:
            print("\n👋 웹 서버를 종료합니다.")
        except Exception as e:
            print(f"❌ 웹 서버 오류: {e}")
    
    def run_interactive_mode(self):
        """대화형 모드 실행"""
        print("\n💻 터미널 대화형 모드를 시작합니다...")
        
        # 익명 사용자로 바로 학습 세션 시작
        user_id = "anonymous_user"
        
        # 기본 프로필로 자동 등록
        default_profile = {
            "name": "익명 사용자",
            "learning_style": "visual",
            "learning_pace": "medium",
            "learning_goal": "basic_understanding",
            "weekly_hours": 4
        }
        
        self.system.register_learner(user_id, default_profile)
        
        # 학습 세션 시작
        self.interactive_learning_session(user_id)
    
    def handle_user_session(self) -> Optional[str]:
        """사용자 세션 처리"""
        users = self.load_user_data()
        
        print("\n👤 사용자 관리")
        print("1. 기존 사용자 로그인")
        print("2. 새 사용자 등록")
        
        choice = input("선택하세요 (1-2): ").strip()
        
        if choice == "1":
            if not users:
                print("❌ 등록된 사용자가 없습니다.")
                return None
            
            print("\n📋 등록된 사용자:")
            for i, user_id in enumerate(users.keys(), 1):
                user_info = users[user_id]
                print(f"{i}. {user_id} (가입일: {user_info.get('created_at', 'N/A')[:10]})")
            
            try:
                user_idx = int(input("사용자 번호를 선택하세요: ")) - 1
                user_list = list(users.keys())
                if 0 <= user_idx < len(user_list):
                    user_id = user_list[user_idx]
                    print(f"✅ {user_id}로 로그인했습니다.")
                    return user_id
                else:
                    print("❌ 잘못된 선택입니다.")
                    return None
            except ValueError:
                print("❌ 숫자를 입력하세요.")
                return None
        
        elif choice == "2":
            user_id = input("사용자 이름을 입력하세요: ").strip()
            if not user_id:
                print("❌ 사용자 이름을 입력해주세요.")
                return None
            
            if user_id in users:
                print("❌ 이미 존재하는 사용자입니다.")
                return None
            
            # 학습 스타일 설정
            learning_style = self.setup_learning_preferences()
            
            # 사용자 등록
            profile = {
                "name": user_id,
                "learning_style": learning_style,
                "created_at": datetime.now().isoformat(),
                "preferences": learning_style
            }
            
            result = self.system.register_learner(user_id, profile)
            
            # 데이터 저장
            users[user_id] = {
                "profile": profile,
                "created_at": datetime.now().isoformat()
            }
            self.save_user_data(users)
            
            print(f"✅ {result['message']}")
            return user_id
        
        else:
            print("❌ 잘못된 선택입니다.")
            return None
    
    def setup_learning_preferences(self) -> Dict[str, Any]:
        """학습 선호도 설정"""
        print("\n🎯 학습 선호도 설정")
        print("더 나은 학습 경험을 위해 몇 가지 질문에 답해주세요.")
        
        preferences = {}
        
        # 1. 학습 스타일
        print("\n1. 선호하는 학습 방식은?")
        print("   1) 시각적 (그래프, 차트, 다이어그램)")
        print("   2) 청각적 (설명, 토론, 음성)")
        print("   3) 실습적 (직접 해보기, 실험)")
        print("   4) 독서적 (텍스트, 문서, 정리)")
        
        style_choice = input("선택 (1-4): ").strip()
        style_map = {"1": "visual", "2": "auditory", "3": "kinesthetic", "4": "reading"}
        preferences["learning_style"] = style_map.get(style_choice, "visual")
        
        # 2. 학습 속도
        print("\n2. 선호하는 학습 속도는?")
        print("   1) 천천히 (충분한 시간으로 깊이 있게)")
        print("   2) 보통 (적당한 속도로 균형있게)")
        print("   3) 빠르게 (효율적으로 요점 중심)")
        
        pace_choice = input("선택 (1-3): ").strip()
        pace_map = {"1": "slow", "2": "medium", "3": "fast"}
        preferences["learning_pace"] = pace_map.get(pace_choice, "medium")
        
        # 3. 목표 설정
        print("\n3. 학습 목표는?")
        print("   1) 기초 이해 (통계의 기본 개념 파악)")
        print("   2) 실무 적용 (실제 문제 해결 능력)")
        print("   3) 심화 학습 (고급 기법 습득)")
        print("   4) 시험 대비 (자격증, 시험 준비)")
        
        goal_choice = input("선택 (1-4): ").strip()
        goal_map = {
            "1": "basic_understanding",
            "2": "practical_application", 
            "3": "advanced_learning",
            "4": "exam_preparation"
        }
        preferences["learning_goal"] = goal_map.get(goal_choice, "basic_understanding")
        
        # 4. 주간 학습 시간
        print("\n4. 주당 학습 가능 시간은?")
        print("   1) 1-2시간 (짧고 집중적으로)")
        print("   2) 3-5시간 (꾸준히 학습)")
        print("   3) 6-10시간 (충분한 시간 투자)")
        print("   4) 10시간 이상 (집중 학습)")
        
        time_choice = input("선택 (1-4): ").strip()
        time_map = {"1": 2, "2": 4, "3": 8, "4": 12}
        preferences["weekly_hours"] = time_map.get(time_choice, 4)
        
        # 설정 확인
        print(f"\n✅ 설정이 완료되었습니다!")
        print(f"   학습 스타일: {preferences['learning_style']}")
        print(f"   학습 속도: {preferences['learning_pace']}")
        print(f"   목표: {preferences['learning_goal']}")
        print(f"   주간 시간: {preferences['weekly_hours']}시간")
        
        return preferences
    
    def interactive_learning_session(self, user_id: str):
        """대화형 학습 세션"""
        print(f"\n🎓 {user_id}님의 학습 세션을 시작합니다!")
        
        session_start = datetime.now()
        session_log = {
            "user_id": user_id,
            "start_time": session_start.isoformat(),
            "activities": []
        }
        
        while True:
            print("\n" + "="*40)
            print("📚 학습 메뉴")
            print("="*40)
            print("1. 콘텐츠 학습")
            print("2. 문제 풀이")
            print("3. 메인 메뉴로 돌아가기")
            
            choice = input("선택하세요 (1-3): ").strip()
            
            if choice == "1":
                self.content_learning_session(user_id, session_log)
            elif choice == "2":
                self.problem_solving_session(user_id, session_log)
            elif choice == "3":
                break
            else:
                print("❌ 잘못된 선택입니다.")
        
        # 세션 종료
        session_log["end_time"] = datetime.now().isoformat()
        session_log["duration"] = str(datetime.now() - session_start)
        self.save_session_log(session_log)
        
        print(f"\n👋 학습 세션이 종료되었습니다. 수고하셨습니다!")
    
    def content_learning_session(self, user_id: str, session_log: Dict[str, Any]):
        """콘텐츠 학습 세션"""
        print("\n📖 콘텐츠 학습")
        
        # 기본 콘텐츠 가져오기 (추천 시스템 사용하지 않음)
        content = self.system.get_personalized_content(user_id)
        
        if "error" in content:
            print(f"❌ {content['error']}")
            return
        
        print(f"\n📚 학습 콘텐츠: {content['content']['title']}")
        print(f"📝 내용: {content['content']['content']}")
        print(f"📊 난이도: {'⭐' * content['content']['difficulty']}")
        
        # 학습 진행 의사 확인
        proceed = input("\n학습을 진행하시겠습니까? (y/n): ").strip().lower()
        if proceed not in ['y', 'yes', '네', 'ㅇ']:
            return
        
        # 학습 시작
        print("\n🚀 학습을 시작합니다...")
        self.display_content_details(content)
        
        # 활동 로그 기록
        session_log["activities"].append({
            "type": "content_learning",
            "content_id": content['content_id'],
            "timestamp": datetime.now().isoformat()
        })
        
        # 이해도 확인
        self.check_understanding(user_id, content)
    
    def display_content_details(self, content: Dict[str, Any]):
        """콘텐츠 상세 표시"""
        print("\n" + "="*50)
        print(f"📚 {content['content']['title']}")
        print("="*50)
        
        # 기본 설명
        print(f"📖 {content['content']['content']}")
        
        # 추가 상세 설명 제공
        detailed_explanations = {
            "stats_basics": self.explain_descriptive_stats(),
            "probability": self.explain_probability(),
            "hypothesis_testing": self.explain_hypothesis_testing()
        }
        
        content_id = content['content_id']
        if content_id in detailed_explanations:
            print("\n📋 상세 설명:")
            detailed_explanations[content_id]()
        
        # 핵심 포인트 정리
        print("\n🎯 핵심 포인트:")
        key_points = self.get_key_points(content_id)
        for i, point in enumerate(key_points, 1):
            print(f"   {i}. {point}")
        
        # 실제 예시 제공
        print("\n💡 실제 예시:")
        example = self.get_practical_example(content_id)
        print(f"   {example}")
        
        input("\n📖 내용을 확인했으면 Enter를 누르세요...")
    
    def explain_descriptive_stats(self):
        """기술통계 상세 설명"""
        print("""
🔢 기술통계란 데이터의 특성을 숫자로 요약하는 방법입니다.

📊 중심경향성 (데이터의 중심):
   • 평균 (Mean): 모든 값의 합 ÷ 개수
   • 중앙값 (Median): 크기 순으로 나열한 가운데 값
   • 최빈값 (Mode): 가장 자주 나타나는 값

📈 산포도 (데이터의 퍼짐):
   • 범위 (Range): 최댓값 - 최솟값
   • 분산 (Variance): 평균으로부터 떨어진 정도의 제곱 평균
   • 표준편차 (Standard Deviation): 분산의 제곱근

🎯 언제 사용하나요?
   • 데이터의 전체적인 모습을 파악할 때
   • 서로 다른 데이터를 비교할 때
   • 데이터의 이상치를 찾을 때
        """)
    
    def explain_probability(self):
        """확률 상세 설명"""
        print("""
🎲 확률이란 어떤 사건이 일어날 가능성을 0과 1 사이의 수로 나타낸 것입니다.

📝 기본 개념:
   • 표본공간: 일어날 수 있는 모든 결과
   • 사건: 관심 있는 특정 결과들의 집합
   • 확률: 사건이 일어날 가능성 (0 ≤ P(A) ≤ 1)

🔢 확률 계산:
   • P(A) = 사건 A가 일어날 경우의 수 / 전체 경우의 수
   • P(A ∪ B) = P(A) + P(B) - P(A ∩ B)  (합사건)
   • P(A ∩ B) = P(A) × P(B)  (독립사건의 곱사건)

🎯 실생활 활용:
   • 날씨 예보 (비 올 확률 70%)
   • 의료 진단 (검사 정확도 95%)
   • 투자 결정 (수익률 예측)
        """)
    
    def explain_hypothesis_testing(self):
        """가설검정 상세 설명"""
        print("""
🔬 가설검정이란 데이터를 통해 가설이 옳은지 판단하는 통계적 방법입니다.

📋 기본 단계:
   1. 귀무가설(H₀) 설정: 변화가 없다, 차이가 없다
   2. 대립가설(H₁) 설정: 변화가 있다, 차이가 있다
   3. 유의수준(α) 설정: 보통 0.05 (5%)
   4. 검정통계량 계산
   5. p-값 계산 및 결론 도출

⚠️ 오류 종류:
   • 1종 오류: 참인 H₀를 기각 (α의 확률로 발생)
   • 2종 오류: 거짓인 H₀를 채택 (β의 확률로 발생)

🎯 실제 적용:
   • 신약 효과 검증
   • 마케팅 전략 효과 분석
   • 품질 관리 검사
        """)
    
    def get_key_points(self, content_id: str) -> List[str]:
        """핵심 포인트 반환"""
        key_points_map = {
            "stats_basics": [
                "평균은 이상치에 민감하지만 중앙값은 안정적",
                "분산과 표준편차는 데이터의 퍼짐 정도를 나타냄",
                "데이터의 분포 형태에 따라 적절한 통계량 선택 필요"
            ],
            "probability": [
                "확률의 합은 항상 1",
                "독립사건의 곱은 각 확률의 곱",
                "조건부 확률은 정보가 주어진 상황에서의 확률"
            ],
            "hypothesis_testing": [
                "귀무가설은 '변화 없음'을 가정",
                "p-값이 유의수준보다 작으면 귀무가설 기각",
                "통계적 유의성과 실질적 중요성은 다름"
            ]
        }
        return key_points_map.get(content_id, ["학습 내용을 정리해보세요"])
    
    def get_practical_example(self, content_id: str) -> str:
        """실제 예시 반환"""
        examples_map = {
            "stats_basics": "학생 10명의 키를 측정했더니 평균 170cm, 표준편차 5cm였다면, 대부분의 학생이 165-175cm 사이에 있을 것입니다.",
            "probability": "동전을 두 번 던져서 모두 앞면이 나올 확률은 1/2 × 1/2 = 1/4 = 0.25 = 25%입니다.",
            "hypothesis_testing": "새로운 교육 방법이 기존 방법보다 효과적인지 확인하기 위해 두 그룹의 점수를 비교하는 t-검정을 실시합니다."
        }
        return examples_map.get(content_id, "구체적인 예시를 생각해보세요")
    
    def check_understanding(self, user_id: str, content: Dict[str, Any]):
        """이해도 확인"""
        print("\n🤔 이해도 확인")
        print("방금 학습한 내용에 대해 확인해보겠습니다.")
        
        understanding_level = input("\n이해도를 선택하세요 (1: 어려움, 2: 보통, 3: 잘 이해): ").strip()
        
        if understanding_level == "1":
            print("💪 다시 한 번 차근차근 학습해보시길 권합니다.")
            print("📚 추가 자료나 기초 내용부터 시작하는 것이 좋겠습니다.")
        elif understanding_level == "2":
            print("👍 좋습니다! 연습 문제로 실력을 다져보세요.")
        elif understanding_level == "3":
            print("🎉 훌륭합니다! 다음 단계로 진행할 준비가 되었습니다.")
        
        # 추가 질문이나 설명 제공
        need_more = input("\n추가 설명이 필요하신가요? (y/n): ").strip().lower()
        if need_more in ['y', 'yes', '네', 'ㅇ']:
            self.provide_additional_explanation(content['content_id'])
    
    def provide_additional_explanation(self, content_id: str):
        """추가 설명 제공"""
        print("\n📖 추가 설명")
        
        additional_info = {
            "stats_basics": """
🔍 더 깊이 알아보기:

📊 어떤 상황에서 어떤 통계량을 사용할까요?
   • 정규분포: 평균과 표준편차 사용
   • 치우친 분포: 중앙값과 사분위수 사용
   • 범주형 데이터: 최빈값과 빈도 사용

💡 실무 팁:
   • 데이터를 처음 볼 때는 히스토그램부터 그려보세요
   • 이상치가 있는지 항상 확인하세요
   • 여러 통계량을 함께 보면 더 정확한 판단이 가능합니다

🎯 연습 방법:
   • 실제 데이터(키, 몸무게, 점수 등)로 직접 계산해보세요
   • 계산기나 엑셀을 활용해보세요
            """,
            "probability": """
🔍 확률의 직관적 이해:

🎲 확률을 체감하는 방법:
   • 동전 던지기를 100번 해보면 대략 50번 정도 앞면이 나옵니다
   • 주사위를 600번 던지면 각 면이 대략 100번씩 나옵니다
   • 복권 당첨 확률은 매우 낮지만 0은 아닙니다

🧠 흔한 착각들:
   • 동전을 5번 던져 모두 앞면이 나와도 다음은 50% 확률
   • 과거 결과가 미래에 영향을 주지 않습니다 (독립사건)
   • 확률이 낮다고 절대 일어나지 않는 것은 아닙니다

🎯 실생활 적용:
   • 보험료 계산
   • 게임 전략 수립
   • 위험 관리
            """,
            "hypothesis_testing": """
🔍 가설검정의 철학:

🤔 왜 가설검정이 필요한가?
   • 우연에 의한 차이인지 진짜 차이인지 구분하기 위해
   • 객관적인 판단 기준을 제공하기 위해
   • 의사결정에 과학적 근거를 제공하기 위해

⚖️ 판단의 기준:
   • p-값이 0.05보다 작으면 "통계적으로 유의하다"
   • 하지만 0.05는 관례일 뿐, 절대적 기준은 아님
   • 실질적 중요성도 함께 고려해야 함

🎯 해석 주의사항:
   • "유의하다" ≠ "중요하다"
   • "유의하지 않다" ≠ "차이가 없다"
   • 표본 크기가 클수록 작은 차이도 유의하게 나옴
            """
        }
        
        info = additional_info.get(content_id, "추가 정보를 준비 중입니다.")
        print(info)
        
        input("\n📚 추가 설명을 확인했으면 Enter를 누르세요...")
    
    def problem_solving_session(self, user_id: str, session_log: Dict[str, Any]):
        """문제 풀이 세션"""
        print("\n🧩 문제 풀이 세션")
        
        # 현재 사용자 수준에 맞는 콘텐츠 가져오기
        content = self.system.get_personalized_content(user_id)
        
        if "error" in content:
            print(f"❌ {content['error']}")
            return
        
        questions = content['content']['questions']
        content_id = content['content_id']
        
        print(f"📝 {content['content']['title']} 문제풀이")
        print(f"📊 총 {len(questions)}개 문제")
        
        correct_count = 0
        total_questions = len(questions)
        
        for i, question in enumerate(questions):
            print(f"\n{'='*50}")
            print(f"📋 문제 {i+1}/{total_questions}")
            print(f"{'='*50}")
            print(f"❓ {question['q']}")
            
            # 선택지 표시
            for j, option in enumerate(question['options']):
                print(f"  {j+1}. {option}")
            
            # 답변 입력
            while True:
                try:
                    answer = input(f"\n답을 선택하세요 (1-{len(question['options'])}): ").strip()
                    answer_idx = int(answer) - 1
                    
                    if 0 <= answer_idx < len(question['options']):
                        break
                    else:
                        print(f"❌ 1-{len(question['options'])} 사이의 숫자를 입력하세요.")
                except ValueError:
                    print("❌ 숫자를 입력하세요.")
            
            # 정답 확인
            result = self.system.submit_answer(user_id, content_id, i, answer_idx)
            
            if result['correct']:
                correct_count += 1
                print("✅ 정답입니다! 🎉")
            else:
                print("❌ 틀렸습니다.")
                print(f"🔍 정답: {result['correct_answer']}")
            
            # 상세 해설 제공
            print(f"\n💡 해설:")
            print(f"   {result['explanation']}")
            
            # 추가 설명 제공
            self.provide_detailed_explanation(content_id, i, question, result)
            
            # 다음 문제로 진행
            if i < total_questions - 1:
                input("\n⏭️ 다음 문제로 진행하려면 Enter를 누르세요...")
        
        # 최종 결과 표시
        self.show_problem_solving_results(correct_count, total_questions, user_id)
        
        # 활동 로그 기록
        session_log["activities"].append({
            "type": "problem_solving",
            "content_id": content_id,
            "correct_count": correct_count,
            "total_questions": total_questions,
            "score": (correct_count / total_questions) * 100,
            "timestamp": datetime.now().isoformat()
        })
    
    def provide_detailed_explanation(self, content_id: str, question_idx: int, 
                                   question: Dict[str, Any], result: Dict[str, Any]):
        """상세 해설 제공"""
        print(f"\n🔍 상세 해설:")
        
        # 문제 유형별 상세 해설
        detailed_explanations = {
            ("stats_basics", 0): """
📊 평균 계산 방법:
   • 모든 값을 더한 후 개수로 나눕니다
   • 공식: (x₁ + x₂ + ... + xₙ) ÷ n
   • 예시: [1,2,3,4,5]의 평균 = (1+2+3+4+5)÷5 = 15÷5 = 3
   
💡 실무 적용:
   • 성적 평가, 품질 관리, 재무 분석 등에 활용
   • 이상치가 있을 때는 중앙값 고려
            """,
            ("stats_basics", 1): """
📈 분포의 치우침 (Skewness):
   • 평균 > 중앙값: 오른쪽 치우침 (positive skew)
   • 평균 < 중앙값: 왼쪽 치우침 (negative skew)
   • 평균 = 중앙값: 대칭 분포
   
💡 실제 예시:
   • 소득 분포: 대부분 오른쪽 치우침
   • 시험 점수: 어려우면 왼쪽, 쉬우면 오른쪽 치우침
            """,
            ("probability", 0): """
🎲 독립사건의 곱셈 법칙:
   • 두 사건이 독립이면: P(A ∩ B) = P(A) × P(B)
   • 동전 던지기는 매번 독립사건
   • 앞면 확률 = 1/2, 두 번 모두 앞면 = 1/2 × 1/2 = 1/4
   
💡 실생활 예시:
   • 두 번의 무작위 추첨에서 연속 당첨 확률
   • 연속된 날씨 예측의 정확도
            """
        }
        
        key = (content_id, question_idx)
        if key in detailed_explanations:
            print(detailed_explanations[key])
        
        # 오답일 경우 추가 도움말
        if not result['correct']:
            print(f"\n🤔 다시 생각해보기:")
            self.provide_wrong_answer_guidance(content_id, question_idx, question)
    
    def provide_wrong_answer_guidance(self, content_id: str, question_idx: int, 
                                    question: Dict[str, Any]):
        """오답 시 가이드 제공"""
        guidance_map = {
            ("stats_basics", 0): """
🔄 다시 접근해보기:
   1. 주어진 숫자들을 모두 더해보세요
   2. 개수를 세어보세요
   3. 합계를 개수로 나누어보세요
   
📝 단계별 계산:
   • 1단계: 1+2+3+4+5 = ?
   • 2단계: 개수는 5개
   • 3단계: 합계 ÷ 5 = ?
            """,
            ("stats_basics", 1): """
🔄 분포의 형태 생각해보기:
   1. 평균과 중앙값 중 어느 것이 더 큰가요?
   2. 큰 값 쪽으로 치우친 것입니다
   3. 평균이 중앙값보다 크면 → 오른쪽 치우침
   
💡 기억 방법:
   • 평균은 극값에 끌려가는 성질이 있습니다
   • 중앙값은 상대적으로 안정적입니다
            """,
            ("probability", 0): """
🔄 확률 계산 다시 해보기:
   1. 첫 번째 동전: 앞면 확률 = ?
   2. 두 번째 동전: 앞면 확률 = ?
   3. 둘 다 앞면: 첫 번째 × 두 번째 = ?
   
💡 기억 방법:
   • 독립사건 = 곱셈
   • 1/2 × 1/2 = 1/4
            """
        }
        
        key = (content_id, question_idx)
        if key in guidance_map:
            print(guidance_map[key])
    
    def show_problem_solving_results(self, correct: int, total: int, user_id: str):
        """문제 풀이 결과 표시"""
        score = (correct / total) * 100
        
        print(f"\n{'='*50}")
        print("🎯 문제 풀이 결과")
        print(f"{'='*50}")
        print(f"✅ 정답: {correct}/{total} 문제")
        print(f"📊 정답률: {score:.1f}%")
        
        # 성과 평가
        if score >= 90:
            print("🏆 우수! 완벽하게 이해했습니다!")
            print("💡 다음 단계로 진행할 준비가 되었습니다.")
        elif score >= 70:
            print("👍 양호! 대부분 이해했습니다.")
            print("💡 틀린 부분을 다시 한 번 확인해보세요.")
        elif score >= 50:
            print("⚠️ 보통! 좀 더 연습이 필요합니다.")
            print("💡 기초 개념을 다시 복습하는 것이 좋겠습니다.")
        else:
            print("🔄 미흡! 기초부터 다시 시작하세요.")
            print("💡 개념 학습을 먼저 하시길 권합니다.")
        
        # 개인화된 피드백
        feedback = self.system.generate_adaptive_feedback(user_id, None)
        if feedback:
            print(f"\n🎯 맞춤형 조언:")
            print(f"   {feedback.get('message', '열심히 하세요!')}")
            
            if feedback.get('next_steps'):
                print(f"\n📋 다음 단계:")
                for step in feedback['next_steps']:
                    print(f"   • {step}")
    
    def show_progress(self, user_id: str):
        """학습 진도 표시"""
        print(f"\n📈 {user_id}님의 학습 진도")
        print("="*50)
        
        # 학습 분석 가져오기
        analytics = self.system.get_learning_analytics(user_id)
        
        if "error" in analytics:
            print(f"❌ {analytics['error']}")
            return
        
        if analytics.get("message"):
            print(analytics["message"])
            return
        
        # 전체 성과 표시
        overall = analytics["overall_stats"]
        print(f"📊 전체 성과:")
        print(f"   총 시도: {overall['total_attempts']}회")
        print(f"   정답: {overall['correct_attempts']}회")
        print(f"   정답률: {overall['success_rate']}%")
        print(f"   현재 레벨: {overall['current_level']}")
        
        # 최근 성과 표시
        recent = analytics["recent_performance"]
        print(f"\n📈 최근 성과:")
        print(f"   최근 시도: {recent['last_10_attempts']}회")
        print(f"   최근 정답률: {recent['recent_success_rate']}%")
        
        # 학습 상태 및 추천사항
        print(f"\n🎯 학습 상태: {analytics['learning_state']}")
        print(f"💡 추천사항: {analytics['recommendation']}")
        
        # 적응형 설정 표시
        adaptive = analytics["adaptive_settings"]
        print(f"\n⚙️ 적응형 설정:")
        print(f"   난이도 선호: {adaptive['difficulty_preference']:.1f}/10")
        print(f"   학습 속도: {adaptive['learning_pace']}")
        print(f"   성공률: {adaptive['success_rate']:.1%}")
        
        # 진도 시각화
        self.visualize_progress(overall['success_rate'])
    
    def visualize_progress(self, success_rate: float):
        """진도 시각화"""
        print(f"\n📊 성과 시각화:")
        
        # 진도 바 생성
        bar_length = 20
        filled_length = int(success_rate / 100 * bar_length)
        bar = "█" * filled_length + "░" * (bar_length - filled_length)
        
        print(f"   진도: [{bar}] {success_rate:.1f}%")
        
        # 레벨 표시
        if success_rate < 30:
            print("   수준: 🔰 초보자")
        elif success_rate < 60:
            print("   수준: 📚 학습자")
        elif success_rate < 80:
            print("   수준: 🎯 숙련자")
        else:
            print("   수준: 🏆 전문가")
    
    def show_analytics(self, user_id: str):
        """성과 분석 표시"""
        print(f"\n📊 {user_id}님의 상세 성과 분석")
        print("="*50)
        
        analytics = self.system.get_learning_analytics(user_id)
        
        if "error" in analytics:
            print(f"❌ {analytics['error']}")
            return
        
        # 기본 분석 표시
        self.show_progress(user_id)
        
        # 추가 분석 정보
        print(f"\n🔍 상세 분석:")
        
        # 학습 패턴 분석
        print(f"   학습 패턴: 꾸준한 학습자 유형")
        print(f"   강점 영역: 기초 개념 이해")
        print(f"   개선 영역: 응용 문제 해결")
        
        # 추천 학습 계획
        print(f"\n📋 추천 학습 계획:")
        print(f"   1. 약점 보완: 확률 개념 다시 학습")
        print(f"   2. 실습 증가: 더 많은 문제 풀이")
        print(f"   3. 심화 학습: 다음 레벨 도전")
        
        # 목표 설정 제안
        print(f"\n🎯 목표 설정 제안:")
        print(f"   단기 목표: 이번 주 정답률 80% 달성")
        print(f"   중기 목표: 다음 달 중급 레벨 진입")
        print(f"   장기 목표: 3개월 내 전체 과정 완료")
    
    def set_learning_goals(self, user_id: str):
        """학습 목표 설정"""
        print(f"\n🎯 {user_id}님의 학습 목표 설정")
        print("="*50)
        
        print("현재 가능한 목표:")
        print("1. 정답률 향상 (예: 80% 달성)")
        print("2. 레벨 승급 (다음 단계 진입)")
        print("3. 약점 보완 (특정 영역 집중)")
        print("4. 학습 시간 증가 (더 많은 연습)")
        
        choice = input("\n설정하고 싶은 목표를 선택하세요 (1-4): ").strip()
        
        if choice == "1":
            target_rate = input("목표 정답률을 입력하세요 (예: 80): ").strip()
            print(f"✅ 목표 설정 완료: 정답률 {target_rate}% 달성")
        elif choice == "2":
            print("✅ 목표 설정 완료: 다음 레벨 진입")
        elif choice == "3":
            weak_area = input("집중하고 싶은 영역을 입력하세요 (예: 확률): ").strip()
            print(f"✅ 목표 설정 완료: {weak_area} 영역 집중 학습")
        elif choice == "4":
            study_time = input("주간 목표 학습 시간을 입력하세요 (예: 5시간): ").strip()
            print(f"✅ 목표 설정 완료: 주간 {study_time} 학습")
        
        print("\n💡 목표 달성을 위한 시스템이 개인화된 학습 계획을 제공합니다!")
    
    def run_visualization_demo(self):
        """시각화 데모 실행"""
        print("\n📊 데이터 시각화 데모")
        print("=" * 50)
        
        if not self.visualization_engine:
            print("❌ 시각화 엔진을 사용할 수 없습니다.")
            return
        
        print("다양한 시각화 기능을 체험해보세요:\n")
        
        # 샘플 데이터 생성
        import random
        random.seed(42)
        
        # 정규분포 데이터
        normal_data = [random.gauss(50, 10) for _ in range(30)]
        
        # 카테고리 데이터
        categories = ["A그룹", "B그룹", "C그룹", "D그룹"]
        values = [85, 92, 78, 88]
        
        # 상관관계 데이터
        x_data = list(range(1, 16))
        y_data = [2*x + random.gauss(0, 3) for x in x_data]
        
        print("1. 📈 기본 통계량 요약")
        print(self.visualization_engine.create_distribution_summary(normal_data))
        
        print("\n\n2. 📊 히스토그램")
        print(self.visualization_engine.create_histogram_ascii(normal_data, "정규분포 예시"))
        
        print("\n\n3. 📊 막대 차트")
        print(self.visualization_engine.create_bar_chart_ascii(categories, values, "그룹별 성과"))
        
        print("\n\n4. 📊 산점도")
        print(self.visualization_engine.create_scatter_plot_ascii(x_data, y_data, "선형 관계 예시"))
        
        print("\n\n5. 🔥 상관계수 히트맵")
        correlation_data = {
            "수학": [80, 85, 90, 75, 88, 92, 78],
            "과학": [82, 87, 89, 73, 90, 94, 76],
            "영어": [78, 83, 91, 70, 85, 89, 74]
        }
        print(self.visualization_engine.create_correlation_heatmap(correlation_data))
        
        print("\n\n✨ 시각화는 데이터의 패턴을 한눈에 파악하는 강력한 도구입니다!")
        input("\n계속하려면 엔터를 누르세요...")
    
    def run_interactive_tutorial(self):
        """인터랙티브 튜토리얼 실행"""
        print("\n🎓 인터랙티브 튜토리얼")
        print("=" * 50)
        
        print("사용 가능한 튜토리얼:\n")
        print("1. 📊 기술통계 완전 정복")
        print("2. 🎲 확률론 마스터하기")
        print("3. 🔬 가설검정 심화 학습")
        print("4. 📈 회귀분석 전문가 과정")
        print("5. 🎯 맞춤형 개념 설명")
        print("6. 메인 메뉴로 돌아가기")
        
        choice = input("\n원하는 튜토리얼을 선택하세요 (1-6): ").strip()
        
        tutorial_map = {
            "1": "stats_basics",
            "2": "probability", 
            "3": "hypothesis_testing",
            "4": "regression_analysis"
        }
        
        if choice in tutorial_map:
            content_id = tutorial_map[choice]
            self.start_detailed_tutorial(content_id)
        elif choice == "5":
            self.start_concept_explanation()
        elif choice == "6":
            return
        else:
            print("❌ 잘못된 선택입니다.")
    
    def start_detailed_tutorial(self, content_id: str):
        """상세 튜토리얼 시작"""
        print(f"\n🎯 {content_id} 심화 학습을 시작합니다...")
        
        # 사용자 프로필 (기본값)
        user_profile = {
            "user_id": "tutorial_user",
            "experience_level": "intermediate",
            "learning_style": "visual",
            "goals": ["개념 이해", "실용적 적용"]
        }
        
        # 인터랙티브 튜토리얼 생성
        tutorial = self.tutorial_engine.create_interactive_tutorial(content_id, user_profile)
        
        print(f"\n📚 {tutorial['title']}")
        print(f"⏱️ 예상 소요 시간: {tutorial.get('estimated_time', '30-45분')}")
        print(f"📋 총 {tutorial['total_steps']}개 모듈로 구성")
        
        # 튜토리얼 모듈 실행
        for i, module in enumerate(tutorial['modules'], 1):
            print(f"\n\n{'='*60}")
            print(f"📖 모듈 {i}/{len(tutorial['modules'])}: {module['title']}")
            print(f"⏱️ {module['estimated_time']}")
            print("="*60)
            
            self.run_tutorial_module(module)
            
            if i < len(tutorial['modules']):
                continue_choice = input("\n다음 모듈로 진행하시겠습니까? (y/n): ").strip().lower()
                if continue_choice != 'y':
                    break
        
        print("\n🎉 튜토리얼을 완료했습니다! 수고하셨습니다.")
        
    def run_tutorial_module(self, module: dict):
        """튜토리얼 모듈 실행"""
        print(f"\n{module.get('description', '')}")
        
        for activity in module.get('activities', []):
            print(f"\n🎯 {activity['title']}")
            print("-" * 40)
            print(activity['content'])
            
            # 인터랙션 시뮬레이션
            if activity.get('interaction') == 'reflection_questions':
                user_input = input("\n💭 생각을 자유롭게 적어보세요: ")
                print("✅ 좋은 생각입니다! 이런 사고과정이 학습에 도움이 됩니다.")
            elif activity.get('interaction') == 'step_by_step_guidance':
                input("\n➡️ 다음 단계로 진행하려면 엔터를 누르세요...")
            elif activity.get('interaction') == 'immediate_feedback':
                answer = input("\n❓ 간단한 질문: 이해가 되셨나요? (y/n): ")
                if answer.lower() == 'y':
                    print("✅ 훌륭합니다! 계속 진행해보세요.")
                else:
                    print("🤔 괜찮습니다. 다시 한번 차근차근 읽어보세요.")
    
    def start_concept_explanation(self):
        """개념별 상세 설명"""
        concept = input("\n설명을 듣고 싶은 개념을 입력하세요 (예: 평균, 확률, 가설검정): ").strip()
        
        if not concept:
            print("❌ 개념을 입력해주세요.")
            return
        
        print(f"\n📚 '{concept}' 개념 설명을 준비합니다...")
        
        # 상세 설명 생성
        explanation = self.explanation_engine.generate_detailed_explanation(concept, "intermediate")
        
        print(f"\n{'='*60}")
        print(f"📖 {concept} 완전 분석")
        print("="*60)
        
        for section in explanation['sections']:
            print(f"\n\n{section['title']}")
            print("-" * 50)
            
            if section['type'] == 'introduction':
                content = section['content']
                print(f"\n📝 정의: {content['definition']}")
                print(f"\n💡 중요성: {content['importance']}")
                print("\n🎯 핵심 포인트:")
                for point in content['key_points']:
                    print(f"  • {point}")
                    
            elif section['type'] == 'step_by_step':
                content = section['content']
                print("\n📋 단계별 과정:")
                for step in content['steps']:
                    print(f"  {step['step']}. {step['action']}")
                    print(f"     💡 {step['detail']}")
                    
            elif section['type'] == 'examples':
                content = section['content']
                print(f"\n📖 {content.get('title', '예시')}")
                print(f"\n🎬 시나리오: {content.get('scenario', '')}")
                if 'lessons' in content:
                    print("\n📚 학습 포인트:")
                    for lesson in content['lessons']:
                        print(f"  • {lesson}")
                        
            elif section['type'] == 'misconceptions':
                content = section['content']
                misconceptions = content.get('misconceptions', [])
                if misconceptions:
                    print("\n⚠️ 주의할 점들:")
                    for misc in misconceptions:
                        print(f"\n❌ 흔한 오해: {misc['misconception']}")
                        print(f"✅ 실제: {misc['reality']}")
                        if 'example' in misc:
                            print(f"📝 예시: {misc['example']}")
        
        print("\n\n✨ 설명이 도움이 되셨나요? 더 궁금한 점이 있으면 언제든 물어보세요!")
        input("\n계속하려면 엔터를 누르세요...")
    
    def show_system_settings(self):
        """시스템 설정 표시"""
        print("\n🔧 시스템 설정")
        print("="*40)
        print("1. 사용자 데이터 관리")
        print("2. 학습 기록 확인")
        print("3. 시스템 정보")
        print("4. 데이터 초기화")
        print("5. 메인 메뉴로 돌아가기")
        
        choice = input("선택하세요 (1-5): ").strip()
        
        if choice == "1":
            self.manage_user_data()
        elif choice == "2":
            self.show_learning_records()
        elif choice == "3":
            self.show_system_info()
        elif choice == "4":
            self.reset_data()
        elif choice == "5":
            return
        else:
            print("❌ 잘못된 선택입니다.")
    
    def manage_user_data(self):
        """사용자 데이터 관리"""
        print("\n👤 사용자 데이터 관리")
        
        users = self.load_user_data()
        
        if not users:
            print("등록된 사용자가 없습니다.")
            return
        
        print("등록된 사용자:")
        for user_id, data in users.items():
            print(f"  • {user_id} (가입일: {data.get('created_at', 'N/A')[:10]})")
        
        print("\n1. 사용자 삭제")
        print("2. 사용자 정보 수정")
        print("3. 돌아가기")
        
        choice = input("선택하세요 (1-3): ").strip()
        
        if choice == "1":
            user_to_delete = input("삭제할 사용자 이름: ").strip()
            if user_to_delete in users:
                del users[user_to_delete]
                self.save_user_data(users)
                print(f"✅ {user_to_delete} 삭제 완료")
            else:
                print("❌ 사용자를 찾을 수 없습니다.")
        elif choice == "2":
            print("사용자 정보 수정 기능은 개발 중입니다.")
    
    def show_learning_records(self):
        """학습 기록 확인"""
        print("\n📚 학습 기록")
        
        try:
            with open(self.session_log_file, 'r', encoding='utf-8') as f:
                logs = json.load(f)
            
            if not logs:
                print("학습 기록이 없습니다.")
                return
            
            print(f"총 {len(logs)}개의 학습 세션:")
            for log in logs[-5:]:  # 최근 5개만 표시
                print(f"  • {log['user_id']} - {log['start_time'][:10]} - {len(log['activities'])}개 활동")
        
        except FileNotFoundError:
            print("학습 기록 파일이 없습니다.")
    
    def show_system_info(self):
        """시스템 정보 표시"""
        print("\n💻 시스템 정보")
        print("="*40)
        
        # 시스템 통계
        stats = self.system.get_system_stats()
        print(f"총 학습자: {stats['total_learners']}명")
        print(f"총 상호작용: {stats['total_interactions']}회")
        print(f"전체 성공률: {stats['overall_success_rate']}%")
        print(f"콘텐츠 수: {stats['content_library_size']}개")
        
        # 파일 정보
        print(f"\n📁 데이터 파일:")
        print(f"사용자 데이터: {self.user_data_file}")
        print(f"세션 로그: {self.session_log_file}")
        
        # 버전 정보
        print(f"\n🔧 버전 정보:")
        print(f"시스템 버전: v2.0")
        print(f"Python 버전: {sys.version}")
    
    def reset_data(self):
        """데이터 초기화"""
        print("\n⚠️ 데이터 초기화")
        print("모든 학습 기록과 사용자 데이터가 삭제됩니다.")
        
        confirm = input("정말로 초기화하시겠습니까? (yes/no): ").strip().lower()
        
        if confirm == "yes":
            try:
                if os.path.exists(self.user_data_file):
                    os.remove(self.user_data_file)
                if os.path.exists(self.session_log_file):
                    os.remove(self.session_log_file)
                
                # 시스템 재초기화
                self.system = SimpleLearningSystem()
                
                print("✅ 데이터 초기화 완료")
            except Exception as e:
                print(f"❌ 초기화 중 오류: {e}")
        else:
            print("초기화가 취소되었습니다.")
    
    def show_learning_guide(self):
        """학습 가이드 표시"""
        print("\n📖 학습 가이드")
        print("="*50)
        
        print("""
🎯 효과적인 학습 방법:

1. 📅 규칙적인 학습
   • 매일 조금씩 꾸준히 학습하세요
   • 한 번에 너무 많이 하지 마세요
   • 휴식을 적절히 취하세요

2. 🔄 반복 학습
   • 어려운 개념은 여러 번 반복하세요
   • 문제를 다시 풀어보세요
   • 설명을 자주 읽어보세요

3. 💡 능동적 학습
   • 단순히 읽기만 하지 마세요
   • 직접 문제를 풀어보세요
   • 다른 사람에게 설명해보세요

4. 🎯 목표 설정
   • 명확한 학습 목표를 세우세요
   • 진도를 정기적으로 확인하세요
   • 성취를 축하하세요

5. 🤝 도움 요청
   • 어려운 내용은 언제든 질문하세요
   • 추가 설명을 요청하세요
   • 다양한 예시를 활용하세요
        """)
        
        print("\n🔗 추가 학습 자료:")
        print("   • 온라인 강의 플랫폼 활용")
        print("   • 통계학 관련 도서 읽기")
        print("   • 실습 데이터로 연습하기")
        print("   • 학습 커뮤니티 참여")
        
        input("\n📚 가이드를 확인했으면 Enter를 누르세요...")
    
    def run_demo_mode(self):
        """데모 모드 실행"""
        print("\n🧪 데모 모드")
        print("시스템의 모든 기능을 간단히 체험해볼 수 있습니다.")
        
        # 데모 사용자 자동 등록
        demo_user = "demo_user"
        demo_profile = {
            "name": "데모 사용자",
            "learning_style": "visual",
            "learning_pace": "medium",
            "learning_goal": "basic_understanding",
            "weekly_hours": 4
        }
        
        self.system.register_learner(demo_user, demo_profile)
        print(f"✅ 데모 사용자 '{demo_user}' 생성 완료")
        
        # 자동 학습 시연
        print("\n🎬 자동 학습 시연:")
        
        # 1. 콘텐츠 추천
        print("\n1. 개인화된 콘텐츠 추천")
        content = self.system.get_personalized_content(demo_user)
        print(f"   추천 콘텐츠: {content['content']['title']}")
        print(f"   추천 이유: {content['recommendation_reason']}")
        
        # 2. 자동 문제 풀이
        print("\n2. 자동 문제 풀이")
        questions = content['content']['questions']
        for i, question in enumerate(questions):
            print(f"   문제 {i+1}: {question['q']}")
            correct_answer = question['correct']
            result = self.system.submit_answer(demo_user, content['content_id'], i, correct_answer)
            print(f"   결과: {'✅' if result['correct'] else '❌'}")
        
        # 3. 학습 분석
        print("\n3. 학습 분석")
        analytics = self.system.get_learning_analytics(demo_user)
        print(f"   성공률: {analytics['overall_stats']['success_rate']}%")
        print(f"   학습 상태: {analytics['learning_state']}")
        
        # 4. 시스템 통계
        print("\n4. 시스템 통계")
        stats = self.system.get_system_stats()
        print(f"   총 상호작용: {stats['total_interactions']}회")
        print(f"   전체 성공률: {stats['overall_success_rate']}%")
        
        print("\n🎉 데모 완료! 실제 학습을 시작하려면 새 사용자를 등록하세요.")
        input("Enter를 누르면 메인 메뉴로 돌아갑니다...")
    
    def load_user_data(self) -> Dict[str, Any]:
        """사용자 데이터 로드"""
        try:
            with open(self.user_data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def save_user_data(self, data: Dict[str, Any]):
        """사용자 데이터 저장"""
        with open(self.user_data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def save_session_log(self, log: Dict[str, Any]):
        """세션 로그 저장"""
        try:
            with open(self.session_log_file, 'r', encoding='utf-8') as f:
                logs = json.load(f)
        except FileNotFoundError:
            logs = []
        
        logs.append(log)
        
        with open(self.session_log_file, 'w', encoding='utf-8') as f:
            json.dump(logs, f, ensure_ascii=False, indent=2)
    
    def run(self):
        """메인 실행 루프"""
        self.show_welcome()
        
        while True:
            self.show_main_menu()
            choice = input("선택하세요 (1-8): ").strip()
            
            if choice == "1":
                self.run_web_interface()
            elif choice == "2":
                self.run_interactive_mode()
            elif choice == "3":
                self.show_system_settings()
            elif choice == "4":
                self.show_learning_guide()
            elif choice == "5":
                self.run_demo_mode()
            elif choice == "6":
                self.run_visualization_demo()
            elif choice == "7":
                self.run_interactive_tutorial()
            elif choice == "8":
                print("\n👋 학습 시스템을 종료합니다.")
                print("🎓 학습하느라 수고하셨습니다!")
                break
            else:
                print("❌ 잘못된 선택입니다. 1-8 사이의 숫자를 입력하세요.")


def main():
    """메인 함수"""
    try:
        launcher = LearningSystemLauncher()
        launcher.run()
    except KeyboardInterrupt:
        print("\n\n👋 학습 시스템을 종료합니다.")
        print("🎓 학습하느라 수고하셨습니다!")
    except Exception as e:
        print(f"\n❌ 오류가 발생했습니다: {e}")
        print("📞 문제가 지속되면 개발팀에 문의해주세요.")


if __name__ == "__main__":
    main()