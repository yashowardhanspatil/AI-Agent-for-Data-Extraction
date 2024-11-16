import os
import re
import time
import streamlit as st
import pandas as pd
from serpapi import Client
from groq import Groq
from dotenv import load_dotenv
from accessSheets import fetch_data

load_dotenv()
SERPAPI_KEY = os.getenv("SERPAPI_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def search_web_with_serpapi(query):
    client = Client(api_key=SERPAPI_KEY)
    result = client.search(q=query, hl="en", gl="in")
    return result.get("organic_results", [])

def extract_emails_from_snippets(snippets):
    text = " ".join(snippets)
    emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    return emails[0] if emails else None

def extract_email_with_groq(snippets, entity):
    client = Groq(api_key=GROQ_API_KEY)
    combined_snippets = " ".join(snippets)
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": (
                    f"Extract the official email address of {entity} from the following text:\n\n"
                    f"{combined_snippets}\n\n"
                    "Only provide the email address, nothing else."
                ),
            }
        ],
        model="llama3-8b-8192",
    )
    return chat_completion.choices[0].message.content.strip()

st.title("AI Agent for Data Extraction")
st.write("Upload a CSV file or provide a Google Sheet link to extract specific information using AI.")


data_source = st.radio("Choose Data Source", ("CSV Upload", "Google Sheets Link"))

if data_source == "CSV Upload":
    uploaded_file = st.file_uploader("Upload a CSV file", type="csv")
    if uploaded_file:
        data = pd.read_csv(uploaded_file)
        st.write("Data Preview:")
        st.write(data.head())
else:
    google_sheet_url = st.text_input("Enter Google Sheet URL")
    if google_sheet_url:
        try:
        
            sheet_id = google_sheet_url.split("/d/")[1].split("/")[0]
            data = fetch_data(sheet_id, range_name="A:Z")
            st.write("Data Preview:")
            st.write(data.head())
        except Exception as e:
            st.error("Could not access the Google Sheet. Please ensure the link is correct and shared with the app.")


if 'data' in locals() and not data.empty:
    main_column = st.selectbox("Select the main column", data.columns)

    prompt_template = st.text_input("Enter your prompt (use {entity} as placeholder)", "Find the email for {entity}")

    if st.button("Start Extraction"):
        st.write("Extracting information...")
        results = []

        for entity in data[main_column]:

            query = f"{entity} contact email"

            search_results = search_web_with_serpapi(query)
            snippets = [result.get("snippet", "") for result in search_results]

            extracted_email = extract_emails_from_snippets(snippets)

            if not extracted_email:
                extracted_email = extract_email_with_groq(snippets, entity)

            results.append({"Entity": entity, "Extracted Info": extracted_email or "No data found"})

            time.sleep(1)

        output_df = pd.DataFrame(results)
        st.write("Extracted Information:")
        st.write(output_df)

        csv = output_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download Results as CSV",
            data=csv,
            file_name="extracted_results.csv",
            mime="text/csv",
        )
