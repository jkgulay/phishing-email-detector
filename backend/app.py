from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for Vue frontend

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Load the trained model and vectorizer
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'models', 'random_forest_model.pkl')
VECTORIZER_PATH = os.path.join(os.path.dirname(__file__), 'models', 'tfidf_vectorizer.pkl')

model = None
tfidf = None

def load_model():
    global model, tfidf
    try:
        with open(MODEL_PATH, 'rb') as f:
            model = pickle.load(f)
        with open(VECTORIZER_PATH, 'rb') as f:
            tfidf = pickle.load(f)
        print("Model and vectorizer loaded successfully!")
    except FileNotFoundError:
        print("Warning: Model files not found. Please train and save the model first.")

load_model()

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None and tfidf is not None
    })

@app.route('/predict', methods=['POST'])
def predict():
    """Predict if an email is phishing or safe"""
    try:
        data = request.get_json()
        email_text = data.get('email_text', '')
        
        if not email_text:
            return jsonify({'error': 'Email text is required'}), 400
        
        if model is None or tfidf is None:
            return jsonify({'error': 'Model not loaded'}), 500
        
        # Vectorize the text
        text_vectorized = tfidf.transform([email_text]).toarray()
        
        # Make prediction
        prediction = model.predict(text_vectorized)[0]
        prediction_proba = model.predict_proba(text_vectorized)[0]
        
        # Get confidence scores
        confidence_safe = float(prediction_proba[0])
        confidence_phishing = float(prediction_proba[1])
        
        # Determine result
        is_phishing = bool(prediction == 1)
        result_message = "⚠️ WARNING: PHISHING DETECTED!" if is_phishing else "✅ Email is Safe."
        
        return jsonify({
            'prediction': int(prediction),
            'is_phishing': is_phishing,
            'message': result_message,
            'confidence': {
                'safe': round(confidence_safe * 100, 2),
                'phishing': round(confidence_phishing * 100, 2)
            }
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/analyze', methods=['POST'])
def analyze_with_ai():
    """Analyze email with AI and provide detailed suggestions"""
    try:
        data = request.get_json()
        email_text = data.get('email_text', '')
        prediction_result = data.get('prediction_result', {})
        
        if not email_text:
            return jsonify({'error': 'Email text is required'}), 400
        
        # Create prompt for AI analysis
        is_phishing = prediction_result.get('is_phishing', False)
        confidence = prediction_result.get('confidence', {})
        
        prompt = f"""You are a cybersecurity expert analyzing an email for phishing indicators.

Email Content:
{email_text}

Our ML Model Prediction:
- Classification: {'PHISHING' if is_phishing else 'SAFE'}
- Confidence: {confidence.get('phishing', 0)}% phishing, {confidence.get('safe', 0)}% safe

Please provide:
1. A detailed analysis of phishing indicators or safety markers in this email
2. Specific red flags or positive signs you notice
3. Practical recommendations for the user
4. Educational insights about this type of email

Keep your response concise but informative (max 300 words)."""

        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a cybersecurity expert specializing in phishing detection and email security."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        ai_analysis = response.choices[0].message.content
        
        return jsonify({
            'analysis': ai_analysis,
            'model_used': 'gpt-4o-mini'
        })
    
    except Exception as e:
        return jsonify({'error': f'AI analysis failed: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
