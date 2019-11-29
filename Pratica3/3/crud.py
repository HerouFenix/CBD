from cassandra.cluster import Cluster
import uuid
import datetime

cluster = Cluster()  # Connect to our Cassandra Server Cluster
session = cluster.connect('cbd_video_sharing')  # Connect to our Keyspace

insert_types = {'user': '(email, name, reg_timestamp, username)',
                'video': '(id, author, upload_timestamp, description, name, tags)',
                'comment_per_author': '(id, video_id, author, comment, upload_timestamp)',
                'comment_per_video': '(id, video_id, author, comment, upload_timestamp)',
                'follower': '(user,video_id)',
                'event': '(id, user, video_id, action, real_timestamp, video_timestamp)',
                'rating': '(id, video_id, value)'}  # Used to store what data goes into what table


def insert_data(column_family, data):
    if column_family.lower() not in insert_types:
        print("Error! There's no table named ", column_family)
        return 0
    else:
        values = insert_types[column_family.lower()]

    try:
        session.execute(f"INSERT INTO {column_family} {values} VALUES {data}")
    except Exception as e:
        print("Error! ", e)
        return 0


def alter_data(column_family, alteration, condition):
    if column_family.lower() not in insert_types:
        print("Error! There's no table named ", column_family)
        return 0

    try:
        session.execute(
            f"UPDATE {column_family} SET {alteration} WHERE {condition}")
    except Exception as e:
        print("Error! ", e)
        return 0


def search_data(column_family, fields, where=None, group_by=None, order_by=None, limit=None, allow_filtering=False):
    if column_family.lower() not in insert_types:
        print("Error! There's no table named ", column_family)
        return 0

    try:
        query_string = f"SELECT {fields} FROM {column_family} "

        if where is not None:
            query_string += f"WHERE {where} "
        if order_by is not None:
            query_string += f"ORDER BY {order_by} "
        if limit is not None:
            query_string += f"LIMIT {limit} "
        if allow_filtering:
            query_string += f"ALLOW FILTERING"

        return_values = [value for value in session.execute(query_string)]
        return return_values
    except Exception as e:
        print("Error! ", e)
        return 0


def main():
    #UNCOMMENT TO TEST INSERTION AND ALTERATION
    
    #insert_data("user", ('test@test.test', 'Python Test',
    #                     str(datetime.datetime.now())[:-3], 'PyBoy'))
    #alter_data("user", "username = 'CoolPyBoy'", "email = 'test@test.test'")

    print("Lista das tags de determinado vídeo")
    #SELECT tags FROM video WHERE id = 19e006d0-0d6d-11ea-9d48-0b1cc2ad2f9d ;
    for i in search_data("video", "tags","id = 19e006d0-0d6d-11ea-9d48-0b1cc2ad2f9d"):
        print(" ",i)

    print("\nOs últimos 5 eventos de determinado vídeo realizados por um utilizador")
    #SELECT * FROM event WHERE user='ds@test.com' AND video_id = 1f1a11e0-0d6d-11ea-9d48-0b1cc2ad2f9d LIMIT 5;
    for i in search_data("event", "*","user='ds@test.com' AND video_id = 1f1a11e0-0d6d-11ea-9d48-0b1cc2ad2f9d", limit=5):
        print(" ",i)

    print("\nOs últimos 5 eventos de determinado vídeo realizados por um utilizador")
    #SELECT * FROM video WHERE author = 'ds@test.com' AND upload_timestamp > '2019-11-22 21:14:40' AND upload_timestamp < '2019-11-22 21:14:43' ALLOW FILTERING;
    for i in search_data("video", "*","author = 'ds@test.com' AND upload_timestamp > '2019-11-22 21:14:40' AND upload_timestamp < '2019-11-22 21:14:43'", allow_filtering=True):
        print(" ",i)

    print("\nPermitir a pesquisa do rating médio de um vídeo e quantas vezes foi votado;")
    #SELECT avg(value), count(value) FROM rating WHERE video_id = 1baab4b0-0d6d-11ea-9d48-0b1cc2ad2f9d ;
    for i in search_data("rating", "avg(value), count(value)","video_id = 1baab4b0-0d6d-11ea-9d48-0b1cc2ad2f9d"):
        print(" ",i)

if __name__ == "__main__":
    main()
