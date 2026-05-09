from rich.console import Console
from rich.prompt import Prompt
from pypdf import PdfReader
from pathlib import Path
import tiktoken



console = Console()

def file_extract():
    """
    Extracts Text from PDF file
    returns Extracted file's encoding
    and number of tokens
    """
    while True:
        # Take file path from user
        file_path = Prompt.ask("[blue]Provide the path of your file[/]")
        file_path = str(Path(file_path))
        doc_content = ""


        # If user file not exists
        try:
            if file_path.endswith(".pdf"):
                reader = PdfReader(file_path)

                # Extract page by page
                for p_no in range(len(reader.pages)):
                    page = reader.pages[p_no].extract_text(0)
                    doc_content += page

            elif file_path.endswith(".txt"):
                with open(file_path, 'r', encoding='utf-8') as f:
                    doc_content += f.read()
            else:
                console.print("\n[red]Provided file should be .pdf or .txt file[/]\n")  
                continue     # ← go back to top, ask again
                
        except FileNotFoundError:
            console.print("\n[red][bold]Please provide a valid file.[/][/]\n")
            continue        # ← go back to top, ask again

        # token encoding -> used for convert into token after chunking convert into string
        encoding = tiktoken.get_encoding("cl100k_base")

        # Saving extracted file
        file_name = Path(file_path).stem
        with open(f"files/{file_name}.txt", "w", encoding="utf-8") as f:
            f.write(doc_content)

        # token count
        tokens = len(encoding.encode(doc_content))
        console.print(f"\nYour file contians [blue][bold]{tokens}[/][/] tokens.")

        return doc_content, tokens
