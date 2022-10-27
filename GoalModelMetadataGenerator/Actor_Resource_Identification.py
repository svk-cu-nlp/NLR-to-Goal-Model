# Requirements filtering by Actor
import spacy
import fasttext
import re
import numpy as np
spacy_nlp = spacy.load('en_core_web_sm')
spacy_stopwords = spacy.lang.en.stop_words.STOP_WORDS
from nltk.corpus import state_union
from nltk.tokenize import sent_tokenize
from nltk.tokenize import PunktSentenceTokenizer
train_text= state_union.raw("2005-GWBush.txt")
model = fasttext.load_model("F:/PURE.bin")
custom_sent_tokenizer= PunktSentenceTokenizer(train_text)
verb_list = []
documents = []
document = []

def cosine(u, v):
    return np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))

def createDataFromPURE():
    requirements = open("Data/nlr.txt", "r")
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
    doc = spacy_nlp(file_content)
    count_token = 0
    verb_count = 0
    word_pair = []
    verb_list = []
    actor = ""
    goal = ""
    resources = []
    for token in doc:
        tag = token.tag_
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
    document = [actor, goal, resources]
    documents.append(document)

def reqFilterByActor():
    actorList = []
    for document in documents:
        actor = document[0]
        if actor not in actorList:
            actorList.append(actor)

    filtered_reqs_by_actor = []
    print("Unique actor..")
    for actor in actorList:
        print(actor)
        filtered_reqs = []
        for document in documents:
            if actor == document[0]:
                filtered_reqs.append(document)

        filtered_reqs_by_actor.append(filtered_reqs)

    # filtered_reqs_by_actor takes filtered_reqs which in turn takes document.
    # document contains [actor, goal, [resources]]
    for filtered_reqs in filtered_reqs_by_actor:
        for document in filtered_reqs:
            actor = document[0]
            goal = document[1]
            res = document[2]
            print("Actor: " + actor + " Goal: " + goal)
            print(res)

    return filtered_reqs_by_actor

def display():
    for document in documents:
        actor = document[0]
        goal = document[1]
        res = document[2]
        print(document)
        #print("Actor: "+actor+" Goal: "+goal)
        #print(res)
        print("===================================")

def createSuperSetofGoals(filtered_reqs):

    super_set_reqs_list = []
    i = 0
    while i<len(filtered_reqs):
        super_set_reqs = []
        j = i + 1
        #print(filtered_reqs[i])
        goal = filtered_reqs[i][1]
        u = model.get_word_vector(goal)
        super_set_reqs.append(filtered_reqs[i])
        #print("Comparing with")
        while j<len(filtered_reqs):
            #print(filtered_reqs[j])
            to_be_removed = filtered_reqs[j]
            goal1 = to_be_removed[1]
            v = model.get_word_vector(goal1)
            sim = cosine(u,v)
            #print(sim)
            if sim > 0.5:
                #print(goal+" and "+goal1+" is similar with confidence "+str(sim))
                super_set_reqs.append(to_be_removed)
                filtered_reqs.remove(to_be_removed)
            j = j + 1
        super_set_reqs_list.append(super_set_reqs)
        i = i + 1
    for super_set_reqs in super_set_reqs_list:
        print("No. of Records: "+str(len(super_set_reqs)))
        print("=========================")
        for req in super_set_reqs:
            print(req)


    return super_set_reqs_list

def find_Highest_Freq(arr):
    fr = [None] * len(arr);
    visited = -1;

    for i in range(0, len(arr)):
        count = 1;
        for j in range(i + 1, len(arr)):
            if (arr[i] == arr[j]):
                count = count + 1;
                # To avoid counting same element again
                fr[j] = visited;

        if (fr[i] != visited):
            fr[i] = count;

    location = fr.index(max(fr))
    #print(arr[location])
    return arr[location]

def findParent(super_set_reqs):
    print(super_set_reqs)
    resource_goal = []
    goalList = []
    print("........Sub goals with respective resources........")
    for reqs in super_set_reqs:
        goal = reqs[1]
        goalList.append(goal)
        resources = reqs[2]
        # validate resource here using previous module
        for r in resources:
            statement = goal+" "+r
            print(statement)
            resource_goal.append(statement)
    # find the parent among goals in goalList
    parent = find_Highest_Freq(goalList)
    print("Parent Goal: "+parent)


def main():
    createDataFromPURE()
    #display()
    filtered_reqs_by_actor = reqFilterByActor()
    Super_Set_ReqList_List = []
    for filtered_reqs in filtered_reqs_by_actor:
        super_set_req_list = createSuperSetofGoals(filtered_reqs)
        Super_Set_ReqList_List.append(super_set_req_list)
        print("=================================!!!!!!!!!============")


    for super_set_req_list in Super_Set_ReqList_List:
        for super_set_reqs in super_set_req_list:
            print("Grouping the requirements............. ")
            findParent(super_set_reqs)


    #f.close()

if __name__ == '__main__':
    main()