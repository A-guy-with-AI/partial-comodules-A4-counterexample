# Twisted group algebras and simple partial comodules

**Author:** A-guy-with-AI

- The note studies finite-dimensional simple partial comodules of finite group algebras.
- Finite duality makes these partial modules for the dual Hopf algebra.
- Theorem A parametrizes the simples by cosets, cocycles and central idempotents modulo characters.
- Construction 2.6 of Batista, Hautekiet, Saracco and Vercruysse gives the untwisted part.
- The binary tetrahedral cover of $A_4$ gives two missing simples, of dimensions 4 and 8.
- Both $A_4$ examples have rational matrices and Lean 4 / Mathlib certificates.
- The note also gives examples for $S_4$ and the generalized dihedral group of order 18.
- Theorem B gives the dimension and matrix blocks over an algebraic closure in characteristic prime to the group order.
- The tables distinguish direct dimension certificates, structural calculations and tests of individual modules.
- The proofs have been reviewed by two AI systems and have had no human expert review.

## Results and evidence

| Result | Dimension or block sizes | Status |
|---|---|---|
| $A_4$ counterexamples | 4 and 8 | Rational PR1–PR5 and matrix-unit certificates in Lean. Exclusion from Construction 2.6 is proved in the note. |
| $S_4$ explicit examples | 4, 8, 4 and 20 | Rational Python matrix checks. A second $A_4$ coset gives another 4 and 8 by translation. |
| $(C_3\times C_3)\rtimes C_2$, inversion action | Two classes of dimension 9 | Paper construction. Python checks for both classes over each of `F_2521` and `F_7561`. |
| Theorem A | Classification | Proof in the note. |
| Theorem B | Dimension, matrix blocks and semisimplicity in the stated characteristic | Proof in the note. |
| Direct Gröbner dimensions for $S_3,D_8,Q_8,D_{10}$ | 51, 180, 180, 253 | Prior upper and lower dimension certificates in finite characteristic. The Gröbner engine and traces are outside this bundle. |
| Remaining dimension census | See the paper and `checks/block_census.tsv` | Reported via Theorem B. The included module checker verifies individual representations. |

The order-18 certificates are modular. Over an algebraic closure of `Q`, complex conjugation interchanges the two nontrivial cocycle classes of the examples, so neither individual simple descends to `Q`. The note's proof explains the two classes using a primitive cube root of unity.

In the TSV, each block list uses `size:multiplicity`. The order-16 labels `G16_n` mean SmallGroups identifiers `(16,n)`. The primes column records the census fields, which can differ from the fields used for the earlier direct Gröbner checks.

## Reproduce the matrix checks

From the directory containing this README, with Python 3.9 or later:

```sh
for f in checks/modules/*.json; do
  python3 -B checks/verif_module.py "$f" || exit 1
done
```

Each run should report zero failed relations and `ABSOLUMENT SIMPLE`, with the generated algebra of dimension $d^2$. The verifier, JSONs, generator and Lean sources are byte-for-byte copies. The verifier already imports the sibling `code/hpar.py` helper, which contains the required group and relation routines and the order-18 group registration. The verifier needed no import edit. To regenerate the dimension-four matrix proof body, use the local helper via `PYTHONPATH`:

```sh
PYTHONPATH="$PWD/code" python3 -B checks/gen_lean.py \
  checks/modules/A4_simple4_Q.json Dim4 /tmp/A4_regenerated_dim4.lean
```

The distributed Lean certificates include axiom-reporting commands. The legacy generator emits the proof body and also prepends an old absolute import path. The command assumes that path does not supply a competing `hpar` module.

## Reproduce the Lean checks

Use Lean `v4.36.0-rc2` and Mathlib commit `9d581dfff2e41de989072ea63abf3daf69311520` (tag `v4.36.0-rc2`). From this bundle's root, the following makes a fresh, separate checkout:

```sh
bundle_dir="$PWD"
mathlib_dir=$(mktemp -d)
git clone --depth 1 --branch v4.36.0-rc2 \
  https://github.com/leanprover-community/mathlib4.git "$mathlib_dir/mathlib4"
cd "$mathlib_dir/mathlib4" || exit 1
lake exe cache get
lake env lean "$bundle_dir/lean/A4_contre_exemple_dim4.lean"
lake env lean "$bundle_dir/lean/A4_contre_exemple_dim8.lean"
```

Both runs should succeed and print only the standard axiom dependencies `propext`, `Classical.choice` and `Quot.sound`. The main finite calculations use `decide +kernel`.

## Build and check the bundle

From this bundle's root:

```sh
tectonic paper.tex
shasum -a 256 -c SHA256SUMS.txt
```

The checksum manifest covers the shipped files except itself. Run the integrity check before rebuilding if the local TeX installation may generate different PDF metadata. Human expert review of the paper proofs is welcome.

