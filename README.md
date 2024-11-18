# PDF Journal Creator

A Streamlit web application that uses OpenAI's Assistant API to create structured journal entries from PDF documents.

## Features

- PDF text extraction
- AI-powered journal creation using OpenAI Assistant
- Clean and intuitive user interface
- Download generated journal entries

## Setup

1. Fork this repository
2. Deploy on Streamlit Cloud:
   - Connect your GitHub account
   - Deploy this repository
   - Add your secrets in the Streamlit dashboard

### Required Secrets

In the Streamlit dashboard, add the following secrets:

```toml
OPENAI_API_KEY = "your-openai-api-key"
ASSISTANT_ID = "your-assistant-id"
```

## Local Development

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Create a `.streamlit/secrets.toml` file with your secrets
4. Run the app:
```bash
streamlit run app.py
```

## License

MIT License
