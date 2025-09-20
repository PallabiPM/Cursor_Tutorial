# NutriScan - AI Nutrition Label Analyzer

A modern web application that uses OCR and AI to analyze nutrition labels and provide easy-to-understand summaries.

## Features

- 📸 Mobile-friendly image upload
- 🔍 Advanced image preprocessing for better OCR accuracy
- 📝 Text extraction using Tesseract OCR
- 🤖 AI-powered summarization using Mistral AI
- 💅 Clean, modern user interface
- 🚀 Instant health insights

## Prerequisites

1. Python 3.8+
2. Tesseract OCR
3. Mistral AI API key

### Installing Tesseract OCR

#### Windows
1. Download the installer from [UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki)
2. Run the installer
3. Add the Tesseract installation directory to your PATH (typically `C:\Program Files\Tesseract-OCR`)

#### macOS
```bash
brew install tesseract
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
```

### Setting Up Mistral AI API Key

1. Create an account at [Mistral AI](https://console.mistral.ai/)
2. Generate an API key from your dashboard
3. Set the API key as an environment variable:

**Windows (PowerShell)**
```powershell
$env:MISTRAL_API_KEY="your_api_key_here"
```

**Windows (Command Prompt)**
```cmd
set MISTRAL_API_KEY=your_api_key_here
```

**macOS/Linux**
```bash
export MISTRAL_API_KEY=your_api_key_here
```

For persistent storage, add the API key to your environment variables or create a `.env` file in the project root:
```env
MISTRAL_API_KEY=your_api_key_here
```

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/nutriscan.git
cd nutriscan
```

2. Create and activate a virtual environment:
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up your environment variables as described above

## Running the Application

1. Start the Streamlit app:
```bash
streamlit run app.py
```

2. Open your browser and navigate to http://localhost:8501

## Usage

1. Upload a nutrition label photo
2. Click "Analyze" to process the image
3. View the AI-generated summary and health insights

## Troubleshooting

### Common Issues

1. **Tesseract not found error**
   - Verify Tesseract is installed
   - Check if the Tesseract path is in your system's PATH
   - On Windows, you might need to set the path explicitly

2. **API Key Error**
   - Ensure MISTRAL_API_KEY is set in your environment variables
   - Check that the API key is valid
   - Verify your internet connection

3. **Poor OCR Results**
   - Use a clear, well-lit photo
   - Ensure the label is properly oriented
   - Try to avoid glare or shadows

## License

MIT License