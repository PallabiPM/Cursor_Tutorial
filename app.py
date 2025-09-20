import os
import re
import json
import numpy as np
import requests
from PIL import Image, ImageEnhance
import pytesseract
import streamlit as st
from dotenv import load_dotenv

# Load environment variables first
load_dotenv()

# Configure page with custom theme
st.set_page_config(
    page_title="NutriScan - AI Nutrition Label Analyzer",
    page_icon="🥗",
    layout="centered",
    initial_sidebar_state="collapsed",
    menu_items={
        'About': "# NutriScan\nAI-Powered Nutrition Label Analysis\n\nMade with ❤️ for better nutrition.",
        'Report a bug': "https://github.com/yourusername/nutriscan/issues",
        'Get help': "https://github.com/yourusername/nutriscan#readme"
    }
)

# Enhanced CSS with Healthline-inspired styling
st.markdown("""
<style>
    /* Modern color palette */
    :root {
        --primary: #2AAA8A;
        --primary-light: #E6F6F0;
        --secondary: #2D3748;
        --accent: #F7FAFC;
        --success: #38A169;
        --warning: #DD6B20;
        --error: #E53E3E;
        --text: #1A202C;
        --text-light: #4A5568;
        --border: #E2E8F0;
    }

    /* Global styles */
    .stApp {
        background: linear-gradient(135deg, var(--primary-light) 0%, #ffffff 100%);
    }

    /* Remove default Streamlit container padding and background */
    .main > div:first-child {
        padding-top: 0;
        padding-bottom: 0;
    }

    .main .block-container {
        padding-top: 0;
        padding-bottom: 0;
        max-width: 100%;
    }

    /* Remove white background from main content */
    .css-1d391kg, .css-12oz5g7 {
        background: none;
    }

    section[data-testid="stSidebar"] {
        background: white;
        border-right: 1px solid var(--border);
    }

    /* Typography */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Helvetica Neue', sans-serif;
        color: var(--secondary);
    }

    p {
        font-family: -apple-system, system-ui, sans-serif;
        color: var(--text);
        line-height: 1.6;
    }

    /* Header/Navigation */
    .app-header {
        background: transparent;
        padding: 2rem;
        margin-bottom: 1rem;
        text-align: center;
    }

    .app-title {
        color: var(--primary);
        font-size: 1.8rem;
        font-weight: 700;
        margin: 0;
    }

    .app-subtitle {
        color: var(--text-light);
        font-size: 1.1rem;
        margin-top: 0.5rem;
    }

    /* Content Cards */
    .content-card {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin: 1.5rem 0;
        border: 1px solid var(--border);
    }

    /* Welcome Section */
    .welcome-section {
        text-align: center;
        padding: 2rem 1rem;
        max-width: 800px;
        margin: 0 auto;
        background: transparent;
    }

    .welcome-title {
        font-size: 2.5rem;
        color: var(--primary);
        margin-bottom: 1rem;
        line-height: 1.2;
    }

    .welcome-subtitle {
        font-size: 1.2rem;
        color: var(--text-light);
        margin-bottom: 2rem;
    }

    /* Upload Zone */
    .upload-zone {
        border: 2px dashed var(--primary);
        border-radius: 12px;
        padding: 2rem;
        text-align: center;
        background: var(--primary-light);
        transition: all 0.3s ease;
    }

    .upload-zone:hover {
        border-color: var(--primary);
        background: white;
    }

    /* Buttons */
    .stButton > button {
        background: var(--primary) !important;
        color: white !important;
        padding: 0.75rem 2rem !important;
        border-radius: 25px !important;
        border: none !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(42, 170, 138, 0.2);
    }

    .stButton > button:disabled {
        background: var(--border) !important;
        cursor: not-allowed;
    }

    /* Progress/Loading */
    .stProgress > div > div {
        background-color: var(--primary);
    }

    /* Success Messages */
    .success-message {
        background: var(--primary-light);
        color: var(--primary);
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid var(--primary);
        margin: 1rem 0;
    }

    /* Health Flags */
    .health-flags {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin: 1rem 0;
    }

    .health-flag {
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 500;
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
    }

    .health-flag.positive {
        background: #F0FFF4;
        color: var(--success);
        border: 1px solid #9AE6B4;
    }

    .health-flag.warning {
        background: #FFFAF0;
        color: var(--warning);
        border: 1px solid #FBD38D;
    }

    .health-flag.info {
        background: #EBF8FF;
        color: #3182CE;
        border: 1px solid #BEE3F8;
    }

    /* Summary Section */
    .summary-section {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-top: 2rem;
    }

    .summary-header {
        color: var(--primary);
        font-size: 1.5rem;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid var(--primary-light);
    }

    /* Footer */
    .app-footer {
        text-align: center;
        padding: 2rem;
        color: var(--text-light);
        font-size: 0.9rem;
        margin-top: 3rem;
        border-top: 1px solid var(--border);
    }

    /* Sidebar */
    .css-1d391kg {
        background-color: var(--accent);
    }

    /* Hide dev-mode hamburger menu */
    .stApp > header {
        display: none !important;
    }

    /* Responsive adjustments */
    @media (max-width: 768px) {
        .welcome-title {
            font-size: 2rem;
        }
        .content-card {
            padding: 1.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Constants
MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"
MISTRAL_MODEL = "mistral-small-latest"

# Nutrient thresholds (per 100g)
THRESHOLDS = {
    'sugars': {'high': 22.5, 'moderate': 5.0},
    'fat': {'high': 17.5, 'moderate': 3.0},
    'saturates': {'high': 5.0},
    'salt': {'high': 1.5}
}

def preprocess_image(image):
    """Enhanced image preprocessing for better OCR results."""
    # Convert to grayscale
    img = image.convert('L')
    
    # Enhance contrast
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(2.0)
    
    # Enhance sharpness
    enhancer = ImageEnhance.Sharpness(img)
    img = enhancer.enhance(2.0)
    
    # Resize if image is too large
    max_size = 1800
    width, height = img.size
    if max(width, height) > max_size:
        ratio = max_size / max(width, height)
        new_size = (int(width * ratio), int(height * ratio))
        img = img.resize(new_size, Image.Resampling.LANCZOS)
    
    return img

def clean_ocr_text(text):
    """Clean and normalize OCR output."""
    # Remove junk characters but keep %
    text = re.sub(r'[^\w\s.,%()-]', '', text)
    
    # Join hyphenated words
    text = re.sub(r'(\w)-\s*\n\s*(\w)', r'\1\2', text)
    
    # Normalize spaces and newlines
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\n\s*\n', '\n', text)
    
    return text.strip()

def extract_text(image):
    """Extract text from image using enhanced OCR."""
    try:
        text = pytesseract.image_to_string(image)
        return text.strip()
    except Exception as e:
        st.error(f"OCR Error: {str(e)}")
        return None

def safe_float_convert(value_str):
    """Safely convert string to float, handling various formats."""
    try:
        clean_str = re.sub(r'[^\d.,]', '', value_str)
        clean_str = clean_str.replace(',', '.')
        return float(clean_str)
    except (ValueError, TypeError):
        return None

def parse_nutrition_table(text):
    """Parse nutrition information using regex."""
    nutrients = {}
    
    # Updated patterns to match common formats
    patterns = {
        'calories': r'Calories[:\s]*(\d+)',
        'total_fat': r'Total Fat[:\s]*(\d+\.?\d*)g',
        'saturated_fat': r'Saturated Fat[:\s]*(\d+\.?\d*)g',
        'trans_fat': r'Trans Fat[:\s]*(\d+\.?\d*)g',
        'cholesterol': r'Cholesterol[:\s]*(\d+)mg',
        'sodium': r'Sodium[:\s]*(\d+)mg',
        'total_carbohydrate': r'Total Carbohydrate[s]?[:\s]*(\d+\.?\d*)g',
        'dietary_fiber': r'Dietary Fiber[:\s]*(\d+\.?\d*)g',
        'total_sugars': r'Total Sugars[:\s]*(\d+\.?\d*)g',
        'added_sugars': r'Added Sugars[:\s]*(\d+\.?\d*)g',
        'protein': r'Protein[:\s]*(\d+\.?\d*)g',
        'vitamin_d': r'Vitamin D[:\s]*(\d+\.?\d*)\s*(?:mcg|µg)',
        'calcium': r'Calcium[:\s]*(\d+)mg',
        'iron': r'Iron[:\s]*(\d+\.?\d*)mg',
        'potassium': r'Potassium[:\s]*(\d+)mg'
    }
    
    # Extract serving information
    serving_size_match = re.search(r'Serving size[:\s]*([\d/]+)\s*([a-zA-Z]+)\s*\((\d+)g\)', text, re.IGNORECASE)
    if serving_size_match:
        nutrients['serving_size'] = {
            'amount': serving_size_match.group(1),
            'unit': serving_size_match.group(2),
            'grams': int(serving_size_match.group(3))
        }
    
    servings_match = re.search(r'(\d+)\s*servings? per container', text, re.IGNORECASE)
    if servings_match:
        nutrients['servings_per_container'] = int(servings_match.group(1))
    
    # Extract nutrients
    for nutrient, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            value = safe_float_convert(match.group(1))
            if value is not None:
                nutrients[nutrient] = {'value': value}
                
                # Look for % Daily Value
                dv_pattern = f"{pattern}.*?(\d+)%"
                dv_match = re.search(dv_pattern, text, re.IGNORECASE)
                if dv_match and len(dv_match.groups()) > 1:
                    nutrients[nutrient]['daily_value_percent'] = safe_float_convert(dv_match.group(2))
    
    return nutrients

def compute_health_flags(nutrients):
    """Compute health flags based on nutrient values."""
    flags = []
    
    if 'total_sugars' in nutrients:
        value = nutrients['total_sugars']['value']
        if value >= THRESHOLDS['sugars']['high']:
            flags.append("⚠️ High in sugar")
        elif value >= THRESHOLDS['sugars']['moderate']:
            flags.append("⚠️ Moderate sugar content")
    
    if 'total_fat' in nutrients:
        value = nutrients['total_fat']['value']
        if value >= THRESHOLDS['fat']['high']:
            flags.append("⚠️ High in fat")
        elif value >= THRESHOLDS['fat']['moderate']:
            flags.append("⚠️ Moderate fat content")
    
    if 'saturated_fat' in nutrients:
        if nutrients['saturated_fat']['value'] >= THRESHOLDS['saturates']['high']:
            flags.append("⚠️ High in saturated fat")
    
    if 'sodium' in nutrients:
        sodium_g = nutrients['sodium']['value'] / 1000  # Convert mg to g
        if sodium_g >= THRESHOLDS['salt']['high']:
            flags.append("⚠️ High in sodium")
    
    # Add protein assessment
    if 'protein' in nutrients:
        if nutrients['protein']['value'] < 5:
            flags.append("ℹ️ Low in protein")
        else:
            flags.append("✅ Good source of protein")
    
    # Add vitamin and mineral assessments
    if 'calcium' in nutrients and nutrients['calcium'].get('daily_value_percent', 0) >= 20:
        flags.append("✅ Good source of calcium")
    
    if 'iron' in nutrients and nutrients['iron'].get('daily_value_percent', 0) >= 20:
        flags.append("✅ Good source of iron")
    
    return flags

def build_mistral_prompt(nutrients, flags):
    """Build a structured prompt for Mistral AI."""
    system_message = """You are a nutrition expert assistant who explains nutrition facts in a clear, friendly way. Your task is to:

1. ALWAYS start with the serving size in grams
2. Explain % Daily Values in simple terms (e.g., "20% of your daily needs")
3. Provide 2-4 clear bullet points covering:
   - Calories and main macronutrients (carbs, fat, protein)
   - Sugar and sodium levels
   - Important vitamins and minerals
   - Any health flags (high/low nutrients)
4. End with one practical, actionable tip for consumers

Keep your tone friendly but cautious, and make the information easy to scan and understand.
Avoid technical jargon - write as if explaining to a friend."""
    
    # Create a structured nutrition facts summary
    nutrition_summary = "Nutrition Facts Summary:\n\n"
    
    # Always put serving size first if available
    if 'serving_size' in nutrients:
        nutrition_summary += f"Serving Size: {nutrients['serving_size']['amount']} {nutrients['serving_size']['unit']} ({nutrients['serving_size']['grams']}g)\n"
    if 'servings_per_container' in nutrients:
        nutrition_summary += f"Servings per Container: {nutrients['servings_per_container']}\n"
    
    # Group nutrients by category for better organization
    categories = {
        'Main Nutrients': ['calories', 'total_fat', 'saturated_fat', 'trans_fat', 'total_carbohydrate', 'protein'],
        'Sugars and Fiber': ['total_sugars', 'added_sugars', 'dietary_fiber'],
        'Minerals': ['sodium', 'potassium', 'calcium', 'iron'],
        'Vitamins': ['vitamin_d']
    }
    
    for category, nutrient_list in categories.items():
        relevant_nutrients = [n for n in nutrient_list if n in nutrients]
        if relevant_nutrients:
            nutrition_summary += f"\n{category}:\n"
            for nutrient in relevant_nutrients:
                data = nutrients[nutrient]
                if isinstance(data, dict) and 'value' in data:
                    nutrition_summary += f"- {nutrient.replace('_', ' ').title()}: {data['value']}"
                    if 'daily_value_percent' in data:
                        nutrition_summary += f" ({data['daily_value_percent']}% Daily Value)"
                    nutrition_summary += "\n"
    
    if flags:
        nutrition_summary += "\nHealth Considerations:\n"
        for flag in flags:
            nutrition_summary += f"- {flag}\n"
    
    user_message = f"""Please analyze these nutrition facts and create a consumer-friendly summary:

{nutrition_summary}

Requirements for your response:
1. Start by clearly stating the serving size in grams
2. When mentioning Daily Values, explain them in simple terms (e.g., "provides 20% of what you need in a day")
3. Provide 2-4 bullet points covering the key nutrients and health considerations
4. End with one practical tip for healthy consumption

Make your summary easy to read and understand, highlighting the most important information first."""
    
    return system_message, user_message

def get_mistral_summary(system_message, user_message, api_key):
    """Get summary from Mistral AI API."""
    if not api_key:
        st.error("Please enter your Mistral AI API key in the sidebar")
        return None
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        # Clean and encode messages to handle special characters
        def clean_text(text):
            # Remove or replace problematic characters
            text = text.encode('ascii', 'ignore').decode('ascii')
            # Normalize whitespace
            text = ' '.join(text.split())
            return text
        
        clean_system_message = clean_text(system_message)
        clean_user_message = clean_text(user_message)
        
        # Prepare the API request
        payload = {
            "model": MISTRAL_MODEL,
            "messages": [
                {"role": "system", "content": clean_system_message},
                {"role": "user", "content": clean_user_message}
            ],
            "temperature": 0.3,
            "max_tokens": 300
        }
        
        # Make the API call
        response = requests.post(
            MISTRAL_API_URL,
            headers=headers,
            json=payload,
            timeout=30
        )
        
        # Handle response status
        if response.status_code == 401:
            st.error("Invalid API key. Please check your Mistral AI API key in the sidebar.")
            return None
        elif response.status_code != 200:
            st.error(f"API Error: Status code {response.status_code}")
            st.error("Response content:")
            try:
                st.json(response.json())
            except:
                st.error(response.text)
            return None
        
        # Parse the response
        try:
            result = response.json()
            if "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0]["message"]["content"]
            else:
                st.error("Unexpected API response format")
                st.json(result)
                return None
        except Exception as e:
            st.error(f"Error parsing API response: {str(e)}")
            st.error(f"Raw response: {response.text}")
            return None
            
    except requests.exceptions.Timeout:
        st.error("Request timed out. Please try again.")
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"Network error: {str(e)}")
        return None
    except Exception as e:
        st.error(f"Error generating summary: {str(e)}")
        if 'response' in locals():
            st.error(f"Response content: {response.text}")
        return None

def render_header():
    """Render the app header with branding."""
    st.markdown("""
    <div class="app-header">
        <h1 class="app-title">🥗 NutriScan</h1>
        <p class="app-subtitle">AI-Powered Nutrition Label Analysis</p>
    </div>
    """, unsafe_allow_html=True)

def render_welcome_screen():
    """Render the welcome screen with introduction."""
    st.markdown("""
    <div class="welcome-section">
        <h1 class="welcome-title">Understand Your Food's Nutrition Facts</h1>
        <p class="welcome-subtitle">
            Upload a photo of any nutrition label and get an instant, AI-powered analysis 
            that helps you make informed decisions about your food choices.
        </p>
    </div>
    """, unsafe_allow_html=True)

def render_upload_section():
    """Render the file upload section."""
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Upload a nutrition label image",
        type=["jpg", "jpeg", "png"],
        help="Supported formats: JPG, JPEG, PNG",
        label_visibility="collapsed"
    )
    st.markdown("""
    <p style="text-align: center; color: var(--text-light); margin-top: 1rem;">
        📸 Take a clear photo of any nutrition label
    </p>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    return uploaded_file

def render_success_upload(image):
    """Render the success message and image preview after upload."""
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(image, caption="", use_column_width=True)
    with col2:
        st.markdown("""
        <div class="success-message">
            <h4 style="margin: 0;">✅ Image Upload Successful!</h4>
            <p style="margin: 0.5rem 0 0 0;">Click 'Analyze' to process the nutrition label.</p>
        </div>
        """, unsafe_allow_html=True)

def render_health_flags(flags):
    """Render health flags with improved styling."""
    st.markdown("<div class='health-flags'>", unsafe_allow_html=True)
    for flag in flags:
        flag_class = (
            "positive" if "✅" in flag 
            else "warning" if "⚠️" in flag 
            else "info"
        )
        st.markdown(f"""
        <div class="health-flag {flag_class}">
            {flag}
        </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

def render_summary_section(nutrients, flags, summary):
    """Render the nutrition summary section."""
    st.markdown("""
    <div class="summary-section">
        <h2 class="summary-header">📊 Nutrition Analysis</h2>
    """, unsafe_allow_html=True)
    
    # Display serving size if available
    if 'serving_size' in nutrients:
        st.markdown(f"""
        <div style="background: var(--accent); padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
            <h4 style="color: var(--secondary); margin: 0;">Serving Size</h4>
            <p style="color: var(--text); font-size: 1.2rem; margin: 0.5rem 0 0 0;">
                {nutrients['serving_size']['amount']} {nutrients['serving_size']['unit']} 
                ({nutrients['serving_size']['grams']}g)
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Display health flags
    if flags:
        st.markdown("<h3>🚦 Health Indicators</h3>", unsafe_allow_html=True)
        render_health_flags(flags)
    
    # Display AI summary
    st.markdown("<h3>💡 Key Insights</h3>", unsafe_allow_html=True)
    st.write(summary)
    
    st.markdown("</div>", unsafe_allow_html=True)

def render_footer():
    """Render the app footer."""
    st.markdown("""
    <div class="app-footer">
        <p>Powered by OCR Technology & AI | Made with ❤️ for better nutrition</p>
        <p style="font-size: 0.8rem; margin-top: 0.5rem;">
            © 2025 NutriScan | <a href="#" style="color: var(--primary);">Terms</a> | 
            <a href="#" style="color: var(--primary);">Privacy</a>
        </p>
    </div>
    """, unsafe_allow_html=True)

def main():
    # Get API key from environment variables
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        st.error("⚠️ Mistral AI API key not found. Please set the MISTRAL_API_KEY environment variable.")
        st.stop()
    
    # Render header
    render_header()
    
    # Welcome screen
    render_welcome_screen()
    
    # Upload section
    uploaded_file = render_upload_section()
    
    if uploaded_file is not None:
        # Process uploaded image
        image = Image.open(uploaded_file)
        render_success_upload(image)
        
        # Analyze button
        if st.button("🔍 Analyze Nutrition Label", key="analyze_btn"):
            with st.spinner("Processing your nutrition label..."):
                # Process image (OCR)
                processed_image = preprocess_image(image)
                raw_text = extract_text(processed_image)
                
                if raw_text:
                    cleaned_text = clean_ocr_text(raw_text)
                    nutrients = parse_nutrition_table(cleaned_text)
                    
                    if nutrients:
                        # Compute health flags
                        flags = compute_health_flags(nutrients)
                        
                        # Generate AI summary
                        with st.spinner("Generating insights..."):
                            system_msg, user_msg = build_mistral_prompt(nutrients, flags)
                            summary = get_mistral_summary(system_msg, user_msg, api_key)
                            
                            if summary:
                                # Show thank you message
                                st.markdown("""
                                <div class="success-message" style="text-align: center;">
                                    <h3 style="margin: 0;">✨ Analysis Complete!</h3>
                                    <p style="margin: 0.5rem 0 0 0;">
                                        Here's your personalized nutrition summary.
                                    </p>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                # Render summary section
                                render_summary_section(nutrients, flags, summary)
                            else:
                                st.error("Unable to generate summary. Please check your API key and try again.")
                    else:
                        st.error("😕 Couldn't read the nutrition information. Please try uploading a clearer photo.")
                else:
                    st.error("📸 Image quality too low. Please try uploading a well-lit, clear photo.")
    
    # Footer
    render_footer()

if __name__ == "__main__":
    try:
        # Check if Tesseract is installed
        try:
            pytesseract.get_tesseract_version()
        except Exception as e:
            st.error("⚠️ Tesseract OCR is not installed. Please check the README for installation instructions.")
            st.stop()
        
        # Run main application
        main()
        
    except Exception as e:
        st.error("⚠️ Application error occurred")
        import traceback
        st.code(traceback.format_exc())