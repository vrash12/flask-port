from transformers import pipeline
import hashlib

# Settings
MODEL = "sshleifer/distilbart-cnn-12-6"
BATCH_SIZE = 5
CACHE = {}

# Initialize the summarizer with GPU acceleration if available
try:
    summarizer = pipeline("summarization", model=MODEL, device=0)  # Use GPU if available
except Exception as e:
    print("GPU not available, using CPU: ", e)
    summarizer = pipeline("summarization", model=MODEL)  # Fallback to CPU

def hash_text(text):
    """ Generate a hash for the given text. """
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def summarize_text(text):

    text_hash = hash_text(text)
    if text_hash in CACHE:
        print("Fetching from cache.")
        return CACHE[text_hash]

    try:
        summary = summarizer(text, max_length=130, min_length=30, truncation=True)
        summary_text = summary[0]['summary_text']
        CACHE[text_hash] = summary_text  # Save to cache
        return summary_text
    except Exception as e:
        print(f"Error during summarization: {e}")
        return ""

def batch_summarize(texts):
    """ Summarize a list of texts in batches. """
    results = []
    for i in range(0, len(texts), BATCH_SIZE):
        batch = texts[i:i+BATCH_SIZE]
        try:
            summaries = summarizer(batch, max_length=130, min_length=30, truncation=True)
            batch_results = [summary['summary_text'] for summary in summaries]
            # Cache each result
            for text, summary_text in zip(batch, batch_results):
                text_hash = hash_text(text)
                CACHE[text_hash] = summary_text
            results.extend(batch_results)
        except Exception as e:
            print(f"Error during batch summarization: {e}")
            results.extend([""] * len(batch))  # Append empty strings in case of error
    return results


