import requests
import numpy as np
import pandas as pd
import key

def getWordList(word):
    api_url = 'https://api.api-ninjas.com/v1/thesaurus?word={}'.format(word)
    #private api key
    response = requests.get(api_url, headers={'X-Api-Key': key.api_key})
    if response.status_code != requests.codes.ok:
        print("Error:", response.status_code, response.text)
    else:
        return getSynonmyms(response.text)

def getSynonmyms(str):
    str = str.split('[')[1].replace(' "], "antonyms":',"").split('", "')
    ser = pd.Series(str)
    ser.loc[0] = ser.loc[0].replace('"','')
    ser.loc[ser.shape[0]-1] = ser.loc[ser.shape[0]-1].replace('"], "antonyms":','').replace(" ","")
    return ser

def oneRound(startWord,startResponse,options):
    #select and prints out options
    topWords = startResponse.head(options)
    for i in range(options):
        print(i+1,topWords.loc[i])

    #check if selected word is an option
    userInput = input("Enter an integer: ")
    while(not userInput.isdigit()):
        print("Error not an integer")
        userInput = input("Enter an integer: ")
    while(int(userInput)>options):
        print("Error not within options")
        userInput = input("Enter an integer: ")        
    
    selectedWord = topWords[int(userInput)-1]
    print('you have chosen: ',selectedWord)
    print("Target word is:",targetWord)
    print()

    #reset starting variables
    return [selectedWord,getWordList(startWord)]

#does not work: intended iterations does not follow through
#pathfinds through options
def pathfind(word,options,numIterations):
    response = getWordList(word)
    print(numIterations)
    for i in range(numIterations):
        topWords = response.head(options)
        randomNum = np.random.randint(options)
        word = topWords.iloc[randomNum]
        response = getWordList(word)
    return word

#a game where the player repeatedly pick words from synonmyms to reach a target word

#initalize game
#starting word
startWord = "kind" #input("Choose Start Word: ")
startResponse = getWordList(startWord)
targetWord = "selfish"
#select top 10 words from list of synonmyms
numOptions = 5

#generates random target word
word = startWord
response = getWordList(word)

#game
#repeat until word becomes target word
temp = oneRound(startWord,startResponse,numOptions)
while(word!=targetWord):
    temp = oneRound(temp[0],temp[1],numOptions)

"""
#creates a path for user to get to
#does not work
iterations = 4
targetWord = [startWord,getWordList(startWord)]
for i in range(iterations):
    targetWord = pathfind(startWord,numOptions,iterations)
print(targetWord)
"""

