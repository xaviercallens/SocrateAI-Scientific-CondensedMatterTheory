# Hypothèse H1 — Profondeur logarithmique et conditionnement du problème inverse de bord sur un pavage hyperbolique

**Statut : Tier C (conjecture) au dépôt ; les pièces qui la soutiennent
sont marquées L, et ses tests sont marqués X (numérique) ou B (arithmétique
exacte) au fur et à mesure.** Voir [`../../docs/rigor_protocol.md`](../../docs/rigor_protocol.md).

> **Révision post-exploration (2026-09-27), avant tout verrouillage
> définitif.** La version initiale de cette hypothèse affirmait que la
> sensibilité $\|\partial\Lambda/\partial g_e\|$ d'une arête décroît
> **exponentiellement** en profondeur sur réseau euclidien plat, par
> analogie directe avec l'instabilité logarithmique du problème de Calderón
> continu. Une relecture externe a montré cette dérivation incohérente
> dimensionnellement (le noyau de Poisson $d/(d^2+s^2)$ intégré au carré sur
> le bord donne une décroissance **polynomiale**, $\sim d^{-1}$ à $d^{-3}$
> selon la normalisation, pas exponentielle). Plutôt que verrouiller une
> prédiction bâtie sur une dérivation fautive, une **passe exploratoire non
> verrouillée** a été exécutée d'abord (`hyperbolic_network.py`,
> `--max-layers 3`, Tier X, seed fixée), pour mesurer directement la forme
> fonctionnelle avant de formuler la prédiction définitive. Ce document
> reporte cette passe et la mécanique corrigée ; §3 contient la prédiction
> **verrouillée pour la suite** (un point de donnée $L=4$, non encore
> calculé au moment de l'écriture de la section, voir
> [`PREREGISTRATION.md`](PREREGISTRATION.md)).
>
> **Ce qui a été mesuré (exploratoire, Tier X, non prédictif) :**
>
> | | $N$ | profondeur max | $\log_{10}\kappa(J)$ |
> |---|---|---|---|
> | $\{7,3\}$ | 35, 112, 315 | 1, 3, 5 | 1,39 / 2,46 / 3,27 |
> | carré | 29, 113, 317 | 2, 5, 9 | 1,73 / 5,07 / 9,72 |
> | triangulaire | 37, 151, 421 | 2, 5, 10 | 3,42 / 8,67 / 12,10 |
>
> À $N$ apparié (~315–320) : **$\log_{10}\kappa$ hyperbolique = 3,27,
> euclidien (carré) = 9,72 — un écart de 6,4 décades**, déjà net à ces
> tailles modestes ([`figures/h0.png`](figures/h0.png)). Dans les deux
> géométries, $\log_{10}\kappa$ croît **localement linéairement avec la
> profondeur maximale** (pente ≈ 0,47/couche pour $\{7,3\}$, ≈ 1,14/couche
> pour le carré) — c'est-à-dire que $\kappa$ décroît **exponentiellement en
> profondeur dans les deux cas**, ce qui est la physique attendue et
> commune aux deux géométries. **Le mécanisme qui distingue les deux
> familles n'est donc pas la forme locale de la décroissance, mais la
> vitesse à laquelle la profondeur elle-même croît avec $N$** :
> logarithmique pour $\{7,3\}$, racine carrée pour le réseau plat — ce qui,
> combiné à une décroissance exponentielle en profondeur commune aux deux,
> donne $\kappa \sim N^{c}$ (polynomial) contre
> $\kappa \sim e^{c\sqrt N}$ (sur-polynomial). **C'est l'énoncé correct de
> H1**, remplaçant la formulation initiale en §1/§2 ci-dessous, qui reste
> affichée pour la traçabilité mais dont l'argument de la décroissance par
> arête doit être lu comme **corrigé par cette révision**.

## 1. Énoncé

> **(H1, fr)** Soit $G_N$ une famille de graphes planaires à $N$ nœuds, munis
> de conductances unitaires, dont l'ensemble de bord $\partial G_N$ est
> l'ensemble des nœuds de la face extérieure, et $\Lambda_N$ l'application
> de Dirichlet-vers-Neumann (réponse de bord). Soit $J_N$ la différentielle
> de $g \mapsto \Lambda_N(g)$ aux conductances unitaires, et
> $d(e)$ la profondeur d'une arête $e$ (distance de graphe au bord).
> **Sur un réseau euclidien** (disque de réseau carré ou triangulaire), la
> sensibilité $\|\partial\Lambda/\partial g_e\|$ décroît **exponentiellement**
> en $d(e)$, la profondeur maximale croît comme $\sqrt N$, et le
> conditionnement de $J_N$ dégénère exponentiellement en $\sqrt N$.
> **Sur un pavage hyperbolique $\{p,q\}$ tronqué par couches**, la
> profondeur maximale croît comme $\log N$, le bord reste une fraction
> finie des nœuds, et le conditionnement de $J_N$ ne dégénère que
> **polynomialement** en $N$ ; la reconstruction des conductances
> intérieures depuis le bord seul reste réalisable à bruit fixé quand $N$
> croît, là où elle échoue sur le réseau euclidien de même taille.

> **(H1, en)** On layer-truncated hyperbolic $\{p,q\}$ tilings, the
> boundary-to-bulk inverse conductance problem stays polynomially
> conditioned as the graph grows, because the maximal depth grows only as
> $\log N$; on Euclidean lattices of equal size it is exponentially
> ill-conditioned in $\sqrt N$. At fixed measurement noise, interior
> conductances are recoverable from boundary data in the hyperbolic case
> and not in the Euclidean one.

## 2. Pourquoi c'est plausible (l'argument, Tier C, avec ses appuis L)

1. **Le problème inverse de conductivité est exponentiellement instable
   avec la profondeur.** Dans le continu (problème de Calderón), la
   stabilité n'est que logarithmique (Alessandrini) et cette instabilité
   est optimale (Mandache, *Inverse Problems* 17, 2001) **[EXTERNE]** : une
   perturbation de conductivité à profondeur $d$ modifie les données de
   bord d'une quantité $\sim e^{-c\,d}$. Le réseau de résistances en est
   la discrétisation naturelle, et ses données de bord déterminent
   l'intérieur exactement pour les graphes planaires circulaires critiques
   (Curtis–Ingerman–Morrow 1998 ; Colin de Verdière 1994) **[EXTERNE]** —
   mais « déterminent » ne dit rien du conditionnement.
2. **En géométrie hyperbolique, la profondeur est bornée par
   $\log N$.** Le nombre de tuiles d'un pavage $\{p,q\}$ croît
   exponentiellement avec le nombre de couches (`2105.01087`,
   `2205.05693` [CORPUS]) ; donc un disque de $N$ nœuds n'a que
   $O(\log N)$ couches, et **aucun nœud n'est à plus de $O(\log N)$ du
   bord.** Le bord est une fraction finie des nœuds (là où, sur un réseau
   plat, elle tend vers $0$ comme $N^{-1/2}$).
3. **Combiner 1 et 2 :** sensibilité minimale $\sim e^{-c\log N} = N^{-c}$
   — polynomiale — au lieu de $e^{-c\sqrt N}$. C'est toute l'hypothèse.

**Le lien holographique, honnêtement.** En AdS, la coordonnée radiale est
l'échelle du groupe de renormalisation, et la profondeur dans le volume est
logarithmique en la taille du bord : c'est la même géométrie qui rend ici
le problème inverse bien posé. **H1 n'est pas l'holographie** (pas de
gravité, pas d'intrication, un Laplacien classique) ; c'est l'énoncé le
plus élémentaire dans lequel « la frontière contient le volume » devient
une propriété **quantitative et falsifiable** de la courbure négative. La
littérature d'holographie discrète mesure sur ces mêmes pavages la relation
masse–dimension d'échelle (`2005.12726`, `1912.07606` [CORPUS]) ; H1 en
est le versant « problème inverse ».

## 3. Ce que H1 prédit, chiffré (à préenregistrer avant chaque test)

| Quantité | Euclidien (disque carré, $N$ nœuds) | Hyperbolique ($\{7,3\}$, $L$ couches, $N$ nœuds) |
|---|---|---|
| fraction de bord $|\partial G|/N$ | $\to 0$ comme $N^{-1/2}$ | reste $\gtrsim 0{,}4$ |
| profondeur maximale $d_{\max}$ | $\sim \sqrt{N}/2$ | $= L \sim \log N$ |
| $\log\|\partial\Lambda/\partial g_e\|$ vs $d(e)$ | pente négative constante (exponentielle) | même pente locale, mais $d(e) \le L$ borné |
| $\log \kappa(J_N)$ vs $N$ | croît comme $\sqrt N$ | croît comme $\log N$ |
| reconstruction de 3 arêtes intérieures à 0,5 % de bruit | échoue au-delà d'un $N^\*$ modeste | réussit jusqu'aux tailles testées |

**Réfutation :** $\log\kappa$ hyperbolique croissant plus vite que
polynomialement ; ou reconstruction hyperbolique échouant au même $N$ que
l'euclidienne ; ou sensibilité hyperbolique décroissant avec $d$ **plus vite**
que l'euclidienne (ce qui indiquerait que la géométrie nuit au lieu
d'aider). Une seule de ces trois observations suffit.

**Ce qui rendrait le test `INVALIDE` :** un pavage mal construit (le
contrôle : caractéristique d'Euler $V-E+F=1$, degré $q$ à l'intérieur,
faces à $p$ côtés) ; un rang de $J$ inférieur au nombre d'arêtes dès le
cas exact (alors certaines arêtes sont **inrecouvrables** par construction,
et il faut restreindre l'énoncé aux arêtes recouvrables avant de parler de
conditionnement).

## 4. Chaîne de vérification (par tiers)

| Étape | Outil | Tier | Fichier |
|---|---|---|---|
| Construction des pavages et contrôles géométriques | Python, réflexions hyperboliques | X | `hyperbolic_network.py --self-test` |
| Comptages, profondeur, $J$, $\kappa$, sensibilité, reconstructions | numpy | X | `hyperbolic_network.py` |
| $\Lambda$ et rang de $J$ **en arithmétique rationnelle exacte** sur $\{7,3\}$ à 1–2 couches | `fractions.Fraction` | **B** | `hyperbolic_exact.py` (à écrire après H0) |
| Croissance exponentielle des couches / profondeur $\le L$ | Lean 4 (combinatoire finie de l'inflation) | **A** (cible) | `lean/` (après B) |
| Recouvrabilité exacte d'un petit réseau (Curtis–Morrow) | Lean 4 | **A** (long) | roadmap H3 |
| Réseau physique hyperbolique vs plat, même $N$ | résistances, ESP32 | expérience | `PREREGISTRATION.md` |

## 5. Ce que H1 apporte, s'il tient

- Une **raison quantitative** pour laquelle les pavages hyperboliques sont
  la plateforme naturelle de « reconstruction du volume depuis le bord » —
  argument absent, sous cette forme, des dix articles du pilier
  `hyperbolic` du corpus.
- Un **critère de conception** pour tout simulateur holographique discret
  (circuits, résonateurs, réseaux de tenseurs) : le rapport
  $d_{\max}/\log N$ mesure directement à quel point le bord « voit »
  l'intérieur.
- Une **expérience de garage à contrôle intégré** : deux réseaux de même
  taille, un seul paramètre changé (la courbure de la connectivité), une
  prédiction opposée pour chacun.

## 6. Ce que H1 n'apporte pas

Aucune conclusion sur la gravité quantique, sur l'intrication, ni sur
AdS/CFT au sens strict. Si H1 est confirmée, on aura montré qu'un
Laplacien sur un graphe à courbure négative rend un problème inverse bien
conditionné — c'est tout, et c'est déjà une phrase qu'un expert des
problèmes inverses et un expert d'holographie peuvent lire tous les deux
sans grimacer.
