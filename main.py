from parsing import parse
import shelve
import tomllib as toml
import os
import sys

def get_input(s):

    i = input(s)

    if i == "exit":
        sys.exit(0)
    
    return i

def get_story_path():
    #generates a list of folder names in the current directory
    stories = [name.removeprefix("story_") for name in os.listdir("./") if name.startswith("story_") and os.path.isdir("./" + name)]

    if len(stories) == 0:
        return "ERROR: Can't find any stories in this directory.\nPlease ensure that all "
    if len(stories) == 1:
        #only one story so we don't need to prompt the user
        return stories[0]

    while True:
        print("Please select a story")
        for id, story_name in enumerate(stories): 
            print("%s) %s" % (id, story_name))

        selected = get_input("> ")
        if selected.isnumeric() and int(selected) < len(stories):
            return stories[int(selected)]
        
        print("Something went wrong. Pease make sure you enter a number between 0 and %s (inclusive)" % (len(stories) - 1))


def generate_story(path) -> dict:
    with open("./story_%s/%s.toml" % (path, path), "rb") as f:
        storydata = toml.load(f)

    return storydata


def main():

    path = get_story_path()

    if path.startswith("ERROR:"):
        print(path)
        return

    storydata = generate_story(path)


    with shelve.open("story_%s/savedata" % path) as data:

        if data.get("inventory") == None:
            data["inventory"] = ["Knife"]
        
        print(data['inventory'], storydata)


        while True:
            input_str = get_input("> ")


            if input_str.lower() == "help":
                print_help()
                continue
            if "inventory" in input_str:
                print_inventory(data["inventory"])
                continue

            result = parse(input_str)

            match result["ERROR"]:
                case 1:
                    print("I'm not sure what action you're trying to take")
                    continue
                case 2:
                    print("You can only take one action at a time")
                    continue
                case 3:
                    print("I'm not sure what object(s) you're trying to [%s]" % result.get("verb"))
                    pass
                case 0:


                    print(result.get("verb"), result.get("noun")[0])



def print_help():
    print("You can use the verbs to interact with the world: ")
    print(" 'push', 'pull', 'take', 'use', 'look', 'go to', 'open', 'close' ")

def print_inventory(inv):
    for item in inv:
        print(item)



if __name__ == "__main__":
    main()