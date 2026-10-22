> **Priorité du 22/10/2026 : recherche dimensionnelle, CAO plus tard.** Voir `recherche_mesures_2026-10-22/RECHERCHE MESURES - LIRE EN PREMIER.txt`, le registre de cotes et les sources. Sept nouveaux PDF archivés, dont les plans architecturaux de gares réelles à Perisher. Rail de garage JC imprimable supplémentaire identifié sur Cults, compatibilité D-Line à vérifier. Les déclarations ci-dessous de recherche « épuisée », de cotes confirmant notre géométrie et de gare fonctionnelle sans modification ne sont pas des conclusions validées. Les pinces et leurs ressorts d'origine restent conservés.

> **Reprise Codex — 21/10/2026 :** état courant dans `AVANCEMENT_PROJET.txt` et `reprise_codex/LIRE EN PREMIER.txt`. Les anciennes mentions de modèle complet ou de zéro collision ne valident pas le débrayage. Les dix STL de Claude sont des prototypes. Un banc manuel réglable et un audit du balayage sont ajoutés ; leurs scripts Fusion n'ont pas encore été exécutés. La géométrie et les efforts de la vraie pince restent à mesurer. Les cotes tirées de modèles d'amateurs sont des références de conception, pas des plans constructeur.

# Gare débrayable pour télésiège Jägerndorfer 1:32 — dossier technique (v2, recherche approfondie)

Recherche du 20/10/2026. Objectif : modéliser dans Fusion 360 une gare **débrayable** compatible avec le siège
Jägerndorfer D-Line « Waidoffen » JC86541 (pince fonctionnelle, on ne modifie pas les sièges).

Légende : ✅ sourcé · 🗣️ retour de modéliste (forum) · 🧮 calculé par moi · 📏 À MESURER (introuvable en ligne)

---

## 0. En bref
- **Câble JC = 2 mm plastique** 🗣️ (et non 3 mm) · **entraxe des brins JC = 155 mm** 🗣️ (confirmé, 2 sources) ·
  **vitesse en ligne JC ≈ 15 cm/s** 🗣️ (= pile la vitesse réelle 5 m/s à l'échelle 1:32).
- La pince JC « à ressorts hélicoïdaux » (famille AK 2016 → D-Line 2019) a de **vrais galets de roulement mobiles** : c'est
  la meilleure base JC pour une gare débrayable 🗣️. Un modéliste a une gare débrayable qui marche avec ces pinces 🗣️.
- **Le point dur** (unanime chez les experts) : les ressorts sont durs (diamètre réaliste pour l'apparence) → il faut beaucoup
  de force sur le levier et une **forte pression des pneus** sur la plaque de friction, sinon la pince bascule ou bloque 🗣️.
  ➜ La gare doit **tenir la pince dans les 3 axes** (rails + contre-rails) et ouvrir avec une **came longue et douce**.
- Une gare D-Line réelle fait **12 à 36 m (pas de 2 m)**, un 6 places à bulle ≥ **26 m** et **9,9 m de large** ✅
  → **≈ 81 × 31 cm au 1:32**. La gare D-Line JC (fixe) fait 40 × 28 cm.

## 1. Les produits Jägerndorfer

| Élément | Réf. | Données |
|---|---|---|
| Siège 6 pl. D-Line « Waidoffen » Hochfügen | **JC86541** | ✅ 1:32, au catalogue depuis le 16/12/2019, 41,90 € |
| Même moule D-Line | JC86503 / 86504 / 86505 / 86506-x / 86507-x / 86542 | ✅ dimensions boîte/article : **12 × 6 × 11 cm** ; 🗣️ un 6 places JC fait « un peu plus de 100 mm » de large |
| Pince D-Line seule (2 pcs) | **JC51001** noir · JC51002 argent · JC51003 noir/rouge | ✅ 19,90 € (17,51 € chez Rainer Modellbahnen) |
| Gare D-Line JC (fixe, pinces qui tournent autour de la poulie) | JC84383 | ✅ aval ≈ 40 × 28 × 24 cm (Digitec : 39 × 24 × 21) ; amont 37 × 16,5 × 30 cm ; entretoise de poulie ≈ 40 mm ; vis 3×12 et 3×25 |
| Set « Ski Lift Luxe » (ton 1er lien) | JC83393 | ✅ gare UNI-G + retour + 6 pl. + cabine VIP + 8 m de câble (ligne ≤ 4 m) |
| Câble | JC50092 (10 m) / JC50090 (+ manchon) | 🗣️ **Ø 2 mm, plastique** ; remplaçants utilisés : PP 2 mm Kanirope, acier 2 mm 7×19, PP 3 mm soudé |
| Manchon + clé Allen | JC50091 | 🗣️ mieux : souder les bouts de câble PP à chaud (pas de nœud) |
| Poulie (Umlenkrad) | JC50093 · caoutchouc JC50082 | 🗣️ alésage central **Ø 10 mm** ; 📏 Ø extérieur |
| Moteur + vis sans fin / pignons | JC50081 / JC50083 | 🗣️ moteur fragile (300–500 h), pignons plastique qui s'usent, palier de poulie trop faible. Remplacements cités : **moto-réducteur 12 V / 21 tr/min à arbre sur roulement**, ou Bühler 24 V sous 12 V |
| Pylônes | JC50100 / JC50200 · galets JC50010 | 🗣️ joints toriques 10×1 dans les gorges des galets = passage des pinces plus doux et câble +1 mm plus haut |

### La pince JC D-Line : ce qu'on sait
- ✅ Mode d'emploi : « **appuyer le levier vers le bas**, poser sur le câble, relâcher ». Pince **monostable** (se referme seule).
  → En gare, le levier doit être **maintenu appuyé sur tout le trajet débrayé**, y compris la courbe (contrairement à la vraie D5000, bistable « à point mort »).
- ✅ Visible : corps en « bateau », **plaque de friction striée sur le dessus** (là où appuient les pneus), 2 ressorts hélicoïdaux sur tiges guides
  (« Federstöcke »), **galet blanc au bout du levier**, **galets de roulement blancs**.
- 🗣️ Histoire : 2016-17, nouvelle pince « AK » en zamak à ressorts hélicoïdaux (Omega IV/V) → 2019, pince D-Line vendue à part.
- 🗣️ PHB (2017, impliqué dans la conception des modèles JC) : pince **conçue pour le débrayage**, mais ressorts au diamètre réaliste
  → trop durs pour un vrai débrayage. Sur un rail incliné, la composante de la force du ressort au point d'ouverture fixe la
  **pression que les pneus doivent fournir**. Conçue pour **câble plastique 2 mm** (petites « dents » dans le canal).
- 🗣️ Petz (2017) : galets de gare **tous mobiles et bien placés → meilleure base qu'une pince DT** ; mais levier **trop dur** (use les
  paliers et les galets blancs). Mâchoire agrandissable pour 2–3 mm (3 mm max).
- 🗣️ Défauts de la 1ʳᵉ série D-Line (2024) : mâchoire trop étroite pour le câble JC (corrigé ensuite), 4 pinces sur 13 difficiles à
  poser, ressorts qui coincent (casse parfois), vis cruciformes trop serrées qui cassent au démontage. JC a ensuite **réduit la précharge**
  → tient moins bien, surtout sur câble 2 mm.
- 🗣️ Fränzchen (2022) : « depuis les nouvelles pinces JC, il y a même des galets pour le rail de roulement » ; sa gare débrayable
  Lego fonctionne mais demande beaucoup d'entretien.

## 2. Le vrai télésiège et les vraies gares D-Line

| Donnée réelle | Valeur | Source | 1:32 🧮 |
|---|---|---|---|
| Écartement en ligne 6-CLD (Waidoffen) | 6,4 m | ✅ lift-world, Doppelmayr | **200 mm** (JC : 155 mm) |
| Câble Waidoffen | Ø 45 mm (Fatzer) | ✅ | 1,4 mm (JC : 2 mm) |
| Vitesse en ligne | 5,0 m/s (D-Line ≤ 7 m/s) | ✅ | 156 mm/s |
| Vitesse en gare | 5 → **1 m/s** ; max réglementaire FR 1,3 m/s pour sièges ouverts | ✅ Eduscol, RM2 | 31 – 40 mm/s |
| Espacement des sièges Waidoffen | 🧮 ≈ 41,5 m (8,3 s) | ✅ 2600 p/h, 58 sièges | ≈ 1,30 m |
| Longueur de gare D-Line | **12 à 36 m par pas de 2 m** | ✅ Liftblog | 375 – 1125 mm |
| Longueur gare 6 places à bulle (6,4 m de voie) | **≥ 25,99 m** (ouverture des bulles + sortie des skieurs) | ✅ lettre Doppelmayr USA | **≈ 812 mm** |
| Largeur du bâtiment (voie 6,4 m) | **9,9 m** | ✅ idem | **≈ 309 mm** |
| Poulies D-Line 6 places (Pic Vert) | motrice 5,4 m · retour 6,3 m | ✅ | 169 / 197 mm |
| Exemple 8-CLD (Ramcharger 8) | gare 18 m, poulie ≈ 7,3 m, voie 7,7 m, 13 tr/min à 5,1 m/s | ✅ Liftblog | — |
| Masse à vide d'un DCD6 | 648 kg | ✅ Pic Vert | 🧮 ≈ 20 g « à l'échelle » (📏 peser le JC) |
| Sièges en gare (6 places) | ≤ 3 : 1 ralentisseur, 1 contour, 1 lanceur | ✅ remontees-mecaniques.net | — |
| Effort de serrage d'une pince classique | ≈ 5 kN | ✅ Eduscol | — |

### Séquence réelle en gare (Eduscol, remontees-mecaniques.net, Wikipedia DE)
1. **« Trompettes » d'entrée** : elles guident les pinces et les remettent à l'horizontale.
2. Les **rails reprennent le poids** du siège via les galets de la pince → le câble ne fait plus que tirer.
3. Les **pneus appuient sur le patin/peigne** (plaque de friction) → plus aucun effort sur le câble.
4. Le **rail-came appuie sur le galet du levier** → la mâchoire mobile s'ouvre (d'un seul côté).
5. Le câble **sort par le bas** de la mâchoire ouverte ; le rail décale la pince d'**≈ 10 mm** à l'ouverture maximale.
6. **Ralentisseur** : pneus de plus en plus lents (diamètres de poulies de courroie différents d'un pneu à l'autre) → contour
   (pneus ou chaîne, cadenceur +/- vite, pneu à embrayage-frein pour le garage) → **lanceur** : vitesse croissante linéairement
   jusqu'à la vitesse exacte du câble → embrayage : levier écrasé, câble guidé dans la mâchoire, levier relâché.
- **Entraînement des pneus** : le plus courant = **galets entraînés par le câble + courroies** (vitesse synchronisée d'office) ;
  sinon depuis la poulie, ou moteur électrique asservi. Règle ✅ : **au moins 2 pneus toujours en contact avec la plaque**.
- D-Line : convoyeur à pneus avec tendeurs de courroies, rail de roulement monté sur caoutchouc, guidage extérieur amorti ✅.

### La vraie pince D5000 et la gare D-Line vues en vidéo (Doppelmayr « Detachable grip-D » 2016 + film en gare)
- **Pince** : 2 ressorts hélicoïdaux parallèles en diagonale (« coil spring grip with slack point »), **levier terminé par un galet
  blanc** (galet de commande), **plaque de friction en peigne** sur le dessus de toute la pince, mâchoire extérieure prolongée par
  de **longues langues d'entrée** à l'avant et à l'arrière (passage des galets de ligne), **2 galets de roulement** avant/arrière
  sous la plaque, axe transversal (suspente) terminé par un **galet de guidage**. Câble jusqu'à 64 mm. La maquette JC reprend
  ces éléments (galet blanc en haut, galets blancs aux bouts d'axe, plaque striée, corps en « bateau »).
- **Gare** : la poutre de pneus est **au-dessus et côté intérieur**, pneus verticaux **quasi jointifs** (pas ≈ Ø du pneu),
  qui appuient sur la plaque de friction ; **rail de roulement profilé** sous la pince ; le galet du levier roule sur un rail
  côté extérieur ; rails cuivre en dessous pour le chauffage des sièges.
- Catalogue d'outillage Doppelmayr 2022 : « D-Line friction wheel 550 » (probablement galets de prise de mouvement Ø 550 mm
  → ≈ 17 mm au 1:32), jauge d'alignement de la ligne d'ouverture/fermeture spécifique D3000/D5000, testeur de tension de courroies
  des convoyeurs à pneus.
- Pneus de gare du marché : 4.00-8 / 4.80-8 (≈ 400 mm) → **≈ 12,5 mm au 1:32**, pas ≈ 13 mm 🧮 (estimation visuelle, non officielle).

## 3. Retours d'expérience de modélistes (Alpinforum, 2013-2025)
- **Projet de diplôme HTL Wels (2018)** : gare débrayable 1:32 complète, > 7000 pièces, impression 3D + 500 pièces usinées, freinage
  par chaînes avec rapports de pignons, 7 moteurs, 12 barrières optiques, 1 microcontrôleur par gare (fil « sunset »).
- **Gare Lego de Franz** (pinces JC) : pinces guidées sur rail blanc, pneus au-dessus ; 11 pneus à vitesse constante (zone
  d'embrayage), 8 pneus accélérateurs par paires de vitesse croissante ; plaques plastiques rugueuses collées sur la pince
  pour que 2 pneus touchent toujours ; rail d'embrayage noir-rouge qui appuie le levier ; 2 petites poulies guident le câble
  (la 1ʳᵉ très fine pour que la pince ouverte passe) ; le rail d'embrayage reste horizontal → pince ouverte sur quelques cm ;
  entraînement : 3 moteurs (dont un pris sur la poulie motrice par chaîne). Écartement : 137 mm.
- Échecs : **pneus trop espacés** (pas de contact continu), pneus trop lisses (prendre du caoutchouc tendre), pince qui **vrille**
  sous l'effort du ressort (→ galet stabilisateur en face), câble plié 4 fois en gare (en faire 2 maxi).
- Conseils : câble qui arrive **légèrement par-dessous**, pince poussée vers le haut puis relâchée ; garder le rail à hauteur
  constante et abaisser la poulie ; entraîner les pneus **rapides** (pas les lents) pour éviter jeu et vibrations ;
  calcul de rapport (thomas74) : **rapport = circonférence de gorge de la poulie de câble ÷ circonférence du pneu** ;
  galets miniatures 2 × 5 mm sous la plaque de friction pour éviter le basculement ; WD40 sur le rail.
- Petz (2018) : un passage de point de débrayage « mécanique » est très difficile au 1:32, la version Lego marche grâce à
  une **très forte pression des pneus**. Petz (2017) : prévoir ≥ 65 mm de dégagement entre siège et poteaux ; 155 mm d'entraxe
  est **très serré dans la boucle** de gare.
- Commerce : **Modellseilbahnen Doppelwihr** (DE) fait des pièces 1:32 imprimées 3D compatibles JC, dont un **« Schleifenbahnhof »**
  (rail de garage en boucle pour pinces JC, réf. 5016/5017, vis M2) → preuve qu'un rail de roulement marche avec les galets JC.

## 4. Calculs préliminaires de conception 🧮 (à valider avec les mesures)
- **Poulie / moteur** : poulie ≈ Ø 155 mm (= entraxe JC) → 487 mm/tour → 15 cm/s = **18,5 tr/min**. Le moto-réducteur
  **12 V / 21 tr/min** cité par Petz convient en prise directe (≈ 17 cm/s).
- **Pneus Ø 12 mm** : 150 mm/s → **239 tr/min** ; 35 mm/s en gare → **56 tr/min** ; rapport total ≈ 4,3. Avec 10 pneus dans le
  ralentisseur : ≈ **×1,18 par pas** (poulies de courroie de diamètres dégressifs, comme en vrai).
- **Longueur du ralentisseur** (et du lanceur) : décélération réelle ≈ 1 m/s² → à l'échelle 0,031 m/s² → **≈ 375 mm** ;
  version compacte (décélération ×2) ≈ 195 mm.
- **Pas des pneus** ≤ longueur de la plaque de friction / 2 (📏). Ex. : plaque de 25 mm → pas ≤ 12 mm → pneus Ø ≤ 11 mm,
  soit ~17 à 31 pneus par zone et par côté.
- **Effort de poussée à l'ouverture** ≈ force du levier × tan(pente de la came) + frottement. Ex. : 5 N sur le levier et came
  à 15° → ≈ 1,3 N à fournir par les pneus → avec μ ≈ 0,8, ≈ 1,7 N d'appui réparti sur 2 pneus → **pneus montés sur ressorts réglables**.
- **Astuce** : hors câble, le rail des sièges peut s'écarter de 155 mm à **200 mm (vraie échelle)** dans la boucle, ce qui règle le
  problème de dégagement signalé par Petz, pendant que le câble reste à 155 mm sur la poulie.

## 5. Architecture proposée (à discuter)
Modules imprimés 3D, un seul moteur sur la poulie, pneus entraînés par courroies/joints toriques depuis la poulie ou par
galets sur le câble (synchro mécanique, comme en vrai) :
1. Trompette d'entrée + batterie de galets (câble légèrement remonté vers la pince).
2. Prise en charge : rails sous les galets de la pince + contre-rail anti-basculement + 2–3 pneus à vitesse câble.
3. Came d'ouverture longue (pente douce) sur le galet du levier ; déviation du câble vers le bas.
4. Ralentisseur, quai, **rail de maintien du levier continu**, contour (pneus en courbe ou chaîne), lanceur.
5. Came de fermeture (relâche progressive), câble guidé dans la mâchoire, sortie.
6. Option garage : rail en boucle type Doppelwihr.

## 6. MESURES À PRENDRE (pied à coulisse + balance) — indispensables pour Fusion
Origine : **axe du câble**, pince fermée. X = sens de marche, Y = extérieur, Z = haut. Idéal : **photos de face, de côté et de
dessus sur papier millimétré** en plus des cotes.

**Pince (JC86541 ou JC51001)**
1. Ø réel du câble JC et Ø dans la mâchoire fermée ; ouverture maxi, levier à fond.
2. Galet du levier : Ø, largeur, position (X, Y, Z) relâché **et** à fond → course.
3. Force pour ouvrir (levier sur une balance de cuisine, en grammes) au début et à fond.
4. Galets de roulement : nombre, Ø, largeur, entraxe, position Z du bas, axes (fixes ou tournants ?).
5. Plaque de friction : longueur, largeur, hauteur Z du dessus, pas des stries.
6. Sens de sortie du câble à l'ouverture (bas ? côté ?) et de quel côté est la mâchoire mobile.
7. Encombrement de la suspente sous la pince (largeur, position) pour que les rails ne la touchent pas.
8. Hauteur câble → bas du siège, largeur hors tout du siège, masse du siège (g).

**Ligne / gares**
9. Ø extérieur de la poulie JC et hauteur du câble au-dessus de la plaque de la gare UNI-G (JC83393).
10. Hauteur du câble aux pylônes et entraxe réel mesuré (vérifier les 155 mm).

## 7. Fichiers de référence (dossier `references\`)
- ✅ Catalogue Doppelwihr décembre 2024 (15 Mo) : JC = **voie 155 mm** (3ᵉ confirmation) ; rails de garage « ausgelegt für
  JC Klemme zur Auflage auf Schiene » (5009 : 408 × 128 × 149 mm, 12 véhicules ; 5016/5017 avec sortie ; 5018 : 501 × 367 mm,
  17 véhicules) ; pylônes sur mesure ≤ 500 mm en 155 mm ; câble PP 3 mm soudé pour JC (avec leurs galets) ; leurs propres
  sièges utilisent du PP 2 mm.
- ✅ Catalogue hiver Jägerndorfer 2026 (13 Mo) : gares Platin 39 × 24 × 21 cm, **1 099 g** ; pylône JC50100 **450 mm** ;
  nouveaux sièges D-Line « Palinkopf » (JC86500-x) et « Gampenbahn » (JC86501-x) ; JC51001/51002 toujours au catalogue.
- ✅ Thingiverse 7292017 « rolna4 » (téléchargé à la main par l'utilisateur) : **galet de déviation latéral de l'entrée
  d'une gare UNI-G JC** (photos de la gare vue de dessous). STP en mm : **Ø 16,0 × 7,3 mm**, gorge torique Ø moyen 11,8 mm
  de **rayon 1,4 mm** → fond de gorge **Ø 9,0 mm** (axe d'un câble Ø 2 à r = 5,5 mm), alésage **Ø 3,2 mm** (chanfrein Ø 4,5).
  Importé dans le modèle Fusion comme pièce de référence.
- ✅ Thingiverse 5229610 (pylône compatible JC, fichier Blender `Mast_JC_21.7.blend` en mm) : galets **Ø 16,3 × 7,1 mm**
  centrés à **x ≈ ±77 mm → voie 155 mm** (4ᵉ confirmation), pas des galets dans un balancier ≈ **13,5 mm**, balancier
  de 4 galets ≈ 41,5 mm, chapeau de pylône 164,8 mm de large, galets à z ≈ 180,6 mm (axe) → câble à ≈ 186 mm du sol
  sur le pylône « normal » imprimé ; socle 124 × 124 mm. (JC50100 d'origine : 450 mm.)
- ✅ **MakerWorld 2883608** siège 6 places D-Line « Spittal » (domi_56, SDFL-C), téléchargé le 21/10 avec accord :
  `makerworld_2883608_siege_Spittal\` → `6er_Sessel_D_Line_debrayable.3mf` (pour vraie pince JC) et
  `6er_Sessel_D_Line_fixe.3mf` (pince imprimée) ; STL extraits dans `extrait_debrayable\` et `extrait_fixe\`
  (outil `mf3_extract.py`, coupes numériques). Pièces : assise 97 × 30 × 17, garde-corps 107 × 23,5 × 37,8,
  **suspente + cadre `Gehaenge_k` 115 × 23 × 109,9 mm**.
  - **Attache de la pince JC** (sommet de `Gehaenge_k`) : tube Ø 6 de 12,2 mm de long, couché en travers du câble
    (= axe de balancement longitudinal du siège) ; perçage **Ø 4,2 aux deux bouts, Ø 2,4 au milieu** sur 4,2 mm
    → téton Ø 4 de la pince d'un côté, **vis M2 × 12-14** de l'autre. Axe à **106,9 mm au-dessus du bas** de la
    pièce, décalé de **13,6 à 25,8 mm** sur le côté par rapport au milieu du siège. Bras de suspente 6 mm d'épaisseur.
  - Version fixe : `Gehaenge_fix` 115 × 21 × 110,3 (trous Ø 3 au sommet) + `Klemme_fix` **20 × 8,3 × 4,1 mm**,
    cavalier en U renversé (ouverture ~2,5 mm) posé sur le câble.
  - 📏 Reste à mesurer sur la pince JC : position du téton par rapport au câble (fiche F10-F11) → donnera la hauteur
    câble → siège exacte (recalage de `H_cable` / `Siege_H`).
- ✅ **Dessins déposés EUIPO 001945759-0001 à 0020** (Jägerndorfer Ges.m.b.H, 10/11/2011, expirés 2016-2017,
  Locarno 21.01) : photos de produits 2011 (télécabines 8 pl. à l'ancienne pince, sièges 4 et 6 pl., pylône, manchon
  de câble, boîte du set) ; aucune cote. Titulaire 481251 : 20 dessins, 0 marque, aucun dépôt plus récent.
- Doublon : `Downloads\e726e5dd9c~Winterkatalog _2026.pdf` = même catalogue 2026 (enregistré via la boîte de dialogue).

## 7 bis. CAO commencée (20/10)
- Script `JC_Gare_Debrayable` (dossier Scripts Fusion) : nouveau document paramétrique, 23 paramètres utilisateur, plan
  d'implantation à l'échelle (bâtiment 812 × 309 mm, voie 200 mm, poulie 200 mm, zones entrée 94 / ralentisseur 375 /
  zone lente / contour / embarquement 150 / lanceur 375 / embrayage 94 mm), élévation (câble 125 mm, toit 200 mm),
  volumes gabarits (dalle, poulie, câble Ø 2, 3 enveloppes de sièges).
- ~~Question ouverte : voie 200 mm vs 155 mm~~ → **tranché (v2)** : ligne au standard JC 155 mm, `Voie_gare` paramétrable.
- **v2** : une seule gare débrayable (aval) = **motrice + tension + garage** ; gare retour JC en haut. Garage 8 places en U
  à l'arrière (comme Waidoffen : rez-de-chaussée, arrière), aiguillages à 135° et 225° sur le contour. Gare 812 mm + garage
  501 mm = **1 312 mm**. 36 pneus par côté. Jeu entre sièges face à face 35 mm, siège → mur 17 mm.
- **Étapes 2 et 3 (20/10)** : poulie motrice Ø 155 (2 demi-coques sans support, joint torique 3 mm), moyeu hexagonal
  à alésage D6, moteur JGB37-520 (gabarit), chariot de tension sur 2 tiges Ø 4, poutre centrale alu 15×15 à 181 mm,
  3 poteaux Ø 16, 2 brides, toit R1. Le câble descend de 10 mm vers la poulie. 0 interférence (32 corps).
  Corrigé : mur arrière à 152,5 mm de l'axe (les sièges balaient 137,5 mm au contour).
  Script maître `JC_Gare_Construire`. STL + notice/achats dans `STL\`.
- Règle de conception retenue : **poulie, moteur et chariot de tension suspendus par le haut** (au contour, l'intérieur
  des sièges passe à ~17 mm de l'axe, sous la poulie). Moteur 12 V ~21 tr/min → ≈ 17 cm/s avec une poulie Ø 155.

## 7 ter. Modèles 3D existants (recherche du 20/10)
Aucun modèle publié de **gare débrayable** pour sièges JC, ni de **CAO de la pince JC D-Line** → mesures toujours nécessaires.
Modèles utiles trouvés :
- **MakerWorld 2883608** « Doppelmayr 6er D-Line Sessel für JC-Seilbahnen » (Modellseilbahnen Spittal / domi_56, licence SDFL-C,
  gratuit) : siège 6 places D-Line imprimable qui reçoit une **vraie pince JC** (D-Line ou normale, vis M2x12-14 + 2 M2x6 + 2 M2x8),
  profil d'impression « débrayable » ; l'auteur prépare un système complet (pylône + automatisme), pas fini. → flotte de sièges
  pas chère (siège imprimé + pince JC51001). Instagram @modellseilbahnen_spittal.
- **MakerWorld 1461885** « Roll-on batteries for Jägerndorfer 1:32 » (Mike) et **Printables 782640** « Modellseilbahn 6er
  Rollenbatterie V1.0 » (modellskigebiet Kelmental, 4/6/8 galets dont maintien) → batteries pour le portique d'entrée.
- **Printables 1274550** « 10 MGD Seilbahn Klemme » (Lötgott) : pince débrayable imprimable pour câble 2 mm (plan B si les
  pinces JC sont trop dures). **Thingiverse 6798061** : pince débrayable compatible LEGO (câble 3 mm, élastique) = principe.
- Thingiverse Domi_56 : plaque de base de la gare compacte JC (5676591), échelles pour pylônes JC (5676698).
- Décoratifs seulement : MakerWorld 1620092 « D-Line gondola terminal » (réduit, sans mécanisme), CGTrader/TurboSquid/3D Warehouse
  (gares et sièges D-Line en rendu 3ds Max/OBJ/SKP), Prusa « Station for model cable car (LGB) » (gare fixe 1:32 KMS).
- Vidéos H0 : « Erster kuppelbarer Sessel auf der JC-Umlaufbahn in 1:87 », « JC-Umlaufbahn in 1:87, kuppelbar umgebaut ».
- 2ᵉ passe (21/10) :
  - **3D Warehouse** « Doppelmayr 6-CLD Detachable chairlift bottom/top station » (Thomas Stendys, « highly detailed and real
    dimensions », type UNI-G, SketchUp importable dans Fusion) → meilleure référence trouvée pour l'intérieur d'une vraie gare
    débrayable (rails, poutres de pneus, hauteurs). **Téléchargé le 21/10** (accord de l'utilisateur, GLB sans compte)
    → cotes relevées au § 7 quater.
  - **CadCrowd** « Detachable Quad-Chairlift Grip Mechanism » (SolidWorks, projet d'école) ; **Thingiverse 4670705** pinces POMA
    TB-50/TB-41 (Joh76) → références de mécanisme réel.
  - Projets francophones : télécabine débrayable imprimée de CécéAlpes (PLA + profilés alu 10×10 + Arduino) et d'abludo
    (remontees-mecaniques.net, sujets 29086 et 33278 ; conseil : balanciers compacts sinon la pince frotte) ; Techlug (LEGO).
  - Alpinforum « Leo's Seilbahnmodelle » : Petz → **les suspentes des sièges JC sont trop courtes** (mauvais plan envoyé au
    mouliste) et **les 6 places touchent les cadres de pylônes** avec l'entraxe JC étroit ; galets à gorge plus plate = passage
    « butterweich » des pinces ; axes de galets : vis inox M2, alésage galet 2 mm, trous de balancier ~1,6 mm.
  - TheTimmy376 (Alpinforum) : 3S débrayable imprimé, transfert par pneus LEGO, 25 cm/s, profilés alu industriels.
  - 3ᵉ passe (21/10, mots-clés « jc chairlift », « jd chairlift », « jaegerndorfer », « JägernDorfer ») : siège Spittal
    confirmé par l'utilisateur (bonne marque). Photos de la fiche : vraie pince JC D-Line (corps noir, ressorts rouges, galet
    blanc en haut) montée sur la suspente imprimée, au passage de la colonne d'entrée d'une gare D-Line JC. Vue 3D : plaque 1
    assise, 2 et 4 repose-pieds/garde-corps, 3 suspente + cadre (la pince elle-même n'est PAS dans le fichier, seule son
    attache sur la suspente). Cults3D : « 6-seater D-Line armchair (without clamp) » payant (~7 $, page bloquée aux robots) et
    gondole 1:32 « Schwarzwandbahn » compatible JC. MakerWorld : trépied de canon à neige 1:32 (3412460), canon TechnoAlpin M18
    1:32 (3434693). Jaegerndorfer USA « Customization » = logos de stations seulement (Sales@jaegerndorfer-usa.com).
    Toujours aucune gare débrayable ni CAO de pince JC publiée.
  - Rien de nouveau sur Thangs, Sketchfab, MyMiniFactory, GitHub. Yeggi, Cults3D, Printables et le forum
    remontees-mecaniques.net bloquent les robots (lus via moteurs de recherche).
  - 4ᵉ passe (21/10) : siège Spittal téléchargé et mesuré (voir § 7) ; registre EUIPO (dessins 2011 sans intérêt
    pour la pince D-Line) ; fiche officielle JC51001 sans cotes ; profil MakerWorld domi_56 : pas de pièces de gare
    publiées. **La recherche en ligne est épuisée : seules les mesures de la fiche peuvent débloquer la suite.**

## 7 ter bis. 5ᵉ passe dans le navigateur (21/10) — gares débrayables 1:32 qui marchent
- 🗣️ **msgSteinachkogel** (Alpinforum « Kuppelbare Modellseilbahn » 70794, mars 2025 ; YouTube @msgsteinachkogel ;
  Instagram @msg_steinachkogel « 6-CLD Steinachkogelbahn im Bau ») : télésiège 1:32 débrayable **avec les pinces JC D-Line**
  (« Umbau auf D-Line Klemmen », sept. 2024). Ce qu'il a appris :
  - le plus dur a été de trouver un **rail de seulement 0,6 mm de profondeur** pour la pince D-Line ;
  - il a remplacé les 2 ressorts d'origine par **un seul ressort très léger** : assez de serrage pour un siège, et des efforts
    bien plus faibles au débrayage (= la réponse au « point dur » des ressorts trop durs) ;
  - pour ne pas modifier la pince, pas des pneus de **3 plots LEGO = 24 mm** (40 mm avec les anciennes pinces JC à garniture
    agrandie) ; convoyeur à pneus entraîné par une chaîne de centaines de maillons ; pièces dessinées sous Onshape et imprimées ;
  - 1ʳᵉ version : au débrayage, ce n'est pas le câble qui s'écarte mais **le rail qui part vers l'extérieur de 8 mm** ; le contour
    est 16 mm plus large que l'entraxe du câble ; tout tenait sous le toit d'une gare JC. Ancienne étape : « pinces à gravité »
    (mâchoire basse de la pince JC sciée, demi-tube collé), idée de Crapoulliot42.
- 🗣️ **Olang Valdaora** (Johannes, Alpinforum « 6EUB OLANG I+II - Kuppelbare Talstation » 50507, 2014-2025 ; YouTube) :
  télécabine 1:32 débrayable complète qui tourne (10 m, 1,70 m de dénivelé) + une 2ᵉ ligne avec une **pince à ressorts
  hélicoïdaux et point mort** faite maison (« Modellseilbahn 1:32 D-Line Klemme Testlauf », 2021, 120 000 vues) — « débrayage
  très doux avec des rails bien réglés ». Solutions :
  - pneus imprimés d'une pièce avec leurs poulies, reliés **pneu à pneu par des joints toriques** (Ø libre ≈ 12 mm, très
    élastiques) : pas cher, compact, accélération douce ; mais la vitesse tombe de moitié après ~10 pneus → moteurs
    d'appoint (6 dans la gare) ; un réducteur chinois a cassé sous la tension des joints ;
  - les pneus appuient sur une **mousse élastique** collée sur la pince ; galets de pince sur micro-roulements ;
  - came d'ouverture = rampe imprimée réglable en hauteur par vis M3 + écrous ;
  - galets de ligne = roulements à gorge Ø 13 mm + joint torique rainuré ;
  - **régulation d'espacement** : roue codeuse IR sur la poulie + 2 micro-rupteurs + Arduino (Elegoo UNO) qui arrête un pneu tant
    que la distance n'est pas atteinte — fonctionne ;
  - **garage** : chaîne imprimée qui coulisse dans un rail et pousse les véhicules.
- 🗣️ **MB 99** (Maximilian Breitfuss, YouTube) : télécabine Doppelmayr 1:32 débrayable avec gares, cabines et sièges JC
  modifiés : 12 moteurs 9 V, 65 roues de convoyeur, 142 engrenages, 4,2 m.
- ✅ **StarRail AG** (Suisse, starrail.ch) : batteries de galets SR 026/027 (25 CHF) à coller sur le toit d'une gare JC 1:32 pour
  guider le câble à l'entrée et à la sortie (les véhicules D-Line lourds « sautent » sur la poulie JC).
- ✅ Alpivio EVO 10 (Avantive, 2026) : cabines Leitner 1:32, pince de type H0 (seilbahnshop.com).
- Thingiverse (lisible dans le navigateur) : rien de neuf pour JC. remontees-mecaniques.net (lisible) : rien de JC débrayable.
  **Printables, Cults3D et Yeggi** restent bloqués par leur vérification anti-robot (à passer par l'utilisateur s'il le veut).

## 7 quater. Gare 6-CLD réelle (3D Warehouse) — cotes relevées (21/10)
Dossier `references\3dwarehouse_6CLD_gare_aval\` : GLB complet (36,7 Mo), **STL de la machinerie au 1:32 dans le repère de
notre gare** (X vers la ligne, 0 = centre du contour, Z = 0 au quai ; Fusion : Insérer un maillage, mm, sans centrer),
8 vues à l'échelle (`rendus\`), `LISEZMOI`. Modèle d'amateur (T. Stendys 2015, type UNI-G), cohérent avec le réel.

| Cote | Réel | 1:32 🧮 | Notre modèle |
|---|---|---|---|
| Câble | Ø 0,05 m | 1,6 mm | JC 2 mm |
| Voie à l'entrée | 5,57 m | 174 mm | JC 155 mm |
| Câble au-dessus du quai | 3,35 m | 105 mm | `H_cable` 125 (siège JC plus haut) |
| Bas du siège au-dessus du quai | 0,46 m | 14 mm | 125 − 110 = **15 mm ✓** |
| Pneus | Ø 0,41 m (16"), pas 0,45 m | **Ø 12,8, pas 14,1** | `D_pneu` 12,5 ✓, `Pas_pneu` 13 (gardé : plaque JC inconnue) |
| Position des pneus | pile au-dessus du câble, bas à +0,086 m | +2,7 mm | à caler sur la plaque JC (D3) |
| Nombre de pneus | 24 par côté en droite (10,35 m) + 15 au contour | 323 mm | 36 par côté |
| Rail des galets de pince | C ouvert vers le câble, 0,43–0,55 m à l'extérieur, ±0,15 m | 13–17 mm, ±4,7 mm | = notre rail + contre-rail ✓ |
| Entrée sans pneus (pince encore sur le câble) | 4,2 m après les trompettes | 131 mm | `L_entree` 94 |
| Câble au débrayage | −0,48 m vers l'intérieur, −0,26 m en hauteur | 15 / 8 mm | `Delta_poulie` 10 mm vers le bas ✓ |
| Poulie | Ø 4,4–4,6 m, centre 1,25 m côté ligne / contour | ≈ 140 mm, +39 mm | Ø 155 concentrique (plus simple) |
| Contour des pinces | rayon 3,03 m ; sièges à 0,88 m du centre | 95 / 27 mm | 77,5 / 17 mm |
| Siège | 3,62 m de large, centre 0,34 m à l'intérieur de la pince | 113 / 11 mm | `Siege_L` 120 |
| Bâtiment | 19,6 × 8,0 m, toit en arc, faîte +2,1 m sur le câble | 612 × 251, +66 mm | 812 × 309 (Waidoffen D-Line), toit +75 mm |
| Garage | voies parallèles 17 m, entraxe 4,4 m, 1 aiguillage au sommet du contour | 530 / 137 mm | U, 2 aiguillages |

Conclusions : nos choix sont confirmés (pneus, hauteur du siège, câble abaissé, rail tenu en haut et en bas). Idée à garder
pour plus tard : écarter aussi le câble vers l'intérieur (15 mm) au débrayage, ce qui dégage la mâchoire plus franchement.

## 8. Existant sur ce PC
- Script Fusion `JC_Gabarit_Gare` (24/08/2026) : entraxe 155 mm ✅ confirmé ; **câble 3 mm ❌ → 2 mm** ; pas des sièges 1300 mm ✅ ;
  gare 390 × 240 × 210 mm = cotes Digitec de la gare D-Line JC (fixe), à remplacer par la longueur d'une gare débrayable.

## 9. Sources
- Jägerndorfer : fiche JC83393 (jaegern-dorfer.com) ; catalogue Gondeln & Sesseln, pièces détachées, fiche JC84383 et notice
  « Umlaufstation Set D-Line » (jaegerndorfer.at) ; jc-vertrieb.com (JC86541, JC51001, JC50081, JC50092, JC50093)
- Amazon.de JC86505 · Digitec · Rainer Modellbahnen (modellbahn.at) JC51001
- Alpinforum : « Jägerndorfer Modellseilbahnen » p. 70-80 ; « Kuppelbare Modellgondelbahn » ; « Kuppelbare Modellseilbahn aus Lego »
  p. 1-2 ; « Kuppelbare Gondelbahn (EUB) » p. 1-2 ; « Kuppelbare Sesselbahn » ; « Klemme für kuppelbare Modellgondelbahn » ;
  « Kuppelbare Modellseilbahn 1:32 von sunset » ; « Kuppelbare Modellbahn kaufen/bauen? »
- tips.at (HTL Wels 2018) · Modellseilbahnen Doppelwihr (notice MA 5016) · Thingiverse 5229610 / 7292017
- lift-world.info (Waidoffen) · Doppelmayr médiacentre et brochure D-Line · Liftblog (D-Line, Ramcharger 8) · lettre Doppelmayr USA
  (Routt County) · forum.stationsdeski.net et remontees-mecaniques.net (TSD6 Pic Vert, dossiers « pince débrayable » et
  « circulation en gare ») · Eduscol STI « Remontées mécaniques : présentation, technologie et construction »
- Wikipedia DE « Stationsförderer », « Kuppelbare Klemme » · STRMTG · ropewaygrips.ch
- YouTube Doppelmayr Group « D-Line – Detachable grip-D » (2016) · « Doppelmayr D-Line D5000 Grip Seat Heating Detach » ·
  Franz « Kuppelbare Lego Modellseilbahn » · Doppelmayr Werkzeugkatalog 2022 · seilbahnshop.com (pièces JC 1:32)
