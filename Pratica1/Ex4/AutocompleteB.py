import redis


r = redis.Redis()
    
def main():

    search = input("Search for ('ENTER' to quit): ")

    if len(search) == 0:
        return "EXIT"
    
    #In the same vain as the last exercise, lets use the ZRANGEBYSCORE ability of Ordered Sets to optimize our search
    # https://redis.io/commands/zrangebyscore

    #Syntax:
    #   ZREVRANGEBYSCORE key min max [WITHSCORES] [LIMIT offset count] 
    #   key - Our Ordered Set's name
    #   min - -inf
    #   max - +inf
    #   WITHSCORES argument makes the command return both the element and its score

    #Why:
    #   Returns all the elements in the sorted set at key with a score between min and max (including elements with score equal to min or max). The elements are considered to be ordered from low to high scores.
    autocomplete = [key for key in r.zrangebylex(name="Names",min=f"[{search}",max=f"[{search}\xff")]
    all_results = [(str(key,"utf-8"),value) for key,value in r.zrevrangebyscore(name="ScoredNames",min="-inf",max="+inf",withscores=True) if key in autocomplete]


    if len(all_results) == 0:
        print("No results found!")
    else:
        for i in all_results:
            print('{:10} : {}'.format(i[0],i[1]))

    print()
    return "CONTINUE"
    

if __name__ == '__main__':
    #ordenado pela popularidade decrescente do nome

    #NOTE: I had to create 2 ordered sets, one where all ranks are the same and one with the ranking in the .csv
    #   This was done due to the fact that zrangebylex doesn't work if we have differente scores:
    #       "When all the elements in a sorted set are inserted with the same score, in order to force lexicographical ordering, this command returns all the elements in the sorted set at key with a value between min and max."
    #       "If the elements in the sorted set have different scores, the returned elements are unspecified."
    #           -https://redis.io/commands/zrangebylex 

    with open("nomes-registados-2018.csv","r") as reader: #Add data to name_counter
        for line in reader:
            #Format:
            #   name,gender,popularity

            line_data = line.strip().split(",")
            r.zadd("ScoredNames",{line_data[0]:line_data[2]}) 
            r.zadd("Names",{line_data[0]:0}) 


    inserts = r.zcount("ScoredNames",min="-inf",max="+inf")
    print(f"Successfully inserted {inserts} entries\n")

    #And now we start the program
    while True:
        result = main()
        if result == "EXIT":
            break
    
    print("Smell ya later")

