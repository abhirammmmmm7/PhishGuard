import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score, classification_report

# LOAD DATASET
df = pd.read_csv("datasets/dataset2.csv")

# SPLIT FEATURES & LABEL
X = df.drop("phishing", axis=1)
y = df["phishing"]

# SAVE FEATURE ORDER (VERY IMPORTANT)
FEATURE_COLUMNS = X.columns.tolist()

# TRAIN / TEST SPLIT
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# MODEL
model = GradientBoostingClassifier(
    n_estimators=300,
    learning_rate=0.05,
    max_depth=3,
    random_state=42
)

model.fit(X_train, y_train)

# EVALUATION
y_pred = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))

# SAVE MODEL + FEATURE ORDER
joblib.dump(model, "ml/phishing_model.pkl")
joblib.dump(FEATURE_COLUMNS, "ml/feature_columns.pkl")

print("New model trained and saved")
