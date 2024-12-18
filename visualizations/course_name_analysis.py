import streamlit as st
import pandas as pd
import plotly.express as px
import jieba
import numpy as np
from collections import defaultdict
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def analyze_course_names(filtered_df):
    st.subheader("课程名称关键词分析")
    
    word_scores = defaultdict(list)
    word_counts = defaultdict(int)
    
    for name, score in zip(filtered_df['课程名称'], filtered_df['平均分']):
        words = jieba.lcut(name)
        for word in words:
            if len(word) > 1 and word not in ['导论', '概论', '基础', '研究']:
                word_scores[word].append(score)
                word_counts[word] += 1
    
    st.subheader("课程关键词词云")
    wordcloud = WordCloud(
        width=800,
        height=400,
        background_color='white',
        font_path='simhei.ttf',  # 使用支持中文的字体
        min_font_size=10,
        max_font_size=100
    )
    
    wordcloud.generate_from_frequencies(word_counts)
    
    plt.figure(figsize=(15, 8))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    st.pyplot(plt)
    
    keywords_stats = []
    for word in word_scores:
        if word_counts[word] >= 2:
            keywords_stats.append({
                '关键词': word,
                '平均分': np.mean(word_scores[word]),
                '出现次数': word_counts[word],
                '标准差': np.std(word_scores[word])
            })
    
    keywords_df = pd.DataFrame(keywords_stats)
    keywords_df = keywords_df.sort_values('平均分', ascending=False)
    
    st.subheader("关键词评分分布")
    fig = px.scatter(
        keywords_df,
        x='出现次数',
        y='平均分',
        size='出现次数',
        text='关键词',
        color='标准差',
        title="课程关键词分析",
        labels={
            '出现次数': '关键词出现次数',
            '平均分': '平均评分',
            '标准差': '评分标准差'
        }
    )
    
    fig.update_traces(textposition='top center')
    fig.update_layout(
        showlegend=True,
        height=600
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("关键词详细统计")
    st.dataframe(
        keywords_df.round(2),
        use_container_width=True
    )
    
    st.subheader("查看特定关键词的课程")
    selected_keyword = st.selectbox(
        "选择关键词查看相关课程",
        options=keywords_df['关键词'].tolist()
    )
    
    if selected_keyword:
        related_courses = filtered_df[
            filtered_df['课程名称'].str.contains(selected_keyword)
        ][['课程名称', '任课教师', '平均分', '评价人数']].sort_values('平均分', ascending=False)
        
        st.write(f'包含"{selected_keyword}"的课程：')
        st.dataframe(related_courses, use_container_width=True) 