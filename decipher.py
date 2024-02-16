from nltk.tokenize import sent_tokenize, word_tokenize

#Take passage input and split the sentences
passage = input('Type the text:')
# passage = "Hello. I am Maz Fahim"
sentences = sent_tokenize(passage)

pattern = '*'
stopwords = ['.', ',', '?', '!']
changedSentences = ""
for sentence in sentences:
    words = word_tokenize(sentence)
    changedWords = ""
    for word in words:
        if word in stopwords or word == ' ': 
            continue
        changedLetters = ""
        letters = list(word)
        for letter in letters:
            if pattern == '*':
                changedAsciiValue = ord(letter) - 4
            elif pattern == '#':
                changedAsciiValue = ord(letter) + 4
            elif pattern == '@':
                changedAsciiValue = ord(letter) - 22
            elif pattern == '*':
                changedAsciiValue = ord(letter) - 16
            changedCharacter = chr(changedAsciiValue)
            changedLetters= changedLetters + changedCharacter

        changedWords = changedWords + changedLetters + ' '
        if pattern == '*':
            pattern = '#'
        elif pattern == '#':
            pattern = '@'
        elif pattern == '@':
            pattern = '$'
        if pattern == '$':
            pattern = '*'

    # changedWords = changedWords + '.'
    wordList = list(changedWords)
    wordList[-1] = '.'
    changedWords = ''.join(wordList)
    changedSentences = changedSentences + changedWords + ' '
print(changedSentences)
