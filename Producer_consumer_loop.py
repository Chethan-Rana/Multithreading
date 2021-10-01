import concurrent.futures
import logging
import queue
import random
import threading
import time

 

def producer(queue, event):

    while not event.is_set():
        for i in range(100):
            message = random.randint(1, 101)
            logging.info("Producer set %s message: %s",i, message)
            queue.put(message)

 

    logging.info("Producer received event. Exiting")
    return 0

 
def consumer(queue, event):
    
    while not event.is_set() or not queue.empty():
        for i in range(100):
            message = queue.get()
            logging.info(
                "Consumer storing %s message: %s (size=%d)", i, message, queue.qsize()
            )

 

    logging.info("Consumer received all values. Quiting")
    return 0

 

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

 

    pipeline = queue.Queue(maxsize=10)
    event = threading.Event()
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(producer, pipeline, event)
        executor.submit(consumer, pipeline, event)


        time.sleep(0.1)
        logging.info("Main: about to set event")
        event.set()
