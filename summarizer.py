
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from dotenv import load_dotenv
import asyncio

from loader import file_extract
from chunker import chunker
from strategies import *


load_dotenv()
console = Console()

MODEL = {
    "gemini": {"model":"gemini-3-flash-preview", "url":"https://generativelanguage.googleapis.com/v1beta/", "api":"GOOGLE_AI_STUDIO"},
    "minmax": {"model":"minimax/minimax-m2.5:free", "url":"https://openrouter.ai/api/v1", "api":"OPENROUTER_API_KEY"},
    "glm": {"model":"zai-org/GLM-5.1:fireworks-ai", "url":"https://router.huggingface.co/v1", "api":"HF_TOKEN"}
}

def choose_model():
    model = {
        1: "gemini",
        2: "minmax",
        3: "glm"
    }

    console.print("[bold]Choose Model:")
    for key, m in model.items():
        console.print(f" [bold]{key}[/]. {model[key].capitalize()}")
    model_choice = int(Prompt.ask("Enter number", choices=["1", "2", "3"], default="1"))

    console.print(Panel(f"[green]Model: {model[model_choice]}[/GREEN]\n[dim]Api Provider:"\
                         f" {MODEL[model[model_choice]]["api"].upper()}", border_style='green'))

    return MODEL[model[model_choice]]

async def run_map_reduce(chunks, config):
    summaries = await map_step(chunks, config)      # await, not asyncio.run
    final = await reduce_step(summaries, config)    # await, not asyncio.run
    return final


def choose_strategy(chunks: list, config: dict):
    if len(chunks) == 1:
        console.print("\n[bold]Your documnet is small [blue]Stuff[/] method will be chosen[/]\n")
        return asyncio.run(stuff(chunks, config))
    elif len(chunks) > 1:
        console.print("\n[bold]Your document is large [blue]Map Reduce[/] will be used[/]\n")
        return asyncio.run(run_map_reduce(chunks, config))  # one single asyncio.run


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
