import joblib

model = joblib.load("ml/phishing_model.pkl")
FEATURE_COLUMNS = joblib.load("ml/feature_columns.pkl")
