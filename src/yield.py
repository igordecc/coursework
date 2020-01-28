def yiedlol():
    for i in range(10):
        yield i

if __name__ == '__main__':
    for i in yiedlol():
        print(i)
