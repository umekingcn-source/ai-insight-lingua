import streamlit as st
import feedparser
import google.generativeai as genai
import pandas as pd
import datetime
import time

# --- 配置页面 ---
st.set_page_config(
    page_title="AI Insight & Lingua", 
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 自定义样式 (参考 U-MEKING 风格) ---
st.markdown("""
<style>
/* 导入 Google Fonts - 参考 U-MEKING 清晰现代的字体 */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=DM+Sans:wght@400;500;600;700&display=swap');

/* 全局字体和颜色设置 */
html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    color: #ffffff;
}

/* 全局样式 - 深色优雅背景 */
.stApp {
    background: linear-gradient(180deg, #0f0f0f 0%, #1a1a1a 50%, #0f0f0f 100%);
}

/* 确保所有文字清晰可见 */
.stMarkdown, .stMarkdown p, .stMarkdown li, .stMarkdown span {
    color: #f0f0f0 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 1rem;
    line-height: 1.7;
}

/* 主标题样式 - 金色渐变 */
.main-header {
    background: linear-gradient(135deg, #d4af37 0%, #f4e4bc 25%, #d4af37 50%, #aa8c2c 75%, #d4af37 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-family: 'DM Sans', sans-serif;
    font-size: 2.5rem;
    font-weight: 700;
    text-align: center;
    margin-bottom: 0.5rem;
    letter-spacing: 1px;
}

/* 副标题样式 - 更清晰 */
.sub-header {
    color: #e0e0e0 !important;
    font-family: 'Inter', sans-serif;
    font-size: 1.1rem;
    text-align: center;
    margin-bottom: 2rem;
    letter-spacing: 0.5px;
    font-weight: 400;
}

/* 卡片样式 - 深色玻璃态 */
.news-card {
    background: linear-gradient(145deg, rgba(30, 30, 30, 0.95), rgba(20, 20, 20, 0.98));
    border-radius: 12px;
    padding: 1.5rem;
    margin: 1rem 0;
    border: 1px solid rgba(212, 175, 55, 0.25);
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.news-card:hover {
    transform: translateY(-3px);
    border-color: rgba(212, 175, 55, 0.5);
    box-shadow: 0 15px 50px rgba(212, 175, 55, 0.1);
}

/* 特色区块 - 金色边框 */
.feature-box {
    background: linear-gradient(135deg, rgba(212, 175, 55, 0.08), rgba(170, 140, 44, 0.05));
    border-radius: 12px;
    padding: 1.5rem;
    margin: 1rem 0;
    border-left: 3px solid #d4af37;
    backdrop-filter: blur(10px);
}

.feature-box p, .feature-box li {
    color: #e0e0e0 !important;
    font-size: 1rem;
}

/* 成就徽章 - 金色主题 */
.achievement-badge {
    background: linear-gradient(135deg, #d4af37, #aa8c2c);
    color: #0a0a0a;
    padding: 0.4rem 1rem;
    border-radius: 20px;
    font-weight: 600;
    display: inline-block;
    margin: 0.25rem;
    font-size: 0.85rem;
    font-family: 'Inter', sans-serif;
}

/* 统计卡片 */
.stat-card {
    background: linear-gradient(145deg, rgba(212, 175, 55, 0.12), rgba(170, 140, 44, 0.08));
    border-radius: 12px;
    padding: 1.2rem;
    text-align: center;
    border: 1px solid rgba(212, 175, 55, 0.25);
}

.stat-number {
    font-size: 2.2rem;
    font-weight: 700;
    font-family: 'DM Sans', sans-serif;
    background: linear-gradient(135deg, #d4af37, #f4e4bc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.stat-label {
    color: #d0d0d0 !important;
    font-size: 0.9rem;
    margin-top: 0.5rem;
    font-family: 'Inter', sans-serif;
    font-weight: 500;
}

/* 按钮样式 - 金色优雅 */
.stButton > button {
    background: linear-gradient(135deg, #d4af37 0%, #aa8c2c 100%);
    color: #0a0a0a !important;
    border: none;
    border-radius: 8px;
    padding: 0.75rem 2rem;
    font-weight: 600;
    font-family: 'Inter', sans-serif;
    transition: all 0.3s ease;
    box-shadow: 0 4px 20px rgba(212, 175, 55, 0.3);
    text-transform: uppercase;
    letter-spacing: 1px;
    font-size: 0.9rem;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 30px rgba(212, 175, 55, 0.4);
    color: #0a0a0a !important;
}

/* 侧边栏样式 */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #111111 0%, #1a1a1a 100%);
    border-right: 1px solid rgba(212, 175, 55, 0.15);
}

[data-testid="stSidebar"] .stMarkdown {
    color: #f0f0f0 !important;
}

[data-testid="stSidebar"] h4 {
    color: #d4af37 !important;
    font-family: 'DM Sans', sans-serif;
    font-weight: 600;
}

/* 输入框样式 */
.stTextInput > div > div > input {
    background: rgba(30, 30, 30, 0.95) !important;
    border: 1px solid rgba(212, 175, 55, 0.35) !important;
    border-radius: 8px;
    color: #ffffff !important;
    font-family: 'Inter', sans-serif;
    font-size: 1rem;
}

.stTextInput > div > div > input:focus {
    border-color: #d4af37 !important;
    box-shadow: 0 0 10px rgba(212, 175, 55, 0.25);
}

.stTextInput > div > div > input::placeholder {
    color: #888888 !important;
}

.stTextArea > div > div > textarea {
    background: rgba(30, 30, 30, 0.95) !important;
    border: 1px solid rgba(212, 175, 55, 0.35) !important;
    border-radius: 8px;
    color: #ffffff !important;
    font-family: 'Inter', sans-serif;
    font-size: 1rem;
}

.stTextArea > div > div > textarea:focus {
    border-color: #d4af37 !important;
    box-shadow: 0 0 10px rgba(212, 175, 55, 0.25);
}

.stTextArea > div > div > textarea::placeholder {
    color: #888888 !important;
}

/* 选择框样式 */
.stSelectbox > div > div {
    background: rgba(30, 30, 30, 0.95) !important;
    border: 1px solid rgba(212, 175, 55, 0.35) !important;
    border-radius: 8px;
}

.stSelectbox > div > div > div {
    color: #ffffff !important;
}

/* Tab 样式 */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: rgba(20, 20, 20, 0.9);
    border-radius: 10px;
    padding: 0.5rem;
    border: 1px solid rgba(212, 175, 55, 0.15);
}

.stTabs [data-baseweb="tab"] {
    border-radius: 6px;
    color: #d0d0d0 !important;
    font-weight: 500;
    font-family: 'Inter', sans-serif;
    font-size: 1rem;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #d4af37, #aa8c2c) !important;
    color: #0a0a0a !important;
}

/* Expander 样式 - 整体容器 */
[data-testid="stExpander"] {
    background: transparent !important;
    border: none !important;
}

/* Expander 头部/摘要部分 */
[data-testid="stExpander"] > details {
    background: rgba(30, 30, 30, 0.9) !important;
    border-radius: 8px !important;
    border: 1px solid rgba(212, 175, 55, 0.25) !important;
    overflow: hidden;
}

[data-testid="stExpander"] > details:hover {
    border-color: rgba(212, 175, 55, 0.5) !important;
}

/* Expander 摘要/标题行 */
[data-testid="stExpander"] > details > summary {
    background: rgba(30, 30, 30, 0.9) !important;
    padding: 1rem 1.2rem !important;
    cursor: pointer;
    display: flex !important;
    align-items: center !important;
    gap: 0.5rem !important;
}

/* 确保展开箭头正常显示 */
[data-testid="stExpander"] > details > summary > span:first-child {
    flex-shrink: 0;
    display: flex;
    align-items: center;
}

/* Expander 标题文字 - 修复重叠问题 */
[data-testid="stExpander"] > details > summary > span:last-child,
[data-testid="stExpander"] > details > summary > span:last-child p {
    color: #FFD700 !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    line-height: 1.5 !important;
    margin: 0 !important;
    padding: 0 !important;
    white-space: normal !important;
    word-break: break-word !important;
    overflow: visible !important;
    text-overflow: unset !important;
}

/* Expander 内容区域 */
[data-testid="stExpander"] > details > div[data-testid="stExpanderDetails"] {
    background: rgba(25, 25, 25, 0.95) !important;
    border-top: 1px solid rgba(212, 175, 55, 0.15) !important;
    padding: 1rem 1.2rem !important;
}

/* Expander 内容区域文字 */
[data-testid="stExpander"] > details > div p,
[data-testid="stExpander"] > details > div span,
[data-testid="stExpander"] > details > div li {
    color: #e8e8e8 !important;
}

/* Expander 内链接 */
[data-testid="stExpander"] a {
    color: #d4af37 !important;
    font-weight: 500;
}

[data-testid="stExpander"] a:hover {
    color: #FFD700 !important;
}

/* Metric 样式 */
[data-testid="stMetricValue"] {
    background: linear-gradient(135deg, #d4af37, #f4e4bc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 700;
    font-family: 'DM Sans', sans-serif;
}

/* 渐变分割线 - 金色 */
.gradient-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(212, 175, 55, 0.6), transparent);
    margin: 1.5rem 0;
    border: none;
}

/* 引用样式 - 更清晰 */
.quote-box {
    background: linear-gradient(135deg, rgba(212, 175, 55, 0.1), rgba(170, 140, 44, 0.08));
    border-left: 3px solid #d4af37;
    padding: 1.2rem 1.5rem;
    border-radius: 0 10px 10px 0;
    font-style: italic;
    color: #e8e8e8 !important;
    font-family: 'DM Sans', sans-serif;
    font-size: 1.1rem;
    line-height: 1.6;
}

/* 标签样式 */
.tag {
    background: rgba(212, 175, 55, 0.2);
    color: #d4af37 !important;
    padding: 0.35rem 0.9rem;
    border-radius: 15px;
    font-size: 0.85rem;
    margin-right: 0.5rem;
    display: inline-block;
    font-family: 'Inter', sans-serif;
    font-weight: 600;
    border: 1px solid rgba(212, 175, 55, 0.4);
}

/* 品牌 Logo 区域 */
.brand-logo {
    text-align: center;
    padding: 1.5rem 0;
}

.brand-icon {
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
    filter: drop-shadow(0 0 10px rgba(212, 175, 55, 0.5));
}

.brand-title {
    background: linear-gradient(135deg, #d4af37, #f4e4bc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-family: 'DM Sans', sans-serif;
    font-size: 1.5rem;
    font-weight: 700;
    letter-spacing: 3px;
    margin: 0;
}

.brand-subtitle {
    color: #a0a0a0 !important;
    font-size: 0.8rem;
    font-family: 'Inter', sans-serif;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-top: 0.3rem;
}

/* 特性图标卡片 */
.feature-icon-card {
    background: linear-gradient(145deg, rgba(30, 30, 30, 0.95), rgba(20, 20, 20, 0.98));
    border-radius: 12px;
    padding: 1.5rem;
    text-align: center;
    border: 1px solid rgba(212, 175, 55, 0.2);
    transition: all 0.3s ease;
}

.feature-icon-card:hover {
    border-color: rgba(212, 175, 55, 0.5);
    transform: translateY(-3px);
}

.feature-icon {
    font-size: 2rem;
    margin-bottom: 0.8rem;
}

.feature-title {
    color: #d4af37 !important;
    font-family: 'DM Sans', sans-serif;
    font-weight: 600;
    font-size: 1.1rem;
    margin-bottom: 0.5rem;
}

.feature-desc {
    color: #d0d0d0 !important;
    font-size: 0.95rem;
    font-family: 'Inter', sans-serif;
    line-height: 1.6;
}

/* 底部信息 */
.footer-text {
    text-align: center;
    color: #a0a0a0 !important;
    font-size: 0.9rem;
    font-family: 'Inter', sans-serif;
    letter-spacing: 0.5px;
}

.footer-text strong {
    color: #d4af37 !important;
}

/* 进度条颜色 */
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #d4af37, #aa8c2c);
}

/* 滚动条样式 */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: #0f0f0f;
}

::-webkit-scrollbar-thumb {
    background: rgba(212, 175, 55, 0.4);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: rgba(212, 175, 55, 0.6);
}

/* 信息提示框 */
.stAlert {
    background: rgba(30, 30, 30, 0.95) !important;
    border: 1px solid rgba(212, 175, 55, 0.25);
    border-radius: 8px;
    color: #f0f0f0 !important;
}

.stAlert p,
.stAlert span,
.stAlert div,
[data-testid="stAlert"] p,
[data-testid="stAlert"] span {
    color: #e8e8e8 !important;
    font-family: 'Inter', sans-serif !important;
}

/* st.info 信息框 */
[data-baseweb="notification"] {
    background: rgba(30, 30, 30, 0.95) !important;
    border-left: 4px solid #d4af37 !important;
}

[data-baseweb="notification"] div {
    color: #e8e8e8 !important;
}

/* 链接样式 */
a {
    color: #d4af37 !important;
    text-decoration: none;
    transition: color 0.3s ease;
}

a:hover {
    color: #f4e4bc !important;
}

/* 标签文字 */
label {
    color: #e0e0e0 !important;
    font-family: 'Inter', sans-serif;
    font-weight: 500;
}

/* Spinner 文字 */
.stSpinner > div {
    color: #d4af37 !important;
}

/* 警告框文字 */
.stWarning {
    color: #f0f0f0 !important;
}

/* Hero 横幅区域 */
.hero-section {
    position: relative;
    background: url('https://images.unsplash.com/photo-1620712943543-bcc4688e7485?w=1600&h=400&fit=crop') center/cover no-repeat;
    border-radius: 16px;
    padding: 3rem 2rem;
    margin-bottom: 2rem;
    overflow: hidden;
    border: 1px solid rgba(212, 175, 55, 0.3);
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
}

.hero-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(135deg, rgba(15, 15, 15, 0.85) 0%, rgba(26, 26, 26, 0.75) 50%, rgba(15, 15, 15, 0.85) 100%);
    z-index: 1;
}

.hero-content {
    position: relative;
    z-index: 2;
    text-align: center;
}

/* 装饰图片 */
.decorative-img {
    border-radius: 12px;
    overflow: hidden;
    border: 2px solid rgba(212, 175, 55, 0.3);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
    transition: all 0.3s ease;
}

.decorative-img:hover {
    transform: scale(1.02);
    border-color: rgba(212, 175, 55, 0.6);
}

.decorative-img img {
    width: 100%;
    height: auto;
    display: block;
    filter: brightness(0.9);
    transition: filter 0.3s ease;
}

.decorative-img:hover img {
    filter: brightness(1);
}

/* 引用框图标 */
.quote-icon {
    font-size: 2rem;
    margin-right: 1rem;
    vertical-align: middle;
}

/* 特性卡片带图片 */
.feature-card-with-img {
    background: linear-gradient(145deg, rgba(30, 30, 30, 0.95), rgba(20, 20, 20, 0.98));
    border-radius: 16px;
    overflow: hidden;
    border: 1px solid rgba(212, 175, 55, 0.2);
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4);
}

.feature-card-with-img:hover {
    transform: translateY(-5px);
    border-color: rgba(212, 175, 55, 0.5);
    box-shadow: 0 20px 60px rgba(212, 175, 55, 0.15);
}

.feature-card-img {
    width: 100%;
    height: 120px;
    object-fit: cover;
    filter: brightness(0.8);
    transition: filter 0.3s ease;
}

.feature-card-with-img:hover .feature-card-img {
    filter: brightness(1);
}

.feature-card-content {
    padding: 1.2rem;
    text-align: center;
}

/* 侧边栏图片 */
.sidebar-image {
    border-radius: 12px;
    overflow: hidden;
    margin: 1rem 0;
    border: 1px solid rgba(212, 175, 55, 0.3);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
}

.sidebar-image img {
    width: 100%;
    height: auto;
    display: block;
}

/* 新闻配图 */
.news-image {
    width: 100%;
    height: 180px;
    object-fit: cover;
    border-radius: 10px;
    margin-bottom: 1rem;
    border: 1px solid rgba(212, 175, 55, 0.2);
}

/* 浮动装饰元素 */
.floating-decoration {
    position: fixed;
    width: 300px;
    height: 300px;
    background: radial-gradient(circle, rgba(212, 175, 55, 0.08) 0%, transparent 70%);
    border-radius: 50%;
    pointer-events: none;
    z-index: -1;
}

.floating-decoration.top-right {
    top: 10%;
    right: -100px;
    animation: float 6s ease-in-out infinite;
}

.floating-decoration.bottom-left {
    bottom: 10%;
    left: -100px;
    animation: float 8s ease-in-out infinite reverse;
}

@keyframes float {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-20px); }
}

/* Tab 面板图片横幅 */
.tab-banner {
    width: 100%;
    height: 150px;
    background-size: cover;
    background-position: center;
    border-radius: 12px;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
    border: 1px solid rgba(212, 175, 55, 0.2);
}

.tab-banner::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(90deg, rgba(15, 15, 15, 0.9) 0%, rgba(15, 15, 15, 0.3) 100%);
}

.tab-banner-content {
    position: relative;
    z-index: 1;
    padding: 1.5rem;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.tab-banner-title {
    color: #d4af37 !important;
    font-family: 'DM Sans', sans-serif;
    font-size: 1.5rem;
    font-weight: 700;
    margin: 0;
}

.tab-banner-subtitle {
    color: #e0e0e0 !important;
    font-family: 'Inter', sans-serif;
    font-size: 0.95rem;
    margin-top: 0.5rem;
}

/* 图片画廊样式 */
.image-gallery {
    display: flex;
    gap: 1rem;
    margin: 1rem 0;
}

.gallery-item {
    flex: 1;
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid rgba(212, 175, 55, 0.2);
    transition: all 0.3s ease;
}

.gallery-item:hover {
    transform: scale(1.02);
    border-color: rgba(212, 175, 55, 0.5);
}

.gallery-item img {
    width: 100%;
    height: 100px;
    object-fit: cover;
    filter: brightness(0.85);
    transition: filter 0.3s ease;
}

.gallery-item:hover img {
    filter: brightness(1);
}

/* 装饰线条 */
.decorative-line {
    height: 2px;
    background: linear-gradient(90deg, transparent, rgba(212, 175, 55, 0.5), transparent);
    margin: 2rem 0;
}

/* 侧边栏励志图片 */
.motivation-section {
    background: linear-gradient(145deg, rgba(30, 30, 30, 0.95), rgba(20, 20, 20, 0.98));
    border-radius: 12px;
    padding: 1rem;
    margin: 1rem 0;
    border: 1px solid rgba(212, 175, 55, 0.2);
}

.motivation-img {
    width: 100%;
    border-radius: 8px;
    margin-bottom: 0.8rem;
}

.motivation-text {
    color: #e0e0e0 !important;
    font-family: 'Inter', sans-serif;
    font-size: 0.85rem;
    text-align: center;
    font-style: italic;
}
</style>
""", unsafe_allow_html=True)

# 添加浮动装饰元素
st.markdown("""
<div class="floating-decoration top-right"></div>
<div class="floating-decoration bottom-left"></div>
""", unsafe_allow_html=True)

# --- 侧边栏配置 ---
with st.sidebar:
    # Logo 和标题 - U-MEKING 风格
    st.markdown("""
    <div class="brand-logo">
        <div class="brand-icon">🧠</div>
        <h2 class="brand-title">AI LINGUA</h2>
        <p class="brand-subtitle">Insight & Growth</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 侧边栏装饰图片
    st.markdown("""
    <div class="sidebar-image">
        <img src="https://images.unsplash.com/photo-1620712943543-bcc4688e7485?w=300&h=150&fit=crop" alt="AI Brain" />
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)
    
    # API Key 输入
    st.markdown("#### 🔑 API 配置")
    default_key = st.secrets.get("GEMINI_API_KEY", "")
    api_key = st.text_input("Gemini API Key", value=default_key, type="password")
    
    st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)
    
    # 今日成就
    st.markdown("#### 🏆 今日成就")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-number">3</div>
            <div class="stat-label">📖 已读新闻</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-number">12</div>
            <div class="stat-label">📚 新单词</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 成就徽章
    st.markdown("**🎖️ 获得徽章**")
    st.markdown("""
    <div>
        <span class="achievement-badge">🔥 连续3天</span>
        <span class="achievement-badge">⭐ 阅读达人</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)
    
    # 学习趋势
    st.markdown("#### 📈 本周趋势")
    chart_data = pd.DataFrame({
        'Day': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
        'Words': [10, 15, 12, 18, 8]
    })
    st.bar_chart(chart_data.set_index('Day'), color="#d4af37")
    
    st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)
    
    # 每日激励 - 带图片
    st.markdown("#### 💡 每日激励")
    st.markdown("""
    <div class="motivation-section">
        <img class="motivation-img" src="https://images.unsplash.com/photo-1488190211105-8b0e65b80b4e?w=300&h=120&fit=crop" alt="Learning" />
        <p class="motivation-text">"Stay hungry, stay foolish."<br>— Steve Jobs</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 底部信息
    st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="footer-text">
        <p>Powered by <strong>Gemini AI</strong></p>
        <p>© 2026 AI Lingua Dashboard</p>
    </div>
    """, unsafe_allow_html=True)

# --- RSS 源 ---
RSS_FEEDS = {
    "🔥 Hacker News (Tech)": "https://news.ycombinator.com/rss",
    "🤖 TechCrunch AI": "https://techcrunch.com/category/artificial-intelligence/feed/",
    "🧪 OpenAI Blog": "https://openai.com/blog/rss.xml",
    "📡 MIT Tech Review": "https://www.technologyreview.com/feed/"
}

# --- 核心函数 ---
def call_gemini_with_retry(model, prompt, max_retries=3):
    """带重试机制的 Gemini API 调用"""
    for attempt in range(max_retries):
        try:
            response = model.generate_content(prompt)
            return response.text, None
        except Exception as e:
            error_str = str(e)
            # 处理配额限制错误
            if "429" in error_str or "quota" in error_str.lower() or "rate" in error_str.lower():
                if attempt < max_retries - 1:
                    wait_time = 15 * (attempt + 1)  # 递增等待时间
                    time.sleep(wait_time)
                    continue
                else:
                    return None, f"""
⚠️ **API 配额已用尽**

您的 Gemini API 免费配额已达到限制。请尝试以下解决方案：

1. **稍后重试** - 等待 1-2 分钟后再次点击分析按钮
2. **升级 API** - 访问 [Google AI Studio](https://aistudio.google.com/) 升级您的 API 计划
3. **更换 API Key** - 在侧边栏输入新的 API Key

💡 **提示**: 免费层每分钟有请求限制，建议每次分析后等待几秒钟再进行下一次分析。
"""
            else:
                return None, f"AI 调用出错: {e}"
    return None, "重试次数已用尽，请稍后再试"

def get_ai_summary(text, api_key):
    if not api_key:
        return "请先在侧边栏输入 API Key"
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.0-flash')
    
    prompt = f"""
    你是一位资深的 AI 产品经理兼英语私教。请阅读以下新闻标题和摘要：
    '{text}'
    
    请完成以下任务：
    1. **【洞察】**：用中文一针见血地分析这条新闻对 AI 行业或普通人的启示（100字以内）。
    2. **【词汇】**：提取 3 个核心英文科技术语/高频词，给出中文释义和例句。
    3. **【难度】**：给这篇英文的阅读难度打分（1-5星）。
    """
    
    result, error = call_gemini_with_retry(model, prompt)
    if error:
        return error
    return result

def prompt_coach(user_prompt, api_key):
    if not api_key:
        return "请先输入 API Key"
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.0-flash')
    
    system_prompt = """
    你是一个严厉但有益的 'Prompt Engineer 导师'。
    当用户发给你一段英文 Prompt 时，你的任务是：
    1. **点评 (Critique)**：指出用户 Prompt 中的语法错误、逻辑模糊之处。
    2. **优化 (Refine)**：给出一个更地道、更高效的英文 Prompt 版本。
    3. **执行 (Execute)**：最后，按照用户原本的意图（或优化后的意图）执行任务。
    
    输出格式要求：
    ---
    ### 👨‍🏫 导师点评
    (这里写点评)
    ### ✨ 优化建议
    (这里写优化后的 Prompt)
    ---
    ### 🤖 AI 回答
    (这里写实际的执行结果)
    """
    
    full_prompt = f"{system_prompt}\n\n用户输入的 Prompt：\n{user_prompt}"
    
    result, error = call_gemini_with_retry(model, full_prompt)
    if error:
        return error
    return result

# --- 主界面 ---

# Hero 横幅区域 - 带背景图片
st.markdown("""
<div class="hero-section">
    <div class="hero-overlay"></div>
    <div class="hero-content">
        <h1 class="main-header">✦ AI Insight & Lingua Dashboard ✦</h1>
        <p class="sub-header">保持好奇，刻意练习。编程护城河消失了，但认知的护城河由你自己建造。</p>
    </div>
</div>
""", unsafe_allow_html=True)

# 引用框 - 带装饰图片
col_quote, col_img = st.columns([3, 1])
with col_quote:
    st.markdown("""
    <div class="quote-box">
        <span class="quote-icon">💭</span>
        "The only way to do great work is to love what you do." — Steve Jobs
    </div>
    """, unsafe_allow_html=True)
with col_img:
    st.markdown("""
    <div class="decorative-img">
        <img src="https://images.unsplash.com/photo-1677442136019-21780ecad995?w=200&h=150&fit=crop" alt="AI Illustration" />
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Tab 区域
tab1, tab2 = st.tabs(["📰 资讯与英语学习", "💪 Prompt 练兵场"])

with tab1:
    # Tab 横幅
    st.markdown("""
    <div class="tab-banner" style="background-image: url('https://images.unsplash.com/photo-1504711434969-e33886168f5c?w=1200&h=300&fit=crop');">
        <div class="tab-banner-content">
            <h2 class="tab-banner-title">📰 AI 资讯 & 英语学习</h2>
            <p class="tab-banner-subtitle">每日精选科技新闻，在阅读中提升英语能力</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 功能介绍 - 三栏布局（带图片）
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="feature-card-with-img">
            <img class="feature-card-img" src="https://images.unsplash.com/photo-1457369804613-52c61a468e7d?w=400&h=200&fit=crop" alt="Reading">
            <div class="feature-card-content">
                <div class="feature-icon">📖</div>
                <div class="feature-title">阅读原文</div>
                <div class="feature-desc">获取最新 AI 科技资讯<br>提升英语阅读能力</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="feature-card-with-img">
            <img class="feature-card-img" src="https://images.unsplash.com/photo-1677442136019-21780ecad995?w=400&h=200&fit=crop" alt="AI Analysis">
            <div class="feature-card-content">
                <div class="feature-icon">🧠</div>
                <div class="feature-title">AI 解析</div>
                <div class="feature-desc">Gemini AI 深度分析<br>洞察行业趋势</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="feature-card-with-img">
            <img class="feature-card-img" src="https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=400&h=200&fit=crop" alt="Vocabulary">
            <div class="feature-card-content">
                <div class="feature-icon">📚</div>
                <div class="feature-title">词汇学习</div>
                <div class="feature-desc">提取核心术语<br>建立专业词汇库</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 初始化 session_state
    if 'news_entries' not in st.session_state:
        st.session_state.news_entries = []
    if 'ai_analyses' not in st.session_state:
        st.session_state.ai_analyses = {}
    if 'current_feed' not in st.session_state:
        st.session_state.current_feed = None
    
    # 新闻源选择
    col_select, col_btn = st.columns([3, 1])
    with col_select:
        selected_feed = st.selectbox("🌐 选择新闻源", list(RSS_FEEDS.keys()))
    with col_btn:
        st.markdown("<br>", unsafe_allow_html=True)
        refresh_btn = st.button("🔄 刷新资讯", use_container_width=True)
    
    # 当切换新闻源或点击刷新时获取新数据
    if refresh_btn or (st.session_state.current_feed != selected_feed and st.session_state.current_feed is not None):
        with st.spinner("🔍 正在获取最新资讯..."):
            feed = feedparser.parse(RSS_FEEDS[selected_feed])
            st.session_state.news_entries = feed.entries[:5] if feed.entries else []
            st.session_state.current_feed = selected_feed
            # 清空之前的分析结果
            st.session_state.ai_analyses = {}
    
    # 首次加载时自动获取
    if not st.session_state.news_entries and st.session_state.current_feed is None:
        st.session_state.current_feed = selected_feed
        with st.spinner("🔍 正在加载资讯..."):
            feed = feedparser.parse(RSS_FEEDS[selected_feed])
            st.session_state.news_entries = feed.entries[:5] if feed.entries else []
    
    # 显示新闻列表
    if not st.session_state.news_entries:
        st.warning("暂无资讯，请点击刷新或选择其他新闻源")
    else:
        for idx, entry in enumerate(st.session_state.news_entries):
            entry_key = f"entry_{idx}_{hash(entry.get('link', idx))}"
            
            st.markdown(f"""
            <div class="news-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span class="tag">#{idx+1}</span>
                    <span style="color: #6b7280; font-size: 0.8rem; font-family: 'Montserrat', sans-serif;">
                        📅 {entry.get('published', 'Unknown')[:25] if entry.get('published') else 'Unknown'}
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            with st.expander(f"📰 {entry.title}", expanded=False):
                st.markdown(f"**🔗 原文链接**: [点击跳转]({entry.link})")
                
                summary_text = entry.get('summary', entry.title)
                st.info(summary_text[:500] + "..." if len(summary_text) > 500 else summary_text)
                
                # 使用唯一的按钮key
                btn_key = f"btn_{idx}_{hash(entry.get('link', idx))}"
                
                if st.button("🧠 AI 深度解析", key=btn_key):
                    with st.spinner("🤔 AI 正在思考..."):
                        analysis = get_ai_summary(summary_text, api_key)
                        st.session_state.ai_analyses[entry_key] = analysis
                
                # 显示已保存的分析结果
                if entry_key in st.session_state.ai_analyses:
                    st.markdown("""
                    <div class="feature-box">
                    """, unsafe_allow_html=True)
                    st.markdown(st.session_state.ai_analyses[entry_key])
                    st.markdown("</div>", unsafe_allow_html=True)

with tab2:
    # Tab 横幅
    st.markdown("""
    <div class="tab-banner" style="background-image: url('https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=1200&h=300&fit=crop');">
        <div class="tab-banner-content">
            <h2 class="tab-banner-title">💪 Prompt 练兵场</h2>
            <p class="tab-banner-subtitle">磨练你的 AI 提示词技能，成为 Prompt 大师</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 功能介绍 - 带图片布局
    col_info, col_img = st.columns([2, 1])
    with col_info:
        st.markdown("""
        <div class="feature-box">
            <h3 style="color: #d4af37; font-family: 'DM Sans', sans-serif; margin-bottom: 1rem;">🎯 如何使用</h3>
            <p style="color: #e0e0e0; font-family: 'Inter', sans-serif;">在这里输入你想问 AI 的英文指令，AI 导师会：</p>
            <ul style="color: #d0d0d0; font-family: 'Inter', sans-serif; line-height: 2;">
                <li>✏️ 点评你的 Prompt 中的语法和逻辑问题</li>
                <li>✨ 给出优化后的专业版本</li>
                <li>🤖 执行你的指令并给出回答</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    with col_img:
        st.markdown("""
        <div class="decorative-img" style="margin-top: 0;">
            <img src="https://images.unsplash.com/photo-1655720828018-edd2daec9349?w=300&h=250&fit=crop" alt="AI Assistant" />
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 示例提示
    st.markdown("""
    <div style="margin-bottom: 1rem;">
        <span class="tag">💡 示例</span>
        <span style="color: #9ca3af; font-size: 0.9rem; font-family: 'Source Sans Pro', sans-serif;">
            Explain Quantum Computing to a 5 year old
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    user_input = st.text_area(
        "✍️ 输入你的英文 Prompt",
        height=120,
        placeholder="Type your English prompt here..."
    )
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        submit_btn = st.button("🚀 提交训练", use_container_width=True)
    
    if submit_btn:
        if user_input:
            with st.spinner("📝 导师正在批改作业..."):
                result = prompt_coach(user_input, api_key)
                st.markdown("""
                <div class="news-card">
                """, unsafe_allow_html=True)
                st.markdown(result)
                st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.warning("⚠️ 请输入内容！")

# 底部装饰
st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)

# 底部图片画廊
st.markdown("""
<div class="image-gallery">
    <div class="gallery-item">
        <img src="https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=300&h=150&fit=crop" alt="Robot">
    </div>
    <div class="gallery-item">
        <img src="https://images.unsplash.com/photo-1507146153580-69a1fe6d8aa1?w=300&h=150&fit=crop" alt="AI">
    </div>
    <div class="gallery-item">
        <img src="https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=300&h=150&fit=crop" alt="Code">
    </div>
    <div class="gallery-item">
        <img src="https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=300&h=150&fit=crop" alt="Tech">
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="decorative-line"></div>', unsafe_allow_html=True)

st.markdown("""
<div class="footer-text">
    <p>✦ Built with <strong>Streamlit</strong> | Powered by <strong>Google Gemini</strong> | Crafted with Passion ✦</p>
</div>
""", unsafe_allow_html=True)
