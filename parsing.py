from __future__ import annotations
import re
import string
import itertools

verbs = {
    "push"  : ["push"],
    "pull"  : ["pull", "drag", "haul", "yank"],
    "take"  : ["take", "get", "steal", "grab", "nab", "collect", "pick up", "acquire"],
    "use"   : ["use", "open", "combine"],
    "look"  : ["look", "see", "view", "peek", "stare", "peer", "investigate"],
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
    
    if len(verbs_in_sentence) == 0:
        return {"ERROR" : 1, "verb" : verbs_in_sentence[0]}
    if len(verbs_in_sentence) > 1:
        return {"ERROR" : 2, "verb" : verbs_in_sentence}
    
    verb = verbs_in_sentence[0]
    
    for key in verbs:
        if verb in verbs[key]:
            verb = key
    
    objects = []

    for word in sentence:
        if word in scene_nouns:
            objects.append(word)

    if (len(objects) == 0) and (verb != "look"):
        return {'ERROR' : 3, 'verb' : verb}
    
    return {'ERROR' : 0, 'verb' : verb, 'noun' : objects}
    



class has_items:
    def __init__(self, data: dict[str, any], path: dict[str, any]):

        self.items : list[item] = []

        for key in path:
            if key.startswith("item"):
                self.items.append( item(data, key) )

    def list_items(self) -> list:
        out = []
        for i in self.items:
            out += i.alias
        return out
    
    def get_item(self, item_name: str) -> item:
        for i in self.items:
            if item_name in i.alias:
                return i
        return None



class item(has_items):
    def __init__(self, data: dict, key: str):
        i: dict = data[key]
        
        self.alias = i["alias"]
        self.desc = i["name"]
        self.can_be_picked_up = i.get("can_be_picked_up", True)

        super().__init__(data, i)


class room(has_items):
    def __init__(self, data: dict, key: str):
        r: dict = data[key]
        self.name : str = r["name"]
        self.desc : str = r["desc"]
        self.can_go_back : bool = r.get("can_go_back", True)

        self.navi : dict[str, str] = {}

        for key in r:
            if key.startswith("navi_"):
                self.navi[key[5:]] = r[key]
        
        super().__init__(data, r)



if __name__ == "__main__":
    parse("go to shed!")
    parse("steal, a hairpin")
    parse("peer into the unknown")