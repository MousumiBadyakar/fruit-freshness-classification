import streamlit as st
import numpy as np
import tensorflow as tf
from PIL import Image

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Fruit Freshness Detector",
    page_icon="🍎",
    layout="centered"
)

# -----------------------------
# Custom CSS
# -----------------------------
st.markdown("""
<style>
.main {
    background-color: #f8f9fa;
}
.title {
    text-align: center;
    font-size: 42px;
    font-weight: 700;
    margin-bottom: 5px;
}
.subtitle {
    text-align: center;
    font-size: 18px;
    color: #666;
    margin-bottom: 30px;
}
.result-box {
    padding: 5px 15px;
    border-radius: 10px;
    text-align: center;
    margin-top: 8px;
    color: white !important;
}
.fresh {
    background-color: #198754;
    border: 2px solid #0f5132;
}
.rotten {
    background-color: #dc3545;
    border: 2px solid #b02a37;
}
.result-box h2 {
    color: white !important;
    font-size: 22px;
    margin: 2px 0 4px 0;
}
.result-box h3 {
    color: white !important;
    font-size: 16px;
    margin: 2px 0;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Header
# -----------------------------
st.markdown(
    '<div class="title">🍎 Fruit Freshness Detector</div>',
    unsafe_allow_html=True
)
st.markdown(
    '<div class="subtitle">Upload a fruit image to check whether it is Fresh or Rotten</div>',
    unsafe_allow_html=True
)
st.divider()

# -----------------------------
# Load Model
# -----------------------------
@st.cache_resource
def load_model():
    return tf.keras.models.load_model("fruits_classification_model.keras")

model = load_model()

# -----------------------------
# Image Preprocessing
# -----------------------------
def preprocess_image(image):
    image = image.resize((224, 224))
    image = np.array(image) / 255.0
    image = np.expand_dims(image, axis=0)
    return image

# -----------------------------
# Upload Section
# -----------------------------
st.subheader("📤 Upload Fruit Image")
uploaded_file = st.file_uploader(
    "Choose an image",
    type=["jpg", "jpeg", "png"]
)

# -----------------------------
# Prediction
# -----------------------------
if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(
            image,
            caption="Uploaded Fruit Image",
            width=350
        )
    if st.button("🔍 Check Freshness", use_container_width=True):
        with st.spinner("Analyzing the fruit..."):
            processed_image = preprocess_image(image)
            prediction = model.predict(processed_image, verbose=0)
            confidence = float(prediction[0][0])
        # -----------------------------
        # Prediction Logic
        # -----------------------------
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
        # -----------------------------
        # Result
        # -----------------------------
        st.markdown(
            f"""
            <div class="result-box {result_class}">
                <h2>{emoji} {label}</h2>
                <h3>Confidence: {percentage:.2f}%</h3>
            </div>
            """,
            unsafe_allow_html=True
        )
        # -----------------------------
        # Confidence
        # -----------------------------
        st.markdown(
            "<h3 style='margin-top: 18px; margin-bottom: 5px;'>📊 Prediction Confidence</h3>",
            unsafe_allow_html=True
        )
        st.progress(int(percentage))
        st.write(
            f"The model is **{percentage:.2f}% confident** "
            f"that the fruit is **{label.lower()}**."
        )