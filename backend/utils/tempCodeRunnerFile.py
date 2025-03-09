from transformers import pipeline

def load_pre_trained_model():
    """
    Load a pre-trained model from Hugging Face's model hub.
    
    Returns:
        pipeline: A text classification pipeline.
    """
    try:
        # Load a pre-trained model for text classification
        model_name = "facebook/bart-large-mnli"
        fact_checker = pipeline("text-classification", model=model_name)
        print(f"Loaded pre-trained model: {model_name}")
        return fact_checker
    except Exception as e:
        print(f"Error loading pre-trained model: {e}")
        raise