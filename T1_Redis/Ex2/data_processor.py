name_counter = {} #Dictionary that stores, as keys, the initial letters of each name and as values the total amount of names that start with that letter

with open("female-names.txt","r") as reader: #Add data to name_counter
    for line in reader:
        if line[0].upper() not in name_counter:
            name_counter[line[0].upper()] = 0
        
        name_counter[line[0].upper()] += 1

with open("initials4redis.txt","w") as writer:
    for key, value in name_counter.items():
        writer.write(f" SET {key} {value}\n")


