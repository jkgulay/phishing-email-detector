import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
import os

# Create models directory
os.makedirs('models', exist_ok=True)

# Load the dataset
print("Loading dataset...")
df = pd.read_csv('../data/phishing_email.csv')
df = df.dropna()
print(f"Dataset loaded. Total emails: {df.shape[0]}")

# Convert Text to Numbers (TF-IDF)
print("Converting text to TF-IDF features...")
tfidf = TfidfVectorizer(max_features=5000, stop_words='english')
X = tfidf.fit_transform(df['text_combined']).toarray()
y = df['label']

# Split Data
print("Splitting data...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Train the Model
print("Training Random Forest model...")
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
from sklearn.metrics import accuracy_score
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy * 100:.2f}%")

# Save the model and vectorizer
print("Saving model and vectorizer...")
with open('models/random_forest_model.pkl', 'wb') as f:
    pickle.dump(model, f)

with open('models/tfidf_vectorizer.pkl', 'wb') as f:
    pickle.dump(tfidf, f)

print("✅ Model and vectorizer saved successfully!")
print("Files saved:")
print("  - models/random_forest_model.pkl")
print("  - models/tfidf_vectorizer.pkl")
