from parsing import parse, room, item
import shelve
import tomllib as toml
import os
import sys




def get_input(s) -> str:
    i = input(s)

    if i == "exit":
        sys.exit(0)
    
    return i


def get_story_path() -> str:
    """
    Finds all story folders. If only one is available: automatically load it.
    If multiple are available: prompt the user to choose one.
    Returns a string.
    """


    #generates a list of folder names in the current directory
    stories = [name.removeprefix("story_") for name in os.listdir("./") if name.startswith("story_") and os.path.isdir("./" + name)]

    if len(stories) == 0:
        return "ERROR: Can't find any stories in this directory.\nPlease ensure that all "
    
    #only one story so we don't need to prompt the user
    if len(stories) == 1:
        return stories[0]
    
    #prompts the user to select a story from the directory
    while True:
        print("Please select a story")
        for id, story_name in enumerate(stories): 
            print("%s) %s" % (id, story_name))

        selected = get_input("> ")
        if selected.isnumeric() and int(selected) < len(stories):
            return stories[int(selected)]
        
        print("Something went wrong. Pease make sure you enter a number between 0 and %s (inclusive)" % (len(stories) - 1))


def generate_story(path) -> dict:
    """
    Takes in a story name and opens its toml file: then generates a series of nested objects for the story.
    """
    storydata = {}
    with open("./story_%s/%s.toml" % (path, path), "rb") as f:
        data = toml.load(f)

        storydata["default"] = data["default"]
        storydata["intro"] = data["intro"]


        for key in data:
            if key.startswith("room_"):
                storydata[key[5:]] = room(data, key)


    return storydata



def main():
    
    path = get_story_path()

    if path.startswith("ERROR:"):
        print(path)
        return

    storydata = generate_story(path)


    with shelve.open("story_%s/savedata" % path) as savedata:

        if savedata.get("inventory") == None:
            savedata["inventory"] = []
        
        room_name = savedata.get("current_room", storydata["default"])
        current_room: room = storydata[room_name]
        last_room_name = ""
        focus = current_room

        if not savedata.get("has_seen_intro", False):
            savedata["has_seen_intro"] = True
            print(storydata["intro"])
        else:
            print(current_room.name)

        while True:

            savedata["current_room"] = room_name

            input_str = get_input("> ")

            if input_str.lower().startswith("help"):
                print_help(input_str)
                continue
            if "inventory" in input_str:
                print_inventory(savedata["inventory"])
                continue
            
            nouns = ["around", "it", "back"] + current_room.list_items() + focus.list_items() + list(current_room.navi.keys())
            print(nouns)
            result : dict = parse(input_str, nouns)
            
            match result["ERROR"]:
                case 1:
                    print("I'm not sure what action you're trying to take")
                    continue
                case 2:
                    print("You can only take one action at a time")
                    continue
                case 3:
                    print("I'm not sure what object(s) you're trying to [%s]" % result.get("verb"))
                    continue
                case _:
                    pass
        

            match result.get("verb"):
                case "take":
                    item_name = result.get("noun")[0]
                    if item_name == "it":
                        i = focus
                        item_name = focus.alias[0]
                    else:
                        i = focus.get_item(item_name)
                    if i == None:
                        print("I can't find the item '%s'" % item_name)
                    elif i.can_be_picked_up:
                        if item_name in savedata["inventory"]:
                            print("You already have this item")
                            continue
                        savedata["inventory"] += [item_name]
                        print('You take the %s' % item_name)
                        focus = i
                    else:
                        print("You can't seem to fit the %s in your pockets" % item_name)

                case "go":
                    destination = result.get("noun")[0]
                    if destination == "back":
                        if last_room_name == "":
                            print("I'm not sure where you're trying to go")
                            continue
                        else:
                            destination = last_room_name
                    elif destination not in current_room.navi.keys():
                        print("I'm not sure where you're trying to go.")
                        continue
                    else:
                        destination = current_room.navi[destination]
                    last_room_name = room_name
                    room_name = destination
                    current_room = storydata[room_name]
                    focus = current_room
                    print(current_room.name)

                case "look":
                    nouns = result.get("noun")
                    if len(nouns) == 0:
                        print(focus.desc)
                        continue
                    noun = nouns[0]
                    if noun == "around":
                        print(current_room.desc)
                        focus = current_room
                    elif noun == "it":
                        print(focus.desc)
                    elif noun in focus.list_items():
                        i = focus.get_item(noun)
                        print(i.desc)
                        focus = i
                    elif noun in current_room.list_items():
                        i = current_room.get_item(noun)
                        focus = i
                        print(i.desc)
                    else:
                        print("I can't quite tell what you're trying to look at")
                
                case _:
                    print("I can't %s that" % result.get("verb"))


def print_help(input_str: str):
    print("You can any one of these actions to interact with the world: ")
    print(" 'push', 'pull', 'take', 'use', 'look', 'go to', 'open', 'close' ")
    print("You can also use the command 'check inventory' to see what items you've collected")
    print("You can use the 'exit' command when you're done playing")


def print_inventory(inv):
    if len(inv) == 0:
        print("Your inventory is empty")
        return
    print("You have a(n):", end=' ')
    for item in inv:
        print(item, end=" ")


if __name__ == "__main__":
    main()