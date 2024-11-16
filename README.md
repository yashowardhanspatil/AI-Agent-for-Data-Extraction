
# AI Agent for Data Extraction

**Project Description**

The AI Agent for Data Extraction is a powerful tool designed to automate the retrieval of specific information, such as emails or contact details, for entities listed in a CSV file or Google Sheet. This tool integrates:

- SerpAPI for web searches,
- Regex and Groq LLM for information extraction,
- A user-friendly Streamlit dashboard for interaction.
This project is ideal for researchers, marketers, and analysts needing automated data extraction capabilities.


## Features

- Supports CSV upload or Google Sheets integration for input.
- Retrieves specific information (e.g., emails, contact details) for given entities.
- Combines regex-based extraction with Groq LLM for improved accuracy.
- Allows users to export extracted results as a CSV file.
## Setup Instructions
1. Clone the Repository
```
git clone https://github.com/yashowardhanspatil/ai-agent-data-extraction.git
cd ai-agent-data-extraction

```
2. Install Dependencies

Ensure Python 3.8 or later is installed. Install required dependencies:

```
pip install -r requirements.txt
```
3. Set Up Environment Variables
```
SERPAPI_KEY=your-serpapi-api-key
GROQ_API_KEY=your-groq-api-key
```
4. Set Up Google Sheets API

        1. Enable the Google Sheets API in your Google Cloud project.

        2. Download the credentials.json file and place it in the project directory.

        3. Upon first run, the app will generate a token.json file for authentication.

5. Run the Application
Start the Streamlit app:
    
    streamlit run app.py

## Usage Guide
### Step 1: Choose Data Source

- CSV Upload: Upload a CSV file containing entity names (e.g., company names).

- Google Sheets: Paste a Google Sheet link to import data.

### Step 2: Define Search Query

Enter a prompt template like:

    Find the email address for {entity}.

The placeholder {entity} will be replaced dynamically by each entry in the selected column.

### Step 3: Start Extraction

- Click the Start Extraction button.

- The tool uses SerpAPI to search for information and Regex/Groq to extract specific details.


## API Keys & Environment Variables

- SERPAPI_KEY: Obtain from [SerpAPI](https://serpapi.com/).

- GROQ_API_KEY: Obtain from [Groq](https://groq.com/).

- Google Sheets API:

   - Enable in your [Google Cloud Console](https://developers.google.com/workspace/guides/create-project).

  - Download credentials.json and place it in the project directory.
  
## Optional Features

- Regex-Based Extraction: Efficiently extracts emails without relying on Groq for every query.
- Improved Query Design: Custom query templates to improve data retrieval accuracy.
- Error Handling: Gracefully handles missing data and API errors.
