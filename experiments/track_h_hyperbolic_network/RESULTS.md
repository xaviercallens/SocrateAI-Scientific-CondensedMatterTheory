# Résultats H0 — H1 confirmée sur le point préenregistré (Tier X)

> Préenregistré dans [`PREREGISTRATION.md`](PREREGISTRATION.md) avant
> exécution. Mécanique et passe exploratoire (non verrouillée, antérieure)
> dans [`HYPOTHESIS.md`](HYPOTHESIS.md). Grand livre :
> [`../../docs/elenchus/ledger.json`](../../docs/elenchus/ledger.json),
> `H0-X-0001`.

## Verdict : `CONFIRMÉ`

| | prédit | mesuré |
|---|---|---|
| profondeur max, $L=4$ | 7 | **7** (exact) |
| $N$, $L=4$ | 800–900 | **847** |
| $\log_{10}\kappa$, $L=4$ | $4{,}2\pm0{,}5$ | **3,89** (dans la barre) |
| critère de séparation ($\log_{10}\kappa < 8$) | — | **3,89**, séparation nette |

**Le résultat central, plus fort que la barre préenregistrée ne l'exigeait :**
à $N$ apparié (~800), le réseau hyperbolique donne $\log_{10}\kappa=3{,}89$
contre $\log_{10}\kappa=11{,}77$ pour le carré plat — **un écart de 7,9
décades**, plus large encore qu'à $N\sim315$ (6,4 décades). L'écart se
creuse avec $N$, comme H1 le prédit.

## Constat non préenregistré, honnête à rapporter tel quel

Le réseau hyperbolique $\{7,3\}$ reste à **rang plein** à toutes les tailles
testées (42/42, 140/140, 399/399, **1078/1078**). Les réseaux plats
développent un déficit de rang **croissant** : carré 0/44 → 0/200 → 0/592 →
**185/1528** ; triangulaire 0/87 → 0/401 → 102/1176 → **1143/3071**. À
$N\sim1000$, plus du tiers des arêtes intérieures du réseau triangulaire
plat sont **structurellement inrecouvrables** depuis le bord, alors que le
réseau hyperbolique de taille comparable garde toutes ses arêtes
identifiables. Ce n'était pas dans la prédiction initiale ; ce n'est donc
pas cité comme confirmation de H1, mais comme un second phénomène,
cohérent avec H1 et probablement lié par le même mécanisme (bord
proportionnellement plus grand ⇒ plus d'équations que d'inconnues).

## Ce qui reste incertain, dit franchement

Les courbes de $\log_{10}\kappa$ des réseaux plats **s'aplatissent**
visiblement aux deux plus grandes tailles ([`figures/h0.png`](figures/h0.png),
panneau de droite : +4,65 décades entre $N=113$ et $N=317$, seulement
+2,05 entre $N=317$ et $N=797$ pour le carré). Deux lectures possibles,
non tranchées ici : (a) un véritable ralentissement physique de la
croissance de $\kappa$, ou (b) l'approche du plafond de précision de
`float64` ($\kappa_{\max}\sim10^{15\text{–}16}$), qui commence à comprimer
les valeurs mesurées avant ce plafond. $\log_{10}\kappa\sim12$ reste à
3–4 décades de ce plafond — probablement pas encore saturé, mais assez
proche pour que la question mérite un calcul en précision étendue
(`mpmath` ou `Fraction`) avant d'aller plus loin sur les grandes tailles
plates. **Cela ne change rien à la conclusion à $N\le850$**, où l'écart
mesuré (7,9 décades) est très au-dessus de tout artefact de précision
plausible à ces échelles.

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

- **Deban, Borcea *et al.*, « Resistor network approaches to electrical
  impedance tomography » (`1107.0343`)** — confirme, par une méthode
  différente (*layer peeling*), exactement le phénomène mesuré ici côté
  plat : la reconstruction devient rapidement instable quand la taille du
  réseau croît. **Le côté « réseau plat » de H1 n'est donc pas une
  observation isolée : c'est la manifestation, sur un réseau de
  résistances, d'un fait déjà établi dans la littérature d'EIT.**
- **« Uniform stability estimates for the discrete Calderón problems »
  (`1104.4858`)** — établit des bornes de stabilité **logarithmiques** pour
  le problème de Calderón discret sur réseau, dans un cadre général ; ne
  traite pas spécifiquement le cas hyperbolique.

Piste adjacente non vérifiée : les graphes hyperboliques sont
Gromov-hyperboliques, donc « arborescents » à grande échelle — H1 pourrait
être, en partie, un corollaire de résultats de reconstruction de métrique
d'arbre depuis les distances aux feuilles, non recherchés ici faute de
temps.

## Ce que H0 autorise maintenant

Le critère d'arrêt de [`roadmap.md`](../../docs/roadmap.md) M3 / de
[`roadmap_holographie_analogique.md`](../../docs/roadmap_holographie_analogique.md)
H0 est atteint : **on peut concevoir le premier montage.** Nombre de
conception recommandé : $\{7,3\}$, $L=2$ (112 nœuds, 140 résistances, 77
sondes de bord) pour le premier prototype — assez petit pour un câblage
manuel raisonnable, déjà à $\log_{10}\kappa=2{,}46$ (très bien conditionné),
avec un déficit de rang nul. $L=3$ (315 nœuds) comme cible d'extension une
fois H1a validé.

## Prochaine étape

1. `hyperbolic_exact.py` (Tier B) : reproduire le rang plein et un
   sous-ensemble de $\Lambda$ en arithmétique rationnelle exacte sur
   $\{7,3\}$ $L=1$–2, pour éliminer toute ambiguïté de précision flottante
   sur le résultat central.
2. Recherche de nouveauté approfondie (pas bornée à quelques requêtes)
   avant toute rédaction destinée à publication.
3. Construction physique $L=2$ (roadmap H1a).
