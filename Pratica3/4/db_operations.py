from cassandra.cluster import Cluster
from random import randrange
from datetime import datetime, timedelta

cluster = Cluster()  # Connect to our Cassandra Server Cluster
session = cluster.connect('cbd_store_chain_db')  # Connect to our Keyspace

insert_types = {'product': '(id, manufacturer, name, price, stock_per_store, type)',
                'clerk': '(store_id, id, age, name, salary)',
                'store': '(city, id, employee_set, street, zipcode)',
                'sale': '(store_id, clerk_id, sale_timestamp, products_sold)'}  # Used to store what data goes into what table

random_names = ['Harleigh Rooney',
                'Rachael Johns',
                'Mariella Simmonds',
                'Shannon Whelan',
                'Tamar Poole',
                'Andrea Cairns',
                'Sonny Frey',
                'Ritik Carney',
                'Dalton Drew',
                'Lyndsey Carpenter',
                'Ivo Osborn',
                'Tommie Sargent',
                'Huey Arellano',
                'Josiah Santos',
                'Madison Frame',
                'Franco Cousins',
                'Silas Austin',
                'Leo Waller',
                'Tyriq Mackenzie',
                'Elliott Madden',
                'Cerys Walter',
                'Mahamed Alfaro',
                'Rumaysa Bains',
                'Huxley Mcloughlin',
                'Luke Broadhurst',
                'Isra Philip',
                'Chantelle Bartlett',
                'Kyle Valdez',
                'Ralphie Carr',
                'Jayda Bruce'
                ]

random_cities = ['Aveiro',
                 'Braga',
                 'Tomar',
                 'Porto',
                 'Lisboa',
                 'Vila Moura',
                 'Gaia',
                 'Espinho']

random_streets = ['Priors Knoll',
                  'Grays Maltings',
                  'Hollin Drift',
                  'Ashtree Willows',
                  'Woodstock Drift',
                  'Welbourne Road',
                  'Highlands',
                  'Cotton Furlong',
                  'Upper Sound',
                  'Eleanor Glas',
                  'Oakdene Avenue',
                  'Montpelier Trees',
                  'CC Jlo Row'
                  ]

random_zipcodes = ['42001',
                   '11714',
                   '22630',
                   '48430',
                   '94070',
                   '07601',
                   '30019',
                   '32780',
                   '27253',
                   '26554',
                   '79106',
                   '58501',
                   '42069'
                   ]

random_product_names = [['coffee', 'drink'],
                        ['lego', 'toy'],
                        ['ham', 'food'],
                        ['football', 'toy'],
                        ['vodka', 'alcohol'],
                        ['jagermeister', 'alcohol'],
                        ['bourbon', 'alcohol'],
                        ['tea', 'drink'],
                        ['sugar', 'spice'],
                        ['peas', 'food'],
                        ['catfish', 'food'],
                        ['kiwi', 'food'],
                        ['towels', 'bathroom']
                        ]

random_company_names = ['McAlex Donaldsons',
                        'Just an idea',
                        'Donaldson Unlimited',
                        'Bold',
                        'The Blacksmith Council',
                        'Sounds a bit evil',
                        'Lauren Clifford Associates',
                        'Sounds Professional',
                        'Clifford of Canada',
                        'Geographical',
                        'Blacksmith Industries',
                        'Classic',
                        'Clifford, Blacksmith And Donaldson, Associates',
                        'Sounds Professional',
                        'Sewing Schmewing',
                        'Silly',
                        'Clifford and Co',
                        'Classic',
                        'Clifford Corp',
                        'Sound big and possibly a bit souless',
                        'Coach Coach Coach'
                        ]


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


def random_date(start, end):
    """
    This function will return a random datetime between two datetime
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)


def populate_db():
    store_clerk_map = {}

    print("INSERTING DATA TO STORES")
    for i in range(13):
        # 'store': '(city, id, employee_set, street, zipcode)'

        print("INSERTING STORE -", i)
        city = random_cities[randrange(len(random_cities))]
        insert_data(
            "store", (city, i, {}, random_streets[i], random_zipcodes[i]))

        store_clerk_map[i] = [city, []]

    print("\nINSERTING DATA TO CLERKS")
    for i in range(30):
        # 'clerk': '(store_id, id, age, name, salary)'

        print("INSERTING CLERK -", i)

        store = randrange(13)
        store_clerk_map[store][1].append(i)

        insert_data("clerk", (store, i, randrange(
            16, 61), random_names[i], randrange(400, 601)))

    print("\nINSERTING DATA TO PRODUCTS")
    for i in range(13):
        # 'product': '(id, manufacturer, name, price, stock_per_store, type)'

        print("INSERTING PRODUCT -", i)

        insert_data(
            "product", (i, random_company_names[randrange(13)], random_product_names[i][0], randrange(2, 20) + float('0' + str(randrange(99))), {
                        store: randrange(30) for store in range(13)}, random_product_names[i][1]))

    print("\nINSERTING DATA TO SALES")
    d1 = datetime.strptime('01/01/19 00:00:00', '%m/%d/%y %H:%M:%S')
    d2 = datetime.strptime('12/31/19 00:00:00', '%m/%d/%y %H:%M:%S')

    for i in range(20):
        # 'sale': '(store_id, clerk_id, sale_timestamp, products_sold)'

        print("INSERTING SALE -", i)

        products = [randrange(13)]

        while randrange(10) > 5:
            products.append(randrange(13))

        while True:
            store = randrange(13)
            if len(store_clerk_map[store][1]) == 0:
                continue
            else:
                break

        employee = store_clerk_map[store][1][randrange(
            len(store_clerk_map[store][1]))]

        insert_data(
            "sale", (store, employee, str(random_date(d1, d2)), products))

    print("\nUPDATING THE STORE'S EMPLOYEE SET")
    for store in store_clerk_map:
        new_set = "{"
        for emp in store_clerk_map[store][1]:
            new_set += str(emp) + ","
        new_set = new_set[:-1] + "}"

        condition = "city= '" + store_clerk_map[store][0] + "' AND id= " + str(store)
        
        alter_data("store", "employee_set= " + new_set, condition)

def main():
    populate_db()


if __name__ == "__main__":
    main()
