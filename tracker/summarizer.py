import textwrap

def summarize(messages):
    """Return a short summary for a list of messages."""
    if not messages:
        return ""
    text = " ".join(messages)
    text = textwrap.shorten(text, width=200, placeholder="...")
    return f"Summary: {text}"
