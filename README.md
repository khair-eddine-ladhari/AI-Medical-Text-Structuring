# AI Medical Text Structuring

Automatically extract structured medical information from raw transcriptions using OpenAI function calling and export the results to a clean CSV file.

---

## What it does

- Reads a CSV file of medical transcriptions
- Uses **GPT-4o-mini** with function calling to extract structured fields
- Maps medical specialties to **ICD codes**
- Exports the structured data to a new CSV file

---

## Output fields

| Field | Description |
|---|---|
| `age` | Patient age extracted from transcription |
| `medical_specialty` | Detected medical specialty |
| `recommended_treatment` | Suggested treatment from transcription |
| `icd_code` | Mapped ICD-10 code |

---

## Project structure

```
project/
├── main.py                  # Main script
├── transcriptions.csv       # Input file (your data)
├── structured_data.csv      # Output file (generated)
├── .env                     # Your API key (never push)
├── .env.example             # Template for API key
└── requirements.txt         # Dependencies
```

---

## Getting started

### 1. Clone the repository

```bash
git clone https://github.com/khair-eddine-ladhari/AI-Medical-Text-Structuring.git
cd AI-Medical-Text-Structuring
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up environment variables

Create a `.env` file in the root folder:

```
OPENAI_API_KEY=your_openai_api_key_here
```

### 4. Add your input file

Make sure `transcriptions.csv` exists with a column named `transcription`.

Example:

```
transcription
"Patient is a 45 year old male with diabetes. Recommended metformin."
"55 year old female with hypertension. Prescribed lisinopril."
```

### 5. Run the script

```bash
python main.py
```

The output will be saved as `structured_data.csv`.

---

## ICD codes supported

| Condition | ICD-10 Code |
|---|---|
| Diabetes | E11 |
| Hypertension | I10 |
| Asthma | J45 |

> More conditions can be added easily in the `icd_map` dictionary.

---

## Requirements

```
pandas
openai
python-dotenv
```

---

## Environment variables

| Variable | Description |
|---|---|
| `OPENAI_API_KEY` | Your OpenAI API key |

---

## Notes

- The script always appends a row even if the API fails (fallback to `Unknown`)
- ICD code mapping is keyword-based and can be extended
- Uses `gpt-4o-mini` for cost efficiency

---

## Author

**Khair-Eddine Ladhari** — [GitHub](https://github.com/khair-eddine-ladhari)
