import streamlit as st
from presidio_analyzer import AnalyzerEngine, RecognizerResult
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig
import json

# Initialize Presidio Analyzer and Anonymizer
analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()

st.title("🔒 Advanced Microsoft Presidio PII Anonymization")
st.write("This app detects and anonymizes Personally Identifiable Information (PII) using Microsoft Presidio.")

# User input text
user_text = st.text_area("Enter text to anonymize", height=150)

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
