import threading

ev = threading.Event()
ov = threading.Event()
counter = 1
limit = 10

# TODO: Need to understand the deep difference between Event and Condition variable

class Even_printer(threading.Thread):

    def __init__(self):
        super(Even_printer, self).__init__()

    def run(self):
        global counter
        global limit

        flag = True
        while flag:
            ev.wait()
            if counter % 2 == 0 and counter <= limit:
                print("E", counter)
                counter += 1
                # cv.notify()
                # cv.wait()
            ov.set()
            if counter > limit:
                flag = False
                print(f"{threading.current_thread().name} has set flag to {flag}")
                # ev.notify()
                continue

            ev.clear()

        print(f"{threading.current_thread().name} has finished execution")


class Odd_printer(threading.Thread):

    def __init__(self):
        super(Odd_printer, self).__init__()

    def run(self):
        global counter
        global limit

        flag = True
        while flag:
            ov.wait()
            if counter % 2 != 0 and counter <= limit:
                print("O", counter)
                counter += 1
                # cv.notify()
                # cv.wait()
            ev.set()
            if counter > limit:
                flag = False
                print(f"{threading.current_thread().name} set flag to {flag}")
                # ev.notify()
                continue

            ov.clear()

        print(f"{threading.current_thread().name} has finished execution")


if __name__ == "__main__":
    even_thread = Even_printer()
    odd_thread = Odd_printer()

    ev.set()

    even_thread.start()
    odd_thread.start()

    even_thread.join()
    odd_thread.join()
