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
        return getSynonmyms(response.text.replace(word,""))

def getSynonmyms(str):
    str = str.split('[')[1]
    str = str.replace(' "], "antonyms":',"")
    str = str.split('", "')
    ser = pd.Series(str)
    ser.loc[0] = ser.loc[0].replace('"','')
    ser.loc[ser.shape[0]-1] = ser.loc[ser.shape[0]-1].replace('"], "antonyms":','').replace(" ","")
    return ser.to_list()

def oneRound(startWord,options):
    #select and prints out options
    tempResponse = getWordList(startWord)
    topWords = tempResponse[:options]
    for i in range(options):
        print(i+1,topWords[i])

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
    return selectedWord

#pathfind randomly chooses one of the options and returns the choosen word
#does not allow duplicates points on path
def pathfind(word,options):
    global turns
    path = []
    response = getWordList(word)
    topWords = response[:options]
    for j in range(turns):
        word = np.random.choice(topWords)
        while(word in path):
            try:
                topWords.remove(word)
            except:
                print("Error RAN OUT OF OPTIONS")
            word = np.random.choice(topWords)
        path.append(word)
        response = getWordList(word)
    return word

#a game where the player repeatedly pick words from synonmyms to reach a target word

#initalize game
#starting word
word = "kind" #input("Choose Start Word: ")
numOptions = 5
targetWord = word

#creates a path for user to get to
turns = int(input("Choose number of turns you would like to play:"))
targetWord = pathfind(targetWord,numOptions)

#game
#repeat until word becomes target word
print("Your Target is:", targetWord)
while(turns!=0):
    word = oneRound(word,numOptions)
    turns = turns-1
    if(word == targetWord):
        print("You Win! :)")
        exit()
print("You Lose")


