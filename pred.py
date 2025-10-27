# --- 1. SETUP: Install necessary libraries ---
# (scikit-learn, pandas, and numpy are pre-installed in Colab)

import kagglehub
import pandas as pd
import numpy as np
from pathlib import Path
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

print("--- Libraries Imported ---")

# --- 2. LOAD DATA: Download from Kaggle and load into Pandas ---

print("\n--- Downloading Dataset ---")
# Download the dataset to the Colab environment
# path = kagglehub.dataset_download("uciml/pima-indians-diabetes-database")
# dataset_path = Path(path)
csv_file = "diabetes.csv"
print(f"Dataset downloaded to: {csv_file}")

# Load the dataset
data = pd.read_csv(csv_file)
print("\n--- Data Head ---")
print(data.head())

# --- 3. PRE-PROCESSING: Clean and prepare the data ---

# In this dataset, '0' is often used as a placeholder for missing data
# in columns where it's biologically impossible (e.g., BMI, BloodPressure).
# We will replace these 0s with NaN (Not a Number).
cols_to_clean = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']
data[cols_to_clean] = data[cols_to_clean].replace(0, np.nan)

# Now, we'll fill the missing values (NaN) with the median of each column.
# This is a common imputation strategy.
for col in cols_to_clean:
    median = data[col].median()
    data[col] = data[col].fillna(median)

print("\n--- Data after cleaning 0-values (head) ---")
print(data.head())

# --- 4. FEATURE ENGINEERING & SPLITTING ---

# Define our features (X) and target (y)
features = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']
target = 'Outcome'

X = data[features]
y = data[target]

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
print(f"\nTraining set shape: {X_train.shape}")
print(f"Testing set shape: {X_test.shape}")

# --- 5. DATA SCALING ---

# Logistic Regression performs better with scaled features.
# We will fit the scaler ONLY on the training data.
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)

# We use the same fitted scaler to transform the test data.
X_test_scaled = scaler.transform(X_test)

# --- 6. MODEL TRAINING ---

print("\n--- Training Logistic Regression Model ---")
# Initialize and train the model
model = LogisticRegression(random_state=42)
model.fit(X_train_scaled, y_train)
print("Model training complete.")

# --- 7. MODEL EVALUATION ---

print("\n--- Evaluating Model ---")
# Make predictions on the test set
y_pred = model.predict(X_test_scaled)

# Calculate and print accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy:.4f}")

# Print a detailed classification report
print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=['No Diabetes (0)', 'Diabetes (1)']))

# --- 8. SAVE ARTIFACTS ---

# This is the most important step for your MLOps pipeline.
# We save the trained model AND the scaler.
model_filename = 'diabetes_model.joblib'
scaler_filename = 'scaler.joblib'

joblib.dump(model, model_filename)
joblib.dump(scaler, scaler_filename)

print(f"\n--- Artifacts Saved ---")
print(f"Model saved to: {model_filename}")
print(f"Scaler saved to: {scaler_filename}")
print("\nThese two files are what your CI/CD pipeline will version and deploy.")