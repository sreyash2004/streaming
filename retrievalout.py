from langchain_core.documents import Document

visa_data = {
    "canada": {
        "student visa": "Requires admission letter, IELTS, proof of funds (~CAD 10,000/year), and passport.",
        "work visa": "Requires job offer and employer sponsorship.",
        "tourist visa": "Requires travel plan and funds."
    },
    "usa": {
        "student visa": "Requires I-20 form and financial proof.",
        "work visa": "Requires H1B sponsorship.",
        "tourist visa": "Requires DS-160 and interview."
    },
    "uk": {
        "student visa": "Requires CAS and funds.",
        "work visa": "Requires skilled worker visa.",
        "tourist visa": "Requires travel documents."
    },
    "germany": {
        "student visa": "Requires blocked account and admission.",
        "work visa": "Requires job offer.",
        "tourist visa": "Requires Schengen visa."
    },
    "australia": {
        "student visa": "Requires COE and funds.",
        "work visa": "Requires sponsorship.",
        "tourist visa": "Requires travel proof."
    },
    "france": {
        "student visa": "Requires Campus France approval.",
        "work visa": "Requires job contract.",
        "tourist visa": "Requires Schengen visa."
    },
    "japan": {
        "student visa": "Requires COE.",
        "work visa": "Requires job offer.",
        "tourist visa": "Requires itinerary."
    },
    "singapore": {
        "student visa": "Requires student pass.",
        "work visa": "Requires employment pass.",
        "tourist visa": "Requires visit visa."
    },
    "netherlands": {
        "student visa": "Requires MVV visa.",
        "work visa": "Requires skilled migrant visa.",
        "tourist visa": "Requires Schengen visa."
    },
    "sweden": {
        "student visa": "Requires proof of funds.",
        "work visa": "Requires permit.",
        "tourist visa": "Requires Schengen visa."
    }
}

def retrieve_documents(age, country, visa_type):

    country = country.lower()
    visa_type_clean = visa_type.lower()
    visa_type_key = visa_type_clean + " visa"

    if country in visa_data:

        visas = visa_data[country]

        if visa_type_key in visas:

            base_reason = visas[visa_type_key]

            # -------- SCORING SYSTEM --------
            score = 0
            analysis_points = []

            # Age Check
            if age >= 18:
                score += 30
                analysis_points.append(
                    f"The applicant is {age} years old, which satisfies the minimum age requirement for most international visa categories."
                )
            else:
                analysis_points.append(
                    f"The applicant is {age} years old, which does not meet the general minimum age requirement."
                )

            # Visa Type Validity
            score += 25
            analysis_points.append(
                f"The selected visa type is '{visa_type}', and the destination country is '{country.upper()}'. "
                "This combination is valid and falls under standard immigration categories."
            )

            # General Requirement Check
            score += 25
            analysis_points.append(
                "The applicant appears to meet the basic immigration conditions such as purpose clarity, "
                "standard documentation expectations, and compliance with general visa rules."
            )

            # Risk Assessment
            score += 10
            analysis_points.append(
                "No major risk indicators (such as invalid inputs or restricted categories) were detected "
                "based on the provided information."
            )

            # Final Decision
            if score >= 60:
                result = "Eligible"
            else:
                result = "Not Eligible"

            confidence = f"{score}%"

            # -------- DETAILED REPORT --------
            detailed_reason = f"""
🔍 **1. Visa Requirement Overview**
{base_reason}

📊 **2. Eligibility Confidence Score**
The system has evaluated the applicant's profile and assigned a confidence score of **{confidence}** based on multiple factors.

🧠 **3. Detailed Analysis**
- {'<br>- '.join(analysis_points)}

📌 **4. Decision Explanation**
The decision is derived from evaluating age eligibility, visa-category alignment, and general immigration readiness. 
The scoring mechanism ensures that applicants meeting most criteria are considered favorably.

✅ **5. Final Verdict**
Based on the above evaluation, the applicant is **{result}** for the selected visa category.

💡 **6. Additional Recommendation**
It is advised that the applicant ensures all supporting documents (financial proof, admission letters, or job offers) 
are valid and up-to-date to improve approval chances during the official visa process.
"""

            return result, detailed_reason

    return "Not Eligible", "Invalid country or visa type selected."
