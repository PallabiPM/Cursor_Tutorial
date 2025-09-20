import os
import io
import requests
from PIL import Image, ImageEnhance
import pytesseract
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure page
st.set_page_config(
    page_title="Nutrition Label Scanner",
    page_icon="🔍",
    layout="centered"
)

# Constants
HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")
if not HUGGINGFACE_API_TOKEN:
    st.error("Please set the HUGGINGFACE_API_TOKEN environment variable")
    st.stop()

API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
HEADERS = {"Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"}

# Check if Tesseract is installed
try:
    pytesseract.get_tesseract_version()
except Exception as e:
    st.error("Error: Tesseract is not installed or not in PATH. Please check the README for installation instructions.")
    st.stop()

@st.cache_data
def preprocess_image(_image):
    """Preprocess image for better OCR results."""
    # Convert to grayscale
    img = _image.convert('L')
    
    # Enhance contrast
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(2.0)
    
    # Enhance sharpness
    enhancer = ImageEnhance.Sharpness(img)
    img = enhancer.enhance(2.0)
    
    # Resize if image is too large
    max_size = 1800
    if max(img.size) > max_size:
        ratio = max_size / max(img.size)
        new_size = tuple(int(dim * ratio) for dim in img.size)
        img = img.resize(new_size, Image.Resampling.LANCZOS)
    
    return img

@st.cache_data
def extract_text(image):
    """Extract text from image using OCR."""
    try:
        text = pytesseract.image_to_string(image)
        return text.strip()
    except Exception as e:
        st.error(f"OCR Error: {str(e)}")
        return None

@st.cache_data
def get_summary(_text):
    """Get summary from Hugging Face API."""
    if not _text:
        return "No text to summarize."
    
    try:
        response = requests.post(
            API_URL,
            headers=HEADERS,
            json={
                "inputs": _text,
                "options": {"wait_for_model": True}
            }
        )
        response.raise_for_status()
        summary = response.json()[0]["summary_text"]
        return summary
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {str(e)}")
        return None

def main():
    st.title("Nutrition Label Scanner")
    st.write("Upload a photo of a nutrition label to extract and summarize its contents.")
    
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        # Display the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        
        with st.spinner("Processing image..."):
            # Preprocess image
            processed_image = preprocess_image(image)
            
            # Extract text
            text = extract_text(processed_image)
            
            if text and len(text.strip()) > 0:
                st.subheader("Extracted Text")
                st.text_area("", text, height=200)
                
                with st.spinner("Generating summary..."):
                    summary = get_summary(text)
                    if summary:
                        st.subheader("AI Summary")
                        st.write(summary)
            else:
                st.warning("No text was extracted from the image. Please try with a clearer image.")

if __name__ == "__main__":
    main()
