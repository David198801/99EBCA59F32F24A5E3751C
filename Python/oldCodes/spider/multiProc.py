import multiprocessing
import os



datas = {'A':'AQI','P':'P25','O':'O3', 'S':'SO2', 'N':'NO2', 'C':'CO'}

def run_proc(name):
    print datas[name]

if __name__ == '__main__':
    for i in datas:
        p = multiprocessing.Process(target=run_proc, args=(i))
        p.start()