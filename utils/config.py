import streamlit as st
import pandas as pd

def setup_page():
    st.set_page_config(
        page_title="复旦大学课程评价分析", 
        layout="wide",
        initial_sidebar_state="expanded"
    )
    st.title("复旦大学课程评价数据分析大屏")

@st.cache_data
def load_data(filename):
    if filename == "all":
        # 加载所有学期的数据并合并
        semester_files = [
            "2023_3.csv", "2023_2.csv", "2023_1.csv",
            "2022_3.csv", "2022_2.csv", "2022_1.csv"
        ]
        dfs = []
        for file in semester_files:
            try:
                df = pd.read_csv(f'dataset/{file}')
                df['学期'] = file.replace('.csv', '')  # 添加学期标识
                dfs.append(df)
            except FileNotFoundError:
                st.warning(f"文件 {file} 不存在")
        return pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()
    else:
        return pd.read_csv(f'dataset/{filename}')

def create_sidebar_filters(df):
    st.sidebar.title("筛选条件")
    
    # 添加学期选择
    semester_files = {
        "全部学期": "all",
        "2023-2024-3": "2023_3.csv",
        "2023-2024-2": "2023_2.csv",
        "2023-2024-1": "2023_1.csv",
        "2022-2023-3": "2022_3.csv",
        "2022-2023-2": "2022_2.csv",
        "2022-2023-1": "2022_1.csv"
    }
    selected_semester = st.sidebar.selectbox(
        "选择学期",
        options=list(semester_files.keys()),
        index=0
    )
    
    st.sidebar.markdown("---")  # 添加分隔线
    
    # 院系筛选
    st.sidebar.subheader("院系筛选")
    departments = sorted(df['开课院系'].unique())
    select_all = st.sidebar.checkbox("选择所有院系", value=True)
    
    if select_all:
        selected_dept = departments
    else:
        selected_dept = st.sidebar.multiselect(
            '选择院系', 
            departments,
            default=departments[0] if not select_all else []
        )
        if not selected_dept:
            selected_dept = [departments[0]]
    
    st.sidebar.markdown("---")
    
    # 课程特征筛选
    st.sidebar.subheader("课程特征")
    
    # 学分范围
    credit_range = st.sidebar.slider(
        "学分范围",
        min_value=float(df['学分'].min()),
        max_value=float(df['学分'].max()),
        value=(float(df['学分'].min()), float(df['学分'].max())),
        step=0.5
    )
    
    # 评分范围
    score_range = st.sidebar.slider(
        "评分范围",
        min_value=float(df['平均分'].min()),
        max_value=float(df['平均分'].max()),
        value=(float(df['平均分'].min()), float(df['平均分'].max())),
        step=1.0
    )
    
    # 选课人数范围
    enrollment_range = st.sidebar.slider(
        "选课人数范围",
        min_value=int(df['选课人数'].min()),
        max_value=int(df['选课人数'].max()),
        value=(int(df['选课人数'].min()), int(df['选课人数'].max())),
        step=1
    )
    
    st.sidebar.markdown("---")
    
    # 课程类型筛选（根据课程编码前缀）
    st.sidebar.subheader("课程类型")
    course_types = sorted(df['课程编码'].apply(lambda x: x[:4]).unique())
    selected_course_types = st.sidebar.multiselect(
        '课程类型（根据编码前缀）',
        course_types,
        default=course_types
    )
    
    # 评价数据筛选
    st.sidebar.subheader("评价数据要求")
    min_reviews = st.sidebar.number_input(
        "最少评价人数",
        min_value=1,
        max_value=int(df['评价人数'].max()),
        value=1
    )
    
    return (
        selected_semester,
        semester_files[selected_semester],
        selected_dept,
        credit_range,
        score_range,
        enrollment_range,
        selected_course_types,
        min_reviews
    )

def filter_data(df, selected_dept, credit_range, score_range, enrollment_range, selected_course_types, min_reviews):
    """根据筛选条件过滤数据"""
    return df[
        (df['开课院系'].isin(selected_dept)) &
        (df['学分'].between(credit_range[0], credit_range[1])) &
        (df['平均分'].between(score_range[0], score_range[1])) &
        (df['选课人数'].between(enrollment_range[0], enrollment_range[1])) &
        (df['课程编码'].apply(lambda x: x[:4]).isin(selected_course_types)) &
        (df['评价人数'] >= min_reviews)
    ]

def show_metrics(filtered_df):
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("平均评分", f"{filtered_df['平均分'].mean():.2f}")
    with col2:
        st.metric("课程数量", len(filtered_df['课程名称'].unique()))
    with col3:
        st.metric("教师数量", len(filtered_df['任课教师'].unique()))
    with col4:
        st.metric("参评人数", filtered_df['评价人数'].sum()) 