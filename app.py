import streamlit as st
import numpy as np
import tensorflow as tf
from PIL import Image
from textwrap import dedent

def render_html(html):
    st.markdown(dedent(html), unsafe_allow_html=True)

st.set_page_config(
    page_title="Fruit Freshness Detector",
    page_icon="🍎",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
.stApp {
    background:
        radial-gradient(circle at 15% 10%, rgba(32, 201, 151, 0.10), transparent 28%),
        radial-gradient(circle at 85% 20%, rgba(25, 135, 84, 0.08), transparent 30%),
        linear-gradient(135deg, #07100d 0%, #0b1713 50%, #07100d 100%);
    color: #f5f7f6;
}

.block-container {
    max-width: 1150px;
    padding-top: 2.5rem;
    padding-bottom: 3rem;
}

.hero {
    text-align: center;
    padding: 10px 0 38px 0;
}

.hero-icon {
    font-size: 48px;
    margin-bottom: 8px;
}

.hero-title {
    font-size: 48px;
    font-weight: 800;
    letter-spacing: -1.5px;
    margin: 0;
    color: #f5f7f6;
}

.hero-title span {
    background: linear-gradient(90deg, #20c997, #65e6b5);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-subtitle {
    font-size: 17px;
    color: #8fa39a;
    margin-top: 10px;
}

.section-title {
    color: #f5f7f6;
    font-size: 21px;
    font-weight: 700;
    margin-bottom: 12px;
}

.section-description {
    color: #8fa39a;
    font-size: 14px;
    margin-bottom: 18px;
}

.panel {
    background: rgba(18, 31, 26, 0.82);
    border: 1px solid rgba(89, 117, 104, 0.25);
    border-radius: 22px;
    padding: 25px;
    box-shadow: 0 18px 45px rgba(0, 0, 0, 0.22);
    backdrop-filter: blur(12px);
}

.panel-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 8px;
}

.panel-icon {
    font-size: 25px;
}

.panel-title {
    color: #f5f7f6;
    font-size: 21px;
    font-weight: 700;
}

.panel-description {
    color: #8fa39a;
    font-size: 14px;
    line-height: 1.6;
    margin-bottom: 18px;
}

.preview-panel {
    min-height: 295px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.empty-preview {
    text-align: center;
    width: 100%;
    padding: 45px 20px;
}

.empty-icon {
    font-size: 55px;
    margin-bottom: 12px;
}

.empty-text {
    color: #81958b;
    font-size: 15px;
}

.upload-info {
    text-align: center;
    color: #7f958b;
    font-size: 13px;
    margin-top: 16px;
}

.upload-info b {
    color: #a9bcb3;
}

.stFileUploader {
    margin-top: 8px;
}

div[data-testid="stFileUploader"] {
    background: rgba(11, 22, 18, 0.9);
    border: 1px dashed rgba(32, 201, 151, 0.38);
    border-radius: 15px;
    padding: 8px;
}

div[data-testid="stFileUploaderDropzone"] {
    background: transparent;
}

div[data-testid="stFileUploaderDropzoneInstructions"] {
    color: #9aada4;
}

.stButton > button {
    height: 52px;
    border-radius: 14px;
    border: 1px solid rgba(32, 201, 151, 0.45);
    background: linear-gradient(90deg, #198754, #20a879);
    color: white;
    font-size: 16px;
    font-weight: 700;
    box-shadow: 0 8px 25px rgba(25, 135, 84, 0.18);
    transition: all 0.2s ease;
}

.stButton > button:hover {
    border-color: #65e6b5;
    background: linear-gradient(90deg, #20a879, #20c997);
    transform: translateY(-2px);
    box-shadow: 0 12px 30px rgba(32, 201, 151, 0.20);
}

.result-card {
    margin-top: 20px;
    padding: 18px;
    border-radius: 18px;
    text-align: center;
    color: white;
    box-shadow: 0 12px 30px rgba(0, 0, 0, 0.22);
}

.result-card.fresh {
    background: linear-gradient(135deg, #126b47, #15966a);
    border: 1px solid rgba(101, 230, 181, 0.35);
}

.result-card.rotten {
    background: linear-gradient(135deg, #8f2632, #c73d4d);
    border: 1px solid rgba(255, 150, 160, 0.35);
}

.result-icon {
    font-size: 32px;
}

.result-label {
    font-size: 27px;
    font-weight: 800;
    margin: 2px 0;
}

.result-confidence {
    font-size: 14px;
    color: rgba(255, 255, 255, 0.88);
}

.confidence-title {
    color: #f5f7f6;
    font-size: 19px;
    font-weight: 700;
    margin-top: 24px;
    margin-bottom: 10px;
}

[data-testid="stProgressBar"] > div {
    background-color: #1b3028;
}

[data-testid="stProgressBar"] > div > div {
    background: linear-gradient(90deg, #198754, #20c997);
}

.confidence-text {
    text-align: center;
    color: #8fa39a;
    font-size: 14px;
    margin-top: 8px;
}

.how-title {
    text-align: center;
    color: #f5f7f6;
    font-size: 25px;
    font-weight: 750;
    margin: 45px 0 20px 0;
}

.info-card {
    background: rgba(18, 31, 26, 0.82);
    border: 1px solid rgba(89, 117, 104, 0.25);
    border-radius: 18px;
    padding: 25px 20px;
    text-align: center;
    min-height: 150px;
    box-shadow: 0 12px 30px rgba(0, 0, 0, 0.16);
}

.info-icon {
    font-size: 32px;
    margin-bottom: 8px;
}

.info-title {
    color: #f5f7f6;
    font-size: 17px;
    font-weight: 700;
}

.info-text {
    color: #81958b;
    font-size: 13px;
    line-height: 1.5;
    margin-top: 7px;
}

.footer {
    text-align: center;
    color: #61766c;
    font-size: 13px;
    margin-top: 40px;
    padding-top: 20px;
    border-top: 1px solid rgba(89, 117, 104, 0.15);
}

.stImage img {
    border-radius: 16px;
    border: 1px solid rgba(89, 117, 104, 0.25);
}

.image-preview-box {
    width: 100%;
    height: 295px;
    border-radius: 16px;
    overflow: hidden;
    border: 1px solid rgba(89, 117, 104, 0.25);
    background: #0f1e18;
    display: flex;
    align-items: center;
    justify-content: center;
}

.image-preview-box img {
    width: 100%;
    height: 100%;
    object-fit: contain;
    display: block;
}

</style>
""", unsafe_allow_html=True)

render_html("""
<div class="hero">
    <div class="hero-icon">🍎</div>
    <div class="hero-title">Fruit Freshness <span>Detector</span></div>
    <div class="hero-subtitle">AI-powered fruit freshness detection using deep learning</div>
</div>
""")

@st.cache_resource
def load_model():
    return tf.keras.models.load_model("fruits_classification_model.keras")

model = load_model()

def preprocess_image(image):
    image = image.resize((224, 224))
    image = np.array(image) / 255.0
    image = np.expand_dims(image, axis=0)
    return image

left_col, right_col = st.columns([1, 1], gap="large")

with left_col:
    render_html("""
    <div class="panel">
        <div class="panel-header">
            <div class="panel-icon">📤</div>
            <div class="panel-title">Upload Fruit</div>
        </div>
        <div class="panel-description">
            Upload a clear image of a fruit and let the trained AI model analyze its freshness. 👇
        </div>
    </div>
    """)
    uploaded_file = st.file_uploader(
        "Choose a fruit image",
        type=["jpg", "jpeg", "png"],
        label_visibility="collapsed"
    )
    render_html("""
    <div class="upload-info">
        <b>Supported formats</b> · JPG · JPEG · PNG
    </div>
    """)

with right_col:
    render_html("""
    <div class="section-title">🖼️ Image Preview</div>
    """)
    if uploaded_file is not None:
        image = Image.open(uploaded_file).convert("RGB")
        image_html = image.copy()
        image_html.thumbnail((900, 500))
        import io
        buffer = io.BytesIO()
        image_html.save(buffer, format="PNG")
        import base64
        encoded_image = base64.b64encode(buffer.getvalue()).decode()
        render_html(f"""
        <div class="image-preview-box">
             <img src="data:image/png;base64,{encoded_image}">
        </div>
    """)

    else:
        render_html("""
        <div class="panel preview-panel">
            <div class="empty-preview">
                <div class="empty-icon">🍓</div>
                <div class="empty-text">Your fruit image will appear here</div>
            </div>
        </div>
        """)

if uploaded_file is not None:
    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    if st.button("🔍  Analyze Freshness", use_container_width=True):
        with st.spinner("🧠 Analyzing your fruit..."):
            processed_image = preprocess_image(image)
            prediction = model.predict(processed_image, verbose=0)
            confidence = float(prediction[0][0])
        if confidence > 0.5:
            label = "Rotten"
            emoji = "🔴"
            percentage = confidence * 100
            result_class = "rotten"
        else:
            label = "Fresh"
            emoji = "🟢"
            percentage = (1 - confidence) * 100
            result_class = "fresh"
        render_html(f"""
        <div class="result-card {result_class}">
            <div class="result-icon">{emoji}</div>
            <div class="result-label">{label}</div>
            <div class="result-confidence">Model Confidence · <b>{percentage:.2f}%</b></div>
        </div>
        """)
        render_html("""
        <div class="confidence-title">📊 Prediction Confidence</div>
        """)
        st.progress(int(percentage))
        render_html(f"""
        <div class="confidence-text">
            The model is <b>{percentage:.2f}% confident</b> that this fruit is <b>{label.lower()}</b>.
        </div>
        """)

render_html("""
<div class="how-title">⚙️ How It Works</div>
""")

info1, info2, info3 = st.columns(3, gap="medium")

with info1:
    render_html("""
    <div class="info-card">
        <div class="info-icon">📤</div>
        <div class="info-title">1. Upload</div>
        <div class="info-text">Choose a clear image of the fruit you want to analyze.</div>
    </div>
    """)

with info2:
    render_html("""
    <div class="info-card">
        <div class="info-icon">🧠</div>
        <div class="info-title">2. Analyze</div>
        <div class="info-text">The trained deep learning model processes the uploaded image.</div>
    </div>
    """)

with info3:
    render_html("""
    <div class="info-card">
        <div class="info-icon">🍎</div>
        <div class="info-title">3. Predict</div>
        <div class="info-text">Receive a Fresh or Rotten prediction with confidence.</div>
    </div>
    """)

render_html("""
<div class="footer">
    🍎 Fruit Freshness Detector · TensorFlow · Streamlit
</div>
""")