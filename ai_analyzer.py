import os
import google.generativeai as genai
from dotenv import load_dotenv


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=api_key)


def analyze_resume(resume_text, job_description=""):

    model = genai.GenerativeModel("gemini-3.6-flash")

    prompt = f"""
You are an expert resume analyzer and job matching assistant.

Analyze the resume carefully.

RESUME:
{resume_text}

TARGET JOB DESCRIPTION:
{job_description}

IMPORTANT JSON RULES:

1. Return ONLY one valid JSON object.
2. Do NOT return Markdown.
3. Do NOT use ``` or ```json.
4. Do NOT add explanations before or after the JSON.
5. Make sure every JSON string is enclosed in double quotes.
6. Make sure every item in an array is separated by a comma.
7. Make sure there are NO trailing commas.
8. Make sure all brackets and braces are properly closed.
9. The response must be directly parseable using Python json.loads().
10. Do not invent skills that are not present in the resume.

Use exactly this structure:

{{
    "skills_detected": [],
    "missing_skills": [],
    "resume_score": 0,
    "score_explanation": "",
    "job_role_match": [
        {{
            "role": "",
            "match_percentage": 0,
            "reason": ""
        }},
        {{
            "role": "",
            "match_percentage": 0,
            "reason": ""
        }},
        {{
            "role": "",
            "match_percentage": 0,
            "reason": ""
        }}
    ],
    "suggestions": [],
    "job_description_match": null
}}

Rules:

- skills_detected: list only technical and professional skills actually found in the resume.
- missing_skills: important general skills that would improve the candidate's profile.
- resume_score: integer from 0 to 100.
- score_explanation: short explanation of the resume score.
- job_role_match: exactly 3 suitable job roles.
- match_percentage: integer from 0 to 100.
- reason: short explanation for each job role.
- suggestions: exactly 5 practical suggestions for improving the resume.

TARGET JOB MATCH:

If the target job description is NOT empty, replace "job_description_match": null with:

"job_description_match": {{
    "match_score": 0,
    "matching_skills": [],
    "missing_job_skills": [],
    "suggestions": []
}}

Rules for job_description_match:

- match_score: integer from 0 to 100.
- matching_skills: skills present in both the resume and target job description.
- missing_job_skills: important skills required by the target job but missing from the resume.
- suggestions: exactly 3 practical suggestions specifically for the target job.

If the target job description is empty:

"job_description_match": null

FINAL CHECK BEFORE RESPONDING:

Make sure the JSON is valid.
Make sure commas are present between all array items.
Make sure there are no comments.
Make sure there is no Markdown.
Return ONLY the JSON object.
"""

    response = model.generate_content(prompt)

    return response.text