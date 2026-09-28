# Préenregistrement — H0, point de donnée L=4 (confirmation)

> Écrit et commité **avant** l'exécution de `hyperbolic_network.py --max-layers 4`.
> Les points $L=1,2,3$ ont déjà été mesurés dans la passe exploratoire non
> verrouillée documentée dans [`HYPOTHESIS.md`](HYPOTHESIS.md) ; $L=4$ est
> une donnée **neuve**, jamais calculée au moment de l'écriture de ce
> document (la graine `rng.default_rng(7)` est fixe, donc $L=1..3$
> reproduiront des nombres déjà connus — seul $L=4$ teste quelque chose).

## Affirmation

Sur $\{7,3\}$, $\log_{10}\kappa(J)$ à $L=4$ continue la tendance
**linéaire en profondeur** observée à $L=1..3$ (pente ≈ 0,47/couche,
ordonnée à l'origine ≈ 0,92 sur l'ajustement des trois premiers points),
**et non** une tendance en $\sqrt N$ comme le réseau plat.

## Prédiction chiffrée

- Profondeur max à $L=4$ : **7** (pattern 1,3,5,7 — un pas de 2 par couche,
  déjà exact sur les 3 points connus).
- $N$ à $L=4$ : le nombre de tuiles par couche pour $\{7,3\}$ est
  1,7,21,56 (vérifié en `self_test`, séquence géométrique de raison
  $\to 2{,}67$) ; $L=4$ doit ajouter $\sim 56\times 2{,}67 \approx 150$
  nouvelles tuiles, portant $N$ à l'ordre de **800–900**.
- $\log_{10}\kappa$ à $L=4$ : extrapolation linéaire en profondeur depuis
  les 3 points connus $\Rightarrow \mathbf{4{,}2 \pm 0{,}5}$ (barre large :
  un seul régime linéaire local n'est pas garanti au-delà de 3 points).
- **Critère de séparation** (le seul qui compte vraiment) :
  $\log_{10}\kappa(\{7,3\}, L{=}4)$ doit être **strictement inférieur** à
  $\log_{10}\kappa$ d'un réseau plat de $N$ comparable (~800), qui,
  extrapolé linéairement depuis les 3 points carrés connus (pente
  ≈ 1,14/couche, profondeur attendue $\sim\sqrt{800/\pi}\times2\approx32$),
  serait de l'ordre de $\mathbf{15}$–$\mathbf{20}$ — un écart attendu
  d'au moins **10 décades**.

## Hypothèse nulle

$\log_{10}\kappa(\{7,3\}, L{=}4)$ rejoint ou dépasse l'extrapolation du
réseau plat à $N$ comparable, ou cesse de suivre une tendance linéaire en
profondeur (rupture de pente visible sur les 4 points).

## Critère de réfutation

$\log_{10}\kappa(\{7,3\}, L{=}4) > 8$ (à mi-chemin de l'extrapolation
plate) **ou** rupture de linéarité en profondeur détectable à l'œil sur le
graphe (résidu > 1 décade par rapport à l'ajustement des 3 premiers
points).

## Causes d'échec connues

- SVD lente ou mémoire insuffisante à $N\sim850$ ($E\sim1100$,
  $\dim(\text{DtN})\sim{600}\times{600}\Rightarrow J$ de taille
  $\sim180000\times1100$) : réduire à `--max-layers 4` seul (pas de
  balayage plat à cette taille, déjà mesuré à $N\sim317$ suffit pour la
  comparaison).
- Rang déficient à $L=4$ (comme observé pour le réseau triangulaire à
  $N=421$) : rapporter le déficit, restreindre $\kappa$ au sous-espace
  identifiable (déjà fait par construction dans `analyse()`).

## Verdict

Un seul verdict, au sens de
[`../../docs/rigor_protocol.md`](../../docs/rigor_protocol.md) §3 :
`CONFIRMÉ` si le critère de séparation tient ET que la prédiction
$4{,}2\pm0{,}5$ est dans la barre ; `NON CONCLUANT` si la séparation tient
mais hors barre (la tendance qualitative est bonne, le modèle quantitatif
linéaire-en-profondeur ne l'est pas) ; `RÉFUTÉ` si le critère de
réfutation se déclenche.
