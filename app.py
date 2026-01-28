import streamlit as st
import feedparser
import google.generativeai as genai
import pandas as pd
import datetime

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
/* 导入 Google Fonts - 专业优雅的字体 */
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700&family=Montserrat:wght@300;400;500;600;700&family=Source+Sans+Pro:wght@300;400;600&display=swap');

/* 全局样式 - 深色优雅背景 */
.stApp {
    background: linear-gradient(180deg, #0a0a0a 0%, #1a1a1a 50%, #0d0d0d 100%);
}

/* 主标题样式 - 金色渐变 */
.main-header {
    background: linear-gradient(135deg, #d4af37 0%, #f4e4bc 25%, #d4af37 50%, #aa8c2c 75%, #d4af37 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-family: 'Playfair Display', serif;
    font-size: 2.8rem;
    font-weight: 700;
    text-align: center;
    margin-bottom: 0.5rem;
    letter-spacing: 2px;
}

/* 副标题样式 */
.sub-header {
    color: #9ca3af;
    font-family: 'Montserrat', sans-serif;
    font-size: 1rem;
    text-align: center;
    margin-bottom: 2rem;
    letter-spacing: 1px;
    font-weight: 300;
}

/* 卡片样式 - 深色玻璃态 */
.news-card {
    background: linear-gradient(145deg, rgba(26, 26, 26, 0.95), rgba(15, 15, 15, 0.98));
    border-radius: 12px;
    padding: 1.5rem;
    margin: 1rem 0;
    border: 1px solid rgba(212, 175, 55, 0.2);
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
    background: linear-gradient(135deg, rgba(212, 175, 55, 0.05), rgba(170, 140, 44, 0.05));
    border-radius: 12px;
    padding: 1.5rem;
    margin: 1rem 0;
    border-left: 3px solid #d4af37;
    backdrop-filter: blur(10px);
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
    font-family: 'Montserrat', sans-serif;
}

/* 统计卡片 */
.stat-card {
    background: linear-gradient(145deg, rgba(212, 175, 55, 0.1), rgba(170, 140, 44, 0.05));
    border-radius: 12px;
    padding: 1.2rem;
    text-align: center;
    border: 1px solid rgba(212, 175, 55, 0.2);
}

.stat-number {
    font-size: 2.2rem;
    font-weight: 700;
    font-family: 'Playfair Display', serif;
    background: linear-gradient(135deg, #d4af37, #f4e4bc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.stat-label {
    color: #9ca3af;
    font-size: 0.85rem;
    margin-top: 0.5rem;
    font-family: 'Montserrat', sans-serif;
    font-weight: 500;
}

/* 按钮样式 - 金色优雅 */
.stButton > button {
    background: linear-gradient(135deg, #d4af37 0%, #aa8c2c 100%);
    color: #0a0a0a;
    border: none;
    border-radius: 8px;
    padding: 0.75rem 2rem;
    font-weight: 600;
    font-family: 'Montserrat', sans-serif;
    transition: all 0.3s ease;
    box-shadow: 0 4px 20px rgba(212, 175, 55, 0.3);
    text-transform: uppercase;
    letter-spacing: 1px;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 30px rgba(212, 175, 55, 0.4);
}

/* 侧边栏样式 */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d0d0d 0%, #1a1a1a 100%);
    border-right: 1px solid rgba(212, 175, 55, 0.1);
}

[data-testid="stSidebar"] .stMarkdown {
    color: #e5e7eb;
}

/* 输入框样式 */
.stTextInput > div > div > input {
    background: rgba(26, 26, 26, 0.9);
    border: 1px solid rgba(212, 175, 55, 0.3);
    border-radius: 8px;
    color: #e5e7eb;
    font-family: 'Source Sans Pro', sans-serif;
}

.stTextInput > div > div > input:focus {
    border-color: #d4af37;
    box-shadow: 0 0 10px rgba(212, 175, 55, 0.2);
}

.stTextArea > div > div > textarea {
    background: rgba(26, 26, 26, 0.9);
    border: 1px solid rgba(212, 175, 55, 0.3);
    border-radius: 8px;
    color: #e5e7eb;
    font-family: 'Source Sans Pro', sans-serif;
}

.stTextArea > div > div > textarea:focus {
    border-color: #d4af37;
    box-shadow: 0 0 10px rgba(212, 175, 55, 0.2);
}

/* 选择框样式 */
.stSelectbox > div > div {
    background: rgba(26, 26, 26, 0.9);
    border: 1px solid rgba(212, 175, 55, 0.3);
    border-radius: 8px;
}

/* Tab 样式 */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: rgba(15, 15, 15, 0.8);
    border-radius: 10px;
    padding: 0.5rem;
    border: 1px solid rgba(212, 175, 55, 0.1);
}

.stTabs [data-baseweb="tab"] {
    border-radius: 6px;
    color: #9ca3af;
    font-weight: 500;
    font-family: 'Montserrat', sans-serif;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #d4af37, #aa8c2c);
    color: #0a0a0a;
}

/* Expander 样式 */
.streamlit-expanderHeader {
    background: rgba(26, 26, 26, 0.8);
    border-radius: 8px;
    border: 1px solid rgba(212, 175, 55, 0.2);
    font-family: 'Source Sans Pro', sans-serif;
}

.streamlit-expanderHeader:hover {
    border-color: rgba(212, 175, 55, 0.4);
}

/* Metric 样式 */
[data-testid="stMetricValue"] {
    background: linear-gradient(135deg, #d4af37, #f4e4bc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 700;
    font-family: 'Playfair Display', serif;
}

/* 渐变分割线 - 金色 */
.gradient-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(212, 175, 55, 0.5), transparent);
    margin: 1.5rem 0;
    border: none;
}

/* 引用样式 */
.quote-box {
    background: linear-gradient(135deg, rgba(212, 175, 55, 0.08), rgba(170, 140, 44, 0.05));
    border-left: 3px solid #d4af37;
    padding: 1.2rem 1.5rem;
    border-radius: 0 10px 10px 0;
    font-style: italic;
    color: #d1d5db;
    font-family: 'Playfair Display', serif;
    font-size: 1.1rem;
}

/* 标签样式 */
.tag {
    background: rgba(212, 175, 55, 0.15);
    color: #d4af37;
    padding: 0.3rem 0.8rem;
    border-radius: 15px;
    font-size: 0.8rem;
    margin-right: 0.5rem;
    display: inline-block;
    font-family: 'Montserrat', sans-serif;
    font-weight: 500;
    border: 1px solid rgba(212, 175, 55, 0.3);
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
    font-family: 'Playfair Display', serif;
    font-size: 1.5rem;
    font-weight: 600;
    letter-spacing: 3px;
    margin: 0;
}

.brand-subtitle {
    color: #6b7280;
    font-size: 0.75rem;
    font-family: 'Montserrat', sans-serif;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-top: 0.3rem;
}

/* 特性图标卡片 */
.feature-icon-card {
    background: linear-gradient(145deg, rgba(26, 26, 26, 0.9), rgba(15, 15, 15, 0.95));
    border-radius: 12px;
    padding: 1.5rem;
    text-align: center;
    border: 1px solid rgba(212, 175, 55, 0.15);
    transition: all 0.3s ease;
}

.feature-icon-card:hover {
    border-color: rgba(212, 175, 55, 0.4);
    transform: translateY(-3px);
}

.feature-icon {
    font-size: 2rem;
    margin-bottom: 0.8rem;
}

.feature-title {
    color: #d4af37;
    font-family: 'Montserrat', sans-serif;
    font-weight: 600;
    font-size: 1rem;
    margin-bottom: 0.5rem;
}

.feature-desc {
    color: #9ca3af;
    font-size: 0.85rem;
    font-family: 'Source Sans Pro', sans-serif;
    line-height: 1.5;
}

/* 底部信息 */
.footer-text {
    text-align: center;
    color: #6b7280;
    font-size: 0.8rem;
    font-family: 'Montserrat', sans-serif;
    letter-spacing: 1px;
}

.footer-text a {
    color: #d4af37;
    text-decoration: none;
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
    background: #0a0a0a;
}

::-webkit-scrollbar-thumb {
    background: rgba(212, 175, 55, 0.3);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: rgba(212, 175, 55, 0.5);
}

/* 信息提示框 */
.stAlert {
    background: rgba(26, 26, 26, 0.9);
    border: 1px solid rgba(212, 175, 55, 0.2);
    border-radius: 8px;
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
</style>
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
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"AI 调用出错: {e}"

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
    
    try:
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return str(e)

# --- 主界面 ---
# 主标题
st.markdown("""
<h1 class="main-header">✦ AI Insight & Lingua Dashboard ✦</h1>
""", unsafe_allow_html=True)

# 副标题
st.markdown("""
<p class="sub-header">保持好奇，刻意练习。编程护城河消失了，但认知的护城河由你自己建造。</p>
""", unsafe_allow_html=True)

# 引用框
st.markdown("""
<div class="quote-box">
    "The only way to do great work is to love what you do." — Steve Jobs
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Tab 区域
tab1, tab2 = st.tabs(["📰 资讯与英语学习", "💪 Prompt 练兵场"])

with tab1:
    # 功能介绍 - 三栏布局
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="feature-icon-card">
            <div class="feature-icon">📖</div>
            <div class="feature-title">阅读原文</div>
            <div class="feature-desc">获取最新 AI 科技资讯<br>提升英语阅读能力</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="feature-icon-card">
            <div class="feature-icon">🧠</div>
            <div class="feature-title">AI 解析</div>
            <div class="feature-desc">Gemini AI 深度分析<br>洞察行业趋势</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="feature-icon-card">
            <div class="feature-icon">📚</div>
            <div class="feature-title">词汇学习</div>
            <div class="feature-desc">提取核心术语<br>建立专业词汇库</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 新闻源选择
    col_select, col_btn = st.columns([3, 1])
    with col_select:
        selected_feed = st.selectbox("🌐 选择新闻源", list(RSS_FEEDS.keys()))
    with col_btn:
        st.markdown("<br>", unsafe_allow_html=True)
        refresh_btn = st.button("🔄 刷新资讯", use_container_width=True)
    
    if refresh_btn:
        with st.spinner("🔍 正在获取最新资讯..."):
            feed = feedparser.parse(RSS_FEEDS[selected_feed])
            
            if not feed.entries:
                st.warning("暂无资讯，请稍后重试或选择其他新闻源")
            else:
                for idx, entry in enumerate(feed.entries[:5]):
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
                        
                        if st.button("🧠 AI 深度解析", key=f"btn_{entry.link}"):
                            with st.spinner("🤔 AI 正在思考..."):
                                analysis = get_ai_summary(summary_text, api_key)
                                st.markdown("""
                                <div class="feature-box">
                                """, unsafe_allow_html=True)
                                st.markdown(analysis)
                                st.markdown("</div>", unsafe_allow_html=True)

with tab2:
    # 功能介绍
    st.markdown("""
    <div class="feature-box">
        <h3 style="color: #d4af37; font-family: 'Playfair Display', serif; margin-bottom: 1rem;">🎯 Prompt 练兵场</h3>
        <p style="color: #9ca3af; font-family: 'Source Sans Pro', sans-serif;">在这里输入你想问 AI 的英文指令，AI 导师会：</p>
        <ul style="color: #9ca3af; font-family: 'Source Sans Pro', sans-serif; line-height: 1.8;">
            <li>✏️ 点评你的 Prompt 中的语法和逻辑问题</li>
            <li>✨ 给出优化后的专业版本</li>
            <li>🤖 执行你的指令并给出回答</li>
        </ul>
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
st.markdown("""
<div class="footer-text">
    <p>✦ Built with <strong>Streamlit</strong> | Powered by <strong>Google Gemini</strong> | Crafted with Passion ✦</p>
</div>
""", unsafe_allow_html=True)
