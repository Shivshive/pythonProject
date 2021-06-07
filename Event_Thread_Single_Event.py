import threading

counter = 0
limit = 10

ev = threading.Event()


class Even_Printer(threading.Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        global counter
        global limit

        flag = True
        while flag:
            if counter % 2 == 0:
                print(f"{threading.current_thread().name} Inside If to print counter {counter}")
                print("E", counter)
                counter += 1
                print(f"{threading.current_thread().name} Inside If counter += 1 {counter}")

            if counter > limit:
                flag = False
                print(f"{threading.current_thread().name} setting flag to {flag}")
                ev.set()
                continue

            print(f"{threading.current_thread().name} ev.set()")
            ev.set()
            print(f"{threading.current_thread().name} ev.wait()")
            ev.wait()

        print(f"{threading.current_thread().name} has finished execution")


class Odd_printer(threading.Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        global counter
        global limit

        flag = True
        while flag:
            print(f"{threading.current_thread().name} ev.wait()")
            ev.wait()
            if not counter % 2 == 0:
                print(f"{threading.current_thread().name} Inside If to print counter {counter}")
                print("O", counter)
                counter += 1
                print(f"{threading.current_thread().name} Inside If counter += 1 {counter}")

            if counter > limit:
                print(f"{threading.current_thread().name} is setting flag to {flag}")
                flag = False
                ev.set()
                continue

            print(f"{threading.current_thread().name} ev.set()")
            ev.set()

        print(f"{threading.current_thread().name} has finished exeuction.")


if __name__ == "__main__":
    e_thread = Even_Printer()
    o_thread = Odd_printer()

    e_thread.start()
    o_thread.start()

    e_thread.join()
    o_thread.join()
