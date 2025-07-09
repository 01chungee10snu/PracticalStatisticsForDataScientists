"""
통합 콘텐츠 관리 모듈
- 중복 내용 통합
- 콘텐츠 일관성 관리
- 레벨 간 연결성 제공
"""

import pandas as pd
import numpy as np
from . import data_processing, visualization


class ContentIntegrator:
    """콘텐츠 통합 및 관리 클래스"""
    
    def __init__(self):
        self.unified_dataset = None
        self.content_mapping = {
            'beginner': {
                'focus': 'qualitative_research',
                'methods': ['case_study', 'interview', 'observation'],
                'visualization': 'descriptive_stats'
            },
            'intermediate': {
                'focus': 'factor_analysis',
                'methods': ['statistical_theory', 'matrix_analysis'],
                'visualization': 'factor_plots'
            },
            'advanced': {
                'focus': 'machine_learning',
                'methods': ['classification', 'regression', 'clustering'],
                'visualization': 'advanced_analytics'
            }
        }
    
    def generate_unified_dataset(self, n_subjects=300):
        """모든 레벨에서 사용할 통합 데이터셋 생성"""
        self.unified_dataset = data_processing.generate_research_dataset(n_subjects)
        return self.unified_dataset
    
    def get_level_specific_data(self, level='beginner', analysis_focus=None):
        """레벨별 특화 데이터 반환"""
        if self.unified_dataset is None:
            self.generate_unified_dataset()
        
        if level == 'beginner':
            # 연구방법론: 기본 인구통계 + 그룹 정보
            cols = ['subject_id', 'age', 'gender', 'education', 'group', 'success']
            if analysis_focus == 'demographics':
                cols.extend(['performance_score'])
            return self.unified_dataset[cols]
        
        elif level == 'intermediate':
            # 요인분석: 심리측정 문항들
            psychometric_cols = [col for col in self.unified_dataset.columns if col.startswith('Q')]
            base_cols = ['subject_id']
            return self.unified_dataset[base_cols + psychometric_cols]
        
        elif level == 'advanced':
            # 머신러닝: 전체 데이터
            return self.unified_dataset
        
        else:
            return self.unified_dataset
    
    def create_bridge_content(self, from_level, to_level):
        """레벨 간 연결 콘텐츠 생성"""
        bridges = {
            ('beginner', 'intermediate'): self._create_qualitative_to_quantitative_bridge,
            ('intermediate', 'advanced'): self._create_statistical_to_ml_bridge,
            ('beginner', 'advanced'): self._create_research_to_analytics_bridge
        }
        
        bridge_func = bridges.get((from_level, to_level))
        if bridge_func:
            return bridge_func()
        else:
            return f"직접 연결: {from_level} -> {to_level}"
    
    def _create_qualitative_to_quantitative_bridge(self):
        """질적 연구 -> 양적 분석 연결"""
        return {
            'title': '질적 연구에서 양적 분석으로의 전환',
            'concepts': [
                '사례 연구에서 수집한 정성적 데이터를 정량화하는 방법',
                '인터뷰 응답을 리커트 척도로 변환하는 과정',
                '관찰 데이터를 수치화하는 기법',
                '코딩된 질적 데이터를 통계 분석에 활용하는 방안'
            ],
            'example_code': """
# 질적 데이터를 양적 데이터로 변환
interview_responses = ['매우 동의', '동의', '보통', '비동의', '매우 비동의']
likert_scale = {'매우 동의': 5, '동의': 4, '보통': 3, '비동의': 2, '매우 비동의': 1}
quantified_data = [likert_scale[response] for response in interview_responses]
            """,
            'dataset': self.get_level_specific_data('beginner', 'demographics')
        }
    
    def _create_statistical_to_ml_bridge(self):
        """통계적 분석 -> 머신러닝 연결"""
        return {
            'title': '전통적 통계 분석에서 머신러닝으로의 확장',
            'concepts': [
                '요인분석 결과를 머신러닝 특성으로 활용하는 방법',
                '통계적 가정 검정에서 데이터 기반 검증으로의 전환',
                '전통적 회귀분석과 머신러닝 회귀의 차이점',
                '교차검증을 통한 모델 성능 평가'
            ],
            'example_code': """
# 요인분석 결과를 머신러닝에 활용
from sklearn.decomposition import FactorAnalysis
from sklearn.ensemble import RandomForestClassifier

# 요인분석으로 차원 축소
fa = FactorAnalysis(n_components=4)
factor_scores = fa.fit_transform(scaled_data)

# 머신러닝 모델 학습
model = RandomForestClassifier()
model.fit(factor_scores, target_variable)
            """,
            'dataset': self.get_level_specific_data('intermediate')
        }
    
    def _create_research_to_analytics_bridge(self):
        """연구방법론 -> 데이터 분석 연결"""
        return {
            'title': '연구 설계에서 데이터 분석까지의 전 과정',
            'concepts': [
                '연구 질문을 분석 가능한 형태로 변환하는 방법',
                '연구 설계에서 데이터 수집 전략 수립',
                '윤리적 고려사항을 포함한 데이터 분석 프로세스',
                '연구 결과를 실무에 적용하는 방안'
            ],
            'example_code': """
# 연구 질문을 데이터 분석으로 변환
research_question = "교육 프로그램이 학습 성과에 미치는 영향"
# -> 실험군/대조군 비교 분석
# -> 성과 지표 정의 및 측정
# -> 통계적 검정 수행
            """,
            'dataset': self.get_level_specific_data('advanced')
        }
    
    def consolidate_duplicate_content(self):
        """중복 콘텐츠 통합"""
        duplicates = {
            'statistical_concepts': {
                'beginner': ['기술통계', '빈도분석', '교차분석'],
                'intermediate': ['상관분석', '분산분석'],
                'advanced': ['회귀분석', '분류분석', '군집분석']
            },
            'visualization_methods': {
                'beginner': ['히스토그램', '막대그래프', '파이차트'],
                'intermediate': ['산점도', '히트맵', '인수분해도'],
                'advanced': ['ROC곡선', '학습곡선', '특성중요도']
            },
            'data_validation': {
                'beginner': ['데이터 정확성 확인', '이상치 탐지'],
                'intermediate': ['신뢰도 분석', '타당도 검증'],
                'advanced': ['교차검증', '모델 성능 평가']
            }
        }
        
        # 중복 제거 및 통합 콘텐츠 생성
        integrated_content = {}
        for category, levels in duplicates.items():
            integrated_content[category] = {
                'progression': self._create_progressive_content(levels),
                'unified_examples': self._create_unified_examples(category)
            }
        
        return integrated_content
    
    def _create_progressive_content(self, level_content):
        """단계별 진행 콘텐츠 생성"""
        progression = []
        for level, concepts in level_content.items():
            progression.append({
                'level': level,
                'concepts': concepts,
                'prerequisite': self._get_prerequisites(level),
                'next_step': self._get_next_steps(level)
            })
        return progression
    
    def _get_prerequisites(self, level):
        """레벨별 선수 학습 내용"""
        prerequisites = {
            'beginner': ['기본 수학', '연구윤리'],
            'intermediate': ['기본 통계', '선형대수'],
            'advanced': ['중급 통계', '프로그래밍 기초']
        }
        return prerequisites.get(level, [])
    
    def _get_next_steps(self, level):
        """레벨별 다음 단계 학습 내용"""
        next_steps = {
            'beginner': ['기본 통계 개념', '데이터 수집 방법'],
            'intermediate': ['고급 통계 기법', '머신러닝 기초'],
            'advanced': ['딥러닝', '빅데이터 분석']
        }
        return next_steps.get(level, [])
    
    def _create_unified_examples(self, category):
        """통합 예시 생성"""
        examples = {
            'statistical_concepts': {
                'scenario': '학습자 성취도 분석',
                'data_description': '학습자 200명의 사전/사후 성취도 데이터',
                'analysis_progression': [
                    '기술통계로 전반적 경향 파악',
                    '상관분석으로 변수 간 관계 탐색',
                    '머신러닝으로 성취도 예측 모델 구축'
                ]
            },
            'visualization_methods': {
                'scenario': '설문조사 결과 시각화',
                'data_description': '다섯 개 영역별 만족도 점수',
                'analysis_progression': [
                    '막대그래프로 영역별 평균 비교',
                    '히트맵으로 영역 간 상관관계 표시',
                    '인터랙티브 대시보드로 종합 분석'
                ]
            },
            'data_validation': {
                'scenario': '실험 데이터 품질 검증',
                'data_description': '실험군/대조군 비교 실험 데이터',
                'analysis_progression': [
                    '데이터 정확성 및 완전성 확인',
                    '측정도구 신뢰도 검증',
                    '모델 성능 교차검증'
                ]
            }
        }
        return examples.get(category, {})
    
    def create_comprehensive_example(self):
        """전체 레벨을 아우르는 종합 예시 생성"""
        if self.unified_dataset is None:
            self.generate_unified_dataset()
        
        comprehensive_example = {
            'title': '온라인 교육 효과성 연구: 질적 연구에서 머신러닝까지',
            'scenario': '새로운 온라인 교육 프로그램의 효과를 다각도로 분석',
            'research_progression': {
                'beginner_stage': {
                    'method': '사례 연구 및 인터뷰',
                    'data': self.get_level_specific_data('beginner'),
                    'analysis': '참여자 특성 분석 및 질적 피드백 수집',
                    'visualization': visualization.plot_research_methodology
                },
                'intermediate_stage': {
                    'method': '심리측정 및 요인분석',
                    'data': self.get_level_specific_data('intermediate'),
                    'analysis': '학습동기, 만족도, 성취도 요인 구조 분석',
                    'visualization': visualization.plot_factor_analysis
                },
                'advanced_stage': {
                    'method': '예측 모델링 및 분류',
                    'data': self.get_level_specific_data('advanced'),
                    'analysis': '성공 예측 모델 개발 및 개인화 추천',
                    'visualization': visualization.plot_advanced_analytics
                }
            },
            'integration_points': [
                '질적 인터뷰 내용을 정량화하여 요인분석에 활용',
                '요인분석 결과를 머신러닝 특성으로 활용',
                '전체 분석 결과를 종합하여 교육 개선 방안 도출'
            ]
        }
        
        return comprehensive_example
    
    def generate_content_roadmap(self):
        """학습 로드맵 생성"""
        roadmap = {
            'learning_path': [
                {
                    'stage': 1,
                    'level': 'beginner',
                    'title': '연구 방법론 기초',
                    'duration': '4주',
                    'objectives': [
                        '과학적 연구 방법 이해',
                        '사례 연구 설계 능력 습득',
                        '기본적인 데이터 수집 기법 학습'
                    ],
                    'deliverables': ['연구 계획서 작성', '인터뷰 가이드 개발']
                },
                {
                    'stage': 2,
                    'level': 'intermediate',
                    'title': '통계적 분석 기법',
                    'duration': '6주',
                    'objectives': [
                        '요인분석 이론 이해',
                        '측정도구 개발 및 검증',
                        '다변량 분석 기법 습득'
                    ],
                    'deliverables': ['측정도구 개발', '요인분석 보고서']
                },
                {
                    'stage': 3,
                    'level': 'advanced',
                    'title': '머신러닝 응용',
                    'duration': '8주',
                    'objectives': [
                        '예측 모델 개발',
                        '분류 및 군집 분석',
                        '모델 성능 평가 및 최적화'
                    ],
                    'deliverables': ['예측 모델 개발', '분석 대시보드 구축']
                }
            ],
            'skill_matrix': self._create_skill_matrix(),
            'assessment_criteria': self._create_assessment_criteria()
        }
        
        return roadmap
    
    def _create_skill_matrix(self):
        """기술 역량 매트릭스 생성"""
        skills = {
            'research_design': {
                'beginner': ['문헌 조사', '연구 질문 설정', '윤리 승인'],
                'intermediate': ['실험 설계', '표본 설계', '측정도구 개발'],
                'advanced': ['A/B 테스트', '준실험 설계', '인과추론']
            },
            'data_analysis': {
                'beginner': ['기술통계', '빈도분석', '교차분석'],
                'intermediate': ['상관분석', '요인분석', '분산분석'],
                'advanced': ['회귀분석', '분류분석', '군집분석']
            },
            'programming': {
                'beginner': ['엑셀 활용', '기본 통계 소프트웨어'],
                'intermediate': ['R 기초', 'Python 기초'],
                'advanced': ['고급 R/Python', '머신러닝 라이브러리']
            },
            'visualization': {
                'beginner': ['기본 차트', '표 작성'],
                'intermediate': ['통계 그래프', '히트맵'],
                'advanced': ['대시보드', '인터랙티브 시각화']
            }
        }
        return skills
    
    def _create_assessment_criteria(self):
        """평가 기준 생성"""
        criteria = {
            'beginner': {
                'knowledge': ['연구 방법론 이해도', '윤리적 고려사항'],
                'skills': ['인터뷰 수행 능력', '데이터 수집 기법'],
                'deliverables': ['연구 계획서', '데이터 수집 보고서']
            },
            'intermediate': {
                'knowledge': ['통계적 개념 이해', '측정 이론'],
                'skills': ['요인분석 수행', '신뢰도 분석'],
                'deliverables': ['분석 보고서', '측정도구 개발']
            },
            'advanced': {
                'knowledge': ['머신러닝 알고리즘', '모델 평가 방법'],
                'skills': ['예측 모델 개발', '성능 최적화'],
                'deliverables': ['예측 모델', '분석 대시보드']
            }
        }
        return criteria


# 글로벌 인스턴스 생성
content_integrator = ContentIntegrator()