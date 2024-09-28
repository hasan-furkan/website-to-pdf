import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pdfkit
from tqdm import tqdm 

def get_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def get_sub_links(soup, base_url):
    links = set()
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        full_url = urljoin(base_url, href)
        if full_url.startswith(base_url):  
            links.add(full_url)
    return links

def extract_content(soup):
    content = {}
    content['titles'] = [h.get_text() for h in soup.find_all(['h1', 'h2', 'h3'])]
    content['images'] = [img['src'] for img in soup.find_all('img', src=True)]
    content['code_blocks'] = [pre.get_text() for pre in soup.find_all(['pre', 'code'])]
    return content

def remove_sidebar(soup):
    sidebar = soup.find(id="doc-menu")
    if sidebar:
        sidebar.decompose()

def create_pdf(html_content, output_pdf):
    print("Creating PDF...")
    options = {
        'no-outline': None,
        'disable-external-links': None,
    }
    pdfkit.from_string(html_content, output_pdf, options=options)
    print(f"PDF saved as {output_pdf}")


# Başlangıç URL'si
url = "https://docs.djangoproject.com/en/5.1/"
html_content = get_html(url)

if html_content:
    soup = BeautifulSoup(html_content, 'lxml')
    all_pages = {url: html_content}
    
    internal_links = get_sub_links(soup, url)
    print(f"Found {len(internal_links)} internal links.")

    for link in tqdm(internal_links, desc="Processing pages"):
        page_html = get_html(link)
        if page_html:
            all_pages[link] = page_html

    site_data = {}
    for page_url, page_html in all_pages.items():
        page_soup = BeautifulSoup(page_html, 'html.parser')
        remove_sidebar(page_soup)
        site_data[page_url] = extract_content(page_soup)

    html_string = ""
    for page_url, content in site_data.items():
        html_string += f"<h1>{page_url}</h1>"
        for title in content['titles']:
            html_string += f"<h2>{title}</h2>"
        for paragraph in content['paragraphs']:
            html_string += f"<p>{paragraph}</p>"
        for image in content['images']:
            full_image_url = urljoin(page_url, image)
            html_string += f"<img src='{full_image_url}' />"
        for code_block in content['code_blocks']:
            html_string += f"<pre><code>{code_block}</code></pre>"

    create_pdf(html_string, "output.pdf")