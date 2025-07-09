import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA, FactorAnalysis
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
from . import data_processing

# Plotly import with error handling
try:
    import plotly.graph_objects as go
    import plotly.express as px
    from plotly.subplots import make_subplots
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    print("Plotly not available. Interactive dashboards will be disabled.")

sns.set_theme(style="whitegrid")
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False


def plot_statistics(data):
    """평균, 분산, 상관관계 그래프를 그려 base64 이미지로 반환"""
    fig, axs = plt.subplots(1, 3, figsize=(12, 4))
    axs[0].bar(data.index, data['x'])
    axs[0].set_title('평균')
    axs[0].axhline(data['x'].mean(), color='red', linestyle='--')

    axs[1].hist(data['x'], bins=10, color='skyblue')
    axs[1].set_title('분산')
    axs[1].axvline(data['x'].var(), color='red', linestyle='--')

    sns.scatterplot(x='x', y='y', data=data, ax=axs[2])
    axs[2].set_title('상관관계')

    buf = BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('utf8')


def plot_iris_example(df=None):
    """Iris 데이터셋을 활용한 기본 통계 그래프"""
    if df is None:
        df = data_processing.load_public_dataset()

    fig, axs = plt.subplots(1, 2, figsize=(10, 4))
    sns.histplot(df['sepal_length'], kde=True, ax=axs[0])
    axs[0].set_title('꽃받침 길이 분포')

    sns.scatterplot(x='sepal_length', y='petal_length', hue='species', data=df, ax=axs[1])
    axs[1].set_title('꽃받침 길이와 꽃잎 길이')

    buf = BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('utf8')


def plot_research_methodology(df, analysis_type='descriptive'):
    """연구방법론 레벨용 시각화 - 질적/양적 연구 개념 설명"""
    fig = plt.figure(figsize=(15, 10))
    
    if analysis_type == 'descriptive':
        # 기술통계 시각화
        gs = fig.add_gridspec(2, 3, hspace=0.3, wspace=0.3)
        
        # 연령 분포
        ax1 = fig.add_subplot(gs[0, 0])
        sns.histplot(df['age'], bins=15, kde=True, ax=ax1)
        ax1.set_title('연령 분포')
        ax1.axvline(df['age'].mean(), color='red', linestyle='--', label=f'평균: {df["age"].mean():.1f}')
        ax1.legend()
        
        # 성별 분포
        ax2 = fig.add_subplot(gs[0, 1])
        gender_counts = df['gender'].value_counts()
        ax2.pie(gender_counts.values, labels=gender_counts.index, autopct='%1.1f%%')
        ax2.set_title('성별 분포')
        
        # 교육 수준
        ax3 = fig.add_subplot(gs[0, 2])
        education_counts = df['education'].value_counts()
        ax3.bar(education_counts.index, education_counts.values)
        ax3.set_title('교육 수준 분포')
        ax3.tick_params(axis='x', rotation=45)
        
        # 그룹별 성공률
        ax4 = fig.add_subplot(gs[1, 0])
        success_by_group = df.groupby('group')['success'].mean()
        ax4.bar(success_by_group.index, success_by_group.values)
        ax4.set_title('그룹별 성공률')
        ax4.set_ylabel('성공률')
        
        # 연령-성과 상관관계
        ax5 = fig.add_subplot(gs[1, 1])
        if 'performance_score' in df.columns:
            sns.scatterplot(x='age', y='performance_score', hue='group', data=df, ax=ax5)
            ax5.set_title('연령-성과 상관관계')
        
        # 성별-교육 교차표
        ax6 = fig.add_subplot(gs[1, 2])
        crosstab = pd.crosstab(df['gender'], df['education'])
        sns.heatmap(crosstab, annot=True, fmt='d', ax=ax6)
        ax6.set_title('성별-교육 교차표')
        
    elif analysis_type == 'comparative':
        # 비교 분석 시각화
        gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)
        
        # 그룹 비교 박스플롯
        ax1 = fig.add_subplot(gs[0, 0])
        if 'performance_score' in df.columns:
            sns.boxplot(x='group', y='performance_score', data=df, ax=ax1)
            ax1.set_title('그룹별 성과 점수 비교')
        
        # 성별 비교
        ax2 = fig.add_subplot(gs[0, 1])
        if 'performance_score' in df.columns:
            sns.violinplot(x='gender', y='performance_score', data=df, ax=ax2)
            ax2.set_title('성별 성과 점수 비교')
        
        # 교육 수준별 비교
        ax3 = fig.add_subplot(gs[1, 0])
        if 'performance_score' in df.columns:
            sns.boxplot(x='education', y='performance_score', data=df, ax=ax3)
            ax3.set_title('교육 수준별 성과 비교')
            ax3.tick_params(axis='x', rotation=45)
        
        # 다중 변수 관계
        ax4 = fig.add_subplot(gs[1, 1])
        if 'performance_score' in df.columns:
            sns.scatterplot(x='age', y='performance_score', hue='gender', 
                          style='group', data=df, ax=ax4)
            ax4.set_title('다중 변수 관계 분석')
    
    buf = BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png', dpi=300, bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('utf8')


def plot_factor_analysis(df, n_factors=4):
    """요인분석 레벨용 시각화"""
    # 요인분석 수행
    scaler = StandardScaler()
    df_scaled = scaler.fit_transform(df.select_dtypes(include=[np.number]))
    
    fa = FactorAnalysis(n_components=n_factors, random_state=42)
    factor_scores = fa.fit_transform(df_scaled)
    
    fig = plt.figure(figsize=(16, 12))
    gs = fig.add_gridspec(3, 3, hspace=0.4, wspace=0.4)
    
    # 1. 요인 로딩 히트맵
    ax1 = fig.add_subplot(gs[0, 0])
    loadings = fa.components_.T
    sns.heatmap(loadings, annot=True, fmt='.2f', ax=ax1, cmap='RdBu_r')
    ax1.set_title('요인 로딩 행렬')
    ax1.set_xlabel('요인')
    ax1.set_ylabel('변수')
    
    # 2. 스크리 플롯
    ax2 = fig.add_subplot(gs[0, 1])
    pca = PCA()
    pca.fit(df_scaled)
    eigenvalues = pca.explained_variance_
    ax2.plot(range(1, len(eigenvalues) + 1), eigenvalues, 'bo-')
    ax2.axhline(y=1, color='r', linestyle='--', label='Kaiser 기준')
    ax2.set_title('스크리 플롯 (고유값)')
    ax2.set_xlabel('성분 번호')
    ax2.set_ylabel('고유값')
    ax2.legend()
    
    # 3. 설명 분산 비율
    ax3 = fig.add_subplot(gs[0, 2])
    explained_var = pca.explained_variance_ratio_
    cumulative_var = np.cumsum(explained_var)
    ax3.bar(range(1, len(explained_var) + 1), explained_var, alpha=0.7, label='개별 설명 분산')
    ax3.plot(range(1, len(cumulative_var) + 1), cumulative_var, 'ro-', label='누적 설명 분산')
    ax3.set_title('설명 분산 비율')
    ax3.set_xlabel('성분 번호')
    ax3.set_ylabel('설명 분산 비율')
    ax3.legend()
    
    # 4-6. 요인 점수 산점도
    for i in range(min(3, n_factors-1)):
        ax = fig.add_subplot(gs[1, i])
        scatter = ax.scatter(factor_scores[:, i], factor_scores[:, i+1], alpha=0.6)
        ax.set_xlabel(f'요인 {i+1}')
        ax.set_ylabel(f'요인 {i+2}')
        ax.set_title(f'요인 {i+1} vs 요인 {i+2}')
        ax.grid(True, alpha=0.3)
    
    # 7. 요인 점수 분포
    ax7 = fig.add_subplot(gs[2, 0])
    for i in range(n_factors):
        ax7.hist(factor_scores[:, i], alpha=0.5, label=f'요인 {i+1}', bins=20)
    ax7.set_title('요인 점수 분포')
    ax7.set_xlabel('요인 점수')
    ax7.set_ylabel('빈도')
    ax7.legend()
    
    # 8. 요인 간 상관관계
    ax8 = fig.add_subplot(gs[2, 1])
    factor_corr = np.corrcoef(factor_scores.T)
    sns.heatmap(factor_corr, annot=True, fmt='.2f', ax=ax8, cmap='RdBu_r')
    ax8.set_title('요인 간 상관관계')
    
    # 9. 공통성 (Communalities)
    ax9 = fig.add_subplot(gs[2, 2])
    communalities = np.sum(loadings**2, axis=1)
    ax9.bar(range(len(communalities)), communalities)
    ax9.set_title('공통성 (Communalities)')
    ax9.set_xlabel('변수')
    ax9.set_ylabel('공통성')
    ax9.axhline(y=0.5, color='r', linestyle='--', label='기준선 (0.5)')
    ax9.legend()
    
    buf = BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png', dpi=300, bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('utf8')


def plot_advanced_analytics(df, analysis_type='classification'):
    """고급 분석 레벨용 시각화"""
    fig = plt.figure(figsize=(16, 12))
    
    if analysis_type == 'classification':
        from sklearn.model_selection import train_test_split
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.metrics import classification_report, confusion_matrix
        
        # 데이터 준비
        X = df.select_dtypes(include=[np.number]).drop('target', axis=1, errors='ignore')
        if 'target' in df.columns:
            y = df['target']
        else:
            y = df['success'] if 'success' in df.columns else df.iloc[:, -1]
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
        
        # 모델 학습
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        
        gs = fig.add_gridspec(3, 3, hspace=0.4, wspace=0.4)
        
        # 1. 특성 중요도
        ax1 = fig.add_subplot(gs[0, 0])
        feature_importance = pd.DataFrame({
            'feature': X.columns,
            'importance': model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        sns.barplot(data=feature_importance.head(10), x='importance', y='feature', ax=ax1)
        ax1.set_title('특성 중요도')
        
        # 2. 혼동 행렬
        ax2 = fig.add_subplot(gs[0, 1])
        cm = confusion_matrix(y_test, y_pred)
        sns.heatmap(cm, annot=True, fmt='d', ax=ax2, cmap='Blues')
        ax2.set_title('혼동 행렬')
        ax2.set_xlabel('예측값')
        ax2.set_ylabel('실제값')
        
        # 3. 예측 확률 분포
        ax3 = fig.add_subplot(gs[0, 2])
        pred_proba = model.predict_proba(X_test)[:, 1] if len(model.classes_) == 2 else model.predict_proba(X_test)[:, 0]
        ax3.hist(pred_proba, bins=20, alpha=0.7, edgecolor='black')
        ax3.set_title('예측 확률 분포')
        ax3.set_xlabel('예측 확률')
        ax3.set_ylabel('빈도')
        
        # 4. 특성 간 상관관계
        ax4 = fig.add_subplot(gs[1, 0])
        corr_matrix = X.corr()
        sns.heatmap(corr_matrix, annot=True, fmt='.2f', ax=ax4, cmap='RdBu_r')
        ax4.set_title('특성 간 상관관계')
        
        # 5. 주성분 분석
        ax5 = fig.add_subplot(gs[1, 1])
        pca = PCA(n_components=2)
        X_pca = pca.fit_transform(StandardScaler().fit_transform(X))
        scatter = ax5.scatter(X_pca[:, 0], X_pca[:, 1], c=y, alpha=0.6)
        ax5.set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.2%} variance)')
        ax5.set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.2%} variance)')
        ax5.set_title('주성분 분석 (PCA)')
        
        # 6. 클러스터링
        ax6 = fig.add_subplot(gs[1, 2])
        kmeans = KMeans(n_clusters=3, random_state=42)
        clusters = kmeans.fit_predict(X_pca)
        scatter = ax6.scatter(X_pca[:, 0], X_pca[:, 1], c=clusters, alpha=0.6)
        ax6.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], 
                   c='red', marker='x', s=100, linewidths=3)
        ax6.set_xlabel('PC1')
        ax6.set_ylabel('PC2')
        ax6.set_title('K-means 클러스터링')
        
        # 7. 학습 곡선
        ax7 = fig.add_subplot(gs[2, 0])
        train_sizes = np.linspace(0.1, 1.0, 10)
        train_scores = []
        val_scores = []
        
        for size in train_sizes:
            X_temp, _, y_temp, _ = train_test_split(X_train, y_train, 
                                                   train_size=size, random_state=42)
            model_temp = RandomForestClassifier(n_estimators=50, random_state=42)
            model_temp.fit(X_temp, y_temp)
            train_scores.append(model_temp.score(X_temp, y_temp))
            val_scores.append(model_temp.score(X_test, y_test))
        
        ax7.plot(train_sizes, train_scores, 'o-', label='훈련 정확도')
        ax7.plot(train_sizes, val_scores, 'o-', label='검증 정확도')
        ax7.set_title('학습 곡선')
        ax7.set_xlabel('훈련 샘플 비율')
        ax7.set_ylabel('정확도')
        ax7.legend()
        
        # 8. 잔차 분석
        ax8 = fig.add_subplot(gs[2, 1])
        if hasattr(model, 'predict_proba'):
            proba = model.predict_proba(X_test)[:, 1] if len(model.classes_) == 2 else model.predict_proba(X_test)[:, 0]
            residuals = (y_test.astype(int) - proba) if hasattr(y_test, 'astype') else (y_test - proba)
            ax8.scatter(proba, residuals, alpha=0.6)
            ax8.axhline(y=0, color='r', linestyle='--')
            ax8.set_title('잔차 분석')
            ax8.set_xlabel('예측 확률')
            ax8.set_ylabel('잔차')
        
        # 9. 교차 검증 결과
        ax9 = fig.add_subplot(gs[2, 2])
        from sklearn.model_selection import cross_val_score
        cv_scores = cross_val_score(model, X, y, cv=5)
        ax9.bar(range(1, 6), cv_scores)
        ax9.axhline(y=cv_scores.mean(), color='r', linestyle='--', 
                   label=f'평균: {cv_scores.mean():.3f}')
        ax9.set_title('교차 검증 정확도')
        ax9.set_xlabel('폴드')
        ax9.set_ylabel('정확도')
        ax9.legend()
    
    buf = BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png', dpi=300, bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('utf8')


def create_interactive_dashboard(df, level='advanced'):
    """인터랙티브 대시보드 생성 (Plotly 기반)"""
    if not PLOTLY_AVAILABLE:
        return "<div>Plotly가 설치되지 않아 인터랙티브 대시보드를 생성할 수 없습니다.</div>"
    
    if level == 'beginner':
        # 연구방법론 대시보드
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('연령 분포', '성별 비율', '교육 수준', '그룹별 성과'),
            specs=[[{'type': 'histogram'}, {'type': 'pie'}],
                   [{'type': 'bar'}, {'type': 'box'}]]
        )
        
        # 연령 분포
        fig.add_trace(go.Histogram(x=df['age'], name='연령'), row=1, col=1)
        
        # 성별 비율
        gender_counts = df['gender'].value_counts()
        fig.add_trace(go.Pie(labels=gender_counts.index, values=gender_counts.values, name='성별'), row=1, col=2)
        
        # 교육 수준
        education_counts = df['education'].value_counts()
        fig.add_trace(go.Bar(x=education_counts.index, y=education_counts.values, name='교육수준'), row=2, col=1)
        
        # 그룹별 성과
        if 'performance_score' in df.columns:
            for group in df['group'].unique():
                group_data = df[df['group'] == group]['performance_score']
                fig.add_trace(go.Box(y=group_data, name=group), row=2, col=2)
        
    elif level == 'intermediate':
        # 요인분석 대시보드
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        scaler = StandardScaler()
        df_scaled = scaler.fit_transform(df[numeric_cols])
        
        fa = FactorAnalysis(n_components=4, random_state=42)
        factor_scores = fa.fit_transform(df_scaled)
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('요인 로딩', '요인 점수 분포', '요인 상관관계', '공통성'),
            specs=[[{'type': 'heatmap'}, {'type': 'histogram'}],
                   [{'type': 'heatmap'}, {'type': 'bar'}]]
        )
        
        # 요인 로딩 히트맵
        loadings = fa.components_.T
        fig.add_trace(go.Heatmap(z=loadings, colorscale='RdBu_r', name='로딩'), row=1, col=1)
        
        # 요인 점수 분포
        for i in range(4):
            fig.add_trace(go.Histogram(x=factor_scores[:, i], name=f'요인 {i+1}', opacity=0.7), row=1, col=2)
        
        # 요인 상관관계
        factor_corr = np.corrcoef(factor_scores.T)
        fig.add_trace(go.Heatmap(z=factor_corr, colorscale='RdBu_r', name='상관관계'), row=2, col=1)
        
        # 공통성
        communalities = np.sum(loadings**2, axis=1)
        fig.add_trace(go.Bar(x=list(range(len(communalities))), y=communalities, name='공통성'), row=2, col=2)
    
    elif level == 'advanced':
        # 머신러닝 대시보드
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('특성 분포', '상관관계', '클러스터링', '차원 축소'),
            specs=[[{'type': 'histogram'}, {'type': 'heatmap'}],
                   [{'type': 'scatter'}, {'type': 'scatter'}]]
        )
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            # 특성 분포
            for col in numeric_cols[:3]:
                fig.add_trace(go.Histogram(x=df[col], name=col, opacity=0.7), row=1, col=1)
            
            # 상관관계
            corr_matrix = df[numeric_cols].corr()
            fig.add_trace(go.Heatmap(z=corr_matrix.values, x=corr_matrix.columns, 
                                   y=corr_matrix.columns, colorscale='RdBu_r'), row=1, col=2)
            
            # 클러스터링
            if len(numeric_cols) >= 2:
                scaler = StandardScaler()
                X_scaled = scaler.fit_transform(df[numeric_cols])
                kmeans = KMeans(n_clusters=3, random_state=42)
                clusters = kmeans.fit_predict(X_scaled)
                
                fig.add_trace(go.Scatter(x=X_scaled[:, 0], y=X_scaled[:, 1], 
                                       mode='markers', marker=dict(color=clusters)), row=2, col=1)
                
                # 차원 축소
                pca = PCA(n_components=2)
                X_pca = pca.fit_transform(X_scaled)
                fig.add_trace(go.Scatter(x=X_pca[:, 0], y=X_pca[:, 1], 
                                       mode='markers', marker=dict(color=clusters)), row=2, col=2)
    
    fig.update_layout(height=800, showlegend=True, title_text=f"{level.capitalize()} Level Dashboard")
    return fig.to_html(include_plotlyjs='cdn')


def create_unified_visualization(df, level='beginner', analysis_type='default'):
    """레벨별 통합 시각화 함수"""
    if level == 'beginner':
        return plot_research_methodology(df, analysis_type)
    elif level == 'intermediate':
        return plot_factor_analysis(df)
    elif level == 'advanced':
        return plot_advanced_analytics(df, analysis_type)
    else:
        return plot_statistics(df)


def generate_visualization_report(df, level='all'):
    """종합 시각화 보고서 생성"""
    report = {
        'basic_stats': {},
        'visualizations': {},
        'insights': []
    }
    
    # 기본 통계
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 0:
        report['basic_stats'] = {
            'mean': df[numeric_cols].mean().to_dict(),
            'std': df[numeric_cols].std().to_dict(),
            'correlation': df[numeric_cols].corr().to_dict()
        }
    
    # 시각화 생성
    if level in ['beginner', 'all']:
        report['visualizations']['beginner'] = plot_research_methodology(df)
    
    if level in ['intermediate', 'all'] and len(numeric_cols) >= 4:
        report['visualizations']['intermediate'] = plot_factor_analysis(df)
    
    if level in ['advanced', 'all']:
        report['visualizations']['advanced'] = plot_advanced_analytics(df)
    
    # 인사이트 생성
    if len(numeric_cols) > 0:
        # 상관관계 인사이트
        corr_matrix = df[numeric_cols].corr()
        high_corr = np.where(np.abs(corr_matrix) > 0.7)
        for i, j in zip(high_corr[0], high_corr[1]):
            if i < j:
                report['insights'].append(
                    f"{corr_matrix.index[i]}와 {corr_matrix.columns[j]} 간에 강한 상관관계 ({corr_matrix.iloc[i,j]:.3f})"
                )
    
    return report