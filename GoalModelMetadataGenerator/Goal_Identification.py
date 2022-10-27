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
    document = [actor, goal, resources, isor, usingToken, resources_after_using, before_of_the, after_of_the, file_content]
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
    solutionsWithEither = []
    isEither = 0
    for filtered_reqs in filtered_reqs_by_actor:
        for document in filtered_reqs:
            actor = document[0]
            goal = document[1]
            res = document[2]
            #statement = document[8]
            # if "either"
            # if isEither == 0:
            #     solutionsWithEither.append(document)

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
        isUsing = reqs[4]
        ofArray = reqs[6]
        if "of" in ofArray:
            afterofarray = reqs[7]
            count = 0
            strmsg = ""

            # strmsg = strmsg+" "+ofArray[0]
            #
            # for b in afterofarray:
            #     strmsg+= " "+b
            for a in afterofarray:
                if(count == 0):
                    strmsg = strmsg + a + " of "
                else:
                    strmsg = strmsg + " " + a
                count = count +1

            print("modified sub goal resource "+strmsg)
        if isUsing == "true":
            resources_after_using = reqs[5]
            print("resources using ..........")
            print(resources_after_using)
            # parsing resources after keyword "using"
        for r in resources:
            statement = goal+" "+r
            print(statement)
            resource_goal.append(statement)
        isor = reqs[3]
        if isor == "true":
            print("decomposition type: OR")
        else:
            print("decomposition type: AND")


    # find the parent among goals in goalList
    # parse csv of parent goal dataset and find the parent
    par = find_Highest_Freq(goalList)
    parent = findParentFromDataset(par)
    print("parent is "+par+" "+parent)
    # for goal in goalList:
    #     parent = findParentFromDataset(goal)
    #     print("Parent Goal: "+parent)

def findParentFromDataset(goal):
    # read csv and make a list of words group by type_no

    # for goal in goalList:
    type_wise_matched = []
    with open('Data/Parent_Goal_Dataset.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        highest_sim = 0
        ops = ""
        for row in csv_reader:
            if line_count == 0:
                #print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                u = model.get_word_vector(goal)
                v = model.get_word_vector(row[1])
                sim = cosine(u, v)
                #print(row[1]+str(sim))
                if sim > 0.45:
                    if sim > highest_sim:
                        highest_sim = sim
                        ops = row[3]
                    #print(goal+ " "+ str(highest_sim)+ " "+ ops)
                    type_wise_matched.append(row[3])
                # print("COmparing "+goal+" with")
                # print(f'\t{row[0]} {row[1]} {row[3]}.')

                line_count += 1
    return ops


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
    #findParentFromDataset('preview')
    main()