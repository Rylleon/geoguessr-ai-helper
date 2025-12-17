import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 配置部分 ---
# 把你的 API Key 填在这里，或者在运行时输入
API_KEY = "AIzaSyCWO31kSsm03HBfubUyG_LdW0hjWdxCaLA" 

# --- 核心逻辑 ---
def analyze_image(image, api_key):
    genai.configure(api_key=api_key)
    # 使用支持视觉的模型，如 gemini-1.5-flash (速度快) 或 gemini-1.5-pro (更精准)
    model = genai.GenerativeModel('gemini-1.5-flash') 
    
    # 这里是我们刚才确立的“人设”和“规则”
    system_prompt = """
    你是一个世界顶级的 GeoGuessr 玩家助手。
    你的任务是分析上传的街景图片，推测具体位置。
    
    分析逻辑：
    1. 国家 (Country)：根据道路标线、植被、建筑、电线杆等特征确定。
    2. 区域 (Region/State)：根据地形、具体植被（如德州的杜松）、土壤颜色等细化。
    3. 预测坐标 (Coordinates)：
       - 必须输出具体的经纬度。
       - 为了模拟真实玩家，请在目标区域内对坐标进行高精度的随机微调（小数点后保留12-15位），不要输出过于整齐的坐标。
       - 格式必须严格遵守：/w PlonkIt !g [纬度], [经度]
    
    请直接输出分析结果，保持简洁清晰。
    """
    
    response = model.generate_content([system_prompt, image])
    return response.text

# --- 网页界面 ---
st.title("🌍 GeoGuessr 街景分析助手")
st.write("上传截图，AI 帮你猜地点")

user_api_key = st.text_input("输入 Google API Key (如果代码里没填)", type="password")
uploaded_file = st.file_uploader("上传图片...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='上传的图片', use_column_width=True)
    
    if st.button('开始分析'):
        if not API_KEY and not user_api_key:
            st.error("请输入 API Key")
        else:
            key = API_KEY if API_KEY else user_api_key
            with st.spinner('Gemini 正在观察地形...'):
                try:
                    result = analyze_image(image, key)
                    st.markdown(result)
                except Exception as e:
                    st.error(f"出错啦: {e}")