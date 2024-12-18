import streamlit as st

def show_chart_with_fullscreen(fig, title=None, key=None):
    """显示带有全屏功能的图表组件"""
    # 创建唯一的图表ID
    chart_id = f"chart_{abs(hash(str(fig)))}"
    
    # 添加全屏按钮的CSS样式
    st.markdown("""
        <style>
        .chart-container {
            position: relative;
            width: 100%;
            margin-bottom: 1rem;
        }
        .fullscreen-button {
            position: absolute;
            top: 10px;
            right: 10px;
            z-index: 999;
            background-color: rgba(255, 255, 255, 0.9);
            border: 1px solid #ddd;
            border-radius: 4px;
            padding: 5px 10px;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 5px;
        }
        .fullscreen-button:hover {
            background-color: #ffffff;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .fullscreen-chart {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        </style>
    """, unsafe_allow_html=True)
    
    # 添加全屏切换的JavaScript代码
    js_code = f"""
    <div class="chart-container" id="{chart_id}_container">
        <button class="fullscreen-button" onclick="toggleFullscreen_{chart_id}()">
            <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
                <path d="M1.5 1a.5.5 0 0 0-.5.5v4a.5.5 0 0 1-1 0v-4A1.5 1.5 0 0 1 1.5 0h4a.5.5 0 0 1 0 1h-4zM10 .5a.5.5 0 0 1 .5-.5h4A1.5 1.5 0 0 1 16 1.5v4a.5.5 0 0 1-1 0v-4a.5.5 0 0 0-.5-.5h-4a.5.5 0 0 1-.5-.5zM.5 10a.5.5 0 0 1 .5.5v4a.5.5 0 0 0 .5.5h4a.5.5 0 0 1 0 1h-4A1.5 1.5 0 0 1 0 14.5v-4a.5.5 0 0 1 .5-.5zm15 0a.5.5 0 0 1 .5.5v4a1.5 1.5 0 0 1-1.5 1.5h-4a.5.5 0 0 1 0-1h4a.5.5 0 0 0 .5-.5v-4a.5.5 0 0 1 .5-.5z"/>
            </svg>
            全屏
        </button>
        <div class="fullscreen-chart">
            {f'<h3>{title}</h3>' if title else ''}
            <div id="{chart_id}"></div>
        </div>
    </div>
    <script>
        function toggleFullscreen_{chart_id}() {{
            var container = document.getElementById("{chart_id}_container");
            if (!document.fullscreenElement) {{
                if (container.requestFullscreen) {{
                    container.requestFullscreen();
                }} else if (container.webkitRequestFullscreen) {{
                    container.webkitRequestFullscreen();
                }} else if (container.msRequestFullscreen) {{
                    container.msRequestFullscreen();
                }}
            }} else {{
                if (document.exitFullscreen) {{
                    document.exitFullscreen();
                }} else if (document.webkitExitFullscreen) {{
                    document.webkitExitFullscreen();
                }} else if (document.msExitFullscreen) {{
                    document.msExitFullscreen();
                }}
            }}
        }}
        
        document.addEventListener('fullscreenchange', function() {{
            var container = document.getElementById("{chart_id}_container");
            if (document.fullscreenElement === container) {{
                container.style.background = 'white';
                container.style.padding = '20px';
            }} else {{
                container.style.background = 'none';
                container.style.padding = '0';
            }}
        }});
    </script>
    """
    
    # 显示HTML和图表
    st.markdown(js_code, unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True, key=key if key else chart_id)
