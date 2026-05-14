
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from dotenv import load_dotenv
import asyncio
import tomllib


from loader import file_extract
from chunker import chunker
from strategies import *


load_dotenv()
console = Console()

def choose_model():

    model = {
        1: "gemini",
        2: "minmax",
        3: "glm",
        4: "qwen"
    }

    console.print("[bold]Choose Model:")
    for key, m in model.items():
        console.print(f" [bold]{key}[/]. {model[key].capitalize()}")
    model_choice = int(Prompt.ask("Enter Number", choices=["1", "2", "3"], default="1"))

    # read toml file
    with open("llm_config.toml", 'rb') as f:
        llm_config = tomllib.load(f)

    ACTIVE_MODEL = model[model_choice]
    llm = {
        "BASE_URL": llm_config['models'][ACTIVE_MODEL]["url"],
        "API": llm_config['models'][ACTIVE_MODEL]["api"],
        "MODEL": llm_config['models'][ACTIVE_MODEL]["name"]
    }

    return llm


async def run_map_reduce(chunks, config):
    summaries = await map_step(chunks, config)      # await, not asyncio.run
    final = await reduce_step(summaries, config)    # await, not asyncio.run
    return final


def choose_strategy(chunks: list, config: dict):
    if len(chunks) == 1:
        console.print("\n[bold]Your documnet is small [blue]Stuff[/] method will be chosen[/]\n")
        return asyncio.run(stuff(chunks, config))
    
    elif len(chunks) > 1:

        console.print("\n[bold]Your document is large choose one method to summarize:\n[bold]1. Map Reduce[/]\n2. Refine")
        method = int(Prompt.ask("Enter Number", choices=["1", "2"], default=1))
        
        # Map Reduce Method
        if method == 1:
            return asyncio.run(run_map_reduce(chunks, config))  # one single asyncio.run
        
        # Refine Method
        elif method == 2:
            return asyncio.run(refine(chunks, config))



def main():
    console.print(Panel("[bold][bold green]Welcome to our Document summarizer[/][/]\n", border_style="green"))

    text, tokens = file_extract()
    console.print("[green]File extraction successfull.[/]")

    model = choose_model()

    console.print("[blue]Chunking...[/]")
    chunks = chunker(text)
    console.print(f"\n[bold][blue]{len(chunks)}[/][/] Chunks Created.")

    reply = choose_strategy(chunks, model)
    console.print(f"[bold][green]Bot[/green]: {reply}[/bold]")




if __name__ == "__main__":
    main()

