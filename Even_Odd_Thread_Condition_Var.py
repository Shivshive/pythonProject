import threading

cv = threading.Condition()
counter = 0
limit = 10


class Even_printer(threading.Thread):

    def __init__(self):
        super(Even_printer, self).__init__()

    def run(self):
        global counter
        global limit

        flag = True
        while flag:
            with cv:
                if counter % 2 == 0 and counter <= limit:
                    print("E", counter)
                    counter += 1
                    # cv.notify()
                    # cv.wait()
                cv.notify()
                if counter > limit:
                    flag = False
                    print(f"{threading.current_thread().name} has set flag to {flag}")
                    # cv.notify()
                    continue

                cv.wait()

        print(f"{threading.current_thread().name} has finished execution")


class Odd_printer(threading.Thread):

    def __init__(self):
        super(Odd_printer, self).__init__()

    def run(self):
        global counter
        global limit

        flag = True
        while flag:
            with cv:
                if counter % 2 != 0 and counter <= limit:
                    print("O", counter)
                    counter += 1
                    # cv.notify()
                    # cv.wait()
                cv.notify()
                if counter > limit:
                    flag = False
                    print(f"{threading.current_thread().name} set flag to {flag}")
                    cv.notify()
                    continue

                cv.wait()

        print(f"{threading.current_thread().name} has finished execution")


if __name__ == "__main__":
    even_thread = Even_printer()
    odd_thread = Odd_printer()

    even_thread.start()
    odd_thread.start()

    even_thread.join()
    odd_thread.join()
