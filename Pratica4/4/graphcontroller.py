from neo4j import GraphDatabase


class PokemonGraphController(object):

    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self._driver.close()

    def insert_data(self):
        self.insert_nodes()
        self.insert_relations()

    def insert_nodes(self):
        with self._driver.session() as session:
            # Nodes
            print("Inserting Pokemon")
            session.run(
                "LOAD CSV WITH HEADERS FROM 'file:///pokemon.csv' AS Row MERGE (pokemon:Pokemon {name: Row.Name}) SET  pokemon.number=Row.Entry, pokemon.total=Row.Total, pokemon.hp=Row.HP, pokemon.attack=Row.Attack, pokemon.defense=Row.Defense, pokemon.spatk=Row.Sp.Atk, pokemon.spdef=Row.Sp.Def, pokemon.speed=Row.Speed")

            print("Inserting Generations")
            session.run(
                "LOAD CSV WITH HEADERS FROM 'file:///pokemon.csv' AS Row MERGE (generation:Generation {number: Row.Generation})")

            print("Inserting Type 1")
            session.run(
                "LOAD CSV WITH HEADERS FROM 'file:///pokemon.csv' AS Row MERGE (tipo:Type {type: Row.Type1})")

            print("Inserting Type 2")
            session.run(
                "LOAD CSV WITH HEADERS FROM 'file:///pokemon.csv' AS Row WITH Row WHERE NOT Row.Type2 IS null MERGE (tipo:Type {type: Row.Type2})")

    def insert_relations(self):
        with self._driver.session() as session:
            # Relationships
            print("\nInserting Pokemon-Generation Relationships")
            session.run(
                "LOAD CSV WITH HEADERS FROM 'file:///pokemon.csv' AS Row MATCH(pokemon:Pokemon {name: Row.Name}),(generation:Generation {number: Row.Generation}) CREATE (pokemon)-[:GEN]->(generation)")

            print("Inserting Pokemon-Type1 Relationships")
            session.run(
                "LOAD CSV WITH HEADERS FROM 'file:///pokemon.csv' AS Row MATCH(pokemon:Pokemon {name: Row.Name}),(type:Type {type: Row.Type1}) CREATE (pokemon)-[:Type]->(type)")

            print("Inserting Pokemon-Type2 Relationships")
            session.run(
                "LOAD CSV WITH HEADERS FROM 'file:///pokemon.csv' AS Row WITH Row WHERE NOT Row.Type2 IS null MATCH(pokemon:Pokemon {name: Row.Name}),(type:Type {type: Row.Type2}) CREATE (pokemon)-[:Type]->(type)")

            print("Inserting Pokemon-type Weaknesses")
            session.run(
                "LOAD CSV WITH HEADERS FROM 'file:///pokemon_type_weakness.csv' AS Row WITH Row  MATCH(attacker:Type {type: Row.Attacker}),(defender:Type {type: Row.Defender}) CREATE (attacker)-[:WEAK_AGAINST]->(defender)")

            print("Inserting Pokemon-type Strength")
            session.run(
                "LOAD CSV WITH HEADERS FROM 'file:///pokemon_type_strength.csv' AS Row WITH Row  MATCH(attacker:Type {type: Row.Attacker}),(defender:Type {type: Row.Defender}) CREATE (attacker)-[:STRONG_AGAINST]->(defender)")

            print("Inserting Pokemon-type Immunities")
            session.run(
                "LOAD CSV WITH HEADERS FROM 'file:///pokemon_type_immune.csv' AS Row WITH Row  MATCH(attacker:Type {type: Row.Attacker}),(defender:Type {type: Row.Defender}) CREATE (defender)-[:IMMUNE_AGAINST]->(attacker)")

    def query_builder(self, query):
        with self._driver.session() as session:
            return session.run(query)


if __name__ == "__main__":
    controller = PokemonGraphController(
        "bolt://localhost:7687", "neo4j", "pokemon")

    #controller.insert_data()

    counter = 1

    query_list = ["MATCH (n:Type) RETURN n", 
                  "MATCH(poke:Pokemon)-[:Type]->(:Type {type:\"Dragon\"}) MATCH(poke)-[:GEN]->(:Generation {number:\"1\"}) WHERE toInt(poke.attack) > 80 return poke",
                  "MATCH(poke:Pokemon)-[:Type]->(:Type {type:\"Steel\"}) RETURN poke ORDER BY poke.HP DESC LIMIT 1",
                  "MATCH(poke:Pokemon) RETURN poke ORDER BY poke.speed LIMIT 3",
                  "MATCH(poke:Pokemon)-[:Type]->(:Type {type:\"Psychic\"}) MATCH(poke)-[:Type]->(:Type{type:\"Fire\"}) MATCH(poke)-[:GEN]->(:Generation{number:\"5\"}) return poke",
                  "MATCH(immune:Type)-[:IMMUNE_AGAINST]->(attacker:Type{type:\"Ghost\"}) return immune",
                  "MATCH(lucario:Pokemon{name:\"Lucario\"})-[:Type]->(lucario_types:Type) MATCH(lucario_types:Type)-[:STRONG_AGAINST]->(types:Type) RETURN types",
                  "MATCH(gyarados:Pokemon{name:\"Gyarados\"})-[:Type]->(gyarados_type:Type) MATCH(gyarados_type:Type)-[:WEAK_AGAINST]->(types:Type) MATCH(pokemon:Pokemon)-[:Type]->(types) WITH COUNT(pokemon) AS counter RETURN counter",
                  "MATCH(pokemon:Pokemon)-[:Type]->(:Type{type:\"Fighting\"}) MATCH(pokemon)-[:Type]->(types:Type) MATCH(types)-[:WEAK_AGAINST]->(:Type{type:\"Water\"}) RETURN pokemon",
                  "MATCH(pokemon:Pokemon) WHERE(pokemon.name ENDS WITH 'chu') RETURN pokemon"]
    
    query_verbose = ["Get all Pokemon Types in the database",
                     "Get all Dragon Type Pokemons from the first generation that have over 80 attack",
                     "Get the Steel Pokemon with the Highest HP",
                     "Get the 3 Pokemon with the lowest speed",
                     "Get all Psychich type Pokemon from the 5th Generation that are also Fire type",
                     "Get all Pokemons immune to Ghost Type",
                     "Get all Pokemons that Lucario is Strong Against",
                     "Get how many Pokemons that Gyarados is weak against",
                     "List all Fighting Type Pokemon that are Weak against Water",
                     "List all Pokemon whose name ends with \"chu\""]
    with open("../CBD_L44c_output.txt", "w") as writer:
        for current_query in query_list:
            query = current_query
            writer.write("Query " +  str(counter) + ": " + query_verbose[counter-1]+"\n")
            writer.write("  " +  current_query +"\n")

            counter += 1

            query_result = controller.query_builder(query)
            for i in query_result:
                print(i.items()[0][1])
                writer.write("  " + str(i.items()[0][1]) + "\n")
            writer.write("\n\n")

    controller.close()
