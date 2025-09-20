import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API token
api_token = os.getenv("HUGGINGFACE_API_TOKEN")
if not api_token:
    print("Error: HUGGINGFACE_API_TOKEN not found in .env file")
    exit(1)

# API configuration
API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
HEADERS = {"Authorization": f"Bearer {api_token}"}

# Sample nutrition label text
sample_text = """
Nutrition Facts
Serving Size 1 cup (228g)
Amount Per Serving
Calories 250
Total Fat 12g
Saturated Fat 3g
Trans Fat 0g
Cholesterol 30mg
Sodium 470mg
Total Carbohydrate 31g
Dietary Fiber 0g
Total Sugars 5g
Protein 5g
"""

# Test API
print("Testing Hugging Face API connection...")
try:
    response = requests.post(
        API_URL,
        headers=HEADERS,
        json={
            "inputs": sample_text,
            "options": {"wait_for_model": True}
        }
    )
    response.raise_for_status()
    summary = response.json()[0]["summary_text"]
    print("\nAPI Test Successful! ✅")
    print("\nSample Text Summary:")
    print("-" * 50)
    print(summary)
    print("-" * 50)
except requests.exceptions.RequestException as e:
    print(f"\nAPI Test Failed! ❌")
    print(f"Error: {str(e)}")
