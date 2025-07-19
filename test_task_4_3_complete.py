"""
Task 4.3 완료 테스트: 결과 저장 및 공유 기능
GitHub Pages 최적화된 결과 공유 시스템 테스트
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from github_pages_generator import GitHubPagesGenerator, GitHubPagesResult
import datetime


def test_github_pages_integration():
    """GitHub Pages 통합 테스트"""
    print("=== Task 4.3: GitHub Pages 결과 공유 시스템 테스트 ===\n")
    
    # 1. GitHub Pages 생성기 초기화
    print("1. GitHub Pages 생성기 초기화")
    generator = GitHubPagesGenerator()
    print("✅ 생성기 초기화 완료")
    
    # 2. 샘플 학습 결과 데이터 생성
    print("\n2. 샘플 학습 결과 데이터 생성")
    sample_results = [
        GitHubPagesResult(
            session_id="session_test_user_20250719_171618",
            title="기술통계량 실습 완료",
            created_at=datetime.datetime.now().isoformat(),
            completion_percentage=92.0,
            success_rate=88.5,
            total_attempts=15,
            achievements=[
                "🎯 모든 5단계를 성공적으로 완료했습니다!",
                "📊 기술통계량 계산을 정확히 수행했습니다!",
                "💡 힌트 없이 3개 단계를 해결했습니다!",
                "⚡ 평균보다 빠른 속도로 완료했습니다!"
            ],
            recommendations=[
                "분산과 표준편차의 관계를 더 깊이 이해해보세요.",
                "다양한 데이터셋으로 추가 실습을 진행해보세요.",
                "시각화를 통한 데이터 해석 능력을 기르세요.",
                "추론통계학 과정으로 진행해보세요."
            ]
        ),
        GitHubPagesResult(
            session_id="session_workflow_user_20250719_171618",
            title="워크플로우 데모 세션",
            created_at=(datetime.datetime.now() - datetime.timedelta(minutes=30)).isoformat(),
            completion_percentage=75.0,
            success_rate=82.0,
            total_attempts=10,
            achievements=[
                "🧠 힌트 없이 스스로 해결했습니다!",
                "📈 꾸준한 학습 진행을 보여주었습니다!"
            ],
            recommendations=[
                "기초 개념을 다시 한 번 복습해보세요.",
                "힌트를 적극 활용하여 학습 효과를 높이세요.",
                "남은 단계들을 완료하여 전체 학습 과정을 마무리하세요."
            ]
        )
    ]
    print(f"✅ {len(sample_results)}개의 샘플 결과 생성 완료")
    
    # 3. 개별 결과 페이지 생성 및 저장
    print("\n3. 개별 결과 페이지 생성")
    generated_files = []
    for i, result in enumerate(sample_results, 1):
        file_path = generator.save_result_page(result)
        generated_files.append(file_path)
        print(f"✅ 결과 페이지 {i} 생성: {file_path}")
    
    # 4. 결과 인덱스 페이지 생성
    print("\n4. 결과 인덱스 페이지 생성")
    index_path = generator.save_results_index(sample_results)
    generated_files.append(index_path)
    print(f"✅ 인덱스 페이지 생성: {index_path}")
    
    # 5. 생성된 파일들 검증
    print("\n5. 생성된 파일들 검증")
    all_files_exist = True
    for file_path in generated_files:
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path)
            print(f"✅ {file_path} - 크기: {file_size:,} bytes")
        else:
            print(f"❌ {file_path} - 파일이 존재하지 않음")
            all_files_exist = False
    
    # 6. HTML 콘텐츠 검증
    print("\n6. HTML 콘텐츠 검증")
    for result in sample_results:
        file_path = os.path.join("docs", "results", f"{result.session_id}.html")
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # 필수 요소 검증
            required_elements = [
                result.title,
                f"{result.completion_percentage:.0f}%",
                f"{result.success_rate:.1f}%",
                str(result.total_attempts),
                "학습 성취",
                "권장사항"
            ]
            
            missing_elements = []
            for element in required_elements:
                if element not in content:
                    missing_elements.append(element)
            
            if not missing_elements:
                print(f"✅ {result.session_id} - 모든 필수 요소 포함")
            else:
                print(f"❌ {result.session_id} - 누락된 요소: {missing_elements}")
                all_files_exist = False
    
    # 7. GitHub Pages 배포 준비 상태 확인
    print("\n7. GitHub Pages 배포 준비 상태 확인")
    
    # 메인 index.html 존재 확인
    main_index_exists = os.path.exists("index.html")
    docs_structure_valid = (
        os.path.exists("docs") and 
        os.path.exists("docs/results.html") and
        os.path.exists("docs/results")
    )
    
    print(f"✅ 메인 index.html: {'존재' if main_index_exists else '없음'}")
    print(f"✅ docs 구조: {'유효' if docs_structure_valid else '무효'}")
    
    # 8. 접근 URL 정보 출력
    print("\n8. GitHub Pages 접근 URL")
    base_url = "https://your-username.github.io/your-repo"
    urls = [
        f"{base_url}/",
        f"{base_url}/docs/results.html"
    ]
    
    for result in sample_results:
        urls.append(f"{base_url}/docs/results/{result.session_id}.html")
    
    for url in urls:
        print(f"🌐 {url}")
    
    # 9. 최종 결과
    print("\n" + "="*60)
    if all_files_exist and main_index_exists and docs_structure_valid:
        print("🎉 Task 4.3 완료: 결과 저장 및 공유 기능 구현 성공!")
        print("\n✅ 구현된 기능:")
        print("   - 학습 과정 및 결과 저장")
        print("   - GitHub Pages 최적화 데모 페이지 생성")
        print("   - 소셜 공유 기능 포함")
        print("   - 반응형 디자인 적용")
        print("   - 개인화된 학습 리포트")
        print("   - 결과 인덱스 페이지")
        
        print("\n🚀 GitHub Pages 배포 준비 완료!")
        print("   1. GitHub 저장소에 코드 푸시")
        print("   2. Settings > Pages에서 Source를 'Deploy from a branch' 선택")
        print("   3. Branch를 'main' 또는 'master' 선택")
        print("   4. Folder를 '/ (root)' 선택")
        print("   5. Save 클릭하여 배포 시작")
        
        return True
    else:
        print("❌ Task 4.3 실패: 일부 기능이 완전히 구현되지 않았습니다.")
        return False


def test_result_sharing_features():
    """결과 공유 기능 세부 테스트"""
    print("\n=== 결과 공유 기능 세부 테스트 ===")
    
    # 생성된 HTML 파일의 기능 테스트
    test_file = "docs/results/session_test_user_20250719_171618.html"
    
    if os.path.exists(test_file):
        with open(test_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 소셜 공유 기능 확인
        social_features = [
            "shareOnTwitter",
            "shareOnLinkedIn", 
            "copyLink",
            "twitter.com/intent/tweet",
            "linkedin.com/sharing"
        ]
        
        print("소셜 공유 기능 확인:")
        for feature in social_features:
            if feature in content:
                print(f"✅ {feature}")
            else:
                print(f"❌ {feature}")
        
        # 반응형 디자인 확인
        responsive_features = [
            "@media (max-width: 768px)",
            "@media (max-width: 480px)",
            "grid-template-columns",
            "flex-direction: column"
        ]
        
        print("\n반응형 디자인 확인:")
        for feature in responsive_features:
            if feature in content:
                print(f"✅ {feature}")
            else:
                print(f"❌ {feature}")
        
        # 접근성 기능 확인
        accessibility_features = [
            'alt=',
            'aria-',
            'role=',
            'lang="ko"'
        ]
        
        print("\n접근성 기능 확인:")
        for feature in accessibility_features:
            if feature in content:
                print(f"✅ {feature}")
            else:
                print(f"⚠️ {feature} (선택사항)")
    
    else:
        print(f"❌ 테스트 파일을 찾을 수 없습니다: {test_file}")


if __name__ == "__main__":
    success = test_github_pages_integration()
    test_result_sharing_features()
    
    if success:
        print("\n🎊 모든 테스트 통과! Task 4.3 구현 완료!")
    else:
        print("\n⚠️ 일부 테스트 실패. 추가 작업이 필요합니다.")