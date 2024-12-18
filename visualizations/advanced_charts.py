import plotly.express as px
import streamlit as st
import pandas as pd
import numpy as np

def plot_3d_course_analysis(df: pd.DataFrame):
    """
    创建3D散点图展示课程评分、学分和评价人数的关系
    
    Args:
        df: 包含课程数据的DataFrame
    """
    # 数据预处理
    plot_data = df[['课程名称', '平均分', '学分', '评价人数']].copy()
    
    # 创建3D散点图
    fig = px.scatter_3d(
        plot_data,
        x='平均分',
        y='学分',
        z='评价人数',
        color='平均分',  # 使用评分作为颜色映射
        hover_data=['课程名称'],  # 悬浮显示课程名称
        title='课程评分、学分与评价人数的3D关系图',
        labels={
            '平均分': '课程评分',
            '学分': '学分',
            '评价人数': '评价人数'
        },
        color_continuous_scale='viridis'
    )
    
    # 自定义图表布局
    fig.update_layout(
        scene=dict(
            xaxis_title='课程评分',
            yaxis_title='学分',
            zaxis_title='评价人数'
        ),
        width=800,
        height=600,
    )
    
    # 在Streamlit中显示图表
    st.plotly_chart(fig, use_container_width=True)
    
    # 添加交互说明
    with st.expander("📊 图表交互说明"):
        st.markdown("""
        - 鼠标拖动可旋转3D视图
        - 双击可重置视图
        - 滚轮可缩放视图
        - 悬停在点上可查看详细信息
        - 右上角工具栏提供更多交互选项
        """)
        
    # 添加数据分析解释
    with st.expander("📈 数据分析解释"):
        # 计算相关系数
        corr_score_credit = df['平均分'].corr(df['学分'])
        corr_score_enrollment = df['平均分'].corr(df['评价人数'])
        corr_credit_enrollment = df['学分'].corr(df['评价人数'])
        
        st.markdown(f"""
        ### 相关性分析
        - 课程评分与学分的相关系数: {corr_score_credit:.3f}
        - 课程评分与评价人数的相关系数: {corr_score_enrollment:.3f}
        - 学分与评价人数的相关系数: {corr_credit_enrollment:.3f}
        """)

def plot_teacher_ranking(df: pd.DataFrame):
    """
    创建教师课程平均分排名图表
    
    Args:
        df: 包含课程数据的DataFrame
    """
    st.subheader("教师课程平均分排名")
    
    # 计算每个教师的统计数据
    teacher_stats = df.groupby('任课教师').\
        agg({
            '平均分': ['mean', 'count'],  # 计算平均分的平均值和课程数量
            '评价人数': 'sum'  # 总评价人数
        }).round(2)
    
    # 重命名列
    teacher_stats.columns = ['平均评分', '授课数量', '总评价人数']
    teacher_stats = teacher_stats.reset_index()
    
    # 按平均评分排序并取前30名
    top_teachers = teacher_stats.nlargest(30, '平均评分')
    
    # 创建条形图
    fig = px.bar(
        top_teachers,
        x='任课教师',
        y='平均评分',
        color='授课数量',  # 用授课数量作为颜色
        hover_data=['总评价人数', '授课数量'],  # 悬浮显示详细信息
        title='教师课程平均分TOP30',
        labels={
            '任课教师': '教师姓名',
            '平均评分': '课程平均分',
            '授课数量': '授课课程数',
            '总评价人数': '总评价人数'
        },
        color_continuous_scale='Viridis'
    )
    
    # 自定义图表布局
    fig.update_layout(
        xaxis_tickangle=-45,  # 斜着显示教师名字
        showlegend=True,
        height=600
    )
    
    # 添加数值标签
    fig.update_traces(
        texttemplate='%{y:.2f}',
        textposition='outside'
    )
    
    # 显示图表
    st.plotly_chart(fig, use_container_width=True)
    
    # 显示详细数据表格
    with st.expander("📊 查看详细数据"):
        # 添加排名列
        top_teachers['排名'] = range(1, len(top_teachers) + 1)
        # 重排列顺序
        display_cols = ['排名', '任课教师', '平均评分', '授课数量', '总评价人数']
        st.dataframe(
            top_teachers[display_cols].set_index('排名'),
            use_container_width=True
        )
    
    # 添加统计信息
    with st.expander("📈 统计信息"):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("总教师数", len(teacher_stats))
        with col2:
            st.metric("平均授课数量", f"{teacher_stats['授课数量'].mean():.1f}")
        with col3:
            st.metric("平均评分中位数", f"{teacher_stats['平均评分'].median():.2f}")
