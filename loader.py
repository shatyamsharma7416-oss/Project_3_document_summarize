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

    # Take file path from user
    file_path = Prompt.ask("[blue]Provide the path of your file[/]")
    file_path = str(Path(file_path))

    # If user file not exists
    try:
        if file_path.endswith(".pdf"):
            reader = PdfReader(file_path)
        elif file_path.endswith(".txt"):
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = f.read()
        else:
            console.print("\n[red]Provided file should be .pdf or .txt file[/]\n")
            file_extract()
            
    except FileNotFoundError:
        console.print("\n[red][bold]Please provide a valid file.[/][/]\n")
        file_extract()

    else:
        # token encoding -> used for convert into token after chunking convert into string
        encoding = tiktoken.get_encoding("cl100k_base")
        doc_content = ""

        # Extract page by page
        for p_no in range(reader.pages.__len__()):
            page = reader.pages[p_no].extract_text(0)
            doc_content += page

        # Saving extracted file
        file_name = Path(file_path).stem
        with open(f"files/{file_name}.txt", "w", encoding="utf-8") as f:
            f.write(doc_content)

        # File encoded
        file_encode = encoding.encode(doc_content)
        # token count
        tokens = len(encoding.encode(doc_content))
        console.print(f"\nYour file contians [blue][bold]{tokens}[/][/] tokens.")

        return doc_content, tokens
