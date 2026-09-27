# Axe 4 — Chaos ondulatoire : billard micro-ondes

> Analyse critique : [`../../docs/experimental_program.md`](../../docs/experimental_program.md) §4.
> Sécurité : [`../../docs/safety.md`](../../docs/safety.md) §1 — **lire avant d'ouvrir le four**.

## Pivot par rapport au plan initial

La version optique (laser dans un billard tapissé de morceaux de CD) ne peut pas
livrer le résultat visé :

- les CD sont des **réseaux de diffraction** de pas 1,6 µm, pas des miroirs :
  chaque rebond disperse la lumière en ordres multiples ;
- le chaos **ondulatoire** (loi de Weyl, statistique spectrale) demande des
  **modes résonants**. Dans une cavité de 20 cm à 650 nm, l'espacement des modes
  est de l'ordre de $10^{-12}$ m : il faudrait un laser monomode accordable.

Le billard **micro-ondes** est l'expérience canonique du domaine et devient
accessible pour ~100 €. La carcasse du four y est utilisée **entièrement
passive** : magnétron, transformateur et condensateur déposés.

---

## Affirmation
Une cavité micro-ondes quasi-2D en forme de billard de Sinaï possède un spectre
dont la fonction de comptage suit la loi de Weyl
$N(k) \simeq \frac{A}{4\pi}k^2 - \frac{P}{4\pi}k$, où $A$ et $P$ sont l'aire et
le périmètre — c'est-à-dire que **la géométrie détermine le spectre**.

## Observable
$|S_{21}(f)|$ entre deux antennes, de 0,5 à 6 GHz. Chaque résonance est un mode.
Grandeurs dérivées : fonction de comptage $N(k)$ ; après dépliage,
distribution des espacements $P(s)$.

## Protocole
- Cavité : carcasse de four, ~30 × 30 cm, hauteur réduite à $d = 8$ mm par une
  plaque métallique. Sous $c/2d = 18{,}7$ GHz, seuls les modes TM₀ existent :
  la cavité est **rigoureusement 2D**, et l'équation de Helmholtz y est celle
  d'un billard quantique.
- Diffuseur de Sinaï : cylindre imprimé en 3D, recouvert d'adhésif aluminium,
  diamètre 6 cm, **déplaçable**.
- NanoVNA / LiteVNA, deux antennes fouet couplées faiblement par de petits
  trous.
- Acquisition sur 10 positions du diffuseur (pour moyenner la statistique) ;
  plus une **cavité rectangulaire vide** comme témoin **intégrable**.

## Prédiction
- **Loi de Weyl** : ajustement de $N(k)$ donnant une aire à moins de 10 % de
  $A$ mesurée au mètre, et un terme de périmètre de signe négatif.
- Nombre de modes attendu jusqu'à 6 GHz ($k = 126\ \mathrm{m^{-1}}$,
  $A = 0{,}09\ \mathrm{m^2}$) : $N \approx A k^2/4\pi \approx 113$.
- **Statistique** : billard de Sinaï → répulsion de niveaux, $P(s)$ de type
  **GOE** (Wigner), $P(s\to0)\to 0$. Rectangle témoin → **Poisson**,
  $P(s\to0)$ maximal.

## Hypothèse nulle
$N(k)$ ne suit pas une loi quadratique, ou l'aire ajustée s'écarte de plus de
30 % de l'aire réelle ; et $P(s)$ est identique pour le Sinaï et le rectangle.

## Critère de réfutation
- Weyl : aire ajustée hors de ±30 % de l'aire géométrique.
- Statistique : Sinaï et rectangle non distinguables (Kolmogorov–Smirnov,
  $p > 0{,}05$).

## Hiérarchie des objectifs — à fixer maintenant
**La loi de Weyl est l'objectif principal** : ~113 modes suffisent largement à
ajuster deux paramètres.
**La statistique GOE est l'objectif secondaire** : distinguer GOE de Poisson sur
113 niveaux est possible mais bruité. Si elle sort `NON CONCLUANT`, c'est un
résultat attendu, pas un échec — et le remède est connu : agrandir la cavité ou
moyenner sur plus de positions du diffuseur.

## Analyses prévues
Détection de pics sur $|S_{21}|$ avec seuil fixé d'avance ; ajustement de
Lorentziennes ; dépliage par la courbe de Weyl ajustée ; $P(s)$ et
statistique $\Sigma^2$.

## Causes d'échec connues (→ `INVALIDE`)
- Couplage d'antenne trop fort : élargit les résonances jusqu'au recouvrement.
  Réduire la pénétration jusqu'à ce que les positions de pic cessent de bouger.
- Mauvais contact électrique de la plaque supérieure : fuites, modes parasites.
  Adhésif cuivre sur tout le pourtour.
- Modes hors-plan si $f > c/2d$ : rester sous 18 GHz (le VNA s'arrête à 6).
- Calibration du VNA absente ou dérivant en température.

## Référence à retirer du plan initial
Le lien avec l'**amplituèdre** ne tient pas et doit disparaître du texte. La
matrice $S$ d'une cavité chaotique relève de la **théorie des matrices
aléatoires** (Wigner–Dyson) ; l'amplituèdre est une géométrie positive calculant
les amplitudes de $\mathcal{N}=4$ super-Yang–Mills. Aucun énoncé ne relie les
deux. La vraie question — « peut-on entendre la forme d'un tambour ? » (Kac) —
est déjà excellente, et elle est exacte.
