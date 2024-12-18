import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def analyze_enrollment_correlation(filtered_df):
    st.subheader("评分与选课人数关系分析")
    
    correlation = filtered_df['平均分'].corr(filtered_df['选课人数'])
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_scatter = px.scatter(
            filtered_df,
            x='选课人数',
            y='平均分',
            color='开课院系',
            size='评价人数',
            hover_data=['课程名称', '任课教师'],
            title=f"选课人数与评分关系 (相关系数: {correlation:.3f})",
            labels={
                '选课人数': '选课人数',
                '平均分': '课程评分'
            }
        )
        fig_scatter.update_layout(height=500)
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    with col2:
        bins = pd.qcut(filtered_df['选课人数'], q=5)
        grouped_stats = filtered_df.groupby(bins)['平均分'].agg([
            ('平均分数', 'mean'),
            ('课程数量', 'count'),
            ('标准差', 'std')
        ]).round(2)
        
        grouped_stats.index = [f'{int(bin.left)}-{int(bin.right)}人' for bin in grouped_stats.index]
        grouped_stats.index.name = '选课人数区间'
        
        st.subheader("分区间统计")
        st.dataframe(grouped_stats, use_container_width=True)
        
        fig_box = go.Figure()
        for bin_range in bins.unique():
            bin_data = filtered_df[bins == bin_range]['平均分']
            fig_box.add_trace(go.Box(
                y=bin_data,
                name=f'{int(bin_range.left)}-{int(bin_range.right)}人',
                boxpoints='outliers'
            ))
        
        fig_box.update_layout(
            title="不同选课人数区间的评分分布",
            xaxis_title="选课人数区间",
            yaxis_title="评分",
            height=500
        )
        st.plotly_chart(fig_box, use_container_width=True)
    
    st.subheader("大班课程(100人以上)评分TOP10")
    large_classes = filtered_df[filtered_df['选课人数'] >= 100].sort_values('平均分', ascending=False).head(10)
    st.dataframe(
        large_classes[[
            '课程名称', '任课教师', '选课人数', 
            '评价人数', '平均分', '开课院系'
        ]],
        use_container_width=True
    ) 