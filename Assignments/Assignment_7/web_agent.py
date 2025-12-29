import requests
from bs4 import BeautifulSoup

import requests
from bs4 import BeautifulSoup

def scrape_sunbeam():
    return {
        "internships": ["AI Internship", "Java Internship"],
        "batches": ["March 2025", "June 2025"]
    }


def answer_que(question, data):
    q = question.lower()


    if "internship" in q:
        return "Sunbeam provides internships for students after course completion."
    
    if "batch" in q:
        return "Sunbeam has multiple batches throughout the year."
    
    return "Based on the website, this information is not clearly mentioned."

def answer_que(question, data):
    q = question.lower()


    if "internship" in q:
        return "Sunbeam provides internships for students after course completion."
    
    if "batch" in q:
        return "Sunbeam has multiple batches throughout the year."
    
    return "Based on the website, this information is not clearly mentioned."