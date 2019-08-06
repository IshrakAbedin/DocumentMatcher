from nltk.tokenize import word_tokenize as tokenize
from nltk.corpus import stopwords
import textract
from string import digits
import copy

def getTF(path):
    stops = stopwords.words('english')
    punctuations = ['(',')',';',':','[',']',',', '.', '!', '\"', '#', '$', '%', '&', '\'', '*', '+', '-', '/', '<', '=', '>', '?', '@', '\\', '^', '_', '`', '{', '|', '}', '~']
    remove_digits = str.maketrans('', '', digits)
    dic = {}
    tf = {}
    wordz = set()
    tokens = []
    try:
        text = textract.process(path).decode().translate(remove_digits)
    except Exception as identifier:
        print('--Err: FAILED TO PARSE ' + path + ' in normal mode, trying OCR')
        try:
            text = textract.process(path, method = 'tesseract').decode().translate(remove_digits)
        except Exception as identifier:
            print('--Err: FAILED TO PARSE ' + path + ' even in OCR mode, skipping')
            return dict(), 1
        #return set({}), {}

    tempTokens = tokenize(text)

    if len(tempTokens) == 0:
        print('--Err: FAILED TO PARSE ' + path + ' in normal mode, trying OCR')
        try:
            text = textract.process(path, method = 'tesseract').decode().translate(remove_digits)
        except Exception as identifier:
            print('--Err: FAILED TO PARSE ' + path + ' even in OCR mode, skipping')
            return dict(), 1

    for word in tempTokens:
        if word.lower() not in stops and word.lower() not in punctuations and len(word) > 1:
            tokens.append(word)

    for word in tokens:
        if dic.__contains__(word):
            dic[word] = dic[word] + 1
        else:
            dic[word] = 1

    counter1 = 0
    for key, value in sorted(dic.items(), key=lambda item: item[1], reverse = True):
        if counter1 >= 200:
            break
        tf[key] = value
        #wordz.add(key)
        counter1 += 1
    return tf, 0

def getDF(filesTF):
    df = copy.deepcopy(filesTF)
    for file in df:
        for word in df[file]:
            #print(file, word, df[file][word])
            df[file][word] = 0

    for file in df:
        for word in df[file]:
            for comparison in filesTF:
                if filesTF[comparison].__contains__(word):
                    df[file][word] = (df[file])[word] + 1

    return df

def getNword(tfidf, n):
    wordz = set()
    counter1 = 0
    for key, value in sorted(tfidf.items(), key=lambda item: item[1], reverse = True):
        if counter1 >=n:
            break
        wordz.add(key)
        counter1 += 1
    
    return wordz