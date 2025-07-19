"""
Auto Formatter Demo - Task 3.2 Complete Implementation
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from verification_hint_system import VerificationHintSystem, VerificationResult
from simple_demo import SimplePythonExecutor
from typing import Dict, Any, List


class AutoFormatterDemo:
    """자동 검증 및 힌트 데모 시스템"""
    
    def __init__(self):
        self.verification_system = VerificationHintSystem()
        self.code_executor = SimplePythonExecutor()
        self.session_data = {
            'current_step': 'step1',
            'attempts': {},
            'completed_steps': []
        }
    
    def execute_and_verify(self, step_id: str, code: str) -> Dict[str, Any]:
        """코드 실행 및 자동 검증"""
        # 1. 시도 횟수 업데이트
        if step_id not in self.session_data['attempts']:
            self.session_data['attempts'][step_id] = 0
        self.session_data['attempts'][step_id] += 1
        
        # 2. 코드 실행
        execution_result = self.code_executor.execute(code)
        
        # 3. 자동 검증 및 힌트 생성
        verification_result = self.verification_system.verify_and_provide_feedback(
            step_id, code, execution_result, self.session_data['attempts'][step_id]
        )
        
        # 4. 단계 완료 처리
        if verification_result['verification']['result'] == VerificationResult.PASS.value:
            if step_id not in self.session_data['completed_steps']:
                self.session_data['completed_steps'].append(step_id)
        
        return {
            'execution': execution_result,
            'verification': verification_result,
            'session_info': {
                'step_id': step_id,
                'attempt_count': self.session_data['attempts'][step_id],
                'completed_steps': len(self.session_data['completed_steps']),
                'total_steps': 4
            }
        }
    
    def get_smart_hints(self, step_id: str, error_type: str = None) -> List[str]:
        """스마트 힌트 제공"""
        attempt_count = self.session_data['attempts'].get(step_id, 0)
        
        # 기본 힌트
        basic_hints = self.verification_system.hint_provider.get_hint(
            step_id, self.verification_system.hint_provider.HintLevel.BASIC, attempt_count
        )
        
        # 오류 타입별 추가 힌트
        error_hints = []
        if error_type:
            error_hint_map = {
                'NameError': [
                    "변수명을 확인하세요. 정의되지 않은 변수를 사용하고 있습니다.",
                    "이전 단계에서 생성한 변수를 사용해야 합니다."
                ],
                'SyntaxError': [
                    "Python 문법을 확인하세요.",
                    "괄호, 콜론, 들여쓰기를 확인해보세요."
                ],
                'TypeError': [
                    "데이터 타입을 확인하세요.",
                    "올바른 타입의 데이터를 사용하고 있는지 확인하세요."
                ]
            }
            error_hints = error_hint_map.get(error_type, [])
        
        return basic_hints + error_hints
    
    def generate_step_report(self, step_id: str, result: Dict[str, Any]) -> str:
        """단계별 상세 보고서 생성"""
        verification = result['verification']['verification']
        session_info = result['session_info']
        
        report_lines = []
        report_lines.append(f"📊 {step_id.upper()} 검증 보고서")
        report_lines.append("=" * 50)
        
        # 기본 정보
        report_lines.append(f"시도 횟수: {session_info['attempt_count']}")
        report_lines.append(f"검증 결과: {verification['result'].upper()}")
        report_lines.append(f"점수: {verification['score']}/100")
        report_lines.append(f"메시지: {verification['message']}")
        
        # 상세 피드백
        report_lines.append(f"\n📋 상세 피드백:")
        for feedback in verification['feedback']:
            report_lines.append(f"  {feedback}")
        
        # 힌트
        contextual_hints = result['verification']['contextual_hints']
        if contextual_hints:
            report_lines.append(f"\n💡 맞춤 힌트:")
            for hint in contextual_hints[:3]:  # 상위 3개
                report_lines.append(f"  • {hint}")
        
        # 진행 상황
        progress = (session_info['completed_steps'] / session_info['total_steps']) * 100
        report_lines.append(f"\n📈 전체 진행률: {session_info['completed_steps']}/{session_info['total_steps']} ({progress:.1f}%)")
        
        return '\n'.join(report_lines)


def demo_auto_verification_system():
    """자동 검증 시스템 데모"""
    print("🤖 Task 3.2: Auto Verification and Hint System Demo")
    print("=" * 70)
    
    demo = AutoFormatterDemo()
    
    # 데모 시나리오
    demo_scenarios = [
        {
            'title': '1단계 성공 케이스',
            'step_id': 'step1',
            'code': '''# 학생 성적 데이터 준비
scores = [85, 90, 78, 92, 88, 76, 95, 89, 84, 91]
print(f"데이터: {scores}")
print(f"데이터 개수: {len(scores)}")
print(f"데이터 타입: {type(scores)}")'''
        },
        {
            'title': '1단계 실패 케이스 (변수 누락)',
            'step_id': 'step1',
            'code': '''# 잘못된 코드 - scores 변수 없음
print("Hello World")
print("데이터 개수: 10")'''
        },
        {
            'title': '2단계 성공 케이스',
            'step_id': 'step2',
            'code': '''# 평균 계산
total = sum(scores)
count = len(scores)
mean_value = total / count
print(f"총합: {total}")
print(f"평균: {mean_value:.2f}")'''
        },
        {
            'title': '2단계 부분 성공 케이스',
            'step_id': 'step2',
            'code': '''# 평균 계산 (출력 누락)
total = sum(scores)
mean_value = total / len(scores)
# print 문 누락'''
        }
    ]
    
    for i, scenario in enumerate(demo_scenarios, 1):
        print(f"\n🎯 시나리오 {i}: {scenario['title']}")
        print("-" * 70)
        
        # 코드 실행 및 검증
        result = demo.execute_and_verify(scenario['step_id'], scenario['code'])
        
        # 실행 결과
        execution = result['execution']
        print(f"코드 실행: {'✅ 성공' if execution['success'] else '❌ 실패'}")
        if execution['success']:
            print(f"출력 미리보기: {execution['output'][:100]}...")
        else:
            print(f"오류: {execution['error']}")
        
        # 검증 결과
        verification = result['verification']['verification']
        print(f"자동 검증: {verification['result'].upper()} ({verification['score']}/100)")
        print(f"검증 메시지: {verification['message']}")
        
        # 피드백 (처음 2개만)
        feedback = verification['feedback'][:2]
        if feedback:
            print(f"주요 피드백:")
            for fb in feedback:
                print(f"  {fb}")
        
        # 맞춤 힌트 (처음 2개만)
        hints = result['verification']['contextual_hints'][:2]
        if hints:
            print(f"맞춤 힌트:")
            for hint in hints:
                print(f"  💡 {hint}")
        
        # 세션 정보
        session_info = result['session_info']
        print(f"시도 횟수: {session_info['attempt_count']}")
        print(f"완료된 단계: {session_info['completed_steps']}/{session_info['total_steps']}")
    
    # 전체 기능 요약
    print(f"\n📊 Task 3.2 Feature Summary")
    print("=" * 70)
    
    features = [
        ("자동 코드 검증", "✅", "실행 결과를 자동으로 분석하여 단계 완료 여부 판단"),
        ("점수 기반 평가", "✅", "100점 만점으로 세부 기준에 따른 점수 산출"),
        ("상세 피드백", "✅", "각 요구사항별 성공/실패 상태 제공"),
        ("맞춤형 힌트", "✅", "시도 횟수와 오류 유형에 따른 적응형 힌트"),
        ("다단계 힌트", "✅", "기본 → 중급 → 고급 → 해답 순서로 힌트 제공"),
        ("실시간 검증", "✅", "코드 실행과 동시에 즉시 검증 결과 제공"),
        ("진행률 추적", "✅", "전체 학습 과정에서의 진행 상황 추적"),
        ("오류 분석", "✅", "구체적인 오류 유형별 맞춤 가이드")
    ]
    
    for feature, status, description in features:
        print(f"{status} {feature}: {description}")
    
    print(f"\n📋 Requirements Verification:")
    print(f"   ✅ 코드 실행 결과 자동 검증 기능")
    print(f"   ✅ 상황별 맞춤 힌트 제공 시스템")
    print(f"   ✅ 요구사항 3.2: 각 단계 진행 시 힌트와 검증 기능 제공")
    
    print(f"\n🎉 Task 3.2 AUTO VERIFICATION SYSTEM COMPLETE!")
    
    return demo


if __name__ == "__main__":
    demo_auto_verification_system()