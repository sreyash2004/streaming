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

def retrieve_documents(query, k=2):

    query_lower = query.lower()
    docs = []

    for country, visas in visa_data.items():
        if country in query_lower:
            for visa, text in visas.items():
                if visa in query_lower:
                    docs.append(
                        Document(
                            page_content=text,
                            metadata={"country": country, "visa_type": visa}
                        )
                    )

    if not docs:
        docs.append(
            Document(
                page_content="Visa depends on funds, background, and country rules.",
                metadata={"country": "General", "visa_type": "General"}
            )
        )

    return docs[:k]
