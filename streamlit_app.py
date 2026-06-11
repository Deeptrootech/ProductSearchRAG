import streamlit as st
import requests
import pandas as pd

# ------------------
# CONFIG
# ------------------

API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="Product Search Assistant",
    page_icon="🛍️",
    layout="centered"
)

# ------------------
# DARK THEME
# ------------------

st.markdown("""
<style>

.stApp {
    background-color: black;
}

h1,h2,h3,p,label {
    color: white;
}

[data-testid="stFileUploader"] {
    background-color: #161b22;
    padding: 15px;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# ------------------
# HEADER
# ------------------

st.title("🛍️ Product Search Assistant")
st.caption("Semantic product search using RAG + Vector Database")

st.divider()

# ------------------
# UPLOAD CSV
# ------------------

st.subheader("Upload Product Dataset")

uploaded_file = st.file_uploader(
    "Choose CSV file",
    type=["csv"]
)

if uploaded_file:

    if st.button("Upload Dataset"):

        files = {
            "file": (
                uploaded_file.name,
                uploaded_file.getvalue(),
                "text/csv"
            )
        }

        with st.spinner("Uploading..."):

            response = requests.post(
                f"{API_URL}/upload",
                files=files
            )

        if response.status_code == 200:
            st.success("Dataset uploaded successfully")
        else:
            st.error("Upload failed")

st.divider()

# ------------------
# SEARCH
# ------------------

st.subheader("Search Products")

query = st.text_input(
    "What product are you looking for?",
    placeholder="Gaming laptop under $1000"
)

if st.button("Search"):
    if query:
        with st.spinner("Searching..."):
            response = requests.post(f"{API_URL}/search", params={"query": query})

        if response.status_code == 200:
            results = response.json().get("products")
            st.success(f"Found {len(results)} matching products")

            for product in results:
                with st.container():
                    st.markdown(f"### {product.get('product_name', 'Unknown')}")

                    if "category" in product:
                        st.caption(product["category"])

                    if "price" in product:
                        st.write(
                            f"💰 Price: ₹{product['price']}"
                        )

                    if "features" in product:
                        st.write(
                            f"**Features:** {product['features']}"
                        )

                    if "description" in product:
                        st.write(
                            product["description"]
                        )

                    st.divider()

        else:
            st.error("Search failed")
