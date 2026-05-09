import os
import asyncio
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()


async def summarize_chunk(client, chunk: str, config: dict, prompt=None) -> str:
    system_prompt = prompt or "Generate a short summary (around 800 tokens) of the given text."
    response = await client.chat.completions.create(
        model = config["model"],
        max_tokens = 900,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": chunk}
        ]
    )

    return response.choices[0].message.content

async def map_step(chunks, config) -> list:
    client = AsyncOpenAI(
        base_url = config["url"],
        api_key = os.getenv(config["api"])
    )

    # create a task for every chunk
    tasks = [summarize_chunk(client, chunk, config) for chunk in chunks]

    # fire all tasks in parallel, wait for all
    summaries = await asyncio.gather(*tasks)
    return list(summaries)


async def reduce_step(Summary_chunks, config) -> str:
    reduce_prompt = "You are given summaries of different sections of a document. Combine them into one coherent, concise final summary."

    client = AsyncOpenAI(
        base_url = config["url"],
        api_key = os.getenv(config["api"])
    )
    print(Summary_chunks)
    chunk = " ".join(Summary_chunks)

    # create a single summary
    summary = await summarize_chunk(client, chunk, config, reduce_prompt)

    return summary


async def stuff(chunk, config):
    """ 
    summarize small document
    """

    client = AsyncOpenAI(
        base_url = config["url"],
        api_key = os.getenv(config["api"])
    )

    # get summary
    summary = await summarize_chunk(client, chunk[0], config)

    return summary


async def refine(chunks: list, config:dict):
    """
    Usage previous summary and current chunk to generate summary.
    """
    client = AsyncOpenAI(
        base_url = config["url"],
        api_key = os.getenv(config["api"])
    )

    running_summary = await summarize_chunk(client, chunks[0], config)

    for chunk in chunks[1:]:
        print(chunk)
        print("\n\n\n\n")
        refine_prompt = f"""You have a running summary so far:
---
{running_summary}
---
Refine and extend it with the following new section. Do not lose important information."""
        running_summary = await summarize_chunk(client, chunks[0], config, refine_prompt)
    
    return running_summary

