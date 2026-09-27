# Actifs réutilisables sur cette machine

**Méthode.** Inventaire en lecture seule par
[`tools/inventory_assets.py`](../../tools/inventory_assets.py), relancé le
2026-09-27 sur 11 dépôts (`~` et les checkouts git du disque de données), puis
**vérification à la main** de chaque actif retenu. Données brutes :
[`inventory.json`](inventory.json).

**Pourquoi la vérification à la main est indispensable.** Le premier passage
comptait des occurrences de mots-clés, et plusieurs étaient fausses :

- `ssh` correspondait au protocole SSH : **toutes** les « occurrences du modèle
  SSH » (dont 6 dans AutoevolveAI et 12 dans runux) ont disparu après
  correction du motif ;
- `bott` correspondait à « bottleneck » ;
- dans LeanMaster, « winding » désigne les **modes d'enroulement de la corde**
  en T-dualité, et « chern » les **classes de Chern du réseau de Mukai** de K3 —
  des homonymes, sans rapport avec le nombre d'enroulement ou le nombre de
  Chern d'une bande ;
- dans AutoevolveAI, les occurrences de « SYK », « Berry », « holography » sont
  dans des **compendiums de questions de benchmark** (`papers/200_compendium/`,
  `results/*.json`), pas dans du code de physique.

Un comptage de mots-clés est un filtre, pas un résultat. Les tableaux ci-dessous
ne retiennent que ce qui a été ouvert et lu.

---

## 1. Réutilisables — vérifiés

| Actif | Chemin | Ce que c'est | Vérifié comment | Usage ici |
|---|---|---|---|---|
| **Pipeline de preuve LeanMaster** | `~/SocrateAI-Scientific-Agora-LeanMaster` | 10 bibliothèques, ≥ 573 théorèmes audités ; portes `axiom_audit.py`, `statement_lock.py`, `sorry_grep.py`, `phrasing_lint.py` | `docs/VERIFIED_FOUNDATION.md` lu ; skill `leanmaster-onboard` | héberger la future bibliothèque de matière topologique |
| **Mathlib** (checkout LeanMaster) | `.lake/packages/mathlib` | `CliffordAlgebra` ; `circleIntegral` et `circleIntegral.integral_sub_inv_of_mem_ball` (∮(z−w)⁻¹ = 2πi pour w intérieur) | fichiers source lus | T2 SSH (enroulement), T3 table périodique (Clifford) |
| **Prouveur local** | Ollama, `Goedel-Prover-V2-8B` | prouveur Lean 8B, sur la T4 | `/api/ps` | preuve à bas coût (skill `lean-tiered-proving`) |
| **Harnais ANSE** | `~/AutoevolveAI` | agents vérification d'abord ; SymPy ; Chroma ; embeddings `qwen3-embedding:0.6b` | code lu (`anse/memory/*`) | RAG, boucle conjecture → vérification |
| **Environnement Gudhi** | `~/SocrateAI-Scientific-DualScaleSimulator/.venv-tda` (Python 3.10) | `gudhi`, `scipy`, `sympy` installés | `site-packages` listé | TDA immédiatement disponible, sans installation |
| **Chaîne CUDA T4 validée** | `~/runux-ai-runtime` | CUDA 11.8, PyTorch 2.7.1+cu118, noyaux INT64 déterministes (dérive nulle sur 5 passes, selon le rapport interne) ; espace de travail Rust | `GPU_T4_VALIDATION_REPORT.md` lu | calcul GPU reproductible bit à bit |
| **Motif « Tier B » exact** | `~/SocrateAI-Scientific-Mensura` | arithmétique `Fraction` exacte + oracles d'erreur numériques ; `rust/` + `lean/` | README lu | vérifier une conjecture numérique avant de la prouver |
| **Calcul distribué** | `~/SocrateAI-Scientific-Agora-Home` | infrastructure DarkMatterK3@Home (calcul bénévole navigateur + natif) | README lu | balayages de paramètres, moyennes sur le désordre |
| **Infra GCP + MCP** | `~/SocrateAI-Wolfram-Hypergraph`, `~/AutoevolveAI` | Terraform, Dockerfiles, `cloudbuild.yaml`, serveurs MCP | arborescence lue | déploiement à grande échelle |
| **Ce dépôt** | ici | corpus à contrôle d'identité (73 articles), collection Chroma `adscmt_literature`, serveur MCP `adscmt-rag`, `ssh_check.py` | exécuté | socle de la recherche |

## 2. Présents mais **non** réutilisables comme fondations

| Actif | Pourquoi |
|---|---|
| `DualScaleSimulator/proofs/TachyonCondensationKTheory.lean` | La « K-théorie » y est un triplet d'entiers `(rank, c₁, c₂)`, avec un champ `Float`, sans Mathlib. C'est une comptabilité entière, pas une formalisation de la K-théorie. Utile tout au plus comme esquisse de nommage. |
| `DualScaleSimulator/.../dbrane_inflow.py` | Modèle jouet `numpy` des états de bord de D-brane ; ne calcule pas d'écoulement d'anomalie. |
| Occurrences « physique » d'AutoevolveAI | Texte de benchmarks, pas du code de calcul (voir plus haut). |
| « winding » / « chern » de LeanMaster | Homonymes (modes de corde, classes de Chern de K3). |

**[INTERPRÉTATION]** Ce constat correspond à l'avertissement du propre
`LL.md` de LeanMaster sur les « ombres arithmétiques » : un nom de fichier
ambitieux ne garantit pas le contenu formalisé.

## 3. Absents de la machine

`rusty-SUNDIALS` et `rust-linux-mini-kernel` sont sur GitHub
(`xaviercallens/…`) mais **n'ont pas de checkout local**, ni dans `~` ni sur le
disque de données. Pour les réutiliser : les cloner d'abord.

## 4. Contrainte matérielle mesurée

Une seule **Tesla T4 (15 Go)**, partagée. Mesuré le 2026-09-27 : GPU à 99 %,
13 Go de VRAM occupés par `Goedel-Prover-V2-8B`. Toute charge GPU de ce
programme — embeddings, diagonalisation, transformée de Walsh–Hadamard —
**entre en concurrence avec le prouveur Lean**. Ordre de grandeur utile : un
vecteur d'état de $N$ qubits en `complex128` occupe $16 \cdot 2^N$ octets, soit
8,6 Go à $N = 29$ ; **$N = 29$ est le plafond sur cette carte, prouveur
arrêté**. Au-delà : calcul distribué (§1, lignes « calcul distribué » et
« infra GCP »).

---

Régénérer :

```bash
python3 tools/inventory_assets.py --max-files 2500
```
