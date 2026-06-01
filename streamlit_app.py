"""Simple Streamlit app."""
import streamlit as st
import requests

st.set_page_config(page_title="Product Search", page_icon="🔍")
st.title("🔍 Product Search")

API_URL = "http://localhost:8000"


# ============ UPLOAD PAGE ============
def upload_page():
    st.header("📤 Upload Products")
    uploaded_file = st.file_uploader("Choose CSV file", type=["csv"])
    
    if uploaded_file:
        if st.button("Upload"):
            files = {"file": (uploaded_file.name, uploaded_file)}
            response = requests.post(f"{API_URL}/upload", files=files)
            
            if response.status_code == 200:
                st.success(f"✅ {response.json()['products_processed']} products uploaded")
            else:
                st.error("❌ Upload failed")


# ============ SEARCH PAGE ============
def search_page():
    st.header("🔎 Search Products")
    query = st.text_input("What are you looking for?")
    top_k = st.slider("Results", 1, 10, 5)
    
    if st.button("Search") and query:
        response = requests.post(f"{API_URL}/search", params={"query": query, "top_k": top_k})
        
        if response.status_code == 200:
            data = response.json()
            
            st.subheader("💡 Recommendation")
            st.write(data["recommendation"])
            
            st.subheader(f"📦 {data['total']} Products Found")
            for product in data["products"]:
                with st.expander(f"{product['product_name']} - ${product['price']}"):
                    st.write(f"**Category:** {product['category']}")
                    st.write(f"**Features:** {product['features']}")
                    st.write(f"**Description:** {product['description']}")


# ============ MAIN ============
page = st.sidebar.radio("Navigate", ["Search", "Upload"])

if page == "Search":
    search_page()
else:
    upload_page()
