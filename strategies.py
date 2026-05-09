import os
import asyncio
from dotenv import load_dotenv
from openai import AsyncOpenAI, OpenAI
from rich.console import Console

load_dotenv()
MODEL = {
    "gemini": "gemini-3-flash-preview",
    "minmax": "minimax/minimax-m2.5:free",
    "glm": "zai-org/GLM-5.1:fireworks-ai"
}

BASE_URL = {
    "huggingface": "https://router.huggingface.co/v1",
    "openrouter": "https://openrouter.ai/api/v1",
    "google": "https://generativelanguage.googleapis.com/v1beta/"
}

async def summarize_chunk(client, chunk, index, config: dict) -> str:
    Console().print("[yellow]Summarizing...[/]")
    response = await client.chat.completions.create(
        model = MODEL[config["model"]],
        max_tokens = 1000,
        messages=[
            {"role": "system", "content":"generate short summary(around 800 tokens) of the given text"},
            {"role": "user", "content": chunk}
        ]
    )

    return response.choices[0].message.content

async def map_step(chunks, config) -> list:
    client = AsyncOpenAI(
        base_url = BASE_URL[config["url"]],
        api_key = os.getenv("GOOGLE_AI_STUDIO"),
    )

    # create a task for every chunk
    tasks = [summarize_chunk(client, chunk, i, config) for i, chunk in enumerate(chunks)]

    # fire all tasks in parallel, wait for all
    summaries = await asyncio.gather(*tasks)
    return list(summaries)


async def reduce_step(Summary_chunks, config) -> str:
    client = AsyncOpenAI(
        base_url = BASE_URL[config["url"]],
        api_key = os.getenv("GOOGLE_AI_STUDIO")
    )

    chunk = " ".join(Summary_chunks)

    # create a single summary
    summary = await summarize_chunk(client, chunk, 0, config)

    return summary


async def stuff(chunk, config):
    """ 
    summarize small document
    """

    client = AsyncOpenAI(
        base_url = BASE_URL[config["url"]],
        api_key = os.getenv("HF_TOKEN")
    )

    # get summary
    summary = await summarize_chunk(client, chunk[0], 0, config)
    print(summary)

    return summary
