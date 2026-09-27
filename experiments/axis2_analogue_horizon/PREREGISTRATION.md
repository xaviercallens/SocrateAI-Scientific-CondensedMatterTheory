# Axe 2 — Horizon analogue : superradiance sur vortex de vidange

> Analyse critique : [`../../docs/experimental_program.md`](../../docs/experimental_program.md) §2.
> Protocole : [`../../docs/rigor_protocol.md`](../../docs/rigor_protocol.md).

## Reformulation préalable — ne pas chercher le rayonnement de Hawking

La température de Hawking analogue d'un écoulement de paillasse
($\kappa \sim 1\ \mathrm{s^{-1}}$) vaut

$$T_H = \frac{\hbar\kappa}{2\pi k_B} \sim 10^{-12}\ \mathrm{K}$$

soit **quatorze ordres de grandeur** sous le bruit thermique ambiant. L'émission
spontanée est hors d'atteinte, définitivement et pour tout capteur.

Ce qui est mesurable, et qui l'a été (Weinfurtner *et al.*, `1008.1911` ;
Euvé *et al.*, `1511.08145` ; Torres *et al.*, `1612.06180` — tous trois dans le
corpus), c'est la **diffusion stimulée** : on envoie une onde connue et on mesure
la conversion de modes. C'est l'objet de ce préenregistrement.

---

## Affirmation
Un écoulement drainant-tournant possède une ergosphère ; une onde de surface
envoyée dans le sens de la rotation en ressort **amplifiée** (superradiance),
au détriment du moment cinétique de l'écoulement.

## Observable
Coefficient de réflexion $|R_{m}|^2$ pour un mode azimutal $m$, mesuré par FS-SS,
comparé entre $m > 0$ (corotatif) et $m < 0$ (contrarotatif).

## Protocole
- Bac cylindrique, diamètre ≥ 40 cm, bonde centrale, alimentation **tangentielle**
  en circuit fermé (pompe TBTS), profilé d'entrée imprimé en 3D.
- Régime stationnaire vérifié : hauteur d'eau stable à ±1 mm sur 10 min.
- Excitation d'ondes planes à la périphérie, $f = 2$–4 Hz.
- Décomposition azimutale de $\eta(r,\theta,t)$ en modes $m = \pm1, \pm2$.
- Témoin : **même bac, même débit, alimentation radiale** (pas de rotation) —
  aucune ergosphère, donc aucune amplification attendue.
- 5 répétitions ; sens de rotation inversé pour contrôler les asymétries du
  montage.

## Prédiction
$|R_m|^2 > 1$ pour les modes corotatifs dans la bande
$0 < \omega < m\Omega_H$, avec une amplification de 10 à 30 %.
$|R_m|^2 < 1$ pour les modes contrarotatifs.
Témoin sans rotation : $|R_m|^2 < 1$ pour les deux signes.

## Hypothèse nulle
$|R_m|^2 < 1$ partout : toute l'énergie envoyée est dissipée, sans transfert
depuis l'écoulement.

## Critère de réfutation
Pas de différence significative entre modes corotatifs et contrarotatifs
(test de Welch, $p > 0{,}05$ sur 5 répétitions), ou amplification inversée par
le changement de sens de rotation du montage — ce qui signalerait un artefact.

## Analyses prévues
Décomposition en modes azimutaux par FFT en $\theta$ ; détection synchrone en
$t$ ; estimation de $\Omega_H$ par le champ de vitesse mesuré, **indépendamment**
de la mesure de $|R|^2$.

## Causes d'échec connues (→ `INVALIDE`)
- Écoulement non stationnaire (battement de pompe) : filtrer, tamponner.
- Formation d'un entonnoir d'air jusqu'à la bonde : change entièrement le
  problème ; maintenir une hauteur d'eau suffisante.
- Amortissement visqueux dominant la conversion : mesurer d'abord l'atténuation
  sans écoulement.
- Ondes stationnaires sur la paroi cylindrique : absorbeur périphérique.

## Ce que cette expérience ne montre pas
**Rien sur la gravité quantique, ni sur l'holographie.** L'analogie de Unruh
reproduit la *cinématique* d'un champ sur une métrique courbe, non la
*dynamique* d'Einstein : pas de constante de Newton, pas d'action
d'Einstein–Hilbert, pas de rétroaction du champ sur la géométrie. Le résultat
porte sur la diffusion d'ondes sur un horizon effectif, et s'arrête là.
