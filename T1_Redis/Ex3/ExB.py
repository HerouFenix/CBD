import redis

r = redis.Redis()

class SimplePostSet:
    def __init__(self):
        self.r = redis.Redis()
        self.key = "users" #Key set for users' name

    def save_user(self,username):
        self.r.sadd(self.key,username)

    def get_user(self):
        return [str(key, "utf-8") for key in list(self.r.smembers(self.key))]
    
    def get_all_keys(self):
        return [str(key, "utf-8") for key in list(r.keys("*"))]
    
class SimplePostList:
    def __init__(self):
        self.r = redis.Redis()
        self.key = "users" #Key set for users' name

    def save_user_left(self,username):
        self.r.lpush(self.key,username) #Note: No clue why this is bugging out. Both self.key and username are of <class 'str'> so this should work...
    
    def save_user_right(self,username):
        self.r.rpush(self.key,username)

    def get_user(self):
        all_users = []
        for i in range(0,self.r.lrange(self.key)):
            all_users.append(str(self.r.lindex(self.key,i)),'utf-8')
        return all_users

    def get_all_keys(self):
        return [str(key, "utf-8") for key in list(self.r.keys("*"))]


class SimplePostHash:
    def __init__(self):
        self.r = redis.Redis()
        self.key = "people:users:" #Key for users' name
        self.incrementer = -1
        self.name = "people" #Hash map's name
   
    def save_user(self,username):
        self.incrementer += 1
        self.r.hset(self.name,str(self.key) + str(self.incrementer),username)

    def get_user(self):
        all_users = []
        for i in range(0,self.incrementer+1):
            all_users.append(str(self.r.hget(self.name, str(self.key) + str(i)), 'utf-8'))
        return all_users
   
    def get_all_keys(self):
        return [str(key, "utf-8") for key in list(r.keys("*"))]

def main():
    post_set = SimplePostSet()

    #Set some users
    users = ["DS", "Claudia", "Vasco", "Vasconcelos"]
    
    print("##############Set##############")
    for username in users:
        post_set.save_user(username)
    
    print(post_set.get_all_keys())
    print(post_set.get_user())

    print("##############Hash##############")
    post_hash = SimplePostHash()
    for username in users:
        post_hash.save_user(username)
    
    print(post_hash.get_all_keys()) 
    print(post_hash.get_user())

    print("##############List##############")
    post_list = SimplePostList()
    for username in users:
        post_list.save_user_left("oof")

    print(post_list.get_all_keys())
    print(post_list.get_user())

if __name__ == '__main__':
    main()

