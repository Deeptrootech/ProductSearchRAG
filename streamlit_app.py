"""Simple Streamlit app."""
import streamlit as st
import requests

st.set_page_config(page_title="Product Search", page_icon="🔍", layout="wide")

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
    }
    .recommendation-box {
        background-color: #f0f8ff;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin: 10px 0;
    }
    .product-card {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #ddd;
        margin: 10px 0;
    }
    .similarity-score {
        color: #28a745;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">🔍 Product Search</h1>', unsafe_allow_html=True)

API_URL = "http://localhost:8000"


# ============ UPLOAD PAGE ============
def upload_page():
    st.header("📤 Upload Products")
    st.markdown("---")

    uploaded_file = st.file_uploader("Choose CSV file", type=["csv"], label_visibility="visible")

    if uploaded_file:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.info(f"Selected file: {uploaded_file.name}")
        with col2:
            if st.button("Upload", use_container_width=True):
                files = {"file": (uploaded_file.name, uploaded_file)}
                response = requests.post(f"{API_URL}/upload", files=files)

                if response.status_code == 200:
                    st.success(f"✅ {response.json()['products_processed']} products uploaded successfully!")
                else:
                    st.error("❌ Upload failed. Please try again.")

    st.markdown("### CSV Format")
    st.markdown("""
    Your CSV should include the following columns:
    - `product_id` (optional)
    - `product_name`
    - `category`
    - `price`
    - `features`
    - `description`
    """)


# ============ SEARCH PAGE ============
def search_page():
    st.header("🔎 Search Products")
    st.markdown("---")

    # Search input section
    col1, col2 = st.columns([4, 1])
    with col1:
        query = st.text_input("What are you looking for?", placeholder="e.g., wireless headphones under $100", label_visibility="visible")
    with col2:
        top_k = st.slider("Results", min_value=1, max_value=10, value=5, step=1)

    search_button = st.button("🔍 Search", use_container_width=True, type="primary")

    if search_button and query:
        with st.spinner("Searching products..."):
            response = requests.post(f"{API_URL}/search", params={"query": query, "top_k": top_k})

        if response.status_code == 200:
            data = response.json()

            # Display recommendation with markdown
            st.markdown("### 💡 AI Recommendation")
            st.markdown('<div class="recommendation-box">', unsafe_allow_html=True)
            st.markdown(data["recommendation"])
            st.markdown('</div>', unsafe_allow_html=True)

            # Display retrieved products
            st.markdown(f"### 📦 {data['total']} Products Found")
            st.markdown("---")

            # Display products in a grid layout
            for idx, product in enumerate(data["products"], 1):
                with st.expander(f"**{idx}. {product['product_name']}** - ${product['price']}", expanded=(idx == 1)):
                    col1, col2 = st.columns([2, 1])

                    with col1:
                        st.markdown(f"**Category:** {product['category']}")
                        st.markdown(f"**Features:** {product['features']}")
                        st.markdown(f"**Description:** {product['description']}")

                    with col2:
                        similarity_score = product.get('score', 0)
                        # Convert distance to similarity (lower distance = higher similarity)
                        similarity = max(0, 1 - similarity_score) if similarity_score > 0 else 1.0
                        st.metric("Similarity", f"{similarity:.2%}")
                        st.markdown(f"**Product ID:** {product.get('product_id', 'N/A')}")

                st.markdown("---")
        else:
            st.error("❌ Search failed. Please try again.")


# ============ MAIN ============
page = st.sidebar.radio("Navigate", ["🔎 Search", "📤 Upload"], label_visibility="collapsed")

if page == "🔎 Search":
    search_page()
else:
    upload_page()

# Footer
st.markdown("---")
st.markdown("<div style='text-align: center; color: gray;'>Powered by RAG-based Product Search</div>", unsafe_allow_html=True)
