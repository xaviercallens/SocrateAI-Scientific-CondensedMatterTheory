# Axe 3 — Vortex et charge topologique

> Analyse critique : [`../../docs/experimental_program.md`](../../docs/experimental_program.md) §3.
> Protocole : [`../../docs/rigor_protocol.md`](../../docs/rigor_protocol.md).

## Décision de voie à prendre avant tout achat

La lame de phase spirale imprimée en 3D **ne peut pas fonctionner en optique** :
elle demande une hauteur totale $h = \ell\lambda/(n-1) = 1{,}3\ \mu$m avec une
précision de forme de ~65 nm, soit 40 à 80 fois plus fin que la couche d'une
imprimante FDM ou SLA. Ce n'est pas un problème de réglage.

| Voie | Support | Charge quantifiée | Mesure de phase | 3D utile |
|---|---|---|---|---|
| **A** — hologramme en fourche | film transparent + laser | oui | interférométrie (difficile) | non |
| **B** — vortex acoustique | anneau de haut-parleurs déphasés | oui | microphone balayé (facile) | supports seulement |

**Voie B recommandée.** À 3 kHz dans l'air, $\lambda \approx 11$ cm. Le contenu
mathématique — singularité de phase, moment cinétique orbital, nombre
d'enroulement entier — est **identique** au cas optique, et la phase se mesure
directement, ce qui est le point dur en optique.

**Pas de lame transmissive.** L'impédance acoustique du PLA vaut ~$10^4$ fois
celle de l'air : une plaque de 1 cm transmet environ −44 dB à 3 kHz. C'est un
miroir, pas une lame de phase, et la formule $h = \ell\lambda/(n-1)$ ne
s'applique pas. Le vortex est donc produit par un **anneau de $N = 8$
haut-parleurs** alimentés avec des déphasages $2\pi\ell n/N$ ; $\ell$ devient un
paramètre logiciel. (Alternative : surface hélicoïdale **réfléchissante**
imprimée, de hauteur totale $\ell\lambda/2 \approx 5{,}5$ cm.)

Le préenregistrement ci-dessous est rédigé pour la voie B ; la voie A utilise
les mêmes critères sur l'intensité seule.

---

## Affirmation
Un anneau de sources déphasées de $2\pi\ell n/N$ produit une onde portant une
singularité de phase sur l'axe ; l'intégrale de la phase sur un contour fermé entourant l'axe
vaut $2\pi\ell$ avec $\ell$ **entier**, et cet entier est **inchangé** lorsqu'un
obstacle est inséré dans le faisceau.

## Observable
Champ complexe $p(x,y)$ dans un plan transverse, amplitude et phase, obtenu par
balayage d'un microphone sur une grille, en référence de phase avec le signal
d'excitation.
Grandeur dérivée : $\ell = \frac{1}{2\pi}\oint \nabla\varphi \cdot d\mathbf{l}$
sur plusieurs contours de rayons différents.

## Protocole
- $f = 3$ kHz ($\lambda = 11$ cm).
- Anneau de $N = 8$ petits haut-parleurs sur un cercle de rayon ~10 cm, support
  imprimé ; interface audio 8 canaux ; déphasage du canal $n$ : $2\pi\ell n/N$.
- **Étalonnage préalable** : amplitude et phase de chaque haut-parleur mesurées
  isolément, puis compensées. Sans cela, $\ell$ n'est pas entier *par
  construction*.
- Grille de mesure 30 × 30 points, pas 2 cm, à 50 cm de l'anneau.
- Microphone + interface audio ; référence de phase = signal d'excitation.
- Conditions : $\ell = 0$ (tous en phase, témoin) ; $\ell = 1$ ; $\ell = 2$ ;
  $\ell = 1$ **avec obstacle** (disque imprimé de 3 cm décentré).
- 3 répétitions.

## Prédiction
- $\ell = 0$ : maximum d'amplitude sur l'axe, aucune circulation de phase
  ($|\oint| < 0{,}3 \times 2\pi$).
- $\ell = 1$ : **creux** d'amplitude sur l'axe ($\le 20$ % du maximum annulaire),
  circulation $= 2\pi \pm 0{,}3 \times 2\pi$.
- $\ell = 2$ : circulation $= 4\pi$, creux plus large.
- **Avec obstacle : la circulation reste $2\pi$** (entier inchangé), même si
  l'amplitude est fortement déformée.

## Hypothèse nulle
La circulation mesurée n'est pas quantifiée : elle varie continûment avec le
rayon du contour, ou change de valeur quand l'obstacle est inséré.

## Critère de réfutation
$|\ell_{\text{mesuré}} - \ell_{\text{nominal}}| > 0{,}3$ pour l'un des contours,
ou changement de $\ell$ de plus de 0,3 à l'insertion de l'obstacle.

## Analyses prévues
Déroulement de phase 2D ; intégrale de circulation sur ≥ 4 rayons de contour ;
localisation du zéro d'amplitude. Gudhi : persistance de la classe $H_1$ du
sous-niveau d'amplitude, **avec la même analyse sur le témoin $\ell = 0$**
comme contrôle négatif.

## Causes d'échec connues (→ `INVALIDE`)
- Réflexions sur les murs de la cave : mousse absorbante, ou fenêtrage temporel
  pour isoler le front direct.
- Champ proche : rester à $\ge 3\lambda$ de l'anneau.
- Dérive de phase de l'interface audio : réinjecter la référence à chaque point.
- Haut-parleurs non appariés en amplitude ou en phase → $\ell$ non entier
  **par construction**. Étalonner chaque voie isolément avant la campagne.
- Trop peu de sources ($N < 2|\ell|+1$) : le champ n'échantillonne pas la
  phase azimutale ; garder $N = 8$ pour $|\ell| \le 2$.

## Correction factuelle reportée du plan initial
Pas de piste : **CD 1,6 µm, DVD 0,74 µm, Blu-ray 0,32 µm** (le plan attribuait
0,74 µm au CD). À $\lambda = 650$ nm, le premier ordre sort à **24° pour un CD**,
**61° pour un DVD** — une vérification de montage à faire à l'œil.
