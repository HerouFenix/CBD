import redis


r = redis.Redis()

#Idea:
#   Each User produces 2 lists:
#       users:messages:<username> -> Stores all messages the user specified in <username> has created
#       users:subscriptions:<username> -> Stores all users a given user (specified in <username>) is subscribed to

# There's some hashes with user's infos:
#       users:info:<username> -> Used to store info on all users (Name ; Password ; Posts ; Subscriptions)


    

    

#Check if given user exists
def check_user_existance(username):
    all_users = [str(key, "utf-8") for key in list(r.keys("users:info:"+username))]
    if len(all_users) == 0:
        return False
    return True


#Create a new user
def create_user(username,password):
    r.hset("users:info:"+username,'name',username)
    r.hset("users:info:"+username,'password',password)
    r.hset("users:info:"+username,'posts','0')
    r.hset("users:info:"+username,'subscriptions','[]')


def main():
    current_user = None
    while True:
        if current_user:
            option = input(
                    "\nWhat would you like to do?\n" +
                    " 1 - Logout\n" +
                    " 2 - Subscribe to user\n" +
                    " 3 - Unsubscribe from user\n" +
                    " 4 - Post Message\n" +
                    " 5 - Read Subscriptions\n" +
                    " 6 - Read your posts\n" +
                    " 7 - Your Info\n" +
                    " 8 - List all users\n" +
                    " ENTER - Quit\n"
                    )
            if len(option) == 0:
                break

            elif option == "1": #LOGOUT
                print("See ya {}!".format(current_user))
                current_user = None
            
            elif option == "2": #SUBSCRIBE
                sub = input("Type the username of the user you wish to subscribe to: ")
                user_subscriptions = [str(key, "utf-8") for key in list(r.lrange("users:subscriptions:"+username,0,-1))]

                if not check_user_existance(sub):
                    print("Sorry but the user {} doesn't exist!".format(sub))
                    continue
                elif sub in user_subscriptions:
                    print("You're already subscribed to {}!".format(sub))
                    continue
                else:
                    r.rpush("users:subscriptions:"+current_user, sub)
                    r.hset("users:info:"+current_user,"subscriptions", str([str(key, "utf-8") for key in list(r.lrange("users:subscriptions:"+username,0,-1))]))

                    print("Subscribed to {} successfully!".format(sub))                    

            elif option == "3": #UNSUBSCRIBE
                sub = input("Type the username of the user you wish to unsubscribe from: ")
                user_subscriptions = [str(key, "utf-8") for key in list(r.lrange("users:subscriptions:"+username,0,-1))]

                if sub in user_subscriptions:
                    r.lrem("users:subscriptions:"+username,1,sub)
                    r.hset("users:info:"+current_user,"subscriptions", str([str(key, "utf-8") for key in list(r.lrange("users:subscriptions:"+username,0,-1))]))
                    print("Unsubscribed from {} successfully!".format(sub))
                else:
                    print("You're not subscribed to {}!".format(sub))
                
            elif option == "4": #POST MESSAGE
                msg = input("Write your message: ")

                r.rpush("users:messages:"+current_user, msg)
                r.hset("users:info:"+current_user,"posts", str(int(str(r.hget("users:info:"+current_user,'posts'), "utf-8"))+1))
                print("Message posted successfully!")                    

            elif option == "5": #READ SUBSCRIPTIONS MESSAGES
                user_subscriptions = [str(key, "utf-8") for key in list(r.lrange("users:subscriptions:"+username,0,-1))]

                for user in user_subscriptions:
                    print("\n"+user+"'s messages:")
                    
                    for message in [str(key, "utf-8") for key in list(r.lrange("users:messages:"+user,0,-1))]:
                        print("->     "+message)

            elif option == "6": #READ OWN MESSAGES
                print("\nYour messages:")
                for message in [str(key, "utf-8") for key in list(r.lrange("users:messages:"+current_user,0,-1))]:
                    print("->     "+message)

            elif option == "7": #USER INFO
                print("\nYour INFO:")
                info = [str(key, "utf-8") for key in list(r.hgetall("users:info:"+current_user))]
                for i in info:
                    print(i + " - " + str(r.hget("users:info:"+current_user,i), "utf-8"))

            elif option == "8": #USER INFO
                print("\nAll users:")
                for i in [str(key, "utf-8") for key in list(r.keys("users:info:*"))]:
                    print(str(r.hget(i,'name'),'utf-8'))
        else:
            option = input(
                    "\nWhat would you like to do?\n" +
                    " 1 - Login\n" +
                    " 2 - Create new user\n" +
                    " ENTER - Quit\n"
                    )

            if len(option) == 0:
                break

            elif option == "1": #LOGIN
                username = input("Type in your username: ")
                password = input("Type in your password: ")

                if check_user_existance(username):
                    if str(r.hget('users:info:'+username,'password'),'utf-8') == password:
                        current_user = username
                        print("Login Success!")
                        continue
                
                print("Login Failed!")
                continue

            elif option == "2": #CREATE USER
                username = input("Type in a username: ")
                password = input("Type in a password: ")

                if check_user_existance(username):
                    print("Creation failed! That username is already taken")
                else:
                    create_user(username,password)
                    print("User created successfully!")
                    current_user = username
                

if __name__ == '__main__':
    
    main()
    print("Smell ya later")

