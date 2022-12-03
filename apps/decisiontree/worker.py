from multiprocessing.pool import ThreadPool
from time import sleep


# task executed in a worker thread
def task():
    # report a message
    print('Worker executing task...')
    # block for a moment
    sleep(1)


# initialize a worker in the thread pool
def initialize_worker():
    # report a message
    print('Initializing worker...')


# protect the entry point
if __name__ == '__main__':
    # create and configure the thread pool
    with ThreadPool(2, initializer=initialize_worker) as pool:
        # issue tasks to the thread pool
        for _ in range(40):
            _ = pool.apply_async(task)
        # close the thread pool
        pool.close()
        # wait for all tasks to complete
        pool.join()
