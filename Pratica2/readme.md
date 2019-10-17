# Prática CBD - 2

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
To search for a specific Document, you can just put one of the document's fields in the find() method, like so:
```
>db.testcollection.find({"_id":0})
{ "_id" : 0, "name" : "DS", "description" : "Hey demons, it's me, ya boi", "team": "Pirocanhoes" }

>db.testcollection.find({"name": "Chico com Ch"})
{ "_id" : 2, "name" : "Chico com Ch", "description" : "Minimeu", "team": "FTW" }
```

You can also pass multiple keys and mix them with **AND** and/or **OR** like so:
```
> db.testcollection.find({$or: [{team: "Pirocanhoes"},{team: "FTW"}]})
{ "_id" : 0, "name" : "DS", "description" : "Hey", "team" : "Pirocanhoes" }
{ "_id" : 1, "name" : "Andre", "description" : "acoreano", "team" : "Pirocanhoes" }
{ "_id" : 2, "name" : "Chico", "description" : "minimeu", "team" : "FTW" }

> db.testcollection.find({$and: [{team: "Pirocanhoes"},{name: "DS"}]})
{ "_id" : 0, "name" : "DS", "description" : "Hey", "team" : "Pirocanhoes" }
```

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

## Types & Arrays
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

## Aggregations & Mapreduces

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
