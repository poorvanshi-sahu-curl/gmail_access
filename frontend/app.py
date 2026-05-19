import streamlit as st
import requests
import os

API = os.getenv("BACKEND_URL", "http://localhost:8000")

st.set_page_config(page_title="Gemma Gmail Assistant", page_icon="✉️")
st.title("✉️ Gemma Gmail Assistant")

if "emails" not in st.session_state:
    st.session_state.emails = []

if st.button("📥 Load Emails"):
    with st.spinner("Fetching emails..."):
        try:
            res = requests.get(f"{API}/emails/", timeout=30)
            if res.status_code == 200 and res.text:
                st.session_state.emails = res.json()
                st.success(f"✅ Loaded {len(st.session_state.emails)} emails!")
            else:
                st.error(f"Backend error: {res.status_code} — {res.text}")
        except requests.exceptions.ConnectionError:
            st.error("❌ Cannot connect to backend. Is it running on port 8000?")
        except requests.exceptions.Timeout:
            st.error("⏱️ Request timed out.")
        except Exception as e:
            st.error(f"Unexpected error: {str(e)}")

emails = st.session_state.emails

if emails:
    tab1, tab2, tab3, tab4 = st.tabs([
        "📌 Summarize", "✍️ Draft Reply", "🔍 Search", "🗂️ Categorize"
    ])

    email_subjects = [f"{e['subject']} — {e['sender']}" for e in emails]

    with tab1:
        selected = st.selectbox("Select email", email_subjects, key="sum")
        email = emails[email_subjects.index(selected)]
        st.caption(f"From: {email['sender']} | {email['date']}")
        with st.expander("View email body"):
            st.write(email["body"])
        if st.button("📌 Summarize", key="btn_sum"):
            with st.spinner("Thinking..."):
                try:
                    res = requests.post(
                        f"{API}/summarize/",
                        json={"email_body": email["body"]},
                        timeout=60
                    )
                    st.markdown(res.json()["summary"])
                except Exception as e:
                    st.error(f"Error: {e}")

    with tab2:
        selected = st.selectbox("Select email", email_subjects, key="draft")
        email = emails[email_subjects.index(selected)]
        st.caption(f"From: {email['sender']} | {email['date']}")
        with st.expander("View email body"):
            st.write(email["body"])
        tone = st.selectbox("Tone", ["professional", "friendly", "concise"], key="tone")
        if st.button("✍️ Draft Reply", key="btn_draft"):
            with st.spinner("Drafting..."):
                try:
                    res = requests.post(
                        f"{API}/draft/",
                        json={"email_body": email["body"], "tone": tone},
                        timeout=60
                    )
                    st.text_area("Draft", res.json()["draft"], height=200)
                except Exception as e:
                    st.error(f"Error: {e}")

    with tab3:
        question = st.text_input("💬 Ask a question about your emails")
        if st.button("🔍 Search", key="btn_search") and question:
            with st.spinner("Searching..."):
                try:
                    bodies = [e["body"] for e in emails]
                    res = requests.post(
                        f"{API}/search/",
                        json={"emails": bodies, "question": question},
                        timeout=60
                    )
                    st.markdown(res.json()["answer"])
                except Exception as e:
                    st.error(f"Error: {e}")

    with tab4:
        selected = st.selectbox("Select email", email_subjects, key="cat")
        email = emails[email_subjects.index(selected)]
        st.caption(f"From: {email['sender']} | {email['date']}")
        with st.expander("View email body"):
            st.write(email["body"])
        if st.button("🗂️ Categorize", key="btn_cat"):
            with st.spinner("Categorizing..."):
                try:
                    res = requests.post(
                        f"{API}/categorize/",
                        json={"email_body": email["body"]},
                        timeout=60
                    )
                    category = res.json()["category"]
                    # Color code the category
                    colors = {
                        "Urgent": "🔴", "Work": "🔵", "Personal": "🟢",
                        "Finance": "🟡", "Shopping": "🟠",
                        "Newsletter": "⚪", "Spam": "⛔"
                    }
                    icon = colors.get(category, "📧")
                    st.success(f"{icon} Category: **{category}**")
                except Exception as e:
                    st.error(f"Error: {e}")
else:
    st.info("👆 Click 'Load Emails' to get started!")