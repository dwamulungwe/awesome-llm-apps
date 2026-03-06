import os
import base64
from PIL import Image as PILImage
import streamlit as st
from openai import OpenAI

# -----------------------------
# Configure OpenAI API Key
# -----------------------------
if "OPENAI_API_KEY" not in st.session_state:
    st.session_state.OPENAI_API_KEY = None

with st.sidebar:
    st.title("ℹ️ Configuration")
    
    if not st.session_state.OPENAI_API_KEY:
        api_key = st.text_input(
            "Enter your OpenAI API Key:",
            type="password"
        )
        st.caption(
            "Get your API key from [OpenAI](https://platform.openai.com/account/api-keys) 🔑"
        )
        if api_key:
            st.session_state.OPENAI_API_KEY = api_key
            st.success("API Key saved!")
            st.rerun()
    else:
        st.success("API Key is configured")
        if st.button("🔄 Reset API Key"):
            st.session_state.OPENAI_API_KEY = None
            st.rerun()
    
    st.info(
        "This tool provides AI-powered analysis of medical imaging data using "
        "advanced radiological knowledge."
    )
    st.warning(
        "⚠DISCLAIMER: All analyses should be reviewed by qualified healthcare professionals."
    )

    st.info(
        "This tool was developed by Chinedu David."
    )
# -----------------------------
# GPT-4V Helper
# -----------------------------
def generate_analysis_with_image(prompt, image_path):
    """Send prompt + image to GPT-4V via base64 embedding (OpenAI SDK >=1.0)"""
    if not st.session_state.OPENAI_API_KEY:
        st.error("OpenAI API Key not configured.")
        return ""
    
    client = OpenAI(api_key=st.session_state.OPENAI_API_KEY)

    # Read and encode image
    with open(image_path, "rb") as f:
        image_bytes = f.read()
    image_b64 = base64.b64encode(image_bytes).decode("utf-8")

    # Embed the image in the user prompt
    full_prompt = f"{prompt}\n\nPatient Image (base64 PNG): {image_b64}"

    # GPT-4V chat completion
    response = client.chat.completions.create(
        model="gpt-4.1-mini",  # GPT-4V
        messages=[{"role": "user", "content": full_prompt}],
        max_tokens=1000
    )

    return response.choices[0].message.content

# -----------------------------
# Streamlit App UI
# -----------------------------
st.title("🏥 Medical Imaging Diagnosis Agent")
st.write("Upload a medical image for professional analysis")

upload_container = st.container()
image_container = st.container()
analysis_container = st.container()

# -----------------------------
# GPT Prompt Template
# -----------------------------
query_template = """
You are a highly skilled medical imaging expert with extensive knowledge in radiology and diagnostic imaging. Analyze the patient's medical image provided as a file path: {image_path} and structure your response as follows:

### 1. Image Type & Region
- Specify imaging modality (X-ray/MRI/CT/Ultrasound/etc.)
- Identify the patient's anatomical region and positioning
- Comment on image quality and technical adequacy

### 2. Key Findings
- List primary observations systematically
- Note any abnormalities in the patient's imaging with precise descriptions
- Include measurements and densities where relevant
- Describe location, size, shape, and characteristics
- Rate severity: Normal/Mild/Moderate/Severe

### 3. Diagnostic Assessment
- Provide primary diagnosis with confidence level
- List differential diagnoses in order of likelihood
- Support each diagnosis with observed evidence from the patient's imaging
- Note any critical or urgent findings

### 4. Patient-Friendly Explanation
- Explain the findings in simple, clear language that the patient can understand
- Avoid medical jargon or provide clear definitions
- Include visual analogies if helpful
- Address common patient concerns related to these findings

Format your response using clear markdown headers and bullet points. Be concise yet thorough.
"""

# -----------------------------
# Upload Image
# -----------------------------
with upload_container:
    uploaded_file = st.file_uploader(
        "Upload Medical Image",
        type=["jpg", "jpeg", "png", "dicom"],
        help="Supported formats: JPG, JPEG, PNG, DICOM"
    )

if uploaded_file is not None:
    with image_container:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            image = PILImage.open(uploaded_file)
            width, height = image.size
            aspect_ratio = width / height
            new_width = 500
            new_height = int(new_width / aspect_ratio)
            resized_image = image.resize((new_width, new_height))
            
            st.image(
                resized_image,
                caption="Uploaded Medical Image",
                use_container_width=True
            )
            
            analyze_button = st.button(
                "🔍 Analyze Image",
                type="primary",
                use_container_width=True
            )
    
    with analysis_container:
        if analyze_button:
            if not st.session_state.OPENAI_API_KEY:
                st.warning("Please configure your OpenAI API key in the sidebar.")
            else:
                with st.spinner("🔄 Analyzing image with GPT-4V... Please wait."):
                    try:
                        temp_path = "temp_resized_image.png"
                        resized_image.save(temp_path)
                        
                        # Run GPT-4V analysis
                        result = generate_analysis_with_image(
                            query_template.format(image_path=temp_path),
                            temp_path
                        )
                        
                        st.markdown("### 📋 Analysis Results")
                        st.markdown("---")
                        st.markdown(result)
                        st.markdown("---")
                        st.caption(
                            "Note: This analysis is generated by AI and should be reviewed by "
                            "a qualified healthcare professional."
                        )
                    except Exception as e:
                        st.error(f"Analysis error: {e}")
else:
    st.info("👆 Please upload a medical image to begin analysis")