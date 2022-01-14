import wikipediaapi
import requests
from bs4 import BeautifulSoup
import webbrowser
import csv


def write(title, summary):
    with open('wiki.csv', 'w', newline='') as f:
        fieldnames = ['Title', 'Summary']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({'Title': title, 'Summary': summary})
        f.close()


w = wikipediaapi.Wikipedia(language='en', extract_format=wikipediaapi.ExtractFormat.WIKI)
while True:
    titles = []
    summaries = []
    for i in range(0, 5):
        a = "https://en.wikipedia.org/wiki/Special:Random"
        u = requests.get(a)
        soup = BeautifulSoup(u.content, 'html.parser')
        title = soup.find(class_="firstHeading").text
        titles.append(title)
        p = w.page(title)
        if p.exists():
            summaries.append(p.summary)
    c = 1
    for title in titles:
        print(c, ". Title:" + title + "\n Summary:" + summaries[c-1])
        c = c + 1
    choice = int(input("\n\nEnter your choice(0 to break):"))
    if choice == 0:
        print("You have terminated the code...")
        break
    else:
        url = 'https://en.wikipedia.org/wiki/%s' % titles[choice - 1]
        webbrowser.open(url)
        write(titles[choice-1], summaries[choice-1])
