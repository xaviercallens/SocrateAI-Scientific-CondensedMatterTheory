# Préenregistrement 2 — contrôle à nombre de sondes égal, application Neumann-vers-Dirichlet, et H2 (constante de temps RC)

> Écrit et commité **avant** l'exécution de `probe_matched.py` et
> `rc_network.py`. Aucun des nombres prédits ci-dessous n'a été calculé au
> moment de l'écriture.

## A. Contrôle à nombre de sondes égal (objection « plus d'électrodes »)

**Objection.** À $N\approx315$, $\{7,3\}$ dispose de 203 sondes de bord,
le disque carré de 76. L'écart de conditionnement pourrait venir du nombre
de sondes, pas de la géométrie.

**Protocole.** Sous-échantillonner le bord de $\{7,3\}$ à exactement le
nombre de sondes du réseau plat apparié (sondes régulièrement espacées en
angle ; les nœuds de bord non utilisés deviennent intérieurs, à courant
nul — modèle correct d'une électrode non branchée), et recalculer
$\kappa(J)$ exact (formule d'extension harmonique). Tailles : $L=2$ vs
carré $N=113$ (44 sondes) ; $L=3$ vs carré $N=317$ (76 sondes).

**Formes rivales, évaluées avant le calcul.**
- (a) *intrinsèque à la géométrie* : l'écart reste $\ge 2$ décades à
  $N\approx315$ ;
- (b) *artefact du nombre de sondes* : l'écart tombe sous 1 décade.

**Prédiction : (a).** $\log_{10}\kappa(\{7,3\}, L{=}3, 76\ \text{sondes})
\le 7{,}7$ (écart $\ge 2$ avec le carré à $9{,}72$).
**Réfutation :** écart $< 1$ décade.

## B. Application Neumann-vers-Dirichlet (ce que le matériel mesure)

Le montage injecte des courants et lit des tensions : il mesure
$\Lambda^{+}$ (pseudo-inverse sur le sous-espace à somme nulle), de
jacobienne $\partial\Lambda^{+}/\partial g_e =
-\Lambda^{+}(\partial\Lambda/\partial g_e)\Lambda^{+}$.

**Prédiction :** la séparation qualitative subsiste —
$\kappa(J_{\Lambda^+})$ reste plus petit pour $\{7,3\}$ que pour le carré
à $N$ apparié, pour $N\le317$. Pas de prédiction chiffrée sur l'ampleur
(aucune base pour la fixer). **Réfutation :** inversion de l'ordre à un
$N$ apparié.

## C. H2 — constante de temps du réseau RC (piste rusty-SUNDIALS)

**Modèle.** Chaque nœud porte une capacité $C=1$ vers la masse ; bord à
tension imposée : $C\,\dot V_i = -(L_{ii}V_i + L_{ib}V_b)$. Le temps de
relaxation est $\tau = C/\lambda_{\min}(L_{ii})$ ; la raideur
(*stiffness*) est $\lambda_{\max}(L_{ii})/\lambda_{\min}(L_{ii})$.

**Formes rivales pour $\lambda_{\min}(L_{ii})$ en fonction de $N$,
posées avant le calcul :** (i) bornée inférieurement par une constante ;
(ii) $\sim 1/\log^2 N$ ; (iii) $\sim 1/N$.

**Prédiction :** $\{7,3\}$ suit (i), les réseaux plats suivent (iii).
Motivation, non démonstration : un graphe hyperbolique régulier est non
moyennable, et le bas du spectre du laplacien d'un graphe non moyennable
de degré borné est strictement positif (Kesten ; Dodziuk ; Mohar
[EXTERNE]) ; sur un disque plat de rayon $R$, $\lambda_{\min}\sim R^{-2}
\sim N^{-1}$. **Réfutation :** $\lambda_{\min}(\{7,3\})$ décroissant d'un
facteur $\ge 2$ entre $L=2$ et $L=4$.

**Validation croisée à deux codes (cœur de la synergie rusty-SUNDIALS).**
1. *Contrôle à réponse connue* : pour ce système linéaire, la solution
   exacte est $V(t)=e^{-L_{ii}t}(V_0-V_\infty)+V_\infty$ (`scipy.linalg.expm`).
   Tout intégrateur (CVODE de rusty-SUNDIALS ; BDF de SciPy en référence)
   doit la reproduire à la tolérance demandée **avant** que ses autres
   sorties soient utilisées.
2. *Régime permanent = $\Lambda$* : sous $V_b=e_j$, les courants de bord
   à l'état stationnaire intégré sont la colonne $j$ de $\Lambda$ ; ils
   doivent coïncider avec le complément de Schur (numpy) à $10^{-6}$ près.

Le chemin rusty-SUNDIALS exige l'extension Python compilée
(`maturin`) ; si elle n'est pas importable, le contrôle 1 est exécuté avec
SciPy seul et le chemin CVODE est déclaré **non exécuté**, pas « réussi ».
