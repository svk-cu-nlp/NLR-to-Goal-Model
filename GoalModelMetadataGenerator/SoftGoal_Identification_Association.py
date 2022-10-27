# Requirements filtering by Actor
import spacy
import csv
import fasttext
import re
import nltk
import numpy as np
spacy_nlp = spacy.load('en_core_web_sm')
spacy_stopwords = spacy.lang.en.stop_words.STOP_WORDS
from nltk.corpus import state_union
from nltk.tokenize import sent_tokenize
from nltk.tokenize import PunktSentenceTokenizer
train_text= state_union.raw("2005-GWBush.txt")
model = fasttext.load_model("F:/PURE.bin")
# from sentence_transformers import SentenceTransformer, util
# Fibermodel = SentenceTransformer('bert-large-nli-stsb-mean-tokens')
custom_sent_tokenizer= PunktSentenceTokenizer(train_text)
verb_list = []
documents = []
document = []
docSimList = []

def cosine(u, v):
    return np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))

def createDataFromPURE():
    requirements = open("Data/nfrs.txt", "r")
    Lines = requirements.readlines()
    for line in Lines:
        # remove suporting verbs
        #line = removeSupportingVerbs(line)
        POSTaggingUsingSpacy(line)


def removeSupportingVerbs(line):
    supporting_verbs = open("Data/supportive_verbs.txt", "r")
    status = 0
    Lines = supporting_verbs.readlines()
    for l in Lines:
        l = l.lstrip()
        l = l.rstrip()
        if l in line:
            #print("removing "+l)
            status = 1
            #patt = re.compile(l)
            #line = patt.sub('', line)
            #print(line)
    return status


def POSTaggingUsingSpacy(file_content, verb_list = []):
    #print("===========================================")
    #print(file_content)
    isor = ""
    usingToken = ""
    # send file_content to document
    nltk_tokens = nltk.word_tokenize(file_content)

    if "either" in nltk_tokens or "or" in nltk_tokens:
        isor = "true"

    if "using" in nltk_tokens or "through" in nltk_tokens:
        usingToken = "true"
    doc = spacy_nlp(file_content)

    count_token = 0
    verb_count = 0
    word_pair = []
    verb_list = []
    actor = ""
    goal = ""
    gotUsing = 0
    resources = []
    resources_after_using = []
    before_of_the = []
    after_of_the = []
    gotOf = 0
    prev_token = ""
    for token in doc:
        tag = token.tag_
        if token.text == "using":
            gotUsing = 1
        if token.text != "of":   #The system Admin shall show price of the selected products
            if gotOf == 0:
                before_of_the = []
        else:
            gotOf = 1
            before_of_the.append("of")
        #print(token.text, token.tag_, token.is_stop)
        if "NN" in tag:
            word_pair.append(token.text)

        else:
            if "VB" in tag:
                # if verb_count == 0:
                #print("Goal: "+token.text)
                    # check whether the verb is supporting or not. If supporting, make verb_count negative
                status = removeSupportingVerbs(token.text)
                if status == 0:
                    #print("Goal: " + token.text)
                    verb_list.append(token.text)
                    verb_count = verb_count + 1

            else:
                joint_words = ""
                for word in word_pair:
                    joint_words = joint_words+" "+word
                if word_pair:
                    joint_words = joint_words.lstrip()
                    joint_words = joint_words.rstrip()
                    #f.write(str(line)+" "+joint_words + "\n")
                    if(count_token == 0):
                        #print("Actor: "+joint_words)
                        actor = joint_words

                    if (count_token > 0):
                        #print("Resource: "+joint_words)
                        # here we have to check for validity of the resource
                        resources.append(joint_words)
                        if gotOf == 0:
                            before_of_the.append(joint_words)
                        if gotOf == 1:
                            after_of_the.append(joint_words)
                        if gotUsing == 1:
                            resources_after_using.append(joint_words)
                    count_token = count_token + 1
                word_pair = []

    count_token = 0
    if verb_list:
        array_length = len(verb_list)
        #print(verb_list)
        #print("Goal: "+verb_list[0])
        goal = verb_list[0]

    #print("Actor: "+actor+" Goal: "+goal)
    #print(resources)
    document = [actor, verb_list, resources, isor, usingToken, resources_after_using, before_of_the, after_of_the, file_content]
    documents.append(document)



def display():
    for document in documents:
        actor = document[0]
        goal = document[1]
        res = document[2]
        print(document)
        #print("Actor: "+actor+" Goal: "+goal)
        #print(res)
        print("===================================")

def findAssociation():
    requirements = open("Data/nlr.txt", "r")
    Lines = requirements.readlines()
    for document in documents:
        matchFound = 0
        token1 = document[0]
        token2 = document[1]
        tokenArray = document[2]
        tokenArray.append(token1)
        # merge these token and then check with merged tokens(only goal and resources) of each line of nlrs
        tokenArray = tokenArray + token2
        print(document)
        print(tokenArray)
        maxSim = 0
        nfr = ""
        nlr = ""
        for line in Lines:
            print(line)
            docSim = []
            # Extract info for each line and compare
            info = extractInfo(line)
            act = info[0]
            gl = info[1]
            resArray = info[2]
            resArray.append(gl)
            print(resArray)

            for res in resArray:
                for token in tokenArray:
                    u = model.get_word_vector(res)
                    v = model.get_word_vector(token)
                    #emb1 = Fibermodel.encode(res, convert_to_tensor=True)
                    #emb2 = Fibermodel.encode(token, convert_to_tensor=True)
                    sim = cosine(u, v)
                    #sim = util.pytorch_cos_sim(emb1, emb2)
                    #print(res +" "+token+" sim: "+str(sim))
                    if sim > maxSim:
                        maxSim = sim
                        nfr = document[8]
                        nlr = line

            print("........................................")


        print("===================================")
        nfrassociation = [maxSim, nfr, nlr]
        docSimList.append(nfrassociation)
        print("Final : "+str(maxSim)+" "+nfr+" "+nlr)

def extractInfo(file_content, verb_list = []):
    doc = []
    #print("===========================================")
    #print(file_content)
    isor = ""
    usingToken = ""
    # send file_content to document
    nltk_tokens = nltk.word_tokenize(file_content)

    if "either" in nltk_tokens or "or" in nltk_tokens:
        isor = "true"

    if "using" in nltk_tokens or "through" in nltk_tokens:
        usingToken = "true"
    doc = spacy_nlp(file_content)
    count_token = 0
    verb_count = 0
    word_pair = []
    verb_list = []
    actor = ""
    goal = ""
    gotUsing = 0
    resources = []
    resources_after_using = []
    before_of_the = []
    after_of_the = []
    gotOf = 0
    prev_token = ""
    for token in doc:
        tag = token.tag_
        if token.text == "using":
            gotUsing = 1
        if token.text != "of":   #The system Admin shall show price of the selected products
            if gotOf == 0:
                before_of_the = []
        else:
            gotOf = 1
            before_of_the.append("of")
        #print(token.text, token.tag_, token.is_stop)
        if "NN" in tag:
            word_pair.append(token.text)

        else:
            if "VB" in tag:
                if verb_count == 0:
                    #print("Goal: "+token.text)
                    # check whether the verb is supporting or not. If supporting, make verb_count negative
                    status = removeSupportingVerbs(token.text)
                    if status == 0:
                        verb_list.append(token.text)
                        verb_count = verb_count + 1

            else:
                joint_words = ""
                for word in word_pair:
                    joint_words = joint_words+" "+word
                if word_pair:
                    joint_words = joint_words.lstrip()
                    joint_words = joint_words.rstrip()
                    #f.write(str(line)+" "+joint_words + "\n")
                    if(count_token == 0):
                        #print("Actor: "+joint_words)
                        actor = joint_words

                    if (count_token > 0):
                        #print("Resource: "+joint_words)
                        # here we have to check for validity of the resource
                        resources.append(joint_words)
                        if gotOf == 0:
                            before_of_the.append(joint_words)
                        if gotOf == 1:
                            after_of_the.append(joint_words)
                        if gotUsing == 1:
                            resources_after_using.append(joint_words)
                    count_token = count_token + 1
                word_pair = []

    count_token = 0
    if verb_list:
        array_length = len(verb_list)
        #print(verb_list)
        #print("Goal: "+verb_list[0])
        goal = verb_list[0]

    #print("Actor: "+actor+" Goal: "+goal)
    #print(resources)
    doc = [actor, goal, resources, isor, usingToken, resources_after_using, before_of_the, after_of_the, file_content]
    return doc

def getAssociation():
    for nfrassociation in docSimList:
        simScore = nfrassociation[0]
        nfr = nfrassociation[1]
        nlr = nfrassociation[2]
        # search csv to get nfr category of the particular nfr statement
        doc = extractInfo(nlr)
        # print doc and
def main():
    createDataFromPURE()
    #display()
    findAssociation()
    # doc = extractInfo("The system shall produce search results in an acceptable time")
    # print(doc)

if __name__ == '__main__':
    #findParentFromDataset('preview')
    main()