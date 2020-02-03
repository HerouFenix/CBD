# Prática CBD - 2

# Index
- [Initial Configurations](#initial-configurations)
 - [Using Robo3T](#using-robo3t)
 - [Initial MongoDB Interactions](#initial-mongodb-interactions)
	 - [Storage Structures](#storage-structures)
		 - [Database](#database)
		 - [Collections](#collections)
		 - [Documents](#documents)
	- [Storage Structures](#storage-structures)
		 - [Database](#database)
		 - [Collections](#collections)
		 - [Documents](#documents)
	- [Some Commands](#some-commands)
		 - [Database Commands](#database-commands)
			 - [Creating a Database](#creating-a-database)
			 - [Checking what the current Database is](#checking-what-the-current-database-is)
			 - [Viewing all Databases](#viewing-all-databases)
			 - [Dropping a Database](#dropping-a-database)
		 - [Collection Commands](#collections-commands)
			 - [Creating a Collection](#creating-a-collection)
			 - [Viewing all Collections](#viewing-all-collections)
			 - [Dropping a Collection](#dropping-a-collection)
		 - [Document Commands](#document-commands)			 
			 - [Insert a Document](#insert-a-document)
			 - [Query a Document](#query-a-document)
			 - [Update a Document](#update-a-document)
			 - [Delete a Document](#delete-a-document)
	- [Types & Arrays](#types-and-arrays)
		- [Types](#types)
		- [Arrays](#arrays)
	- [Aggregations & Mapreduces](#aggregations-and-mapreduces)
		- [Aggregations](#aggregations)
			- [Aggregate Functions Table](#aggregate-functions-table)
			- [Pipeline Stages](#pipeline-stages)
		- [Mapreduces](#mapreduces)
 - [Query Construction](#query-construction)
	 - [Setup](#setup)
	 - [Exercises](#exercises)
- [Server Side Functions](#server-side-functions)
	- [a)](#a)
	- [b)](#b)
	- [c)](#c)
	- [d)](#d)
- [MongoDB Driver](#mongodb-driver)
	- [Setup](#setup)
	-  [a)](#a)
	- [b)](#b)
	- [c)](#c)
- [Freeform DB](#freeform-db)
		

# Initial Configurations
Checkout https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/

### Starting the MongoDB Server
``` 
$ sudo service mongod start
```
### Stopping the MongoDB Server
``` 
$ sudo service mongod stop
```
### Restarting the MongoDB Server
``` 
$ sudo service mongod restart
```
### Booting up the MongoDB Shell
``` 
$ mongo
```

# Using Robo3t
You can think of Robo3t as a sort of IDE for our MongoDB Server (kinda like the SQLManager).

### Installation:
`$ sudo snap install robo3t-snap`

### Usage:
1. Initiate the MongoDB Server (`$ sudo service mongod start`)
2.  Start Robo3t
3. On the top bar click **File>Connection**
4. On the newly opened window, click **Create**
5. Input the server's IP and Port (by default it should be **localhost** and **27017**) and name the server
6. Right-click on the server's name and choose **Open Shell**
7. And you're done. You can now interact with your server through Robo3t instead of having to use the normal bash terminal

# Initial MongoDB Interactions

## Storage Structures
### Database

> Database is a physical container for collections. Each database gets its own set of files on the file system. A single MongoDB server typically has multiple databases.

### Collections

> Collection is a group of MongoDB documents. It is the equivalent of an RDBMS table. A collection exists within a single database. Collections do not enforce a schema. Documents within a collection can have different fields. Typically, all documents in a collection are of similar or related purpose.

### Documents

> A document is a set of key-value pairs. Documents have dynamic schema. Dynamic schema means that documents in the same collection do not need to have the same set of fields or structure, and common fields in a collection's documents may hold different types of data.

Basically:
-	A server contains multiple Databases, which in turn have several Collections that possess some Documents.

-	Making an analogy with non-document oriented databases, **Collections** correspond to **Tables**, whilst **Documents** correspond to **Tuples/Rows**, in which each of the Document's **Fields** are the **Columns**

## Some Commands

### Database Commands:
#### Creating a Database
This command is used to create and switch to a new DB
```
> use testDB
switched to db testDB
```

#### Checking what the current Database is
This command returns the name of the database you're currently using
```
> db
testDB
```
#### Viewing all Databases
Check what databases exist (Note that our newly created DB doesn't show up yet because its completely empty!)
```
> show dbs
admin   0.000GB
config  0.000GB
local   0.000GB
```
#### Dropping a Database
Drops the current database
```
> db.dropDatabase()
```

### Collection Commands:
#### Creating a Collection
db.createCollection(name, options) is used to create collection. The options field allows a user to specify parameters like memory size and indexing.
```
> db.createCollection("testcollection")
{  "ok"  :  1  }
```
Note that if you're using Robo3t, the object will be displayed in the gui and not in the form of a dictionary
Also, pay attention to the fact that: 
> In MongoDB, you don't need to create collection. MongoDB creates collection automatically, when you insert a document.

#### Viewing all Collections
Show all collections in the currently selected Database
```
> show collections
testcollection
```
#### Dropping a Collection
Drop the collection
```
>db.testcollection.drop()
true
```

### Document Commands:
#### Insert a Document
To insert data into a MongoDB collection, you need to use the **insert()** or **save()** method.

Using the **insert** method boils down to **db.COLLECTION_NAME.insert(DOCUMENT)**
```
> db.testcollection.insert({
   _id: 0,
   name: 'DS', 
   description: 'Hey demons, it\'s me, ya boi',
   team: "Pirocanhoes"
})
Inserted 1 record(s) in 7ms
```

To insert **multiple documents** in a single query, you can pass an array of documents in insert() command.

```
> db.testcollection.insert([
   {_id: 1,
    name: 'André Baião', 
    description: 'Acoreano',
    team: "Pirocanhoes"},
    {_id: 2,
    name: 'Chico com Ch', 
    description: 'Minimeu',
    team: "FTW"}
    ])
Inserted 1 record(s) in 3ms
```

In regards to the **save()** method:

> To insert the document you can use **db.post.save(document)** also. If you don't specify **_id** in the document then **save()** method will work same as **insert()** method. If you specify _id then it will replace whole data of document containing _id as specified in save() method.

#### Query a Document
##### Query All Documents in collection
To query data from MongoDB collection, you need to use MongoDB's **find()** method.
```
> db.testcollection.find()
{ "_id" : 0, "name" : "DS", "description" : "Hey demons, it's me, ya boi", "team": "Pirocanhoes" }
{ "_id" : 1, "name" : "André Baião", "description" : "Acoriano", "team": "Pirocanhoes" }
{ "_id" : 2, "name" : "Chico com Ch", "description" : "Minimeu", "team": "FTW" }
```

You can also use the **prety()** method to format the way the query gets displayed:
```
> db.testcollection.find().pretty()
{ "_id" : 0, "name" : "DS", "description" : "Hey demons, it's me, ya boi", "team": "Pirocanhoes" }
{
	"_id" : 1,
	"name" : "André Baião",
	"description" : "Acoriano"
	"team": "Pirocanhoes"
}
{
	"_id" : 2,
	"name" : "Chico com Ch",
	"description" : "Minimeu"
	"team": "FTW"
}
```
##### Query for a specific Document in the collection
To search for a specific Document, you can just put one of the document's fields in the find() method, like so:
```
>db.testcollection.find({"_id":0})
{ "_id" : 0, "name" : "DS", "description" : "Hey demons, it's me, ya boi", "team": "Pirocanhoes" }

>db.testcollection.find({"name": "Chico com Ch"})
{ "_id" : 2, "name" : "Chico com Ch", "description" : "Minimeu", "team": "FTW" }
```

##### Output only SOME fields 
If you only want to show **SOME** of the fields you can use the find() method like so:
```
> db.testcollection.find({}, {name: 1, team: 1})
{ "_id" : 0, "name" : "DS","team": "Pirocanhoes" }
{ "_id" : 1, "name" : "André Baião", "team": "Pirocanhoes" }
{ "_id" : 2, "name" : "Chico com Ch", "team": "FTW" }
```
And if instead of including the fields you want to **exclude them** all you've gotta do is change that 1 to a 0
```
> db.testcollection.find({}, {description: 0})
{ "_id" : 0, "name" : "DS","team": "Pirocanhoes" }
{ "_id" : 1, "name" : "André Baião", "team": "Pirocanhoes" }
{ "_id" : 2, "name" : "Chico com Ch", "team": "FTW" }
```

##### Pass multiple keys
You can also pass multiple keys and mix them with **AND** and/or **OR** like so:
```
> db.testcollection.find({$or: [{team: "Pirocanhoes"},{team: "FTW"}]})
{ "_id" : 0, "name" : "DS", "description" : "Hey", "team" : "Pirocanhoes" }
{ "_id" : 1, "name" : "Andre", "description" : "acoreano", "team" : "Pirocanhoes" }
{ "_id" : 2, "name" : "Chico", "description" : "minimeu", "team" : "FTW" }

> db.testcollection.find({$and: [{team: "Pirocanhoes"},{name: "DS"}]})
{ "_id" : 0, "name" : "DS", "description" : "Hey", "team" : "Pirocanhoes" }
```

##### Query by comparassion
There are also commands for querying **Greater than**, **Lesser than**, **Not Equals**, etc etc

As a couple of examples, you can have:
```
> db.testcollection.find({"_id": {$gt: 0}}) #Find all documents which have an ID field greater than 0
{ "_id" : 1, "name" : "Andre", "description" : "acoreano", "team" : "Pirocanhoes" }
{ "_id" : 2, "name" : "Chico", "description" : "minimeu", "team" : "FTW" }

> db.testcollection.find({"_id": {$ne: 1}})
{ "_id" : 0, "name" : "DS", "description" : "Hey", "team" : "Pirocanhoes" }
{ "_id" : 2, "name" : "Chico", "description" : "minimeu", "team" : "FTW" }
```
Check out the other options over at https://www.tutorialspoint.com/mongodb/mongodb_query_document.htm

#### Update a Document
There are 2 ways to update a document in MongoDB, using UPDATE or SAVE:

-	**db.COLLECTION_NAME.update(SELECTION_CRITERIA, UPDATED_DATA)**:
	-	Updates the values in the existing document
		```
		> db.testcollection.update({'name':'Chico'},{$set:{'team':'Pirocanhoes'}})
		Updated 1 existing record(s) in 5ms
		```
	
	-	**NOTE:** By default, MongoDB will only update a single document. To update multiple documents, you need to set a parameter 'multi' to true.
		```
		> db.testcollection.update({'_id':{$gte: 0}},
		   {$set:{'description':'Winner of the DETIgameroom'}},{multi:true})
		Updated 3 existing record(s) in 23ms
		```

-	**db.COLLECTION_NAME.save({_id:ObjectId(),NEW_DATA})**:
	-	Replaces the existing document with the document passed in the passed as argument
		```
		> db.testcollection.save(
		   {
		      "_id" : 2, "name":"Rafa Simoes", "description": "MongoDB Creator", "team": "Pirocanhoes"
		   }
		)
		Updated 1 existing record(s) in 1ms
		```


#### Delete a Document
Deleting a document in MongoDB is as simple as using the Remove method.
This method has 2, optional, criteria:
-   **deletion criteria** − (Optional) deletion criteria according to documents will be removed.
    
-   **justOne** − (Optional) if set to true or 1, then remove only one document. This is used if multiple documents match your deletion criteria and you want to delete ONLY THE FIRST ONE

```
> db.testcollection.remove({'name':'Rafa Simoes'})
Removed 1 record(s) in 2ms

> db.testcollection.remove({'team':'Pirocanhoes'},1)
Removed 1 record(s) in 1ms
```

## Types and Arrays
### Types
MongoDB supports many datatypes, which includes:

-   **String** − This is the most commonly used datatype to store the data. String in MongoDB must be UTF-8 valid.
    
-   **Integer** − This type is used to store a numerical value. Integer can be 32 bit or 64 bit depending upon your server.
    
-   **Boolean** − This type is used to store a boolean (true/ false) value.
    
-   **Double** − This type is used to store floating point values.
    
-   **Min/ Max keys** − This type is used to compare a value against the lowest and highest BSON elements.
    
-   **Arrays** − This type is used to store arrays or list or multiple values into one key.
    
-   **Timestamp** − ctimestamp. This can be handy for recording when a document has been modified or added.
    
-   **Object** − This datatype is used for embedded documents.
    
-   **Null** − This type is used to store a Null value.
    
-   **Symbol** − This datatype is used identically to a string; however, it's generally reserved for languages that use a specific symbol type.
    
-   **Date** − This datatype is used to store the current date or time in UNIX time format. You can specify your own date time by creating object of Date and passing day, month, year into it.
    
-   **Object ID** − This datatype is used to store the document’s ID.
    
-   **Binary data** − This datatype is used to store binary data.
    
-   **Code** − This datatype is used to store JavaScript code into the document.
    
-   **Regular expression** − This datatype is used to store regular expression.

>Taken from:  https://www.tutorialspoint.com/mongodb/mongodb_datatype.htm


### Arrays
When it comes down to **arrays** you can basically insert any of these types in the form of an array by encapsulating them in a **[ ]**. This will allow you to have a filed that corresponds to an array of any of the data types above, or will allow you to achieve things like inserting multiple documents at once by including them in an array

## Indexes

> Indexes support the efficient resolution of queries. Without indexes, MongoDB must scan every document of a collection to select those documents that match the query statement. This scan is highly inefficient and require MongoDB to process a large volume of data.
> 
> Indexes are special data structures, that store a small portion of the
> data set in an easy-to-traverse form. The index stores the value of a
> specific field or set of fields, ordered by the value of the field as
> specified in the index.

### Creating an Index

To create an index you need to use ensureIndex() method of MongoDB.

### Syntax
To create an Index, all you've gotta do is use the **ensureIndex()** method.
This method's syntax looks like this : `db.COLLECTION_NAME.ensureIndex({KEY:1})`. KEY corresponds to the field we want to Index, 1 means we want the field to be indexed in Ascending order (if we were to use -1 it'd mean we wanted the field to be stored in descending order). 

Note that we can pass multiple KEYs to index multiple fields at once

The ensureIndex() method also accepts list of options (which are optional). To check out this list visit https://www.tutorialspoint.com/mongodb/mongodb_indexing.htm

```
> db.testcollection.ensureIndex({"name":1})
{
	"createdCollectionAutomatically" : true,
	"numIndexesBefore" : 1,
	"numIndexesAfter" : 2,
	"ok" : 1
}
```

## Aggregations and Mapreduces

### Aggregations

> Aggregations operations process data records and return computed
> results. Aggregation operations group values from multiple documents
> together, and can perform a variety of operations on the grouped data
> to return a single result. In SQL count(*) and with group by is an
> equivalent of mongodb aggregation.

**Note:** The following code examples will be presented using the Database and Collection used by the tutorial - https://www.tutorialspoint.com/mongodb/mongodb_aggregation.htm. This has been done due to the fact that aggregation functions make sense to use when you have a lot of fields/data and want to group them by certain parameters or functions, hence, to use a custom Database I'd have to come up with something more complex than this exercise is worth.

The aggregate function looks like `db.COLLECTION_NAME.aggregate(AGGREGATE_OPERATION)`.

For the following examples, consider the collection containing these documents:
```
{ _id:  ObjectId(7df78ad8902c),
  title:  'MongoDB Overview', 
  description:  'MongoDB is no sql database', 
  by_user:  'tutorials point', 
  url:  'http://www.tutorialspoint.com', tags:  ['mongodb',  'database',  'NoSQL'], 
  likes:  100  
},  
{ _id:  ObjectId(7df78ad8902d),
  title:  'NoSQL Overview', 
  description:  'No sql database is very fast', 
  by_user:  'tutorials point', 
  url:  'http://www.tutorialspoint.com', 
  tags:  ['mongodb',  'database',  'NoSQL'], 
  likes:  10  
},  
{ _id:  ObjectId(7df78ad8902e) 
  title:  'Neo4j Overview', 
  description:  'Neo4j is no sql database', 
  by_user:  'Neo4j', 
  url:  'http://www.neo4j.com', tags:  ['neo4j',  'database',  'NoSQL'], 
  likes:  750  
}
```

Imagine we want to display a list stating **how many tutorials are written by each user**. We can achieve this like so:
```
> db.mycol.aggregate([{$group :  {_id :  "$by_user", num_tutorial :  {$sum :  1}}}]) 
{  "result"  :  [  {  "_id"  :  "tutorials point",  "num_tutorial"  :  2  },  {  "_id"  :  "Neo4j",  "num_tutorial"  :  1  }  ],  "ok"  :  1  }
```

#### Aggregate Functions Table
-	**$sum**

	-	Sums up the defined value from all documents in the collection.

	-	`db.mycol.aggregate([{$group : {_id : "$by_user", num_tutorial : {$sum : "$likes"}}}])`

-	**$avg**

	-	Calculates the average of all given values from all documents in the collection.

	-	`db.mycol.aggregate([{$group : {_id : "$by_user", num_tutorial : {$avg : "$likes"}}}])`

-	**$min**

	-	Gets the minimum of the corresponding values from all documents in the collection.

	-	`db.mycol.aggregate([{$group : {_id : "$by_user", num_tutorial : {$min : "$likes"}}}])`


-	**$max**

	-	Gets the maximum of the corresponding values from all documents in the collection.

	-	`db.mycol.aggregate([{$group : {_id : "$by_user", num_tutorial : {$max : "$likes"}}}])`

-	**$push**

	-	Inserts the value to an array in the resulting document.

	-	`db.mycol.aggregate([{$group : {_id : "$by_user", url : {$push: "$url"}}}])`

-	**$addToSet**

	-	Inserts the value to an array in the resulting document but does not create duplicates.

	-	`db.mycol.aggregate([{$group : {_id : "$by_user", url : {$addToSet : "$url"}}}])`

-	**$first**

	-	Gets the first document from the source documents according to the grouping. Typically this makes only sense together with some previously applied “$sort”-stage.

	-	`db.mycol.aggregate([{$group : {_id : "$by_user", first_url : {$first : "$url"}}}])`

-	**$last**

	-	Gets the last document from the source documents according to the grouping. Typically this makes only sense together with some previously applied “$sort”-stage.

	-	`db.mycol.aggregate([{$group : {_id : "$by_user", last_url : {$last : "$url"}}}])`


#### Pipeline Stages
In Aggregations we have one (or several) pipeline stages, in which we're querying data. The execution of the aggregate function passes through each stage IN ORDER and does whatever it has to do. The full list can be found at https://docs.mongodb.com/manual/reference/operator/aggregation-pipeline/.

So in the end, we have the syntax:
**db.collection.aggregate( [ {PIPELINE_STAGE_1}, {PIPELINE_STAGE_2}, ... ], OPTIONS)**

The Options is an optional field. For more information visit https://docs.mongodb.com/manual/reference/method/db.collection.aggregate/

### Mapreduce

> **Map-reduce** is a data processing paradigm for condensing large volumes of data into useful aggregated results. MongoDB uses **mapReduce** command for map-reduce operations. MapReduce is generally used for processing large data sets.

The syntax is as follows:
```
>db.collection.mapReduce(  
	function()  {emit(key,value);},  //map function  
	function(key,values)  {return reduceFunction},  {  //reduce function  
		out: collection, 
		query: document, 
		sort: document, 
		limit: number 
	}
)
``` 
Where:
-   **map** is a javascript function that maps a value with a key and emits a key-value pair
    
-   **reduce** is a javascript function that reduces or groups all the documents having the same key
    
-   **out** specifies the location of the map-reduce query result
    
-   **query** specifies the optional selection criteria for selecting documents
    
-   **sort** specifies the optional sort criteria
    
-   **limit** specifies the optional maximum number of documents to be returned

Consider the following document:
```
{  "post_text":  "tutorialspoint is an awesome website for tutorials",  
   "user_name":  "mark",  
   "status":"active"  }
```


Now, lets use a MapReduce function on our **posts** collection to **select all the active posts, group them on the basis of user_name and then count the number of posts by each user**. This can be achieved using following code:
```
db.posts.mapReduce(  
	function()  { emit(this.user_id,1);  },  
	function(key, values)  {return  Array.sum(values)},  { 
		query:{status:"active"},
		out:"post_total"  
	}
)
```
Which will generate the output:
```
{
   "result" : "post_total",
   "timeMillis" : 9,
   "counts" : {
      "input" : 4,
      "emit" : 4,
      "reduce" : 2,
      "output" : 2
   },
   "ok" : 1,
}
```
The result shows that a total of 4 documents matched the query (status:"active"), the map function emitted 4 documents with key-value pairs and finally the reduce function grouped mapped documents having the same keys into 2.

To see which documents matched the query we can append **.find()** to the end of the map reduce function:
```
db.posts.mapReduce(  
	function()  { emit(this.user_id,1);  },  
	function(key, values)  {return  Array.sum(values)},  { 
		query:{status:"active"},
		out:"post_total"  
	}
).find()
```
Which will output:
```
{  "_id"  :  "tom",  "value"  :  2  }  
{  "_id"  :  "mark",  "value"  :  2  }
```


# Query Construction
## Setup
1. Just run `mongoimport --db cbd --collection rest --drop --file <path/>restaurants.json` to create the db **cbd** and add to it the collection **rest** containing all documents in the **restaurants.json** file.
2. To check if you did it correctly, run the following command and check if the output is the same as presented 
	```
	$ ./mongo
	> use cbd
	> db.rest.count() 
	3772
	```
## Exercises
For this exercise we had to present a TXT file containing all the queries made. To make it easier on me, instead of writing the answers here and on the TXT, I just copied the TXT's contents into the following code block:

```
// NMEC: 89348

#1
// Liste todos os documentos da coleção.
db.rest.find()

#2
// Apresente os campos restaurant_id, nome, localidade e gastronomia para todos os documentos da coleção.
db.rest.find({}, {restaurant_id: 1, nome: 1, gastronomia: 1, localidade: 1})

#3
// Apresente os campos restaurant_id, nome, localidade e código postal (zipcode), mas exclua o campo _id de todos os documentos da coleção.
db.rest.find({}, {_id: 0, restaurant_id: 1, nome: 1, localidade: 1, 'address.zipcode': 1})

#4 
//Indique o total de restaurantes localizados no Bronx.
db.rest.aggregate([{$match: {localidade: {$eq: 'Bronx'}}},{$count: "No of Restaurants in Bronx"}])
//309

#5 
//Apresente os primeiros 5 restaurantes localizados no Bronx.
db.rest.find( { localidade: { $eq: 'Bronx' }} ).limit(5)

#6 
//Liste todos os restaurantes que tenham pelo menos um score superior a 85.
db.rest.find({'grades.score' : {$gt: 85}})

#7
//Encontre os restaurantes que obtiveram uma ou mais pontuações (score) entre [80 e 100].
db.rest.find({$and: [{'grades.score' : {$gte: 80}},{'grades.score': {$lte: 100}}]})
//NOTA: Dizer ao stor, somewhy o AND nao esta a funcionar como devia, i.e, deu como output um restaurante que nao tem nenhum score no range

#8
//Indique os restaurantes com latitude inferior a -95,7.
db.rest.find({"address.coord.0": {$lt: -97.5}})

#9
//Indique os restaurantes que não têm gastronomia "American", tiveram uma (ou mais) pontuação superior a 70 e estão numa latitude inferior a -65.
db.rest.find({gastronomia: {$ne: "American"}, 'grades.score': {$gt: 70}, 'address.coord.0': {$lt: -65}})

#10
//Liste o restaurant_id, o nome, a localidade e gastronomia dos restaurantes cujo nome começam por "Wil".
db.rest.find({nome: {$regex: 'Wil*'}}, {restaurant_id: 1,nome: 1, localidade: 1, gastronomia: 1})

#11
// Liste o nome, a localidade e a gastronomia dos restaurantes que pertencem ao Bronx e cuja gastronomia é do tipo "American" ou "Chinese".
db.rest.find({ localidade: { $eq: 'Bronx' }, $or: [{gastronomia: { $eq: 'American' }},{gastronomia: { $eq: 'Chinese' }}]}, {nome: 1, localidade: 1, gastronomia: 1})

#12
//Liste o restaurant_id, o nome, a localidade e a gastronomia dos restaurantes localizados em "Staten Island", "Queens", "Bronx" ou "Brooklyn".
db.rest.find({$or: [{localidade: { $eq: 'Bronx' }}, {localidade: { $eq: 'Queens' }}, {localidade: { $eq: 'Staten Island' }}, {localidade: { $eq: 'Brooklyn' }}]}, {nome: 1, restaurant_id: 1, gastronomia:1, localidade: 1})

#13
//Liste o nome, a localidade, o score e gastronomia dos restaurantes que alcançaram sempre pontuações inferiores ou igual a 3.
db.rest.find({'grades.score': {$not: {$gt: 3}}},{nome: 1, 'grades.score': 1, gastronomia:1, localidade: 1})

#14
//Liste o nome e as avaliações dos restaurantes que obtiveram uma avaliação com um grade "A", um score 10 na data "2014-08-11T00: 00: 00Z" (ISODATE).
db.rest.find({'grades': {'$elemMatch': {grade: 'A', score: 10, date: ISODate("2014-08-11T00:00:00Z")}}},{'grades.grade': 1, nome: 1})

#15
//Liste o restaurant_id, o nome e os score dos restaurantes nos quais a segunda avaliação foi grade "A" e ocorreu em ISODATE "2014-08-11T00: 00: 00Z".
db.rest.find({'grades.1.grade': {$eq: 'A'}, 'grades.1.date': {$eq: ISODate("2014-08-11T00:00:00Z")}},{restaurant_id: 1, nome: 1, 'grades.score': 1})

#16
//Liste o restaurant_id, o nome, o endereço (address) e as coordenadas geográficas (coord) dos restaurantes onde o 2o elemento da matriz de coordenadas tem um valor superior a 42 e inferior ou igual a 52.
db.rest.find({$and: [{'address.coord.1': {$gt:42}},{'address.coord.1': {$lte:52}}]},{restaurant_id: 1, address: 1, nome: 1})

#17
//Liste o nome de todos os restaurantes por ordem crescente.
db.rest.find({},{nome: 1}).sort({nome: 1})

#18
//Liste nome, gastronomia e localidade de todos os restaurantes ordenando por ordem crescente da gastronomia e, em segundo, por ordem decrescente de localidade.
db.rest.find({},{nome: 1,gastronomia: 1, localidade: 1}).sort({gastronomia: 1, localidade: -1})

#19
//Liste nome, localidade, grade e gastronomia de todos os restaurantes localizados em Brooklyn que não incluem gastronomia "American" e obtiveram uma classificação (grade) "A". Deve apresentá-los por ordem decrescente de gastronomia.
db.rest.find({localidade: 'Brooklyn', gastronomia: {$ne: 'American'}},{nome: 1, localidade: 1, 'grades.grade': 1, gastronomia: 1}).sort({gastronomia: -1})

#20
//Conte o total de restaurante existentes em cada localidade.
db.rest.aggregate([{$group : { _id : '$localidade', no_restaurants : {$sum : 1}}}])

#21
//Liste todos os restaurantes cuja média dos score é superior a 30.
db.rest.aggregate([{$addFields : { average_score :  {$avg : '$grades.score'}}}, {$match : {average_score: {$gt: 30}}}])
//Note the usage of pipeline stages, first to get the average score and then to use it as a comparasion

#22
//Indique os restaurantes que têm gastronomia "American", o somatório de score é superior a 70 e estão numa latitude inferior a -65.
db.rest.aggregate([{$addFields : { total_score :  {$sum : '$grades.score'}}}, {$match : {total_score: {$gt: 70}, gastronomia: 'American', 'address.coord.0': {$lt: -65}}}])

#23
//Apresente uma lista com todos os tipos de gastronomia e o respetivo número de restaurantes, ordenada por ordem decrescente deste número.
db.rest.aggregate([{$group : { _id : '$gastronomia', no_restaurants : {$sum : 1}}}, {$sort: {no_restaurants: -1}}])

#24
//Apresente o número de gastronomias diferentes na rua "Flatbush Avenue"
db.rest.aggregate([{$match: {'address.rua': 'Flatbush Avenue'}},{$group: {'_id': '$gastronomia'}},{$count: "no_gastronomy"}])
// 9

#25
// Conte quantos restaurantes existem por rua e ordene por ordem decrescente
db.rest.aggregate([{$group : { _id : '$address.rua', no_restaurants : {$sum : 1}}}, {$sort: {no_restaurants: -1}}])

#26
// Quantos restaurantes italianos existem na Broadway?
db.rest.aggregate([{$match: {gastronomia: 'Italian', 'address.rua': 'Broadway'}},{$count: 'no_restaurants'}])
// 6

#27
// Liste o nome e score total de todos os restaurantes de comida Indiana com um score total menor que 15. 
db.rest.aggregate([{$addFields: {total_score: {$sum: '$grades.score'}}}, {$match: {'gastronomia': 'Indian', 'total_score': {$lt: 15}}}, {$group: {_id: '$_id', nome: {'$first': '$nome'}, 'total_score': {'$first': '$total_score'}}}])


#28
// Quantos restaurantes possuem 'Restaurant' no nome?
db.rest.aggregate([{$match: {nome: {$regex: 'Restaurant*'}}},{$count: 'no_restaurants'}])
//561

#29
// Indique qual a gastronomia mais comum
db.rest.aggregate([{$group : { _id : '$gastronomia', no_restaurants : {$sum : 1}}}, {$sort: {no_restaurants: -1}}, {$limit: 1}])
//American

#30
// Indique o score médio total de todos os restaurantes
db.rest.aggregate([{$addFields : { average_score :  {$avg : '$grades.score'}}}, {$group : {_id:null, average_score :  {$avg : '$average_score'}}}])
//+-11.17
```

## Server Side Functions

### a)
Start a mongo shell and input the following commands:
```
> load("<path to folder containing file>/populatePhones.js")
true

> populatePhones
function (country, start, stop) {

  var prefixes = [21, 22, 231, 232, 233, 234 ];
  for (var i = start; i <= stop; i++) {

    var prefix = prefixes[(Math.random() * 6) << 0]
    var countryNumber = (prefix * Math.pow(10, 9 - prefix.toString().length)) + i;
    var num = (country * 1e9) + countryNumber;
    var fullNumber = "+" + country + "-" + countryNumber;

    db.phones.insert({
      _id: num,
      components: {
        country: country,
        prefix: prefix,
        number: i
      },
      display: fullNumber
    });
    print("Inserted number " + fullNumber);
  }
  print("Done!");
}

> populatePhones(351, 1, 5)
Inserted number +351-220000001
Inserted number +351-220000002
Inserted number +351-220000003
Inserted number +351-220000004
Inserted number +351-210000005
Done!
```

Somethings to note are the fact that we're not actually adding any data to any database, our data is being stored "in shell" and not in the server and the fact that this can probably also be done using Robo3T rather than the shell, but I'm not really sure how to so...meh


### b)
Simply run the following commands (note that the first one is used to drop the data we inserted into the shell in exercise a) )

```
> db.phones.drop()
true
> populatePhones(351, 1, 200000)
(...)
Inserted number +351-220199995
Inserted number +351-220199996
Inserted number +351-232199997
Inserted number +351-232199998
Inserted number +351-234199999
Inserted number +351-210200000
Done!

//And now to test if it worked
> db.phones.find().count()
200000

> db.phones.find({"components.country": 351})
{ "_id" : 351220000001, "components" : { "country" : 351, "prefix" : 22, "number" : 1 }, "display" : "+351-220000001" }
{ "_id" : 351231000002, "components" : { "country" : 351, "prefix" : 231, "number" : 2 }, "display" : "+351-231000002" }
{ "_id" : 351232000003, "components" : { "country" : 351, "prefix" : 232, "number" : 3 }, "display" : "+351-232000003" }
{ "_id" : 351231000004, "components" : { "country" : 351, "prefix" : 231, "number" : 4 }, "display" : "+351-231000004" }
{ "_id" : 351220000005, "components" : { "country" : 351, "prefix" : 22, "number" : 5 }, "display" : "+351-220000005" }
{ "_id" : 351220000006, "components" : { "country" : 351, "prefix" : 22, "number" : 6 }, "display" : "+351-220000006" }
{ "_id" : 351210000007, "components" : { "country" : 351, "prefix" : 21, "number" : 7 }, "display" : "+351-210000007" }
{ "_id" : 351231000008, "components" : { "country" : 351, "prefix" : 231, "number" : 8 }, "display" : "+351-231000008" }
{ "_id" : 351234000009, "components" : { "country" : 351, "prefix" : 234, "number" : 9 }, "display" : "+351-234000009" }
{ "_id" : 351232000010, "components" : { "country" : 351, "prefix" : 232, "number" : 10 }, "display" : "+351-232000010" }
{ "_id" : 351232000011, "components" : { "country" : 351, "prefix" : 232, "number" : 11 }, "display" : "+351-232000011" }
{ "_id" : 351232000012, "components" : { "country" : 351, "prefix" : 232, "number" : 12 }, "display" : "+351-232000012" }
{ "_id" : 351232000013, "components" : { "country" : 351, "prefix" : 232, "number" : 13 }, "display" : "+351-232000013" }
{ "_id" : 351231000014, "components" : { "country" : 351, "prefix" : 231, "number" : 14 }, "display" : "+351-231000014" }
{ "_id" : 351220000015, "components" : { "country" : 351, "prefix" : 22, "number" : 15 }, "display" : "+351-220000015" }
{ "_id" : 351232000016, "components" : { "country" : 351, "prefix" : 232, "number" : 16 }, "display" : "+351-232000016" }
{ "_id" : 351231000017, "components" : { "country" : 351, "prefix" : 231, "number" : 17 }, "display" : "+351-231000017" }
{ "_id" : 351210000018, "components" : { "country" : 351, "prefix" : 21, "number" : 18 }, "display" : "+351-210000018" }
{ "_id" : 351234000019, "components" : { "country" : 351, "prefix" : 234, "number" : 19 }, "display" : "+351-234000019" }
{ "_id" : 351231000020, "components" : { "country" : 351, "prefix" : 231, "number" : 20 }, "display" : "+351-231000020" }
Type "it" for more

```

### c)
Create a new file with the following query JS:

```
phonesPerPrefix  =  function () {

return  db.phones.aggregate([{$group: {_id:  "$components.prefix", no_phones: {$sum:  1}}}, {$sort: {no_phones:  -1}}])

}
```

And now lets test it in our shell:
```
> load("phonesPerPrefix.js")
true

> phonesPerPrefix()
{ "_id" : 21, "no_phones" : 33449 }
{ "_id" : 231, "no_phones" : 33381 }
{ "_id" : 234, "no_phones" : 33337 }
{ "_id" : 232, "no_phones" : 33309 }
{ "_id" : 22, "no_phones" : 33276 }
{ "_id" : 233, "no_phones" : 33248 }
```

### d)
Choosing to make a function that finds all numbers with non-repeating digits, we get the function:

```
findNonRepeatingDigits  =  function () {

	var  fullNumber  =  db.phones.find({},{"display":  1, "_id":  0}).toArray();

	var  non_repeating_numbers  = []

	for (var  i  =  0 ; i<fullNumber.length ; i++){
		var  number  =  fullNumber[i].display
		number  =  number.split("-")[1]

		var  arr  = []
		var  non_repeating  =  true

  

		for(var  j  =  0 ; j<number.length ; j++){
			if (arr.includes(number[j])){
				non_repeating  =  false
				break
			}

			arr.push(number[j])

		}

		if (non_repeating){
			non_repeating_numbers.push(fullNumber[i])
		}

	}
	return  non_repeating_numbers
}
```

Which we can test in the terminal like so:
```
> load("findNonRepeatingDigits.js")
true
> findNonRepeatingDigits()
[ (...)
	{
		"display" : "+351-234196750"
	},
	{
		"display" : "+351-234197058"
	},
	{
		"display" : "+351-234197506"
	},
	{
		"display" : "+351-234197508"
	},
	{
		"display" : "+351-234197568"
	},
	{
		"display" : "+351-234197680"
	},
	{
		"display" : "+351-234197850"
	},
	{
		"display" : "+351-234197865"
	},
	{
		"display" : "+351-234198076"
	},
	{
		"display" : "+351-234198650"
	},
	{
		"display" : "+351-234198756"
	}
]
//Note this is the output we get if we have 200 000 numbers in our db
```

## MongoDB Driver
### Setup
-	Pick one of the following drivers (I used python):
-https://docs.mongodb.com/ecosystem/drivers/

-	Installing the Python Driver:
`$ sudo pip3 install pymongo`

### a)
```
from pymongo import  *

from datetime import datetime 

CLIENT = MongoClient()


def  insert_document(collection, new_doc):
	try:
		inserted_id = collection.insert_one(new_doc).inserted_id
		print("Success!\n >",inserted_id,"\n")

	except  Exception  as e:
		print("Error: ", e)
		print("No new document was inserted!\n")

def  update_documents(collection, update_query, update_values):
	try:
		update_count = collection.update_many(update_query, update_values).modified_count
		print("Success!\n >",update_count, " documents updated\n")
		
	except  Exception  as e:
		print("Error: ", e)
		print("No document was updated!\n")

def  search_by_query(collection, search_query):
	try:
		for document in collection.find(search_query):
		print(" >",document,"\n")

	except  Exception  as e:
		print("Error: ", e)
		print("Couldn't search for any document!\n")



def  main(db_name, collection_name):
	db = CLIENT[db_name]
	collection = db[collection_name]

	insert_document(collection, {"address": {"building": "69420", "coord": [-69.0, 420.696969], "rua": "Some Street", "zipcode": "42069"}, "localidade": "Sta Maria da Feira", "gastronomia": "Italian", "grades": [{"date": datetime(2019, 6, 12, 0, 0), "grade": "A", "score": 69}, {"date": datetime(2017, 7, 7, 0, 0), "grade": "B", "score": 100}], "nome": "Fierabella", "restaurant_id": "69696969"})

	update_documents(collection,{"localidade": "Sta Maria da Feira"},{"$set": {"rua": "Ao pe do castelo"}})

	search_by_query(collection,{"gastronomia": "Italian"})

if  __name__  ==  '__main__':
	main("cbd", "rest")
```


### b)
Incremented from the code in the last exercise
```
def  create_new_index(collection,index,name):
	try:
		collection.create_index(index,name=name)

		for indexes in collection.index_information():
			print(" >",indexes,"\n")
	except  Exception  as e:
		print("Error: ", e)
		print("Couldn't creat the index!\n")

def main():
	(...)
	
	create_new_index(collection,"localidade","localidade")
	create_new_index(collection,"gastronomia","gastronomia")
	create_new_index(collection,[("nome",TEXT)],"nome")
```


### c)
Incremented from the code in the last exercise
```
def  count_rest_by_localidade(collection):
	try:
		result = collection.aggregate([{"$group": {"_id": "$localidade", "noRestaurants": {"$sum": 1}}}])
		return ["-> "  +  str(document["_id"]) +  " - "  +  str(document["noRestaurants"]) for document in  list(result)]
	except  Exception  as e:
		print("Error: ", e)
		print("Couldn't query collection!\n")

  
def  count_rest_by_localidade_by_gastronomy(collection):
	try:
		result = collection.aggregate([{"$group": {"_id": {"localidade": "$localidade","gastronomy": "$gastronomia"}, "noRestaurants": {"$sum": 1}}}])
		return ["-> "  +  str(document["_id"]["localidade"]) +  " | "  +  str(document["_id"]["gastronomy"]) +  " - "  +  str(document["noRestaurants"]) for document in  list(result)]
	except  Exception  as e:
		print("Error: ", e)
		print("Couldn't query collection!\n")
 

def  get_rest_with_name_closer_to(collection,name):
	try:
		result = collection.aggregate([{"$match": {"nome": {"$regex": name}}}])
		return ["-> "  +  str(document["nome"]) for document in  list(result)]
	except  Exception  as e:
		print("Error: ", e)
		print("Couldn't query collection!\n")


def main():
	(...)
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
```


# Freeform DB

## The Pokémon GO! Dataset
For this exercise I chose to use the Pokemon GO! Pokedéx Dataset, downloadable at https://raw.githubusercontent.com/Biuni/PokemonGO-Pokedex/master/pokedex.json. This json however came as a single document containing an array of all other documents so some slight editing was needed so I'd **recommend downloading the version I've included in the exercise's directory**
For more Datasets, I'd recommend Kaggle or https://github.com/jdorfman/awesome-json-datasets

Each document looks like this (note the use of arrays such as the one in the type field, and the array of subdocuments such as the one in the next_evolution field):
```
{
      "id": 1,
      "num": "001",
      "name": "Bulbasaur",
      "img": "http://www.serebii.net/pokemongo/pokemon/001.png",
      "type": [
        "Grass",
        "Poison"
      ],
      "height": 0.71,
      "weight":6.9 ,
      "candy": "Bulbasaur Candy",
      "candy_count": 25,
      "egg": "2 km",
      "spawn_chance": 0.69,
      "avg_spawns": 69,
      "spawn_time": "20:00",
      "multipliers": [
        1.58
      ],
      "weaknesses": [
        "Fire",
        "Ice",
        "Flying",
        "Psychic"
      ],
      "next_evolution": [
        {
          "num": "002",
          "name": "Ivysaur"
        },
        {
          "num": "003",
          "name": "Venusaur"
        }
      ]
    }
```

## Setup
Download the dataset file (should be a json) and run the following command:
`$ mongoimport --db cbd --collection pokedex --drop --file pokemon.json`

## Find Queries
```
#Search for all Fire Type Pokémons ordered by Pokedex Entry (id)
 > db.pokedex.find( { type: "Fire"} ).sort({"id":1})

#Search for all Pokémons with 2 or more evolutions (next_evolution)
 > db.pokedex.find( {'next_evolution.1': {$exists: true}} )

#Find all candies (candy) of first evolution Pokémons (prev_evolution) sorted alphabetically
 > db.pokedex.find({'prev_evolution': {$exists: false}},{"_id": 0, candy: 1}).sort({"candy": 1})

#Find all Pokémon weak against Psychic types that have a spawn chance bigger than 0.2
 > db.pokedex.find({'weaknesses': 'Psychic', 'spawn_chance': {$gt: 0.2}})

#Find all Pokémon with a height between 5 and 20 meters sorted in reverse by name
 > db.pokedex.find( {$and: [ {'height': {$gte: 5}}, {'height': {$lte: 20}}] }).sort({"name": -1})

#Find all Pokémon that come from an egg and whose weight is bigger than 10kg. Show only the Pokémons Name and Pokédex ID (id)
 > db.pokedex.find({'weight': {$gt: 10}, 'egg': {$ne: "Not in Eggs"} },{"_id": 0, "name": 1, "id": 1})

#Queries extra para melhoria:
#Find all Pokemon who can eventually evolve into Victreebell (i.e all pokemon who have Weepinbell in their evolution tree) (and format it using pretty)
 > db.getCollection('pokedex').find({ 'next_evolution.name': 'Victreebel' }).pretty()

#Find all Pokemon whose previous evolution has an id higher than 100
 > db.getCollection('pokedex').find({ 'prev_evolution.num': /^1/})

#Find all Pokemon whose name starts with Char and show only their name
 > db.getCollection('pokedex').find({ 'name': {$regex: /^Char/}}, {_id: 0, name:1})

#Find all Pokemon weak to both Ice and Electric
 > db.getCollection('pokedex').find({'weaknesses': { $all: ["Ice", "Electric"] }})

#Find all Pokemon weak only to Psychich and  Ground
 > db.getCollection('pokedex').find({$or: [ {'weaknesses': ["Ground","Psychic"]}, {'weaknesses': ["Psychic", "Ground"]}]})
```


## Aggregate Queries
```
#Count how many Fighting type Pokémons exist who're also weak to Water
 > db.pokedex.aggregate([{$match : { "type" : "Fighting", "weaknesses" : "Flying"}}, {$count: "fighting_weak_to_water"}])

#List the average height, weight and spawn chance for all Pokémon
db.pokedex.aggregate([{$group : { "_id" : 0, avg_height : {"$avg": "$height"}, avg_weight: {"$avg": "$weight"},avg_spawn: {"$avg": "$spawn_chance"}}}])

#List how many Pokémon of each Types there are
 > db.pokedex.aggregate([{$unwind: '$type'},{$group : { _id : '$type', count : {$sum : 1}}}])

#What's the most common weakness?
 > db.pokedex.aggregate([{$unwind: '$weaknesses'},{$group : { _id : '$weaknesses', count : {$sum : 1}}}, {$sort: {count: -1}}, {$limit: 1}])

#Count how many pokemon have 'Pid' in the name
 > db.pokedex.aggregate([{$match: {name: {$regex: 'Pid'}}},{$count: 'no_pokemon_with_pid'}])

#How many evolutions does each Water type Pokémon have?
db.pokedex.aggregate([{$match: {$and: [{prev_evolution: {$exists: false}},{next_evolution: {$exists: true}}, {type: 'Water'}]}}, {$project: {counter: {$size: "$next_evolution"}}}])

#Count the ammount of Pokémon that come from eggs and have exactly 2 types
 > db.pokedex.aggregate([{$match: {type: {$size: 2}}},{$count: 'no_pokeom_egg_multitype'}])

#How many Pokémon with no evolutions don't come from eggs?
 > db.pokedex.aggregate([{$match: {$and: [{egg: "Not in Eggs"}, {prev_evolution: {$exists: false}}, {next_evolution: {$exists: false}}]}},{$count: 'no_pokemon'}])

#Queries extra para melhoria:
#Get 3 random Flying Pokemon
 > db.pokedex.aggregate([{$match: {'type': 'Flying'}}, {$sample: {size: 3}}])

#Get all info on all of Charmander's Evolutions
# To do this, first we create a new collection with all of Charmander's next_evolution subdocuments
 > db.pokedex.aggregate([{$match: {'name':'Charmander'}}, {$unwind: '$next_evolution'}, {$group : { _id : '$next_evolution.num', name: { "$first": "$next_evolution.name" }}}, { $out : "charmanderevolutions" }])

# Now we can perfrom a left outer join to between our two collections
 > db.pokedex.aggregate([ {$lookup: {from: "charmanderevolutions", localField: "name", foreignField: "name", as: "evolution"} }, { $unwind: "$evolution" }])
``` 

