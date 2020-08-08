import requests
from bs4 import BeautifulSoup

JOBVIEW_LIMIT = 50;
INDEED_URL = f"https://kr.indeed.com/취업?q=python&limit={JOBVIEW_LIMIT}"

def get_last_page():
    result = requests.get(INDEED_URL)
    soup = BeautifulSoup(result.text, "html.parser")
    pagination = soup.find("div",{"class":"pagination"})
    links = pagination.find_all('a')
    pages = []
    for page in links[:-1]:
        pages.append(int(page.string))

    max_page=pages[-1]
    return max_page

def extract_job(html):
    title = html.find("h2",{"class":"title"}).find("a")["title"]        
    company = html.find("span",{"class":"company"})
    company_anchor = company.find("a")
    
    if company_anchor is not None:
        company = company_anchor.string
    else:
        company = company.string
    location = html.find("div",{"class":"recJobLoc"})["data-rc-loc"]    
    job_id = html["data-jk"]

    return {'title': title, 'company': company, 'location': location,
    'link': f"https://kr.indeed.com/채용보기?jk={job_id}"}

def get_jobs_detail(last_pages):
    jobs = []
    for page in range(last_pages):        
        print(f"Scrapping {page}")
        result = requests.get(f"{INDEED_URL}&start={page*JOBVIEW_LIMIT}")        
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div",{"class": "jobsearch-SerpJobCard"})    
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs

def get_jobs():
    last_pages = get_last_page()
    jobs = get_jobs_detail(last_pages)
    return jobs
