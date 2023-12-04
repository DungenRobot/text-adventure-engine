import re
import string
import itertools

verbs = {
    "push"  : ["push"],
    "pull"  : ["pull", "drag", "haul", "yank"],
    "take"  : ["take", "get", "steal", "grab", "nab", "collect", "pick up", "acquire"],
    "use"   : ["use", "open"],
    "look"  : ["look", "see", "view", "peek", "stare", "peer"],
    "go"    : ["go", "travel", "move"],
    "close" : ["close", "shut"]
}

all_verbs = []

for v in verbs:
    all_verbs += verbs[v]

def parse(sentence: str, scene_nouns: list = ["shed", "hairpin", "unknown", "cellar"]) -> (str, str):

    #take the input sentence and reduce to to lowercase without punctuation
    sentence = sentence.strip().lower() 
    sentence = ''.join(ch for ch in sentence if ch not in string.punctuation)

    sentence = sentence.split(' ')

    verbs_in_sentence = []
    potential_nouns = []

    for word in sentence:
        if word in all_verbs:
            verbs_in_sentence.append(word)
        else:
            potential_nouns.append(word)

    if len(verbs) == 0:
        return {"ERROR" : 1, "verb" : verbs_in_sentence[0]}
    if len(verbs) > 1:
        return {"ERROR" : 2, "verb" : verbs_in_sentence}
    
    verb = verbs_in_sentence[0]
    
    for key in verbs:
        if verb in verbs[key]:
            print(verb, key)
            verb = key
    
    objects = []

    for word in sentence:
        if word in scene_nouns:
            objects.append(word)

    print(objects)

    if len(objects) == 0:
        return {'ERROR' : 3, 'verb' : verb}
    
    return {'ERROR' : 0, 'verb' : verb, 'noun' : objects}
    



     



parse("go to shed!")
parse("steal, a hairpin")
parse("peer into the unknown")