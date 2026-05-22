



import pandas as pd

from openai import OpenAI
import json

from dotenv import load_dotenv
load_dotenv()
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


tools = [
    {
        "type": "function",
        "function": {
            "name": "extract_medical_info",
            "description": "Extract structured medical info from transcription",
            "parameters": {
                "type": "object",
                "properties": {
                    "age": {
                        "type": "integer"
                    },
                    "medical_specialty": {
                        "type": "string"
                    },
                    "recommended_treatment": {
                        "type": "string"
                    }
                },
                "required": ["age", "medical_specialty", "recommended_treatment"]
            }
        }
    }
]



df_structured = pd.DataFrame(columns=["age","medical_specialty","recommended_treatment","icd_code"])


icd_map = {
    "diabetes": "E11",
    "hypertension": "I10",
    "asthma": "J45"
}



def extract_icd_code(medical_specialty):
    medical_specialty = medical_specialty.lower()

    for key in icd_map:
        if key in medical_specialty:
            return icd_map[key]
        
    return "Unknown"








def extract_medical_info(df):

    for _, row in df.iterrows():

        message = row["transcription"]

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "Extract structured medical information."
                    },
                    {"role": "user", "content": message}
                ],
                tools=tools,
                tool_choice={
                    "type": "function",
                    "function": {"name": "extract_medical_info"}
                }
            )

            tool_calls = response.choices[0].message.tool_calls

            if tool_calls:

                function_call = tool_calls[0].function
                args = json.loads(function_call.arguments)

                age = args.get("age")
                medical_specialty = args.get("medical_specialty", "Unknown")
                recommended_treatment = args.get("recommended_treatment", "Unknown")

            else:
                # fallback (IMPORTANT)
                age = None
                medical_specialty = "Unknown"
                recommended_treatment = "Unknown"

            icd_code = extract_icd_code(medical_specialty)

        except Exception:
            # fallback if API fails
            age = None
            medical_specialty = "Unknown"
            recommended_treatment = "Unknown"
            icd_code = "Unknown"

        # ALWAYS append row (NEVER skip)
        df_structured.loc[len(df_structured)] = [
            age,
            medical_specialty,
            recommended_treatment,
            icd_code
        ]

    return df_structured






df= pd.read_csv("transcriptions.csv")

df_structured=extract_medical_info(df)
df_structured.to_csv("structured_data.csv", index=False)












