class Functions():
    @staticmethod
    def intersect(a, b):
        # print(a, b)
        """ return the intersection of two lists """
        # first case, we have , in gs a and gs b
        try:
            b_a = a.split(',')
            b_b = b.split(',')
            return list(set(b_a) & set(b_b))
        except:
            pass

    @staticmethod
    def generate_possibilities(lista):
        index = 0
        list = set()
        # adiciono os individuos sozinhos
        for k in lista:
            list.add(k)
        # dps add: a+b, a+d
        for k in range(1, len(lista)):
            list.add(lista[0] + lista[k])

        elem = ''
        for k in range(1, len(lista)):
            elem += str(lista[k])
        elem = lista[0] + elem
        list.add(elem)

        return list

    @staticmethod
    def parallel(x):
        str = ('+(%s;)' % x)
        return str