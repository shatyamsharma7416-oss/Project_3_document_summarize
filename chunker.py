import tiktoken
import tiktoken


def chunker(text, chunk_size=1000, overlap=100):
    """
    Decode the Encoded file and store into chunks
    chunk size = 1000, overlap = 100
    """
    # encode the raw Text
    encoding = tiktoken.get_encoding("cl100k_base")
    file_encode = encoding.encode(text)

    chunks = []         # all chunks will be stored here
    start = 0           # Increment by 900 at every loop
    step = chunk_size - overlap

    while start < len(file_encode):
        end = start + chunk_size
        chunk = file_encode[start:end]
        chunks.append(encoding.decode(chunk))   # decode the encoded text and store in chunks

        if end >= len(file_encode):
            break

        start += step
    return chunks    # chunks -> ["first chunk", "second chunk",....]
