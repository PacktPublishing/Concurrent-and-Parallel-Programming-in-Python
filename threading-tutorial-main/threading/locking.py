import threading


counter = 0

lock = threading.Lock()

# lock.acquire()
# lock.release()


def increment():
    global counter
    for i in range(10**6):
        with lock:
            counter += 1
            # more locking
            # more locking

threads = []
for i in range(4):
    x = threading.Thread(target=increment)
    threads.append(x)

for t in threads:
    t.start()

for t in threads:
    t.join()

print('Counter value:', counter)


# counter = x
# thread is locking
# thread <- counter = x
# thread -> counter = counter + 1 -> counter = x + 1
# release locking
# thread 2 is locking
# thread 2 <- counter = x + 1
# thread 2 -> counter = counter + 1 -> counter = x +1 + 1
# release locking

# counter = x + 2