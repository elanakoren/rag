import asyncio
from rag import _ragas_compat  # noqa: F401 - must run before any ragas import
from anthropic import AsyncAnthropic
from ragas.llms import llm_factory
from ragas.metrics.collections import Faithfulness
from langfuse import get_client
import chromadb

from rag.cli import ask_question
from rag.golden_dataset import GOLDEN_DATASET

async def evaluate() -> None:
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_collection(name='library')

    anthropic_client = AsyncAnthropic()
    llm = llm_factory("claude-haiku-4-5-20251001", provider="anthropic", client=anthropic_client, max_tokens=4096)
    scorer = Faithfulness(llm=llm)

    for case in GOLDEN_DATASET:
        answer, excerpts = ask_question(
            collection,
            case['book_title'],
            case['percentage'],
            case['question'],
        )
        result = await scorer.ascore(
            user_input=case['question'],
            response=answer,
            retrieved_contexts=[e['text'] for e in excerpts],
        )
        print(f"[{case['percentage']}%] {case['question']}")
        print(f"  answer: {answer}")
        print(f"  faithfulness: {result.value}")
        print()

    get_client().flush()

def main() -> None:
    asyncio.run(evaluate())
