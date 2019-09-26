# Prática CBD - 1

# Redis Data Types

## String

In Redis, strings are serialized characters in C. Integers are stored in Redis as a string.
### SET key string optional nx|xx
Setting a string value with a characters and an integer

`SET Book:1 "Infinite Jest"`
**Key**: Book:1  ; **Value**: "Infinite Jest"

### GET key 
Getting the value of a key

`GET Book:1`
**Key**: Book:1 ; 
**Return**: "Infinite Jest"

### INCR key & INCRBY key integer
Increase a string "integer" value by 1 or by the value specified in integer. If the value isn't a "string integer" we get returned **(error) ERR value is not an integer or out of range**
```
 SET    Book:2 1 
 INCR   Book:2   
 INCRBY Book:2 5
 ``` 
**Return**: (integer) 2
**Return**: (integer) 7

### DECR key & DECRBY key integer
Decrease a string "integer" value by 1 or by the value specified in integer. If the value isn't a "string integer" we get returned **(error) ERR value is not an integer or out of range**

`SET    Book:3 5 
 DECR   Book:3   
 DECRBY Book:3 2`
**Return**: (integer) 4
**Return**: (integer) 2

### MSET key1 string key2 string (...)
Set multiple key-string value

`MSET Person:1 "DS" Person:2 "Adolfo Dias" Person:3 "Mafalda Meopito"`
**Keys**: Person:1 ,Person:2 ,Person:3 ; **Values**: "DS", "Adolfo Dias", "Mafalda Meopito"


### MGET key1 key2 (...)
Get multiple key's values

`MGET Person:1 Person:2 Person:3`
**Return**: 1)"DS" 2)"Adolfo Dias" 3)"Mafalda Meopito"

## List

Lists in Redis are ordered collections of Redis strings that allows for duplicates values. They're implemented via linked-lists. Basically, a collection of one or more values is a List.

### LPUSH key value & RPUSH key value
The **LPUSH** command adds one or more elements to the front of a list, the **RPUSH** command adds one or more elements to the end of a list.

```
 LPUSH Game:1 "Overwatch"   
 LPUSH Game:1 "CS:GO"       
 RPUSH Game:1 "TES: Skyrim"
 ```
**Key**: Game:1  ; **Value(s)**: "Overwatch", "CS:GO", "TES: Skyrim"

### LRANGE key start end
Getting the values of a List from index start to index end

`LRANGE Game:1`
**Key**: Game:1 ; 
**Return**: 1)"CS:GO" 2)"Overwatch" 3)"TES:Skyrim"

### LINDEX key index
Getting the value of a list at given index

`LINDEX Game:1 0`
**Return**: "CS:GO"


### LPOP key & RPOP key
The **LPOP** command remove the first element from the list and returns it the calling client while the **RPOP** command removes and returns the last element of the list.
```
 LPOP    Game:1  
 RPOP    GAME:1
```
**Return**: "CS:GO"
**Return**: "TES: Skyrim"


### Other Commands
#### LTRIM key start end
Cuts down an existing list from start to end

#### BLOP key second delay & BROP key second delay
To add in implementing simple queues in Redis using the List data-type, the **BLPOP** and **BRPOP** commands are similar to LPOP and RPOP commands only they will block sending a return back to client if the list is empty. These blocking commands return two values, the key of the list and an element.

## Hash

Hash data structures map one or more fields to corresponding value pairs. In Redis, all hash values must be Redis strings with unique field names. Basically a "dictionary" of fields and values

### HSET key field value & HMSET key field1 value1 field 2 value2 (...)
Set the value of a single field or set multiple field-values using the **HMSET** command. We can think of the **KEY** as being the dictionary (as in the actual book), the **FIELD** as being the word in the dictionary, and the **VALUE** the word's meaning

```
 HSET Game:Overwatch Type "FPS"
 HSET Game:CS:GO     Type "FPS" Developer "Valve" Price "Free" 
 ```
**Keys**: Game:Overwatch, Game:CS:GO ; **Field-Value**: Type-FPS, Type-FPS, Developer-Valve, Price-Free

### HGET key field & HMGET key field1 field2 (...) & HGETALL
Get the value of a specified field (or multiple with **HMGET**, or all with **HGETALL**)

```
 HGET    Game:Overwatch Type
 HMGET   Game:CS:GO     Type Developer
 HGETALL Game:CS:GO
 ```
**Return**: "FPS" ; "FPS", "Valve" ; "Type - FPS", "Developer - Valve", "Price - Free"


### Other Commands
#### HEXISTS key field
Returns 1 if given field exists or 0 if it doesn't
#### HLEN key 
Returns the number of fields in given key
#### HKEYS key 
Returns all fields in given key
#### HVALS key 
Returns all values in given key
#### HDEL key field
Delete a given field inside the key
#### HINCRBY key field value
Increases the integer value of a hash field's value by a given number.
