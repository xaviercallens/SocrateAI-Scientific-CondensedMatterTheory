# Résultats H0 — H1 confirmée sur le point préenregistré (Tier X)

> Préenregistré dans [`PREREGISTRATION.md`](PREREGISTRATION.md) avant
> exécution. Mécanique et passe exploratoire (non verrouillée, antérieure)
> dans [`HYPOTHESIS.md`](HYPOTHESIS.md). Grand livre :
> [`../../docs/elenchus/ledger.json`](../../docs/elenchus/ledger.json),
> `H0-X-0001` (corrigé par `H0-X-0002` ci-dessous).

## ERRATUM (2026-09-27, même jour, avant toute rédaction ultérieure)

**Un bug de mesure, pas un résultat physique**, a produit le « plafond »
décrit plus bas en §« Ce qui reste incertain » dans sa version initiale.
La fonction qui calculait $\kappa$ le bornait par sa propre formule de
tolérance de rang : `kappa = s_max / s[rank-1]`, et comme
`s[rank-1] > tol = s_max * max(forme) * eps` par construction,
$\kappa < 1/(\text{max(forme)} \times \epsilon)$ **toujours**, quelle que
soit la vraie valeur physique. Un relecteur externe l'a signalé ; vérifié
directement : pour les trois plus grands cas plats de la passe précédente,
le $\log_{10}\kappa$ « saturé » rapporté correspondait à
$\log_{10}(1/(\text{max(forme)}\times\epsilon))$ à 4 chiffres significatifs
— carré $N=797$ : plafond $10^{11,771}$ contre rapporté $10^{11,77}$ ;
triangulaire $N=1069$ : $10^{11,710}$ contre $10^{11,71}$ ; triangulaire
$N=421$ : $10^{12,111}$ contre $10^{12,10}$. Ce n'est pas une coïncidence à
cette précision : c'était la formule, pas le calcul.

**Corrigé** : `analyse()` rapporte maintenant $\kappa_{\text{brut}} =
s_{\max}/s_{\min}$, **sans troncature**, et signale explicitement quand le
réseau est **numériquement singulier** (`s_min` arrondi à 0 ou au bruit de
`float64`) plutôt que d'afficher un nombre — un plantage silencieux évité,
pas une mesure inventée. Résultat recalculé et **plus fort**, pas plus
faible : les grands réseaux plats ne « plafonnent » pas à ~12 décades, ils
deviennent **exactement singuliers en `float64`** dès $N\sim420$–$1100$
([`figures/h0.png`](figures/h0.png), marqueurs « x », droite). Les points
non affectés (tout `{7,3}`, et les réseaux plats jusqu'à $N=317$) sont
**inchangés** — le tableau du verdict ci-dessous et l'écart à $N\sim315$
restent valides tels quels. L'entrée `H0-X-0001` du grand livre est
remplacée par `H0-X-0002` ; `H0-X-0001` reste dans le fichier comme trace
de l'erreur, avec la correction en note.

**Autre correction, même relecture** : l'attribution « Deban, Borcea *et
al.* » pour `1107.0343` en §« Recherche de nouveauté » était fautive — les
auteurs réels, vérifiés dans `papers/meta/1107.0343.json`, sont **Borcea,
Druskin, Guevara Vasquez & Mamonov**. Corrigé ci-dessous.

## Verdict : `CONFIRMÉ`

| | prédit | mesuré |
|---|---|---|
| profondeur max, $L=4$ | 7 | **7** (exact) |
| $N$, $L=4$ | 800–900 | **847** |
| $\log_{10}\kappa$, $L=4$ | $4{,}2\pm0{,}5$ | **3,89** (dans la barre) |
| critère de séparation ($\log_{10}\kappa < 8$) | — | **3,89**, séparation nette |

**Le résultat central, plus fort que la barre préenregistrée ne l'exigeait,
et plus fort encore après la correction de l'erratum ci-dessus :** à
$N=315$–$317$ (dernier point commun mesurable des deux côtés), le réseau
hyperbolique donne $\log_{10}\kappa=3{,}27$ contre $\log_{10}\kappa=9{,}72$
pour le carré plat — **un écart de 6,4 décades**, ce chiffre-là inchangé
par l'erratum. À $N$ apparié ~800, le réseau hyperbolique reste mesurable
($\log_{10}\kappa=3{,}89$) alors que le jacobien du réseau plat est déjà
**numériquement singulier en `float64`** — un écart plus fort qu'un simple
nombre de décades, puisqu'aucun conditionnement fini ne peut même être
assigné au cas plat à cette taille avec cette méthode. L'écart se creuse
avec $N$, comme H1 le prédit — plus vite, en fait, que ce que la version
non corrigée de ce document affirmait.

## Constat de rang, $N\le317$ (mesure `float64` standard) — **corrigé
plus bas, voir « Certification de rang exacte »**

Aux tailles où $\kappa$ reste mesurable, le réseau hyperbolique $\{7,3\}$
est à rang plein (42/42, 140/140, 399/399, 1078/1078) ; le réseau
triangulaire plat semblait montrer un déficit dès $N=421$ (102/1176) en
`float64`. **La section « Certification de rang exacte » ci-dessous
montre que ce déficit était, lui aussi, un artefact de précision — le
réseau plat est en réalité de rang plein à cette taille.** Le paragraphe
suivant est laissé tel qu'écrit initialement, comme trace, et corrigé
explicitement plus bas plutôt que supprimé.
**Ce déficit de rang « numérique » est calculé avec la même tolérance
`tol = s_max*max(forme)*eps`** dont l'erratum ci-dessus vient de montrer
qu'elle produit des artefacts en aval (sur $\kappa$). Il n'est donc **pas**
certifié que ces arêtes soient *structurellement* inrecouvrables (rang
mathématique déficient) plutôt que *numériquement* indiscernables d'un
rang déficient en `float64` à cette taille. Formulation prudente adoptée
ici : « rang numérique déficient », pas « structurellement
inrecouvrable ». Le calcul exact (arithmétique modulaire, ci-dessous)
tranchera.

## Certification de rang exacte (Tier B) — arithmétique modulaire

Avec des conductances unitaires, le Laplacien $L$ est une matrice
**entière**. Pour un nombre premier $p$ tel que $\det(L_{ii}) \not\equiv 0
\pmod p$, le jacobien $J$ (construit à partir de $L_{ii}^{-1}$) est
$p$-intégral au sens approprié, et
$\mathrm{rang}_{\mathbb{Q}}(J) \ge \mathrm{rang}_{\mathbb{F}_p}(J \bmod p)$ :
le rang sur un corps fini **certifie une borne inférieure exacte** sur le
vrai rang rationnel, sans aucune ambiguïté de virgule flottante. Accord
entre deux nombres premiers indépendants ⇒ certificat, pas une mesure.
Voir [`hyperbolic_exact.py`](hyperbolic_exact.py) (6/6 auto-tests, dont un
recoupement avec le rang flottant sur le cas connu $L=1$).

### Résultat, et il change la conclusion sur le rang

| Cas | rang (deux nombres premiers) | verdict |
|---|---|---|
| $\{7,3\}$, $L=1$ ($N=35$, $E=42$) | 42, 42 | **plein, certifié** |
| $\{7,3\}$, $L=2$ ($N=112$, $E=140$) | 140, 140 | **plein, certifié** |
| carré, $N=113$ ($E=200$) | 200, 200 | plein, certifié |
| triangulaire, $N=187$ ($E=502$) | 502, 502 | plein, certifié |
| **triangulaire, $N=475$ ($E=1331$)** | **1331, 1331** | **plein, certifié** |

**La dernière ligne renverse le constat de la section précédente.** Ce
réseau (taille comparable au triangulaire $N=421$ qui montrait un déficit
de 102/1176 en `float64`) est **exactement de rang plein** — accord parfait
entre les deux nombres premiers, donc certifié, pas une coïncidence de
précision. **Le déficit de rang mesuré en `float64` sur les grands
réseaux plats n'était pas une propriété structurelle : c'était, lui
aussi, un artefact de précision flottante**, du même ordre que le bug de
$\kappa$ corrigé plus haut, mais sur une quantité différente (le rang
plutôt que le rapport des valeurs singulières).

**Conséquence pour H1, à prendre au sérieux.** Le contenu réel de H1
n'est **pas** une différence d'identifiabilité structurelle
(hyperbolique = toujours récupérable, plat = parfois non) — les deux
familles sont, à ces tailles, **exactement de rang plein toutes les
deux**. Le contenu réel de H1 est **purement une question de
conditionnement** : la précision (le nombre de chiffres significatifs)
nécessaire pour effectivement récupérer l'information croît
polynomialement avec $N$ pour l'hyperbolique, et devient si vite
astronomique pour le plat qu'aucune précision physiquement raisonnable
(ou même `float64`) ne suffit. C'est une distinction plus fine que « parfois
impossible » — et c'est la bonne façon de formuler H1 pour un article,
remplaçant tout langage de « structurellement inrecouvrable » utilisé plus
haut dans une version antérieure de ce document.

## Recherche de nouveauté (bornée dans le temps, honnête sur sa portée)

Recherche menée : « resistor network inverse problem hyperbolic lattice
conditioning boundary », « discrete Calderón problem stability depth
hyperbolic graph Gromov ». **Rien trouvé formulant précisément le lien
profondeur-logarithmique / conditionnement-polynomial pour un réseau de
résistances sur pavage hyperbolique** — mais cette recherche est bornée
(deux requêtes, pas une revue systématique), donc l'énoncé correct est
**« non trouvé dans cette recherche »**, pas « inédit ».

Deux résultats directement pertinents, maintenant dans le corpus
(pilier `hyperbolic`) :

- **Borcea, Druskin, Guevara Vasquez & Mamonov, « Resistor network
  approaches to electrical impedance tomography » (`1107.0343`)** —
  confirme, par une méthode différente (*layer peeling* sur grilles
  optimales), exactement le phénomène mesuré ici côté plat : l'instabilité
  croissante avec la taille du réseau. **Le côté « réseau plat » de H1
  n'est donc pas une observation isolée : c'est la manifestation, sur un
  réseau de résistances, d'un fait déjà établi dans la littérature d'EIT.**
- **Ervedoza & de Gournay, « Uniform stability estimates for the discrete
  Calderón problems » (`1104.4858`)** — bornes de stabilité **logarithmiques**
  pour le problème de Calderón discret, en dimension $d\ge3$ (pas le cas
  2D de ce travail) ; motive le mécanisme sans le couvrir.

Piste adjacente non vérifiée : les graphes hyperboliques sont
Gromov-hyperboliques, donc « arborescents » à grande échelle — H1 pourrait
être, en partie, un corollaire de résultats de reconstruction de métrique
d'arbre depuis les distances aux feuilles, non recherchés ici faute de
temps.

## Ce que H0 autorise, et ce qu'il n'autorise **pas encore**

Le critère d'arrêt H0 de
[`roadmap_holographie_analogique.md`](../../docs/roadmap_holographie_analogique.md)
est atteint pour la **conditionnement** : $\{7,3\}$ reste mesurable et bien
séparé du plat jusqu'à $N=847$. **Mais « H0 passe » ne veut pas dire
« construire $L=2$ » va de soi** — c'est une conclusion trop rapide que la
propre simulation contredit déjà : `recon=False` à $L=2$
($\kappa(L{=}2)\approx10^{2{,}46}\approx290$, bruit additif $10^{-3}$ ⇒
erreur de reconstruction attendue $\sim0{,}29$, au-dessus du seuil de
succès $0{,}15$ déjà préenregistré). Deux options, pas encore tranchées,
avant de commander la première résistance :

1. **Spécifier le matériel** pour une erreur relative totale
   $\lesssim5\times10^{-4}$ (budget partagé entre l'ADC, la précision des
   résistances pré-mesurées et la résistance de contact) — recalculer
   `recon` avec ce budget avant d'acheter quoi que ce soit.
2. **Ou reformuler H1b en imagerie différentielle** (localiser 1–2
   résistances *changées* depuis $\Delta\Lambda$, un problème bien mieux
   conditionné que la reconstruction absolue).

**Un second point matériel, distinct, à trancher avant la liste de
composants** : le montage décrit (injection de courant, lecture de
tension) mesure l'application **Neumann-vers-Dirichlet** $\Lambda^{+}$
(sur le sous-espace à somme nulle), **pas** $\Lambda$ elle-même. Sa
jacobienne est $-\Lambda^{+}(\partial\Lambda/\partial g)\Lambda^{+}$, et
inverser vers $\Lambda$ amplifie le bruit par $\kappa(\Lambda)$ — un
facteur qui n'est plus négligeable là où $\kappa$ est justement grand. Soit
on simule directement $\Lambda^{+}$ (pas $\Lambda$), soit le montage
impose des tensions et mesure des courants. **À trancher avant la
nomenclature**, pas après.

## Prochaine étape

1. ~~`hyperbolic_exact.py` (Tier B)~~ — fait, voir ci-dessous.
2. Choisir entre les deux options ci-dessus (budget de précision, ou
   imagerie différentielle) et **simuler ce choix précisément** avant toute
   commande de matériel.
3. Trancher Neumann-vers-Dirichlet vs Dirichlet-vers-Neumann dans le
   montage physique.
4. Recherche de nouveauté approfondie (pas bornée à quelques requêtes)
   avant toute rédaction destinée à publication.
