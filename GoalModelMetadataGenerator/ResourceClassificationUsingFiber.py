import pandas as pd
from sentence_transformers import SentenceTransformer, util
Fibermodel = SentenceTransformer('bert-large-nli-stsb-mean-tokens')
df = pd.read_excel('F:/SoftwareResource.xlsx')
#print(df)
wordlistFile = open("words.txt", "r")
Lines = wordlistFile.readlines()
for line in Lines:
    print("For "+line)
    print("----------------")
    sentences1 = []
    sentences1.append(line)
    embeddings1 = Fibermodel.encode(sentences1, convert_to_tensor=True)
    for ind in df.index:
         w2 = df['Words'][ind]
         sentences2 = []
         cumulative_score = 0
         status = 0
         sentences2.append(w2)
         embeddings2 = Fibermodel.encode(sentences2, convert_to_tensor=True)
         cosine_scores = util.pytorch_cos_sim(embeddings1, embeddings2)
         cumulative_score = cumulative_score + cosine_scores
         #print(w2+" "+str(cosine_scores))
         if (cosine_scores > 0.6):
             print(line +"is Software resource with confidence "+str(cosine_scores))
             status = 1
             break

    if (status == 0):
        avg_score = cumulative_score / 1167
        if (avg_score > 0.3):
            print(line + " is software resource")
        else:
            print("average score is "+str(avg_score))
