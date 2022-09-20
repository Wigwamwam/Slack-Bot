import urllib
from urllib.parse import urlencode
import requests
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
import os

def find_jobs_from(website, job_title, location, desired_characs, filename="results.xls"):
    """
    This function extracts all the desired characteristics of all new job postings
    of the title and location specified and returns them in single file.
    The arguments it takes are:
        - Website: to specify which website to search (options: 'Indeed' or 'CWjobs')
        - Job_title
        - Location
        - Desired_characs: this is a list of the job characteristics of interest,
            from titles, companies, links and date_listed.
        - Filename: to specify the filename and format of the output.
            Default is .xls file called 'results.xls'
    """
    job_soup = load_indeed_jobs_div(job_title, location)
    jobs_list, num_listings = extract_job_information_indeed(job_soup, desired_characs)

    save_jobs_to_excel(jobs_list, filename)

    print('{} new job postings retrieved from {}. Stored in {}.'.format(num_listings,
                                                                        website, filename))

def save_jobs_to_excel(jobs_list, filename):
    jobs = pd.DataFrame(jobs_list)
    jobs.to_excel(filename)


def load_indeed_jobs_div(job_title, location):
    getVars = { 'q' : job_title, 'l' : location, 'fromage' : '7', 'sort' : 'date' }
    url = ('https://uk.indeed.com/jobs?' + urllib.parse.urlencode(getVars))
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    job_soup = soup.find(id="resultsCol")
    return job_soup

def extract_job_information_indeed(job_soup, desired_characs):
    job_elems = job_soup.find_all('div', class_='job_seen_beacon')

    cols = []
    extracted_info = []

    if 'jobTitles' in desired_characs:
        jobTitles = []
        cols.append('jobTitles')
        for job_elem in job_elems:
            jobTitles.append(extract_job_title_indeed(job_elem))
        extracted_info.append(jobTitles)

    if 'companyNames' in desired_characs:
        companyNames = []
        cols.append('companyNames')
        for job_elem in job_elems:
            companyNames.append(extract_company_indeed(job_elem))
        extracted_info.append(companyNames)

    if 'links' in desired_characs:
        links = []
        cols.append('links')
        for job_elem in job_elems:
            links.append(extract_link_indeed(job_elem))
        extracted_info.append(links)

    if 'dates' in desired_characs:
        dates = []
        cols.append('date_listed')
        for job_elem in job_elems:
            dates.append(extract_date_indeed(job_elem))
        extracted_info.append(dates)

    jobs_list = {}

    for j in range(len(cols)):
        jobs_list[cols[j]] = extracted_info[j]

    num_listings = len(extracted_info[0])

    return jobs_list, num_listings


def extract_job_title_indeed(job_elem):
    title_elem = job_elem.find('h2', class_='jobTitle')
    title = title_elem.text.strip()
    return title

def extract_company_indeed(job_elem):
    company_elem = job_elem.find('span', class_='companyName')
    company = company_elem.text.strip()
    return company

def extract_link_indeed(job_elem):
    link = job_elem.find('a')['href']
    link = 'www.indeed.co.uk/' + link
    return link

def extract_date_indeed(job_elem):
    date_elem = job_elem.find('span', class_='date')
    date = date_elem.text.strip()
    return date
