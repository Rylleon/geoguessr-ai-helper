import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. 页面基础配置 ---
st.set_page_config(
    page_title="GeoGuessr AI 助手",
    page_icon="🌍",
    layout="wide"
)

# 自定义 CSS 样式，让界面更美观
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #ff4b4b;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. 侧边栏：API 配置与说明 ---
with st.sidebar:
    st.title("⚙️ 配置中心")
    st.markdown("### 1. 输入你的 API Key")
    # 情况 B：强制用户输入自己的 Key
    user_api_key = st.text_input("Google API Key", type="password", help="在此粘贴你的 Gemini API Key")
    
    st.markdown("---")
    st.markdown("### 2. 如何获取 Key？")
    st.markdown("[点击前往 Google AI Studio](https://aistudio.google.com/app/apikey)")
    st.info("申请完全免费，生成的 Key 粘贴到上方即可使用。")
    
    st.markdown("---")
    st.markdown("### 3. 关于坐标格式")
    st.code("/w PlonkIt !g [纬度], [经度]")
    st.caption("坐标已进行高精度随机化偏移，模拟真实点击。")

# --- 3. 核心逻辑函数 ---
def analyze_image(image, api_key):
    # 配置 API 密钥
    genai.configure(api_key=api_key)
    
    # 使用完整模型路径以避免 404 错误
    # 如果 flash 依然报错，可以尝试改为 'models/gemini-1.5-pro'
    model = genai.GenerativeModel('models/gemini-1.5-flash') 
    
    # 你的核心提示词（已锁定右行规则与坐标伪装）
    system_prompt = """
    你是一个世界顶级的 GeoGuessr 玩家助手，专门分析街景截图。
    
    分析要求：
    1. 首先判定行驶方向（左行或右行）。
    2. 国家 (Country)：根据标线、植被、电线杆、路牌特征判定。
    3. 细分区域 (Region)：观察地形（如桌状山）、土壤颜色、特定树种。
    4. 预测坐标 (Coordinates)：
       - 必须输出经纬度坐标。
       - 严禁输出整齐的小数（如 .500000），必须模拟真实的定位漂移。
       - 小数点后保留 12-15 位随机数字。
       - 格式必须严格为：/w PlonkIt !g [纬度], [经度]
    
    语言要求：中文。保持简洁，不要废话。
    """
    
    # 发起请求
    response = model.generate_content([system_prompt, image])
    return response.text

# --- 4. 主界面布局 ---
st.title("🌍 GeoGuessr 专家级地理分析工具")
st.write("上传一张街景截图，AI 将为你深度解析地理线索并生成伪装坐标。")

col1, col2 = st.columns([1, 1])

with col1:
    uploaded_file = st.file_uploader("📂 选择街景截图 (PNG/JPG)...", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="待分析场景", use_column_width=True)

with col2:
    st.subheader("🔍 分析结果")
    if uploaded_file:
        if st.button("开始深度分析 🚀"):
            if not user_api_key:
                st.error("⚠️ 请在左侧侧边栏填入 API Key 后再试！")
            else:
                with st.spinner("正在解析植被、土壤与道路特征..."):
                    try:
                        result = analyze_image(image, user_api_key)
                        st.markdown("---")
                        st.markdown(result)
                        st.balloons()
                    except Exception as e:
                        st.error(f"分析失败: {str(e)}")
                        if "404" in str(e):
                            st.warning("提示：模型路径错误或该 Key 不支持此模型。请联系管理员更新模型名。")
    else:
        st.info("等待图片上传...")

# --- 5. 页脚 ---
st.markdown("---")
st.caption("仅供学习复盘使用。请尊重 GeoGuessr 社区公平竞赛原则。")
