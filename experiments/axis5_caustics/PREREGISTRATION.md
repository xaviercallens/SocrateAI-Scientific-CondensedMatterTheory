# Axe 5 — Caustiques et théorie des catastrophes

> Analyse critique : [`../../docs/experimental_program.md`](../../docs/experimental_program.md) §5.
> **Axe recommandé pour démarrer** avec l'axe 1a : le moins cher, le plus robuste.

## Pourquoi cet axe est le plus solide du programme

On ne cherche pas un effet fragile à faire apparaître : on vérifie une
**classification**. Le théorème de Thom–Arnold affirme que les caustiques d'une
famille **générique** de fronts d'onde n'appartiennent, en basse dimension,
qu'à une liste **finie** de types stables. Plus la lame est irrégulière, mieux
la démonstration fonctionne — le désordre est le sujet, pas le bruit. L'axe est
donc insensible à la qualité de fabrication, ce qui est rare.

---

## Affirmation
Les singularités du réseau de caustiques produit par une surface réfractante
aléatoire n'appartiennent, de façon stable, qu'à la liste d'Arnold —
pli ($A_2$), fronce ($A_3$), queue d'aronde ($A_4$), ombilics ($D_4^\pm$) — et
en particulier **aucune singularité d'ordre supérieur n'apparaît de façon
stable** sous déformation continue de la lame.

## Observable
Image d'intensité $I(x,y)$ du réseau projeté. Grandeurs dérivées :
- squelette du réseau (lignes de haute intensité) et ses **points de
  branchement** ;
- comptage des **fronces** (points de rebroussement) par unité de surface ;
- diagramme de persistance de $H_0$ et $H_1$ de la filtration par sur-niveau de
  $I$, suivi pendant la déformation.

## Protocole
- Source : laser élargi (télescope), ou simple LED ponctuelle — la cohérence
  n'est pas requise, et une LED **supprime le speckle**, qui est le principal
  parasite avec un laser.
- Surface réfractante, par ordre de simplicité :
  (a) surface d'eau faiblement ridée dans l'aquarium de l'axe 1 ;
  (b) film plastique étiré sur un cadre ;
  (c) résine transparente coulée dans un moule imprimé.
  **Une plaque imprimée en FDM n'est pas optiquement transparente** : ne pas
  compter dessus.
- Projection sur écran mat à 1–2 m ; caméra en RAW, exposition fixe.
- **Déformation continue** : inclinaison ou étirement par pas fins, ≥ 50 images,
  pour observer naissances et morts de fronces.
- Témoin : plaque **plane** (aucune caustique) et lentille **sphérique** (un
  seul point focal, pas de réseau).

## Prédiction
- Le squelette est formé de lignes lisses (plis) se rejoignant en points de
  rebroussement (fronces).
- **Les singularités d'ordre supérieur ($A_4$, $D_4$) n'apparaissent qu'en
  points isolés du paramètre de déformation**, et disparaissent dès qu'on
  s'en écarte — c'est le contenu expérimental de la notion de stabilité.
- Les événements de naissance/mort de fronces apparaissent comme des paires
  naissance–mort dans le diagramme de persistance de $H_1$.
- Témoin plan : aucune structure ; témoin sphérique : un point, pas de réseau.

## Hypothèse nulle
Le réseau ne présente pas de structure classifiable : les points de branchement
ont des ordres variés et arbitraires, sans hiérarchie de stabilité, et la
statistique est indiscernable d'un champ d'intensité aléatoire lissé.

## Critère de réfutation
Observation **reproductible et stable sous déformation** d'une singularité hors
de la liste d'Arnold ; ou statistique de branchement indiscernable de celle d'un
champ gaussien lissé de même spectre (contrôle par simulation).

## Analyses prévues
Extraction de squelette par amincissement morphologique ; comptage des
rebroussements ; Gudhi pour la persistance $H_0/H_1$ sur la filtration en
sur-niveau, **systématiquement accompagnée du même calcul sur le champ gaussien
de contrôle**.

## Causes d'échec connues (→ `INVALIDE`)
- **Speckle** si laser cohérent : passer à une LED, ou moyenner avec un
  diffuseur tournant.
- Saturation de la caméra sur les lignes de caustique : bracketing d'exposition,
  travail en HDR.
- Lame trop lisse (aucune caustique) ou trop rugueuse (réseaux imbriqués
  ininterprétables) : régler l'amplitude avant d'acquérir en série.
- Reflets multiples entre faces de la lame : biseauter, ou traiter la face
  arrière.

## Pourquoi Gudhi est ici pleinement à sa place
Contrairement à l'axe 1, où l'homologie persistante serait un ajout artificiel
(la localisation de bord se mesure par FFT et longueur de décroissance), le
réseau de caustiques **est** un objet topologique : un graphe dont les nombres
de Betti changent par événements discrets sous déformation continue. C'est
exactement ce qu'un diagramme de persistance décrit, et de façon stable au bruit
et au choix de seuil — ce qu'un seuillage d'intensité ne donne pas.
