"""Minimal group and partial-representation routines for the bundled checks."""
from collections import defaultdict
from itertools import product

P = 1000003


class Hopf:
    """n = dim ; mul[i][j] = dict k->c ; comul[i] = list (a,b,c) ; S[i] = dict ; unit = dict"""
    def __init__(self, n, mul, comul, S, unit, name=""):
        self.n, self.mul, self.comul, self.S, self.unit, self.name = n, mul, comul, S, unit, name


def lin_mul(H, u, v):
    r = defaultdict(int)
    for i, a in u.items():
        for j, b in v.items():
            for k, c in H.mul[i][j].items():
                r[k] = (r[k] + a * b * c) % P
    return {k: c for k, c in r.items() if c}


def lin_S(H, u):
    r = defaultdict(int)
    for i, a in u.items():
        for k, c in H.S[i].items():
            r[k] = (r[k] + a * c) % P
    return {k: c for k, c in r.items() if c}


def e(i):
    return {i: 1}


def pis(*vecs):
    """produit pi(v1)pi(v2)... comme polynome (dict mot->coef)"""
    r = {(): 1}
    for v in vecs:
        nr = defaultdict(int)
        for w, a in r.items():
            for i, b in v.items():
                nr[w + (i,)] = (nr[w + (i,)] + a * b) % P
        r = nr
    return {w: c for w, c in r.items() if c}


def padd(f, g, c=1):
    r = dict(f)
    for w, a in g.items():
        v = (r.get(w, 0) + c * a) % P
        if v:
            r[w] = v
        else:
            r.pop(w, None)
    return r


def relations(H):
    n = H.n
    rels = []
    rels.append(padd(pis(H.unit), {(): 1}, -1))
    for h in range(n):
        for k in range(n):
            # PR2
            f = {}
            for (a, b, c) in H.comul[k]:
                f = padd(f, pis(e(h), e(a), lin_S(H, e(b))), c)
                f = padd(f, pis(lin_mul(H, e(h), e(a)), lin_S(H, e(b))), -c)
            rels.append(f)
            # PR3
            f = {}
            for (a, b, c) in H.comul[h]:
                f = padd(f, pis(e(a), lin_S(H, e(b)), e(k)), c)
                f = padd(f, pis(e(a), lin_mul(H, lin_S(H, e(b)), e(k))), -c)
            rels.append(f)
            # PR4
            f = {}
            for (a, b, c) in H.comul[k]:
                f = padd(f, pis(e(h), lin_S(H, e(a)), e(b)), c)
                f = padd(f, pis(lin_mul(H, e(h), lin_S(H, e(a))), e(b)), -c)
            rels.append(f)
            # PR5
            f = {}
            for (a, b, c) in H.comul[h]:
                f = padd(f, pis(lin_S(H, e(a)), e(b), e(k)), c)
                f = padd(f, pis(lin_S(H, e(a)), lin_mul(H, e(b), e(k))), -c)
            rels.append(f)
    return [r for r in rels if r]


def group_from_gens(gens):
    idt = tuple(range(len(gens[0])))
    elts = [idt]
    seen = {idt}
    i = 0
    while i < len(elts):
        g = elts[i]
        for s in gens:
            h = tuple(g[s[k]] for k in range(len(s)))  # g o s
            if h not in seen:
                seen.add(h)
                elts.append(h)
        i += 1
    return elts


def comp(g, h):
    return tuple(g[h[k]] for k in range(len(h)))


def inv(g):
    r = [0] * len(g)
    for i, x in enumerate(g):
        r[x] = i
    return tuple(r)


def group_tables(elts):
    idx = {g: i for i, g in enumerate(elts)}
    n = len(elts)
    m = [[idx[comp(elts[i], elts[j])] for j in range(n)] for i in range(n)]
    iv = [idx[inv(g)] for g in elts]
    return n, m, iv, idx[tuple(range(len(elts[0])))]


def kGdual(elts, name=""):
    n, m, iv, one = group_tables(elts)
    mul = [[({i: 1} if i == j else {}) for j in range(n)] for i in range(n)]
    comul = [[] for _ in range(n)]
    for y in range(n):
        for z in range(n):
            comul[m[y][z]].append((y, z, 1))
    S = [{iv[i]: 1} for i in range(n)]
    return Hopf(n, mul, comul, S, {i: 1 for i in range(n)}, name)


def permutations(elements, multiply, generators):
    index = {x:i for i,x in enumerate(elements)}
    return [tuple(index[multiply(g,x)] for x in elements) for g in generators]


def generalized_dihedral_9():
    elements=list(product(range(3),range(3),range(2)))
    def multiply(a,b):
        x,y,z=a; u,v,w=b
        return ((x+(-1)**z*u)%3,(y+(-1)**z*v)%3,z^w)
    return permutations(elements,multiply,[(1,0,0),(0,1,0),(0,0,1)])


GROUPS = {
    "A4": [(1, 2, 0, 3), (1, 0, 3, 2)],
    "S4": [(1, 0, 2, 3), (1, 2, 3, 0)],
    "G18_DihC3xC3": generalized_dihedral_9(),
}
