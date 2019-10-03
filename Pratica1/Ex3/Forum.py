import redis

r = redis.Redis()

def main():
    print(r.info())
if __name__ == '__main__':
    main()
