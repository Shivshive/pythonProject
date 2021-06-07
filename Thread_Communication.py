import threading
import time


num = 0
con = threading.Condition()


class Producer(threading.Thread):
    """Producer"""
    def run(self):
        global num
        # Get a lock
        con.acquire()
        while True:
            num += 1
            print('Produced 1, There are now {0}.'.format(num))
            time.sleep(1)
            if num >= 5:
                print('Has reached 5, no longer production')
                # Wake up consumers
                con.notify()
                # Wait release lock; wake up - get lock.
                con.wait()
        # Release lock
        con.release()


class Customer(threading.Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.money = 7

    def run(self):
        global num
        while self.money > 0:
            # Because scenes are multiple consumers rushing, if lock operations are taken out of loop, such as producers,
            # Then one consumer thread will lock the entire loop when it is awakened, unable to achieve another consumer snap-up.
            # Add a set of "Get Locks - Release Locks" to the loop, where one consumer releases the lock after the purchase is complete and the other consumer can get locks to participate in the purchase.
            con.acquire()
            if num <= 0:
                print('No more, {0} notify producer.'.format(
                    threading.current_thread().name))
                con.notify()
                con.wait()
            self.money -= 1
            num -= 1
            print('{0} consumed 1, {1} left.'.format(
                threading.current_thread().name, num))
            con.release()
            time.sleep(1)
        print('{0} No money back home.'.format(threading.current_thread().name))


if __name__ == '__main__':
    p = Producer(daemon=True)
    c1 = Customer(name='Customer-1')
    c2 = Customer(name='Customer-2')
    p.start()
    c1.start()
    c2.start()
    c1.join()
    c2.join()