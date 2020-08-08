import requests
from bs4 import BeautifulSoup

URL = f"https://stackoverflow.com/jobs?q=python&sort=i"

def get_last_page():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text,"html.parser")
    pagination = soup.find("div",{"class":"s-pagination"}).find_all("a")
    last_page = pagination[-2].get_text(strip=True)
    return int(last_page)

def extract_jobdetail(html):
    title = html.find("h2",{"class":"mb4"}).find("a")["title"]
    company, location = html.find("h3",{"class":"mb4"}).find_all("span", recursive=False)
    job_id = html['data-jobid']
    company = company.get_text(strip=True)
    location = location.get_text(strip=True)
    return {'title':title, 'company':company, 'location':location, 'link':f"https://stackoverflow.com/jobs/{job_id}"}

def extract_jobs(last_page):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping Stackoverflow : {page}")
        result = requests.get(f"{URL}&pg={page+1}")
        soup = BeautifulSoup(result.text,"html.parser")
        results = soup.find_all("div",{"class":"-job"})
        for result in results:            
            job = extract_jobdetail(result)            
            jobs.append(job)
    return jobs

def get_jobs():
    last_page = get_last_page()
    jobs = extract_jobs(last_page)
    return jobs
