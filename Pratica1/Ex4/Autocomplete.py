import redis


r = redis.Redis()
    
def main():

    search = input("Search for ('ENTER' to quit): ")

    if len(search) == 0:
        return "EXIT"
    
    #Originally all I did was a simple Key Search
    #all_results = [str(key, "utf-8") for key in list(r.keys(search+"*"))]
    
    #A much better way to do it is to use an Ordered Set and use a ZRANGE (by lex)
    # https://redis.io/commands/zrangebylex

    #Syntax:
    #   ZRANGEBYLEX key min max [LIMIT offset count] 
    #   key - Our Ordered Set's name
    #   min - Our input (we have to start in what we're given)
    #   max - Our input\xff
    #       the idea to use \xff as a delimiter came from https://stackoverflow.com/questions/24418807/how-to-imitate-autocomplete-search-with-redis-zrangebylex
    #       \xff is an escape sequence that denotes the largest (lexicographically-wise) character.
    #       \' is an escape character, 'x' denotes hexadecimal character representation and 'ff' is 255 in base 16.
    #       Note that this works becuse Strings are compared as binary array of bytes

    #Why:
    #   When all the elements in a sorted set are inserted with the same score, in order to force lexicographical ordering, this command returns all the elements in the sorted set at key with a value between min and max.

    #Considerations:
    #   Valid start and stop must start with ( or [, in order to specify if the range item is respectively exclusive or inclusive. 
    all_results = [str(key,"utf-8").replace("\n","") for key in r.zrangebylex(name="Names",min=f"[{search}",max=f"[{search}\xff")]

    
    if len(all_results) == 0:
        print("No results found!")
    else:
        for i in all_results:
            print(i)
    print()
    return "CONTINUE"
    

if __name__ == '__main__':
    #First we start by building our structure
    with open("female-names.txt","r") as reader: #Add data to name_counter
        for name in reader:
            #Instead of just using plain old Key, we should use a more appropriate structure
            #r.sadd(name,"")

            #Such as an Ordered Set!!
            #Basically the combination of a Redis Set and a Redis Set. Like a Set, this data structure is ordered, and like a Set, members in this structure are guaranteed to be unique. Each member is given a score and the set is sorted according to these values. If two members have identical scores, the members are then sorted lexicographically by value (i.e alphabetically).
            #So...its pretty much perfect for this sittuation
            r.zadd("Names",{name:0})    #Adds the key name with scorer 0 to our Ordered Set Names

    inserts = r.zcount("ScoredNames",min="-inf",max="+inf")
    print(f"Successfully inserted {inserts} entries\n")
    
    #And now we start the program
    while True:
        result = main()
        if result == "EXIT":
            break
    
    print("Smell ya later")

