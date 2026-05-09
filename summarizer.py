
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from openai import AsyncOpenAI
from dotenv import load_dotenv
from pypdf import PdfReader
from pathlib import Path
import tiktoken
import aiohttp
import asyncio
import os
import time

from loader import file_extract
from chunker import chunker
from strategies import *


load_dotenv()
console = Console()

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


def choose_model():
    MODEL = {
        1: "gemini",
        2: "minmax",
        3: "glm"
    }
    BASE_URL = {
        1: "huggingface",
        2: "openrouter",
        3: "google"

    }

    console.print("[bold]Choose Model:")
    for key, m in MODEL.items():
        console.print(f" [bold]{key}[/]. {MODEL[key].capitalize()}")
    model_choice = int(Prompt.ask("Enter number", choices=["1", "2", "3"], default="1"))

    if model_choice != 1:
        console.print("[bold]Choose API:")
        console.print(f" [bold]1. Hugging Face")
        console.print(f" [bold]2. Open Router")
        api_choice = int(Prompt.ask("Enter number", choices=["1", "2"], default=1))
    else:
        api_choice = 3

    console.print(Panel(f"[green]Model: {MODEL[model_choice]}[/GREEN]\n[dim]Api Provider: {BASE_URL[api_choice].upper()}", border_style='green'))

    return {"model":MODEL[model_choice], "url":BASE_URL[api_choice]}


def choose_strategy(chunks: list, config: dict):
    if len(chunks) == 1:
        console.print("\n[bold]Your documnet is small [blue]Stuff[/] method will be chosen[/]\n")
        return asyncio.run(stuff(chunks, config))
    elif len(chunks) > 1:
        console.print("\n[bold]Your document is large [blue]Map Reduce[/] will be used[/]\n")
        summaries = asyncio.run(map_step(chunks, config))
        return asyncio.run(reduce_step(summaries, config))


def main():
    console.print(Panel("[bold][bold green]Welcome to our Document summarizer[/][/]\n", border_style="green"))

    text, tokens = file_extract()
    console.print("[green]File extraction successfull.[/]")

    model = choose_model()

    console.print("[blue]Chunking...[/]")
    chunks = chunker(text)
    console.print(f"\n[bold][blue]{len(chunks)}[/][/] Chunks Created.")

    reply = choose_strategy(chunks[:3], model)
    console.print(f"[bold][green]Bot[/green]: {reply}[/bold]")




if __name__ == "__main__":
    main()
