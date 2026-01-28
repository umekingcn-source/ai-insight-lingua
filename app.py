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

# --- 自定义样式 ---
st.markdown("""
<style>
/* 导入 Google Fonts - 使用更有特色的字体 */
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

/* 全局样式 */
.stApp {
    background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
}

/* 主标题样式 */
.main-header {
    background: linear-gradient(90deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-family: 'Outfit', sans-serif;
    font-size: 3rem;
    font-weight: 700;
    text-align: center;
    margin-bottom: 0.5rem;
    animation: glow 2s ease-in-out infinite alternate;
}

@keyframes glow {
    from { filter: drop-shadow(0 0 5px rgba(102, 126, 234, 0.5)); }
    to { filter: drop-shadow(0 0 20px rgba(240, 147, 251, 0.8)); }
}

/* 副标题样式 */
.sub-header {
    color: #a0aec0;
    font-family: 'Outfit', sans-serif;
    font-size: 1.1rem;
    text-align: center;
    margin-bottom: 2rem;
    letter-spacing: 0.5px;
}

/* 卡片样式 */
.news-card {
    background: linear-gradient(145deg, rgba(45, 55, 72, 0.9), rgba(26, 32, 44, 0.95));
    border-radius: 16px;
    padding: 1.5rem;
    margin: 1rem 0;
    border: 1px solid rgba(102, 126, 234, 0.3);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    transition: all 0.3s ease;
}

.news-card:hover {
    transform: translateY(-5px);
    border-color: rgba(240, 147, 251, 0.6);
    box-shadow: 0 12px 40px rgba(102, 126, 234, 0.3);
}

/* 特色区块 */
.feature-box {
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.2), rgba(118, 75, 162, 0.2));
    border-radius: 12px;
    padding: 1.5rem;
    margin: 1rem 0;
    border-left: 4px solid #667eea;
}

/* 成就徽章 */
.achievement-badge {
    background: linear-gradient(135deg, #f093fb, #f5576c);
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 20px;
    font-weight: 600;
    display: inline-block;
    margin: 0.25rem;
    font-size: 0.9rem;
}

/* 统计卡片 */
.stat-card {
    background: linear-gradient(145deg, rgba(102, 126, 234, 0.3), rgba(118, 75, 162, 0.3));
    border-radius: 12px;
    padding: 1rem;
    text-align: center;
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.stat-number {
    font-size: 2.5rem;
    font-weight: 700;
    background: linear-gradient(90deg, #667eea, #f093fb);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.stat-label {
    color: #a0aec0;
    font-size: 0.9rem;
    margin-top: 0.5rem;
}

/* 按钮样式 */
.stButton > button {
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 25px;
    padding: 0.75rem 2rem;
    font-weight: 600;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}

.stButton > button:hover {
    transform: scale(1.05);
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
}

/* 侧边栏样式 */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
}

[data-testid="stSidebar"] .stMarkdown {
    color: #e2e8f0;
}

/* 输入框样式 */
.stTextInput > div > div > input {
    background: rgba(45, 55, 72, 0.8);
    border: 1px solid rgba(102, 126, 234, 0.5);
    border-radius: 10px;
    color: white;
}

.stTextArea > div > div > textarea {
    background: rgba(45, 55, 72, 0.8);
    border: 1px solid rgba(102, 126, 234, 0.5);
    border-radius: 10px;
    color: white;
}

/* 选择框样式 */
.stSelectbox > div > div {
    background: rgba(45, 55, 72, 0.8);
    border: 1px solid rgba(102, 126, 234, 0.5);
    border-radius: 10px;
}

/* Tab 样式 */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: rgba(26, 32, 44, 0.5);
    border-radius: 12px;
    padding: 0.5rem;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    color: #a0aec0;
    font-weight: 500;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(90deg, #667eea, #764ba2);
    color: white;
}

/* Expander 样式 */
.streamlit-expanderHeader {
    background: rgba(45, 55, 72, 0.6);
    border-radius: 10px;
    border: 1px solid rgba(102, 126, 234, 0.3);
}

/* Metric 样式 */
[data-testid="stMetricValue"] {
    background: linear-gradient(90deg, #667eea, #f093fb);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 700;
}

/* 装饰性元素 */
.decoration-circle {
    position: fixed;
    border-radius: 50%;
    pointer-events: none;
    opacity: 0.1;
}

.circle-1 {
    width: 300px;
    height: 300px;
    background: radial-gradient(circle, #667eea, transparent);
    top: 10%;
    right: 5%;
}

.circle-2 {
    width: 200px;
    height: 200px;
    background: radial-gradient(circle, #f093fb, transparent);
    bottom: 20%;
    left: 10%;
}

/* 图标动画 */
.animated-icon {
    animation: bounce 2s infinite;
}

@keyframes bounce {
    0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
    40% { transform: translateY(-10px); }
    60% { transform: translateY(-5px); }
}

/* 渐变分割线 */
.gradient-divider {
    height: 2px;
    background: linear-gradient(90deg, transparent, #667eea, #f093fb, #667eea, transparent);
    margin: 2rem 0;
    border: none;
}

/* 引用样式 */
.quote-box {
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(240, 147, 251, 0.1));
    border-left: 4px solid #f093fb;
    padding: 1rem 1.5rem;
    border-radius: 0 12px 12px 0;
    font-style: italic;
    color: #cbd5e0;
}

/* 标签样式 */
.tag {
    background: rgba(102, 126, 234, 0.3);
    color: #a0aec0;
    padding: 0.25rem 0.75rem;
    border-radius: 15px;
    font-size: 0.8rem;
    margin-right: 0.5rem;
    display: inline-block;
}

/* 加载动画 */
.loading-wave {
    display: flex;
    justify-content: center;
    gap: 4px;
}

.loading-wave span {
    width: 8px;
    height: 8px;
    background: #667eea;
    border-radius: 50%;
    animation: wave 1s infinite ease-in-out;
}

.loading-wave span:nth-child(2) { animation-delay: 0.1s; }
.loading-wave span:nth-child(3) { animation-delay: 0.2s; }

@keyframes wave {
    0%, 100% { transform: scaleY(1); }
    50% { transform: scaleY(2); }
}
</style>
""", unsafe_allow_html=True)

# --- 侧边栏配置 ---
with st.sidebar:
    # Logo 和标题
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0;">
        <div style="font-size: 3rem; margin-bottom: 0.5rem;">🧠</div>
        <h2 style="background: linear-gradient(90deg, #667eea, #f093fb); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0;">AI Lingua</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)
    
    # API Key 输入
    st.markdown("### 🔑 API 配置")
    default_key = st.secrets.get("GEMINI_API_KEY", "")
    api_key = st.text_input("Gemini API Key", value=default_key, type="password")
    
    st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)
    
    # 今日成就
    st.markdown("### 🏆 今日成就")
    
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
    st.markdown("### 📈 本周趋势")
    chart_data = pd.DataFrame({
        'Day': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
        'Words': [10, 15, 12, 18, 8]
    })
    st.bar_chart(chart_data.set_index('Day'), color="#667eea")
    
    # 底部信息
    st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; color: #718096; font-size: 0.8rem;">
        <p>Powered by Gemini AI</p>
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
<h1 class="main-header">🚀 AI Insight & Lingua Dashboard</h1>
""", unsafe_allow_html=True)

# 副标题
st.markdown("""
<p class="sub-header">保持好奇，刻意练习。编程护城河消失了，但认知的护城河由你自己建造。</p>
""", unsafe_allow_html=True)

# 引用框
st.markdown("""
<div class="quote-box">
    💡 "The only way to do great work is to love what you do." — Steve Jobs
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Tab 区域
tab1, tab2 = st.tabs(["📰 资讯与英语学习", "💪 Prompt 练兵场"])

with tab1:
    # 功能介绍
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="feature-box">
            <h4>📖 阅读原文</h4>
            <p style="color: #a0aec0; font-size: 0.9rem;">获取最新 AI 科技资讯，提升英语阅读能力</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="feature-box">
            <h4>🧠 AI 解析</h4>
            <p style="color: #a0aec0; font-size: 0.9rem;">Gemini AI 深度分析，洞察行业趋势</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="feature-box">
            <h4>📚 词汇学习</h4>
            <p style="color: #a0aec0; font-size: 0.9rem;">提取核心术语，建立专业词汇库</p>
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
                            <span style="color: #718096; font-size: 0.8rem;">
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
        <h3>🎯 Prompt 练兵场</h3>
        <p style="color: #a0aec0;">在这里输入你想问 AI 的英文指令，AI 导师会：</p>
        <ul style="color: #a0aec0;">
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
        <span style="color: #a0aec0; font-size: 0.9rem;">
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
<div style="text-align: center; color: #718096; padding: 1rem;">
    <p>🚀 Built with Streamlit | 🤖 Powered by Google Gemini | 💜 Made with Love</p>
</div>
""", unsafe_allow_html=True)
