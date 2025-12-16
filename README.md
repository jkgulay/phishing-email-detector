# Phishing Email Detector Web Application

A full-stack web application that uses Machine Learning (Random Forest) and AI (OpenAI GPT-4o-mini) to detect phishing emails and provide detailed security analysis.

## 🚀 Features

- **ML-Powered Detection**: Random Forest classifier trained on phishing email datasets
- **Real-time Analysis**: Instant predictions with confidence scores
- **AI Expert Analysis**: Detailed insights and recommendations from GPT-4o-mini
- **Modern UI**: Clean, responsive interface built with Vue 3 and Vuetify
- **Interactive Visualization**: Confidence scores displayed as progress circles

## 📁 Project Structure

```
IT113_Final_Project/
├── backend/
│   ├── app.py                      # Flask API server
│   ├── train_and_save_model.py     # Model training script
│   ├── requirements.txt            # Python dependencies
│   ├── .env               # Environment variables template
│   └── models/                    # Saved ML models (created after training)
├── frontend/
│   ├── src/
│   │   ├── App.vue               # Main Vue component
│   │   └── main.js               # Vue app initialization
│   ├── index.html                # HTML entry point
│   ├── package.json              # Node dependencies
│   └── vite.config.js            # Vite configuration
├── data/                         # Email datasets
└── notebooks/                    # Jupyter notebooks
```

## 🛠️ Setup Instructions

### Prerequisites

- Python 3.8+
- Node.js 18+
- OpenAI API Key (get one at https://platform.openai.com)

### Backend Setup

1. **Navigate to backend directory:**

   ```bash
   cd backend
   ```

2. **Install Python dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**

   ```bash
   cp .env.example .env
   ```

   Edit `.env` and add your OpenAI API key:

   ```
   OPENAI_API_KEY=sk-your-actual-api-key-here
   ```

4. **Train and save the model:**

   ```bash
   python train_and_save_model.py
   ```

   This will create the `models/` directory with:

   - `random_forest_model.pkl`
   - `tfidf_vectorizer.pkl`

5. **Start the Flask server:**
   ```bash
   python app.py
   ```
   Backend will run on http://localhost:5000

### Frontend Setup

1. **Navigate to frontend directory:**

   ```bash
   cd frontend
   ```

2. **Install Node dependencies:**

   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm run dev
   ```
   Frontend will run on http://localhost:3000

## 🎯 Usage

1. Open your browser and go to http://localhost:3000
2. Paste an email content into the text area
3. Click "Analyze Email" to get ML prediction
4. Click "Get AI-Powered Detailed Analysis" for expert insights
5. Review the results:
   - ✅ Safe or ⚠️ Phishing classification
   - Confidence scores for both outcomes
   - Detailed AI analysis with recommendations

## 🧪 Example Email

Try this example phishing email:

```
URGENT: Your account is suspended. Click here to verify: http://bit.ly/fake

Dear Valued Customer,

We have detected suspicious activity on your account. Your account has been temporarily suspended for security reasons.

To reactivate your account, please click the link below and verify your information immediately:
http://bit.ly/account-verify-now

Failure to verify within 24 hours will result in permanent account closure.

Thank you for your immediate attention to this matter.

Security Team
```

## 🔧 API Endpoints

### `POST /predict`

Predict if an email is phishing or safe.

**Request:**

```json
{
  "email_text": "Your email content here..."
}
```

**Response:**

```json
{
  "prediction": 1,
  "is_phishing": true,
  "message": "⚠️ WARNING: PHISHING DETECTED!",
  "confidence": {
    "safe": 15.23,
    "phishing": 84.77
  }
}
```

### `POST /analyze`

Get AI-powered detailed analysis.

**Request:**

```json
{
  "email_text": "Your email content here...",
  "prediction_result": {
    /* prediction response */
  }
}
```

**Response:**

```json
{
  "analysis": "Detailed AI analysis text...",
  "model_used": "gpt-4o-mini"
}
```

### `GET /health`

Check API health status.

## 🧠 Technologies Used

### Backend

- **Flask**: Web framework
- **scikit-learn**: Machine Learning (Random Forest, TF-IDF)
- **OpenAI API**: AI-powered analysis
- **Flask-CORS**: Cross-origin resource sharing

### Frontend

- **Vue 3**: JavaScript framework
- **Vuetify 3**: Material Design component library
- **Vite**: Build tool
- **Axios**: HTTP client

## 📊 Model Details

- **Algorithm**: Random Forest Classifier
- **Features**: TF-IDF vectorization (5000 features)
- **Training Dataset**: Combined phishing email datasets
- **Train/Test Split**: 70/30
- **Estimators**: 100 trees

## 🔐 Security Notes

- Never commit your `.env` file with real API keys
- The `.env` file is gitignored by default
- Keep your OpenAI API key secure
- Monitor your OpenAI API usage

## 📝 License

This is an academic project for IT113 Final Project.

## 👨‍💻 Development

Built with ❤️ using Machine Learning and AI technologies.
# phishing-email-detector
