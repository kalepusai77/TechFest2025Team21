import requests
from bs4 import BeautifulSoup
import os

def verify_with_fact_check_api(claim):
    url = f"https://factchecktools.googleapis.com/v1alpha1/claims:search?query={claim}&key={os.getenv('FACT_CHECK_API_KEY')}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if "claims" in data:
            return data["claims"][0]["claimReview"][0]["textualRating"]
    
    return "No fact-check available"

def verify_with_politifact(claim):
    try:
        search_url = f"https://www.politifact.com/search/?q={claim}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        result = soup.find("div", class_="c-textgroup__title")
        if result:
            rating = result.find("img")["alt"]
            return rating
        
        return "No fact-check available"
    
    except Exception as e:
        print(f"Error scraping PolitiFact: {e}")
        return "No fact-check available"