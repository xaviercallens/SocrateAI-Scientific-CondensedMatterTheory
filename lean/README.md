# Objectifs Lean 4 — échelle T0 → T3

**Règle.** Un niveau n'est acquis que s'il **compile, sans `sorry`, sans axiome
ajouté**, et si l'énoncé n'a pas été affaibli pour passer. Les portes sont
fournies par le dépôt frère `SocrateAI-Scientific-Agora-LeanMaster` : build,
absence de `sorry`, audit d'axiomes, verrou d'énoncé, producteur ≠ vérificateur.

**Pourquoi une échelle.** Les cibles du plan initial — loi de Weyl,
classification ADE, équivalence Navier–Stokes/géodésiques — sont chacune un
projet de formalisation de plusieurs années. Les viser directement garantit
qu'aucune n'aboutira. Chaque niveau ci-dessous est un théorème autonome : si le
niveau suivant échoue, l'acquis reste.

---

## L'échelle

| Axe | T0 — définitions | T1 — théorème jouet | T2 — **cible réaliste** | T3 — ambition |
|---|---|---|---|---|
| **1 SSH** | hamiltonien SSH, symétrie chirale $\Gamma H \Gamma^{-1} = -H$ | le spectre est symétrique par rapport à 0 | **$\nu\in\{0,-1\}$ ; chaîne impaire : un unique mode nul, au bord gauche ssi $\lvert w\rvert>\lvert v\rvert$** | demi-droite : $\dim\ker=\lvert\nu\rvert$ (Toeplitz) ; dix classes (Bott) |
| **2 Horizon** | écoulement barotrope irrotationnel, métrique acoustique $g_{\mu\nu}$ | $g_{\mu\nu}$ lorentzienne hors horizon | **perturbations $\Rightarrow \partial_\mu(\sqrt{-g}g^{\mu\nu}\partial_\nu\phi)=0$** | spectre thermique |
| **3 Vortex** | phase, indice d'enroulement | invariance par homotopie | **quantification entière (Stokes), additivité** | classification OAM |
| **4 Billard** | Laplacien de Dirichlet, comptage $N(k)$ | valeurs propres explicites du rectangle | **$N(k)\sim Ak^2/4\pi$ pour le rectangle** | loi de Weyl générale |
| **5 Caustiques** | famille génératrice, ensemble critique | stabilité du pli | **forme normale de la fronce ; pour $\tfrac{x^4}{4}+\tfrac{u_2x^2}{2}+u_1x$, caustique $=\{4u_2^3+27u_1^2=0\}$** | classification ADE |

---

## Le théorème central : T2 de l'axe 1

C'est le sommet scientifique du programme, et la seule cible où théorie,
expérience et preuve formelle se referment sur le même énoncé.

**Énoncé**, vérifié numériquement par
[`../experiments/axis1_topological_waves/ssh_check.py`](../experiments/axis1_topological_waves/ssh_check.py)
avant d'être verrouillé. Soit $h(k) = v + w e^{-ik}$, avec $v, w$ réels non nuls
et $|v| \ne |w|$.

1. **Volume.** Le nombre d'enroulement
   $\nu = \frac{1}{2\pi i}\oint_{\text{BZ}} \frac{h'(k)}{h(k)}\,dk$ est un
   entier ; $\nu = 0$ si $|v|>|w|$, et $\nu = -1$ si $|w|>|v|$ (le contour est
   parcouru dans le sens horaire).
2. **Bord.** La chaîne ouverte **impaire** $A_0B_0A_1\dots B_{N-1}A_N$
   ($2N+1$ sites, couplage intra-cellule $v$, inter-cellule $w$) possède
   **exactement un** mode d'énergie nulle, porté par le sous-réseau A,
   $\psi_A(n) \propto (-v/w)^n$.
3. **Correspondance.** Ce mode est localisé au bord **gauche** si et seulement
   si $\nu \ne 0$.

**Deux versions tentantes, et fausses :**

- « Le nombre de modes de bord *exactement* nuls de la chaîne ouverte égale
  $|\nu|$ » est **faux** pour une chaîne paire ($2N$ sites) : son bloc de
  sous-réseau est bidiagonal avec $v$ sur la diagonale, donc
  $\det D = v^N \neq 0$, et il n'existe **aucun** mode exactement nul. Les
  modes de bord de la phase topologique ont une énergie $\sim (v/w)^N$ :
  exponentiellement petite, jamais nulle.
- « $\nu = +1$ dans la phase topologique » : faux avec cette convention de
  signe. Sous verrou d'énoncé, le signe n'est pas un détail.

L'égalité $\dim\ker = |\nu|$ est **vraie sur la demi-droite infinie** : c'est
le théorème d'indice de Toeplitz. C'est la bonne cible **T3**, pas T2.

**Pourquoi c'est le bon objectif :**

- **C'est la correspondance volume–frontière elle-même**, sous sa forme la plus
  pure : un invariant calculé dans le volume (une intégrale sur la zone de
  Brillouin, sans aucune référence au bord) **compte** exactement les modes de
  bord. C'est l'énoncé étudié au §4 de
  [`../docs/literature_review.md`](../docs/literature_review.md).
- **Il est mesurable** dans l'aquarium — c'est l'expérience 1a.
- **Il est à portée de Mathlib** : le membre topologique est une intégrale de
  contour d'une fonction méromorphe sur le cercle, et Mathlib possède l'analyse
  complexe nécessaire. Le membre spectral se traite par récurrence explicite
  sur la chaîne finie.
- **Il se décompose** : le point 2 est de l'algèbre linéaire finie (noyau d'une
  matrice bidiagonale rectangulaire) ; le point 1 est une intégrale de contour ;
  le point 3 relie les deux. Chaque étape est un théorème utile isolément.

**Attention au piège de la porte 4 (verrou d'énoncé).** La version qui « compile
facilement » consiste à définir le nombre d'enroulement *par* la position du
mode de bord, puis à prouver qu'ils s'accordent. C'est une tautologie. Les deux
membres doivent être définis **indépendamment** : $\nu$ par une intégrale sur
la zone de Brillouin du système infini, le mode par le noyau de la matrice de
la chaîne **finie ouverte**. Toute la substance du théorème est dans le fait que
ces deux objets, construits sans se parler, s'accordent.

---

## Ce que Lean certifie, et ce qu'il ne certifie pas

Lean certifie qu'un théorème découle de ses hypothèses. Il ferme l'écart entre
**modèle** et **conclusion**.

Il ne dit **rien** sur l'écart entre **réalité** et **modèle**. Si la chaîne de
piliers imprimés n'est pas décrite par le hamiltonien SSH — parce que le couplage
entre piliers n'est pas au plus proche voisin, ou que l'amortissement casse la
symétrie chirale — alors une preuve impeccable de T2 ne dit rien de l'aquarium.

**Ce second écart se ferme par la mesure, et par rien d'autre.** C'est pourquoi
l'expérience 1a et le théorème T2 sont nécessaires tous les deux, et pourquoi
les présenter ensemble comme une « preuve » unique serait exactement le genre
d'affirmation que
[`../docs/rigor_protocol.md`](../docs/rigor_protocol.md) existe pour attraper.

---

## Branchement sur LeanMaster

Ne pas repartir de zéro. Le dépôt
`SocrateAI-Scientific-Agora-LeanMaster` fournit déjà :

- l'outillage de portes de preuve (build, `sorry`, audit d'axiomes) ;
- des résultats vérifiés sur les réseaux, la K-théorie et les structures
  associées, directement pertinents pour la périodicité de Bott visée en T3 de
  l'axe 1 ;
- un index de recherche de théorèmes, pour savoir ce qui existe déjà avant
  d'énoncer quoi que ce soit.

Les skills `leanmaster-onboard`, `leanmaster-theorem-search` et
`lean-proof-gate` de cet environnement donnent les points d'entrée.
