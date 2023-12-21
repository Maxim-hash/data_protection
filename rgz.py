from lab3 import *

COLORS_NUM = {
    "R" : 0,
    "G" : 1,
    "B" : 2
}

a = 5

def get_prime(left, right):
    while True:
        p = random.randint(left, right)
        if is_prime(p):
            return p

def read_graph(filename):
    vertex_array = {'from': [], 'to': []}
    with open(filename, 'r') as f:
        vertex_num, edge_num = [int(x) for x in next(f).split()]
        for i, line in enumerate(f):
            if i == edge_num:
                colors = [x for x in line.split()]
                break
            fr, to = [int(x) for x in line.split()]
            vertex_array['from'].append(fr)
            vertex_array['to'].append(to)
    return vertex_array, colors, vertex_num


def main():
    vertex_array, colors, vertex_count = read_graph("graph7.txt")
    if(vertex_count > 1001):
        print("Ошибка. Кол-во вершин больше 1001")
        return
    if(len(vertex_array["from"]) > vertex_count * vertex_count):
        print("Ошибка. Кол-во ребер больше количества вершин  более чем в два раза")
        return

    print(f'Граф содержит {vertex_count} вершин и {len(vertex_array["from"])} ребер:')
    for i in range(len(vertex_array["from"])):
        print(f'{vertex_array["from"][i]} {vertex_array["to"][i]}')
    print(f'Раскраска: {colors}')


    color_name = ['R', 'G', 'B']
    color_name_shuffle = color_name.copy()

    while color_name_shuffle == color_name:
        random.shuffle(color_name_shuffle)
    
    dependence = {i : j for i, j in zip(COLORS_NUM.keys(), color_name_shuffle)}

    colors_shuffle = ['' for _ in range(len(colors))]
    for i in range(vertex_count):
        colors_shuffle[i] = dependence[colors[i % 3]]

    print(f'Перекрашеный граф Алисой: {colors_shuffle}')

    r = list()
    for i in colors_shuffle:
        r.append(random.getrandbits(32) >> 2 << 2 | COLORS_NUM[i])

    print(f'r = {r}')



    p = [get_prime(0, 10 ** 9) for _ in range(vertex_count)]
    q = [get_prime(0, 10 ** 9) for _ in range(vertex_count)]
    n = [p[i] * q[i] for i in range(vertex_count)]
    phi = [(p[i] - 1) * (q[i] - 1) for i in range(vertex_count)]
    d = [get_coPrime(phi[i]) for i in range(vertex_count)]
    c = [extented_gcd(d[i], phi[i])[1] for i in range(vertex_count)]
    for i in range(vertex_count):
        while c[i] < 0:
            c[i] += phi[i]

    Z = [rapid_pow(r[i], d[i], n[i]) for i in range(vertex_count)]
    already = set()
    for _ in range(a):
        requested = random.randint(0, vertex_count-1)
        while requested in already:
            requested = random.randint(0, vertex_count-1)
        already.add(requested)
        Z1 = rapid_pow(Z[vertex_array["from"][requested] - 1], 
                       c[vertex_array["from"][requested] - 1], 
                       n[vertex_array["from"][requested] - 1])
        Z2 = rapid_pow(Z[vertex_array["to"][requested] - 1], 
                       c[vertex_array["to"][requested] - 1], 
                       n[vertex_array["to"][requested] - 1])
        
        r1 = to_bin(Z1)
        r2 = to_bin(Z2)
        
        if(r1[0:2] == r2[0:2]):
            print(f"Алиса пыталась обмануть боба!\nу ребра {requested + 1} соединяющего вершины {vertex_array['from'][requested]} и {vertex_array['to'][requested]} совпадают два младших бита\n{r1} | {r2}")
            return
        else:
            print(f"у ребра {requested + 1} соединяющего вершины {vertex_array['from'][requested]} и {vertex_array['to'][requested]} два младших бита различны")
if __name__ == "__main__":
    main()

