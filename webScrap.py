import requests
from bs4 import BeautifulSoup
from bltk.langtools import Tokenizer
#Change the elements according to your need
ambiguous_word = ["মুখ", "মাথা", "চোখ", "হাত"]

while True:
    url = input("Enter the url(Press # to terminate the code):")
    if url == '#':
        break
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    all_p = soup.findAll('p')
    text_of_p = []
    for p in all_p:
        text_of_p.append(p.getText())

    text = ''
    for t in text_of_p:
        text += ' ' + t
    tokenizer = Tokenizer()
    sentences = tokenizer.sentence_tokenizer(text)
    #print(sentences)
    found_sentence = []
    for s in sentences:
        for a in ambiguous_word:
            if a in s:
                found_sentence.append(s)
                print(s)
    if not found_sentence:
        print("No data found")
    else:
        print("New data found")