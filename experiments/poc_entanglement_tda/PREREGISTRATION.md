# PoC — spectre d'intrication d'une chaîne 1D, persistance topologique (Gudhi)

> Préenregistré **avant** toute exécution, conformément à
> [`../../docs/rigor_protocol.md`](../../docs/rigor_protocol.md) §2 et au
> §5 (« Pre-registration ») du protocole Elenchus réel
> (`docs/ELENCHUS.md` du dépôt cloné). Tout ce document est **Tier X**
> (numérique/exploratoire) au sens d'Elenchus : il peut orienter, il ne peut
> jamais à lui seul soutenir une affirmation physique.

**Note de correspondance avec la demande.** La demande utilisateur nommait
« l'Axe 2 », mais l'Axe 2 du programme expérimental
([`../../docs/experimental_program.md`](../../docs/experimental_program.md))
est l'horizon analogue (superradiance sur vortex de vidange), sans rapport
avec les spectres d'intrication. Le contenu réellement décrit — spectre
d'intrication d'une chaîne de spins 1D, SYK, Gudhi, codes-barres de
persistance — correspond au **Projet 3** de
[`../../docs/contribution_map.md`](../../docs/contribution_map.md)
(« TDA de transitions topologiques »), construit ici par-dessus l'Axe 1
(SSH) déjà présent dans ce dépôt. Ce PoC vit dans son propre répertoire,
`experiments/poc_entanglement_tda/`, et ne touche pas
`experiments/axis2_analogue_horizon/`.

**Correction de prémisse, faite avant de coder plutôt qu'après un échec.**
Le SYK **n'est pas** un modèle sans structure topologique, contrairement à
l'hypothèse implicite d'un « témoin négatif générique ». Fidkowski & Kitaev
(`0904.2197`, dans le corpus) montrent que l'invariant $\mathbb{Z}$ d'une
chaîne de Majorana libre s'effondre en $\mathbb{Z}_8$ sous interaction ; You,
Ludwig & Xu (`1602.06964`, dans le corpus) montrent que la statistique
spectrale du SYK, vu comme théorie de bord d'une phase SPT désordonnée en
1D, cycle à travers les trois ensembles de Wigner–Dyson avec une périodicité
liée à cet indice topologique. Le SYK est donc reclassé de « témoin négatif »
à **second système à signal**, testé pour une périodicité empirique en
$N \bmod 8$ plutôt que supposé plat.

---

## Partie A — Chaîne SSH sur anneau (système principal)

### Affirmation
Sur un anneau de $L$ cellules (SSH, hamiltonien $h(k)=v+we^{-ik}$, même
convention que [`../axis1_topological_waves/ssh_exact.py`](../axis1_topological_waves/ssh_exact.py)),
le spectre d'intrication d'un sous-système de $\ell=L/2$ cellules **entières**
contiguës — qui sectionne exactement deux liaisons **inter-cellules** ($w$),
quelle que soit $\ell$ — possède **exactement deux** valeurs propres
$\zeta_n = 1/2$ (les deux moitiés de niveaux de bord fantômes, une par
liaison sectionnée) quand $|w|>|v|$ (phase topologique), et **aucune** quand
$|v|>|w|$ (phase triviale). C'est l'énoncé de Fidkowski (`0909.2654`,
corpus) — dégénérescence du spectre d'intrication $\Leftrightarrow$ modes de
bord du hamiltonien à bandes aplaties — appliqué à ce système précis.

### Observable
Spectre $\{\zeta_n\} \subset [0,1]$ de la matrice de corrélation
$C_{ij}=\langle c_i^\dagger c_j\rangle$ restreinte au sous-système, pour
l'état fondamental (bande inférieure remplie, demi-remplissage).
Ligne de base (non-TDA) : nombre de $\zeta_n$ dans $(1/2-\delta, 1/2+\delta)$
avec $\delta=0{,}05$, et $\min_n |\zeta_n-1/2|$.

### Protocole
- $r = v/w \in \{0{,}2,\, 0{,}3,\, \dots,\, 5{,}0\}$ (grille fine autour de
  $r=1$, plus lâche loin de la transition).
- Deux tailles : $L=100$ et $L=300$ cellules, $\ell=L/2$.
- Construction de $C$ par la solution de bande (exacte, pas de Monte-Carlo).
- Persistance : nuage de points 1D $\{|\zeta_n - 1/2|\}$, complexe de
  Vietoris–Rips, homologie $H_0$ (Gudhi). **Honnêteté requise** : la
  persistance $H_0$ d'un ensemble de scalaires est exactement la liste des
  écarts entre valeurs triées consécutives — ce n'est pas un calcul
  sophistiqué, et le texte des résultats le dira explicitement plutôt que de
  laisser croire à un apport caché de Gudhi ici.

### Prédiction
- $|w|>|v|$ : exactement 2 valeurs avec $|\zeta_n-1/2| < 10^{-6}$ (à la
  précision flottante près, hors zone de transition).
- $|v|>|w|$ : aucune valeur avec $|\zeta_n-1/2| < \delta$.
- Longueur de corrélation $\xi = 1/\ln|w/v|$ : à $r=0{,}9$, $\xi\approx 9{,}5$
  cellules — le brouillage autour de $r\approx 1$ doit **rétrécir** entre
  $L=100$ et $L=300$, signature d'un effet de taille finie et non d'un
  artefact.
- Code-barres : une barre de vie longue (naissance $\approx 0$, mort
  $\approx$ écart au reste du spectre) dans la phase topologique ; aucune
  barre de ce type dans la phase triviale.

### Hypothèse nulle
Le nombre de $\zeta_n$ proches de $1/2$ ne distingue pas les deux phases, ou
ne rétrécit pas avec $L$.

### Critère de réfutation
Phase topologique avec $<2$ valeurs à $10^{-4}$ de $1/2$ ; ou phase triviale
avec $\geq 1$ valeur à $\delta$ de $1/2$ ; ou la largeur de brouillage à
$L=300$ n'est pas strictement plus petite qu'à $L=100$.

### Contrôles (au sens Elenchus)
- **Positif** : $|w|>|v|$ doit produire les 2 barres — si ce contrôle
  n'apparaît pas, l'ensemble est invalidé avant de regarder le témoin SYK.
- **Négatif** : $|v|>|w|$ doit ne produire aucune barre de ce type.

### Causes d'échec connues (→ `INVALIDE`)
- Coupure ne tombant pas sur une frontière de cellule (romprait la
  construction "deux liaisons $w$ sectionnées").
- $\delta$ mal choisi trop petit pour la précision flottante utilisée.
- Confusion avec la chaîne **ouverte** : sur un anneau, il n'y a pas de mode
  de bord physique réel, seulement le mode d'intrication — ne pas présenter
  les deux comme le même objet physique.

---

## Partie B — SYK de Majorana : degré de dégénérescence vs $N \bmod 8$

### Affirmation
Pour le modèle SYK à 4 corps sur $N$ fermions de Majorana (couplages
gaussiens aléatoires $J_{ijkl}$, variance $3!\,J^2/N^3$, normalisation de
Maldacena–Stanford `1604.07818`, déjà dans le corpus), la fréquence à
laquelle l'état fondamental (dans un secteur de parité fixé) est
**exactement dégénéré** (à la précision flottante) dépend de $N \bmod 8$,
avec une fréquence de dégénérescence sensiblement plus élevée pour
$N \equiv 4 \pmod 8$ que pour $N \equiv 0 \pmod 8$ — motivé par, mais
**non dérivé de**, `0904.2197` et `1602.06964`.

### Observable
Sur chaque réalisation de désordre : l'écart entre les deux plus basses
énergies du **même secteur de parité fermionique**. Une réalisation est
comptée « dégénérée » si cet écart est $< 10^{-8}$ fois l'échelle d'énergie
typique ($\sim J\sqrt{N}$).

### Protocole
- $N \in \{8, 12, 16, 20, 24\}$ (multiples de 4, pour une bipartition propre
  en modes complexes — voir « causes d'échec »). $N=8,16,24$ sont
  $\equiv 0 \pmod 8$ ; $N=12,20$ sont $\equiv 4 \pmod 8$.
- 40 réalisations de désordre par $N$ (borné par le temps de calcul CPU :
  $N=24$ donne une diagonalisation dense $4096\times4096$).
- Diagonalisation exacte dans l'espace de Fock complet (les modes de Majorana
  sont appariés en modes complexes **avant** la transformation de
  Jordan–Wigner, et la bipartition se fait sur des modes complexes entiers,
  jamais sur une paire de Majorana coupée en deux).
- **Refus explicite**, pas de calcul silencieux, quand l'état fondamental
  du secteur choisi est proche-dégénéré avec l'état suivant du **même**
  secteur : le spectre d'intrication d'un vecteur arbitraire dans un espace
  presque dégénéré est du bruit de base, pas un résultat.

### Prédiction
Fraction de réalisations dégénérées sensiblement plus élevée à
$N\in\{12,20\}$ qu'à $N\in\{8,16,24\}$.

### Hypothèse nulle
Aucune dépendance en $N \bmod 8$ : la fraction de réalisations dégénérées est
statistiquement compatible entre les deux classes.

### Critère de réfutation
Différence non significative (à 40 réalisations, un test binomial grossier
suffit) entre les deux classes ; **ce résultat serait rapporté comme un
résultat nul**, pas caché ni réinterprété après coup.

### Analyse Gudhi
Pour chaque $N$, nuage de points = les écarts entre les 6 plus basses
énergies (même secteur), sur les 40 réalisations empilées → persistance
$H_0$ → code-barres. Ligne de base : histogramme brut des écarts.
**Prédiction faible et honnête** : aucune affirmation forte n'est faite sur
la forme du code-barres au-delà de « la classe $N\equiv 4$ montre davantage
de barres de durée de vie quasi nulle (paires dégénérées) que la classe
$N\equiv 0$ » — c'est un résumé visuel du même fait numérique que le taux de
dégénérescence, pas une découverte indépendante.

### Causes d'échec connues (→ `INVALIDE` ou exclusion de la réalisation)
- Bipartition sur une paire de Majorana coupée en deux : casserait
  l'équivalence trace fermionique = trace en qubits. Toujours couper sur des
  modes complexes entiers.
- État fondamental proche-dégénéré diagonalisé comme un vecteur unique :
  **réalisation exclue**, comptée séparément, jamais présentée comme un
  spectre d'intrication propre.
- $N=24$ trop lent ou trop gourmand en mémoire sur ce CPU partagé : réduire
  le nombre de réalisations plutôt que d'abandonner silencieusement.

---

## Verdicts et affichage

Un seul verdict par partie (A, B), au sens de
[`../../docs/rigor_protocol.md`](../../docs/rigor_protocol.md) §3 :
`CONFIRMÉ`, `RÉFUTÉ`, `NON CONCLUANT`, `INVALIDE`. La partie A doit être
`CONFIRMÉ` (ses deux contrôles positif/négatif sont la condition d'entrée)
avant que la partie B soit interprétée comme autre chose qu'exploratoire.

Tout ceci est classé **Tier X (numérique)** dans
[`../../docs/elenchus/ledger.json`](../../docs/elenchus/ledger.json) — cette
analyse ne remplace ni les faits Tier B déjà établis dans
`ssh_exact.py`, ni la citation Tier L de Fidkowski ; elle en est une
illustration numérique, avec ses propres contrôles.
