def chunk_text(text: str, chunk_size: int = 400):
    words = text.split()
    # join for strip return spaces between the words
    return [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]