# Résultats — PoC spectre d'intrication → Gudhi

> Préenregistré dans [`PREREGISTRATION.md`](PREREGISTRATION.md) avant toute
> exécution. **Tier X** (numérique/exploratoire) au sens d'Elenchus — voir
> [`../../docs/rigor_protocol.md`](../../docs/rigor_protocol.md) §1 et
> l'entrée de grand livre
> [`../../docs/elenchus/ledger.json`](../../docs/elenchus/ledger.json)
> (`POC-X-0001`, `POC-X-0002`).

**Verdict global : les deux contrôles préenregistrés de la Partie A sont
`CONFIRMÉS` (avec une réfutation localisée d'une sous-prédiction). La
Partie B est `CONFIRMÉE` de façon empiriquement frappante, sans dérivation du
mécanisme.**

---

## Partie A — Chaîne SSH sur anneau

### Ce qui était prédit et ce qui a été trouvé

| | Prédiction | Résultat |
|---|---|---|
| Contrôle positif ($\lvert w\rvert>\lvert v\rvert$) | exactement 2 niveaux à $\zeta=1/2$ | **Confirmé**, exact à la précision flottante ($\lvert\zeta-1/2\rvert=0{,}0000$), à $L=100$ et $L=300$ |
| Contrôle négatif ($\lvert v\rvert>\lvert w\rvert$) | 0 niveau | **Confirmé**, à toutes les valeurs de $r$ testées |
| Rétrécissement du flou près de $r=1$ avec $L$ | flou de largeur $\sim\xi$, plus étroit à $L=300$ | **Réfuté** — voir ci-dessous |

Voir [`figures/ssh_ring_baseline_and_barcodes.png`](figures/ssh_ring_baseline_and_barcodes.png).

### La sous-prédiction réfutée, et pourquoi c'est instructif

En sondant jusqu'à $\lvert r-1\rvert = 10^{-6}$ (bien au-delà de la grille
préenregistrée), le comptage « près de $1/2$ » **saute exactement à $r=1$**,
sans aucun flou mesurable, identiquement à $L=100$ et $L=300$. La prédiction
préenregistrée supposait, à tort, que cette quantité se comporte comme un
paramètre d'ordre générique (crossover lisse de largeur $\sim 1/\xi$). Ce
n'est pas le cas : le comptage est un **invariant topologique quantifié** de
l'intrication (protégé par la même symétrie chirale qui épingle exactement
le mode nul de `ssh_exact.py`), donc il ne peut prendre que des valeurs
entières et change par un **croisement de niveau exact**, pas par une
interpolation continue. C'est précisément le contenu physique du mot
« topologique » — l'erreur de prédiction est localisée à une hypothèse
identifiable (traiter une quantité quantifiée comme un paramètre d'ordre
continu), au sens où Elenchus demande qu'une réfutation soit rapportée.

### Sur la persistance elle-même

Le code-barres $H_0$ (panneaux du bas de la figure) confirme visuellement le
même fait que les deux courbes de référence : une longue barre isolée dans la
phase topologique, aucune dans la phase triviale. **Ceci n'ajoute aucune
information au-delà des courbes de référence** — pour un nuage de points 1D,
$H_0$ est exactement la liste des écarts triés, ainsi que le prévenait
[`../axis1_topological_waves`](../axis1_topological_waves) au §1.4 du
programme expérimental. Gudhi est ici un moyen honnête de visualiser un fait
déjà simple, pas une découverte indépendante.

---

## Partie B — SYK : dégénérescence vs $N \bmod 8$

### Résultat

| $N$ | $N \bmod 8$ | Réalisations dégénérées |
|---|---|---|
| 8  | 0 | **0 / 40** |
| 12 | 4 | **40 / 40** |
| 16 | 0 | **0 / 40** |
| 20 | 4 | **40 / 40** |
| 24 | 0 | **0 / 40** |

**Séparation nette, tout-ou-rien, aux cinq valeurs de $N$ testées** — pas
seulement « plus fréquent », mais 100 % contre 0 % à chaque fois. L'écart
`same_sector_gap / energy_scale` (panneau du milieu de
[`figures/syk_degeneracy.png`](figures/syk_degeneracy.png)) sépare les deux
classes de **~14 ordres de grandeur** : $\sim 10^{-15}$ (précision flottante,
dégénérescence exacte) pour $N \bmod 8=4$, contre $\sim 10^{-4}$–$10^0$ (écart
physique réel) pour $N \bmod 8=0$.

### Le code-barres non supervisé

Le panneau de droite applique $H_0$ à **l'ensemble poolé** des 200
réalisations (les 5 valeurs de $N$ ensemble), **sans jamais donner l'étiquette
de classe à Gudhi**. Une seule barre domine, de longueur **10,7 décades**,
largement au-dessus de toutes les autres (qui mesurent l'espacement interne à
chaque paquet). C'est l'usage de la persistance qui a un sens ici : détecter,
depuis le seul nuage de points, qu'il existe **deux populations séparées**
plutôt qu'une seule — ce que ni le code ni l'analyste n'avaient présupposé
dans la construction du nuage.

### Ce que ce résultat établit, et ce qu'il n'établit pas

**Établit (empiriquement, Tier X) :** la fraction de réalisations SYK à
dégénérescence exacte du fondamental dépend de $N \bmod 8$, avec une
séparation totale entre $N\bmod 8=0$ (jamais dégénéré, sur $3\times40=120$
tirages, $N\in\{8,16,24\}$) et $N\bmod 8=4$ (toujours dégénéré, sur
$2\times40=80$ tirages, $N\in\{12,20\}$), à $N\le 24$.

**N'établit pas :**
- **Le mécanisme.** Aucun opérateur de symétrie antiunitaire n'a été
  construit ou identifié ici ; le lien avec la classification $\mathbb{Z}_8$
  de Fidkowski–Kitaev (`0904.2197`) et la classe de Wigner–Dyson cyclique de
  You–Ludwig–Xu (`1602.06964`) est une **motivation**, pas une dérivation.
  C'est un résultat Tier X (numérique/exploratoire), pas Tier B ni Tier L.
- **La généralité au-delà de $N\le 24$.** Cinq valeurs de $N$, deux classes
  mod 8 sur les quatre possibles pour $N\equiv 0\pmod 4$. Les classes
  $N\bmod 8 \in \{2,6\}$ (qui demanderaient $N\equiv 2\pmod 4$, donc une
  bipartition différente) n'ont pas été testées.
- **Un invariant topologique au sens de l'Axe 1.** Contrairement à la
  Partie A, où le comptage de niveaux à $1/2$ est directement lié à
  l'invariant d'enroulement $\nu$ déjà **prouvé** (`ssh_exact.py`, Tier B),
  aucun invariant analogue n'a été prouvé ici. Le mot « invariant
  topologique » de la demande initiale s'applique à la Partie A de façon
  établie, et à la Partie B seulement par analogie motivée par la
  littérature.

---

## Ce que ce PoC ajoute au dépôt

- Un deuxième système (SSH sur anneau) où la correspondance
  volume–frontière prend la forme d'une dégénérescence du spectre
  d'intrication, complétant la chaîne ouverte déjà traitée dans l'Axe 1 et le
  T2 Lean — les deux constructions partagent maintenant le même hamiltonien
  et la même convention de signe.
- Un signal empirique net, reproductible (graine fixée), sur la
  périodicité $N\bmod 8$ du SYK, qui **change le statut de ce dépôt** sur le
  sujet : le SYK n'est plus catalogué « sans structure topologique » nulle
  part dans ce dépôt.
- Un exemple concret de la discipline de contrôle d'Elenchus payant : la
  prédiction de flou fini-taille a été réfutée plutôt que silencieusement
  abandonnée, et un bug de représentation (barres $H_0$ par classe au lieu du
  poolé) a été détecté en regardant le panneau de référence avant de publier
  la figure.

## Prochaine étape suggérée

Si ce résultat SYK doit devenir plus qu'une observation Tier X : identifier
l'opérateur antiunitaire $T$ prédit par la classification et vérifier
$T^2=\pm 1$ directement (calcul Tier B, en arithmétique exacte sur les
représentations de Majorana), ce qui élèverait la Partie B au niveau où se
trouve déjà la Partie A.

---

## ERRATUM — Partie A (2026-09-27, après la publication de v0.1)

**Ce qui était faux.** La section « La sous-prédiction réfutée » ci-dessus
affirme que le comptage de niveaux à $\zeta=1/2$ ne présente **aucun** flou
de taille finie, et l'explique par la quantification de l'invariant. Cette
affirmation, et son explication, sont **fausses**. Elle est aussi reprise
dans `docs/RELEASE_NOTES_v0.1.md` et dans l'entrée `POC-X-0001` du grand
livre ; les deux reçoivent un erratum, le texte publié n'est pas réécrit.

**Ce qui s'est passé.** Toutes les mesures de la Partie A utilisaient un
sous-système de $\ell = L/2$ cellules. C'est une géométrie **spéciale** :
l'anneau possède alors une réflexion passant par les deux points de coupure
qui échange sous-système et complément ; combinée à la symétrie chirale,
elle annule **exactement** l'hybridation des deux modes de bord. Tester
« deux tailles » avec la même géométrie symétrique ne testait donc rien.

**Le test discriminant** ([`finite_size_scaling.py`](finite_size_scaling.py),
32 contrôles, tous passés) : pour $\ell \neq L/2$, les deux niveaux les plus
proches de $1/2$ s'en écartent de $\delta \sim (v/w)^{\min(\ell,\,L-\ell)}$ —
exactement le flou de taille finie que le préenregistrement prédisait. Taux
de décroissance ajusté contre la théorie $\xi = 1/\ln(w/v)$ :

| $r$ | $\xi$ ajusté | $\xi$ théorique |
|---|---|---|
| 0,5 | 1,39 | 1,44 |
| 0,7 | 2,68 | 2,80 |
| 0,8 | 4,23 | 4,48 |
| 0,9 | 8,42 | 9,49 |

Les rapports successifs $\delta(\ell+1)/\delta(\ell)$ sont monotones, sans
changement de signe, d'écart-type $\sim 0{,}01$ (platitude compensée, au sens
d'Elenchus). L'appariement chiral $\zeta_1+\zeta_2=1$ tient à $10^{-15}$ pour
tous les $(r,\ell)$ : la **paire** était réelle, seule sa distance à $1/2$
était mal rapportée. À $\ell=L/2$, $\delta < 10^{-15}$ : l'artefact est
reproduit et compris.

**Verdict corrigé.** Contrôles positif et négatif : toujours `CONFIRMÉS`
(2 niveaux vs 0, à toute distance raisonnable de $r=1$). Sous-prédiction
de flou fini-taille : `CONFIRMÉE`, et non « réfutée ». L'explication par
« l'invariant quantifié ne peut pas se lisser » est retirée : l'invariant du
système infini est quantifié, mais son image dans le spectre d'intrication
d'un système **fini** se lisse exponentiellement en $\ell/\xi$, comme le
prévoit la relation exacte de Fidkowski (`0909.2654`) entre spectre
d'intrication et modes de bord d'un système fini.

**Comment l'erreur a été attrapée.** Par un relecteur extérieur à la session
(producteur ≠ vérificateur), sur la question « et si $\ell \ne L/2$ ? ». Le
résultat était celui qu'on souhaitait — c'est exactement le cas où Elenchus
demande le plus de suspicion, et où elle a manqué.

**Ce que l'erreur apporte.** La longueur $\xi$ et le nombre de cellules
nécessaires pour contenir 99 % du mode de mur de domaine
(3 / 6 / 10 / 21 cellules par côté pour $r=0{,}5/0{,}7/0{,}8/0{,}9$, calcul
`D1` du même script, mode à énergie exactement nulle, piqué au mur) sont
**les nombres de conception de l'Axe 1a** — voir
[`../../docs/roadmap.md`](../../docs/roadmap.md).
