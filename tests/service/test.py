a=1
print( not isinstance(a,str))


if __name__ == "__main__":
    codes = [1,2,3,4,5,6,7,8,9,10]
    offset = 0
    limit = 3
    total = len(codes)
    while offset < total:
        print("offet:{} limit:{} partial codes:{}".format(offset,limit, codes[offset:offset+limit]))
        offset += limit