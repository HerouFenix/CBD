import redis


r = redis.Redis()
    
def main():

    search = input("Search for ('ENTER' to quit): ")

    if len(search) == 0:
        return "EXIT"
    
    all_results = [str(key, "utf-8") for key in list(r.keys(search+"*"))]
    
    if len(all_results) == 0:
        print("No results found!")
    else:
        for i in all_results:
            print(i)

    return "CONTINUE"
    

if __name__ == '__main__':
    #First we build all keys (and leave the values blank since redis doesn't allow us to search by value =/)
    with open("female-names.txt","r") as reader: #Add data to name_counter
        for name in reader:
            r.sadd(name,"")

    #And now we start the program
    while True:
        result = main()
        if result == "EXIT":
            break
    
    print("Smell ya later")

