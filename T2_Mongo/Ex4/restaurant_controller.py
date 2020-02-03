from pymongo import *
from datetime import datetime

CLIENT = MongoClient()


def insert_document(collection, new_doc):
    try:
        inserted_id = collection.insert_one(new_doc).inserted_id
        print("Success!\n >",inserted_id,"\n")

    except Exception as e:
        print("Error: ", e)
        print("No new document was inserted!\n")


def update_documents(collection, update_query, update_values):
    try:
        update_count = collection.update_many(update_query, update_values).modified_count
        print("Success!\n >",update_count, " documents updated\n")

    except Exception as e:
        print("Error: ", e)
        print("No document was updated!\n")


def search_by_query(collection, search_query):
    try:
        for document in collection.find(search_query):
            print(" >",document,"\n")

    except Exception as e:
        print("Error: ", e)
        print("Couldn't search for any document!\n")


def create_new_index(collection,index,name):
    try:
        collection.create_index(index,name=name)

        for indexes in collection.index_information():
            print(" >",indexes,"\n")

    except Exception as e:
        print("Error: ", e)
        print("Couldn't creat the index!\n")


def count_localidades(collection):
    try:
        result = collection.aggregate([{"$group": {"_id": "$localidade"}}])
        return len(list(result))
    except Exception as e:
        print("Error: ", e)
        print("Couldn't query collection!\n")


def count_rest_by_localidade(collection):
    try:
        result = collection.aggregate([{"$group": {"_id": "$localidade", "noRestaurants": {"$sum": 1}}}])
        return ["-> " + str(document["_id"]) + " - " + str(document["noRestaurants"]) for document in list(result)]
    except Exception as e:
        print("Error: ", e)
        print("Couldn't query collection!\n")


def count_rest_by_localidade_by_gastronomy(collection):
    try:
        result = collection.aggregate([{"$group": {"_id": {"localidade": "$localidade","gastronomy": "$gastronomia"}, "noRestaurants": {"$sum": 1}}}])
        return ["-> " + str(document["_id"]["localidade"]) + " | " + str(document["_id"]["gastronomy"]) + " - " + str(document["noRestaurants"]) for document in list(result)]
    except Exception as e:
        print("Error: ", e)
        print("Couldn't query collection!\n")


def get_rest_with_name_closer_to(collection,name):
    try:
        result = collection.aggregate([{"$match": {"nome": {"$regex": name}}}])
        return ["-> " + str(document["nome"]) for document in list(result)]
    except Exception as e:
        print("Error: ", e)
        print("Couldn't query collection!\n")


def main(db_name, collection_name):
    db = CLIENT[db_name]
    collection = db[collection_name]

    insert_document(collection, {"address": {"building": "69420", "coord": [-69.0, 420.696969], "rua": "Some Street", "zipcode": "42069"}, "localidade": "Sta Maria da Feira", "gastronomia": "Italian", "grades": [{"date": datetime(2019, 6, 12, 0, 0), "grade": "A", "score": 69}, {"date": datetime(
        2017, 7, 7, 0, 0), "grade": "B", "score": 100}], "nome": "Fierabella", "restaurant_id": "69696969"})

    update_documents(collection,{"localidade": "Sta Maria da Feira"},{"$set": {"rua": "Ao pe do castelo"}})

    search_by_query(collection,{"gastronomia": "Italian"})

    create_new_index(collection,"localidade","localidade")
    create_new_index(collection,"gastronomia","gastronomia")
    create_new_index(collection,[("nome",TEXT)],"nome")
    
    print("\nNumber of locations: ", count_localidades(collection))
    
    print("\nNumber of restaurants per locale")
    for i in count_rest_by_localidade(collection):
        print(" ",i)

    print("\nNumber of restaurants per locale and gastronomy")
    for i in count_rest_by_localidade_by_gastronomy(collection):
        print(" ",i)

    print("\nName of restaurants whose names contain \'Park\'")
    for i in get_rest_with_name_closer_to(collection,"Park"):
        print(" ",i)

if __name__ == '__main__':
    main("cbd", "rest")
