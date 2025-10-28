# --- 1. SETUP: Install necessary libraries ---


#import kagglehub
import pandas as pd
import numpy as np
from pathlib import Path
import joblib
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier  # <-- Import Random Forest
from sklearn.metrics import accuracy_score, classification_report

print("--- Libraries Imported ---")

# --- 2. LOAD DATA: Download from Kaggle and load into Pandas ---

print("\n--- Downloading Dataset ---")
# path = kagglehub.dataset_download("uciml/pima-indians-diabetes-database")
# dataset_path = Path(path)
csv_file = "data/diabetes.csv"
print(f"Dataset downloaded to: {csv_file}")

data = pd.read_csv(csv_file)
print(f"/n--- Data Loaded: {csv_file} ---")


# --- 3. PRE-PROCESSING: Clean and prepare the data ---
# (Same as before)
cols_to_clean = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']
data[cols_to_clean] = data[cols_to_clean].replace(0, np.nan)
for col in cols_to_clean:
    data[col] = data[col].fillna(data[col].median())

print("--- Data Pre-processing Complete ---")


# --- 4. FEATURE ENGINEERING & SPLITTING ---
# (Same as before)
features = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']
target = 'Outcome'

X = data[features]
y = data[target]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)


# --- 5. DATA SCALING ---
# (Same as before)
# Note: Random Forest is less sensitive to feature scaling,
# but it's still good practice.
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
print("--- Data Scaling Complete ---")


# --- 6. MODEL TRAINING (UPGRADED) ---

print("\n--- Training Upgraded Model: RandomForest with GridSearchCV ---")

# 1. Define the model
rf = RandomForestClassifier(random_state=42)

# 2. Define a "grid" of parameters to search through
# This tells GridSearchCV what settings to try.
# We'll keep it small so it runs fast on a CPU.
param_grid = {
    'n_estimators': [100, 200],       # Number of trees in the forest
    'max_depth': [10, 20, None],      # Max depth of the trees
    'min_samples_split': [2, 5]       # Min samples required to split a node
}

# 3. Set up the Grid Search
# cv=5 means 5-fold cross-validation
# n_jobs=-1 means use all available CPU cores
grid_search = GridSearchCV(estimator=rf, param_grid=param_grid,
                           cv=5, n_jobs=-1, verbose=1, scoring='accuracy')

# 4. Run the search! This will train many models to find the best one.
grid_search.fit(X_train_scaled, y_train)

# Get the best model found by the search
best_model = grid_search.best_estimator_
print("Model training complete.")
print(f"Best Parameters found: {grid_search.best_params_}")


# --- 7. MODEL EVALUATION ---

print("\n--- Evaluating Upgraded Model ---")
y_pred = best_model.predict(X_test_scaled)

accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy:.4f}")

print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=['No Diabetes (0)', 'Diabetes (1)']))


# --- 8. SAVE ARTIFACTS ---

model_filename = 'diabetes_model.joblib'
scaler_filename = 'scaler.joblib'

# Save the *best* model from the grid search
joblib.dump(best_model, model_filename)
joblib.dump(scaler, scaler_filename)

print(f"\n--- Artifacts Saved ---")
print(f"Best model saved to: {model_filename}")
print(f"Scaler saved to: {scaler_filename}")