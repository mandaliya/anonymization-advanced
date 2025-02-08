import streamlit as st
from presidio_analyzer import AnalyzerEngine
from presidio_analyzer.nlp_engine import NlpEngineProvider, SpacyNlpEngine, StanzaNlpEngine

# Set browser title
st.set_page_config(page_title="Advanced Presidio PII Anonymization", page_icon="🔒")

# Sidebar for NLP model selection
st.sidebar.header("🧠 NLP Model Selection")
selected_model = st.sidebar.selectbox("Choose NLP Model", ["spaCy", "Stanza"], index=0, key="nlp_model_selector")

# Initialize NLP Engine correctly based on selection
if selected_model == "spaCy":
    nlp_engine = SpacyNlpEngine(models={"en": "en_core_web_lg"})  # Using large spaCy model
elif selected_model == "Stanza":
    nlp_engine = StanzaNlpEngine(models={"en": "en"})  # Default Stanza English model

# Initialize Presidio Analyzer with the correct NLP engine
analyzer = AnalyzerEngine(nlp_engine=nlp_engine)

# Set up UI
st.title("🔍 PII Anonymization with Microsoft Presidio")
st.subheader("✍️ Enter Your Own Text or Select an Example")

# Example texts
examples = {
    "General PII Information": """John Doe's email is john.doe@example.com, and his phone number is +1-555-123-4567. 
He lives at 789 Elm Street, Los Angeles, CA, and his credit card number is 4111 1111 1111 1111. 
His birth date is January 10, 1990.""",

    "Financial & Banking Information": """Emma Johnson recently opened an account at Chase Bank. 
Her account number is 123456789, and her Social Security Number is 987-65-4321. 
She paid $1,500 using her Visa card ending in 4242.""",

    "Medical & Health Records": """Dr. Robert Smith is a cardiologist at Boston Medical Center. 
His patient, Alice Brown, was diagnosed with hypertension on April 5, 2023. 
Her medical record ID is 56789 and her insurance number is ABCD-1234-XYZ.""",

    "Corporate & Workplace Data": """Michael Johnson works at Google as a software engineer. 
His work email is michael.johnson@google.com, and his direct phone number is (415) 555-9876. 
He joined Google on August 15, 2018.""",

    "Government & Legal Documents": """Sarah Parker’s passport number is A12345678, and her driver's license is DL-9876543. 
She filed her taxes with the IRS under EIN 12-3456789. 
Her legal case ID is 2023-LAW-4567 in the New York District Court."""
}

# Dropdown for selecting example texts
selected_example = st.selectbox("📌 Select an Example Text", ["(Enter your own text)"] + list(examples.keys()), key="example_selector")

# Default user text (either selected example or empty for custom input)
if selected_example == "(Enter your own text)":
    user_text = st.text_area("Enter text to anonymize", height=150)
else:
    user_text = st.text_area("Enter text to anonymize", examples[selected_example], height=150)

# Analyze and Anonymize Button
if st.button("🔍 Analyze & Anonymize"):
    if not user_text.strip():
        st.warning("⚠️ Please enter some text.")
    else:
        results = analyzer.analyze(text=user_text, entities=[], language="en")
        st.write("📊 **Detected Entities:**", results)