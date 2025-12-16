"""
Generate model evaluation visualizations and metrics
Run this script after training your model to create visualization images
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, 
    classification_report, 
    confusion_matrix,
    roc_curve,
    roc_auc_score,
    precision_recall_curve,
    average_precision_score
)
import os

# Set style for better-looking plots
sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 100

# Create output directory
os.makedirs('evaluation_results', exist_ok=True)

print("=" * 60)
print("PHISHING EMAIL CLASSIFIER - MODEL EVALUATION")
print("=" * 60)

# Load the dataset
print("\n📊 Loading dataset...")
df = pd.read_csv('../data/phishing_email.csv')
df = df.dropna()
print(f"✅ Dataset loaded. Total emails: {df.shape[0]}")

# Convert Text to Numbers (TF-IDF)
print("\n🔄 Converting text to TF-IDF features...")
tfidf = TfidfVectorizer(max_features=5000, stop_words='english')
X = tfidf.fit_transform(df['text_combined']).toarray()
y = df['label']

# Split Data
print("✂️  Splitting data (70/30)...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Train the Model
print("🌲 Training Random Forest model...")
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Make Predictions
print("🔮 Making predictions...")
y_pred = model.predict(X_test)
y_pred_proba = model.predict_proba(X_test)[:, 1]

# Calculate Metrics
accuracy = accuracy_score(y_test, y_pred)
roc_auc = roc_auc_score(y_test, y_pred_proba)
avg_precision = average_precision_score(y_test, y_pred_proba)

print("\n" + "=" * 60)
print("📈 MODEL PERFORMANCE METRICS")
print("=" * 60)
print(f"Accuracy:           {accuracy * 100:.2f}%")
print(f"ROC AUC Score:      {roc_auc:.4f}")
print(f"Average Precision:  {avg_precision:.4f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=['Safe', 'Phishing']))

# ========== VISUALIZATION 1: Confusion Matrix ==========
print("\n📊 Generating Confusion Matrix...")
plt.figure(figsize=(8, 6))
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=True,
            xticklabels=['Safe', 'Phishing'],
            yticklabels=['Safe', 'Phishing'])
plt.title('Confusion Matrix\nRandom Forest Classifier', fontsize=16, fontweight='bold')
plt.xlabel('Predicted Label', fontsize=12)
plt.ylabel('Actual Label', fontsize=12)
plt.tight_layout()
plt.savefig('evaluation_results/confusion_matrix.png', dpi=300, bbox_inches='tight')
print("✅ Saved: evaluation_results/confusion_matrix.png")
plt.close()

# ========== VISUALIZATION 2: Confusion Matrix Normalized ==========
print("📊 Generating Normalized Confusion Matrix...")
plt.figure(figsize=(8, 6))
cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
sns.heatmap(cm_normalized, annot=True, fmt='.2%', cmap='Blues', cbar=True,
            xticklabels=['Safe', 'Phishing'],
            yticklabels=['Safe', 'Phishing'])
plt.title('Normalized Confusion Matrix\nRandom Forest Classifier', fontsize=16, fontweight='bold')
plt.xlabel('Predicted Label', fontsize=12)
plt.ylabel('Actual Label', fontsize=12)
plt.tight_layout()
plt.savefig('evaluation_results/confusion_matrix_normalized.png', dpi=300, bbox_inches='tight')
print("✅ Saved: evaluation_results/confusion_matrix_normalized.png")
plt.close()

# ========== VISUALIZATION 3: ROC Curve ==========
print("📊 Generating ROC Curve...")
fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba)
plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (AUC = {roc_auc:.4f})')
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='Random Classifier')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate', fontsize=12)
plt.ylabel('True Positive Rate', fontsize=12)
plt.title('Receiver Operating Characteristic (ROC) Curve', fontsize=16, fontweight='bold')
plt.legend(loc="lower right", fontsize=10)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('evaluation_results/roc_curve.png', dpi=300, bbox_inches='tight')
print("✅ Saved: evaluation_results/roc_curve.png")
plt.close()

# ========== VISUALIZATION 3: Precision-Recall Curve ==========
print("📊 Generating Precision-Recall Curve...")
precision, recall, _ = precision_recall_curve(y_test, y_pred_proba)
plt.figure(figsize=(8, 6))
plt.plot(recall, precision, color='blue', lw=2, label=f'AP = {avg_precision:.4f}')
plt.xlabel('Recall', fontsize=12)
plt.ylabel('Precision', fontsize=12)
plt.title('Precision-Recall Curve', fontsize=16, fontweight='bold')
plt.legend(loc="lower left", fontsize=10)
plt.grid(True, alpha=0.3)
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.tight_layout()
plt.savefig('evaluation_results/precision_recall_curve.png', dpi=300, bbox_inches='tight')
print("✅ Saved: evaluation_results/precision_recall_curve.png")
plt.close()

# ========== VISUALIZATION 4: Precision Confidence Curve ==========
print("📊 Generating Precision Confidence Curve...")
from sklearn.metrics import precision_score

# Calculate precision at different thresholds
thresholds_range = np.linspace(0, 1, 100)
precisions = []
for thresh in thresholds_range:
    y_pred_thresh = (y_pred_proba >= thresh).astype(int)
    # Avoid division by zero
    if y_pred_thresh.sum() > 0:
        precisions.append(precision_score(y_test, y_pred_thresh, zero_division=0))
    else:
        precisions.append(0)

plt.figure(figsize=(8, 6))
plt.plot(thresholds_range, precisions, color='green', lw=2, marker='o', markersize=3)
plt.xlabel('Confidence Threshold', fontsize=12)
plt.ylabel('Precision', fontsize=12)
plt.title('Precision vs Confidence Threshold', fontsize=16, fontweight='bold')
plt.grid(True, alpha=0.3)
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.axhline(y=0.5, color='r', linestyle='--', alpha=0.5, label='50% baseline')
plt.legend(fontsize=10)
plt.tight_layout()
plt.savefig('evaluation_results/precision_confidence_curve.png', dpi=300, bbox_inches='tight')
print("✅ Saved: evaluation_results/precision_confidence_curve.png")
plt.close()

# ========== VISUALIZATION 5: Recall Confidence Curve ==========
print("📊 Generating Recall Confidence Curve...")
from sklearn.metrics import recall_score

# Calculate recall at different thresholds
recalls = []
for thresh in thresholds_range:
    y_pred_thresh = (y_pred_proba >= thresh).astype(int)
    recalls.append(recall_score(y_test, y_pred_thresh, zero_division=0))

plt.figure(figsize=(8, 6))
plt.plot(thresholds_range, recalls, color='orange', lw=2, marker='o', markersize=3)
plt.xlabel('Confidence Threshold', fontsize=12)
plt.ylabel('Recall', fontsize=12)
plt.title('Recall vs Confidence Threshold', fontsize=16, fontweight='bold')
plt.grid(True, alpha=0.3)
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.axhline(y=0.5, color='r', linestyle='--', alpha=0.5, label='50% baseline')
plt.legend(fontsize=10)
plt.tight_layout()
plt.savefig('evaluation_results/recall_confidence_curve.png', dpi=300, bbox_inches='tight')
print("✅ Saved: evaluation_results/recall_confidence_curve.png")
plt.close()

# ========== VISUALIZATION 6: F1 Confidence Curve ==========
print("📊 Generating F1 Confidence Curve...")
from sklearn.metrics import f1_score

# Calculate F1 score at different thresholds
f1_scores = []
for thresh in thresholds_range:
    y_pred_thresh = (y_pred_proba >= thresh).astype(int)
    f1_scores.append(f1_score(y_test, y_pred_thresh, zero_division=0))

# Find optimal threshold
optimal_idx = np.argmax(f1_scores)
optimal_threshold = thresholds_range[optimal_idx]
optimal_f1 = f1_scores[optimal_idx]

plt.figure(figsize=(8, 6))
plt.plot(thresholds_range, f1_scores, color='purple', lw=2, marker='o', markersize=3)
plt.scatter(optimal_threshold, optimal_f1, color='red', s=100, zorder=5, 
            label=f'Optimal: {optimal_threshold:.2f} (F1={optimal_f1:.3f})')
plt.xlabel('Confidence Threshold', fontsize=12)
plt.ylabel('F1 Score', fontsize=12)
plt.title('F1 Score vs Confidence Threshold', fontsize=16, fontweight='bold')
plt.grid(True, alpha=0.3)
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.axhline(y=0.5, color='r', linestyle='--', alpha=0.5, label='50% baseline')
plt.legend(fontsize=10)
plt.tight_layout()
plt.savefig('evaluation_results/f1_confidence_curve.png', dpi=300, bbox_inches='tight')
print("✅ Saved: evaluation_results/f1_confidence_curve.png")
plt.close()

# ========== VISUALIZATION 7: Confidence Distribution ==========
print("📊 Generating Confidence Distribution...")
plt.figure(figsize=(10, 6))
safe_proba = y_pred_proba[y_test == 0]
phishing_proba = y_pred_proba[y_test == 1]

plt.hist(safe_proba, bins=50, alpha=0.7, label='Safe Emails', color='green', edgecolor='black')
plt.hist(phishing_proba, bins=50, alpha=0.7, label='Phishing Emails', color='red', edgecolor='black')
plt.xlabel('Predicted Probability (Phishing)', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.title('Confidence Distribution by Class', fontsize=16, fontweight='bold')
plt.legend(fontsize=10)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('evaluation_results/confidence_distribution.png', dpi=300, bbox_inches='tight')
print("✅ Saved: evaluation_results/confidence_distribution.png")
plt.close()

# ========== VISUALIZATION 5: Feature Importance (Top 20) ==========
print("📊 Generating Feature Importance...")
feature_names = tfidf.get_feature_names_out()
importances = model.feature_importances_
indices = np.argsort(importances)[-20:]  # Top 20 features

plt.figure(figsize=(10, 8))
plt.barh(range(len(indices)), importances[indices], color='steelblue', edgecolor='black')
plt.yticks(range(len(indices)), [feature_names[i] for i in indices])
plt.xlabel('Feature Importance', fontsize=12)
plt.ylabel('Features (Words)', fontsize=12)
plt.title('Top 20 Most Important Features', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('evaluation_results/feature_importance.png', dpi=300, bbox_inches='tight')
print("✅ Saved: evaluation_results/feature_importance.png")
plt.close()

# ========== VISUALIZATION 6: Class Distribution ==========
print("📊 Generating Class Distribution...")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Original dataset distribution
class_counts = df['label'].value_counts()
colors = ['#4CAF50', '#F44336']
ax1.pie(class_counts, labels=['Safe', 'Phishing'], autopct='%1.1f%%', 
        colors=colors, startangle=90, explode=(0.05, 0.05))
ax1.set_title('Dataset Class Distribution', fontsize=14, fontweight='bold')

# Test set predictions
pred_counts = pd.Series(y_pred).value_counts()
ax2.pie(pred_counts, labels=['Safe', 'Phishing'], autopct='%1.1f%%',
        colors=colors, startangle=90, explode=(0.05, 0.05))
ax2.set_title('Test Set Predictions', fontsize=14, fontweight='bold')

plt.tight_layout()
plt.savefig('evaluation_results/class_distribution.png', dpi=300, bbox_inches='tight')
print("✅ Saved: evaluation_results/class_distribution.png")
plt.close()

# ========== VISUALIZATION 7: Model Performance Metrics Summary ==========
print("📊 Generating Performance Metrics Summary...")
from sklearn.metrics import precision_score, recall_score, f1_score

metrics = {
    'Accuracy': accuracy_score(y_test, y_pred),
    'Precision': precision_score(y_test, y_pred),
    'Recall': recall_score(y_test, y_pred),
    'F1-Score': f1_score(y_test, y_pred),
    'ROC AUC': roc_auc_score(y_test, y_pred_proba)
}

plt.figure(figsize=(10, 6))
bars = plt.bar(metrics.keys(), metrics.values(), color=['#2196F3', '#4CAF50', '#FF9800', '#9C27B0', '#F44336'],
               edgecolor='black', linewidth=1.5)
plt.ylim(0, 1.1)
plt.ylabel('Score', fontsize=12)
plt.title('Model Performance Metrics Summary', fontsize=16, fontweight='bold')
plt.grid(axis='y', alpha=0.3)

# Add value labels on bars
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
             f'{height:.3f}',
             ha='center', va='bottom', fontsize=11, fontweight='bold')

plt.tight_layout()
plt.savefig('evaluation_results/performance_summary.png', dpi=300, bbox_inches='tight')
print("✅ Saved: evaluation_results/performance_summary.png")
plt.close()

# ========== Save Metrics to Text File ==========
print("\n💾 Saving metrics to file...")
with open('evaluation_results/model_metrics.txt', 'w') as f:
    f.write("=" * 60 + "\n")
    f.write("PHISHING EMAIL CLASSIFIER - EVALUATION RESULTS\n")
    f.write("=" * 60 + "\n\n")
    f.write(f"Model: Random Forest Classifier (100 estimators)\n")
    f.write(f"Training Set Size: {X_train.shape[0]} samples\n")
    f.write(f"Test Set Size: {X_test.shape[0]} samples\n")
    f.write(f"Features: {X.shape[1]} (TF-IDF)\n\n")
    f.write("PERFORMANCE METRICS:\n")
    f.write("-" * 60 + "\n")
    f.write(f"Accuracy:           {accuracy * 100:.2f}%\n")
    f.write(f"Precision:          {precision_score(y_test, y_pred):.4f}\n")
    f.write(f"Recall:             {recall_score(y_test, y_pred):.4f}\n")
    f.write(f"F1-Score:           {f1_score(y_test, y_pred):.4f}\n")
    f.write(f"ROC AUC Score:      {roc_auc:.4f}\n")
    f.write(f"Average Precision:  {avg_precision:.4f}\n\n")
    f.write("CLASSIFICATION REPORT:\n")
    f.write("-" * 60 + "\n")
    f.write(classification_report(y_test, y_pred, target_names=['Safe', 'Phishing']))
    f.write("\n" + "=" * 60 + "\n")

print("✅ Saved: evaluation_results/model_metrics.txt")

print("\n" + "=" * 60)
print("✨ ALL VISUALIZATIONS GENERATED SUCCESSFULLY!")
print("=" * 60)
print("\nGenerated files in 'evaluation_results/' folder:")
print("  1.  confusion_matrix.png")
print("  2.  confusion_matrix_normalized.png")
print("  3.  roc_curve.png")
print("  4.  precision_recall_curve.png")
print("  5.  precision_confidence_curve.png")
print("  6.  recall_confidence_curve.png")
print("  7.  f1_confidence_curve.png")
print("  8.  confidence_distribution.png")
print("  9.  feature_importance.png")
print("  10. class_distribution.png")
print("  11. performance_summary.png")
print("  12. model_metrics.txt")
print("\n🎉 You can use these images in your reports and presentations!")
print(f"\n💡 Optimal F1 threshold: {optimal_threshold:.2f} (F1 Score: {optimal_f1:.3f})")
