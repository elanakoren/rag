import anthropic

client = anthropic.Anthropic()

SYSTEM_PROMPT = """You are a research assistant that answers questions using only the excerpts provided below. Each excerpt is labeled with a citation number, like [1], [2], etc.

Rules:
- Answer using only the information in the provided excerpts. Do not use outside knowledge, even if you recognize the source material.
- After each claim in your answer, cite the excerpt number(s) it's based on, e.g. "...as shown in [1]." or "[1][3]" if multiple excerpts support it.
- If the excerpts don't contain enough information to answer the question, say so explicitly rather than guessing or filling gaps from general knowledge.
- Keep your answer concise and directly responsive to the question."""

def call_claude(citation_string, question):
    message = f"{question} Here are the relevant excerpts: {citation_string}"
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1000,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": message}],
    )

    return response.content[0].text
