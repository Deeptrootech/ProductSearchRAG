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
    except Exception:
        return 0.0


# -------------------
# PRODUCT CARD
# -------------------
def render_product(product):
    price = parse_price(product.get("price", 0))

    product_name = product.get(
        "product_name",
        "Unknown Product"
    )

    with st.expander(
            f"🛍️ {product_name} - ${price:.2f}",
            expanded=True
    ):

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(
                f"💰 **Price:** ${price:.2f}"
            )

            st.markdown(
                f"📂 **Category:** "
                f"{product.get('category', 'N/A')}"
            )

            score = product.get("score")

            if score is not None:
                try:
                    st.caption(
                        f"Relevance Score: "
                        f"{float(score):.3f}"
                    )
                except Exception:
                    pass

        with col2:

            features = product.get(
                "features",
                []
            )

            if isinstance(features, str):
                features = [
                    item.strip()
                    for item in features.split(",")
                    if item.strip()
                ]

            if features:
                st.markdown("### 🔖 Features")

                for feature in features:
                    st.markdown(
                        f"- {feature}"
                    )

        pros = product.get("pros", [])
        cons = product.get("cons", [])
        why_choose = product.get(
            "why_choose",
            []
        )

        if pros or cons:

            col3, col4 = st.columns(2)

            with col3:

                if pros:
                    st.markdown(
                        "### 👍 Pros"
                    )

                    for item in pros:
                        st.success(item)

            with col4:

                if cons:
                    st.markdown(
                        "### 👎 Cons"
                    )

                    for item in cons:
                        st.error(item)

        if why_choose:

            st.markdown(
                "### 💡 Why Choose"
            )

            for item in why_choose:
                st.info(item)

        description = product.get(
            "description",
            ""
        )

        if description:
            st.markdown(
                "### 📝 Description"
            )
            st.write(description)


# -------------------
# SIDEBAR
# -------------------
with st.sidebar:
    st.title("🛍️ Product AI")

    if st.button("🗑️ Clear Chat"):
        st.session_state.chat = []
        st.rerun()

    st.divider()

    uploaded_file = st.file_uploader(
        "Upload CSV Dataset",
        type=["csv"]
    )

    if uploaded_file:

        if st.button(
                "Upload Dataset"
        ):

            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    "text/csv"
                )
            }

            try:
                response = requests.post(
                    f"{API_URL}/upload",
                    files=files
                )

                if response.status_code == 200:
                    st.success(
                        "Uploaded Successfully"
                    )
                else:
                    st.error(
                        "Upload Failed"
                    )

            except Exception as e:
                st.error(str(e))

    if st.session_state.chat:

        st.divider()

        st.subheader(
            "Recent Searches"
        )

        recent_queries = [
            msg["content"]
            for msg in st.session_state.chat
            if msg["role"] == "user"
        ][-5:]

        for query in reversed(
                recent_queries
        ):
            st.caption(query)

# -------------------
# TITLE
# -------------------
st.title(
    "💬 Product Search Assistant"
)

st.markdown(
    "Ask anything like "
    "**'best laptop under 1000$'**"
)

st.divider()

# -------------------
# CHAT HISTORY
# -------------------
for message in st.session_state.chat:

    if message["role"] == "user":

        with st.chat_message(
                "user"
        ):
            st.write(
                message["content"]
            )

    else:

        with st.chat_message(
                "assistant"
        ):

            answer = message.get(
                "answer",
                ""
            )

            if answer:
                st.write(answer)

            products = message.get(
                "products",
                []
            )

            if products:
                st.caption(
                    f"Found "
                    f"{len(products)} "
                    f"matching products"
                )

            for product in products:
                render_product(
                    product
                )

# -------------------
# CHAT INPUT
# -------------------
query = st.chat_input(
    "Search products..."
)

if query:

    st.session_state.chat.append({
        "role": "user",
        "content": query
    })

    with st.spinner(
            "Finding products..."
    ):

        try:

            response = requests.post(
                f"{API_URL}/search",
                params={
                    "user_query": query
                },
                timeout=60
            )

            if response.status_code == 200:

                data = response.json()

                st.session_state.chat.append({
                    "role": "assistant",
                    "answer": data.get(
                        "answer",
                        ""
                    ),
                    "products": data.get(
                        "products",
                        []
                    )
                })

            else:

                st.session_state.chat.append({
                    "role": "assistant",
                    "answer": (
                        f"API Error "
                        f"({response.status_code})"
                    ),
                    "products": []
                })

        except Exception as e:

            st.session_state.chat.append({
                "role": "assistant",
                "answer": (
                    f"Server Error: "
                    f"{str(e)}"
                ),
                "products": []
            })

    st.rerun()
