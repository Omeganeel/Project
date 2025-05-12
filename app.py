
import streamlit as st
import joblib
import pandas as pd

# Load models
review_model = joblib.load("review_prediction.pkl")
knn_model = joblib.load("product_recommendation.pkl")

# Load dataset to fetch product details
df = pd.read_csv("Ecommerce_cleaned.csv")

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Product Recommendation", "Review Predictor", "Power BI Dashboard"])

if page == "Product Recommendation":
    st.title("Product Recommendation System")
    customer_id = st.text_input("Enter Customer ID:")
    if st.button("Get Recommendations"):
        if customer_id:
            customer_encoded = int(customer_id)
            recommended_indices = knn_model.kneighbors([[customer_encoded, 0, 0]], n_neighbors=5, return_distance=False)
            recommended_products = df.iloc[recommended_indices[0]][["product_id", "product_category_name", "price"]]
            st.write("Recommended Products:")
            st.dataframe(recommended_products)

elif page == "Review Predictor":
    st.title("Predict Review Score")
    product_id = st.text_input("Enter Product ID:")
    if st.button("Predict Review"):
        if product_id:
            product_encoded = int(product_id)  # Assuming encoded ID is an integer
            prediction = review_model.predict([[product_encoded, 0, 0, 0, 0]])
            st.write(f"Predicted Review Score: {round(prediction[0], 2)}")

elif page == "Power BI Dashboard":
    st.title("Power BI Dashboard")
    st.components.v1.html(
        '<iframe title="Ecommerce_dataset_dashboard_4" width="600" height="373.5" '
        'src="https://app.powerbi.com/view?r=eyJrIjoiNzQxYTRjNzctY2Q0Yi00NzE1LWI3MjItNTA3MDljZjJhOWU2IiwidCI6IjNjYjkxMTI3LTkyNDMtNGQ1Yy04NWJiLTM2Zjc4YTIwMDA2MiJ9" '
        'frameborder="0" allowFullScreen="true"></iframe>',
        height=400,
    )