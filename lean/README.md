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
| **1 SSH** | hamiltonien SSH, symétrie chirale $\Gamma H \Gamma^{-1} = -H$ | le spectre est symétrique par rapport à 0 | **nombre d'enroulement $\in\mathbb{Z}$, et $=$ nombre de modes de bord** | les dix classes (Bott) |
| **2 Horizon** | écoulement barotrope irrotationnel, métrique acoustique $g_{\mu\nu}$ | $g_{\mu\nu}$ lorentzienne hors horizon | **perturbations $\Rightarrow \partial_\mu(\sqrt{-g}g^{\mu\nu}\partial_\nu\phi)=0$** | spectre thermique |
| **3 Vortex** | phase, indice d'enroulement | invariance par homotopie | **quantification entière (Stokes), additivité** | classification OAM |
| **4 Billard** | Laplacien de Dirichlet, comptage $N(k)$ | valeurs propres explicites du rectangle | **$N(k)\sim Ak^2/4\pi$ pour le rectangle** | loi de Weyl générale |
| **5 Caustiques** | famille génératrice, ensemble critique | stabilité du pli | **forme normale de la fronce ; caustique $=4u_2^3+27u_1^2=0$** | classification ADE |

---

## Le théorème central : T2 de l'axe 1

C'est le sommet scientifique du programme, et la seule cible où théorie,
expérience et preuve formelle se referment sur le même énoncé.

**Énoncé.** Soit $H(k)$ le hamiltonien de Bloch SSH à deux bandes,
$$H(k) = \begin{pmatrix} 0 & v + w e^{-ik} \\ v + w e^{ik} & 0\end{pmatrix}$$
gappé ($v \neq w$). Le nombre d'enroulement
$$\nu = \frac{1}{2\pi i}\oint_{\text{BZ}} \frac{d}{dk}\log\big(v + we^{-ik}\big)\,dk$$
est un **entier**, vaut $0$ si $|v|>|w|$ et $1$ si $|w|>|v|$, et **égale le
nombre de modes de bord à énergie nulle** de la chaîne ouverte.

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
- **Il se décompose** : quantification de $\nu$ d'abord ; calcul de $\nu$ selon
  $|v|$ vs $|w|$ ensuite ; comptage des modes de bord en dernier. Chaque étape
  est un théorème utile isolément.

**Attention au piège de la porte 4 (verrou d'énoncé).** La version qui « compile
facilement » consiste à définir le nombre d'enroulement *par* le nombre de modes
de bord, puis à prouver qu'ils sont égaux. C'est une tautologie. Les deux membres
doivent être définis **indépendamment** : $\nu$ par une intégrale sur la zone de
Brillouin du système infini, le comptage par le spectre de la chaîne **finie
ouverte**. Toute la substance du théorème est dans le fait que ces deux objets,
construits sans se parler, coïncident.

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
