def make_averager():
    count = 0
    total = 0

    def averager(new_value):
        nonlocal count,total
        count += 1
        total += new_value
        return total/count

    return averager


avg = make_averager()
print( avg(10) )
print( avg(15) )