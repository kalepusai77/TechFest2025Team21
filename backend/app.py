from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.fact_check import verify_with_fact_check_api, verify_with_politifact
from utils.nlp_utils import extract_key_sentences
from utils.model_utils import load_pre_trained_model

app = Flask(__name__)
CORS(app)

# Load the pre-trained model
fact_checker = load_pre_trained_model()

@app.route("/check", methods=["POST"])
def check():
    data = request.get_json()
    if "article" not in data:
        return jsonify({"error": "No article text provided"}), 400

    article_text = data["article"]
    sentences = extract_key_sentences(article_text)

    results = []
    for sentence in sentences:
        # Classify the sentence using the pre-trained model
        model_result = fact_checker(sentence)

        label_mapping = {
            "entailment": "true",
            "contradiction": "false",
            "neutral": "unverified"
        }

        confidence_threshold = 0.6 

        if model_result[0]["score"] < confidence_threshold:
            user_friendly_label = "unverified"
        else:
            user_friendly_label = label_mapping.get(model_result[0]["label"], "unverified")
        
        
        
        # Verify with external APIs
        fact_check_result = verify_with_fact_check_api(sentence)
        politifact_result = verify_with_politifact(sentence)

        results.append({
            "sentence": sentence,
            "label": user_friendly_label,
            "confidence": model_result[0]["score"],
            "fact_check_verification": fact_check_result,
            "politifact_verification": politifact_result,
        })
    
    return jsonify({"results": results})

if __name__ == "__main__":
    app.run(debug=True)