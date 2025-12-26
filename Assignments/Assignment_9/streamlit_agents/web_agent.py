from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time


def scrape_sunbeam():
    """
    Scrape placement & admission related pages from Sunbeam website
    Returns list of text blocks
    """

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )

    urls = [
        "https://sunbeaminfo.com/placement",
        "https://sunbeaminfo.com/admissions"
    ]

    data = []

    for url in urls:
        driver.get(url)
        time.sleep(5)

        elements = driver.find_elements(
            By.XPATH, "//p | //li | //h2 | //h3 | //div"
        )

        for el in elements:
            text = el.text.strip()
            if len(text) > 40:
                data.append(text)

    driver.quit()
    return list(set(data)) 


def answer_question(data, question):
    """
    Flexible answering using partial keyword matching
    """

    question = question.lower()

    internship_keywords = [
        "intern", "industry", "project", "training", "placement"
    ]

    batch_keywords = [
        "batch", "admission", "start", "schedule", "date"
    ]

    matched_lines = []

    if "intern" in question:
        keywords = internship_keywords
    elif "batch" in question or "start" in question or "admission" in question:
        keywords = batch_keywords
    else:
        return (
            "Please ask about internship or batch/admission information."
        )

    for line in data:
        for key in keywords:
            if key in line.lower():
                matched_lines.append(line)
                break

    if matched_lines:
        return "\n\n".join(matched_lines[:3])

    return (
        "The Sunbeam website mentions industry-oriented training, "
        "placements, and admission schedules across different pages. "
        "Please check the official Placement and Admissions sections "
        "for detailed internship and batch information."
    )
