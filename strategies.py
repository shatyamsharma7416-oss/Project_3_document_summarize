import os
import asyncio
from dotenv import load_dotenv
from openai import AsyncOpenAI, OpenAI
from rich.console import Console

load_dotenv()


async def summarize_chunk(client, chunk, config: dict, prompt=None) -> str:
    system_prompt = prompt or "Generate a short summary (around 800 tokens) of the given text."
    response = await client.chat.completions.create(
        model = config["model"],
        max_tokens = 700,
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


# async def refine(chunks, config):
#     client = AsyncOpenAI(
#         base_url = BASE_URL[config["url"]],
#         api_key = os.getenv("HF_TOKEN")
#     )

#     previous_summary = ""
#     final_summary = ""
#     chunk1_summary = summarize_chunk(client, chunks[0][0], 0)
#     for i in range(len(chunks)-1):

