"""Generateur (Claude) du certificat Lean pour un module partiel simple de kA4*."""
import json, sys
from fractions import Fraction as F
from math import lcm
sys.path.insert(0, "/home/claude/hopf")
import hpar

src, dim_name, out = sys.argv[1], sys.argv[2], sys.argv[3]
d = json.load(open(src))
elts = [tuple(e) for e in d["elements"]]
n, m, iv, one = hpar.group_tables(elts)
assert one == 0
MQ = [[[F(x) for x in r] for r in A] for A in d["matrices"]]
k = len(MQ[0])
D = 1
for A in MQ:
    for r in A:
        for x in r:
            D = lcm(D, x.denominator)
AZ = [[[int(x * D) for x in r] for r in A] for A in MQ]


def mul(A, B):
    return [[sum(A[i][t] * B[t][j] for t in range(k)) for j in range(k)] for i in range(k)]


I = [[F(int(i == j)) for j in range(k)] for i in range(k)]
# mots engendrant M_k : BFS + independance lineaire exacte
words, mats = [], []
basis = []  # (pivot, vecteur) echelonne


def reduce(v):
    v = v[:]
    for p, b in basis:
        if v[p]:
            f = v[p]
            v = [x - f * y for x, y in zip(v, b)]
    return v


def try_add(w, Mq):
    v = reduce([x for r in Mq for x in r])
    nz = next((i for i, x in enumerate(v) if x), None)
    if nz is None:
        return False
    v = [x / v[nz] for x in v]
    for idx, (p, b) in enumerate(basis):
        if b[nz]:
            basis[idx] = (p, [x - b[nz] * y for x, y in zip(b, v)])
    basis.append((nz, v))
    words.append(w)
    mats.append(Mq)
    return True


try_add((), I)
frontier = [((), I)]
while len(words) < k * k and frontier:
    nf = []
    for w, Mq in frontier:
        for x in range(n):
            M2 = mul(Mq, MQ[x])
            if try_add(w + (x,), M2):
                nf.append((w + (x,), M2))
    frontier = nf
assert len(words) == k * k, "pas absolument simple ?"

# resoudre E_ij = sum_k c_k W_k (exact)
import itertools
N2 = k * k
cols = [[x for r in Mq for x in r] for Mq in mats]  # vecteurs W_k


def solve(target):
    # systeme N2 x N2 : sum_k c_k cols[k] = target
    A = [[cols[c][r] for c in range(N2)] + [target[r]] for r in range(N2)]
    for c in range(N2):
        piv = next(r for r in range(c, N2) if A[r][c] != 0)
        A[c], A[piv] = A[piv], A[c]
        f = A[c][c]
        A[c] = [x / f for x in A[c]]
        for r in range(N2):
            if r != c and A[r][c] != 0:
                g = A[r][c]
                A[r] = [x - g * y for x, y in zip(A[r], A[c])]
    return [A[r][N2] for r in range(N2)]


coef = {}
for i in range(k):
    for j in range(k):
        t = [F(int(r == i and c == j)) for r in range(k) for c in range(k)]
        sol = solve(t)
        # W_k^Q = Wtab_k / D^len  => coefficient sur Wtab_k : c / D^len
        coef[i, j] = [sol[t2] / F(D) ** len(words[t2]) for t2 in range(N2)]
Nden = 1
for v in coef.values():
    for x in v:
        Nden = lcm(Nden, x.denominator)
C = {key: [int(x * Nden) for x in v] for key, v in coef.items()}
Wtab = []
for w in words:
    Mz = [[int(i == j) for j in range(k)] for i in range(k)]
    for x in w:
        Mz = [[sum(Mz[i][t] * AZ[x][t][j] for t in range(k)) for j in range(k)] for i in range(k)]
    Wtab.append(Mz)


def mat(Mz):
    return "!![" + "; ".join(", ".join(str(x) for x in r) for r in Mz) + "]"


ns = f"A4Contre{dim_name}"
L = []
L.append("import Mathlib\n")
L.append(f"""/-!
# Contre-exemple à la conjecture B (Batista–Hautekiet–Saracco–Vercruysse) — module de dimension {k}

Certificat engendré par Claude (`gen_lean.py`) à partir de `{src.split('/')[-1]}`.

* Le groupe A₄ est donné par ses 12 permutations de `Fin 4` (`img`), sa table de
  multiplication `mulT` et ses inverses `invT`. On vérifie que la table est celle de
  la composition, que les 12 permutations sont distinctes et paires : c'est donc A₄.
* `A g` est la matrice entière {D} · π(p_g), où π(p_g) ∈ M_{k}(ℚ). La matrice rationnelle est
  `M g = A g / {D}`.
* `pr1` … `pr5` sont les relations PR1–PR5 des représentations partielles
  d'Alves–Batista–Vercruysse pour H = kG* (base p_g, Δ(p_g) = Σ_{{yz=g}} p_y ⊗ p_z,
  S(p_g) = p_{{g⁻¹}}). Elles sont écrites après multiplication par {D}³ :
    PR2 : π(p_a) Σ_y π(p_y) π(p_{{b⁻¹y}}) = π(p_a) π(p_{{b⁻¹a}})
    PR3 : Σ_y π(p_y) π(p_{{a⁻¹y}}) π(p_b) = π(p_{{ab}}) π(p_b)
    PR4 : π(p_a) Σ_y π(p_{{y⁻¹}}) π(p_{{y⁻¹b}}) = π(p_a) π(p_{{ab}})
    PR5 : Σ_y π(p_{{y⁻¹}}) π(p_{{y⁻¹a}}) π(p_b) = π(p_{{ba⁻¹}}) π(p_b)
  (Ces 577 relations coïncident exactement avec celles engendrées par le code de
  référence `hpar.relations`, vérification Python.)
* `pr*_Q` : les mêmes relations pour les matrices rationnelles `M g`.
* `unites` : chaque matrice élémentaire E_ij est combinaison linéaire de produits des
  `A g` (mots `mots`), donc l'algèbre engendrée par les π(p_g) est M_{k}(ℚ) tout entière :
  le module est absolument simple.
* Hors Lean (argument sur papier) : la construction 2.6 ne produit pour A₄ que des
  dimensions Σ χ(1)² ∈ {{1,2,3,4,9,10,11,12}}, la dimension 4 seulement via V₄ et e = 1,
  qui est exclu.
-/
""")
L.append(f"namespace {ns}\n")
L.append("/-- images de 0,1,2,3 par les 12 éléments de A₄ -/")
L.append("def img : Fin 12 → Fin 4 → Fin 4 := ![" + ", ".join("![" + ", ".join(map(str, e)) + "]" for e in elts) + "]")
L.append("def mulT : Fin 12 → Fin 12 → Fin 12 := ![" + ", ".join("![" + ", ".join(map(str, row)) + "]" for row in m) + "]")
L.append("def invT : Fin 12 → Fin 12 := ![" + ", ".join(map(str, iv)) + "]\n")
L.append("theorem mulT_spec : ∀ i j : Fin 12, ∀ t : Fin 4, img (mulT i j) t = img i (img j t) := by decide")
L.append("theorem invT_spec : ∀ i : Fin 12, mulT (invT i) i = 0 ∧ mulT i (invT i) = 0 := by decide")
L.append("theorem img_zero : ∀ t : Fin 4, img 0 t = t := by decide")
L.append("theorem img_inj : ∀ i j : Fin 12, (∀ t : Fin 4, img i t = img j t) → i = j := by decide")
L.append("/-- nombre d'inversions -/")
L.append("def inv4 (f : Fin 4 → Fin 4) : ℕ :=\n  ((List.finRange 4).flatMap fun s => (List.finRange 4).map fun t => (s, t)).countP\n    fun p => decide (p.1 < p.2 ∧ f p.2 < f p.1)")
L.append("theorem img_paire : ∀ i : Fin 12, inv4 (img i) % 2 = 0 := by decide\n")
L.append(f"/-- {D} · π(p_g) -/")
L.append(f"def A : Fin 12 → Matrix (Fin {k}) (Fin {k}) ℤ := ![\n  " + ",\n  ".join(mat(x) for x in AZ) + "]\n")
D3 = D
L.append("set_option maxRecDepth 200000\n")
L.append(f"theorem pr1 : ∑ x : Fin 12, A x = ({D} : ℤ) • (1 : Matrix (Fin {k}) (Fin {k}) ℤ) := by decide +kernel\n")
L.append(f"theorem pr2 : ∀ a b : Fin 12, A a * (∑ y : Fin 12, A y * A (mulT (invT b) y)) = ({D} : ℤ) • (A a * A (mulT (invT b) a)) := by decide +kernel\n")
L.append(f"theorem pr3 : ∀ a b : Fin 12, (∑ y : Fin 12, A y * A (mulT (invT a) y)) * A b = ({D} : ℤ) • (A (mulT a b) * A b) := by decide +kernel\n")
L.append(f"theorem pr4 : ∀ a b : Fin 12, A a * (∑ y : Fin 12, A (invT y) * A (mulT (invT y) b)) = ({D} : ℤ) • (A a * A (mulT a b)) := by decide +kernel\n")
L.append(f"theorem pr5 : ∀ a b : Fin 12, (∑ y : Fin 12, A (invT y) * A (mulT (invT y) a)) * A b = ({D} : ℤ) • (A (mulT b (invT a)) * A b) := by decide +kernel\n")
# simplicite
L.append(f"/-- produit des A le long d'un mot -/\ndef prodA (l : List (Fin 12)) : Matrix (Fin {k}) (Fin {k}) ℤ := l.foldr (fun x acc => A x * acc) 1\n")
L.append(f"def mots : Fin {N2} → List (Fin 12) := ![" + ", ".join("[" + ", ".join(map(str, w)) + "]" for w in words) + "]\n")
L.append(f"def W : Fin {N2} → Matrix (Fin {k}) (Fin {k}) ℤ := ![\n  " + ",\n  ".join(mat(x) for x in Wtab) + "]\n")
L.append(f"theorem W_spec : ∀ t : Fin {N2}, prodA (mots t) = W t := by decide +kernel\n")
L.append(f"def E (i j : Fin {k}) : Matrix (Fin {k}) (Fin {k}) ℤ := Matrix.of fun r c => if r = i ∧ c = j then 1 else 0\n")
L.append(f"def coef : Fin {k} → Fin {k} → Fin {N2} → ℤ := ![" + ", ".join(
    "![" + ", ".join("![" + ", ".join(map(str, C[i, j])) + "]" for j in range(k)) + "]" for i in range(k)) + "]\n")
L.append(f"/-- {Nden} · E_ij est combinaison entière des produits W t : l'algèbre engendrée est M_{k}(ℚ) -/")
L.append(f"theorem unites : ∀ i j : Fin {k}, ({Nden} : ℤ) • E i j = ∑ t : Fin {N2}, coef i j t • W t := by decide +kernel\n")
L.append(f"end {ns}")
open(out, "w").write("\n".join(L))
print("k =", k, "D =", D, "mots :", len(words), "longueur max", max(map(len, words)), "N =", Nden,
      "max |coef| =", max(abs(x) for v in C.values() for x in v))
