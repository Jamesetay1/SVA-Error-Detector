import stanza
#stanza.download('en')
nlp = stanza.Pipeline('en', processors = "tokenize, pos, lemma, depparse", batch_size = "100")

with open('tests.txt', 'r') as file:
    data = file.read()
doc = nlp(data)

nsubj_Agreement_dict = {
                "VB": [],
                "VBD": ["NN", "NNS", "NNP", "NNPS", "PRP_1", "PRP_2", "DT_1", "DT_2"],
                "VBG": [],
                "VBN": ["NN", "NNS", "NNP", "NNPS", "PRP_1", "PRP_2", "DT_1", "DT_2"],
                "VBZ": ["NN", "NNP", "PRP_2", "DT_1"],
                "VBP": ["NNS", "NNPS", "PRP_1", "DT_2"],
}

grouping_dict = {
                "PRP_1": ["i", "you", "they", "we", "theirs"],
                "PRP_2": ["he", "she", "it", "his", "hers"],
                "DT_1": ["this", "that"],
                "DT_2": ["these", "those"],
}

adj_list = ["JJ", "JJR", "JJS"]


correct_list = []
incorrect_list = []

def add_to_list(error, dep, gov, sent):
    if error:
        incorrect_list.append(f'{dep.text} ({dep.xpos}) <--{dep.deprel}-- {gov.text} ({gov.xpos}) in "{sent.text}"')
    else:
        correct_list.append(f'{dep.text} ({dep.xpos}) <--{dep.deprel}-- {gov.text} ({gov.xpos}) in "{sent.text}"')
    return True;


def detect_error(dep, gov):
    if dep.xpos == "MD" or gov.xpos == "MD": return False;
    if dep.xpos in nsubj_Agreement_dict[gov.xpos]:
        return False;

    for key in grouping_dict:
        if dep.text.lower() in grouping_dict[key] and key in nsubj_Agreement_dict[gov.xpos]:
            return False;

    return True;


# Will return the id of the where the dependency was found where 'word' is the governor,
# or 0 if none at all
def find_forward_dep(word, dep, forward_dep_list):
    forward_list = forward_dep_list[word.id-1]
    for i in range(len(forward_list)):
        if forward_list[i].deprel == dep:
            return forward_list[i].id
    return 0


for sent in doc.sentences:
    # We will construct a fowards dependency list
    forward_dep_list = [[] for n in range(len(sent.words))]


    # First lets make our backwards and forwards dependency lists
    for word in sent.words:
        dep = word;  gov = sent.words[dep.head - 1]

        if dep.deprel != "root":
            forward_dep_list[dep.head-1].append(dep)
            #backwards_dep_list[dep.id-1].append(gov)

    # Now that we have forwards and backwards we can search for special cases to mark as errors or not
    for word in sent.words:

        nsubj_forward_dep_id = find_forward_dep(word, "nsubj", forward_dep_list)
        aux_forward_dep_id = find_forward_dep(word, "aux", forward_dep_list)
        cop_forward_dep_id = find_forward_dep(word, "cop", forward_dep_list)

        # If the word is a verb, AND it has a nsubj forward depedency AND it does NOT have any aux forward dependency
        if word.xpos in nsubj_Agreement_dict and nsubj_forward_dep_id != 0 and aux_forward_dep_id == 0:
            dep = sent.words[nsubj_forward_dep_id-1]
            gov = word
            error = detect_error(dep, word)
            add_to_list(error, dep, word, sent)

        # If the word is a verb, AND it has a nsubj forward depedency AND it DOES have any aux forward dependency
        if word.xpos in nsubj_Agreement_dict and nsubj_forward_dep_id != 0 and aux_forward_dep_id != 0:
            dep = sent.words[nsubj_forward_dep_id - 1]
            gov = sent.words[aux_forward_dep_id - 1]
            error = detect_error(dep, gov)
            add_to_list(error, dep, gov, sent)

        # If the word has a copular forward depedency AND an nsubj forward dependency
        # Will work if the subject predicate is an adjective, NP, Pronoun etc.
        # ex: (He is [happy, a dog, it, that])
        if cop_forward_dep_id != 0 and nsubj_forward_dep_id != 0:
            dep = sent.words[nsubj_forward_dep_id - 1]
            gov = sent.words[cop_forward_dep_id - 1] if aux_forward_dep_id == 0 else sent.words[aux_forward_dep_id - 1]
            error = detect_error(dep, gov)
            add_to_list(error, dep, gov, sent)



#Now we can print out some stats
total_num = len(correct_list) + len(incorrect_list)
correct_percent = len(correct_list)/total_num * 100
incorrect_percent = len(incorrect_list)/total_num * 100
print("\nGeneral Statistics:")
print("# of nsubj dependencies considered: " + str(total_num))
print("# and percent of correct uses: " + str(len(correct_list)) + ", " + str(correct_percent))
print("# and percent of correct uses: " + str(len(incorrect_list)) + ", " + str(incorrect_percent))

print("\nThe following nsubj dependencies were found to be incorrect:")
print(*incorrect_list,sep='\n')

print("\nThe following nsubj dependencies were found to be correct:")
print(*correct_list,sep='\n')

#print("\nThe following compound nouns were found and are likely subject verb agreement errors:")
#print(*compounds,sep='\n')