import plotly.graph_objects as go
import plotly.io as pio

# 定义统一的颜色方案
COLORS = {
    'primary': '#1f77b4',     # 主要颜色
    'secondary': '#ff7f0e',   # 次要颜色
    'background': '#ffffff',  # 背景色
    'text': '#000000',       # 文字颜色
    'grid': '#e6e6e6',       # 网格线颜色
}

# 定义统一的字体
FONTS = {
    'family': 'Arial, sans-serif',
    'size': 12,
}

# 创建统一的图表模板
def create_template():
    template = go.layout.Template()
    
    # 基础布局设置
    template.layout = dict(
        font=FONTS,
        paper_bgcolor=COLORS['background'],
        plot_bgcolor=COLORS['background'],
        title=dict(
            font=dict(
                family=FONTS['family'],
                size=FONTS['size'] + 4,
                color=COLORS['text']
            ),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            gridcolor=COLORS['grid'],
            linecolor=COLORS['text'],
            linewidth=1,
            showgrid=True,
            zeroline=False,
            zerolinecolor=COLORS['grid'],
            tickfont=dict(
                family=FONTS['family'],
                size=FONTS['size'],
                color=COLORS['text']
            ),
            title=dict(
                font=dict(
                    family=FONTS['family'],
                    size=FONTS['size'],
                    color=COLORS['text']
                )
            )
        ),
        yaxis=dict(
            gridcolor=COLORS['grid'],
            linecolor=COLORS['text'],
            linewidth=1,
            showgrid=True,
            zeroline=False,
            zerolinecolor=COLORS['grid'],
            tickfont=dict(
                family=FONTS['family'],
                size=FONTS['size'],
                color=COLORS['text']
            ),
            title=dict(
                font=dict(
                    family=FONTS['family'],
                    size=FONTS['size'],
                    color=COLORS['text']
                )
            )
        ),
        legend=dict(
            font=dict(
                family=FONTS['family'],
                size=FONTS['size'],
                color=COLORS['text']
            ),
            bgcolor=COLORS['background'],
            bordercolor=COLORS['grid'],
            borderwidth=1
        ),
        margin=dict(l=10, r=10, t=40, b=10),
        hoverlabel=dict(
            font=dict(
                family=FONTS['family'],
                size=FONTS['size'],
                color=COLORS['background']
            ),
            bgcolor=COLORS['text']
        )
    )
    
    return template

# 设置默认模板
def set_default_theme():
    template = create_template()
    pio.templates['custom_theme'] = template
    pio.templates.default = 'custom_theme'

# 获取主题颜色
def get_theme_colors(n_colors=1):
    """获取主题颜色列表"""
    color_sequence = [
        '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
        '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'
    ]
    return color_sequence[:n_colors] if n_colors > 1 else color_sequence[0]
