cars = range(10)

itercars = iter(cars)
# add 'next(itercars)' here if you also want to skip the first
prev = next(itercars)
for car in itercars:
    print prev
    # do work on 'prev' not 'car'
    # at end of loop:
    prev = car
# now you can do whatever you want to do to the last one on 'prev'