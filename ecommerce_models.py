import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsClassifier
import joblib

# Load dataset
df = pd.read_csv("Ecommerce_cleaned.csv")

# Encode categorical features
product_encoder = LabelEncoder()
category_encoder = LabelEncoder()
customer_encoder = LabelEncoder()

df["product_id_encoded"] = product_encoder.fit_transform(df["product_id"])
df["product_category_encoded"] = category_encoder.fit_transform(df["product_category_name"])
df["customer_id_encoded"] = customer_encoder.fit_transform(df["customer_id"])

# Review Prediction Model
review_features = ["product_id_encoded", "price", "freight_value", "payment_value", "product_category_encoded"]
df_review = df[review_features + ["review_score"]]
X_review = df_review.drop(columns=["review_score"])
y_review = df_review["review_score"]
X_train, X_test, y_train, y_test = train_test_split(X_review, y_review, test_size=0.2, random_state=42)
review_model = RandomForestRegressor(n_estimators=50, random_state=42)
review_model.fit(X_train, y_train)
joblib.dump(review_model, "review_prediction.pkl")

# Product Recommendation Model
recommendation_features = ["customer_id_encoded", "product_id_encoded", "product_category_encoded", "price"]
df_recommendation = df[recommendation_features]
X_recommend = df_recommendation.drop(columns=["customer_id_encoded"])
y_recommend = df_recommendation["customer_id_encoded"]
X_train, X_test, y_train, y_test = train_test_split(X_recommend, y_recommend, test_size=0.2, random_state=42)
knn_model = KNeighborsClassifier(n_neighbors=5)
knn_model.fit(X_train, y_train)
joblib.dump(knn_model, "product_recommendation.pkl")
