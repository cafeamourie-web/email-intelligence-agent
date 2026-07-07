import streamlit as st
import time
import re

# --- CORE AGENT LOGIC ---

def pii_guardrail_scrubber(email_text: str) -> str:
    """Input Guardrail: Scans text and redacts sensitive PII."""
    phone_pattern = r'\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b'
    card_pattern = r'\b(?:\d{4}[-\s]?){3}\d{4}\b'
    scrubbed_text = re.sub(phone_pattern, "[REDACTED_PHONE]", email_text)
    scrubbed_text = re.sub(card_pattern, "[REDACTED_CARD]", scrubbed_text)
    return scrubbed_text

def triage_agent(text: str) -> str:
    """Triage Agent: Categorizes email based on content."""
    text_lower = text.lower()
    if any(w in text_lower for w in ["refund", "charge", "billing", "invoice"]):
        return "Billing/Invoices"
    elif any(w in text_lower for w in ["broken", "error", "crash", "not working"]):
        return "Urgent Support"
    return "General Feedback"

def responder_agent(category: str) -> str:
    """Responder Agent: Generates a template based on category."""
    if category == "Billing/Invoices":
        return "Hello, thank you for reaching out. We have routed this to our Billing Department to look into your invoicing matter immediately."
    elif category == "Urgent Support":
        return "Hello, we are incredibly sorry for the technical issues. Our engineering team has logged this high-priority ticket."
    return "Hello, thank you for your feedback. We appreciate your input and will review it shortly."

# --- STREAMLIT UI ---

st.title("✉️ Multi-Agent Email Intelligence Platform")
user_input = st.text_area("Paste the customer email here:")

if st.button("🚀 Trigger Pipeline"):
    if user_input:
        # 1. Guardrail
        safe_text = pii_guardrail_scrubber(user_input)
        st.write("🔒 **Sanitized Input:**", safe_text)
        
        # 2. Triage
        category = triage_agent(safe_text)
        st.write("🏷️ **Classification:**", category)
        
        # 3. Response
        response = responder_agent(category)
        st.write("✉️ **Drafted Response:**", response)
    else:
        st.warning("Please paste an email first.")
