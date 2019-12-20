with open("../pokemon_type_relations.csv", "r") as reader:
        header = reader.readline().split(",")  # Read header

        while True:
            line = reader.readline()

            if not line: 
                break

            line = line.split(",")
            attacker = line[0]
            weak = []
            strong = []
            immune = []

            for i in range(0, len(line)):
                if line[i] == "0":
                    immune.append(header[i])
                if line[i] == "2":
                    strong.append(header[i])
                if line[i] == "0.5":
                    weak.append(header[i])

            with open("../pokemon_type_strength.csv", "a") as appender:
                for strong_against in strong:
                    appender.write(attacker + "," + strong_against+"\n")

            with open("../pokemon_type_weakness.csv", "a") as appender:
                for weak_against in weak:
                    appender.write(attacker + "," + weak_against+"\n")

            with open("../pokemon_type_immune.csv", "a") as appender:
                for immune_against in immune:
                    appender.write(immune_against + "," + attacker+"\n")
