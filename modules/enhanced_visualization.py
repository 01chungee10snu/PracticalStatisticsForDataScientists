"""
향상된 시각화 엔진
- 인터랙티브 데이터 시각화
- 학습자 맞춤형 차트 생성
- 실시간 데이터 업데이트
- 접근성을 고려한 시각화
"""

import json
import math
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass
from enum import Enum
import base64
from io import BytesIO

class ChartType(Enum):
    HISTOGRAM = "histogram"
    BOXPLOT = "boxplot"
    SCATTER = "scatter"
    LINE = "line"
    BAR = "bar"
    PIE = "pie"
    HEATMAP = "heatmap"
    VIOLIN = "violin"
    DENSITY = "density"
    CORRELATION_MATRIX = "correlation_matrix"

class LearningLevel(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

@dataclass
class VisualizationConfig:
    """시각화 설정"""
    chart_type: ChartType
    title: str
    x_label: str
    y_label: str
    color_scheme: str
    show_statistics: bool
    show_annotations: bool
    interactive: bool
    accessibility_mode: bool
    learning_level: LearningLevel

@dataclass
class ChartAnnotation:
    """차트 주석"""
    x: float
    y: float
    text: str
    arrow: bool
    color: str

class EnhancedVisualizationEngine:
    def __init__(self):
        self.color_schemes = {
            'default': ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6'],
            'colorblind_friendly': ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'],
            'high_contrast': ['#000000', '#ffffff', '#ff0000', '#00ff00', '#0000ff'],
            'pastel': ['#a8e6cf', '#dcedc1', '#ffd3a5', '#fd9853', '#ff8a80']
        }
        
        self.learning_level_configs = {
            LearningLevel.BEGINNER: {
                'show_grid': True,
                'show_statistics': True,
                'annotation_detail': 'high',
                'color_coding': 'simple'
            },
            LearningLevel.INTERMEDIATE: {
                'show_grid': True,
                'show_statistics': True,
                'annotation_detail': 'medium',
                'color_coding': 'moderate'
            },
            LearningLevel.ADVANCED: {
                'show_grid': False,
                'show_statistics': False,
                'annotation_detail': 'low',
                'color_coding': 'complex'
            }
        }
        
        # matplotlib 한글 폰트 설정
        plt.rcParams['font.family'] = 'DejaVu Sans'
        plt.rcParams['axes.unicode_minus'] = False
        
    def create_adaptive_visualization(self, data: Dict[str, Any], 
                                    config: VisualizationConfig,
                                    user_profile: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """적응형 시각화 생성"""
        
        # 사용자 프로필에 따른 설정 조정
        if user_profile:
            config = self._adapt_config_to_user(config, user_profile)
        
        # 데이터 전처리
        processed_data = self._preprocess_data(data, config.chart_type)
        
        # 차트 생성
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # 차트 타입별 생성
        chart_result = self._create_chart_by_type(ax, processed_data, config)
        
        # 통계 정보 추가
        if config.show_statistics:
            self._add_statistical_annotations(ax, processed_data, config)
        
        # 학습 수준별 주석 추가
        if config.show_annotations:
            self._add_learning_annotations(ax, processed_data, config)
        
        # 접근성 개선
        if config.accessibility_mode:
            self._apply_accessibility_features(ax, config)
        
        # 차트를 base64로 인코딩
        chart_base64 = self._chart_to_base64(fig)
        plt.close(fig)
        
        # 해석 가이드 생성
        interpretation_guide = self._generate_interpretation_guide(processed_data, config)
        
        # 인터랙티브 요소 정보
        interactive_elements = self._generate_interactive_elements(processed_data, config)
        
        return {
            'chart_base64': chart_base64,
            'interpretation_guide': interpretation_guide,
            'interactive_elements': interactive_elements,
            'statistical_summary': chart_result.get('statistics', {}),
            'learning_insights': self._generate_learning_insights(processed_data, config),
            'next_steps': self._suggest_next_visualizations(processed_data, config)
        }
    
    def _adapt_config_to_user(self, config: VisualizationConfig, 
                            user_profile: Dict[str, Any]) -> VisualizationConfig:
        """사용자 프로필에 따른 설정 적응"""
        
        # 학습 수준 조정
        if 'learning_level' in user_profile:
            config.learning_level = LearningLevel(user_profile['learning_level'])
        
        # 접근성 요구사항
        if user_profile.get('accessibility_needs'):
            config.accessibility_mode = True
            config.color_scheme = 'high_contrast'
        
        # 시각적 선호도
        if user_profile.get('visual_preference') == 'minimal':
            config.show_annotations = False
            config.color_scheme = 'default'
        elif user_profile.get('visual_preference') == 'detailed':
            config.show_annotations = True
            config.show_statistics = True
        
        return config
    
    def _preprocess_data(self, data: Dict[str, Any], chart_type: ChartType) -> Dict[str, Any]:
        """데이터 전처리"""
        processed = {}
        
        if chart_type == ChartType.HISTOGRAM:
            processed['values'] = np.array(data.get('values', []))
            processed['bins'] = data.get('bins', 'auto')
            
        elif chart_type == ChartType.SCATTER:
            processed['x'] = np.array(data.get('x', []))
            processed['y'] = np.array(data.get('y', []))
            processed['labels'] = data.get('labels', [])
            
        elif chart_type == ChartType.BOXPLOT:
            processed['data'] = [np.array(group) for group in data.get('groups', [])]
            processed['labels'] = data.get('labels', [])
            
        elif chart_type == ChartType.LINE:
            processed['x'] = np.array(data.get('x', []))
            processed['y'] = np.array(data.get('y', []))
            processed['multiple_series'] = data.get('multiple_series', False)
            
        elif chart_type == ChartType.BAR:
            processed['categories'] = data.get('categories', [])
            processed['values'] = np.array(data.get('values', []))
            
        elif chart_type == ChartType.CORRELATION_MATRIX:
            processed['matrix'] = np.array(data.get('correlation_matrix', []))
            processed['labels'] = data.get('variable_names', [])
        
        return processed
    
    def _create_chart_by_type(self, ax, data: Dict[str, Any], 
                            config: VisualizationConfig) -> Dict[str, Any]:
        """차트 타입별 생성"""
        
        colors = self.color_schemes[config.color_scheme]
        result = {'statistics': {}}
        
        if config.chart_type == ChartType.HISTOGRAM:
            values = data['values']
            n, bins, patches = ax.hist(values, bins=data['bins'], 
                                     color=colors[0], alpha=0.7, edgecolor='black')
            
            # 통계 정보 계산
            result['statistics'] = {
                'mean': np.mean(values),
                'median': np.median(values),
                'std': np.std(values),
                'count': len(values)
            }
            
            # 학습 수준에 따른 추가 정보
            if config.learning_level == LearningLevel.BEGINNER:
                # 평균선 추가
                ax.axvline(result['statistics']['mean'], color='red', 
                          linestyle='--', label=f'평균: {result["statistics"]["mean"]:.2f}')
                ax.axvline(result['statistics']['median'], color='green', 
                          linestyle='--', label=f'중앙값: {result["statistics"]["median"]:.2f}')
                ax.legend()
        
        elif config.chart_type == ChartType.SCATTER:
            x, y = data['x'], data['y']
            scatter = ax.scatter(x, y, c=colors[0], alpha=0.6, s=50)
            
            # 상관계수 계산
            correlation = np.corrcoef(x, y)[0, 1]
            result['statistics']['correlation'] = correlation
            
            # 회귀선 추가 (중급 이상)
            if config.learning_level != LearningLevel.BEGINNER:
                z = np.polyfit(x, y, 1)
                p = np.poly1d(z)
                ax.plot(x, p(x), "r--", alpha=0.8, 
                       label=f'회귀선 (r={correlation:.3f})')
                ax.legend()
        
        elif config.chart_type == ChartType.BOXPLOT:
            box_plot = ax.boxplot(data['data'], labels=data['labels'], 
                                patch_artist=True)
            
            # 색상 적용
            for patch, color in zip(box_plot['boxes'], colors):
                patch.set_facecolor(color)
                patch.set_alpha(0.7)
            
            # 각 그룹의 통계 계산
            result['statistics']['group_stats'] = []
            for i, group_data in enumerate(data['data']):
                group_stats = {
                    'group': data['labels'][i] if i < len(data['labels']) else f'Group {i+1}',
                    'median': np.median(group_data),
                    'q1': np.percentile(group_data, 25),
                    'q3': np.percentile(group_data, 75),
                    'mean': np.mean(group_data)
                }
                result['statistics']['group_stats'].append(group_stats)
        
        elif config.chart_type == ChartType.LINE:
            x, y = data['x'], data['y']
            ax.plot(x, y, color=colors[0], linewidth=2, marker='o', markersize=4)
            
            # 추세 분석
            if len(x) > 1:
                slope = (y[-1] - y[0]) / (x[-1] - x[0])
                result['statistics']['trend_slope'] = slope
                result['statistics']['trend_direction'] = 'increasing' if slope > 0 else 'decreasing'
        
        elif config.chart_type == ChartType.BAR:
            categories, values = data['categories'], data['values']
            bars = ax.bar(categories, values, color=colors[:len(categories)])
            
            # 값 라벨 추가 (초급자용)
            if config.learning_level == LearningLevel.BEGINNER:
                for bar, value in zip(bars, values):
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width()/2., height + 0.01*max(values),
                           f'{value:.1f}', ha='center', va='bottom')
            
            result['statistics'] = {
                'max_category': categories[np.argmax(values)],
                'min_category': categories[np.argmin(values)],
                'total': np.sum(values)
            }
        
        elif config.chart_type == ChartType.CORRELATION_MATRIX:
            matrix = data['matrix']
            labels = data['labels']
            
            im = ax.imshow(matrix, cmap='coolwarm', aspect='auto', vmin=-1, vmax=1)
            
            # 라벨 설정
            ax.set_xticks(range(len(labels)))
            ax.set_yticks(range(len(labels)))
            ax.set_xticklabels(labels, rotation=45)
            ax.set_yticklabels(labels)
            
            # 값 표시 (중급 이상)
            if config.learning_level != LearningLevel.BEGINNER:
                for i in range(len(labels)):
                    for j in range(len(labels)):
                        text = ax.text(j, i, f'{matrix[i, j]:.2f}',
                                     ha="center", va="center", color="black")
            
            # 컬러바 추가
            plt.colorbar(im, ax=ax)
        
        # 공통 설정
        ax.set_title(config.title, fontsize=14, fontweight='bold')
        ax.set_xlabel(config.x_label, fontsize=12)
        ax.set_ylabel(config.y_label, fontsize=12)
        
        return result
    
    def _add_statistical_annotations(self, ax, data: Dict[str, Any], 
                                   config: VisualizationConfig):
        """통계 정보 주석 추가"""
        
        if config.chart_type == ChartType.HISTOGRAM:
            values = data['values']
            mean_val = np.mean(values)
            std_val = np.std(values)
            
            # 통계 정보 텍스트 박스
            stats_text = f'평균: {mean_val:.2f}\n표준편차: {std_val:.2f}\n개수: {len(values)}'
            ax.text(0.02, 0.98, stats_text, transform=ax.transAxes, 
                   verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
        elif config.chart_type == ChartType.SCATTER:
            x, y = data['x'], data['y']
            correlation = np.corrcoef(x, y)[0, 1]
            
            # 상관계수 표시
            corr_text = f'상관계수: {correlation:.3f}'
            ax.text(0.02, 0.98, corr_text, transform=ax.transAxes,
                   verticalalignment='top', bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
    
    def _add_learning_annotations(self, ax, data: Dict[str, Any], 
                                config: VisualizationConfig):
        """학습 수준별 주석 추가"""
        
        level_config = self.learning_level_configs[config.learning_level]
        
        if level_config['annotation_detail'] == 'high':
            # 초급자용 상세 설명
            if config.chart_type == ChartType.HISTOGRAM:
                ax.text(0.98, 0.02, '히스토그램: 데이터의 분포를 보여줍니다', 
                       transform=ax.transAxes, ha='right', va='bottom',
                       bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.7))
            
            elif config.chart_type == ChartType.SCATTER:
                ax.text(0.98, 0.02, '산점도: 두 변수 간의 관계를 보여줍니다', 
                       transform=ax.transAxes, ha='right', va='bottom',
                       bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.7))
        
        elif level_config['annotation_detail'] == 'medium':
            # 중급자용 핵심 포인트
            if config.chart_type == ChartType.HISTOGRAM:
                ax.text(0.98, 0.02, '분포의 형태와 중심을 확인하세요', 
                       transform=ax.transAxes, ha='right', va='bottom',
                       bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.7))
    
    def _apply_accessibility_features(self, ax, config: VisualizationConfig):
        """접근성 기능 적용"""
        
        # 고대비 색상 적용
        ax.set_facecolor('white')
        
        # 격자 추가 (스크린 리더 사용자를 위한 구조화)
        ax.grid(True, alpha=0.3)
        
        # 텍스트 크기 증가
        ax.tick_params(labelsize=12)
        
        # 선 두께 증가
        for line in ax.get_lines():
            line.set_linewidth(3)
    
    def _chart_to_base64(self, fig) -> str:
        """차트를 base64 문자열로 변환"""
        buffer = BytesIO()
        fig.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
        buffer.seek(0)
        
        image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        buffer.close()
        
        return image_base64
    
    def _generate_interpretation_guide(self, data: Dict[str, Any], 
                                     config: VisualizationConfig) -> Dict[str, Any]:
        """해석 가이드 생성"""
        
        guide = {
            'what_to_look_for': [],
            'key_insights': [],
            'common_mistakes': [],
            'next_questions': []
        }
        
        if config.chart_type == ChartType.HISTOGRAM:
            values = data['values']
            mean_val = np.mean(values)
            median_val = np.median(values)
            
            guide['what_to_look_for'] = [
                "분포의 형태 (정규분포, 치우침 등)",
                "중심경향성 (평균, 중앙값)",
                "산포도 (데이터의 퍼짐 정도)",
                "이상값의 존재"
            ]
            
            guide['key_insights'] = [
                f"평균({mean_val:.2f})과 중앙값({median_val:.2f})의 차이로 분포의 치우침을 알 수 있습니다",
                "막대의 높이는 해당 구간의 빈도를 나타냅니다"
            ]
            
            if abs(mean_val - median_val) > np.std(values) * 0.1:
                if mean_val > median_val:
                    guide['key_insights'].append("평균이 중앙값보다 크므로 우측으로 치우친 분포입니다")
                else:
                    guide['key_insights'].append("평균이 중앙값보다 작으므로 좌측으로 치우친 분포입니다")
            
            guide['common_mistakes'] = [
                "구간(bin)의 개수에 따라 분포 모양이 달라 보일 수 있습니다",
                "빈도와 확률밀도를 혼동하지 마세요"
            ]
            
            guide['next_questions'] = [
                "이 분포가 정규분포에 가까운가요?",
                "이상값이 있다면 어떻게 처리해야 할까요?",
                "다른 그룹과 비교하면 어떤 차이가 있을까요?"
            ]
        
        elif config.chart_type == ChartType.SCATTER:
            x, y = data['x'], data['y']
            correlation = np.corrcoef(x, y)[0, 1]
            
            guide['what_to_look_for'] = [
                "점들의 전반적인 패턴",
                "선형 관계의 강도와 방향",
                "이상값의 존재",
                "비선형 패턴"
            ]
            
            if abs(correlation) > 0.7:
                strength = "강한"
            elif abs(correlation) > 0.3:
                strength = "중간"
            else:
                strength = "약한"
            
            direction = "양의" if correlation > 0 else "음의"
            
            guide['key_insights'] = [
                f"{direction} {strength} 선형 관계가 관찰됩니다 (r={correlation:.3f})",
                "상관관계가 있다고 해서 인과관계가 있는 것은 아닙니다"
            ]
            
            guide['common_mistakes'] = [
                "상관관계와 인과관계를 혼동하지 마세요",
                "이상값이 상관계수에 큰 영향을 줄 수 있습니다"
            ]
        
        elif config.chart_type == ChartType.BOXPLOT:
            guide['what_to_look_for'] = [
                "중앙값 (박스 안의 선)",
                "사분위수 범위 (박스의 크기)",
                "이상값 (점으로 표시)",
                "그룹 간 차이"
            ]
            
            guide['key_insights'] = [
                "박스의 크기는 데이터의 산포도를 나타냅니다",
                "수염의 길이는 데이터의 범위를 보여줍니다"
            ]
        
        return guide
    
    def _generate_interactive_elements(self, data: Dict[str, Any], 
                                     config: VisualizationConfig) -> List[Dict[str, Any]]:
        """인터랙티브 요소 정보 생성"""
        
        elements = []
        
        if config.interactive:
            if config.chart_type == ChartType.HISTOGRAM:
                elements.append({
                    'type': 'slider',
                    'name': 'bins',
                    'label': '구간 개수',
                    'min': 5,
                    'max': 50,
                    'default': 20,
                    'description': '히스토그램의 구간 개수를 조절합니다'
                })
                
                elements.append({
                    'type': 'checkbox',
                    'name': 'show_normal_curve',
                    'label': '정규분포 곡선 표시',
                    'default': False,
                    'description': '정규분포 곡선을 오버레이로 표시합니다'
                })
            
            elif config.chart_type == ChartType.SCATTER:
                elements.append({
                    'type': 'checkbox',
                    'name': 'show_regression_line',
                    'label': '회귀선 표시',
                    'default': True,
                    'description': '최적 회귀선을 표시합니다'
                })
                
                elements.append({
                    'type': 'dropdown',
                    'name': 'color_by',
                    'label': '색상 구분',
                    'options': ['없음', '그룹별', '값별'],
                    'default': '없음',
                    'description': '점들을 다른 기준으로 색상 구분합니다'
                })
        
        return elements
    
    def _generate_learning_insights(self, data: Dict[str, Any], 
                                  config: VisualizationConfig) -> List[str]:
        """학습 인사이트 생성"""
        
        insights = []
        
        if config.learning_level == LearningLevel.BEGINNER:
            if config.chart_type == ChartType.HISTOGRAM:
                insights.extend([
                    "히스토그램은 연속형 데이터의 분포를 시각화하는 기본적인 방법입니다",
                    "x축은 데이터 값의 구간을, y축은 각 구간의 빈도를 나타냅니다",
                    "분포의 모양을 통해 데이터의 특성을 파악할 수 있습니다"
                ])
            
            elif config.chart_type == ChartType.SCATTER:
                insights.extend([
                    "산점도는 두 연속형 변수 간의 관계를 보여줍니다",
                    "점들이 일직선에 가깝게 배열되면 강한 선형 관계가 있습니다",
                    "상관계수는 -1에서 1 사이의 값을 가집니다"
                ])
        
        elif config.learning_level == LearningLevel.INTERMEDIATE:
            if config.chart_type == ChartType.HISTOGRAM:
                values = data['values']
                skewness = self._calculate_skewness(values)
                
                if abs(skewness) > 0.5:
                    insights.append(f"분포의 비대칭도(skewness)가 {skewness:.2f}로, 치우친 분포입니다")
                
                insights.append("정규성 검정을 통해 정규분포 가정을 확인해보세요")
        
        return insights
    
    def _calculate_skewness(self, data: np.ndarray) -> float:
        """비대칭도 계산"""
        mean = np.mean(data)
        std = np.std(data)
        n = len(data)
        
        skewness = np.sum(((data - mean) / std) ** 3) / n
        return skewness
    
    def _suggest_next_visualizations(self, data: Dict[str, Any], 
                                   config: VisualizationConfig) -> List[Dict[str, str]]:
        """다음 시각화 제안"""
        
        suggestions = []
        
        if config.chart_type == ChartType.HISTOGRAM:
            suggestions.extend([
                {
                    'type': 'boxplot',
                    'reason': '이상값과 사분위수를 더 명확히 보기 위해',
                    'description': '박스플롯으로 분포의 요약 통계를 확인해보세요'
                },
                {
                    'type': 'density',
                    'reason': '부드러운 분포 곡선을 보기 위해',
                    'description': '밀도 플롯으로 연속적인 분포 형태를 확인해보세요'
                }
            ])
        
        elif config.chart_type == ChartType.SCATTER:
            suggestions.extend([
                {
                    'type': 'correlation_matrix',
                    'reason': '여러 변수 간의 관계를 한눈에 보기 위해',
                    'description': '상관행렬로 모든 변수 쌍의 관계를 확인해보세요'
                },
                {
                    'type': 'line',
                    'reason': '시간에 따른 변화를 보기 위해',
                    'description': '시계열 데이터라면 선 그래프로 추세를 확인해보세요'
                }
            ])
        
        elif config.chart_type == ChartType.BOXPLOT:
            suggestions.extend([
                {
                    'type': 'violin',
                    'reason': '분포의 형태를 더 자세히 보기 위해',
                    'description': '바이올린 플롯으로 각 그룹의 분포 형태를 확인해보세요'
                }
            ])
        
        return suggestions
    
    def create_learning_dashboard(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """학습 대시보드 생성"""
        
        dashboard = {
            'progress_chart': None,
            'performance_trend': None,
            'topic_comparison': None,
            'recommendations': []
        }
        
        # 학습 진도 차트
        if 'progress_data' in user_data:
            progress_config = VisualizationConfig(
                chart_type=ChartType.BAR,
                title="학습 진도",
                x_label="주제",
                y_label="완료율 (%)",
                color_scheme='default',
                show_statistics=True,
                show_annotations=True,
                interactive=True,
                accessibility_mode=False,
                learning_level=LearningLevel.INTERMEDIATE
            )
            
            dashboard['progress_chart'] = self.create_adaptive_visualization(
                user_data['progress_data'], progress_config
            )
        
        # 성과 추세 차트
        if 'performance_data' in user_data:
            trend_config = VisualizationConfig(
                chart_type=ChartType.LINE,
                title="학습 성과 추세",
                x_label="시간",
                y_label="점수",
                color_scheme='default',
                show_statistics=True,
                show_annotations=True,
                interactive=True,
                accessibility_mode=False,
                learning_level=LearningLevel.INTERMEDIATE
            )
            
            dashboard['performance_trend'] = self.create_adaptive_visualization(
                user_data['performance_data'], trend_config
            )
        
        # 주제별 비교 차트
        if 'topic_scores' in user_data:
            comparison_config = VisualizationConfig(
                chart_type=ChartType.BOXPLOT,
                title="주제별 성과 비교",
                x_label="주제",
                y_label="점수",
                color_scheme='colorblind_friendly',
                show_statistics=True,
                show_annotations=True,
                interactive=False,
                accessibility_mode=False,
                learning_level=LearningLevel.INTERMEDIATE
            )
            
            dashboard['topic_comparison'] = self.create_adaptive_visualization(
                user_data['topic_scores'], comparison_config
            )
        
        # 개선 권장사항
        dashboard['recommendations'] = [
            "약점 주제에 더 많은 시간을 투자하세요",
            "꾸준한 학습으로 성과 추세를 유지하세요",
            "다양한 시각화 방법을 활용해 데이터를 이해하세요"
        ]
        
        return dashboard

# 사용 예제
if __name__ == "__main__":
    # 시각화 엔진 초기화
    viz_engine = EnhancedVisualizationEngine()
    
    # 샘플 데이터
    sample_data = {
        'values': np.random.normal(50, 15, 1000)
    }
    
    # 시각화 설정
    config = VisualizationConfig(
        chart_type=ChartType.HISTOGRAM,
        title="학생 성적 분포",
        x_label="점수",
        y_label="빈도",
        color_scheme='default',
        show_statistics=True,
        show_annotations=True,
        interactive=True,
        accessibility_mode=False,
        learning_level=LearningLevel.BEGINNER
    )
    
    # 사용자 프로필
    user_profile = {
        'learning_level': 'beginner',
        'visual_preference': 'detailed'
    }
    
    # 적응형 시각화 생성
    result = viz_engine.create_adaptive_visualization(sample_data, config, user_profile)
    
    print("시각화 생성 완료!")
    print(f"해석 가이드 항목 수: {len(result['interpretation_guide']['what_to_look_for'])}")
    print(f"학습 인사이트 수: {len(result['learning_insights'])}")
    print(f"다음 시각화 제안 수: {len(result['next_steps'])}")
    
    # 차트 base64 데이터 길이 확인
    print(f"차트 데이터 크기: {len(result['chart_base64'])} characters")