import streamlit as st
import feedparser
import google.generativeai as genai
import pandas as pd
import datetime

# --- 配置页面 ---
st.set_page_config(page_title="AI Insight & Lingua", layout="wide")

# --- 侧边栏配置 ---
with st.sidebar:
    st.title("⚙️ 设置与状态")
    # 从 secrets 获取默认 API Key，用户也可以自己输入
    default_key = st.secrets.get("GEMINI_API_KEY", "")
    api_key = st.text_input("Gemini API Key", value=default_key, type="password")
    
    st.divider()
    st.subheader("📊 今日成就")
    # 模拟数据，实际可接入本地数据库
    col1, col2 = st.columns(2)
    col1.metric("已读新闻", "3", "+1")
    col2.metric("新单词", "12", "+5")
    
    st.write("本周学习趋势")
    chart_data = pd.DataFrame({'Day': ['Mon', 'Tue', 'Wed'], 'Words': [10, 15, 12]})
    st.bar_chart(chart_data.set_index('Day'))

# --- RSS 源 ---
RSS_FEEDS = {
    "Hacker News (Tech)": "https://news.ycombinator.com/rss",
    "TechCrunch AI": "https://techcrunch.com/category/artificial-intelligence/feed/",
    "OpenAI Blog": "https://openai.com/blog/rss.xml",
    "MIT Tech Review": "https://www.technologyreview.com/feed/"
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
st.title("🚀 AI Insight & Lingua Dashboard")
st.caption("保持好奇，刻意练习。编程护城河消失了，但认知的护城河由你自己建造。")

tab1, tab2 = st.tabs(["📰 资讯与英语学习", "💪 Prompt 练兵场"])

with tab1:
    selected_feed = st.selectbox("选择新闻源", list(RSS_FEEDS.keys()))
    
    if st.button("刷新资讯"):
        feed = feedparser.parse(RSS_FEEDS[selected_feed])
        for entry in feed.entries[:5]: # 只看前5条
            with st.expander(f"🇬🇧 {entry.title}", expanded=False):
                st.write(f"**发布时间**: {entry.get('published', 'Unknown')}")
                st.write(f"**原文链接**: [点击跳转]({entry.link})")
                
                # 只有摘要，没有全文，适合 RSS
                summary_text = entry.get('summary', entry.title)
                st.info(summary_text)
                
                if st.button("🧠 AI 深度解析", key=entry.link):
                    with st.spinner("AI 正在思考..."):
                        analysis = get_ai_summary(summary_text, api_key)
                        st.markdown(analysis)

with tab2:
    st.write("在这里输入你想问 AI 的英文指令，AI 会先教你英语，再回答问题。")
    user_input = st.text_area("输入你的英文 Prompt (例如: Explain Quantum Computing to a 5 year old)", height=100)
    
    if st.button("提交训练"):
        if user_input:
            with st.spinner("导师正在批改作业..."):
                result = prompt_coach(user_input, api_key)
                st.markdown(result)
        else:
            st.warning("请输入内容！")

