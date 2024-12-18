import streamlit as st

def show_top_banner(filtered_df):
    """显示顶部导航栏和KPI指标"""
    # 添加自定义CSS样式
    st.markdown("""
        <style>
        .top-banner {
            padding: 1rem;
            background-color: #f0f2f6;
            border-radius: 0.5rem;
            margin-bottom: 2rem;
        }
        .metric-card {
            background-color: white;
            padding: 1rem;
            border-radius: 0.5rem;
            margin: 0.5rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.12);
            text-align: center;
        }
        .metric-value {
            font-size: 24px;
            font-weight: bold;
            color: #1f77b4;
        }
        .metric-label {
            font-size: 14px;
            color: #666;
            margin-top: 5px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="top-banner">', unsafe_allow_html=True)
    
    # 显示关键指标
    col1, col2, col3, col4 = st.columns(4)
    
    metrics = [
        {
            "label": "平均评分",
            "value": f"{filtered_df['平均分'].mean():.2f}",
            "delta": None,
            "column": col1
        },
        {
            "label": "课程数量",
            "value": len(filtered_df['课程名称'].unique()),
            "delta": None,
            "column": col2
        },
        {
            "label": "教师数量",
            "value": len(filtered_df['任课教师'].unique()),
            "delta": None,
            "column": col3
        },
        {
            "label": "总参评人数",
            "value": f"{filtered_df['评价人数'].sum():,}",
            "delta": None,
            "column": col4
        }
    ]
    
    for metric in metrics:
        with metric["column"]:
            st.markdown(f'''
                <div class="metric-card">
                    <div class="metric-value">{metric["value"]}</div>
                    <div class="metric-label">{metric["label"]}</div>
                </div>
            ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
