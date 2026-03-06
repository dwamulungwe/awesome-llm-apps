import os
from PIL import Image as PILImage
import streamlit as st

# -----------------------------
# Streamlit Page Config
# -----------------------------
st.set_page_config(
    page_title="OmniScan AI",
    page_icon="🏥",
    layout="centered"
)

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    st.title("ℹ️ Configuration")
    st.info(
        "OmniScan AI is an AI-assisted medical imaging prototype designed to support "
        "radiologists and clinicians in reviewing medical scans."
    )
    st.warning(
        "⚠ DISCLAIMER: This tool is for assistance only and must not be used as a "
        "standalone diagnostic system. All results must be reviewed by a qualified "
        "healthcare professional."
    )
    st.info("Developed by Chinedu David")

# -----------------------------
# Local Placeholder Report
# -----------------------------
def generate_local_report(filename: str) -> str:
    extension = os.path.splitext(filename)[1].lower()

    modality_map = {
        ".png": "Medical Image",
        ".jpg": "Medical Image",
        ".jpeg": "Medical Image",
        ".dicom": "DICOM Scan",
        ".dcm": "DICOM Scan"
    }

    modality = modality_map.get(extension, "Uploaded Scan")

    report = f"""
### 1. Image Type & Region
- **Imaging Modality:** {modality}
- **Anatomical Region:** Not yet automatically identified
- **Technical Quality:** Image uploaded successfully and available for review

### 2. Key Findings
- The scan has been uploaded and displayed successfully.
- Automated diagnostic analysis is currently **disabled** in this deployment.
- No machine learning model is currently connected in this version.
- This version is intended for interface testing and workflow development.

### 3. Diagnostic Assessment
- **Primary Assessment:** No automated diagnosis available
- **Confidence Level:** Not applicable
- **Differential Diagnoses:** Not generated in this version
- **Critical Findings:** Not assessed automatically

### 4. Patient-Friendly Explanation
- Your medical scan has been uploaded successfully.
- This current version of OmniScan AI is not yet performing live AI analysis.
- A radiologist or qualified doctor should review the image and provide the medical interpretation.

### 5. System Note
- OmniScan AI is being developed as an **AI-assisted radiology support platform**.
- Final diagnosis and treatment decisions must always be made by a licensed medical professional.
"""
    return report

# -----------------------------
# Main UI
# -----------------------------
st.title("🏥 OmniScan AI")
st.write("Upload a medical image for assisted review")

upload_container = st.container()
image_container = st.container()
analysis_container = st.container()

# -----------------------------
# Upload Image
# -----------------------------
with upload_container:
    uploaded_file = st.file_uploader(
        "Upload Medical Image",
        type=["jpg", "jpeg", "png", "dicom", "dcm"],
        help="Supported formats: JPG, JPEG, PNG, DICOM, DCM"
    )

if uploaded_file is not None:
    with image_container:
        try:
            col1, col2, col3 = st.columns([1, 2, 1])

            with col2:
                image = PILImage.open(uploaded_file)
                width, height = image.size
                aspect_ratio = width / height if height != 0 else 1
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

        except Exception:
            st.error(
                "This file could not be displayed as an image in the current version. "
                "If it is a DICOM file, DICOM processing still needs to be implemented."
            )
            analyze_button = False

    with analysis_container:
        if analyze_button:
            with st.spinner("🔄 Generating OmniScan AI report..."):
                try:
                    result = generate_local_report(uploaded_file.name)

                    st.markdown("### 📋 Analysis Results")
                    st.markdown("---")
                    st.markdown(result)
                    st.markdown("---")
                    st.caption(
                        "Note: This is a placeholder assistive report. "
                        "Automated AI model inference is not yet enabled."
                    )
                except Exception as e:
                    st.error(f"Analysis error: {e}")
else:
    st.info("👆 Please upload a medical image to begin")
