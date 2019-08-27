import time

class Timer:
    """
    Создает контекстный менеджер, а также работает как декоратор
    """
    def __init__(self, num_runs=10):
        self.num_runs = num_runs

    def __call__(self, func):
        def wrapper(*args, num_runs=10):
            avg_time = 0
            for _ in range(self.num_runs):
                t0 = time.time()
                func(*args)
                t1 = time.time()
                avg_time += (t1 - t0)
            avg_time /= self.num_runs
            print("Результат работы функции {}({}) без рекурсии: {}".format(func.__name__, *args, func(*args)))
            print("Количество запусков функции {}({}): {}".format(func.__name__, *args, self.num_runs))
            print("Среднее время выполнения (сек): %.20f" % avg_time)
            return func
        return wrapper

    def __enter__(self):
        print("Enter")
        self.t0 = time.time()
        return self
    
    def __exit__(self, *crap):
        print("Exit")
        self.t1 = time.time()
        run_time = self.t1 - self.t0
        print("Время выполнения (сек): %.20f" % run_time)

# задаем кол-во прогонов
timer = Timer(20)
# измеряем время выполнения при помощи декоратора (~0.сек)
@timer
def fibo(n):
    # print("Выполняется fibo без рекурсии")
    current = 0
    after = 1
    for _ in range(n):
        current, after = after, current + after
    return current

def fibo_rec(n):
    # print("Выполняется fibo с рекурсий")
    if n == 0:
        return 0
    if n == 1:
        return 1
    return fibo_rec(n-1) + fibo_rec(n-2)

fibo(40)

# измеряем время выполнения при помощи контекстного менеджера (~40 сек)
with Timer():
    result = fibo_rec(40)
    print("\nРезультат работы функции fibo(40) с рекурсией:", result)

