# Twisted group algebras and simple partial comodules of finite group algebras

**Author:** A-guy-with-AI · **Paper:** [`paper.pdf`](paper.pdf) (12 pages) · **Status:** preprint, not peer reviewed

## Main results

1. **Counterexample.** Conjecture B of Batista–Hautekiet–Saracco–Vercruysse [1] (also Conjecture 4.1.18 in [3]) is false. It predicts that every finite-dimensional simple partial comodule of a Hopf algebra comes from their Construction 2.6. For the group algebra of the alternating group A₄ there are simple partial comodules of dimensions **4 and 8** that do not arise this way. Both are given by explicit rational matrices and are **certified in Lean 4 / Mathlib**.
2. **Classification (Theorem A).** Over an algebraically closed field, in any characteristic, the finite-dimensional simple partial comodules of a finite group algebra kG are classified by a coset, a 2-cocycle class and a central idempotent of a **twisted** group algebra. The untwisted case is exactly Construction 2.6. For A₄ the missing simples come from the binary tetrahedral cover (quaternions).
3. **Semisimplicity (Theorem B).** If char k does not divide |G|, the universal partial representation algebra (k^G)_par of the dual group algebra is finite-dimensional and semisimple, with an explicit dimension formula. This is the case H = k^G of Conjecture 2.8 of Alves–Batista–Vercruysse [2].

Further examples are given for S₄ and for the generalized dihedral group (C₃×C₃)⋊C₂ of order 18.

## What is verified, and how

| Result | Status |
|---|---|
| A₄ simple modules of dimensions 4 and 8 | **Lean 4 / Mathlib certificate** (`lean/`): group table, all 577 partial-representation identities, generation of the full matrix algebra (absolute simplicity). Standard axioms only. |
| These modules are not from Construction 2.6 | Short argument on paper (Section 7 of the paper): for A₄, that construction only yields dimensions Σχ(1)² ∈ {1, 2, 3, 4, 9, 10, 11, 12}, and 4 only in an excluded case. |
| Examples for S₄ and order 18 | Exact rational (S₄) or modular (order 18) matrix checks with `checks/verif_module.py`. |
| Theorems A and B | Proofs in the paper. They were developed and reviewed by AI systems (two independent reviews, no error found) and have **not been reviewed by a human expert**. |
| Dimensions of (k^G)_par | Direct Gröbner-basis certificates (upper and lower bound) for S₃, D₈, Q₈, D₁₀: 51, 180, 180, 253. Other values in `checks/block_census.tsv` are computed via Theorem B. |

The counterexample (result 1) does not depend on Theorems A and B.

**Comments, corrections and expert review are very welcome. Please open an [issue](../../issues).**

## Reproduce

**Matrix checks** (Python ≥ 3.9, no extra packages), from the repository root:

```sh
for f in checks/modules/*.json; do
  python3 -B checks/verif_module.py "$f" || exit 1
done
```

Each run reports `0 en echec` (zero failed relations) and `ABSOLUMENT SIMPLE` (absolutely simple), with a generated algebra of dimension d².

**Lean certificates.** Lean `v4.36.0-rc2`, Mathlib commit `9d581dfff2e41de989072ea63abf3daf69311520`:

```sh
bundle_dir="$PWD"
mathlib_dir=$(mktemp -d)
git clone https://github.com/leanprover-community/mathlib4.git "$mathlib_dir/mathlib4"
cd "$mathlib_dir/mathlib4" && git checkout 9d581dfff2e41de989072ea63abf3daf69311520
lake exe cache get
lake env lean "$bundle_dir/lean/A4_contre_exemple_dim4.lean"
lake env lean "$bundle_dir/lean/A4_contre_exemple_dim8.lean"
```

Both files should compile and report only `propext`, `Classical.choice` and `Quot.sound`. The finite computations use `decide +kernel`.

**Regenerate a Lean certificate** from its matrices:

```sh
python3 -B checks/gen_lean.py checks/modules/A4_simple4_Q.json Dim4 /tmp/A4_dim4.lean
```

**Integrity:** `shasum -a 256 -c SHA256SUMS.txt`

## Repository layout

- `paper.tex`, `paper.pdf`: the note.
- `lean/`: Lean 4 certificates for the two A₄ modules.
- `checks/verif_module.py`: independent exact checker (partial-representation identities and absolute simplicity).
- `checks/modules/`: explicit matrices (JSON).
- `checks/gen_lean.py`: generator of the Lean certificates.
- `checks/block_census.tsv`: block sizes for all groups tested.
- `code/hpar.py`: group tables and relations used by the checker.

Some file names and program messages are in French.

## References

1. E. Batista, W. Hautekiet, P. Saracco, J. Vercruysse, *Towards a classification of simple partial comodules of Hopf algebras*, J. Algebra 664 (2025) 312–347. [doi:10.1016/j.jalgebra.2024.10.005](https://doi.org/10.1016/j.jalgebra.2024.10.005) · [arXiv:2310.12728](https://arxiv.org/abs/2310.12728)
2. M. M. S. Alves, E. Batista, J. Vercruysse, *Dilations of partial representations of Hopf algebras*, J. London Math. Soc. (2) 100 (2019). [doi:10.1112/jlms.12213](https://doi.org/10.1112/jlms.12213) · [arXiv:1802.03037](https://arxiv.org/abs/1802.03037)
3. W. Hautekiet, *Partial modules and comodules of Hopf algebras*, PhD thesis, Université libre de Bruxelles, 2025. [DI-fusion](https://difusion.ulb.ac.be/vufind/Record/ULB-DIPOT:oai:dipot.ulb.ac.be:2013/390035/Details)
4. M. M. S. Alves, E. Batista, J. Vercruysse, *Partial representations of Hopf algebras*, J. Algebra 426 (2015) 137–187. [arXiv:1309.1659](https://arxiv.org/abs/1309.1659)

## How to cite

See [`CITATION.cff`](CITATION.cff), or use the "Cite this repository" button on GitHub.

## License

Code (`checks/`, `code/`, `lean/`): [MIT](LICENSE). Paper (`paper.tex`, `paper.pdf`) and data (`checks/modules/`, `checks/block_census.tsv`): [CC BY 4.0](LICENSE-paper.md).
