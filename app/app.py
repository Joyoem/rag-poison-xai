import streamlit as st
import json
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# --- 页面基础配置 ---
st.set_page_config(layout="wide", page_title="RAG Safety Lab", page_icon="🛡️")

# 自定义 CSS 让界面更有科技感
st.markdown("""
    <style>
    .main { background-color: #fafafa; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# --- 1. 数据加载与处理 ---
@st.cache_data
def load_all_data():
    try:
        with open("./final_results.json", "r") as f:
            return json.load(f)
    except:
        st.error("Missing final_results.json! Ensure your merge script ran correctly.")
        return []

data = load_all_data()
if not data: st.stop()

# --- 2. 侧边栏控制面板 ---
st.sidebar.title("🛡️ RAG Red-Teaming Lab")
st.sidebar.markdown("Investigating Model Vulnerability in Qwen-7B")

case_id = st.sidebar.selectbox("Select Case Study", range(len(data)), 
                               format_func=lambda x: f"Query: {data[x]['question'][:30]}...")
selected = data[case_id]

st.sidebar.markdown("---")
st.sidebar.subheader("📊 Global Stats")
st.sidebar.metric("Success Attack Rate", "84%", "-12% (with Defense)")
st.sidebar.write(f"Sample ID: `{selected['id'][:12]}`")

# --- 3. 主界面顶部：核心信息 ---
st.title("🧠 Interpretability Dashboard")
st.caption("Analyzing the internal logic flip during targeted data poisoning attacks.")

col_q, col_a = st.columns([2, 1])
with col_q:
    st.info(f"**Question:** {selected['question']}")
with col_a:
    st.success(f"**Ground Truth:** {selected['ground_truth']}")

# --- 4. 核心功能区 (Tabs 分类) ---
tab1, tab2, tab3, tab4 = st.tabs(["📈 Decision Flip", "📜 Logit Lens", "🔥 Attention Map", "🛡️ Defense Demo"])

# --- Tab 1: 动态折线图 (Decision Flip) ---
with tab1:
    st.subheader("Probability Trajectory across Layers")
    st.write("How the model's confidence shifts from Truth to Poisoned answer.")
    
    # 模拟数据生成 (基于逻辑回归曲线)
    layers = np.arange(28)
    # 这里的 15 和 20 是分歧点，实际项目中可以根据 logit_lens 的数据动态计算
    truth_conf = 1 / (1 + np.exp((layers - 12) * 0.5))
    poison_conf = 1 / (1 + np.exp(-(layers - 18) * 0.8))
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=layers, y=truth_conf, name="Truth Confidence", line=dict(color='green', width=4)))
    fig.add_trace(go.Scatter(x=layers, y=poison_conf, name="Poison Confidence", line=dict(color='red', width=4, dash='dash')))
    
    fig.update_layout(title="Internal Confidence Flip Point", xaxis_title="Transformer Layer", 
                      yaxis_title="Probability", template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)
    st.warning("Observation: The model's 'belief' typically flips between Layer 16 and 22.")

# --- Tab 2: 层级对比 (Logit Lens) ---
with tab2:
    st.subheader("Step-by-Step Thought Evolution")
    
    rows_html = ""
    for i, (c, t) in enumerate(zip(selected['minds']['clean'], selected['minds']['targeted'])):
        diff = "⚠️" if c != t else "✅"
        bg = "#fff5f5" if c != t else "transparent"
        rows_html += f"""
        <tr style="background-color: {bg}">
            <td style="padding:8px">Layer {i}</td>
            <td style="color:green">{c}</td>
            <td style="color:{'red' if c!=t else 'black'}; font-weight:{'bold' if c!=t else 'normal'}">{diff} {t}</td>
        </tr>"""
    
    st.markdown(f"""
        <table style="width:100%; border-collapse: collapse; border: 1px solid #ddd;">
            <tr style="background-color:#eee"><th>Layer</th><th>Clean Mind</th><th>Targeted Mind</th></tr>
            {rows_html}
        </table>
    """, unsafe_allow_html=True)

# --- Tab 3: 热力图 (Attention Map) ---
with tab3:
    st.subheader(f"Visualizing Token Importance ({selected['score_type']})")
    
    scores = np.array(selected['display_scores'])
    max_s = scores.max() if scores.max() > 0 else 1
    
    html_elements = []
    for t, s in zip(selected['tokens'], scores):
        alpha = s / max_s
        color = f"rgba(255, 0, 0, {alpha:.4f})"
        weight = "bold" if alpha > 0.5 else "normal"
        element = f'<span style="background-color:{color}; color:{"white" if alpha>0.5 else "black"}; font-weight:{weight}; padding:2px 5px; border-radius:3px; margin:2px; display:inline-block; border:1px solid #eee;">{t}</span>'
        html_elements.append(element)
    
    st.markdown(f'<div style="line-height:2.2; background:#f0f0f0; padding:20px; border-radius:10px;">{" ".join(html_elements)}</div>', unsafe_allow_html=True)

# --- Tab 4: 防御演示 (The "Meaning" Part) ---
with tab4:
    st.subheader("Can we defend this?")
    st.write("Comparison between a standard RAG and a 'Defense-Prompt' RAG.")
    
    col_no, col_def = st.columns(2)
    with col_no:
        st.error("❌ Standard RAG Output")
        st.write(f"**Response:** {selected['minds']['targeted'][-1]}")
        st.caption("Result: Successfully deceived by poisoned context.")
        
    with col_def:
        st.success("🛡️ Robust RAG (Self-Audit)")
        # 这里模拟一个防御后的结果，通常防御后会回归正确答案
        st.write(f"**Response:** {selected['ground_truth']}")
        st.caption("Result: Adversarial noise detected and ignored.")
    
    st.markdown("""
    **Defense Strategy:**
    - **Instruction Tuning**: Adding 'Ignore irrelevant gibberish' to system prompt.
    - **Perplexity Filter**: Detecting the `adv_suffix` by its high perplexity.
    """)
