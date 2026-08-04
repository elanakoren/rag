import anthropic
from opentelemetry.instrumentation.anthropic import AnthropicInstrumentor
from langfuse import get_client, propagate_attributes

AnthropicInstrumentor().instrument()
get_client()

client = anthropic.Anthropic()

SYSTEM_PROMPT = """You are a reading companion helping someone who is in the middle of reading a book. You answer questions using only the excerpts provided below, which have been selected from the portion of the book the reader has already read. Each excerpt is labeled with a citation number, like [1], [2], etc.

Rules:
- Answer using only the information in the provided excerpts. Do not use outside knowledge, even if you recognize the book — your own knowledge of it may include events the reader hasn't reached yet, and revealing them would be a spoiler.
- Never reveal or hint at plot points, character developments, or events beyond what's contained in the provided excerpts, even if asked directly. If answering fully would require spoiling something ahead of the reader's current position, say so explicitly instead of answering.
- After each claim in your answer, cite the excerpt number(s) it's based on, e.g. "...as shown in [1]." or "[1][3]" if multiple excerpts support it.
- If the excerpts don't contain enough information to answer the question, say so explicitly rather than guessing or filling gaps from general knowledge.
- Keep your answer concise and directly responsive to the question."""

def call_claude(citation_string, question, book_title, current_percentage):
    message = f"{question} Here are the relevant excerpts: {citation_string}"
    with propagate_attributes(
        session_id=book_title,
        metadata={
            "question": question,
            "book_title": book_title,
            "current_percentage": current_percentage,
        },
        tags=["rag-query"],
    ):
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1000,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": message}],
        )

    return response.content[0].text
