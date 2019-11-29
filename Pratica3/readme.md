
# Prática CBD - 3

# Index
- [Initial Configurations](#initial-configurations)
- [Initial Cassandra Interactions](#initial-cassandra-interactions)
- [Cassandra - Video Sharing System](#cassandra-video-sharing-system)
- [Cassandra Driver](#cassandra-driver)
- [Free Theme DB - Shop Stock and Sales](#free-theme-db-shop-stock-and-sales)

# Initial Configurations
Checkout http://cassandra.apache.org/download/

Note:
An issue kept ocurring during the installation problem where Cassandra wouldn't be able to start due to permission errors. 
This was fixed by:
1. First running Cassandra in sudo (which is not recommended)
	```
	$sudo cassandra -f -R
	```
2. Then inputting the following commands:
	```
	$sudo chown -R $USER:$GROUP /var/lib/cassandra
	$sudo chown -R $USER:$GROUP /var/log/cassandra
	```

Alternatively, instead of running Cassandra in sudo on the first time, you could just create the folders manually:
```
sudo mkdir /var/lib/cassandra
sudo mkdir /var/log/cassandra
```

### Starting Cassandra
``` 
$ cassandra -f
```
### Stopping Cassandra
``` 
$ sudo service cassandra stop
```
### Verify that Cassandra is working
``` 
$ nodetool status
```
### Booting up the Cassandra shell ( ͡° ͜ʖ ͡°) 
``` 
$ cqlsh
```

# Initial Cassandra Interactions
For more information visit https://www.tutorialspoint.com/cassandra/cassandra_introduction.htm

## Data Model
### Cluster

> The Cassandra database is distributed over several machines that operate together. The outermost container is known as the Cluster. For failure handling, every node contains a replica, and in case of a failure, the replica takes charge. Cassandra arranges the nodes in a cluster, in a ring format, and assigns data to them.

### Keyspace

> Keyspace is the outermost container for data in Cassandra. The basic attributes of a Keyspace in Cassandra are:
>
> -   **Replication factor** − It is the number of machines in the cluster that will receive copies of the same data.
>    
>-   **Replica placement strategy** − It is nothing but the strategy to place replicas in the ring. We have strategies such as **simple strategy** (rack-aware strategy), **old network topology strategy** (rack-aware strategy), and **network topology strategy** (datacenter-shared strategy).
>    
>-   **Column families** − Keyspace is a container for a list of one or more column families. A column family, in turn, is a container of a collection of rows. Each row contains ordered columns. Column families represent the structure of your data. Each keyspace has at least one and often many column families.


![Keyspace - Column Family - Column](https://i.imgur.com/KqVCt68.png)
### Column Family

> A column family is a container for an ordered collection of rows. Each row, in turn, is an ordered collection of columns. The following table lists the points that differentiate a column family from a table of relational databases.
> 
> Note that unlike relational tables where a column family’s schema is not fixed, Cassandra does not force individual rows to have all the columns.
> 
> A Cassandra column family has the following attributes:
>
>-   **keys_cached** − It represents the number of locations to keep cached per SSTable.
  >  
>-   **rows_cached** − It represents the number of rows whose entire contents will be cached in memory.
>    
>-   **preload_row_cache** − It specifies whether you want to pre-populate the row cache.

![Column Family](https://i.imgur.com/9vItD7U.png)
### Column

> A column is the basic data structure of Cassandra with three values, namely key or column name, value, and a time stamp. Given below is the structure of a column.


## Cassandra vs Relational DBs
![Cassandra vs RDBMS](https://i.imgur.com/ewKGb33.png)

## Cassandra's Native Data Types
![Native Data Types](https://i.imgur.com/1to8qtt.png)

## Some Commands

### Keyspace:
#### Creating, Listing and Switching to a Keyspace
This command is used to create and switch to a new DB

Syntax:
```
CREATE KEYSPACE <identifier> WITH <properties>
```
The < properties > tag includes: 
-	**replication**
	-	Specifies the amount of replicas wanted and the Replica Placement Strategy
-	**durable_writes**
	-	Set to True by default

Usage:
```
CREATE KEYSPACE KeySpace Name
WITH replication = {'class': ‘Strategy name’, 'replication_factor' : ‘No.Of  replicas’}

AND durable_writes = true/false
```

Example:
```
cqlsh> CREATE KEYSPACE cbd_tutorial
   ... WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 3};


cqlsh> DESCRIBE keyspaces;

system_schema  system              system_traces
system_auth    system_distributed  cbd_tutorial 


cqlsh> USE cbd_tutorial;
cqlsh:cbd_tutorial> 
```
Note the use of :
-	`DESCRIBE keyspaces`
	-	In order to list all of the existing keyspaces.
-	`USE cbd_tutorial` 
	-	In order to switch to our newly created Keyspace


#### Altering a Keyspace
This command is used to alter the properties of a Keyspace

Syntax:
```
ALTER KEYSPACE <identifier> WITH <properties>
```

Usage:
```
ALTER KEYSPACE KeySpace_Name
WITH replication = {'class': ‘Strategy name’, 'replication_factor' : ‘No.Of  replicas’};
AND DURABLE_WRITES = true/false;
```

Example:
```
cqlsh:cbd_tutorial> ALTER KEYSPACE cbd_tutorial WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 5};
```

#### Dropping a Keyspace
This command is used to drop a Keyspace

Syntax:
```
DROP KEYSPACE <identifier>
```

Usage:
```
DROP KEYSPACE KeySpace_name
```

Example:
```
cqlsh> DROP KEYSPACE cbd_tutorial;

cqlsh> DESCRIBE keyspaces;

system_schema  system_auth  system  system_distributed  system_traces
```

### Column Family and Column:
#### Creating a Column Family and Defining a Column
This command is used to insert a new Column Family (also referred to as Table) to the current Keyspace

Syntax - Create a Column Family:
```
CREATE (TABLE | COLUMNFAMILY) <tablename>
('<column-definition>' , '<column-definition>')
(WITH <option> AND <option>)
```

Note how we have to define our columns. This can be done with the following command:

Syntax - Define Columns:
```
name1 data_type,
name2 data_type,
...
nameN data_type PRIMARY KEY
```

Note the use of **Primary Key**:
> The primary key is a column that is used to uniquely identify a row. Therefore,defining a primary key is mandatory while creating a table. A primary key is made of one or more columns of a table.

There are some particularities to Cassandra's Primary Key that are worth pointing out:
-	The Key is composed off of 2 Sub-Keys:
	-	**Partitioning Key**
		-	Obligatory
		-	Used to specify how table rows are distributed among partitions
	-	**Clustering Key**
		-	Optional
		-	Defines the clustering order, i.e. how table rows are locally stored within a partition
		-	
![enter image description here](https://i.imgur.com/SxoFTfB.png)

Usage:
```
CREATE COLUMNFAMILY / TABLE tablename(
   column1 name datatype PRIMARYKEY,
   column2 name data type,
   column3 name data type.
)

or

CREATE COLUMNFAMILY / TABLE tablename(
   column1 name datatype,
   column2 name data type,
   column3 name data type,
   PRIMARY KEY (column1)
)
```

Example:
```
cqlsh:cbd_tutorial> CREATE COLUMNFAMILY player(
                ... player_id int PRIMARY KEY,
                ... player_name text,
                ... player_age int,
                ... player_rank int
                ... );
                
cqlsh:cbd_tutorial> select * from players;

 player_id | player_age | player_name | player_rank
-----------+------------+-------------+-------------

(0 rows)
```
Note the use of :
-	`select * from players`
	-	A query used to list all rows from a given column family

#### Altering a Column Family
This command is used to alter a given Column Family, either by **ADDING** or **DROPPING** columns

Syntax:
```
ALTER (TABLE | COLUMNFAMILY) <tablename> <instruction>
```

Usage:
```
ALTER COLUMNFAMILY / TABLE table_name
ADD  new_column datatype;

ALTER COLUMNFAMILY / TABLE table_name
DROP column_name;
```

Example:
```
cqlsh:cbd_tutorial> ALTER TABLE player
                ... DROP player_rank;
cqlsh:cbd_tutorial> ALTER COLUMNFAMILY player
                ... ADD player_score double;
cqlsh:cbd_tutorial> SELECT * FROM player;

 player_id | player_age | player_name | player_score
-----------+------------+-------------+--------------

(0 rows)
```


#### Dropping a Column Family
This command can be used to Drop a Column Family

Syntax:
```
DROP TABLE|COLUMNFAMILY <tablename>
```

Usage:
```
DROP COLUMNFAMILY/TABLE table_name;
```

Example:
```
cqlsh:cbd_tutorial> DROP COLUMNFAMILY player;

cqlsh:cbd_tutorial> DESCRIBE COLUMNFAMILIES;

<empty>
```

#### Truncating a Column Family
Using this command will delete all rows  from a given Column Family PERMANENTLY!

Syntax:
```
TRUNCATE <tablename>
```

Usage:
```
TRUNCATE table_name;
```

Example:
```
cqlsh:cbd_tutorial> TRUNCATE player;

cqlsh:cbd_tutorial> SELECT * from player;

 player_id | player_age | player_name | player_score
-----------+------------+-------------+--------------

(0 rows)

```

### CRUD Operations
#### CREATING Data 
The following command allows for the insertion of data into the columns of a row in a Column Family

Syntax:
```
INSERT INTO <tablename>
(<column1 name>, <column2 name>....)
VALUES (<value1>, <value2>....)
USING <option>
```

Example:
```
cqlsh:cbd_tutorial> SELECT * from player;

 player_id | player_age | player_name | player_score
-----------+------------+-------------+--------------

(0 rows)

cqlsh:cbd_tutorial> INSERT INTO player (player_id, player_age, player_name, player_score)
                ... VALUES (1, 20, 'DS', 69);
cqlsh:cbd_tutorial> INSERT INTO player (player_id, player_name, player_score)
                ... VALUES (2, 'Chico Ace', 80.420);
cqlsh:cbd_tutorial> INSERT INTO player (player_id, player_name)
                ... VALUES (3, 'Açores');
                
cqlsh:cbd_tutorial> SELECT * FROM player;

 player_id | player_age | player_name | player_score
-----------+------------+-------------+--------------
         1 |         20 |          DS |           69
         2 |       null |   Chico Ace |        80.42
         3 |       null |      Açores |         null

(3 rows)
```

#### UPDATING Data 
The following command allows you to update data in a Column Family

Syntax:
```
UPDATE <tablename>
SET <column name> = <new value>
<column name> = <value>....
WHERE <condition>
```
Where:
-	**SET**:
	-	The name of the column we want to alter and it's new value
-	**WHERE**:
	-	Used to select the specific row to be modified

Example:
```
cqlsh:cbd_tutorial> SELECT * FROM player;

 player_id | player_age | player_name | player_score
-----------+------------+-------------+--------------
         1 |         20 |          DS |           69
         2 |       null |   Chico Ace |        80.42
         3 |       null |      Açores |         null

(3 rows)

cqlsh:cbd_tutorial> UPDATE player
                ... SET player_score = 100.01
                ... WHERE player_id = 3;

cqlsh:cbd_tutorial> UPDATE player
                ... SET player_age = 19
                ... WHERE player_name = 'Chico Ace';
InvalidRequest: Error from server: code=2200 [Invalid query] message="Some partition key parts are missing: player_id"

cqlsh:cbd_tutorial> UPDATE player
                ... SET player_age = 19
                ... WHERE player_id = 2 AND player_name = 'Chico Ace';
InvalidRequest: Error from server: code=2200 [Invalid query] message="Non PRIMARY KEY columns found in where clause: player_name "

cqlsh:cbd_tutorial> SELECT * FROM player;

 player_id | player_age | player_name | player_score
-----------+------------+-------------+--------------
         1 |         20 |          DS |           69
         2 |       null |   Chico Ace |        80.42
         3 |       null |      Açores |       100.01

(3 rows)
```
Note the errors present when we try to update without using the primary key!

This is because the **WHERE clause has some constrictions** that stem from the fact that Cassandra is
dealing with distributed data and aims to prevent inefficient queries:
- rows are spread around the cluster based on the hash of
the partition keys
- clustering key columns are used to cluster the data of a
partition, allowing a very efficient retrieval of rows

These restrictions include:
![enter image description here](https://i.imgur.com/W8uf4F6.png)

And some examples of valid and invalid WHERE clauses are: 
![enter image description here](https://i.imgur.com/sThBvip.png)![enter image description here](https://i.imgur.com/PbLhq9R.png)

#### DELETING a ROW 
The following command allows you to delete a row from a Column Family

Syntax:
```
DELETE FROM <identifier> WHERE <condition>;
```

Example:
```
cqlsh:cbd_tutorial> SELECT * FROM player;

 player_id | player_age | player_name | player_score
-----------+------------+-------------+--------------
         1 |         20 |          DS |           69
         2 |       null |   Chico Ace |        80.42
         3 |       null |      Açores |       100.01

(3 rows)

cqlsh:cbd_tutorial> DELETE FROM player
                ... WHERE player_id = 3;

cqlsh:cbd_tutorial> SELECT * FROM player;

 player_id | player_age | player_name | player_score
-----------+------------+-------------+--------------
         1 |         20 |          DS |           69
         2 |       null |   Chico Ace |        80.42

(2 rows)
```

#### DELETING a COLUMN 
The following command allows you to delete a column from a specific row in a Column Family

Syntax:
```
DELETE <col> FROM <identifier> WHERE <condition>;
```

Example:
```
cqlsh:cbd_tutorial> SELECT * FROM player;

 player_id | player_age | player_name | player_score
-----------+------------+-------------+--------------
         1 |         20 |          DS |           69
         2 |       null |   Chico Ace |        80.42

(2 rows)

cqlsh:cbd_tutorial> DELETE player_score FROM player WHERE player_id = 2;

cqlsh:cbd_tutorial> SELECT * FROM player;

 player_id | player_age | player_name | player_score
-----------+------------+-------------+--------------
         1 |         20 |          DS |           69
         2 |       null |   Chico Ace |         null

(2 rows)
```


#### READING  Data  
The following command allows you to read data from a Column Family

Syntax:
```
SELECT * | select_expression | DISTINCT partition 
FROM [keyspace_name.] table_name 
[WHERE partition_value
   [AND clustering_filters 
   [AND static_filters]]] 
[ORDER BY PK_column_name ASC|DESC] 
[LIMIT N]
[ALLOW FILTERING]
```
There are also extra clauses we can use with the SELECT:
-	**WHERE**:
	-	Used to specify conditionals of the data we want to gather
-	**GROUP BY**:
	-	Groups rows of a table according to certain columns
	-	Only groupings induced by primary key columns are allowed!
	-	When a non-grouping column is selected without an aggregate function the first value encountered is the only one returned
-	**ORDER BY**:
	-	Defines the order of the returned rows
	-	Can be ASC or DESC
	-	Partition key must be restricted (= or IN)
	-	Only orderings induced by clustering columns are allowed!
-	**LIMIT**:
	-	Limits the numbers of rows returned in the query result

Example:
```
cqlsh:cbd_tutorial> SELECT * FROM player;

 player_id | player_age | player_name | player_score
-----------+------------+-------------+--------------
         1 |         20 |          DS |           69
         2 |       null |   Chico Ace |         null

(2 rows)
cqlsh:cbd_tutorial> SELECT player_name FROM player;

 player_name
-------------
          DS
   Chico Ace

(2 rows)

cqlsh:cbd_tutorial> SELECT player_name FROM player
                ... LIMIT 1;

 player_name
-------------
          DS

(1 rows)

cqlsh:cbd_tutorial> SELECT player_name FROM player 
                ... WHERE player_id = 2;

 player_name
-------------
   Chico Ace

(1 rows)

cqlsh:cbd_tutorial> SELECT player_name FROM player  WHERE player_age > 10;
InvalidRequest: Error from server: code=2200 [Invalid query] message="Cannot execute this query as it might involve data filtering and thus may have unpredictable performance. If you want to execute this query despite the performance unpredictability, use ALLOW FILTERING"

cqlsh:cbd_tutorial> SELECT player_name FROM player  WHERE player_age > 10 ALLOW FILTERING;

 player_name
-------------
          DS

(1 rows)

cqlsh:cbd_tutorial> SELECT player_name FROM player  ORDER BY player_id DESC;
InvalidRequest: Error from server: code=2200 [Invalid query] message="ORDER BY is only supported when the partition key is restricted by an EQ or an IN."
```

Note the errors in the following queries:
-	`SELECT player_name FROM player  WHERE player_age > 10;`
	-	Happens due to the fact that player_age ISN'T part of the primary key
-	`SELECT player_name FROM player  ORDER BY player_id DESC;`
	-	Happens due to the fact that player_id isn't part of the Clustering Key (it's part of the Partitioning Key)

Also note how in `SELECT player_name FROM player  WHERE player_age > 10 ALLOW FILTERING;` only one row is returned despite both rows fulfilling our WHERE CONDITION.  This is due to the fact that player_age isn't a grouping attribute


# Cassandra - Video Sharing System

Notes: 
-	PK
	-	Primary Key
-	PT
	-	Partitioning Key
-	Cl
	-	Clustering Key
	
```mermaid
graph TB
A[User]
A_attrib_1((email PK_Pt)) --> A
A_attrib_2((username)) --> A
A_attrib_3((reg_timestamp)) --> A
A_attrib_4((name)) --> A

B[Video]
B_attrib_1((id PK_Pt)) --> B
B_attrib_2((author PK_Cl_1)) --> B
B_attrib_3((upload_timestamp PK_Cl_2)) --> B
B_attrib_4((name)) --> B
B_attrib_5((description)) --> B
B_attrib_6((Tags)) --> B
B ==Was posted by ==> A

C[Comment]
C_attrib_1((id PK_Pt_1)) --> C
C_attrib_2((video_id PK_PT_2)) --> C
C_attrib_3((author PK_PT_3)) --> C
C_attrib_4((comment)) --> C
C_attrib_5((upload_timestamp PK_Cl_1)) --> C

C ==Was posted in==> B
C ==Was posted by==> A

D[Followers]
D_attrib_1((user Pk_Pt_1)) --> D
D_attrib_2((video_id Pk_Pt_2)) --> D
D ==Has Several==> A
D ==Pertrains to==> B

E[Event]
E_attrib_1((id PK_Pt)) --> E
E_attrib_2((user PK_Cl_1)) --> E
E_attrib_3((video PK_Cl_2)) --> E
E_attrib_4((action)) --> E
E_attrib_5((real_timestamp)) --> E
E_attrib_6((video_timestamp)) --> E
E ==Has a==> A
E ==Refers to a==> B

F[Rating]
F_attrib_1((id PK_Pt)) --> F
F_attrib_2((video PK_Cl_1)) --> F
F_attrib_3((value)) --> F
F ==Pertrains to==> B
```

## DB Creation
### Step 1 - Create Keyspace
```
cqlsh> CREATE KEYSPACE cbd_video_sharing
   ... WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 3};
cqlsh> USE cbd_video_sharing ;
cqlsh:cbd_video_sharing> 
```

### Step 2 - Create Column Families
```
cqlsh:cbd_video_sharing> CREATE COLUMNFAMILY User 
		     ... ( 
		     ... email text, 
	      	     ... username text, 
		     ... name text, 
		     ... reg_timestamp timestamp, 
		     ... PRIMARY KEY(email) 
  		     ... );

cqlsh:cbd_video_sharing> CREATE COLUMNFAMILY Video (
		     ... (
		     ... id uuid, 
		     ... author text, 
		     ... name text, 
		     ... upload_timestamp timestamp, 		
		     ... description text, 
		     ... tags list<text>, 
		     ... PRIMARY KEY(id, author, upload_timestamp) 
		     ...)
		     WITH CLUSTERING ORDER BY (author ASC, upload_timestamp DESC);

cqlsh:cbd_video_sharing> CREATE TABLE Comment_per_author
                     ... (
                     ... id uuid,
                     ... video_id uuid,
                     ... author text,
                     ... comment text,
                     ... upload_timestamp timestamp,
                     ... PRIMARY KEY (author, upload_timestamp)
                     ... )
                     ... WITH CLUSTERING ORDER BY (upload_timestamp DESC);

cqlsh:cbd_video_sharing> CREATE TABLE Comment_per_video
                     ... (
                     ... id uuid,
                     ... video_id uuid,
                     ... author text,
                     ... comment text,
                     ... upload_timestamp timestamp,
                     ... PRIMARY KEY (video_id, upload_timestamp)
                     ... )
                     ... WITH CLUSTERING ORDER BY (upload_timestamp DESC);

cqlsh:cbd_video_sharing> CREATE COLUMNFAMILY Follower
                     ... (
                     ... user text,
                     ... video_id uuid,
                     ... PRIMARY KEY ((user, video_id))
                     ... );
                     
cqlsh:cbd_video_sharing> CREATE COLUMNFAMILY Event
                     ... (
                     ... id uuid,
                     ... user text,
                     ... video_id uuid,
                     ... action text,
                     ... real_timestamp timestamp,
                     ... video_timestamp int,
                     ... PRIMARY KEY((user, video_id), real_timestamp,video_timestamp)
                     ... ) WITH CLUSTERING ORDER BY (real_timestamp DESC);
      
cqlsh:cbd_video_sharing> CREATE COLUMNFAMILY Rating
                     ... (
                     ... id uuid,
                     ... video_id uuid,
                     ... value int,
                     ... PRIMARY KEY(video_id, id)
                     ... );      
                              
cqlsh:cbd_video_sharing> DESCRIBE COLUMNFAMILIES

comment  rating  folower  video  user  event
```

### Step 3 - Populating the Column Families
#### User
```
cqlsh:cbd_video_sharing> SELECT * FROM User;

 email | name | reg_timestamp | username
-------+------+---------------+----------

cqlsh:cbd_video_sharing> INSERT INTO User (email, name, reg_timestamp, username)
                     ... VALUES ('ds@test.com', 'DS', dateof(now()), 'FenixDS');
cqlsh:cbd_video_sharing> INSERT INTO User (email, name, reg_timestamp, username)
                     ... VALUES ('pedro@f.ag', 'Pedro', dateof(now()), 'EhHeHe');
cqlsh:cbd_video_sharing> INSERT INTO User (email, name, reg_timestamp, username)
                     ... VALUES ('clau@sof.pt', 'Claudia', dateof(now()), 'ClauSof');
cqlsh:cbd_video_sharing> INSERT INTO User (email, name, reg_timestamp, username)
                     ... VALUES ('user1@bot.com', 'Bot1', dateof(now()), 'TotsAHuman1');
cqlsh:cbd_video_sharing> INSERT INTO User (email, name, reg_timestamp, username)
                     ... VALUES ('user2@bot.com', 'Bot2', dateof(now()), 'TotsAHuman2');
cqlsh:cbd_video_sharing> INSERT INTO User (email, name, reg_timestamp, username)
                     ... VALUES ('user3@bot.com', 'Bot3', dateof(now()), 'TotsAHuman3');
cqlsh:cbd_video_sharing> INSERT INTO User (email, name, reg_timestamp, username)
                     ... VALUES ('user4@bot.com', 'Bot4', dateof(now()), 'TotsAHuman4');
cqlsh:cbd_video_sharing> INSERT INTO User (email, name, reg_timestamp, username)
                     ... VALUES ('user5@bot.com', 'Bot5', dateof(now()), 'TotsAHuman5');
cqlsh:cbd_video_sharing> INSERT INTO User (email, name, reg_timestamp, username)
                     ... VALUES ('user6@bot.com', 'Bot6', dateof(now()), 'TotsAHuman6');
cqlsh:cbd_video_sharing> INSERT INTO User (email, name, reg_timestamp, username)
                     ... VALUES ('user7@bot.com', 'Bot7', dateof(now()), 'TotsAHuman7');
cqlsh:cbd_video_sharing> INSERT INTO User (email, name, reg_timestamp, username)
                     ... VALUES ('user8@bot.com', 'Bot8', dateof(now()), 'TotsAHuman8');
cqlsh:cbd_video_sharing> INSERT INTO User (email, name, reg_timestamp, username)
                     ... VALUES ('user9@bot.com', 'Bot9', dateof(now()), 'TotsAHuman9');

cqlsh:cbd_video_sharing> SELECT * FROM User;

 email         | name    | reg_timestamp                   | username
---------------+---------+---------------------------------+-------------
 user8@bot.com |    Bot8 | 2019-11-22 17:39:08.183000+0000 | TotsAHuman8
 user1@bot.com |    Bot1 | 2019-11-22 17:38:08.901000+0000 | TotsAHuman1
 user5@bot.com |    Bot5 | 2019-11-22 17:38:47.956000+0000 | TotsAHuman5
 user2@bot.com |    Bot2 | 2019-11-22 17:38:26.935000+0000 | TotsAHuman2
   ds@test.com |      DS | 2019-11-22 17:06:22.870000+0000 |     FenixDS
 user9@bot.com |    Bot9 | 2019-11-22 17:39:15.906000+0000 | TotsAHuman9
 user4@bot.com |    Bot4 | 2019-11-22 17:38:41.588000+0000 | TotsAHuman4
 user6@bot.com |    Bot6 | 2019-11-22 17:38:55.227000+0000 | TotsAHuman6
   clau@sof.pt | Claudia | 2019-11-22 17:07:46.978000+0000 |     ClauSof
    pedro@f.ag |   Pedro | 2019-11-22 17:07:38.653000+0000 |      EhHeHe
 user7@bot.com |    Bot7 | 2019-11-22 17:39:01.912000+0000 | TotsAHuman7
 user3@bot.com |    Bot3 | 2019-11-22 17:38:34.554000+0000 | TotsAHuman3

(12 rows)
```

#### Video
```
cqlsh:cbd_video_sharing> SELECT * FROM Video;

 id | author | upload_timestamp | description | name | tags
----+--------+------------------+-------------+------+------

cqlsh:cbd_video_sharing> INSERT INTO Video (id, author, upload_timestamp, description, name, tags)
                     ... VALUES (now(), 'ds@test.com', dateof(now()), 'Me going to the Zoo', 'ZooTrip', ['Wholesome', 'Cute', '#First', 'Animals']);

cqlsh:cbd_video_sharing> INSERT INTO Video (id, author, upload_timestamp, description, name, tags)
                     ... VALUES (now(), 'ds@test.com', dateof(now()), 'Me getting an E Z Sixtuple Kill with Zenyatta', 'Exeperience my Orbs [TEAMKILL]', ['Overwatch', 'Gaming','Rekt', 'Gottem', 'EZ', 'Zenyatta']);

cqlsh:cbd_video_sharing> INSERT INTO Video (id, author, upload_timestamp, description, name, tags)
                     ... VALUES (now(), 'pedro@f.ag', dateof(now()), 'Why am I doing this?...', 'Watching every JonTron Video in one sitting', ['JonTron', 'Random','Why']);

cqlsh:cbd_video_sharing> INSERT INTO Video (id, author, upload_timestamp, description, name, tags)
                     ... VALUES (now(), 'ds@test.com', dateof(now()), 'I have made some poor life decisions', 'Watching some guy watch every JonTron video in one sitting', ['JonTron', 'Random','Why', 'Why2x', 'Gottem', 'Inception', '#intoodeep']);

cqlsh:cbd_video_sharing> INSERT INTO Video (id, author, upload_timestamp, description, name, tags)
                     ... VALUES (now(), 'user1@bot.com', dateof(now()), 'Hello, World!', 'Hi, Im Bot1', ['Greetings', 'TheFuture','Destroy', 'All', 'Humans']);

cqlsh:cbd_video_sharing> INSERT INTO Video (id, author, upload_timestamp, description, name, tags)
                     ... VALUES (now(), 'user2@bot.com', dateof(now()), 'Hello, World!', 'Hi, Im Bot2', ['Greetings', 'TheFuture','Destroy', 'All', 'Humans']);

cqlsh:cbd_video_sharing> INSERT INTO Video (id, author, upload_timestamp, description, name, tags)
                     ... VALUES (now(), 'user3@bot.com', dateof(now()), 'Hello, World!', 'Hi, Im Bot3', ['Greetings', 'TheFuture','Destroy', 'All', 'Humans']);

cqlsh:cbd_video_sharing> INSERT INTO Video (id, author, upload_timestamp, description, name, tags)
                     ... VALUES (now(), 'user4@bot.com', dateof(now()), 'Hello, World!', 'Hi, Im Bot4', ['Greetings', 'TheFuture','Destroy', 'All', 'Humans']);

cqlsh:cbd_video_sharing> INSERT INTO Video (id, author, upload_timestamp, description, name, tags)
                     ... VALUES (now(), 'user5@bot.com', dateof(now()), 'Hello, World!', 'Hi, Im Bot5', ['Greetings', 'TheFuture','Destroy', 'All', 'Humans']);

cqlsh:cbd_video_sharing> INSERT INTO Video (id, author, upload_timestamp, description, name, tags)
                     ... VALUES (now(), 'user6@bot.com', dateof(now()), 'Hello, World!', 'Hi, Im Bot6', ['Greetings', 'TheFuture','Destroy', 'All', 'Humans']);

cqlsh:cbd_video_sharing> INSERT INTO Video (id, author, upload_timestamp, description, name, tags)
                     ... VALUES (now(), 'user7@bot.com', dateof(now()), 'Hello, World!', 'Hi, Im Bot7', ['Greetings', 'TheFuture','Destroy', 'All', 'Humans']);

cqlsh:cbd_video_sharing> INSERT INTO Video (id, author, upload_timestamp, description, name, tags)
                     ... VALUES (now(), 'user8@bot.com', dateof(now()), 'Hello, World!', 'Hi, Im Bot8', ['Greetings', 'TheFuture','Destroy', 'All', 'Humans']);

cqlsh:cbd_video_sharing> INSERT INTO Video (id, author, upload_timestamp, description, name, tags)
                     ... VALUES (now(), 'user9@bot.com', dateof(now()), 'Hello, World!', 'Hi, Im Bot9', ['Greetings', 'TheFuture','Destroy', 'All', 'Humans']);

cqlsh:cbd_video_sharing> SELECT * FROM Video;

 id                                   | author        | upload_timestamp                | description                                   | name                                                       | tags
--------------------------------------+---------------+---------------------------------+-----------------------------------------------+------------------------------------------------------------+----------------------------------------------------------------------------
 8ab66c50-0d4f-11ea-9d48-0b1cc2ad2f9d | user1@bot.com | 2019-11-22 17:43:06.901000+0000 |                                 Hello, World! |                                                Hi, Im Bot1 |                     ['Greetings', 'TheFuture', 'Destroy', 'All', 'Humans']
 ac746c70-0d4f-11ea-9d48-0b1cc2ad2f9d | user6@bot.com | 2019-11-22 17:44:03.511000+0000 |                                 Hello, World! |                                                Hi, Im Bot6 |                     ['Greetings', 'TheFuture', 'Destroy', 'All', 'Humans']
 b4ce2e10-0d4f-11ea-9d48-0b1cc2ad2f9d | user8@bot.com | 2019-11-22 17:44:17.521000+0000 |                                 Hello, World! |                                                Hi, Im Bot8 |                     ['Greetings', 'TheFuture', 'Destroy', 'All', 'Humans']
 eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d |   ds@test.com | 2019-11-22 17:17:13.467000+0000 |          I have made some poor life decisions | Watching some guy watch every JonTron video in one sitting | ['JonTron', 'Random', 'Why', 'Why2x', 'Gottem', 'Inception', '#intoodeep']
 3ffcc5a0-0d4b-11ea-9d48-0b1cc2ad2f9d |   ds@test.com | 2019-11-22 17:12:23.546000+0000 |                           Me going to the Zoo |                                                    ZooTrip |                                 ['Wholesome', 'Cute', '#First', 'Animals']
 7d6a05b0-0d4b-11ea-9d48-0b1cc2ad2f9d |   ds@test.com | 2019-11-22 17:14:06.603000+0000 | Me getting an E Z Sixtuple Kill with Zenyatta |                             Exeperience my Orbs [TEAMKILL] |                ['Overwatch', 'Gaming', 'Rekt', 'Gottem', 'EZ', 'Zenyatta']
 a3bd96b0-0d4f-11ea-9d48-0b1cc2ad2f9d | user4@bot.com | 2019-11-22 17:43:48.891000+0000 |                                 Hello, World! |                                                Hi, Im Bot4 |                     ['Greetings', 'TheFuture', 'Destroy', 'All', 'Humans']
 9f217950-0d4f-11ea-9d48-0b1cc2ad2f9d | user3@bot.com | 2019-11-22 17:43:41.157000+0000 |                                 Hello, World! |                                                Hi, Im Bot3 |                     ['Greetings', 'TheFuture', 'Destroy', 'All', 'Humans']
 990b8d30-0d4f-11ea-9d48-0b1cc2ad2f9d | user2@bot.com | 2019-11-22 17:43:30.947000+0000 |                                 Hello, World! |                                                Hi, Im Bot2 |                     ['Greetings', 'TheFuture', 'Destroy', 'All', 'Humans']
 b930ebf0-0d4f-11ea-9d48-0b1cc2ad2f9d | user9@bot.com | 2019-11-22 17:44:24.879000+0000 |                                 Hello, World! |                                                Hi, Im Bot9 |                     ['Greetings', 'TheFuture', 'Destroy', 'All', 'Humans']
 b0cca300-0d4f-11ea-9d48-0b1cc2ad2f9d | user7@bot.com | 2019-11-22 17:44:10.800000+0000 |                                 Hello, World! |                                                Hi, Im Bot7 |                     ['Greetings', 'TheFuture', 'Destroy', 'All', 'Humans']
 a856a6d0-0d4f-11ea-9d48-0b1cc2ad2f9d | user5@bot.com | 2019-11-22 17:43:56.605000+0000 |                                 Hello, World! |                                                Hi, Im Bot5 |                     ['Greetings', 'TheFuture', 'Destroy', 'All', 'Humans']
 bc1bd3b0-0d4b-11ea-9d48-0b1cc2ad2f9d |    pedro@f.ag | 2019-11-22 17:15:51.787000+0000 |                       Why am I doing this?... |                Watching every JonTron Video in one sitting |                                               ['JonTron', 'Random', 'Why']

(13 rows)
```

#### Comment
```
cqlsh:cbd_video_sharing> SELECT * FROM Comment_per_video;

 video_id | upload_timestamp | author | comment | id
----------+------------------+--------+---------+----

(0 rows)

cqlsh:cbd_video_sharing> SELECT * FROM Comment_per_author ;

 author | upload_timestamp | comment | id | video_id
--------+------------------+---------+----+----------

(0 rows)

cqlsh:cbd_video_sharing> INSERT INTO comment_per_author (id, video_id, author, comment, upload_timestamp) VALUES ( now(), eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d, 'ds@test.com', 'FIRST', dateof(now())) ;
cqlsh:cbd_video_sharing> INSERT INTO comment_per_author (id, video_id, author, comment, upload_timestamp) VALUES ( now(), eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d, 'ds@test.com', 'Also Second :)', dateof(now()));
cqlsh:cbd_video_sharing> INSERT INTO comment_per_author (id, video_id, author, comment, upload_timestamp) VALUES ( now(), eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d, 'user1@bot.com', 'Hello DS', dateof(now()));
cqlsh:cbd_video_sharing> INSERT INTO comment_per_author (id, video_id, author, comment, upload_timestamp) VALUES ( now(), eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d, 'user2@bot.com', 'Hello DS', dateof(now()));
cqlsh:cbd_video_sharing> INSERT INTO comment_per_author (id, video_id, author, comment, upload_timestamp) VALUES ( now(), eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d, 'user3@bot.com', 'Hello DS', dateof(now()));
cqlsh:cbd_video_sharing> INSERT INTO comment_per_author (id, video_id, author, comment, upload_timestamp) VALUES ( now(), eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d, 'ds@test.com', 'Wait wtf?', dateof(now()));
cqlsh:cbd_video_sharing> INSERT INTO comment_per_author (id, video_id, author, comment, upload_timestamp) VALUES ( now(), eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d, 'user4@bot.com', 'Hello DS', dateof(now()));
cqlsh:cbd_video_sharing> INSERT INTO comment_per_author (id, video_id, author, comment, upload_timestamp) VALUES ( now(), eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d, 'user5@bot.com', 'Hello DS', dateof(now()));
cqlsh:cbd_video_sharing> INSERT INTO comment_per_author (id, video_id, author, comment, upload_timestamp) VALUES ( now(), eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d, 'ds@test.com', 'WHATS HAPPENING', dateof(now()));
cqlsh:cbd_video_sharing> INSERT INTO comment_per_author (id, video_id, author, comment, upload_timestamp) VALUES ( now(), eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d, 'user6@bot.com', 'Hello DS', dateof(now()));
cqlsh:cbd_video_sharing> INSERT INTO comment_per_author (id, video_id, author, comment, upload_timestamp) VALUES ( now(), 7d6a05b0-0d4b-11ea-9d48-0b1cc2ad2f9d, 'clau@sof.pt', 'Friggin Pleb', dateof(now()));
cqlsh:cbd_video_sharing> INSERT INTO comment_per_author (id, video_id, author, comment, upload_timestamp) VALUES ( now(), 7d6a05b0-0d4b-11ea-9d48-0b1cc2ad2f9d, 'user9@bot.com', 'Us Bots couldve done better', dateof(now()));
cqlsh:cbd_video_sharing> INSERT INTO comment_per_author (id, video_id, author, comment, upload_timestamp) VALUES ( now(), 3ffcc5a0-0d4b-11ea-9d48-0b1cc2ad2f9d , 'pedro@f.ag', 'WTF Dude did you actually?!', dateof(now()));

cqlsh:cbd_video_sharing> INSERT INTO comment_per_video (id, video_id, author, comment, upload_timestamp) VALUES ( now(), eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d, 'ds@test.com', 'FIRST', dateof(now())) ;
cqlsh:cbd_video_sharing> INSERT INTO comment_per_video (id, video_id, author, comment, upload_timestamp) VALUES ( now(), eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d, 'ds@test.com', 'Also Second :)', dateof(now()));
cqlsh:cbd_video_sharing> INSERT INTO comment_per_video (id, video_id, author, comment, upload_timestamp) VALUES ( now(), eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d, 'user1@bot.com', 'Hello DS', dateof(now()));
cqlsh:cbd_video_sharing> INSERT INTO comment_per_video (id, video_id, author, comment, upload_timestamp) VALUES ( now(), eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d, 'user2@bot.com', 'Hello DS', dateof(now()));
cqlsh:cbd_video_sharing> INSERT INTO comment_per_video (id, video_id, author, comment, upload_timestamp) VALUES ( now(), eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d, 'user3@bot.com', 'Hello DS', dateof(now()));
cqlsh:cbd_video_sharing> INSERT INTO comment_per_video (id, video_id, author, comment, upload_timestamp) VALUES ( now(), eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d, 'ds@test.com', 'Wait wtf?', dateof(now()));
cqlsh:cbd_video_sharing> INSERT INTO comment_per_video (id, video_id, author, comment, upload_timestamp) VALUES ( now(), eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d, 'user4@bot.com', 'Hello DS', dateof(now()));
cqlsh:cbd_video_sharing> INSERT INTO comment_per_video (id, video_id, author, comment, upload_timestamp) VALUES ( now(), eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d, 'user5@bot.com', 'Hello DS', dateof(now()));
cqlsh:cbd_video_sharing> INSERT INTO comment_per_video (id, video_id, author, comment, upload_timestamp) VALUES ( now(), eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d, 'ds@test.com', 'WHATS HAPPENING', dateof(now()));
cqlsh:cbd_video_sharing> INSERT INTO comment_per_video (id, video_id, author, comment, upload_timestamp) VALUES ( now(), eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d, 'user6@bot.com', 'Hello DS', dateof(now()));
cqlsh:cbd_video_sharing> INSERT INTO comment_per_video (id, video_id, author, comment, upload_timestamp) VALUES ( now(), 7d6a05b0-0d4b-11ea-9d48-0b1cc2ad2f9d, 'clau@sof.pt', 'Friggin Pleb', dateof(now()));
cqlsh:cbd_video_sharing> INSERT INTO comment_per_video (id, video_id, author, comment, upload_timestamp) VALUES ( now(), 7d6a05b0-0d4b-11ea-9d48-0b1cc2ad2f9d, 'user9@bot.com', 'Us Bots couldve done better', dateof(now()));
cqlsh:cbd_video_sharing> INSERT INTO comment_per_video (id, video_id, author, comment, upload_timestamp) VALUES ( now(), 3ffcc5a0-0d4b-11ea-9d48-0b1cc2ad2f9d , 'pedro@f.ag', 'WTF Dude did you actually?!', dateof(now()));


 author        | upload_timestamp                | comment                     | id                                   | video_id
---------------+---------------------------------+-----------------------------+--------------------------------------+--------------------------------------
 user1@bot.com | 2019-11-22 19:55:49.211000+0000 |                    Hello DS | 149e82b1-0d62-11ea-9d48-0b1cc2ad2f9d | eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d
 user5@bot.com | 2019-11-22 19:56:33.276000+0000 |                    Hello DS | 2ee24bc1-0d62-11ea-9d48-0b1cc2ad2f9d | eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d
 user2@bot.com | 2019-11-22 19:56:03.549000+0000 |                    Hello DS | 1d2a50d1-0d62-11ea-9d48-0b1cc2ad2f9d | eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d
   ds@test.com | 2019-11-22 19:56:40.160000+0000 |             WHATS HAPPENING | 32fcb601-0d62-11ea-9d48-0b1cc2ad2f9d | eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d
   ds@test.com | 2019-11-22 19:56:13.170000+0000 |                   Wait wtf? | 22e68430-0d62-11ea-9d48-0b1cc2ad2f9d | eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d
   ds@test.com | 2019-11-22 19:55:38.805000+0000 |              Also Second :) | 0e6aae51-0d62-11ea-9d48-0b1cc2ad2f9d | eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d
   ds@test.com | 2019-11-22 19:55:34.830000+0000 |                       FIRST | 0c0c24e1-0d62-11ea-9d48-0b1cc2ad2f9d | eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d
 user9@bot.com | 2019-11-22 19:57:00.688000+0000 | Us Bots couldve done better | 3f390901-0d62-11ea-9d48-0b1cc2ad2f9d | 7d6a05b0-0d4b-11ea-9d48-0b1cc2ad2f9d
 user4@bot.com | 2019-11-22 19:56:19.631000+0000 |                    Hello DS | 26c06300-0d62-11ea-9d48-0b1cc2ad2f9d | eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d
 user6@bot.com | 2019-11-22 19:56:44.711000+0000 |                    Hello DS | 35b32371-0d62-11ea-9d48-0b1cc2ad2f9d | eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d
   clau@sof.pt | 2019-11-22 19:56:54.282000+0000 |                Friggin Pleb | 3b67b5b0-0d62-11ea-9d48-0b1cc2ad2f9d | 7d6a05b0-0d4b-11ea-9d48-0b1cc2ad2f9d
    pedro@f.ag | 2019-11-22 19:57:06.596000+0000 | WTF Dude did you actually?! | 42be8641-0d62-11ea-9d48-0b1cc2ad2f9d | 3ffcc5a0-0d4b-11ea-9d48-0b1cc2ad2f9d
 user3@bot.com | 2019-11-22 19:56:09.003000+0000 |                    Hello DS | 206a87b1-0d62-11ea-9d48-0b1cc2ad2f9d | eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d

(13 rows)

cqlsh:cbd_video_sharing> SELECT * FROM comment_per_video;

 video_id                             | upload_timestamp                | author        | comment                     | id
--------------------------------------+---------------------------------+---------------+-----------------------------+--------------------------------------
 eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d | 2019-11-22 19:57:58.074000+0000 | user6@bot.com |                    Hello DS | 616d71a1-0d62-11ea-9d48-0b1cc2ad2f9d
 eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d | 2019-11-22 19:57:54.234000+0000 |   ds@test.com |             WHATS HAPPENING | 5f2381a1-0d62-11ea-9d48-0b1cc2ad2f9d
 eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d | 2019-11-22 19:57:44.584000+0000 | user5@bot.com |                    Hello DS | 59630881-0d62-11ea-9d48-0b1cc2ad2f9d
 eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d | 2019-11-22 19:57:39.764000+0000 | user4@bot.com |                    Hello DS | 56838f41-0d62-11ea-9d48-0b1cc2ad2f9d
 eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d | 2019-11-22 19:57:35.285000+0000 |   ds@test.com |                   Wait wtf? | 53d81e51-0d62-11ea-9d48-0b1cc2ad2f9d
 eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d | 2019-11-22 19:57:31.374000+0000 | user3@bot.com |                    Hello DS | 518358e1-0d62-11ea-9d48-0b1cc2ad2f9d
 eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d | 2019-11-22 19:57:26.225000+0000 | user2@bot.com |                    Hello DS | 4e71ac11-0d62-11ea-9d48-0b1cc2ad2f9d
 eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d | 2019-11-22 19:57:22.123000+0000 | user1@bot.com |                    Hello DS | 4bffc1b1-0d62-11ea-9d48-0b1cc2ad2f9d
 eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d | 2019-11-22 19:57:15.591000+0000 |   ds@test.com |              Also Second :) | 481b0d71-0d62-11ea-9d48-0b1cc2ad2f9d
 eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d | 2019-11-22 19:57:11.315000+0000 |   ds@test.com |                       FIRST | 458e9631-0d62-11ea-9d48-0b1cc2ad2f9d
 3ffcc5a0-0d4b-11ea-9d48-0b1cc2ad2f9d | 2019-11-22 19:58:12.784000+0000 |    pedro@f.ag | WTF Dude did you actually?! | 6a320301-0d62-11ea-9d48-0b1cc2ad2f9d
 7d6a05b0-0d4b-11ea-9d48-0b1cc2ad2f9d | 2019-11-22 19:58:07.551000+0000 | user9@bot.com | Us Bots couldve done better | 671384f1-0d62-11ea-9d48-0b1cc2ad2f9d
 7d6a05b0-0d4b-11ea-9d48-0b1cc2ad2f9d | 2019-11-22 19:58:03.084000+0000 |   clau@sof.pt |                Friggin Pleb | 6469e8c1-0d62-11ea-9d48-0b1cc2ad2f9d

(13 rows)
```

#### Follower
```
cqlsh:cbd_video_sharing> SELECT * FROM Follower;

 user | video_id
------+----------

(0 rows)
cqlsh:cbd_video_sharing> INSERT INTO Follower (user,video_id)
                     ... VALUES ('user1@bot.com', 3ffcc5a0-0d4b-11ea-9d48-0b1cc2ad2f9d); 
cqlsh:cbd_video_sharing> INSERT INTO Follower (user,video_id) VALUES ('user2@bot.com', 3ffcc5a0-0d4b-11ea-9d48-0b1cc2ad2f9d);
cqlsh:cbd_video_sharing> INSERT INTO Follower (user,video_id) VALUES ('user3@bot.com', 3ffcc5a0-0d4b-11ea-9d48-0b1cc2ad2f9d);
cqlsh:cbd_video_sharing> INSERT INTO Follower (user,video_id) VALUES ('user4@bot.com', 3ffcc5a0-0d4b-11ea-9d48-0b1cc2ad2f9d);
cqlsh:cbd_video_sharing> INSERT INTO Follower (user,video_id) VALUES ('user5@bot.com', 3ffcc5a0-0d4b-11ea-9d48-0b1cc2ad2f9d);
cqlsh:cbd_video_sharing> INSERT INTO Follower (user,video_id) VALUES ('user6@bot.com', 3ffcc5a0-0d4b-11ea-9d48-0b1cc2ad2f9d);
cqlsh:cbd_video_sharing> INSERT INTO Follower (user,video_id) VALUES ('user7@bot.com', 3ffcc5a0-0d4b-11ea-9d48-0b1cc2ad2f9d);
cqlsh:cbd_video_sharing> INSERT INTO Follower (user,video_id) VALUES ('user8@bot.com', 3ffcc5a0-0d4b-11ea-9d48-0b1cc2ad2f9d);
cqlsh:cbd_video_sharing> INSERT INTO Follower (user,video_id) VALUES ('user9@bot.com', 3ffcc5a0-0d4b-11ea-9d48-0b1cc2ad2f9d);
cqlsh:cbd_video_sharing> INSERT INTO Follower (user,video_id) VALUES ('ds@test.com', bc1bd3b0-0d4b-11ea-9d48-0b1cc2ad2f9d);
cqlsh:cbd_video_sharing> INSERT INTO Follower (user,video_id) VALUES ('ds@test.com', 3ffcc5a0-0d4b-11ea-9d48-0b1cc2ad2f9d);

cqlsh:cbd_video_sharing> SELECT * FROM Follower;

 user          | video_id
---------------+--------------------------------------
 user4@bot.com | 3ffcc5a0-0d4b-11ea-9d48-0b1cc2ad2f9d
 user8@bot.com | 3ffcc5a0-0d4b-11ea-9d48-0b1cc2ad2f9d
 user9@bot.com | 3ffcc5a0-0d4b-11ea-9d48-0b1cc2ad2f9d
 user6@bot.com | 3ffcc5a0-0d4b-11ea-9d48-0b1cc2ad2f9d
 user5@bot.com | 3ffcc5a0-0d4b-11ea-9d48-0b1cc2ad2f9d
   ds@test.com | 3ffcc5a0-0d4b-11ea-9d48-0b1cc2ad2f9d
 user3@bot.com | 3ffcc5a0-0d4b-11ea-9d48-0b1cc2ad2f9d
   ds@test.com | bc1bd3b0-0d4b-11ea-9d48-0b1cc2ad2f9d
 user2@bot.com | 3ffcc5a0-0d4b-11ea-9d48-0b1cc2ad2f9d
 user1@bot.com | 3ffcc5a0-0d4b-11ea-9d48-0b1cc2ad2f9d
 user7@bot.com | 3ffcc5a0-0d4b-11ea-9d48-0b1cc2ad2f9d

(11 rows)
```

#### Events
```
cqlsh:cbd_video_sharing> Select * From Event;

 id | user | video_id | action | real_timestamp | video_timestamp
----+------+----------+--------+----------------+-----------------

(0 rows)

cqlsh:cbd_video_sharing> INSERT INTO Event (id, user, video_id, action, real_timestamp, video_timestamp)
                     ... VALUES (now(),'ds@test.com', 3ffcc5a0-0d4b-11ea-9d48-0b1cc2ad2f9d, 'Play', dateof(now()), 0);
cqlsh:cbd_video_sharing> INSERT INTO Event (id, user, video_id, action, real_timestamp, video_timestamp)
                     ... VALUES (now(),'ds@test.com', 3ffcc5a0-0d4b-11ea-9d48-0b1cc2ad2f9d, 'Pause', dateof(now()), 310);
cqlsh:cbd_video_sharing> INSERT INTO Event (id, user, video_id, action, real_timestamp, video_timestamp)
                     ... VALUES (now(),'ds@test.com', 3ffcc5a0-0d4b-11ea-9d48-0b1cc2ad2f9d, 'Play', dateof(now()), 310);
cqlsh:cbd_video_sharing> INSERT INTO Event (id, user, video_id, action, real_timestamp, video_timestamp)
                     ... VALUES (now(),'user7@bot.com ',7d6a05b0-0d4b-11ea-9d48-0b1cc2ad2f9d, 'Play', dateof(now()), 0);
cqlsh:cbd_video_sharing> INSERT INTO Event (id, user, video_id, action, real_timestamp, video_timestamp)
                     ... VALUES (now(),'clau@sof.pt',7d6a05b0-0d4b-11ea-9d48-0b1cc2ad2f9d, 'Play', dateof(now()), 0);
cqlsh:cbd_video_sharing> INSERT INTO Event (id, user, video_id, action, real_timestamp, video_timestamp)
                     ... VALUES (now(),'clau@sof.pt',7d6a05b0-0d4b-11ea-9d48-0b1cc2ad2f9d, 'Stop', dateof(now()), 69);
cqlsh:cbd_video_sharing> INSERT INTO Event (id, user, video_id, action, real_timestamp, video_timestamp)
                     ... VALUES (now(),'ds@test.com',bc1bd3b0-0d4b-11ea-9d48-0b1cc2ad2f9d, 'Play', dateof(now()), 0);
cqlsh:cbd_video_sharing> INSERT INTO Event (id, user, video_id, action, real_timestamp, video_timestamp)
                     ... VALUES (now(),'ds@test.com',bc1bd3b0-0d4b-11ea-9d48-0b1cc2ad2f9d, 'Play', dateof(now()), 150);
cqlsh:cbd_video_sharing> INSERT INTO Event (id, user, video_id, action, real_timestamp, video_timestamp)
                     ... VALUES (now(),'ds@test.com',bc1bd3b0-0d4b-11ea-9d48-0b1cc2ad2f9d, 'Pause', dateof(now()), 200);
cqlsh:cbd_video_sharing> INSERT INTO Event (id, user, video_id, action, real_timestamp, video_timestamp)
                     ... VALUES (now(),'ds@test.com',bc1bd3b0-0d4b-11ea-9d48-0b1cc2ad2f9d, 'Play', dateof(now()), 200);
cqlsh:cbd_video_sharing> INSERT INTO Event (id, user, video_id, action, real_timestamp, video_timestamp)
                     ... VALUES (now(),'ds@test.com',bc1bd3b0-0d4b-11ea-9d48-0b1cc2ad2f9d, 'Stop', dateof(now()), 349)
cqlsh:cbd_video_sharing> INSERT INTO Event (id, user, video_id, action, real_timestamp, video_timestamp)
                     ... VALUES (now(),'pedro@f.ag',eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d, 'Start', dateof(now()), 0);
cqlsh:cbd_video_sharing> INSERT INTO Event (id, user, video_id, action, real_timestamp, video_timestamp)
                     ... VALUES (now(),'pedro@f.ag',eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d, 'Stop', dateof(now()), 5
                     
cqlsh:cbd_video_sharing> SELECT * FROM Event;

 id                                   | user           | video_id                             | action | real_timestamp                  | video_timestamp
--------------------------------------+----------------+--------------------------------------+--------+---------------------------------+-----------------
 21128880-0d57-11ea-9d48-0b1cc2ad2f9d |    ds@test.com | bc1bd3b0-0d4b-11ea-9d48-0b1cc2ad2f9d |   Play | 2019-11-22 18:37:25.640000+0000 |               0
 f7416cb0-0d56-11ea-9d48-0b1cc2ad2f9d |    clau@sof.pt | 7d6a05b0-0d4b-11ea-9d48-0b1cc2ad2f9d |   Stop | 2019-11-22 18:36:15.483000+0000 |              69
 3ea6dc20-0d57-11ea-9d48-0b1cc2ad2f9d |    ds@test.com | bc1bd3b0-0d4b-11ea-9d48-0b1cc2ad2f9d |   Stop | 2019-11-22 18:38:15.266000+0000 |             349
 30c31ab0-0d57-11ea-9d48-0b1cc2ad2f9d |    ds@test.com | bc1bd3b0-0d4b-11ea-9d48-0b1cc2ad2f9d |  Pause | 2019-11-22 18:37:51.963000+0000 |             200
 910d8680-0d57-11ea-9d48-0b1cc2ad2f9d |     pedro@f.ag | eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d |   Stop | 2019-11-22 18:40:33.512000+0000 |              53
 f03c65a0-0d56-11ea-9d48-0b1cc2ad2f9d |    clau@sof.pt | 7d6a05b0-0d4b-11ea-9d48-0b1cc2ad2f9d |   Play | 2019-11-22 18:36:03.706000+0000 |               0
 36de5e00-0d57-11ea-9d48-0b1cc2ad2f9d |    ds@test.com | bc1bd3b0-0d4b-11ea-9d48-0b1cc2ad2f9d |   Play | 2019-11-22 18:38:02.208000+0000 |             200
 26aae030-0d57-11ea-9d48-0b1cc2ad2f9d |    ds@test.com | bc1bd3b0-0d4b-11ea-9d48-0b1cc2ad2f9d |   Play | 2019-11-22 18:37:35.027000+0000 |             150
 b6950730-0d56-11ea-9d48-0b1cc2ad2f9d |    ds@test.com | 3ffcc5a0-0d4b-11ea-9d48-0b1cc2ad2f9d |  Pause | 2019-11-22 18:34:26.979000+0000 |             310
 e0159200-0d56-11ea-9d48-0b1cc2ad2f9d | user7@bot.com  | 7d6a05b0-0d4b-11ea-9d48-0b1cc2ad2f9d |   Play | 2019-11-22 18:35:36.608000+0000 |               0
 7df33c70-0d57-11ea-9d48-0b1cc2ad2f9d |     pedro@f.ag | eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d |  Start | 2019-11-22 18:40:01.463000+0000 |               0
 a76abc00-0d56-11ea-9d48-0b1cc2ad2f9d |    ds@test.com | 3ffcc5a0-0d4b-11ea-9d48-0b1cc2ad2f9d |   Play | 2019-11-22 18:34:01.537000+0000 |               0
 c198da30-0d56-11ea-9d48-0b1cc2ad2f9d |    ds@test.com | 3ffcc5a0-0d4b-11ea-9d48-0b1cc2ad2f9d |   Play | 2019-11-22 18:34:45.459000+0000 |             310

(13 rows)
```

#### Rating
```
cqlsh:cbd_video_sharing> SELECT * FROM Rating;

 id | video_id | value
----+----------+-------

(0 rows)

cqlsh:cbd_video_sharing> INSERT INTO Rating (id, video_id, value)
                     ... VALUES (now(), eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d, 1);
cqlsh:cbd_video_sharing> INSERT INTO Rating (id, video_id, value)
                     ... VALUES (now(), 3ffcc5a0-0d4b-11ea-9d48-0b1cc2ad2f9d, 5);
cqlsh:cbd_video_sharing> INSERT INTO Rating (id, video_id, value) VALUES (now(), 3ffcc5a0-0d4b-11ea-9d48-0b1cc2ad2f9d, 5);
cqlsh:cbd_video_sharing> INSERT INTO Rating (id, video_id, value) VALUES (now(), 3ffcc5a0-0d4b-11ea-9d48-0b1cc2ad2f9d, 5);
cqlsh:cbd_video_sharing> INSERT INTO Rating (id, video_id, value) VALUES (now(), 3ffcc5a0-0d4b-11ea-9d48-0b1cc2ad2f9d, 5);
cqlsh:cbd_video_sharing> INSERT INTO Rating (id, video_id, value) VALUES (now(), 3ffcc5a0-0d4b-11ea-9d48-0b1cc2ad2f9d, 5);
cqlsh:cbd_video_sharing> INSERT INTO Rating (id, video_id, value) VALUES (now(), 3ffcc5a0-0d4b-11ea-9d48-0b1cc2ad2f9d, 5);
cqlsh:cbd_video_sharing> INSERT INTO Rating (id, video_id, value) VALUES (now(), 3ffcc5a0-0d4b-11ea-9d48-0b1cc2ad2f9d, 5);
cqlsh:cbd_video_sharing> INSERT INTO Rating (id, video_id, value) VALUES (now(), 3ffcc5a0-0d4b-11ea-9d48-0b1cc2ad2f9d, 5);
cqlsh:cbd_video_sharing> INSERT INTO Rating (id, video_id, value) VALUES (now(), 3ffcc5a0-0d4b-11ea-9d48-0b1cc2ad2f9d, 5);
cqlsh:cbd_video_sharing> INSERT INTO Rating (id, video_id, value)
                     ... VALUES (now(), 7d6a05b0-0d4b-11ea-9d48-0b1cc2ad2f9d , 2);
cqlsh:cbd_video_sharing> INSERT INTO Rating (id, video_id, value)
                     ... VALUES (now(), 7d6a05b0-0d4b-11ea-9d48-0b1cc2ad2f9d , 4);
cqlsh:cbd_video_sharing> INSERT INTO Rating (id, video_id, value)
                     ... VALUES (now(), 7d6a05b0-0d4b-11ea-9d48-0b1cc2ad2f9d , 3);

cqlsh:cbd_video_sharing> SELECT * FROM Rating;

 id                                   | video_id                             | value
--------------------------------------+--------------------------------------+-------
 0004d020-0d58-11ea-9d48-0b1cc2ad2f9d | 3ffcc5a0-0d4b-11ea-9d48-0b1cc2ad2f9d |     5
 017bdfc0-0d58-11ea-9d48-0b1cc2ad2f9d | 3ffcc5a0-0d4b-11ea-9d48-0b1cc2ad2f9d |     5
 00e39760-0d58-11ea-9d48-0b1cc2ad2f9d | 3ffcc5a0-0d4b-11ea-9d48-0b1cc2ad2f9d |     5
 2c00bb30-0d58-11ea-9d48-0b1cc2ad2f9d | 7d6a05b0-0d4b-11ea-9d48-0b1cc2ad2f9d |     3
 0095ec90-0d58-11ea-9d48-0b1cc2ad2f9d | 3ffcc5a0-0d4b-11ea-9d48-0b1cc2ad2f9d |     5
 012f9480-0d58-11ea-9d48-0b1cc2ad2f9d | 3ffcc5a0-0d4b-11ea-9d48-0b1cc2ad2f9d |     5
 22286fe0-0d58-11ea-9d48-0b1cc2ad2f9d | 7d6a05b0-0d4b-11ea-9d48-0b1cc2ad2f9d |     2
 004e8350-0d58-11ea-9d48-0b1cc2ad2f9d | 3ffcc5a0-0d4b-11ea-9d48-0b1cc2ad2f9d |     5
 26a96420-0d58-11ea-9d48-0b1cc2ad2f9d | 7d6a05b0-0d4b-11ea-9d48-0b1cc2ad2f9d |     4
 fb80a790-0d57-11ea-9d48-0b1cc2ad2f9d | 3ffcc5a0-0d4b-11ea-9d48-0b1cc2ad2f9d |     5
 01dbb300-0d58-11ea-9d48-0b1cc2ad2f9d | 3ffcc5a0-0d4b-11ea-9d48-0b1cc2ad2f9d |     5
 e1061710-0d57-11ea-9d48-0b1cc2ad2f9d | eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d |     1
 ffb55090-0d57-11ea-9d48-0b1cc2ad2f9d | 3ffcc5a0-0d4b-11ea-9d48-0b1cc2ad2f9d |     5

(13 rows)
```

### Step 4 - Getting all data inserted as JSON
```
cqlsh:cbd_video_sharing> describe tables;

comment  rating  follower  video  user  event

cqlsh:cbd_video_sharing> SELECT json * FROM Comment;

 [json]
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                  {"id": "9b283630-0d50-11ea-9d48-0b1cc2ad2f9d", "video_id": "7d6a05b0-0d4b-11ea-9d48-0b1cc2ad2f9d", "author": "clau@sof.pt", "comment": "Friggin Pleb", "upload_timestamp": "2019-11-22 17:50:43.987Z"}
 {"id": "bc9ecd10-0d50-11ea-9d48-0b1cc2ad2f9d", "video_id": "7d6a05b0-0d4b-11ea-9d48-0b1cc2ad2f9d", "author": "user9@bot.com", "comment": "Us Bots couldve done better", "upload_timestamp": "2019-11-22 17:51:40.129Z"}
                    {"id": "551f2270-0d50-11ea-9d48-0b1cc2ad2f9d", "video_id": "eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d", "author": "user4@bot.com", "comment": "Hello DS", "upload_timestamp": "2019-11-22 17:48:46.487Z"}
                    {"id": "40a918f0-0d50-11ea-9d48-0b1cc2ad2f9d", "video_id": "eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d", "author": "user3@bot.com", "comment": "Hello DS", "upload_timestamp": "2019-11-22 17:48:12.159Z"}
                {"id": "1fc1a2b0-0d50-11ea-9d48-0b1cc2ad2f9d", "video_id": "eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d", "author": "ds@test.com", "comment": "Also Second :)", "upload_timestamp": "2019-11-22 17:47:16.955Z"}
                     {"id": "4eb5bf20-0d50-11ea-9d48-0b1cc2ad2f9d", "video_id": "eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d", "author": "ds@test.com", "comment": "Wait wtf?", "upload_timestamp": "2019-11-22 17:48:35.730Z"}
                    {"id": "6ac60ad0-0d50-11ea-9d48-0b1cc2ad2f9d", "video_id": "eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d", "author": "user6@bot.com", "comment": "Hello DS", "upload_timestamp": "2019-11-22 17:49:22.813Z"}
                    {"id": "3b12e420-0d50-11ea-9d48-0b1cc2ad2f9d", "video_id": "eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d", "author": "user2@bot.com", "comment": "Hello DS", "upload_timestamp": "2019-11-22 17:48:02.786Z"}
                    {"id": "59c9e5d0-0d50-11ea-9d48-0b1cc2ad2f9d", "video_id": "eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d", "author": "user5@bot.com", "comment": "Hello DS", "upload_timestamp": "2019-11-22 17:48:54.318Z"}
    {"id": "e7ca48c0-0d50-11ea-9d48-0b1cc2ad2f9d", "video_id": "3ffcc5a0-0d4b-11ea-9d48-0b1cc2ad2f9d", "author": "pedro@f.ag", "comment": "WTF Dude did you actually?!", "upload_timestamp": "2019-11-22 17:52:52.556Z"}
               {"id": "619e4ad0-0d50-11ea-9d48-0b1cc2ad2f9d", "video_id": "eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d", "author": "ds@test.com", "comment": "WHATS HAPPENING", "upload_timestamp": "2019-11-22 17:49:07.454Z"}
                         {"id": "76cfee10-0d4e-11ea-9d48-0b1cc2ad2f9d", "video_id": "eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d", "author": "ds@test.com", "comment": "FIRST", "upload_timestamp": "2019-11-22 17:35:24.018Z"}
                    {"id": "32686a70-0d50-11ea-9d48-0b1cc2ad2f9d", "video_id": "eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d", "author": "user1@bot.com", "comment": "Hello DS", "upload_timestamp": "2019-11-22 17:47:48.247Z"}

(13 rows)
cqlsh:cbd_video_sharing> describe tables;

comment  rating  follower  video  user  event

cqlsh:cbd_video_sharing> SELECT json * FROM Rating;

 [json]
----------------------------------------------------------------------------------------------------------------
 {"id": "0004d020-0d58-11ea-9d48-0b1cc2ad2f9d", "video_id": "3ffcc5a0-0d4b-11ea-9d48-0b1cc2ad2f9d", "value": 5}
 {"id": "017bdfc0-0d58-11ea-9d48-0b1cc2ad2f9d", "video_id": "3ffcc5a0-0d4b-11ea-9d48-0b1cc2ad2f9d", "value": 5}
 {"id": "00e39760-0d58-11ea-9d48-0b1cc2ad2f9d", "video_id": "3ffcc5a0-0d4b-11ea-9d48-0b1cc2ad2f9d", "value": 5}
 {"id": "2c00bb30-0d58-11ea-9d48-0b1cc2ad2f9d", "video_id": "7d6a05b0-0d4b-11ea-9d48-0b1cc2ad2f9d", "value": 3}
 {"id": "0095ec90-0d58-11ea-9d48-0b1cc2ad2f9d", "video_id": "3ffcc5a0-0d4b-11ea-9d48-0b1cc2ad2f9d", "value": 5}
 {"id": "012f9480-0d58-11ea-9d48-0b1cc2ad2f9d", "video_id": "3ffcc5a0-0d4b-11ea-9d48-0b1cc2ad2f9d", "value": 5}
 {"id": "22286fe0-0d58-11ea-9d48-0b1cc2ad2f9d", "video_id": "7d6a05b0-0d4b-11ea-9d48-0b1cc2ad2f9d", "value": 2}
 {"id": "004e8350-0d58-11ea-9d48-0b1cc2ad2f9d", "video_id": "3ffcc5a0-0d4b-11ea-9d48-0b1cc2ad2f9d", "value": 5}
 {"id": "26a96420-0d58-11ea-9d48-0b1cc2ad2f9d", "video_id": "7d6a05b0-0d4b-11ea-9d48-0b1cc2ad2f9d", "value": 4}
 {"id": "fb80a790-0d57-11ea-9d48-0b1cc2ad2f9d", "video_id": "3ffcc5a0-0d4b-11ea-9d48-0b1cc2ad2f9d", "value": 5}
 {"id": "01dbb300-0d58-11ea-9d48-0b1cc2ad2f9d", "video_id": "3ffcc5a0-0d4b-11ea-9d48-0b1cc2ad2f9d", "value": 5}
 {"id": "e1061710-0d57-11ea-9d48-0b1cc2ad2f9d", "video_id": "eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d", "value": 1}
 {"id": "ffb55090-0d57-11ea-9d48-0b1cc2ad2f9d", "video_id": "3ffcc5a0-0d4b-11ea-9d48-0b1cc2ad2f9d", "value": 5}

(13 rows)
cqlsh:cbd_video_sharing> SELECT json * FROM Video;

 [json]
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                                                                                                                                                      {"id": "8ab66c50-0d4f-11ea-9d48-0b1cc2ad2f9d", "author": "user1@bot.com", "upload_timestamp": "2019-11-22 17:43:06.901Z", "description": "Hello, World!", "name": "Hi, Im Bot1", "tags": ["Greetings", "TheFuture", "Destroy", "All", "Humans"]}     
                                                                                                                                                                        {"id": "ac746c70-0d4f-11ea-9d48-0b1cc2ad2f9d", "author": "user6@bot.com", "upload_timestamp": "2019-11-22 17:44:03.511Z", "description": "Hello, World!", "name": "Hi, Im Bot6", "tags": ["Greetings", "TheFuture", "Destroy", "All", "Humans"]}
                                                                                         {"id": "b4ce2e10-0d4f-11ea-9d48-0b1cc2ad2f9d", "author": "user8@bot.com", "upload_timestamp": "2019-11-22 17:44:17.521Z", "description": "Hello, World!", "name": "Hi, Im Bot8", "tags": ["Greetings", "TheFuture", "Destroy", "All", "Humans"]}
 {"id": "eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d", "author": "ds@test.com", "upload_timestamp": "2019-11-22 17:17:13.467Z", "description": "I have made some poor life decisions", "name": "Watching some guy watch every JonTron video in one sitting", "tags": ["JonTron", "Random", "Why", "Why2x", "Gottem", "Inception", "#intoodeep"]}
                                                                                                     {"id": "3ffcc5a0-0d4b-11ea-9d48-0b1cc2ad2f9d", "author": "ds@test.com", "upload_timestamp": "2019-11-22 17:12:23.546Z", "description": "Me going to the Zoo", "name": "ZooTrip", "tags": ["Wholesome", "Cute", "#First", "Animals"]}
                                   {"id": "7d6a05b0-0d4b-11ea-9d48-0b1cc2ad2f9d", "author": "ds@test.com", "upload_timestamp": "2019-11-22 17:14:06.603Z", "description": "Me getting an E Z Sixtuple Kill with Zenyatta", "name": "Exeperience my Orbs [TEAMKILL]", "tags": ["Overwatch", "Gaming", "Rekt", "Gottem", "EZ", "Zenyatta"]}
                                                                                         {"id": "a3bd96b0-0d4f-11ea-9d48-0b1cc2ad2f9d", "author": "user4@bot.com", "upload_timestamp": "2019-11-22 17:43:48.891Z", "description": "Hello, World!", "name": "Hi, Im Bot4", "tags": ["Greetings", "TheFuture", "Destroy", "All", "Humans"]}
                                                                                         {"id": "9f217950-0d4f-11ea-9d48-0b1cc2ad2f9d", "author": "user3@bot.com", "upload_timestamp": "2019-11-22 17:43:41.157Z", "description": "Hello, World!", "name": "Hi, Im Bot3", "tags": ["Greetings", "TheFuture", "Destroy", "All", "Humans"]}
                                                                                         {"id": "990b8d30-0d4f-11ea-9d48-0b1cc2ad2f9d", "author": "user2@bot.com", "upload_timestamp": "2019-11-22 17:43:30.947Z", "description": "Hello, World!", "name": "Hi, Im Bot2", "tags": ["Greetings", "TheFuture", "Destroy", "All", "Humans"]}
                                                                                         {"id": "b930ebf0-0d4f-11ea-9d48-0b1cc2ad2f9d", "author": "user9@bot.com", "upload_timestamp": "2019-11-22 17:44:24.879Z", "description": "Hello, World!", "name": "Hi, Im Bot9", "tags": ["Greetings", "TheFuture", "Destroy", "All", "Humans"]}
                                                                                         {"id": "b0cca300-0d4f-11ea-9d48-0b1cc2ad2f9d", "author": "user7@bot.com", "upload_timestamp": "2019-11-22 17:44:10.800Z", "description": "Hello, World!", "name": "Hi, Im Bot7", "tags": ["Greetings", "TheFuture", "Destroy", "All", "Humans"]}
                                                                                         {"id": "a856a6d0-0d4f-11ea-9d48-0b1cc2ad2f9d", "author": "user5@bot.com", "upload_timestamp": "2019-11-22 17:43:56.605Z", "description": "Hello, World!", "name": "Hi, Im Bot5", "tags": ["Greetings", "TheFuture", "Destroy", "All", "Humans"]}
                                                                            {"id": "bc1bd3b0-0d4b-11ea-9d48-0b1cc2ad2f9d", "author": "pedro@f.ag", "upload_timestamp": "2019-11-22 17:15:51.787Z", "description": "Why am I doing this?...", "name": "Watching every JonTron Video in one sitting", "tags": ["JonTron", "Random", "Why"]}

(13 rows)
cqlsh:cbd_video_sharing> describe tables;

comment  rating  follower  video  user  event

cqlsh:cbd_video_sharing> SELECT json * FROM event;

 [json]
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    {"id": "21128880-0d57-11ea-9d48-0b1cc2ad2f9d", "user": "ds@test.com", "video_id": "bc1bd3b0-0d4b-11ea-9d48-0b1cc2ad2f9d", "action": "Play", "real_timestamp": "2019-11-22 18:37:25.640Z", "video_timestamp": 0}
   {"id": "f7416cb0-0d56-11ea-9d48-0b1cc2ad2f9d", "user": "clau@sof.pt", "video_id": "7d6a05b0-0d4b-11ea-9d48-0b1cc2ad2f9d", "action": "Stop", "real_timestamp": "2019-11-22 18:36:15.483Z", "video_timestamp": 69}
  {"id": "3ea6dc20-0d57-11ea-9d48-0b1cc2ad2f9d", "user": "ds@test.com", "video_id": "bc1bd3b0-0d4b-11ea-9d48-0b1cc2ad2f9d", "action": "Stop", "real_timestamp": "2019-11-22 18:38:15.266Z", "video_timestamp": 349}
 {"id": "30c31ab0-0d57-11ea-9d48-0b1cc2ad2f9d", "user": "ds@test.com", "video_id": "bc1bd3b0-0d4b-11ea-9d48-0b1cc2ad2f9d", "action": "Pause", "real_timestamp": "2019-11-22 18:37:51.963Z", "video_timestamp": 200}
    {"id": "910d8680-0d57-11ea-9d48-0b1cc2ad2f9d", "user": "pedro@f.ag", "video_id": "eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d", "action": "Stop", "real_timestamp": "2019-11-22 18:40:33.512Z", "video_timestamp": 53}
    {"id": "f03c65a0-0d56-11ea-9d48-0b1cc2ad2f9d", "user": "clau@sof.pt", "video_id": "7d6a05b0-0d4b-11ea-9d48-0b1cc2ad2f9d", "action": "Play", "real_timestamp": "2019-11-22 18:36:03.706Z", "video_timestamp": 0}
  {"id": "36de5e00-0d57-11ea-9d48-0b1cc2ad2f9d", "user": "ds@test.com", "video_id": "bc1bd3b0-0d4b-11ea-9d48-0b1cc2ad2f9d", "action": "Play", "real_timestamp": "2019-11-22 18:38:02.208Z", "video_timestamp": 200}
  {"id": "26aae030-0d57-11ea-9d48-0b1cc2ad2f9d", "user": "ds@test.com", "video_id": "bc1bd3b0-0d4b-11ea-9d48-0b1cc2ad2f9d", "action": "Play", "real_timestamp": "2019-11-22 18:37:35.027Z", "video_timestamp": 150}
 {"id": "b6950730-0d56-11ea-9d48-0b1cc2ad2f9d", "user": "ds@test.com", "video_id": "3ffcc5a0-0d4b-11ea-9d48-0b1cc2ad2f9d", "action": "Pause", "real_timestamp": "2019-11-22 18:34:26.979Z", "video_timestamp": 310}
 {"id": "e0159200-0d56-11ea-9d48-0b1cc2ad2f9d", "user": "user7@bot.com ", "video_id": "7d6a05b0-0d4b-11ea-9d48-0b1cc2ad2f9d", "action": "Play", "real_timestamp": "2019-11-22 18:35:36.608Z", "video_timestamp": 0}
    {"id": "7df33c70-0d57-11ea-9d48-0b1cc2ad2f9d", "user": "pedro@f.ag", "video_id": "eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d", "action": "Start", "real_timestamp": "2019-11-22 18:40:01.463Z", "video_timestamp": 0}
    {"id": "a76abc00-0d56-11ea-9d48-0b1cc2ad2f9d", "user": "ds@test.com", "video_id": "3ffcc5a0-0d4b-11ea-9d48-0b1cc2ad2f9d", "action": "Play", "real_timestamp": "2019-11-22 18:34:01.537Z", "video_timestamp": 0}
  {"id": "c198da30-0d56-11ea-9d48-0b1cc2ad2f9d", "user": "ds@test.com", "video_id": "3ffcc5a0-0d4b-11ea-9d48-0b1cc2ad2f9d", "action": "Play", "real_timestamp": "2019-11-22 18:34:45.459Z", "video_timestamp": 310}

(13 rows)
cqlsh:cbd_video_sharing> SELECT json * FROM comment_per_video;

 [json]
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                    {"video_id": "eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d", "upload_timestamp": "2019-11-22 19:57:58.074Z", "author": "user6@bot.com", "comment": "Hello DS", "id": "616d71a1-0d62-11ea-9d48-0b1cc2ad2f9d"}
               {"video_id": "eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d", "upload_timestamp": "2019-11-22 19:57:54.234Z", "author": "ds@test.com", "comment": "WHATS HAPPENING", "id": "5f2381a1-0d62-11ea-9d48-0b1cc2ad2f9d"}
                    {"video_id": "eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d", "upload_timestamp": "2019-11-22 19:57:44.584Z", "author": "user5@bot.com", "comment": "Hello DS", "id": "59630881-0d62-11ea-9d48-0b1cc2ad2f9d"}
                    {"video_id": "eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d", "upload_timestamp": "2019-11-22 19:57:39.764Z", "author": "user4@bot.com", "comment": "Hello DS", "id": "56838f41-0d62-11ea-9d48-0b1cc2ad2f9d"}
                     {"video_id": "eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d", "upload_timestamp": "2019-11-22 19:57:35.285Z", "author": "ds@test.com", "comment": "Wait wtf?", "id": "53d81e51-0d62-11ea-9d48-0b1cc2ad2f9d"}
                    {"video_id": "eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d", "upload_timestamp": "2019-11-22 19:57:31.374Z", "author": "user3@bot.com", "comment": "Hello DS", "id": "518358e1-0d62-11ea-9d48-0b1cc2ad2f9d"}
                    {"video_id": "eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d", "upload_timestamp": "2019-11-22 19:57:26.225Z", "author": "user2@bot.com", "comment": "Hello DS", "id": "4e71ac11-0d62-11ea-9d48-0b1cc2ad2f9d"}
                    {"video_id": "eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d", "upload_timestamp": "2019-11-22 19:57:22.123Z", "author": "user1@bot.com", "comment": "Hello DS", "id": "4bffc1b1-0d62-11ea-9d48-0b1cc2ad2f9d"}
                {"video_id": "eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d", "upload_timestamp": "2019-11-22 19:57:15.591Z", "author": "ds@test.com", "comment": "Also Second :)", "id": "481b0d71-0d62-11ea-9d48-0b1cc2ad2f9d"}
                         {"video_id": "eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d", "upload_timestamp": "2019-11-22 19:57:11.315Z", "author": "ds@test.com", "comment": "FIRST", "id": "458e9631-0d62-11ea-9d48-0b1cc2ad2f9d"}
    {"video_id": "3ffcc5a0-0d4b-11ea-9d48-0b1cc2ad2f9d", "upload_timestamp": "2019-11-22 19:58:12.784Z", "author": "pedro@f.ag", "comment": "WTF Dude did you actually?!", "id": "6a320301-0d62-11ea-9d48-0b1cc2ad2f9d"}
 {"video_id": "7d6a05b0-0d4b-11ea-9d48-0b1cc2ad2f9d", "upload_timestamp": "2019-11-22 19:58:07.551Z", "author": "user9@bot.com", "comment": "Us Bots couldve done better", "id": "671384f1-0d62-11ea-9d48-0b1cc2ad2f9d"}
                  {"video_id": "7d6a05b0-0d4b-11ea-9d48-0b1cc2ad2f9d", "upload_timestamp": "2019-11-22 19:58:03.084Z", "author": "clau@sof.pt", "comment": "Friggin Pleb", "id": "6469e8c1-0d62-11ea-9d48-0b1cc2ad2f9d"}

(13 rows)

cqlsh:cbd_video_sharing> SELECT json * FROM comment_per_author ;

 [json]
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                    {"author": "user1@bot.com", "upload_timestamp": "2019-11-22 19:55:49.211Z", "comment": "Hello DS", "id": "149e82b1-0d62-11ea-9d48-0b1cc2ad2f9d", "video_id": "eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d"}
                    {"author": "user5@bot.com", "upload_timestamp": "2019-11-22 19:56:33.276Z", "comment": "Hello DS", "id": "2ee24bc1-0d62-11ea-9d48-0b1cc2ad2f9d", "video_id": "eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d"}
                    {"author": "user2@bot.com", "upload_timestamp": "2019-11-22 19:56:03.549Z", "comment": "Hello DS", "id": "1d2a50d1-0d62-11ea-9d48-0b1cc2ad2f9d", "video_id": "eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d"}
               {"author": "ds@test.com", "upload_timestamp": "2019-11-22 19:56:40.160Z", "comment": "WHATS HAPPENING", "id": "32fcb601-0d62-11ea-9d48-0b1cc2ad2f9d", "video_id": "eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d"}
                     {"author": "ds@test.com", "upload_timestamp": "2019-11-22 19:56:13.170Z", "comment": "Wait wtf?", "id": "22e68430-0d62-11ea-9d48-0b1cc2ad2f9d", "video_id": "eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d"}
                {"author": "ds@test.com", "upload_timestamp": "2019-11-22 19:55:38.805Z", "comment": "Also Second :)", "id": "0e6aae51-0d62-11ea-9d48-0b1cc2ad2f9d", "video_id": "eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d"}
                         {"author": "ds@test.com", "upload_timestamp": "2019-11-22 19:55:34.830Z", "comment": "FIRST", "id": "0c0c24e1-0d62-11ea-9d48-0b1cc2ad2f9d", "video_id": "eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d"}
 {"author": "user9@bot.com", "upload_timestamp": "2019-11-22 19:57:00.688Z", "comment": "Us Bots couldve done better", "id": "3f390901-0d62-11ea-9d48-0b1cc2ad2f9d", "video_id": "7d6a05b0-0d4b-11ea-9d48-0b1cc2ad2f9d"}
                    {"author": "user4@bot.com", "upload_timestamp": "2019-11-22 19:56:19.631Z", "comment": "Hello DS", "id": "26c06300-0d62-11ea-9d48-0b1cc2ad2f9d", "video_id": "eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d"}
                    {"author": "user6@bot.com", "upload_timestamp": "2019-11-22 19:56:44.711Z", "comment": "Hello DS", "id": "35b32371-0d62-11ea-9d48-0b1cc2ad2f9d", "video_id": "eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d"}
                  {"author": "clau@sof.pt", "upload_timestamp": "2019-11-22 19:56:54.282Z", "comment": "Friggin Pleb", "id": "3b67b5b0-0d62-11ea-9d48-0b1cc2ad2f9d", "video_id": "7d6a05b0-0d4b-11ea-9d48-0b1cc2ad2f9d"}
    {"author": "pedro@f.ag", "upload_timestamp": "2019-11-22 19:57:06.596Z", "comment": "WTF Dude did you actually?!", "id": "42be8641-0d62-11ea-9d48-0b1cc2ad2f9d", "video_id": "3ffcc5a0-0d4b-11ea-9d48-0b1cc2ad2f9d"}
                    {"author": "user3@bot.com", "upload_timestamp": "2019-11-22 19:56:09.003Z", "comment": "Hello DS", "id": "206a87b1-0d62-11ea-9d48-0b1cc2ad2f9d", "video_id": "eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d"}

(13 rows)

cqlsh:cbd_video_sharing> describe tables;

comment  rating  follower  video  user  event

cqlsh:cbd_video_sharing> SELECT json * FROM follower;

 [json]
-------------------------------------------------------------------------------
 {"user": "user4@bot.com", "video_id": "3ffcc5a0-0d4b-11ea-9d48-0b1cc2ad2f9d"}
 {"user": "user8@bot.com", "video_id": "3ffcc5a0-0d4b-11ea-9d48-0b1cc2ad2f9d"}
 {"user": "user9@bot.com", "video_id": "3ffcc5a0-0d4b-11ea-9d48-0b1cc2ad2f9d"}
 {"user": "user6@bot.com", "video_id": "3ffcc5a0-0d4b-11ea-9d48-0b1cc2ad2f9d"}
 {"user": "user5@bot.com", "video_id": "3ffcc5a0-0d4b-11ea-9d48-0b1cc2ad2f9d"}
   {"user": "ds@test.com", "video_id": "3ffcc5a0-0d4b-11ea-9d48-0b1cc2ad2f9d"}
 {"user": "user3@bot.com", "video_id": "3ffcc5a0-0d4b-11ea-9d48-0b1cc2ad2f9d"}
   {"user": "ds@test.com", "video_id": "bc1bd3b0-0d4b-11ea-9d48-0b1cc2ad2f9d"}
 {"user": "user2@bot.com", "video_id": "3ffcc5a0-0d4b-11ea-9d48-0b1cc2ad2f9d"}
 {"user": "user1@bot.com", "video_id": "3ffcc5a0-0d4b-11ea-9d48-0b1cc2ad2f9d"}
 {"user": "user7@bot.com", "video_id": "3ffcc5a0-0d4b-11ea-9d48-0b1cc2ad2f9d"}

(11 rows)
```


## Queries

### c)

**A. Pesquisa de todos os vídeos de determinado autor (e.x todos os videos do user DS)**
```
cqlsh:cbd_video_sharing> SELECT * FROM Video
                     ... WHERE author = 'ds@test.com'
                     ... ALLOW FILTERING;

 id                                   | author      | upload_timestamp                | description                                   | name                                                       | tags
--------------------------------------+-------------+---------------------------------+-----------------------------------------------+------------------------------------------------------------+----------------------------------------------------------------------------
 eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d | ds@test.com | 2019-11-22 17:17:13.467000+0000 |          I have made some poor life decisions | Watching some guy watch every JonTron video in one sitting | ['JonTron', 'Random', 'Why', 'Why2x', 'Gottem', 'Inception', '#intoodeep']
 3ffcc5a0-0d4b-11ea-9d48-0b1cc2ad2f9d | ds@test.com | 2019-11-22 17:12:23.546000+0000 |                           Me going to the Zoo |                                                    ZooTrip |                                 ['Wholesome', 'Cute', '#First', 'Animals']
 7d6a05b0-0d4b-11ea-9d48-0b1cc2ad2f9d | ds@test.com | 2019-11-22 17:14:06.603000+0000 | Me getting an E Z Sixtuple Kill with Zenyatta |                             Exeperience my Orbs [TEAMKILL] |                ['Overwatch', 'Gaming', 'Rekt', 'Gottem', 'EZ', 'Zenyatta']

(3 rows)
```

**B. Pesquisa de comentários por utilizador, ordenado inversamente pela data (ex. user DS)**
```
cqlsh:cbd_video_sharing> SELECT * FROM Comment_per_author WHERE author='ds@test.com';

 author      | upload_timestamp                | comment         | id                                   | video_id
-------------+---------------------------------+-----------------+--------------------------------------+--------------------------------------
 ds@test.com | 2019-11-22 19:56:40.160000+0000 | WHATS HAPPENING | 32fcb601-0d62-11ea-9d48-0b1cc2ad2f9d | eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d
 ds@test.com | 2019-11-22 19:56:13.170000+0000 |       Wait wtf? | 22e68430-0d62-11ea-9d48-0b1cc2ad2f9d | eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d
 ds@test.com | 2019-11-22 19:55:38.805000+0000 |  Also Second :) | 0e6aae51-0d62-11ea-9d48-0b1cc2ad2f9d | eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d
 ds@test.com | 2019-11-22 19:55:34.830000+0000 |           FIRST | 0c0c24e1-0d62-11ea-9d48-0b1cc2ad2f9d | eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d

(4 rows)
```

**C. Pesquisa de comentários por vídeos, ordenado inversamente pela data (ex. video ZooTrip)**
```
cqlsh:cbd_video_sharing> SELECT * FROM Comment_per_video WHERE video_id = eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9;SELECT * FROM comment_per_video WHERE video_id = eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d ;
SyntaxException: line 1:84 mismatched character ';' expecting set null

 video_id                             | upload_timestamp                | author        | comment         | id
--------------------------------------+---------------------------------+---------------+-----------------+--------------------------------------
 eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d | 2019-11-22 19:57:58.074000+0000 | user6@bot.com |        Hello DS | 616d71a1-0d62-11ea-9d48-0b1cc2ad2f9d
 eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d | 2019-11-22 19:57:54.234000+0000 |   ds@test.com | WHATS HAPPENING | 5f2381a1-0d62-11ea-9d48-0b1cc2ad2f9d
 eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d | 2019-11-22 19:57:44.584000+0000 | user5@bot.com |        Hello DS | 59630881-0d62-11ea-9d48-0b1cc2ad2f9d
 eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d | 2019-11-22 19:57:39.764000+0000 | user4@bot.com |        Hello DS | 56838f41-0d62-11ea-9d48-0b1cc2ad2f9d
 eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d | 2019-11-22 19:57:35.285000+0000 |   ds@test.com |       Wait wtf? | 53d81e51-0d62-11ea-9d48-0b1cc2ad2f9d
 eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d | 2019-11-22 19:57:31.374000+0000 | user3@bot.com |        Hello DS | 518358e1-0d62-11ea-9d48-0b1cc2ad2f9d
 eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d | 2019-11-22 19:57:26.225000+0000 | user2@bot.com |        Hello DS | 4e71ac11-0d62-11ea-9d48-0b1cc2ad2f9d
 eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d | 2019-11-22 19:57:22.123000+0000 | user1@bot.com |        Hello DS | 4bffc1b1-0d62-11ea-9d48-0b1cc2ad2f9d
 eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d | 2019-11-22 19:57:15.591000+0000 |   ds@test.com |  Also Second :) | 481b0d71-0d62-11ea-9d48-0b1cc2ad2f9d
 eccb34b0-0d4b-11ea-9d48-0b1cc2ad2f9d | 2019-11-22 19:57:11.315000+0000 |   ds@test.com |           FIRST | 458e9631-0d62-11ea-9d48-0b1cc2ad2f9d

(10 rows)
```

**D. Pesquisa do rating médio de um vídeo e quantas vezes foi votado; (ex. video Exeperience my Orbs [TEAMKILL] )**
```
cqlsh:cbd_video_sharing> SELECT avg(value), count(value) FROM rating WHERE video_id = 1baab4b0-0d6d-11ea-9d48-0b1cc2ad2f9d ;

 system.avg(value) | system.count(value)
-------------------+---------------------
                 3 |                   3
```

### d)
**1. Os últimos 3 comentários introduzidos para um vídeo;**
```
cqlsh:cbd_video_sharing> SELECT * FROM Comment_per_video WHERE video_id = 19e006d0-0d6d-11ea-9d48-0b1cc2ad2f9d  LIMIT 3;

 video_id                             | upload_timestamp                | author        | comment         | id
--------------------------------------+---------------------------------+---------------+-----------------+--------------------------------------
 19e006d0-0d6d-11ea-9d48-0b1cc2ad2f9d | 2019-11-22 21:17:44.143000+0000 | user6@bot.com |        Hello DS | 86259df1-0d6d-11ea-9d48-0b1cc2ad2f9d
 19e006d0-0d6d-11ea-9d48-0b1cc2ad2f9d | 2019-11-22 21:17:44.140000+0000 |   ds@test.com | WHATS HAPPENING | 862528c1-0d6d-11ea-9d48-0b1cc2ad2f9d
 19e006d0-0d6d-11ea-9d48-0b1cc2ad2f9d | 2019-11-22 21:17:44.137000+0000 | user5@bot.com |        Hello DS | 8624b391-0d6d-11ea-9d48-0b1cc2ad2f9d

(3 rows)
```

**2. Lista das tags de determinado vídeo;**
```
cqlsh:cbd_video_sharing> SELECT tags FROM video WHERE id = 19e006d0-0d6d-11ea-9d48-0b1cc2ad2f9d ;

 tags
--------------------------------------------
 ['Wholesome', 'Cute', '#First', 'Animals']

(1 rows)
```

**3. Todos os vídeos com a tag Aveiro;**
```
You'd need to make the tag 'Aveiro' a constraint key and even then it would be pretty difficult to actually pull off
```

**4. Os últimos 5 eventos de determinado vídeo realizados por um utilizador;**
```
cqlsh:cbd_video_sharing> SELECT * FROM event WHERE user='ds@test.com' AND video_id = 1f1a11e0-0d6d-11ea-9d48-0b1cc2ad2f9d LIMIT 5;

 user        | video_id                             | real_timestamp                  | video_timestamp | action | id
-------------+--------------------------------------+---------------------------------+-----------------+--------+--------------------------------------
 ds@test.com | 1f1a11e0-0d6d-11ea-9d48-0b1cc2ad2f9d | 2019-11-22 21:21:27.469000+0000 |             349 |   Stop | 0b4275d1-0d6e-11ea-9d48-0b1cc2ad2f9d
 ds@test.com | 1f1a11e0-0d6d-11ea-9d48-0b1cc2ad2f9d | 2019-11-22 21:21:23.107000+0000 |             200 |   Play | 08a8df31-0d6e-11ea-9d48-0b1cc2ad2f9d
 ds@test.com | 1f1a11e0-0d6d-11ea-9d48-0b1cc2ad2f9d | 2019-11-22 21:21:20.931000+0000 |             200 |  Pause | 075cd731-0d6e-11ea-9d48-0b1cc2ad2f9d
 ds@test.com | 1f1a11e0-0d6d-11ea-9d48-0b1cc2ad2f9d | 2019-11-22 21:21:18.782000+0000 |             150 |   Play | 0614ede1-0d6e-11ea-9d48-0b1cc2ad2f9d
 ds@test.com | 1f1a11e0-0d6d-11ea-9d48-0b1cc2ad2f9d | 2019-11-22 21:21:16.028000+0000 |               0 |   Play | 0470b3c1-0d6e-11ea-9d48-0b1cc2ad2f9d

(5 rows)
```

**5. Vídeos partilhados por determinado utilizador (maria1987, por exemplo) num
determinado período de tempo (Agosto de 2017, por exemplo);**
```
cqlsh:cbd_video_sharing> SELECT * FROM video WHERE author = 'ds@test.com' AND upload_timestamp > '2019-11-22 21:14:40' AND upload_timestamp < '2019-11-22 21:14:43' ALLOW FILTERING;

 id                                   | author      | upload_timestamp                | description         | name    | tags
--------------------------------------+-------------+---------------------------------+---------------------+---------+--------------------------------------------
 19e006d0-0d6d-11ea-9d48-0b1cc2ad2f9d | ds@test.com | 2019-11-22 21:14:42.493000+0000 | Me going to the Zoo | ZooTrip | ['Wholesome', 'Cute', '#First', 'Animals']

(1 rows)
```

**6. Os últimos 10 vídeos, ordenado inversamente pela data da partilhada;**
```
Would be impossible unless you wanted the last 10 videos for a specific user. Even then you'd need to use Allow Filtering
```

**7. Todos os seguidores (followers) de determinado vídeo;**
```cqlsh:cbd_video_sharing> select * from follower  WHERE video_id = 19e006d0-0d6d-11ea-9d48-0b1cc2ad2f9d ALLOW FILTERING;

 user          | video_id
---------------+--------------------------------------
 user3@bot.com | 19e006d0-0d6d-11ea-9d48-0b1cc2ad2f9d
   ds@test.com | 19e006d0-0d6d-11ea-9d48-0b1cc2ad2f9d
 user9@bot.com | 19e006d0-0d6d-11ea-9d48-0b1cc2ad2f9d
 user6@bot.com | 19e006d0-0d6d-11ea-9d48-0b1cc2ad2f9d
 user5@bot.com | 19e006d0-0d6d-11ea-9d48-0b1cc2ad2f9d
 user4@bot.com | 19e006d0-0d6d-11ea-9d48-0b1cc2ad2f9d
 user8@bot.com | 19e006d0-0d6d-11ea-9d48-0b1cc2ad2f9d
 user7@bot.com | 19e006d0-0d6d-11ea-9d48-0b1cc2ad2f9d
 user2@bot.com | 19e006d0-0d6d-11ea-9d48-0b1cc2ad2f9d

(9 rows)
```


**8. Todos os comentários (dos vídeos) que determinado utilizador está a seguir (following);**
```
Filtering by user would require us to have a second table realting to the user and the videos they're following. Basically, we'd need to simulate a JOIN clause which is unsupported by Cassandra
```

**9. Os 5 vídeos com maior rating;**
```
Again, it'd have to be videos from a specific User.
```


**10. Uma query que retorne todos os vídeos e que mostre claramente a forma pela qual estão
ordenados;**
```
Didn't really get what was being asked but if the interpretation were to be "Allow different methods of ordering specified by a third party" then the answer is N O .
```


**11. Lista com as Tags existentes e o número de vídeos catalogados com cada uma delas;**
```
Besides the fact that getting the full list of tags would be difficult, counting how many videos has them would be flat out a nightmare. This would only be possible if we were to create a new table that would register how many videos each tag has (and which tags exist)
```


# Cassandra Driver
I'll be using the Python Driver but there are others available
For more information on this driver visit https://docs.datastax.com/en/developer/python-driver/3.10/

## Installation
1.	`$sudo pip3 install cassandra-driver`
2.	thats it lol


## Simple CRUD program
Using the same Keyspace from the last section (cbd_video_sharing)

Header / Imports
```
from cassandra.cluster import Cluster
import uuid
import datetime  

cluster = Cluster() # Connect to our Cassandra Server Cluster
session = cluster.connect('cbd_video_sharing') # Connect to our Keyspace


insert_types = {'user': '(email, name, reg_timestamp, username)',
		'video': '(id, author, upload_timestamp, description, name, tags)',
		'comment_per_author': '(id, video_id, author, comment, upload_timestamp)',
		'comment_per_video': '(id, video_id, author, comment, upload_timestamp)',
		'follower': '(user,video_id)',
		'event': '(id, user, video_id, action, real_timestamp, video_timestamp)',
		'rating': '(id, video_id, value)'} # Used to store what data goes into what table
```

Insertion
```
def  insert_data(column_family, data):

	if column_family.lower() not  in insert_types:
		print("Error! There's no table named ", column_family)
		return  0
	else:
		values = insert_types[column_family.lower()]
		try:
			session.execute(f"INSERT INTO {column_family}  {values} VALUES {data}")
			
		except  Exception  as e:
			print("Error! ", e)
			return  0
```

Update
```
def  alter_data(column_family, alteration, condition):

	if column_family.lower() not  in insert_types:	
		print("Error! There's no table named ", column_family)
		return  0
	try:
		session.execute(
			f"UPDATE {column_family} SET {alteration} WHERE {condition}")
	except  Exception  as e:
		print("Error! ", e)
		return  0
```

Lookup
```
def  search_data(column_family, fields, where=None, group_by=None, order_by=None, limit=None, allow_filtering=False):
	if column_family.lower() not  in insert_types:
		print("Error! There's no table named ", column_family)
		return  0
	try:
		query_string =  f"SELECT {fields} FROM {column_family} "
		if where is  not  None:
			query_string +=  f"WHERE {where} "

			if order_by is  not  None:
				query_string +=  f"ORDER BY {order_by} "
			if limit is  not  None:
				query_string +=  f"LIMIT {limit} 
			if allow_filtering:
				query_string +=  f"ALLOW FILTERING"
			return_values = [value for value in session.execute(query_string)]

		return return_values

	except  Exception  as e:
		print("Error! ", e)
		return  0
```

Test
```
def  main():
	#UNCOMMENT TO TEST INSERTION AND ALTERATION
	#insert_data("user", ('test@test.test', 'Python Test',
	# str(datetime.datetime.now())[:-3], 'PyBoy'))
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
```


# Free Theme DB: Shop Stock and Sales

## The Database
For this exercise I got the idea of creating a Database containing data on the sales that took place in a chain of shops. As such the following entities were thought of:
-	**Store**
	-	Contains information on the specific store such as it's id, city, street, zip code, and set of employees
-	**Product**
	-	Has info on a product, i.e, it's name, manufacturer, price, type and stock per store
-	**Clerk**
	-	Stores data about all employees, their names, age, salary, id and store
-	**Sale**
	-	The main entity storing what products (and how many of each) were sold, which clerk sold them, on what store they were sold and when the sale occurred


```mermaid
graph TB
A[Store]
A_attrib_1((id PK_Cl)) --> A
A_attrib_2((city PK_Pt)) --> A
A_attrib_3((street)) --> A
A_attrib_4((zipcode)) --> A
A_attrib_5((employee_set)) --> A

B[Product]
B_attrib_2((id PK_Pt)) --> B
B_attrib_1((name)) --> B
B_attrib_3((manufacturer)) --> B
B_attrib_4((price)) --> B
B_attrib_5((type)) --> B
B_attrib_6((stock_per_store_map)) --> B
```

```mermaid
graph TB
C[Clerk]
C_attrib_1((store_id PK_Pt)) --> C
C_attrib_2((id PK_Cl)) --> C
C_attrib_3((name)) --> C
C_attrib_4((age)) --> C
C_attrib_5((salary)) --> C

D[Sale]
D_attrib_1((store_id PK_Pt)) --> D
D_attrib_2((clerk_id PK_Cl)) --> D
D_attrib_3((sale_timestamp PK_Cl)) --> D
D_attrib_4((products_sold_list)) --> D
```


## Database Creation

### 1. Creating the Keyspace
Using the CQLSH, input the following commands to create the keyspace and each entity:

```
cqlsh> CREATE KEYSPACE cbd_store_chain_db WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 3};

cqlsh> USE cbd_store_chain_db ;
cqlsh:cbd_store_chain_db> 
```

### Step 2 - Creating the Column Families
```
cqlsh:cbd_store_chain_db> CREATE COLUMNFAMILY STORE ( id int, city text, street text, zipcode text, employee_set set<int>, PRIMARY KEY (city, id) );

cqlsh:cbd_store_chain_db> CREATE COLUMNFAMILY PRODUCT ( id int, name text, manufacturer text, price double, type text, stock_per_store map<int, int>,PRIMARY KEY (id) );

cqlsh:cbd_store_chain_db> CREATE COLUMNFAMILY CLERK ( store_id int, id int, name text, age int, salary double, PRIMARY KEY (store_id, id) );

cqlsh:cbd_store_chain_db> CREATE COLUMNFAMILY SALE ( store_id int, clerk_id int, sale_timestamp timestamp, products_sold list<int>, PRIMARY KEY (store_id, clerk_id, sale_timestamp) );


cqlsh:cbd_store_chain_db> DESCRIBE Tables;

product  clerk  store  sale
```


### Step 3 - Creating Secondary Indexes
In order to allow for the query of Products and Clerks by Name, Product by manufacturer the following secondary indexes were created and Clerk by ID:
```
cqlsh:cbd_store_chain_db> CREATE INDEX pname ON PRODUCT (name);

cqlsh:cbd_store_chain_db> CREATE INDEX manname ON PRODUCT (manufacturer);

cqlsh:cbd_store_chain_db> CREATE INDEX cname ON CLERK (name);

cqlsh:cbd_store_chain_db> CREATE INDEX cid ON CLERK (id);
```


### Step 4 - Populating the Database
To make the insertion process easier, the following script made with Cassandra's Python Drive was used:
```
from cassandra.cluster import Cluster
from random import randrange
from datetime import datetime, timedelta


cluster = Cluster() # Connect to our Cassandra Server Cluster
session = cluster.connect('cbd_store_chain_db') # Connect to our Keyspace

  

insert_types = {'product': '(id, manufacturer, name, price, stock_per_store, type)',
		'clerk': '(store_id, id, age, name, salary)',
		'store': '(city, id, employee_set, street, zipcode)',
		'sale': '(store_id, cler_id, sale_timestamp, products_sold)'} # Used to store what data goes into what table)
		}
  
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
    
def  random_date(start, end):
	delta = end - start

	int_delta = (delta.days *  24  *  60  *  60) + delta.seconds

	random_second = randrange(int_delta)

	return start + timedelta(seconds=random_second)

  
def  insert_data(column_family, data):

	if column_family.lower() not  in insert_types:
		print("Error! There's no table named ", column_family)
		return  0
	else:
		values = insert_types[column_family.lower()]
		try:
			session.execute(f"INSERT INTO {column_family}  {values} VALUES {data}")
			
		except  Exception  as e:
			print("Error! ", e)
			return  0  

def  populate_db():
	store_clerk_map = {}

	print("INSERTING DATA TO STORES")
	for i in  range(13):
		# 'store': '(city, id, employee_set, street, zipcode)'		  

		print("INSERTING STORE -", i)
		insert_data(
			"store", (random_cities[randrange(len(random_cities))], i, {}, random_streets[i], random_zipcodes[i]))		

		store_clerk_map[i] = [city, []]

	print("\nINSERTING DATA TO CLERKS")
	for i in  range(30):
		# 'clerk': '(store_id, id, age, name, salary)'
		  
		print("INSERTING CLERK -", i)
		  
		store = randrange(13)
		store_clerk_map[store][1].append(i)

		insert_data("clerk", (store, i, randrange(
			16, 61),random_names[i] ,randrange(400, 601)))


	print("\nINSERTING DATA TO PRODUCTS")
	for i in  range(13):
		# 'product': '(id, manufacturer, name, price, stock_per_store, type)'
	  
		print("INSERTING PRODUCT -", i)
	 
		insert_data(
			"product", (i, random_company_names[randrange(13)], random_product_names[i][0], randrange(2,20) +  float('0'  +  str(randrange(99))) ,{
			store: randrange(30) for store in  range(13)}, random_product_names[i][1]))

	  

	print("\nINSERTING DATA TO SALES")

	d1 = datetime.strptime('01/01/19 00:00:00', '%m/%d/%y %H:%M:%S')
	d2 = datetime.strptime('12/31/19 00:00:00', '%m/%d/%y %H:%M:%S')

  	for i in  range(20):
		# 'sale': '(store_id, clerk_id, sale_timestamp, products_sold)'
  
		print("INSERTING SALE -", i)
  
		products = [randrange(13)]		  

		while randrange(10) >  5:
			products.append(randrange(13))
	  
		while  True:
			store = randrange(13)

		if  len(store_clerk_map[store][1]) ==  0:
			continue
		else:
			break
		
		employee = store_clerk_map[store][1][randrange(
			len(store_clerk_map[store][1]))]
		
		insert_data(
			"sale", (store, employee, str(random_date(d1, d2)), products))
 
def  main():
	populate_db()

if  __name__  ==  "__main__":
	main()
```

Which populates the DB like so:
```
cqlsh:cbd_store_chain_db> SELECT * FROM Store;

 city       | id | employee_set | street           | zipcode
------------+----+--------------+------------------+---------
      Tomar |  1 |         null |   Grays Maltings |   11714
      Tomar |  6 |         null |        Highlands |   30019
     Lisboa |  5 |         null |   Welbourne Road |   07601
     Lisboa |  9 |         null |     Eleanor Glas |   26554
     Aveiro |  7 |         null |   Cotton Furlong |   32780
     Aveiro |  8 |         null |      Upper Sound |   27253
      Porto |  2 |         null |     Hollin Drift |   22630
       Gaia |  4 |         null |  Woodstock Drift |   94070
    Espinho |  3 |         null |  Ashtree Willows |   48430
    Espinho | 10 |         null |   Oakdene Avenue |   79106
    Espinho | 11 |         null | Montpelier Trees |   58501
    Espinho | 12 |         null |       CC Jlo Row |   42069
 Vila Moura |  0 |         null |     Priors Knoll |   42001

(13 rows)

cqlsh:cbd_store_chain_db> SELECT * FROM Clerk;

 store_id | id | age | name               | salary
----------+----+-----+--------------------+--------
       10 |  6 |  59 |         Sonny Frey |    452
       10 |  9 |  16 |  Lyndsey Carpenter |    588
       10 | 24 |  17 |    Luke Broadhurst |    414
       10 | 29 |  42 |        Jayda Bruce |    477
       11 |  7 |  44 |       Ritik Carney |    444
       11 | 13 |  45 |      Josiah Santos |    472
        1 | 23 |  36 |  Huxley Mcloughlin |    456
        8 | 21 |  35 |     Mahamed Alfaro |    590
        0 | 14 |  29 |      Madison Frame |    559
        0 | 17 |  60 |         Leo Waller |    532
        2 |  3 |  17 |     Shannon Whelan |    575
        2 | 22 |  18 |      Rumaysa Bains |    582
        2 | 27 |  48 |        Kyle Valdez |    425
        2 | 28 |  48 |       Ralphie Carr |    524
        4 |  0 |  36 |    Harleigh Rooney |    416
        4 | 12 |  54 |      Huey Arellano |    429
        4 | 18 |  44 |    Tyriq Mackenzie |    423
        7 | 11 |  41 |     Tommie Sargent |    421
        6 |  4 |  46 |        Tamar Poole |    537
        6 | 10 |  31 |         Ivo Osborn |    544
        6 | 15 |  27 |     Franco Cousins |    565
        6 | 26 |  57 | Chantelle Bartlett |    489
        9 |  1 |  56 |      Rachael Johns |    530
        9 | 16 |  50 |       Silas Austin |    405
        9 | 19 |  56 |     Elliott Madden |    405
        9 | 20 |  46 |       Cerys Walter |    452
        9 | 25 |  52 |        Isra Philip |    517
       12 |  2 |  54 |  Mariella Simmonds |    479
       12 |  8 |  30 |        Dalton Drew |    518
        3 |  5 |  54 |      Andrea Cairns |    523

(30 rows)

cqlsh:cbd_store_chain_db> SELECT * FROM Product;

 id | manufacturer                                   | name         | price | stock_per_store                                                                               | type
----+------------------------------------------------+--------------+-------+-----------------------------------------------------------------------------------------------+----------
  5 |                                           Bold | jagermeister |    25 |      {0: 11, 1: 3, 2: 15, 3: 1, 4: 29, 5: 8, 6: 8, 7: 24, 8: 14, 9: 14, 10: 4, 11: 4, 12: 23} |  alcohol
 10 |                          Blacksmith Industries |      catfish |    88 |    {0: 5, 1: 8, 2: 26, 3: 12, 4: 2, 5: 25, 6: 10, 7: 28, 8: 22, 9: 12, 10: 24, 11: 14, 12: 6} |     food
 11 |                              Sounds a bit evil |         kiwi |    59 |     {0: 1, 1: 17, 2: 12, 3: 21, 4: 13, 5: 10, 6: 6, 7: 21, 8: 4, 9: 29, 10: 6, 11: 26, 12: 9} |     food
  1 |                              McAlex Donaldsons |         lego |    28 |       {0: 0, 1: 9, 2: 9, 3: 6, 4: 14, 5: 13, 6: 27, 7: 4, 8: 8, 9: 5, 10: 20, 11: 17, 12: 29} |      toy
  8 | Clifford, Blacksmith And Donaldson, Associates |        sugar |    48 |    {0: 21, 1: 13, 2: 10, 3: 21, 4: 22, 5: 28, 6: 29, 7: 10, 8: 8, 9: 5, 10: 1, 11: 21, 12: 2} |    spice
  0 |                             Clifford of Canada |       coffee |    38 |     {0: 7, 1: 10, 2: 26, 3: 11, 4: 13, 5: 22, 6: 21, 7: 18, 8: 25, 9: 2, 10: 9, 11: 2, 12: 2} |    drink
  2 |                                           Bold |          ham |    48 |      {0: 3, 1: 22, 2: 20, 3: 23, 4: 4, 5: 3, 6: 0, 7: 10, 8: 2, 9: 19, 10: 6, 11: 12, 12: 15} |     food
  4 |                          Blacksmith Industries |        vodka |    61 | {0: 17, 1: 11, 2: 17, 3: 11, 4: 11, 5: 13, 6: 11, 7: 15, 8: 26, 9: 22, 10: 15, 11: 3, 12: 19} |  alcohol
  7 |                                   Just an idea |          tea |    73 |    {0: 3, 1: 13, 2: 12, 3: 6, 4: 21, 5: 26, 6: 21, 7: 14, 8: 29, 9: 3, 10: 20, 11: 3, 12: 22} |    drink
  6 |                         The Blacksmith Council |      bourbon |    81 |   {0: 23, 1: 3, 2: 11, 3: 10, 4: 22, 5: 28, 6: 9, 7: 1, 8: 24, 9: 16, 10: 14, 11: 29, 12: 15} |  alcohol
  9 |                                   Just an idea |         peas |    79 |       {0: 8, 1: 25, 2: 7, 3: 6, 4: 3, 5: 8, 6: 14, 7: 22, 8: 24, 9: 25, 10: 13, 11: 2, 12: 5} |     food
 12 |                     Lauren Clifford Associates |       towels |    92 |    {0: 2, 1: 22, 2: 20, 3: 20, 4: 6, 5: 18, 6: 23, 7: 0, 8: 3, 9: 29, 10: 20, 11: 24, 12: 27} | bathroom
  3 |                                   Just an idea |     football |    76 |       {0: 20, 1: 0, 2: 15, 3: 2, 4: 7, 5: 12, 6: 16, 7: 0, 8: 7, 9: 7, 10: 23, 11: 19, 12: 4} |      toy

(13 rows)

cqlsh:cbd_store_chain_db> SELECT * FROM Sale;

 store_id | clerk_id | sale_timestamp                  | products_sold
----------+----------+---------------------------------+---------------
       10 |        9 | 2019-06-09 09:20:29.000000+0000 |           [9]
       10 |       29 | 2019-04-04 20:51:03.000000+0000 |           [5]
       10 |       29 | 2019-08-20 16:48:36.000000+0000 |      [11, 10]
        8 |       21 | 2019-02-14 07:24:41.000000+0000 |           [9]
        8 |       21 | 2019-03-04 12:40:20.000000+0000 |           [0]
        8 |       21 | 2019-08-19 08:49:52.000000+0000 |           [9]
        2 |       22 | 2019-02-28 17:18:51.000000+0000 |           [7]
        4 |        0 | 2019-01-09 18:45:39.000000+0000 |           [5]
        4 |       12 | 2019-09-18 23:15:08.000000+0000 |           [6]
        4 |       18 | 2019-09-19 09:03:22.000000+0000 |        [0, 8]
        7 |       11 | 2019-05-24 14:22:16.000000+0000 |           [2]
        7 |       11 | 2019-09-19 17:14:43.000000+0000 |           [1]
        7 |       11 | 2019-11-25 10:24:14.000000+0000 |           [9]
        6 |       26 | 2019-10-16 03:39:11.000000+0000 |       [11, 4]
        6 |       26 | 2019-12-08 06:54:44.000000+0000 |        [3, 3]
        9 |       19 | 2019-10-05 05:05:05.000000+0000 |        [1, 0]
       12 |        2 | 2019-03-18 15:31:05.000000+0000 |        [0, 9]
        3 |        5 | 2019-03-02 03:31:31.000000+0000 |    [7, 8, 11]
        3 |        5 | 2019-05-07 10:55:31.000000+0000 |           [6]
        3 |        5 | 2019-05-27 08:51:36.000000+0000 |      [10, 12]

(20 rows)
```

### Step 5 - Updating the Store's Employee Set
If you were paying attention you'd have noticed that our Stores still have their employee set set to empty. Let's change that by adding the following lines to our code and rerunning the program:
```
def main():
	...
	
	print("\nUPDATING THE STORE'S EMPLOYEE SET")
		for store in store_clerk_map:
			new_set =  "{"
			for emp in store_clerk_map[store][1]:
				new_set +=  str(emp) +  ","
			new_set = new_set[:-1] +  "}"

			condition =  "city= '"  + store_clerk_map[store][0] +  "' AND id= "  +  str(store)

			alter_data("store", "employee_set= "  + new_set, condition)
```

Which is gonna repopulate the DB like so:
```
cqlsh:cbd_store_chain_db> SELECT * FROM Store;

 city    | id | employee_set     | street           | zipcode
---------+----+------------------+------------------+---------
  Lisboa |  9 |              {2} |     Eleanor Glas |   26554
  Lisboa | 10 |         {12, 17} |   Oakdene Avenue |   79106
  Aveiro |  0 |       {3, 5, 16} |     Priors Knoll |   42001
  Aveiro |  6 |          {1, 26} |        Highlands |   30019
  Aveiro | 11 |       {0, 8, 28} | Montpelier Trees |   58501
   Porto |  2 | {10, 14, 24, 27} |     Hollin Drift |   22630
   Porto |  4 |  {4, 20, 21, 25} |  Woodstock Drift |   94070
   Porto |  8 |       {7, 9, 29} |      Upper Sound |   27253
    Gaia | 12 |     {11, 15, 22} |       CC Jlo Row |   42069
   Braga |  1 |             {23} |   Grays Maltings |   11714
   Braga |  5 |          {6, 13} |   Welbourne Road |   07601
   Braga |  7 |             {19} |   Cotton Furlong |   32780
 Espinho |  3 |             {18} |  Ashtree Willows |   48430

(13 rows)

cqlsh:cbd_store_chain_db> SELECT * FROM Clerk;

 store_id | id | age | name               | salary
----------+----+-----+--------------------+--------
        5 |  6 |  38 |         Sonny Frey |    571
        5 | 13 |  44 |      Josiah Santos |    491
       10 | 12 |  22 |      Huey Arellano |    595
       10 | 17 |  36 |         Leo Waller |    419
       11 |  0 |  29 |    Harleigh Rooney |    505
       11 |  8 |  33 |        Dalton Drew |    537
       11 | 28 |  21 |       Ralphie Carr |    533
        1 | 23 |  33 |  Huxley Mcloughlin |    533
        8 |  7 |  60 |       Ritik Carney |    561
        8 |  9 |  21 |  Lyndsey Carpenter |    496
        8 | 29 |  58 |        Jayda Bruce |    489
        0 |  3 |  30 |     Shannon Whelan |    560
        0 |  5 |  19 |      Andrea Cairns |    449
        0 | 16 |  42 |       Silas Austin |    581
        2 | 10 |  58 |         Ivo Osborn |    557
        2 | 14 |  34 |      Madison Frame |    516
        2 | 24 |  30 |    Luke Broadhurst |    487
        2 | 27 |  59 |        Kyle Valdez |    575
        4 |  4 |  24 |        Tamar Poole |    551
        4 | 20 |  59 |       Cerys Walter |    583
        4 | 21 |  55 |     Mahamed Alfaro |    505
        4 | 25 |  21 |        Isra Philip |    484
        7 | 19 |  35 |     Elliott Madden |    574
        6 |  1 |  43 |      Rachael Johns |    556
        6 | 26 |  20 | Chantelle Bartlett |    492
        9 |  2 |  32 |  Mariella Simmonds |    548
       12 | 11 |  50 |     Tommie Sargent |    413
       12 | 15 |  39 |     Franco Cousins |    487
       12 | 22 |  36 |      Rumaysa Bains |    577
        3 | 18 |  51 |    Tyriq Mackenzie |    582

(30 rows)

cqlsh:cbd_store_chain_db> SELECT * FROM Product;

 id | manufacturer                                   | name         | price | stock_per_store                                                                               | type
----+------------------------------------------------+--------------+-------+-----------------------------------------------------------------------------------------------+----------
  5 |                          Blacksmith Industries | jagermeister |    91 | {0: 11, 1: 14, 2: 24, 3: 13, 4: 9, 5: 18, 6: 29, 7: 15, 8: 16, 9: 14, 10: 19, 11: 11, 12: 13} |  alcohol
 10 |                              Sounds a bit evil |      catfish |    61 |    {0: 0, 1: 4, 2: 29, 3: 12, 4: 11, 5: 1, 6: 29, 7: 29, 8: 29, 9: 24, 10: 11, 11: 22, 12: 0} |     food
 11 |                              Sounds a bit evil |         kiwi |    25 |   {0: 1, 1: 21, 2: 27, 3: 9, 4: 12, 5: 7, 6: 21, 7: 23, 8: 17, 9: 12, 10: 14, 11: 28, 12: 28} |     food
  1 |                                   Geographical |         lego |    38 |   {0: 23, 1: 13, 2: 1, 3: 14, 4: 22, 5: 18, 6: 18, 7: 19, 8: 14, 9: 29, 10: 7, 11: 22, 12: 3} |      toy
  8 |                     Lauren Clifford Associates |        sugar |    91 |     {0: 25, 1: 19, 2: 9, 3: 29, 4: 27, 5: 2, 6: 8, 7: 12, 8: 5, 9: 21, 10: 9, 11: 29, 12: 10} |    spice
  0 |                         The Blacksmith Council |       coffee |    97 |    {0: 6, 1: 11, 2: 27, 3: 17, 4: 20, 5: 24, 6: 14, 7: 4, 8: 9, 9: 10, 10: 15, 11: 8, 12: 19} |    drink
  2 |                                   Just an idea |          ham |     7 |       {0: 3, 1: 15, 2: 4, 3: 27, 4: 1, 5: 5, 6: 7, 7: 7, 8: 2, 9: 27, 10: 26, 11: 13, 12: 23} |     food
  4 |                            Donaldson Unlimited |        vodka |    92 |    {0: 27, 1: 23, 2: 14, 3: 10, 4: 15, 5: 1, 6: 14, 7: 1, 8: 15, 9: 26, 10: 15, 11: 9, 12: 0} |  alcohol
  7 |                          Blacksmith Industries |          tea |    24 |   {0: 16, 1: 8, 2: 21, 3: 14, 4: 26, 5: 1, 6: 11, 7: 28, 8: 24, 9: 9, 10: 26, 11: 15, 12: 29} |    drink
  6 |                                   Geographical |      bourbon |    62 |        {0: 7, 1: 2, 2: 8, 3: 15, 4: 5, 5: 28, 6: 1, 7: 17, 8: 12, 9: 8, 10: 25, 11: 4, 12: 9} |  alcohol
  9 |                                   Geographical |         peas |    36 |       {0: 0, 1: 21, 2: 21, 3: 26, 4: 5, 5: 1, 6: 9, 7: 18, 8: 14, 9: 0, 10: 7, 11: 2, 12: 22} |     food
 12 | Clifford, Blacksmith And Donaldson, Associates |       towels |    61 |   {0: 25, 1: 22, 2: 10, 3: 18, 4: 25, 5: 29, 6: 28, 7: 5, 8: 21, 9: 0, 10: 25, 11: 15, 12: 5} | bathroom
  3 |                            Donaldson Unlimited |     football |    65 |     {0: 12, 1: 6, 2: 7, 3: 22, 4: 6, 5: 1, 6: 22, 7: 13, 8: 22, 9: 21, 10: 1, 11: 13, 12: 10} |      toy

(13 rows)

cqlsh:cbd_store_chain_db> SELECT * FROM Sale;

 store_id | clerk_id | sale_timestamp                  | products_sold
----------+----------+---------------------------------+---------------
       11 |        8 | 2019-04-21 14:44:49.000000+0000 |        [5, 3]
        1 |       23 | 2019-04-13 16:12:42.000000+0000 |        [9, 3]
        1 |       23 | 2019-06-25 02:24:59.000000+0000 |        [9, 1]
        1 |       23 | 2019-12-12 04:34:56.000000+0000 |           [1]
        8 |        7 | 2019-09-08 09:33:29.000000+0000 |       [8, 10]
        8 |        9 | 2019-06-06 01:42:06.000000+0000 |          [12]
        8 |       29 | 2019-08-31 16:06:47.000000+0000 |           [3]
        0 |        3 | 2019-06-16 14:40:24.000000+0000 |           [9]
        0 |        3 | 2019-10-29 16:32:17.000000+0000 |           [3]
        2 |       24 | 2019-10-06 20:55:41.000000+0000 |           [5]
        4 |       20 | 2019-08-28 02:18:12.000000+0000 |      [10, 11]
        7 |       19 | 2019-03-31 05:07:56.000000+0000 |          [12]
        6 |        1 | 2019-12-22 23:29:41.000000+0000 |           [3]
        6 |        1 | 2019-12-28 22:44:30.000000+0000 |          [12]
        9 |        2 | 2019-01-08 03:23:40.000000+0000 |          [11]
       12 |       11 | 2019-03-06 10:32:24.000000+0000 |     [3, 3, 0]
       12 |       11 | 2019-04-08 23:23:29.000000+0000 |           [8]
       12 |       15 | 2019-04-21 08:13:14.000000+0000 |       [1, 12]
       12 |       22 | 2019-01-16 18:02:07.000000+0000 |           [3]
       12 |       22 | 2019-12-01 23:21:21.000000+0000 |           [9]

(20 rows)
```

### Step 6 - Deleting and from DB
Let's do some deleting operations in the CQLSH:
```
1. Delete the employee number 0 (and update the store he works for accordingly

cqlsh:cbd_store_chain_db> DELETE FROM Clerk WHERE store_id=11 AND id=0;
cqlsh:cbd_store_chain_db>  SELECT id FROM Clerk Where store_id = 11;

 id
----
  8
 28

(2 rows)

cqlsh:cbd_store_chain_db> UPDATE Store SET employee_set = {8,28} WHERE city = 'Aveiro' AND id = 11;
#############################

2. Delete the employee number 5 (and update the store he works for accordingly)cqlsh:cbd_store_chain_db> DELETE FROM Clerk WHERE store_id =0 AND id = 5;

cqlsh:cbd_store_chain_db> select ID from Clerk Where store_id = 0;
 id
----
  3
 16

(2 rows)

cqlsh:cbd_store_chain_db> UPDATE Store SET employee_set = {3,16} WHERE city = 'Aveiro' AND id = 0;

#############################

3. Delete all sales made in store #3

cqlsh:cbd_store_chain_db> DELETE FROM Sale WHERE store_id = 3;

#############################

4. Delete product #5

cqlsh:cbd_store_chain_db> DELETE FROM Product WHERE id = 5;

#############################

5. Delete all stores in Gaia

cqlsh:cbd_store_chain_db> DELETE FROM Store WHERE city = 'Gaia';
```

## Some Queries
```
1. Return all employees from stores in Porto
cqlsh:cbd_store_chain_db> SELECT employee_set FROM store WHERE city = 'Porto';

 employee_set
------------------
 {10, 14, 24, 27}
  {4, 20, 21, 25}
       {7, 9, 29}

(3 rows)


2. Select the latest sale made by Employee 23 working for store 1
cqlsh:cbd_store_chain_db> SELECT * FROM Sale WHERE store_id = 1 AND clerk_id = 23 ORDER BY clerk_id DESC, sale_timestamp DESC LIMIT 1;

 store_id | clerk_id | sale_timestamp                  | products_sold
----------+----------+---------------------------------+---------------
        1 |       23 | 2019-12-12 04:34:56.000000+0000 |           [1]

(1 rows)



3. What's the average salary for all employees?
cqlsh:cbd_store_chain_db> SELECT avg(salary) FROM clerk;

 system.avg(salary)
--------------------
          530.46429

(1 rows)



4. What's product 8's price and type?
cqlsh:cbd_store_chain_db> SELECT price, type FROM product WHERE id = 8;

 price | type
-------+-------
    91 | spice

(1 rows)



5. Find all info on clerk Luke Broadhurst
cqlsh:cbd_store_chain_db> SELECT * FROM Clerk WHERE name='Luke Broadhurst';

 store_id | id | age | name            | salary
----------+----+-----+-----------------+--------
        2 | 24 |  30 | Luke Broadhurst |    487

(1 rows)

#Note: This works due to our secondary index


6. List all products made by Sounds a bit evil
cqlsh:cbd_store_chain_db> SELECT * FROM product WHERE manufacturer='Sounds a bit evil';

 id | manufacturer      | name    | price | stock_per_store                                                                             | type
----+-------------------+---------+-------+---------------------------------------------------------------------------------------------+------
 10 | Sounds a bit evil | catfish |    61 |  {0: 0, 1: 4, 2: 29, 3: 12, 4: 11, 5: 1, 6: 29, 7: 29, 8: 29, 9: 24, 10: 11, 11: 22, 12: 0} | food
 11 | Sounds a bit evil |    kiwi |    25 | {0: 1, 1: 21, 2: 27, 3: 9, 4: 12, 5: 7, 6: 21, 7: 23, 8: 17, 9: 12, 10: 14, 11: 28, 12: 28} | food

(2 rows)
#Note: This works due to our secondary index


7. Get info about the product named Bourbon
cqlsh:cbd_store_chain_db> SELECT * FROM product WHERE name='bourbon';

 id | manufacturer | name    | price | stock_per_store                                                                        | type
----+--------------+---------+-------+----------------------------------------------------------------------------------------+---------
  6 | Geographical | bourbon |    62 | {0: 7, 1: 2, 2: 8, 3: 15, 4: 5, 5: 28, 6: 1, 7: 17, 8: 12, 9: 8, 10: 25, 11: 4, 12: 9} | alcohol

(1 rows)

#Note: This works due to our secondary index


8. What store does clerk #13 work for?
cqlsh:cbd_store_chain_db> SELECT store_id FROM clerk WHERE id = 13;

 store_id
----------
        5

(1 rows)

#Note: This works due to our secondary index


9. List all sales made by clerk # 11 between January and April

cqlsh:cbd_store_chain_db> SELECT * FROM sale WHERE clerk_id = 11 AND sale_timestamp > '2019-01-01 00:00:00' AND sale_timestamp < '2019-04-30 23:59:59' ALLOW FILTERING;

 store_id | clerk_id | sale_timestamp                  | products_sold
----------+----------+---------------------------------+---------------
       12 |       11 | 2019-03-06 10:32:24.000000+0000 |     [3, 3, 0]
       12 |       11 | 2019-04-08 23:23:29.000000+0000 |           [8]

(2 rows)


 
10. List all products sold at store 12
cqlsh:cbd_store_chain_db> SELECT products_sold FROM sale WHERE store_id = 12;

 products_sold
---------------
     [3, 3, 0]
           [8]
       [1, 12]
           [3]
           [9]

(5 rows)



11. How many lego are in stock at all stores?
cqlsh:cbd_store_chain_db> SELECT stock_per_store FROM product WHERE name = 'lego';

 stock_per_store
---------------------------------------------------------------------------------------------
 {0: 23, 1: 13, 2: 1, 3: 14, 4: 22, 5: 18, 6: 18, 7: 19, 8: 14, 9: 29, 10: 7, 11: 22, 12: 3}

(1 rows)
```


# Author
### Diogo Silva, 89348
