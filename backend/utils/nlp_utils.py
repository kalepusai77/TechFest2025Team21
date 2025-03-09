import spacy

# Load Spacy English model
nlp = spacy.load("en_core_web_sm")

def extract_key_sentences(article_text, max_sentences=5):
    """
    Extract key sentences from the article using Spacy.
    
    Args:
        article_text (str): The input article text.
        max_sentences (int): Maximum number of sentences to extract.
    
    Returns:
        list: A list of key sentences.
    """
    doc = nlp(article_text)
    sentences = [sent.text.strip() for sent in doc.sents]
    return sentences[:max_sentences]