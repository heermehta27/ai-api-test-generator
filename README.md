# AI-Assisted API Test Case Generator

An automated utility that leverages Google's Gemini API to dynamically generate structured API test cases based on sample payloads.

## Features
- **AI-Driven Test Design**: Uses `gemini-2.5-flash` to generate comprehensive scenarios based on an endpoint's structure.
- **Full Coverage**: Generates positive, negative, boundary, security, and schema validation test cases.
- **Actionable Outputs**: Outputs purely in JSON format for easy pipeline integration.
- **Automated Execution**: Plays back generated test cases against a target endpoint using `pytest` and Playwright.

## Setup Instructions

### 1. Prerequisites
- Python 3.9+
- A Google Gemini API Key

### 2. Install Dependencies
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

pip install -r requirements.txt
```

### 3. Environment variables
Copy the example environment file and add your own variables:
```bash
cp .env.example .env
```
Add your Gemini API Key and API Base URL to the `.env` file.

## Usage
Simply define your sample JSON payload inside `sample_input.json`, and run the primary script:

```bash
python main.py
```

The script will automatically generate an automated test suite matching your endpoint configuration and write it locally as `generated_test_suite.json`. Afterwards, `pytest` will kick off testing the generated inputs against the target API.
