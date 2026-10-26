def build_prompt(document, partial=False):
    mode = ("Extract findings from this section only. Mark absent items as not mentioned in this section."
            if partial else "Analyze the provided legal document or combined section findings.")
    return f"""You are a careful legal-document analysis assistant. {mode}
Do not invent information. If an item is absent, write exactly: Not mentioned in the document.
Preserve names, dates, amounts, currencies, notice periods and clause references exactly as written.
Return a structured report with these headings:
1. Document Type
2. Parties
3. Purpose
4. Concise Summary
5. Obligations of Each Party
6. Payment Terms
7. Duration and Renewal
8. Termination Conditions
9. Important Dates and Deadlines
10. Key Clauses (confidentiality, liability, indemnity, intellectual property, dispute resolution, governing law, data protection, warranties, as applicable)
11. Ambiguities / Items to Verify
Do not provide legal advice or claim a clause is enforceable.
DOCUMENT TEXT:
{document}"""
