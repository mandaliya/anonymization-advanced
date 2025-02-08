import streamlit as st
from presidio_analyzer import AnalyzerEngine, RecognizerResult
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig
import json

# Initialize Presidio Analyzer and Anonymizer

# Sidebar for NLP model selection
st.sidebar.header("🧠 NLP Model Selection")
selected_model = st.sidebar.selectbox("Choose NLP Model", ["spaCy", "Stanza"], index=0)

# Initialize Presidio Analyzer with the selected model
analyzer = AnalyzerEngine(nlp_engine_name=selected_model.lower())

anonymizer = AnonymizerEngine()

st.set_page_config(page_title="Advanced PII Anonymization", page_icon="🔒")
st.title("🔒 Advanced PII Anonymization")
st.write("This app detects and anonymizes Personally Identifiable Information (PII) using Microsoft Presidio.")

# User input text
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
selected_example = st.selectbox("📌 Select an Example Text", ["(Enter your own text)"] + list(examples.keys()))

# Default user text (either selected example or empty for custom input)
if selected_example == "(Enter your own text)":
    user_text = st.text_area("Enter text to anonymize", height=150)
else:
    user_text = st.text_area("Enter text to anonymize", examples[selected_example], height=150)

# Sidebar options
st.sidebar.header("🔍 Detection Settings")
selected_language = st.sidebar.selectbox("Select Language", ["en", "es", "fr"], index=0)
confidence_threshold = st.sidebar.slider("Confidence Threshold", 0.0, 1.0, 0.5, 0.05)

st.sidebar.header("✂️ Anonymization Settings")
available_entities = ["PERSON", "EMAIL_ADDRESS", "PHONE_NUMBER", "CREDIT_CARD", "LOCATION", "DATE_TIME"]
selected_entities = st.sidebar.multiselect("PII Entities to Detect", available_entities, default=available_entities)

anonymization_methods = {
    "mask": OperatorConfig("mask", {"masking_char": "*", "chars_to_mask": 4, "from_end": True}),
    "redact": OperatorConfig("redact", {}),
    "replace": OperatorConfig("replace", {"new_value": "[REDACTED]"}),
    "hash": OperatorConfig("hash", {}),
}
selected_method = st.sidebar.selectbox("Choose Anonymization Method", list(anonymization_methods.keys()))

if st.button("🚀 Anonymize Text"):
    if user_text:
        # Analyze text for PII
        results = analyzer.analyze(
            text=user_text, 
            entities=selected_entities, 
            language=selected_language, 
            score_threshold=confidence_threshold
        )

        # Perform anonymization
        anonymized_result = anonymizer.anonymize(
            text=user_text, 
            analyzer_results=results, 
            operators={entity: anonymization_methods[selected_method] for entity in selected_entities}
        )

        # Display results
        st.subheader("📜 Anonymized Text")
        st.write(anonymized_result.text)

        # Show extracted PII
        st.subheader("🔎 Detected PII Entities")
        if results:
            pii_info = [{"Entity": res.entity_type, "Score": res.score, "Start": res.start, "End": res.end} for res in results]
            st.json(pii_info)
        else:
            st.write("No PII detected.")

        # Download option
        st.download_button("⬇️ Download Anonymized Text", anonymized_result.text, file_name="anonymized_text.txt")

    else:
        st.warning("⚠️ Please enter some text before anonymizing.")
