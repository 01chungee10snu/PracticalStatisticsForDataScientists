#!/usr/bin/env python3
"""
의존성 없는 데이터 시각화 모듈
- ASCII 아트로 차트 생성
- 기본 Python만 사용
- 브라우저에서 표시 가능한 시각화
"""

import math
from typing import List, Dict, Any, Tuple


class SimpleVisualization:
    """의존성 없는 간단한 시각화 클래스"""
    
    def __init__(self):
        self.chart_width = 60
        self.chart_height = 20
    
    def create_histogram_ascii(self, data: List[float], title: str = "히스토그램") -> str:
        """ASCII 아트 히스토그램 생성"""
        if not data:
            return "데이터가 없습니다."
        
        # 데이터 범위 계산
        min_val = min(data)
        max_val = max(data)
        
        # 구간 설정 (보통 5-10개 구간)
        num_bins = min(8, len(set(data)))
        bin_width = (max_val - min_val) / num_bins if max_val != min_val else 1
        
        # 빈도 계산
        bins = [0] * num_bins
        for value in data:
            if max_val == min_val:
                bin_idx = 0
            else:
                bin_idx = min(int((value - min_val) / bin_width), num_bins - 1)
            bins[bin_idx] += 1
        
        # 최대 빈도로 정규화
        max_freq = max(bins) if bins else 1
        
        # ASCII 차트 생성
        result = [f"\n📊 {title}"]
        result.append("=" * 50)
        
        for i in range(self.chart_height, 0, -1):
            line = f"{i:2d} |"
            for bin_count in bins:
                if bin_count * self.chart_height / max_freq >= i:
                    line += "██"
                else:
                    line += "  "
            result.append(line)
        
        # X축 레이블
        x_axis = "   +"
        for i in range(num_bins):
            x_axis += "--"
        result.append(x_axis)
        
        # 구간 레이블
        labels = "     "
        for i in range(num_bins):
            bin_start = min_val + i * bin_width
            labels += f"{bin_start:.1f}"[:4].ljust(4)
        result.append(labels)
        
        return "\n".join(result)
    
    def create_bar_chart_ascii(self, categories: List[str], values: List[float], title: str = "막대 차트") -> str:
        """ASCII 막대 차트 생성"""
        if not categories or not values or len(categories) != len(values):
            return "유효하지 않은 데이터입니다."
        
        max_val = max(values) if values else 1
        
        result = [f"\n📊 {title}"]
        result.append("=" * 50)
        
        for i, (category, value) in enumerate(zip(categories, values)):
            bar_length = int((value / max_val) * 40) if max_val > 0 else 0
            bar = "█" * bar_length
            result.append(f"{category[:10]:10s} |{bar:<40s} {value:.1f}")
        
        return "\n".join(result)
    
    def create_scatter_plot_ascii(self, x_data: List[float], y_data: List[float], title: str = "산점도") -> str:
        """ASCII 산점도 생성"""
        if not x_data or not y_data or len(x_data) != len(y_data):
            return "유효하지 않은 데이터입니다."
        
        min_x, max_x = min(x_data), max(x_data)
        min_y, max_y = min(y_data), max(y_data)
        
        # 정규화
        width, height = 50, 20
        
        result = [f"\n📊 {title}"]
        result.append("=" * 60)
        
        # 차트 영역 초기화
        chart = [[" " for _ in range(width)] for _ in range(height)]
        
        # 데이터 포인트 배치
        for x, y in zip(x_data, y_data):
            if max_x != min_x and max_y != min_y:
                chart_x = int((x - min_x) / (max_x - min_x) * (width - 1))
                chart_y = int((max_y - y) / (max_y - min_y) * (height - 1))
                if 0 <= chart_x < width and 0 <= chart_y < height:
                    chart[chart_y][chart_x] = "●"
        
        # 출력
        for i, row in enumerate(chart):
            y_val = max_y - (i / (height - 1)) * (max_y - min_y) if max_y != min_y else max_y
            result.append(f"{y_val:6.1f} |{''.join(row)}")
        
        # X축
        x_axis = "       +" + "-" * width
        result.append(x_axis)
        result.append(f"       {min_x:6.1f}{'':<{width-12}}{max_x:6.1f}")
        
        return "\n".join(result)
    
    def create_distribution_summary(self, data: List[float]) -> str:
        """분포 요약 통계 시각화"""
        if not data:
            return "데이터가 없습니다."
        
        n = len(data)
        sorted_data = sorted(data)
        
        # 기본 통계량 계산
        mean = sum(data) / n
        median = sorted_data[n//2] if n % 2 == 1 else (sorted_data[n//2-1] + sorted_data[n//2]) / 2
        
        # 사분위수
        q1 = sorted_data[n//4]
        q3 = sorted_data[3*n//4]
        
        # 분산과 표준편차
        variance = sum((x - mean) ** 2 for x in data) / n
        std_dev = math.sqrt(variance)
        
        result = ["\n📈 분포 요약 통계"]
        result.append("=" * 40)
        result.append(f"📊 데이터 개수: {n}")
        result.append(f"📊 평균: {mean:.2f}")
        result.append(f"📊 중앙값: {median:.2f}")
        result.append(f"📊 표준편차: {std_dev:.2f}")
        result.append(f"📊 최솟값: {min(data):.2f}")
        result.append(f"📊 최댓값: {max(data):.2f}")
        result.append("")
        
        # 상자그림 (간단한 버전)
        result.append("📦 상자그림 (Box Plot)")
        result.append("-" * 40)
        
        # 정규화된 위치 계산
        min_val, max_val = min(data), max(data)
        if max_val != min_val:
            q1_pos = int((q1 - min_val) / (max_val - min_val) * 30)
            median_pos = int((median - min_val) / (max_val - min_val) * 30)
            q3_pos = int((q3 - min_val) / (max_val - min_val) * 30)
            
            box_plot = ["-"] * 30
            box_plot[0] = "|"  # 최솟값
            box_plot[q1_pos] = "["  # Q1
            box_plot[median_pos] = "|"  # 중앙값
            box_plot[q3_pos] = "]"  # Q3
            box_plot[29] = "|"  # 최댓값
            
            result.append("".join(box_plot))
            result.append(f"{min_val:.1f}                           {max_val:.1f}")
        
        return "\n".join(result)
    
    def create_correlation_heatmap(self, data_dict: Dict[str, List[float]]) -> str:
        """상관계수 히트맵 (ASCII)"""
        variables = list(data_dict.keys())
        n_vars = len(variables)
        
        if n_vars < 2:
            return "상관분석을 위해서는 최소 2개의 변수가 필요합니다."
        
        # 상관계수 계산
        correlations = {}
        for i, var1 in enumerate(variables):
            correlations[var1] = {}
            for j, var2 in enumerate(variables):
                if var1 == var2:
                    correlations[var1][var2] = 1.0
                else:
                    # 피어슨 상관계수 계산
                    data1, data2 = data_dict[var1], data_dict[var2]
                    if len(data1) != len(data2):
                        correlations[var1][var2] = 0.0
                        continue
                    
                    n = len(data1)
                    if n == 0:
                        correlations[var1][var2] = 0.0
                        continue
                    
                    mean1 = sum(data1) / n
                    mean2 = sum(data2) / n
                    
                    numerator = sum((data1[k] - mean1) * (data2[k] - mean2) for k in range(n))
                    denominator1 = sum((data1[k] - mean1) ** 2 for k in range(n))
                    denominator2 = sum((data2[k] - mean2) ** 2 for k in range(n))
                    
                    if denominator1 == 0 or denominator2 == 0:
                        correlations[var1][var2] = 0.0
                    else:
                        correlations[var1][var2] = numerator / math.sqrt(denominator1 * denominator2)
        
        # ASCII 히트맵 생성
        result = ["\n🔥 상관계수 히트맵"]
        result.append("=" * 50)
        
        # 헤더
        header = "        "
        for var in variables:
            header += f"{var[:6]:>8s}"
        result.append(header)
        
        # 상관계수 매트릭스
        for var1 in variables:
            row = f"{var1[:6]:6s}  "
            for var2 in variables:
                corr = correlations[var1][var2]
                # 상관계수에 따른 심볼
                if corr > 0.7:
                    symbol = "██"
                elif corr > 0.3:
                    symbol = "▓▓"
                elif corr > -0.3:
                    symbol = "░░"
                elif corr > -0.7:
                    symbol = "▒▒"
                else:
                    symbol = "  "
                
                row += f"{symbol}({corr:+.2f})"[:8]
            result.append(row)
        
        result.append("\n범례: ██(강한양의상관) ▓▓(양의상관) ░░(약한상관) ▒▒(음의상관)")
        
        return "\n".join(result)
    
    def create_html_chart(self, chart_type: str, data: Dict[str, Any]) -> str:
        """브라우저용 HTML 차트 생성"""
        if chart_type == "bar":
            return self._create_html_bar_chart(data)
        elif chart_type == "line":
            return self._create_html_line_chart(data)
        elif chart_type == "scatter":
            return self._create_html_scatter_plot(data)
        else:
            return "<p>지원하지 않는 차트 타입입니다.</p>"
    
    def _create_html_bar_chart(self, data: Dict[str, Any]) -> str:
        """HTML/CSS 막대 차트"""
        categories = data.get("categories", [])
        values = data.get("values", [])
        title = data.get("title", "막대 차트")
        
        if not categories or not values:
            return "<p>데이터가 없습니다.</p>"
        
        max_val = max(values) if values else 1
        
        html = f"""
        <div class="chart-container">
            <h3>{title}</h3>
            <div class="bar-chart">
        """
        
        for category, value in zip(categories, values):
            height_percent = (value / max_val) * 100 if max_val > 0 else 0
            html += f"""
                <div class="bar-item">
                    <div class="bar" style="height: {height_percent}%; background: linear-gradient(45deg, #007bff, #0056b3);">
                        <span class="bar-value">{value:.1f}</span>
                    </div>
                    <div class="bar-label">{category}</div>
                </div>
            """
        
        html += """
            </div>
        </div>
        <style>
            .chart-container { margin: 20px 0; }
            .bar-chart { display: flex; align-items: end; height: 200px; gap: 10px; padding: 20px; background: #f8f9fa; border-radius: 8px; }
            .bar-item { display: flex; flex-direction: column; align-items: center; flex: 1; }
            .bar { position: relative; min-height: 10px; border-radius: 4px 4px 0 0; transition: all 0.3s; }
            .bar:hover { transform: scale(1.05); }
            .bar-value { position: absolute; top: -25px; color: #333; font-size: 12px; font-weight: bold; }
            .bar-label { margin-top: 10px; font-size: 12px; text-align: center; }
        </style>
        """
        
        return html
    
    def _create_html_line_chart(self, data: Dict[str, Any]) -> str:
        """HTML/CSS 라인 차트"""
        x_data = data.get("x_data", [])
        y_data = data.get("y_data", [])
        title = data.get("title", "라인 차트")
        
        if not x_data or not y_data:
            return "<p>데이터가 없습니다.</p>"
        
        # SVG로 라인 차트 생성
        width, height = 400, 200
        margin = 40
        
        min_x, max_x = min(x_data), max(x_data)
        min_y, max_y = min(y_data), max(y_data)
        
        # 점들의 좌표 계산
        points = []
        for x, y in zip(x_data, y_data):
            if max_x != min_x and max_y != min_y:
                svg_x = margin + (x - min_x) / (max_x - min_x) * (width - 2 * margin)
                svg_y = height - margin - (y - min_y) / (max_y - min_y) * (height - 2 * margin)
                points.append(f"{svg_x:.1f},{svg_y:.1f}")
        
        polyline = " ".join(points)
        
        html = f"""
        <div class="chart-container">
            <h3>{title}</h3>
            <svg width="{width}" height="{height}" style="border: 1px solid #ddd; background: white;">
                <!-- 격자 -->
                <defs>
                    <pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse">
                        <path d="M 20 0 L 0 0 0 20" fill="none" stroke="#e0e0e0" stroke-width="1"/>
                    </pattern>
                </defs>
                <rect width="100%" height="100%" fill="url(#grid)" />
                
                <!-- 데이터 라인 -->
                <polyline points="{polyline}" fill="none" stroke="#007bff" stroke-width="3"/>
                
                <!-- 데이터 포인트 -->
        """
        
        for i, (x, y) in enumerate(zip(x_data, y_data)):
            if max_x != min_x and max_y != min_y:
                svg_x = margin + (x - min_x) / (max_x - min_x) * (width - 2 * margin)
                svg_y = height - margin - (y - min_y) / (max_y - min_y) * (height - 2 * margin)
                html += f'<circle cx="{svg_x:.1f}" cy="{svg_y:.1f}" r="4" fill="#007bff"/>'
        
        html += f"""
                <!-- 축 레이블 -->
                <text x="{margin}" y="{height - 10}" font-size="12">{min_x:.1f}</text>
                <text x="{width - margin}" y="{height - 10}" font-size="12">{max_x:.1f}</text>
                <text x="5" y="{height - margin}" font-size="12">{min_y:.1f}</text>
                <text x="5" y="{margin}" font-size="12">{max_y:.1f}</text>
            </svg>
        </div>
        """
        
        return html
    
    def _create_html_scatter_plot(self, data: Dict[str, Any]) -> str:
        """HTML/CSS 산점도"""
        x_data = data.get("x_data", [])
        y_data = data.get("y_data", [])
        title = data.get("title", "산점도")
        
        if not x_data or not y_data:
            return "<p>데이터가 없습니다.</p>"
        
        width, height = 400, 300
        margin = 40
        
        min_x, max_x = min(x_data), max(x_data)
        min_y, max_y = min(y_data), max(y_data)
        
        html = f"""
        <div class="chart-container">
            <h3>{title}</h3>
            <svg width="{width}" height="{height}" style="border: 1px solid #ddd; background: white;">
                <!-- 배경 격자 -->
                <defs>
                    <pattern id="scatter-grid" width="25" height="25" patternUnits="userSpaceOnUse">
                        <path d="M 25 0 L 0 0 0 25" fill="none" stroke="#f0f0f0" stroke-width="1"/>
                    </pattern>
                </defs>
                <rect width="100%" height="100%" fill="url(#scatter-grid)" />
        """
        
        # 데이터 포인트
        for x, y in zip(x_data, y_data):
            if max_x != min_x and max_y != min_y:
                svg_x = margin + (x - min_x) / (max_x - min_x) * (width - 2 * margin)
                svg_y = height - margin - (y - min_y) / (max_y - min_y) * (height - 2 * margin)
                html += f"""
                <circle cx="{svg_x:.1f}" cy="{svg_y:.1f}" r="5" fill="#007bff" fill-opacity="0.7" 
                        stroke="#0056b3" stroke-width="1">
                    <title>({x:.2f}, {y:.2f})</title>
                </circle>
                """
        
        html += f"""
                <!-- 축 -->
                <line x1="{margin}" y1="{height-margin}" x2="{width-margin}" y2="{height-margin}" 
                      stroke="#333" stroke-width="2"/>
                <line x1="{margin}" y1="{margin}" x2="{margin}" y2="{height-margin}" 
                      stroke="#333" stroke-width="2"/>
                
                <!-- 축 레이블 -->
                <text x="{width/2}" y="{height-5}" text-anchor="middle" font-size="12">X 값</text>
                <text x="15" y="{height/2}" text-anchor="middle" font-size="12" transform="rotate(-90 15 {height/2})">Y 값</text>
                
                <!-- 범위 표시 -->
                <text x="{margin}" y="{height-10}" font-size="10">{min_x:.1f}</text>
                <text x="{width-margin}" y="{height-10}" font-size="10">{max_x:.1f}</text>
                <text x="25" y="{height-margin}" font-size="10">{min_y:.1f}</text>
                <text x="25" y="{margin+5}" font-size="10">{max_y:.1f}</text>
            </svg>
        </div>
        """
        
        return html


# 전역 시각화 인스턴스
visualizer = SimpleVisualization()


def create_statistics_visualization(data: List[float], title: str = "통계 분석") -> str:
    """통계 분석을 위한 종합 시각화"""
    if not data:
        return "데이터가 없습니다."
    
    result = []
    
    # 기본 통계량
    result.append(visualizer.create_distribution_summary(data))
    
    # 히스토그램
    result.append(visualizer.create_histogram_ascii(data, f"{title} - 분포"))
    
    return "\n\n".join(result)


def create_comparison_chart(categories: List[str], values: List[float], title: str = "비교 차트") -> str:
    """카테고리별 비교 차트"""
    return visualizer.create_bar_chart_ascii(categories, values, title)


def create_relationship_plot(x_data: List[float], y_data: List[float], title: str = "관계 분석") -> str:
    """두 변수 간의 관계 시각화"""
    result = []
    
    # 산점도
    result.append(visualizer.create_scatter_plot_ascii(x_data, y_data, title))
    
    # 상관계수 계산
    if len(x_data) == len(y_data) and len(x_data) > 1:
        n = len(x_data)
        mean_x = sum(x_data) / n
        mean_y = sum(y_data) / n
        
        numerator = sum((x_data[i] - mean_x) * (y_data[i] - mean_y) for i in range(n))
        denominator_x = sum((x_data[i] - mean_x) ** 2 for i in range(n))
        denominator_y = sum((y_data[i] - mean_y) ** 2 for i in range(n))
        
        if denominator_x > 0 and denominator_y > 0:
            correlation = numerator / math.sqrt(denominator_x * denominator_y)
            
            result.append(f"\n📊 상관분석 결과")
            result.append("=" * 30)
            result.append(f"상관계수: {correlation:.3f}")
            
            if abs(correlation) > 0.8:
                strength = "매우 강한"
            elif abs(correlation) > 0.6:
                strength = "강한"
            elif abs(correlation) > 0.4:
                strength = "중간"
            elif abs(correlation) > 0.2:
                strength = "약한"
            else:
                strength = "매우 약한"
            
            direction = "양의" if correlation > 0 else "음의"
            result.append(f"해석: {strength} {direction} 상관관계")
    
    return "\n".join(result)