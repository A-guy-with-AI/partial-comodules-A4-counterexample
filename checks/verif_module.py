"""Verificateur independant (Claude) d'un module partiel explicite sur kG*.

Entree JSON :
  {"group": "A4", "field": "p" ou "Q", "prime": 1201 (si p),
   "elements": [liste des permutations (listes d'entiers) dans l'ordre des matrices],
   "matrices": [ M_0, ..., M_{n-1} ]  (M_i = pi(p_{g_i}), d x d ; entrees entiers
                 ou chaines "a/b")}

Verifie, en arithmetique exacte :
  1. les elements forment bien le groupe demande (meme groupe que hpar.GROUPS) ;
  2. PR1-PR5 (relations generees par le code de Claude, hpar.relations) ;
  3. absolue simplicite : l'algebre engendree par les M_i est de dimension d^2 (Burnside).
"""
import json, sys
from fractions import Fraction
import os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "code"))
import hpar


def main(path):
    D = json.load(open(path))
    field = D["field"]
    p = D.get("prime")
    if field == "p":
        assert all(p % q for q in range(2, int(p ** .5) + 1)), "p non premier"
        conv = lambda x: Fraction(x) % p if not isinstance(x, str) else (Fraction(x).numerator * pow(Fraction(x).denominator, p - 2, p)) % p
        red = lambda x: x % p
        inv = lambda x: pow(int(x), p - 2, p)
    else:
        conv = lambda x: Fraction(x)
        red = lambda x: x
        inv = lambda x: Fraction(1) / Fraction(x)  # corrige : 1/1 donnait le flottant 1.0
    elts = [tuple(e) for e in D["elements"]]
    ref = hpar.group_from_gens(hpar.GROUPS[D["group"]])
    assert sorted(elts) == sorted(ref), "pas le bon groupe"
    n = len(elts)
    M = [[[red(conv(x)) for x in row] for row in m] for m in D["matrices"]]
    d = len(M[0])
    assert len(M) == n and all(len(m) == d and all(len(r) == d for r in m) for m in M)

    # structure de kG* dans l'ordre fourni (coefficients entiers)
    hpar.P = 10 ** 18 + 9  # coefficients des relations : petits entiers, on reduit ensuite
    H = hpar.kGdual(elts)
    rels = hpar.relations(H)

    def mul(A, B):
        return [[red(sum(A[i][k] * B[k][j] for k in range(d) if A[i][k])) for j in range(d)] for i in range(d)]

    I = [[1 if i == j else 0 for j in range(d)] for i in range(d)]
    cache = {(): I}

    def word(w):
        if w not in cache:
            cache[w] = mul(word(w[:-1]), M[w[-1]])
        return cache[w]
    bad = 0
    for r in rels:
        acc = [[0] * d for _ in range(d)]
        for w, c in r.items():
            c = c if c < hpar.P // 2 else c - hpar.P  # coefficient entier signe
            W = word(w)
            for i in range(d):
                for j in range(d):
                    if W[i][j]:
                        acc[i][j] = red(acc[i][j] + c * W[i][j])
        if any(x != 0 for row in acc for x in row):
            bad += 1
    print(f"Relations PR1-PR5 : {len(rels)} testees, {bad} en echec")
    if D.get("orbit_only"):
        # dim de l'orbite du vecteur e_0 sous les mots en M_i : borne inf de dim H_par
        vb, vp = [], []
        def addv(v):
            v = v[:]
            for (pc, b) in zip(vp, vb):
                if v[pc]:
                    f = v[pc]; v = [red(x - f*y) for x, y in zip(v, b)]
            nz = next((i for i, x in enumerate(v) if x), None)
            if nz is None: return None
            f = inv(v[nz]); v = [red(x*f) for x in v]
            vb.append(v); vp.append(nz); return True
        def app(m, v):
            return [red(sum(m[i][k]*v[k] for k in range(d) if v[k])) for i in range(d)]
        start = [1 if i == 0 else 0 for i in range(d)]
        addv(start); fr = [start]
        while fr:
            nf = []
            for v in fr:
                for m in M:
                    w = app(m, v)
                    if addv(w): nf.append(w)
            fr = nf
        print(f"orbite de e_0 : dimension {len(vb)}  => dim H_par >= {len(vb)}" if bad == 0 else "relations en echec")
        return bad == 0

    # dimension de l'algebre engendree
    basis = []  # vecteurs aplatis echelonnes
    piv = []

    def add(v):
        v = v[:]
        for (pc, b) in zip(piv, basis):
            if v[pc]:
                f = v[pc]
                v = [red(x - f * y) for x, y in zip(v, b)]
        nz = next((i for i, x in enumerate(v) if x), None)
        if nz is None:
            return False
        f = inv(v[nz])
        v = [red(x * f) for x in v]
        for k, b in enumerate(basis):
            if b[nz]:
                g = b[nz]
                basis[k] = [red(x - g * y) for x, y in zip(b, v)]
        basis.append(v); piv.append(nz)
        return True
    frontier = [I]
    add([x for row in I for x in row])
    while frontier and len(basis) < d * d:
        nf = []
        for A in frontier:
            for m in M:
                B = mul(A, m)
                if add([x for row in B for x in row]):
                    nf.append(B)
        frontier = nf
    print(f"dim de l'algebre engendree = {len(basis)} (d^2 = {d*d})")
    ok = bad == 0 and len(basis) == d * d
    print(f"=> module partiel ABSOLUMENT SIMPLE de dimension {d}" if ok else "=> ECHEC")
    return ok


if __name__ == "__main__":
    main(sys.argv[1])
