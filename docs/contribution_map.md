# Carte de contribution : votre expertise × le programme de Ryu

**Question.** Avec une expertise en Lean 4, IA neuro-symbolique, IA et
programmation assistée, solveurs Rust, noyau Rust, optimisation GPU, déploiement
HPC à grande échelle et Gudhi (INRIA), où contribuer de façon **crédible** au
programme AdS/CMT / matière topologique ?

**Sources.** Problèmes ouverts : [`ryu_review.md`](ryu_review.md) §5. Actifs
réutilisables, vérifiés sur cette machine : [`assets/README.md`](assets/README.md).
Protocole : [`rigor_protocol.md`](rigor_protocol.md).

**Tout ce document relève de l'[INTERPRÉTATION]** : ce sont des recommandations,
pas des résultats. Chaque « nouveauté » annoncée reste à confirmer par une
recherche bibliographique dédiée avant d'être revendiquée.

---

## 0. Le constat de départ

Le programme de Ryu est **théorique et numérique**. Son dossier de 202 articles
ne contient **aucune formalisation** et **aucune ingénierie logicielle
publiée** comme contribution en soi. Or ses travaux récents (2023–2026) sont
**nettement plus algorithmiques** : transformées rapides, échantillonnage
Monte-Carlo, diagonalisations massives de matrices aléatoires non hermitiennes.

Votre profil ne vous place pas en concurrence avec les théoriciens du domaine :
il vous place **exactement sur les deux manques** — la vérification formelle et
le passage à l'échelle. C'est la position la plus solide pour contribuer sans
formation doctorale dans la spécialité.

**La limite à regarder en face.** La crédibilité dans ce domaine vient de la
physique. Une contribution d'ingénierie est reconnue quand elle **reproduit
d'abord** un résultat publié, puis va au-delà. Les trois projets recommandés
commencent tous par une reproduction.

---

## 1. Compétence par compétence

### Lean 4 — **le levier le plus fort**

- **Projet.** Formaliser le théorème de Ryu–Hatsugai (`cond-mat/0112197`) sous
  sa forme SSH : enroulement du volume ↔ mode de bord de la chaîne ouverte
  impaire.
- **Pourquoi c'est réaliste.** L'énoncé est fixé et vérifié numériquement
  ([`lean/README.md`](../lean/README.md),
  [`ssh_check.py`](../experiments/axis1_topological_waves/ssh_check.py)) ; il
  reste à le passer au `statement_lock.py` de LeanMaster. Le **cas
  topologique** se ramène à un lemme existant de Mathlib : pour
  $h(z) = v + wz$, $h'/h = (z + v/w)^{-1}$, et
  `circleIntegral.integral_sub_inv_of_mem_ball` donne $2\pi i$ quand
  $|v/w| < 1$ — d'où $\nu = +1$ dans le sens trigonométrique, convention
  choisie pour cette raison. Le **cas trivial** (pôle extérieur) n'est pas
  couvert par ce lemme et demande le théorème de Cauchy. Le membre de bord est
  de l'algèbre linéaire finie.
- **Suite (T3).** La table périodique par le problème d'extension de Clifford
  (Kitaev `0901.2686`), avec la `CliffordAlgebra` de Mathlib. Projet long, de
  valeur de référence durable.
- **Actifs.** Pipeline à portes de LeanMaster, prouveur local Goedel-Prover,
  skills `lean-tiered-proving` et `lean-proof-gate`.
- **Risque.** Faible pour T2, élevé pour T3.

### GPU — **l'entrée la plus directe dans les travaux récents de Ryu**

- **Projet.** Implémentation GPU de l'algorithme de Xiao & Ryu
  (`2601.00761`) : entropies de Rényi de stabilisateur par **transformée de
  Walsh–Hadamard rapide** et échantillonnage de chaînes de Pauli.
- **Pourquoi.** Le cœur est une transformée en $O(N 2^N)$ sur un vecteur de
  $2^N$ amplitudes : un noyau limité par la bande passante mémoire, idéal pour
  le GPU. Reproduire leurs courbes, puis repousser $N$.
- **Chiffre qui borne le projet.** Le calcul tient le vecteur d'état **et** un
  second tableau de $2^N$ entrées (produit ou transformée) :
  $2 \times 16 \cdot 2^N$ octets en `complex128`. Sur la T4 de 15 Go :
  **$N = 28$** en `complex128` (8,6 Go), **$N = 29$** seulement en `complex64`
  ou avec une transformée en place — et dans les deux cas, prouveur arrêté.
  Au-delà, découpage multi-GPU de la transformée (elle se factorise par blocs).
- **Actifs.** Chaîne CUDA 11.8 / PyTorch 2.7.1 validée sur T4 et discipline de
  reproductibilité bit à bit de `runux-ai-runtime`.

### Solveur Rust — **dynamique hors équilibre**

- **Projet.** Intégrateur pour la dynamique de SYK lindbladien (`2112.13489`) et
  des trempes de fermions libres (la matrice de corrélation obéit à une EDO
  linéaire de taille $L \times L$, donc des systèmes de milliers de sites sont
  accessibles).
- **Actif.** `rusty-SUNDIALS` — **pas de checkout local**, à cloner.
- **Risque.** Moyen : pour SYK, la taille de l'espace d'états reste le goulot,
  et c'est une question de GPU plus que d'intégrateur.

### Noyau Rust — **le lien le plus indirect, à dire franchement**

`rust-linux-mini-kernel` n'a pas de rapport direct avec la physique de la
matière condensée, et le présenter comme tel serait une surenchère. Ce qui s'y
transfère, c'est la **méthode** : une spécification Lean 4 d'un composant, et
une implémentation Rust dont on vérifie la conformité. Appliquée ici, elle donne
un objectif précis et rare : **une transformée de Walsh–Hadamard en Rust
vérifiée contre sa spécification Lean**, noyau du projet GPU ci-dessus. Pas de
checkout local non plus.

### Neuro-symbolique — **boucle conjecture → vérification → preuve**

- **Projet.** Les règles de somme de Kruchkov & Ryu (`2312.17318`) relient une
  intégrale optique à des invariants topologiques et géométriques. Boucle :
  un modèle propose des variantes (autres classes de symétrie, autres bandes) ;
  vérification exacte en arithmétique rationnelle sur des modèles de liaisons
  fortes ; preuve Lean des cas qui survivent.
- **Actifs.** Couche symbolique d'ANSE (SymPy), motif « Tier B » exact de
  Mensura (`Fraction` + oracles d'erreur), CAG de Wolfram-Hypergraph.
- **Règle.** Une conjecture produite par un modèle a le statut **C** (au sens de
  LeanMaster) tant qu'elle n'a pas passé la vérification exacte, et **A**
  seulement une fois prouvée par le noyau.

### IA et programmation assistée — **reproduction systématique**

- **Projet.** Un harnais qui prend un article du corpus, en extrait la figure
  numérique principale, et la **reproduit** avec un code testé. Chaque
  reproduction réussie est un actif ; chaque échec documenté est un résultat.
- **Actifs.** Collection `adscmt_literature` et serveur MCP `adscmt-rag` de ce
  dépôt, harnais ANSE.

### HPC à grande échelle — **moyennes sur le désordre**

- **Projet.** Les statistiques spectrales de matrices aléatoires non
  hermitiennes (une demi-douzaine d'articles de Ryu en 2025–2026) et les
  diagrammes de phase de modèles désordonnés demandent des millions de
  réalisations indépendantes : **parallélisme parfait**.
- **Actifs.** Infrastructure de calcul distribué d'Agora-Home, Terraform et
  Cloud Build de Wolfram-Hypergraph et d'ANSE.

### Gudhi (INRIA) — **détection non supervisée de transitions topologiques**

- **Projet.** Homologie persistante sur des nuages de points d'états
  fondamentaux (ou de champs de courbure de Berry) à travers l'espace des
  paramètres, pour détecter une transition topologique **sans connaître
  l'invariant à l'avance**. Point de contrôle obligatoire : le même calcul sur
  une famille sans transition (voir [`rigor_protocol.md`](rigor_protocol.md) §5).
- **Actif.** `.venv-tda` de DualScaleSimulator : **Gudhi déjà installé**.
- **Risque.** Moyen : la TDA doit battre une ligne de base simple (le gap
  spectral) pour être intéressante.

---

## 2. Les trois projets recommandés, dans l'ordre

| # | Projet | Compétences | Première étape vérifiable | Durée indicative |
|---|---|---|---|---|
| **1** | **Ryu–Hatsugai / SSH en Lean 4** | Lean, IA, noyau (méthode) | énoncé passé à `statement_lock.py` ; puis le cas topologique via `circleIntegral.integral_sub_inv_of_mem_ball` compile, sans `sorry` | semaines |
| **2** | **Moteur d'entropie de stabilisateur GPU** (Xiao–Ryu) | GPU, Rust, noyau (méthode), HPC | reproduire une courbe de `2601.00761` à $N \le 20$ | semaines à mois |
| **3** | **TDA de transitions topologiques** | Gudhi, HPC, IA | le modèle SSH : la transition en $\lvert v\rvert = \lvert w\rvert$ est détectée, et le témoin sans transition ne l'est pas | semaines |

**Pourquoi cet ordre.** Le projet 1 a l'énoncé le plus sûr (vérifié
numériquement, et dont le cas topologique s'appuie sur un lemme Mathlib
existant), il réutilise le pipeline le plus mature de la
machine, et il **boucle avec l'expérience** de l'axe 1a : le même énoncé est
prouvé en Lean, vérifié numériquement, et mesuré dans l'aquarium. Le projet 2
est l'entrée la plus directe dans les travaux actuels de Ryu. Le projet 3 est
le plus risqué scientifiquement, et le plus original.

**Ce qu'il ne faut pas faire en premier :** la dualité EHM ↔ AdS/CFT
(`ryu_review.md` §5, point 5). C'est le problème le plus profond de la liste, et
le moins susceptible de céder à l'ingénierie.
