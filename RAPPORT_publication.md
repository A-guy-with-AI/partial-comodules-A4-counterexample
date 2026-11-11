# Rapport de publication

- L’article en anglais est livré en source LaTeX et en PDF de 12 pages. Le PDF a été compilé avec Tectonic 0.17.0 et les 12 pages ont été rendues pour contrôle. La signature de l’article et le champ auteur du PDF portent uniquement le pseudonyme demandé.
- Les deux fichiers Lean, les dix JSON, le vérificateur et le générateur correspondent octet pour octet aux sources. Le fichier `code/hpar.py` est un extrait minimal, avec l’enregistrement du groupe d’ordre 18. L’import du vérificateur est celui de l’original.
- Les dix modules ont passé le vérificateur Python sur les fichiers du dossier. Les deux certificats Lean ont été recompilés avec Lean 4 / Mathlib. Le contrôle des axiomes donne uniquement `propext`, `Classical.choice` et `Quot.sound`. Le générateur reproduit les corps des preuves à partir des JSON. Les certificats distribués comportent leurs propres commentaires et commandes d’affichage des axiomes.
- Les matrices d’ordre 18 sont livrées sur les deux corps finis où elles ont été vérifiées. Le fichier `checks/block_census.tsv` rassemble les listes complètes de blocs. Le moteur Gröbner et les traces historiques de dimension restent dans le dossier de recherche.
- Le manuscrit distingue les certificats Lean, l’exclusion sur papier de la construction 2.6 et le statut des théorèmes généraux. Les deux relectures ont été faites par IA. Une relecture par un expert humain reste à faire.

## Contrôle d’anonymat

Le grep n’a relevé aucune occurrence des chaînes interdites dans les noms de fichiers, les sources, les données, le texte extrait du PDF et ses métadonnées. Le contrôle des adresses électroniques n’a donné aucune occurrence. Les noms de chercheurs apparaissent dans les citations ou comme éponymes mathématiques.

La vérification élargie des chemins absolus a repéré un ancien chemin d’import Linux dans le générateur. Il est conservé pour respecter la copie à l’identique, et la commande du README fournit le module local par `PYTHONPATH`. Les mentions du système d’IA dans les fichiers d’origine ont également été conservées. L’article ne comporte aucune coordonnée ni aucun chemin local absolu.

Le manifeste SHA-256 couvre tous les fichiers livrés, à l’exception du manifeste lui-même.

