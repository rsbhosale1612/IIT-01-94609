import requests
from bs4 import BeautifulSoup

def screape_sunbeam():
    
    url = "https://www.sunbeaminfo.com"
    responce = requests.get(url)
    soup = BeautifulSoup(responce.text, "html.parser")

    text_data = soup.get_text(separator= " ").lower()
    return text_data

def answer_que(question, data):
    q = question.lower()


    if "internship" in q:
        return "Sunbeam provides internships for students after course completion."
    
    if "batch" in q:
        return "Sunbeam has multiple batches throughout the year."
    
    return "Based on the website, this information is not clearly mentioned."