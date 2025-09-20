# Nutrition Label Scanner

A Streamlit web application that uses OCR to extract text from nutrition labels and provides an AI-generated summary using the Hugging Face BART model.

## Features

- Mobile-friendly image upload
- Image preprocessing for better OCR accuracy
- Text extraction using Tesseract OCR
- AI-powered summarization using facebook/bart-large-cnn
- Clean, user-friendly interface

## Prerequisites

1. Python 3.8+
2. Tesseract OCR binary
3. Hugging Face API token

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

### Getting a Hugging Face API Token

1. Create an account at [Hugging Face](https://huggingface.co)
2. Go to your profile settings
3. Navigate to "Access Tokens"
4. Create a new token with read access
5. Copy the token

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/nutrition-label-scanner.git
cd nutrition-label-scanner
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

4. Create a `.env` file in the project root and add your Hugging Face API token:
```
HUGGINGFACE_API_TOKEN=your_token_here
```

## Running the Application

1. Start the Streamlit app:
```bash
streamlit run app.py
```

2. Open your browser and navigate to the URL shown in the terminal (typically http://localhost:8501)

## Usage

1. Upload an image of a nutrition label using the file uploader
2. The app will preprocess the image and extract text using OCR
3. The extracted text will be displayed in a scrollable box
4. An AI-generated summary will appear below the extracted text

## Troubleshooting

### Common Issues

1. **Tesseract not found error**
   - Verify Tesseract is installed
   - Check if the Tesseract path is correctly set in your system's PATH variable
   - On Windows, you may need to set the path explicitly in the code

2. **Poor OCR Results**
   - Ensure the image is clear and well-lit
   - Try adjusting the image preprocessing parameters
   - Make sure the text in the image is properly oriented

3. **API Errors**
   - Verify your Hugging Face API token is correct
   - Check your internet connection
   - The model might be loading if it's the first request (cold start)

## License

MIT License
