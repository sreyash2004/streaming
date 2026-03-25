def build_prompt(profile, docs):

    doc_text = "\n".join([doc.page_content for doc in docs])

    prompt = f"""
You are an AI Visa Officer.

Analyze the applicant profile and visa rules.

------------------------
APPLICANT PROFILE:
{profile}

------------------------
VISA RULES:
{doc_text}

------------------------

TASK:

1. Decide: ELIGIBLE or NOT ELIGIBLE
2. Give clear REASON
3. If NOT ELIGIBLE → give IMPROVEMENTS
4. Give CONFIDENCE SCORE (0–100%)

------------------------

FORMAT STRICTLY:

ELIGIBILITY: ELIGIBLE / NOT ELIGIBLE  
REASON: ...  
IMPROVEMENTS: ...  
CONFIDENCE SCORE: ...%

"""

    return prompt
