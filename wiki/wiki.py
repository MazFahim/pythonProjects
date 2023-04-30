import wikipediaapi
import requests
from bs4 import BeautifulSoup
import webbrowser
import csv


def write(title_, summary):
    with open('wiki.csv', 'w', newline='') as f:
        fieldnames = ['Title', 'Category']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({'Title': title_, 'Summary': summary})
        f.close()


w = wikipediaapi.Wikipedia(language='en', extract_format=wikipediaapi.ExtractFormat.WIKI)
while True:
    titles = []
    categories = []
    for i in range(0, 5):
        a = "https://en.wikipedia.org/wiki/Special:Random"
        u = requests.get(a)
        soup = BeautifulSoup(u.content, 'html.parser')
        title = soup.find(class_="firstHeading").text
        titles.append(title)
        p = w.page(title)
        category = ""
        if p.exists():
            for c in p.categories:
                #print(c.removeprefix('Category:'))
                #category.append(c.removeprefix('Category:'))
                category = category + '|' + c.removeprefix('Category:')
        categories.append(category)
    c = 1
    for title in titles:
        print(f"{c} .Title:{ title }\n Categories:")
        print(categories[c-1])
        c = c + 1

    while True:
        choice = int(input("\n\nEnter your choice(0 to break, 6 to refresh):"))
        if choice == 0:
            print("You have terminated the code...")
            exit()
        elif choice == 6:
            print('Refreshing search result:')
            break
        else:
            #write(titles[choice-1], summaries[choice-1])
            url = 'https://en.wikipedia.org/wiki/%s' % titles[choice - 1]
            webbrowser.open(url)