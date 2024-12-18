import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils.chart_components import show_chart_with_fullscreen

def plot_top_courses(filtered_df):
    """绘制课程评分TOP 10"""
    st.subheader("最受欢迎课程排名")
    top_courses = filtered_df.groupby('课程名称')[['平均分', '评价人数']].agg({
        '平均分': 'mean',
        '评价人数': 'sum'
    }).sort_values('平均分', ascending=False).head(10)
    
    fig = px.bar(
        top_courses,
        y=top_courses.index,
        x='平均分',
        orientation='h',
        text='平均分',
        color='评价人数'
    )
    fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    fig.update_layout(
        title=None,
        margin=dict(t=20)
    )
    st.plotly_chart(fig, use_container_width=True)

def plot_teacher_scores(filtered_df):
    """绘制教师评分分布"""
    st.subheader("教师评分箱线图")
    fig = go.Figure()
    fig.add_trace(go.Box(
        y=filtered_df['平均分'],
        x=filtered_df['任课教师'],
        name='教师评分'
    ))
    fig.update_layout(
        title=None,
        margin=dict(t=20),
        xaxis_title="教师",
        yaxis_title="评分"
    )
    st.plotly_chart(fig, use_container_width=True)

def plot_credit_score_relation(filtered_df):
    """绘制学分与评分关系图"""
    st.subheader("学分-评分散点图")
    fig = px.scatter(
        filtered_df,
        x='学分',
        y='平均分',
        size='评价人数',
        color='开课院系',
        hover_data=['课程名称', '任课教师']
    )
    fig.update_layout(
        title=None,
        margin=dict(t=20)
    )
    st.plotly_chart(fig, use_container_width=True)

def plot_score_distribution(filtered_df):
    """绘制评分分布图"""
    st.subheader("评分分布直方图")
    fig = px.histogram(
        filtered_df,
        x='平均分',
        nbins=30,
        color='开课院系'
    )
    fig.update_layout(
        title=None,
        margin=dict(t=20)
    )
    st.plotly_chart(fig, use_container_width=True)

def plot_department_comparison(df):
    """绘制院系平均分对比图"""
    st.subheader("各院系课程平均分对比")
    dept_scores = df.groupby('开课院系')['平均分'].agg(['mean', 'count']).reset_index()
    dept_scores.columns = ['开课院系', '平均分', '课程数量']
    dept_scores = dept_scores.sort_values('平均分', ascending=True)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=dept_scores['开课院系'],
        x=dept_scores['平均分'],
        orientation='h',
        text=dept_scores.apply(lambda x: f"平均分: {x['平均分']:.2f}<br>课程数: {int(x['课程数量'])}", axis=1),
        hoverinfo='text',
        marker_color='#1f77b4'
    ))
    
    fig.update_layout(
        title=None,
        margin=dict(t=20),
        xaxis_title='平均分',
        yaxis_title='开课院系',
        height=max(400, len(dept_scores) * 25),  # 根据院系数量动态调整高度
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)

def plot_course_flow(filtered_df):
    """绘制学生选课流向桑基图"""
    st.subheader("学生选课流向")
    
    # 准备桑基图数据
    flow_data = filtered_df.groupby(['开课院系', '课程名称'])['选课人数'].sum().reset_index()
    
    # 创建节点标签的映射
    departments = list(flow_data['开课院系'].unique())
    courses = list(flow_data['课程名称'].unique())
    
    # 创建节点索引
    dept_to_index = {dept: i for i, dept in enumerate(departments)}
    course_to_index = {course: i + len(departments) for i, course in enumerate(courses)}
    
    # 准备桑基图数据
    source = [dept_to_index[row['开课院系']] for _, row in flow_data.iterrows()]
    target = [course_to_index[row['课程名称']] for _, row in flow_data.iterrows()]
    value = flow_data['选课人数'].tolist()
    
    # 创建节点标签
    labels = departments + courses
    
    # 创建颜色映射
    colors = px.colors.qualitative.Set3 * (len(labels) // len(px.colors.qualitative.Set3) + 1)
    node_colors = colors[:len(labels)]
    
    # 创建桑基图
    fig = go.Figure(data=[go.Sankey(
        node = dict(
            pad = 15,
            thickness = 20,
            line = dict(color = "black", width = 0.5),
            label = labels,
            color = node_colors
        ),
        link = dict(
            source = source,
            target = target,
            value = value
        )
    )])
    
    # 更新布局
    fig.update_layout(
        title=None,
        margin=dict(t=20),
        height=800  # 增加图表高度以便更好地显示
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_detailed_table(filtered_df):
    """显示课程详细数据表格"""
    st.subheader("课程详细数据")
    st.dataframe(
        filtered_df[
            ['课程名称', '任课教师', '学分', 
             '选课人数', '评价人数', '平均分', '中位数']
        ].sort_values('平均分', ascending=False),
        use_container_width=True
    )