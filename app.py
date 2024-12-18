import streamlit as st
from utils.config import setup_page, load_data, create_sidebar_filters, filter_data
from utils.components import show_top_banner
from visualizations.basic_charts import (
    plot_top_courses, plot_teacher_scores, 
    plot_credit_score_relation, plot_score_distribution, 
    plot_department_comparison,
    show_detailed_table,
    plot_course_flow
)
from visualizations.course_name_analysis import analyze_course_names
from visualizations.enrollment_analysis import analyze_enrollment_correlation
from visualizations.advanced_charts import plot_3d_course_analysis, plot_teacher_ranking

def main():
    setup_page()
    # 初始加载全部数据
    selected_semester, semester_file, selected_dept, credit_range, score_range, enrollment_range, selected_course_types, min_reviews = create_sidebar_filters(load_data("all"))
    df = load_data(semester_file)
    filtered_df = filter_data(df, selected_dept, credit_range, score_range, enrollment_range, selected_course_types, min_reviews)
    
    # 显示顶部导航栏和KPI指标
    show_top_banner(filtered_df)
    
    tab1, tab2, tab3 = st.tabs(["基础分析", "课程名称分析", "选课人数分析"])
    
    with tab1:
        # 院系评分对比
        plot_department_comparison(filtered_df)
        
        # 3D课程分析图表
        plot_3d_course_analysis(filtered_df)
        
        # 教师课程平均分排名
        plot_teacher_ranking(filtered_df)
        
        # 第一行：课程TOP10和教师评分
        col1, col2 = st.columns(2)
        with col1:
            plot_top_courses(filtered_df)
        with col2:
            plot_teacher_scores(filtered_df)
        
        # 第二行：学分-评分关系和评分分布
        col3, col4 = st.columns(2)
        with col3:
            plot_credit_score_relation(filtered_df)
        with col4:
            plot_score_distribution(filtered_df)
        
        # 添加桑基图（占据整行）
        plot_course_flow(filtered_df)
        
        # 详细数据表格
        show_detailed_table(filtered_df)
    
    with tab2:
        analyze_course_names(filtered_df)
    
    with tab3:
        analyze_enrollment_correlation(filtered_df)

if __name__ == "__main__":
    main()