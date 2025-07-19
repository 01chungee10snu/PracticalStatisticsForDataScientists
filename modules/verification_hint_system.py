"""
Verification and Hint System - Task 3.2 Implementation
"""

import re
import ast
from typing import Dict, Any, List, Optional, Tuple
from enum import Enum


class VerificationResult(Enum):
    """검증 결과"""
    PASS = "pass"
    FAIL = "fail"
    PARTIAL = "partial"
    ERROR = "error"


class HintLevel(Enum):
    """힌트 수준"""
    BASIC = "basic"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    SOLUTION = "solution"


class CodeVerifier:
    """코드 검증기"""
    
    def __init__(self):
        self.verification_rules = {
            'step1': self._verify_step1_data_preparation,
            'step2': self._verify_step2_central_tendency,
            'step3': self._verify_step3_dispersion,
            'step4': self._verify_step4_interpretation
        }
    
    def verify_step_completion(self, step_id: str, code: str, 
                             execution_result: Dict[str, Any]) -> Dict[str, Any]:
        """단계 완료 검증"""
        if step_id not in self.verification_rules:
            return {
                'result': VerificationResult.ERROR.value,
                'message': f'Unknown step: {step_id}',
                'score': 0,
                'feedback': []
            }
        
        return self.verification_rules[step_id](code, execution_result)
    
    def _verify_step1_data_preparation(self, code: str, result: Dict[str, Any]) -> Dict[str, Any]:
        """1단계: 데이터 준비 검증"""
        feedback = []
        score = 0
        
        # 1. 실행 성공 여부 (30점)
        if not result.get('success', False):
            return {
                'result': VerificationResult.FAIL.value,
                'message': '코드 실행에 실패했습니다.',
                'score': 0,
                'feedback': ['코드 문법을 확인하고 다시 시도하세요.']
            }
        
        score += 30
        
        # 2. 변수 생성 확인 (30점)
        variables = result.get('variables', {})
        if 'scores' in variables:
            score += 30
            feedback.append('✓ scores 변수가 올바르게 생성되었습니다.')
        else:
            feedback.append('✗ scores 변수를 생성해야 합니다.')
        
        # 3. 데이터 출력 확인 (20점)
        output = result.get('output', '')
        if '데이터:' in output or 'scores' in output:
            score += 20
            feedback.append('✓ 데이터가 올바르게 출력되었습니다.')
        else:
            feedback.append('✗ 데이터를 출력해야 합니다.')
        
        # 4. 데이터 개수 출력 확인 (20점)
        if '개수:' in output or 'len(' in code.lower():
            score += 20
            feedback.append('✓ 데이터 개수가 출력되었습니다.')
        else:
            feedback.append('✗ 데이터 개수를 출력해야 합니다.')
        
        # 결과 판정
        if score >= 80:
            result_status = VerificationResult.PASS.value
            message = '1단계를 성공적으로 완료했습니다!'
        elif score >= 50:
            result_status = VerificationResult.PARTIAL.value
            message = '1단계를 부분적으로 완료했습니다. 몇 가지 개선이 필요합니다.'
        else:
            result_status = VerificationResult.FAIL.value
            message = '1단계 요구사항을 충족하지 못했습니다.'
        
        return {
            'result': result_status,
            'message': message,
            'score': score,
            'feedback': feedback
        }    

    def _verify_step2_central_tendency(self, code: str, result: Dict[str, Any]) -> Dict[str, Any]:
        """2단계: 중심경향성 계산 검증"""
        feedback = []
        score = 0
        
        if not result.get('success', False):
            return {
                'result': VerificationResult.FAIL.value,
                'message': '코드 실행에 실패했습니다.',
                'score': 0,
                'feedback': ['코드 문법을 확인하고 다시 시도하세요.']
            }
        
        score += 20
        
        # 변수 확인
        variables = result.get('variables', {})
        output = result.get('output', '')
        
        # 평균 계산 확인 (40점)
        if any(var in variables for var in ['mean_value', 'mean', 'average']):
            score += 40
            feedback.append('✓ 평균값이 올바르게 계산되었습니다.')
        elif 'sum(' in code and '/' in code:
            score += 20
            feedback.append('△ 평균 계산 로직은 있지만 변수에 저장되지 않았습니다.')
        else:
            feedback.append('✗ 평균을 계산해야 합니다.')
        
        # 출력 확인 (40점)
        if '평균:' in output or 'mean' in output.lower():
            score += 40
            feedback.append('✓ 평균값이 올바르게 출력되었습니다.')
        else:
            feedback.append('✗ 평균값을 출력해야 합니다.')
        
        # 결과 판정
        if score >= 80:
            result_status = VerificationResult.PASS.value
            message = '2단계를 성공적으로 완료했습니다!'
        elif score >= 50:
            result_status = VerificationResult.PARTIAL.value
            message = '2단계를 부분적으로 완료했습니다.'
        else:
            result_status = VerificationResult.FAIL.value
            message = '2단계 요구사항을 충족하지 못했습니다.'
        
        return {
            'result': result_status,
            'message': message,
            'score': score,
            'feedback': feedback
        }
    
    def _verify_step3_dispersion(self, code: str, result: Dict[str, Any]) -> Dict[str, Any]:
        """3단계: 산포도 계산 검증"""
        feedback = []
        score = 0
        
        if not result.get('success', False):
            return {
                'result': VerificationResult.FAIL.value,
                'message': '코드 실행에 실패했습니다.',
                'score': 0,
                'feedback': ['코드 문법을 확인하고 다시 시도하세요.']
            }
        
        score += 20
        
        variables = result.get('variables', {})
        output = result.get('output', '')
        
        # 분산 계산 확인 (30점)
        if 'variance' in variables:
            score += 30
            feedback.append('✓ 분산이 올바르게 계산되었습니다.')
        else:
            feedback.append('✗ 분산을 계산해야 합니다.')
        
        # 표준편차 계산 확인 (30점)
        if any(var in variables for var in ['std_dev', 'std', 'standard_deviation']):
            score += 30
            feedback.append('✓ 표준편차가 올바르게 계산되었습니다.')
        else:
            feedback.append('✗ 표준편차를 계산해야 합니다.')
        
        # 출력 확인 (20점)
        if '표준편차:' in output or 'std' in output.lower():
            score += 20
            feedback.append('✓ 표준편차가 올바르게 출력되었습니다.')
        else:
            feedback.append('✗ 표준편차를 출력해야 합니다.')
        
        # 결과 판정
        if score >= 80:
            result_status = VerificationResult.PASS.value
            message = '3단계를 성공적으로 완료했습니다!'
        elif score >= 50:
            result_status = VerificationResult.PARTIAL.value
            message = '3단계를 부분적으로 완료했습니다.'
        else:
            result_status = VerificationResult.FAIL.value
            message = '3단계 요구사항을 충족하지 못했습니다.'
        
        return {
            'result': result_status,
            'message': message,
            'score': score,
            'feedback': feedback
        }
    
    def _verify_step4_interpretation(self, code: str, result: Dict[str, Any]) -> Dict[str, Any]:
        """4단계: 결과 해석 검증"""
        feedback = []
        score = 0
        
        if not result.get('success', False):
            return {
                'result': VerificationResult.FAIL.value,
                'message': '코드 실행에 실패했습니다.',
                'score': 0,
                'feedback': ['코드 문법을 확인하고 다시 시도하세요.']
            }
        
        score += 20
        
        output = result.get('output', '')
        
        # 요약 출력 확인 (30점)
        if '요약' in output or '분석' in output:
            score += 30
            feedback.append('✓ 결과 요약이 포함되었습니다.')
        else:
            feedback.append('✗ 결과 요약을 포함해야 합니다.')
        
        # 통계량 출력 확인 (30점)
        stats_count = sum(1 for term in ['평균', '표준편차', '분산', '최솟값', '최댓값'] if term in output)
        if stats_count >= 3:
            score += 30
            feedback.append('✓ 주요 통계량들이 출력되었습니다.')
        elif stats_count >= 1:
            score += 15
            feedback.append('△ 일부 통계량이 출력되었습니다.')
        else:
            feedback.append('✗ 주요 통계량들을 출력해야 합니다.')
        
        # 해석 포함 확인 (20점)
        if '해석' in output or '의미' in output or '분석' in output:
            score += 20
            feedback.append('✓ 결과 해석이 포함되었습니다.')
        else:
            feedback.append('✗ 결과에 대한 해석을 포함해야 합니다.')
        
        # 결과 판정
        if score >= 80:
            result_status = VerificationResult.PASS.value
            message = '4단계를 성공적으로 완료했습니다!'
        elif score >= 50:
            result_status = VerificationResult.PARTIAL.value
            message = '4단계를 부분적으로 완료했습니다.'
        else:
            result_status = VerificationResult.FAIL.value
            message = '4단계 요구사항을 충족하지 못했습니다.'
        
        return {
            'result': result_status,
            'message': message,
            'score': score,
            'feedback': feedback
        }


class HintProvider:
    """힌트 제공 시스템"""
    
    def __init__(self):
        self.hint_database = {
            'step1': {
                HintLevel.BASIC: [
                    "리스트를 사용하여 데이터를 저장하세요.",
                    "print() 함수로 결과를 출력하세요.",
                    "len() 함수로 데이터 개수를 확인할 수 있습니다."
                ],
                HintLevel.INTERMEDIATE: [
                    "scores = [85, 90, 78, ...] 형태로 리스트를 만드세요.",
                    "f-string을 사용하여 깔끔하게 출력하세요: print(f'데이터: {scores}')",
                    "type() 함수로 데이터 타입도 확인해보세요."
                ],
                HintLevel.ADVANCED: [
                    "데이터의 기본 정보를 모두 출력하세요: 데이터 내용, 개수, 타입",
                    "출력 형식을 일관되게 맞춰보세요.",
                    "다음 단계에서 사용할 변수명을 명확하게 정하세요."
                ],
                HintLevel.SOLUTION: [
                    "scores = [85, 90, 78, 92, 88, 76, 95, 89, 84, 91]",
                    "print(f'데이터: {scores}')",
                    "print(f'데이터 개수: {len(scores)}')"
                ]
            },
            'step2': {
                HintLevel.BASIC: [
                    "sum() 함수로 총합을 구하세요.",
                    "평균 = 총합 / 개수 입니다.",
                    "소수점 둘째 자리까지 출력하세요."
                ],
                HintLevel.INTERMEDIATE: [
                    "total = sum(scores)로 총합을 구하세요.",
                    "mean_value = total / len(scores)로 평균을 계산하세요.",
                    ":.2f 형식으로 소수점을 제한할 수 있습니다."
                ],
                HintLevel.ADVANCED: [
                    "중간 계산 과정도 출력해보세요 (총합, 개수).",
                    "변수명을 명확하게 정하여 다음 단계에서 사용하세요.",
                    "계산 결과가 합리적인지 확인해보세요."
                ],
                HintLevel.SOLUTION: [
                    "total = sum(scores)",
                    "mean_value = total / len(scores)",
                    "print(f'평균: {mean_value:.2f}')"
                ]
            },
            'step3': {
                HintLevel.BASIC: [
                    "분산은 편차 제곱의 평균입니다.",
                    "표준편차는 분산의 제곱근입니다.",
                    "** 0.5 또는 math.sqrt()를 사용하세요."
                ],
                HintLevel.INTERMEDIATE: [
                    "variance = sum((x - mean_value) ** 2 for x in scores) / len(scores)",
                    "std_dev = variance ** 0.5",
                    "범위 = max(scores) - min(scores)도 계산해보세요."
                ],
                HintLevel.ADVANCED: [
                    "편차를 먼저 계산한 후 제곱하여 평균을 구하세요.",
                    "표준편차의 의미를 생각해보세요 (데이터의 퍼짐 정도).",
                    "계산 결과를 검증해보세요."
                ],
                HintLevel.SOLUTION: [
                    "variance = sum((x - mean_value) ** 2 for x in scores) / len(scores)",
                    "std_dev = variance ** 0.5",
                    "print(f'표준편차: {std_dev:.2f}')"
                ]
            },
            'step4': {
                HintLevel.BASIC: [
                    "모든 통계량을 정리하여 출력하세요.",
                    "결과에 대한 해석을 추가하세요.",
                    "보고서 형태로 구성해보세요."
                ],
                HintLevel.INTERMEDIATE: [
                    "'=== 기술통계량 요약 ===' 형태로 제목을 만드세요.",
                    "평균, 표준편차, 최솟값, 최댓값을 모두 포함하세요.",
                    "해석 섹션을 별도로 만드세요."
                ],
                HintLevel.ADVANCED: [
                    "통계량의 실제 의미를 설명하세요.",
                    "데이터의 특성을 분석하여 결론을 내리세요.",
                    "학급 성적의 맥락에서 해석해보세요."
                ],
                HintLevel.SOLUTION: [
                    "print('=== 기술통계량 요약 ===')",
                    "print(f'평균: {mean_value:.2f}')",
                    "print('=== 해석 ===')",
                    "print('이 학급의 평균 점수는 양호한 수준입니다.')"
                ]
            }
        }
    
    def get_hint(self, step_id: str, hint_level: HintLevel, 
                 attempt_count: int = 1) -> List[str]:
        """힌트 제공"""
        if step_id not in self.hint_database:
            return ["이 단계에 대한 힌트가 없습니다."]
        
        step_hints = self.hint_database[step_id]
        
        # 시도 횟수에 따른 힌트 수준 자동 조정
        if attempt_count <= 2:
            level = HintLevel.BASIC
        elif attempt_count <= 4:
            level = HintLevel.INTERMEDIATE
        elif attempt_count <= 6:
            level = HintLevel.ADVANCED
        else:
            level = HintLevel.SOLUTION
        
        # 사용자가 지정한 수준이 있으면 우선 사용
        if hint_level != HintLevel.BASIC:
            level = hint_level
        
        return step_hints.get(level, step_hints[HintLevel.BASIC])
    
    def get_contextual_hint(self, step_id: str, verification_result: Dict[str, Any]) -> List[str]:
        """상황별 맞춤 힌트"""
        contextual_hints = []
        
        if verification_result['result'] == VerificationResult.FAIL.value:
            if verification_result['score'] < 30:
                contextual_hints.extend([
                    "코드 실행에 문제가 있습니다. 문법을 확인해보세요.",
                    "기본적인 Python 문법을 다시 확인해보세요."
                ])
            else:
                contextual_hints.extend([
                    "일부 요구사항이 누락되었습니다.",
                    "피드백을 참고하여 부족한 부분을 보완하세요."
                ])
        
        elif verification_result['result'] == VerificationResult.PARTIAL.value:
            contextual_hints.extend([
                "좋은 시작입니다! 몇 가지만 더 추가하면 됩니다.",
                "피드백의 ✗ 항목들을 확인하여 보완하세요."
            ])
        
        # 피드백 기반 구체적 힌트
        feedback = verification_result.get('feedback', [])
        for fb in feedback:
            if '✗' in fb:
                if 'scores' in fb:
                    contextual_hints.append("scores 변수를 생성하세요: scores = [85, 90, ...]")
                elif '출력' in fb:
                    contextual_hints.append("print() 함수를 사용하여 결과를 출력하세요.")
                elif '평균' in fb:
                    contextual_hints.append("sum(scores) / len(scores)로 평균을 계산하세요.")
                elif '표준편차' in fb:
                    contextual_hints.append("분산의 제곱근이 표준편차입니다.")
        
        return contextual_hints if contextual_hints else self.get_hint(step_id, HintLevel.BASIC)


class VerificationHintSystem:
    """통합 검증 및 힌트 시스템"""
    
    def __init__(self):
        self.verifier = CodeVerifier()
        self.hint_provider = HintProvider()
    
    def verify_and_provide_feedback(self, step_id: str, code: str, 
                                  execution_result: Dict[str, Any],
                                  attempt_count: int = 1) -> Dict[str, Any]:
        """검증 및 피드백 제공"""
        # 1. 코드 검증
        verification_result = self.verifier.verify_step_completion(
            step_id, code, execution_result
        )
        
        # 2. 상황별 힌트 생성
        contextual_hints = self.hint_provider.get_contextual_hint(
            step_id, verification_result
        )
        
        # 3. 일반 힌트 생성
        general_hints = self.hint_provider.get_hint(
            step_id, HintLevel.BASIC, attempt_count
        )
        
        # 4. 통합 결과 생성
        return {
            'verification': verification_result,
            'contextual_hints': contextual_hints,
            'general_hints': general_hints,
            'step_id': step_id,
            'attempt_count': attempt_count,
            'next_hint_level': self._get_next_hint_level(attempt_count)
        }
    
    def _get_next_hint_level(self, attempt_count: int) -> str:
        """다음 힌트 수준 결정"""
        if attempt_count <= 2:
            return "기본 힌트"
        elif attempt_count <= 4:
            return "중급 힌트"
        elif attempt_count <= 6:
            return "고급 힌트"
        else:
            return "해답 힌트"


# 테스트용 함수
def test_verification_hint_system():
    """검증 및 힌트 시스템 테스트"""
    system = VerificationHintSystem()
    
    print("=== Task 3.2: Verification and Hint System Test ===")
    
    # 테스트 케이스들
    test_cases = [
        {
            'step_id': 'step1',
            'code': '''scores = [85, 90, 78, 92, 88, 76, 95, 89, 84, 91]
print(f"데이터: {scores}")
print(f"데이터 개수: {len(scores)}")''',
            'execution_result': {
                'success': True,
                'output': '데이터: [85, 90, 78, 92, 88, 76, 95, 89, 84, 91]\n데이터 개수: 10',
                'variables': {'scores': [85, 90, 78, 92, 88, 76, 95, 89, 84, 91]}
            },
            'attempt_count': 1
        },
        {
            'step_id': 'step2',
            'code': '''total = sum(scores)
mean_value = total / len(scores)
print(f"평균: {mean_value:.2f}")''',
            'execution_result': {
                'success': True,
                'output': '평균: 86.80',
                'variables': {'total': 868, 'mean_value': 86.8}
            },
            'attempt_count': 2
        },
        {
            'step_id': 'step1',
            'code': '''# 잘못된 코드
print("Hello")''',
            'execution_result': {
                'success': True,
                'output': 'Hello',
                'variables': {}
            },
            'attempt_count': 3
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n--- Test Case {i}: {test_case['step_id']} ---")
        
        result = system.verify_and_provide_feedback(
            test_case['step_id'],
            test_case['code'],
            test_case['execution_result'],
            test_case['attempt_count']
        )
        
        verification = result['verification']
        print(f"Verification Result: {verification['result']}")
        print(f"Score: {verification['score']}/100")
        print(f"Message: {verification['message']}")
        
        print(f"\nFeedback:")
        for feedback in verification['feedback']:
            print(f"  {feedback}")
        
        print(f"\nContextual Hints:")
        for hint in result['contextual_hints'][:2]:  # 처음 2개만 표시
            print(f"  💡 {hint}")
        
        print(f"Next Hint Level: {result['next_hint_level']}")


if __name__ == "__main__":
    test_verification_hint_system()