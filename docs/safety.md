# Sécurité

Trois dangers réels dans ce programme : le four à micro-ondes, les lasers, et
l'eau près du secteur. Chacun peut tuer ou rendre aveugle. Le reste du montage
est bénin.

---

## 1. Four à micro-ondes — le condensateur haute tension

**Le danger n'est pas le magnétron : c'est le condensateur.** Un four contient
un condensateur de ~1 µF chargé à ~2 kV. Il stocke environ 2 joules à haute
tension — largement de quoi provoquer une fibrillation cardiaque — et il peut
**conserver sa charge des semaines après le débranchement**. Beaucoup de fours
ont une résistance de décharge interne, mais elle tombe en panne silencieusement.
**Il faut toujours supposer que le condensateur est chargé.**

La carcasse n'est **inerte** que lorsque les pièces suivantes en ont été
physiquement retirées :

1. Débrancher, attendre au minimum 24 h.
2. **Décharger le condensateur** en court-circuitant ses bornes à travers une
   résistance de 10 kΩ / 5 W montée sur un manche isolé — jamais un tournevis
   nu, qui produit un arc et projette du métal en fusion.
3. Court-circuiter ensuite les bornes avec un fil, et **laisser ce fil en
   place**.
4. **Déposer** : condensateur, transformateur HT, diode HT, magnétron.
5. Vérifier au multimètre que rien ne subsiste entre les bornes.

**Le magnétron ne doit jamais être alimenté hors de sa cavité fermée.** Une
fuite de micro-ondes cuit la cornée et le cristallin sans aucune sensation
d'avertissement, et la cataracte qui suit est irréversible. Ce programme
n'utilise **jamais** le magnétron : l'axe 4 emploie un VNA de quelques
milliwatts.

Précaution supplémentaire : les aimants en ferrite du magnétron sont puissants
— les tenir loin des cartes, disques durs et porteurs de stimulateur cardiaque.

---

## 2. Lasers

**Le risque est la rétine, et il est instantané.** Une brûlure rétinienne se
produit plus vite que le réflexe de clignement (~0,25 s) et ne fait pas mal :
la rétine n'a pas de récepteurs de douleur. On ne s'aperçoit de rien.

- **Lunettes adaptées à la longueur d'onde et à la densité optique.** Des
  lunettes pour 650 nm ne protègent pas à 780 nm. Elles doivent porter la
  longueur d'onde et l'OD imprimés.
- **Traiter tout bloc optique (OPU) comme émettant un faisceau infrarouge
  invisible.** La diode de lecture CD est à 780 nm : elle équipe tout lecteur
  CD et la plupart des lecteurs combo DVD (la diode DVD, à 650 nm, est rouge
  visible). Aucun éblouissement, aucun réflexe de clignement, aucune
  sensation — et une puissance qui peut atteindre plusieurs centaines de mW
  pour une diode de graveur. C'est le composant le plus dangereux du
  programme. Le traiter avec plus de précaution
  que le laser de chantier, pas moins. Vérifier la présence du faisceau avec une
  carte de détection IR ou la caméra d'un téléphone, jamais à l'œil.
- **Les CD et DVD sont des réseaux de diffraction**, pas des miroirs : un
  faisceau incident ressort en **plusieurs ordres**, dans des directions
  inattendues, à pleine puissance. C'est le mode d'accident le plus probable de
  l'axe 3 et de l'axe 4. Cartographier tous les ordres sur un écran mat avant de
  travailler.
- **Faisceau horizontal, sous le niveau des yeux**, en étant assis comme debout.
  Retirer montre, bague et bracelet : le reflet spéculaire d'un métal poli
  renvoie un faisceau dans la pièce.
- Fond mat et sombre derrière le montage, pas de surface vitrée ni de miroir.

**Le télescope aggrave tout.** Un instrument qui élargit le faisceau à
l'émission **concentre** la lumière parasite à l'observation. Ne jamais regarder
vers le montage à travers une optique de collection.

---

## 3. Eau et électricité

L'aquarium est le cœur du programme et se trouvera près de capteurs, de moteurs
et d'un ordinateur.

- **Interrupteur différentiel 30 mA** sur toute la ligne alimentant la zone.
  Non négociable : c'est le seul dispositif qui protège une personne.
- **Pompes et moteurs en TBTS** (≤ 24 V) dès que possible. Une pompe 230 V
  immergée dans un bricolage n'a pas sa place ici.
- Alimentations et connexions **au-dessus du niveau de l'eau**, avec une boucle
  d'égouttage sur chaque câble pour que l'eau ruisselante tombe avant la prise.
- Un aquarium de 100 × 50 × 20 cm contient 100 litres, soit **100 kg**.
  Vérifier la charge du support et la planéité du sol : une rupture de cuve
  vide la totalité en quelques secondes, sur le matériel électrique.
- Prévoir l'évacuation avant de remplir, pas après.

---

## 4. Impression 3D et résines

- Imprimer en **ABS ou en résine** dégage des composés organiques volatils et
  des particules ultrafines : ventiler, ou utiliser du PLA/PETG.
- Les **résines SLA non polymérisées sont sensibilisantes cutanées** : gants
  nitrile, lunettes, et ne jamais rincer à l'évier — l'alcool isopropylique
  chargé de résine est un déchet chimique.
- Le plateau chauffant et la buse (200–250 °C) brûlent au contact.

---

## 5. Règle générale

Deux principes qui couvrent le reste :

1. **Ne jamais travailler seul sur la partie haute tension ou laser.** Une
   personne présente, sachant où est le disjoncteur.
2. **Un montage se désénergise avant d'être modifié.** La majorité des accidents
   surviennent lors d'un « petit réglage rapide » sur un montage sous tension.
