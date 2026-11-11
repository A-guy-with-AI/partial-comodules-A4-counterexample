import Mathlib

/-!
# Contre-exemple à la conjecture B (Batista–Hautekiet–Saracco–Vercruysse) — module de dimension 4

Certificat engendré par Claude (`gen_lean.py`) à partir de `A4_simple4_Q.json`.

* Le groupe A₄ est donné par ses 12 permutations de `Fin 4` (`img`), sa table de
  multiplication `mulT` et ses inverses `invT`. On vérifie que la table est celle de
  la composition, que les 12 permutations sont distinctes et paires : c'est donc A₄.
* `A g` est la matrice entière 18 · π(p_g), où π(p_g) ∈ M_4(ℚ). La matrice rationnelle est
  `M g = A g / 18`.
* `pr1` … `pr5` sont les relations PR1–PR5 des représentations partielles
  d'Alves–Batista–Vercruysse pour H = kG* (base p_g, Δ(p_g) = Σ_{yz=g} p_y ⊗ p_z,
  S(p_g) = p_{g⁻¹}). Elles sont écrites après multiplication par 18³ :
    PR2 : π(p_a) Σ_y π(p_y) π(p_{b⁻¹y}) = π(p_a) π(p_{b⁻¹a})
    PR3 : Σ_y π(p_y) π(p_{a⁻¹y}) π(p_b) = π(p_{ab}) π(p_b)
    PR4 : π(p_a) Σ_y π(p_{y⁻¹}) π(p_{y⁻¹b}) = π(p_a) π(p_{ab})
    PR5 : Σ_y π(p_{y⁻¹}) π(p_{y⁻¹a}) π(p_b) = π(p_{ba⁻¹}) π(p_b)
  (Ces 577 relations coïncident exactement avec celles engendrées par le code de
  référence `hpar.relations`, vérification Python.)
* `unites` : chaque matrice élémentaire E_ij est combinaison linéaire de produits des
  `A g` (mots `mots`), donc l'algèbre engendrée par les π(p_g) est M_4(ℚ) tout entière :
  le module est absolument simple.
* Hors Lean (argument sur papier) : la construction 2.6 ne produit pour A₄ que des
  dimensions Σ χ(1)² ∈ {1,2,3,4,9,10,11,12}, la dimension 4 seulement via V₄ et e = 1,
  qui est exclu.
-/

namespace A4ContreDim4

/-- images de 0,1,2,3 par les 12 éléments de A₄ -/
def img : Fin 12 → Fin 4 → Fin 4 := ![![0, 1, 2, 3], ![1, 2, 0, 3], ![1, 0, 3, 2], ![2, 0, 1, 3], ![2, 1, 3, 0], ![0, 3, 1, 2], ![0, 2, 3, 1], ![1, 3, 2, 0], ![3, 1, 0, 2], ![3, 0, 2, 1], ![2, 3, 0, 1], ![3, 2, 1, 0]]
def mulT : Fin 12 → Fin 12 → Fin 12 := ![![0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], ![1, 3, 4, 0, 6, 7, 2, 10, 11, 8, 5, 9], ![2, 5, 0, 8, 9, 1, 7, 6, 3, 4, 11, 10], ![3, 0, 6, 1, 2, 10, 4, 5, 9, 11, 7, 8], ![4, 7, 1, 11, 8, 3, 10, 2, 0, 6, 9, 5], ![5, 8, 9, 2, 7, 6, 0, 11, 10, 3, 1, 4], ![6, 10, 3, 9, 11, 0, 5, 4, 1, 2, 8, 7], ![7, 11, 8, 4, 10, 2, 1, 9, 5, 0, 3, 6], ![8, 2, 7, 5, 0, 11, 9, 1, 4, 10, 6, 3], ![9, 6, 5, 10, 3, 8, 11, 0, 2, 7, 4, 1], ![10, 9, 11, 6, 5, 4, 3, 8, 7, 1, 0, 2], ![11, 4, 10, 7, 1, 9, 8, 3, 6, 5, 2, 0]]
def invT : Fin 12 → Fin 12 := ![0, 3, 2, 1, 8, 6, 5, 9, 4, 7, 10, 11]

theorem mulT_spec : ∀ i j : Fin 12, ∀ t : Fin 4, img (mulT i j) t = img i (img j t) := by decide
theorem invT_spec : ∀ i : Fin 12, mulT (invT i) i = 0 ∧ mulT i (invT i) = 0 := by decide
theorem img_zero : ∀ t : Fin 4, img 0 t = t := by decide
theorem img_inj : ∀ i j : Fin 12, (∀ t : Fin 4, img i t = img j t) → i = j := by decide
/-- nombre d'inversions -/
def inv4 (f : Fin 4 → Fin 4) : ℕ :=
  ((List.finRange 4).flatMap fun s => (List.finRange 4).map fun t => (s, t)).countP
    fun p => decide (p.1 < p.2 ∧ f p.2 < f p.1)
theorem img_paire : ∀ i : Fin 12, inv4 (img i) % 2 = 0 := by decide

/-- 18 · π(p_g) -/
def A : Fin 12 → Matrix (Fin 4) (Fin 4) ℤ := ![
  !![0, 0, 0, 0; 0, 0, 0, 0; 0, 0, 3, -3; 0, 0, -3, 3],
  !![0, -1, 0, -1; 0, 3, 0, 3; 0, 0, 0, 0; 0, 3, 0, 3],
  !![0, 0, 0, 0; 18, 6, 3, 3; 0, 0, 0, 0; 0, 0, 0, 0],
  !![0, -1, -1, 0; 0, 3, 3, 0; 0, 3, 3, 0; 0, 0, 0, 0],
  !![0, 0, 0, 0; 0, 3, 0, -3; 0, 0, 0, 0; 0, -3, 0, 3],
  !![0, 0, 0, 0; 0, 0, 0, 0; 18, 3, 6, 3; 0, 0, 0, 0],
  !![0, 0, 0, 0; 0, 0, 0, 0; 0, 0, 0, 0; 18, 3, 3, 6],
  !![6, 1, 1, 0; 0, 0, 0, 0; 0, 0, 0, 0; -18, -3, -3, 0],
  !![0, 0, 0, 0; 0, 3, -3, 0; 0, -3, 3, 0; 0, 0, 0, 0],
  !![6, 1, 0, 1; 0, 0, 0, 0; -18, -3, 0, -3; 0, 0, 0, 0],
  !![0, 0, -1, -1; 0, 0, 0, 0; 0, 0, 3, 3; 0, 0, 3, 3],
  !![6, 0, 1, 1; -18, 0, -3, -3; 0, 0, 0, 0; 0, 0, 0, 0]]

set_option maxRecDepth 200000

theorem pr1 : ∑ x : Fin 12, A x = (18 : ℤ) • (1 : Matrix (Fin 4) (Fin 4) ℤ) := by decide +kernel

theorem pr2 : ∀ a b : Fin 12, A a * (∑ y : Fin 12, A y * A (mulT (invT b) y)) = (18 : ℤ) • (A a * A (mulT (invT b) a)) := by decide +kernel

theorem pr3 : ∀ a b : Fin 12, (∑ y : Fin 12, A y * A (mulT (invT a) y)) * A b = (18 : ℤ) • (A (mulT a b) * A b) := by decide +kernel

theorem pr4 : ∀ a b : Fin 12, A a * (∑ y : Fin 12, A (invT y) * A (mulT (invT y) b)) = (18 : ℤ) • (A a * A (mulT a b)) := by decide +kernel

theorem pr5 : ∀ a b : Fin 12, (∑ y : Fin 12, A (invT y) * A (mulT (invT y) a)) * A b = (18 : ℤ) • (A (mulT b (invT a)) * A b) := by decide +kernel

/-- produit des A le long d'un mot -/
def prodA (l : List (Fin 12)) : Matrix (Fin 4) (Fin 4) ℤ := l.foldr (fun x acc => A x * acc) 1

def mots : Fin 16 → List (Fin 12) := ![[], [0], [1], [2], [3], [4], [5], [6], [7], [10], [0, 1], [0, 4], [0, 5], [1, 2], [1, 6], [2, 4]]

def W : Fin 16 → Matrix (Fin 4) (Fin 4) ℤ := ![
  !![1, 0, 0, 0; 0, 1, 0, 0; 0, 0, 1, 0; 0, 0, 0, 1],
  !![0, 0, 0, 0; 0, 0, 0, 0; 0, 0, 3, -3; 0, 0, -3, 3],
  !![0, -1, 0, -1; 0, 3, 0, 3; 0, 0, 0, 0; 0, 3, 0, 3],
  !![0, 0, 0, 0; 18, 6, 3, 3; 0, 0, 0, 0; 0, 0, 0, 0],
  !![0, -1, -1, 0; 0, 3, 3, 0; 0, 3, 3, 0; 0, 0, 0, 0],
  !![0, 0, 0, 0; 0, 3, 0, -3; 0, 0, 0, 0; 0, -3, 0, 3],
  !![0, 0, 0, 0; 0, 0, 0, 0; 18, 3, 6, 3; 0, 0, 0, 0],
  !![0, 0, 0, 0; 0, 0, 0, 0; 0, 0, 0, 0; 18, 3, 3, 6],
  !![6, 1, 1, 0; 0, 0, 0, 0; 0, 0, 0, 0; -18, -3, -3, 0],
  !![0, 0, -1, -1; 0, 0, 0, 0; 0, 0, 3, 3; 0, 0, 3, 3],
  !![0, 0, 0, 0; 0, 0, 0, 0; 0, -9, 0, -9; 0, 9, 0, 9],
  !![0, 0, 0, 0; 0, 0, 0, 0; 0, 9, 0, -9; 0, -9, 0, 9],
  !![0, 0, 0, 0; 0, 0, 0, 0; 54, 9, 18, 9; -54, -9, -18, -9],
  !![-18, -6, -3, -3; 54, 18, 9, 9; 0, 0, 0, 0; 54, 18, 9, 9],
  !![-18, -3, -3, -6; 54, 9, 9, 18; 0, 0, 0, 0; 54, 9, 9, 18],
  !![0, 0, 0, 0; 0, 9, 0, -9; 0, 0, 0, 0; 0, 0, 0, 0]]

theorem W_spec : ∀ t : Fin 16, prodA (mots t) = W t := by decide +kernel

def E (i j : Fin 4) : Matrix (Fin 4) (Fin 4) ℤ := Matrix.of fun r c => if r = i ∧ c = j then 1 else 0

def coef : Fin 4 → Fin 4 → Fin 16 → ℤ := ![![![162, -36, -27, -27, 0, -18, -18, 0, 9, -18, 3, 3, 6, 3, 6, 3], ![-162, 27, 27, 54, 0, -27, 0, 27, -27, 27, 0, 0, 0, -18, 0, 18], ![-486, 135, 81, 54, 0, 81, 108, -27, 27, 27, -18, -18, -36, 0, -18, -18], ![-162, 27, 27, 54, 0, 27, 0, 27, -27, 27, 0, 0, 0, 0, -18, -18]], ![![18, -3, -6, -3, -3, -3, -3, 0, 3, 0, 0, 1, 1, 2, 0, 0], ![0, 0, 9, 9, 0, 0, 0, 0, -9, 0, 0, 0, 0, -3, 0, 3], ![-108, 18, 9, 9, 18, 18, 18, 0, 9, 0, 0, -6, -6, -3, 0, -3], ![0, 0, 9, 9, 0, 0, 0, 0, -9, 0, 0, 0, 0, -3, 0, -3]], ![![36, -12, -6, -6, 0, -3, -3, 0, 0, -6, 2, 1, 2, 0, 2, 1], ![-54, 9, 9, 9, 0, -9, 0, 9, 0, 9, -3, 3, 0, 0, -3, 3], ![-54, 27, 9, 9, 0, 9, 18, -9, 0, 9, -3, -3, -6, 0, -3, -3], ![-54, 9, 9, 9, 0, 9, 0, 9, 0, 9, -3, -3, 0, 0, -3, -3]], ![![36, -6, -6, -6, 0, -3, -3, 0, 0, -6, 0, 0, 1, 0, 2, 1], ![-54, 9, 9, 9, 0, -9, 0, 9, 0, 9, 0, 0, 0, 0, -3, 3], ![-54, 9, 9, 9, 0, 9, 18, -9, 0, 9, 0, 0, -6, 0, -3, -3], ![-54, 9, 9, 9, 0, 9, 0, 9, 0, 9, 0, 0, 0, 0, -3, -3]]]

/-- 54 · E_ij est combinaison entière des produits W t : l'algèbre engendrée est M_4(ℚ) -/
theorem unites : ∀ i j : Fin 4, (54 : ℤ) • E i j = ∑ t : Fin 16, coef i j t • W t := by decide +kernel

end A4ContreDim4

#print axioms A4ContreDim4.mulT_spec
#print axioms A4ContreDim4.img_inj
#print axioms A4ContreDim4.img_paire
#print axioms A4ContreDim4.pr1
#print axioms A4ContreDim4.pr2
#print axioms A4ContreDim4.pr3
#print axioms A4ContreDim4.pr4
#print axioms A4ContreDim4.pr5
#print axioms A4ContreDim4.W_spec
#print axioms A4ContreDim4.unites
