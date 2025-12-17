import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 页面基础设置 ---
st.set_page_config(page_title="GeoGuessr 助手", page_icon="🌍")

st.title("🌍 GeoGuessr 街景分析助手")
st.markdown("上传截图，AI 帮你推测经纬度。")

# --- 侧边栏：让用户输入 Key ---
with st.sidebar:
    st.header("🔑 身份验证")
    st.markdown("为了使用本工具，你需要填入自己的 Google API Key。")
    
    # 获取用户输入的 Key
    user_api_key = st.text_input("在此输入 Google API Key", type="password")
    
    st.markdown("---")
    st.markdown("### 如何获取 Key？")
    st.markdown("1. 访问 [Google AI Studio](https://aistudio.google.com/app/apikey)")
    st.markdown("2. 点击 'Create API key'")
    st.markdown("3. 复制那一串字符粘贴到上方即可")
    st.info("提示：你的 Key 仅用于当前会话，不会被存储。")

# --- 核心逻辑函数 ---
def analyze_image(image, api_key):
    # 配置 API
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash') 
    
    # 系统提示词 (你之前调教好的)
    system_prompt = """
    你是一个世界顶级的 GeoGuessr 玩家助手。
    你的任务是分析上传的街景图片，推测具体位置。
    
    分析逻辑：
    1. 国家 (Country)：根据道路标线、植被、建筑、电线杆等特征确定。
    2. 区域 (Region/State)：根据地形、具体植被、土壤颜色等细化。
    3. 预测坐标 (Coordinates)：
       - 必须输出具体的经纬度。
       - 为了模拟真实玩家，请在目标区域内对坐标进行高精度的随机微调（小数点后保留12-15位），不要输出过于整齐的坐标。
       - 格式必须严格遵守：/w PlonkIt !g [纬度], [经度]
    
    请直接输出分析结果，保持简洁清晰。
    """
    
    response = model.generate_content([system_prompt, image])
    return response.text

# --- 主界面逻辑 ---
uploaded_file = st.file_uploader("请上传街景截图...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # 展示图片
    image = Image.open(uploaded_file)
    st.image(image, caption='已上传图片', use_column_width=True)
    
    # 按钮点击事件
    if st.button('开始分析 🚀'):
        if not user_api_key:
            st.error("❌ 请先在左侧侧边栏输入你的 Google API Key 才能开始！")
        else:
            with st.spinner('Gemini 正在观察地形... (约需 3-5 秒)'):
                try:
                    result = analyze_image(image, user_api_key)
                    st.success("分析完成！")
                    st.markdown(result)
                except Exception as e:
                    st.error(f"发生错误: {e}")
                    st.warning("请检查你的 API Key 是否正确，或者网络是否通畅。")
