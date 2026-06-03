import streamlit as st
import requests

st.set_page_config(page_title="Product Assistant", page_icon="🤖")

API_URL = "http://localhost:8000"

st.markdown("""
<div class="header">
    <h1>Product Assistant</h1>
    <p>AI-powered product recommendations</p>
</div>
""", unsafe_allow_html=True)

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
if prompt := st.chat_input("Ask about products..."):

    # User message
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # API call
    with st.spinner("Searching..."):
        response = requests.post(
            f"{API_URL}/search",
            params={"query": prompt, "top_k": 5}
        )

    if response.status_code == 200:
        data = response.json()

        answer = data["recommendation"]

        # Append products
        answer += "\n\n### Recommended Products\n"

        for p in data["products"]:
            answer += f"""
**{p['product_name']}**
- Price: ${p['price']}
- Category: {p['category']}
- Features: {p['features']}

"""

        st.session_state.messages.append(
            {"role": "assistant", "content": answer}
        )

        with st.chat_message("assistant"):
            st.markdown(answer)

st.markdown("""
<style>

.stApp {
    background-color: #0f172a;
    color: white;
}

/* Header */
.header {
    text-align: center;
    padding: 1rem;
    margin-bottom: 20px;
}

.header h1 {
    font-size: 2.5rem;
    font-weight: 700;
}

.header p {
    color: #94a3b8;
}

/* Chat messages */
[data-testid="stChatMessage"] {
    border-radius: 18px;
    padding: 12px;
    margin-bottom: 12px;
}

/* User Bubble */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    background: #2563eb;
}

/* Assistant Bubble */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
    background: #1e293b;
}

/* Input */
.stChatInput {
    position: fixed;
    bottom: 20px;
    width: 70%;
}

</style>
""", unsafe_allow_html=True)