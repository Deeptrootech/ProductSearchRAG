import streamlit as st
import requests

API_URL = "http://localhost:8000"

# -------------------
# CONFIG
# -------------------
st.set_page_config(
    page_title="Product AI Assistant",
    page_icon="🛍️",
    layout="wide"
)

# -------------------
# SESSION STATE
# -------------------
if "chat" not in st.session_state:
    st.session_state.chat = []


# -------------------
# SAFE PRICE PARSER
# -------------------
def parse_price(price):
    try:
        return float(str(price).replace("$", "").replace("USD", "").strip())
    except:
        return 0


# -------------------
# PRODUCT CARD (STREAMLIT VERSION - NO HTML ISSUES)
# -------------------
def render_product(p):
    price = parse_price(p.get("price", 0))

    with st.container():
        st.markdown("### 🛍️ " + p.get("product_name", "Unknown Product"))

        col1, col2 = st.columns([1, 1])

        with col1:
            st.markdown(f"💰 **Price:** ${price:,.0f}")
            st.markdown(f"📂 **Category:** {p.get('category', 'N/A')}")
            st.markdown(f"⭐ **Rating:** {p.get('rating', 'N/A')}")

        with col2:
            st.markdown("### 🔖 Features")
            for f in p.get("features", []):
                st.markdown(f"- {f}")

        st.markdown("---")

        col3, col4 = st.columns(2)

        with col3:
            st.markdown("### 👍 Pros")
            for x in p.get("pros", []):
                st.success(x)

        with col4:
            st.markdown("### 👎 Cons")
            for x in p.get("cons", []):
                st.error(x)

        st.markdown("### 💡 Why Choose")
        for x in p.get("why_choose", []):
            st.info(x)

        if p.get("description"):
            st.markdown("### 📝 Description")
            st.write(p.get("description"))

        st.markdown("---")


# -------------------
# SIDEBAR
# -------------------
with st.sidebar:
    st.title("🛍️ Product AI")

    uploaded_file = st.file_uploader("Upload CSV Dataset", type=["csv"])

    if uploaded_file:
        if st.button("Upload"):
            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    "text/csv"
                )
            }

            res = requests.post(f"{API_URL}/upload", files=files)

            if res.status_code == 200:
                st.success("Uploaded Successfully")
            else:
                st.error("Upload Failed")

# -------------------
# TITLE
# -------------------
st.title("💬 Product Search Assistant")

st.markdown("Ask anything like *'best laptop under 1000$'*")

st.divider()

# -------------------
# CHAT DISPLAY
# -------------------
for msg in st.session_state.chat:

    if msg["role"] == "user":
        with st.chat_message("user"):
            st.write(msg["content"])

    else:
        with st.chat_message("assistant"):
            st.write(msg.get("answer", ""))

            for p in msg.get("products", []):
                render_product(p)

# -------------------
# INPUT
# -------------------
query = st.chat_input("Search products...")

if query:

    # user message
    st.session_state.chat.append({
        "role": "user",
        "content": query
    })

    # API call
    with st.spinner("Finding best products..."):
        try:
            response = requests.post(
                f"{API_URL}/search",
                params={"query": query}
            )

            if response.status_code == 200:
                data = response.json()

                st.session_state.chat.append({
                    "role": "assistant",
                    "answer": data.get("answer", ""),
                    "products": data.get("products", [])
                })

            else:
                st.session_state.chat.append({
                    "role": "assistant",
                    "answer": "Error fetching results",
                    "products": []
                })

        except Exception as e:
            st.session_state.chat.append({
                "role": "assistant",
                "answer": f"Server error: {str(e)}",
                "products": []
            })

    st.rerun()
