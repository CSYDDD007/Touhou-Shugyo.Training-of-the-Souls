class A():
    def __init__(self):
        print('a')
        self.b = self.A_1()
        self.speed = 10
    class A_1():
        def __init__(self):
            print('b')
AA = A()

a = {'a':0, 'self':AA}
exec("self.speed = 20", globals(), a)
print(a.get('b'))
print(AA.speed)
n = 1_000_000
nn = f"{n:,}"
print(nn)