import requests
from bs4 import BeautifulSoup

def get_last_page(url):
    result = requests.get(url)
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

def extract_jobs(last_page, url):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping Stackoverflow : {page}")
        result = requests.get(f"{url}&pg={page+1}")
        soup = BeautifulSoup(result.text,"html.parser")
        results = soup.find_all("div",{"class":"-job"})
        for result in results:            
            job = extract_jobdetail(result)            
            jobs.append(job)
    return jobs

def get_jobs(word):
    url = f"https://stackoverflow.com/jobs?q={word}&sort=i"
    last_page = get_last_page(url)
    jobs = extract_jobs(last_page , url)
    return jobs
