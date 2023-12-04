from parsing import parse
import shelve

def print_help():
    print("You can use the verbs to interact with the world: ")
    print(" 'push', 'pull', 'take', 'use', 'look', 'go to', 'open', 'close' ")


def main():

    with shelve.open("savedata") as data:

        if data.get("inventory") == None:
            data["inventory"] = []
        
        print(data['inventory'])

        data['inventory'].append("Knife")

        print(data['inventory'])

        return

        while True:
            input_str = input("> ")
            result = parse(input_str)

            match result.ERROR:
                case 1:
                    print("I'm not sure what action you're trying to take")
                    continue
                case 2:
                    print("You can only take one action at a time")
                    continue
                case 3:
                    print("I'm not sure what object(s) you're trying to [%s]" % result.verb)
                    pass
                case 0:
                    


                    pass

            if result.ERROR: print(result)



if __name__ == "__main__":
    main()