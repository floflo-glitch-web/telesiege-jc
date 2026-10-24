# Gare débrayable Jägerndorfer 1:32 avec garage

Projet de conception d'une gare **débrayable** pour une maquette de télésiège
Jägerndorfer (JC) au 1:32, en gardant les sièges et leurs pinces d'origine.
Siège de référence : D-Line « Waidoffen » JC86541.

## Où en est le projet (24 octobre 2026)

- **Rail de la pince : validé en ligne droite.** Le tronçon d'essai v5 est
  rentré parfaitement sur la vraie pince : deux petits galets en tandem dans
  une gorge, gros galet à plat dans un profil en C. La v6, sans renfort sous
  le contre-rail, est la version courante.
- **Rail en virage : v2 à essayer.** La v1 frottait au bout d'axe du gros
  galet ; la paroi du C est reculée de 0,6 mm dans la courbe.
- **Cotes de la pince :** une mesure réelle (axe des galets, 28 mm bout à
  bout) et des cotes estimées sur deux photos à cette échelle.
- **Encore inconnu :** la came d'ouverture (course et effort du levier,
  sortie du câble), les longueurs le long du câble (bloc strié, écart des
  galets) et le siège suspendu. Liste à jour :
  [mesures/MESURES_RESTANTES.txt](mesures/MESURES_RESTANTES.txt).
- **Pas encore validé :** came, pneus, entraînement, aiguillages et garage.
  Les STL de la gare dans `cao/STL_gare/` sont des prototypes. Aucun fichier
  Fusion `.f3d` final n'existe encore.

Le détail, essai par essai, est dans [AVANCEMENT.txt](AVANCEMENT.txt).

## Organisation du dépôt

| Dossier | Contenu |
| --- | --- |
| [`mesures/`](mesures) | Ce qu'on sait de la pince et du siège, et ce qu'il reste à mesurer |
| [`mesures/photos/`](mesures/photos) | Photos de la pince, cotes estimées à l'échelle, coupe 2D |
| [`essais/rail/`](essais/rail) | **Travail en cours** : rails d'essai imprimables (droit v6, virage v2), générateurs et notices |
| [`essais/banc/`](essais/banc) | Banc manuel réglable (prototype non essayé), son générateur et son script Fusion |
| [`cao/`](cao) | CAO de la gare : notice, paramètres, script de reconstruction Fusion |
| [`cao/scripts_gare/`](cao/scripts_gare) | Scripts Fusion d'origine de la gare (historique) |
| [`cao/STL_gare/`](cao/STL_gare) | Dix STL prototypes de la gare, notice d'impression et achats |
| [`cao/rapports/`](cao/rapports) | Audit des STL et du balayage des sièges |
| [`cao/apercus/`](cao/apercus) | Vues des prototypes |
| [`recherche/`](recherche) | Dossier technique, registre des cotes, sources, documents étudiés |
| [`references/`](references) | Liens vers les modèles et catalogues de tiers |
| [`outils/`](outils) | Audit hors Fusion et sauvegarde complète en ZIP |

## Par où commencer

1. [mesures/MESURES_RESTANTES.txt](mesures/MESURES_RESTANTES.txt) : les
   prochaines mesures, par priorité, et la méthode photo qui marche.
2. [essais/rail/NOTICE_VIRAGE.txt](essais/rail/NOTICE_VIRAGE.txt) : le
   prochain essai à imprimer, avec les questions à vérifier.
3. [mesures/photos/COTES_SUR_PHOTO.txt](mesures/photos/COTES_SUR_PHOTO.txt) :
   toutes les cotes de la pince connues à ce jour.
4. [recherche/LIRE_EN_PREMIER.txt](recherche/LIRE_EN_PREMIER.txt) et
   [recherche/REGISTRE_COTES.csv](recherche/REGISTRE_COTES.csv) : la recherche
   dimensionnelle du 22/10 (110 entrées, inconnues signalées).
5. [recherche/DOSSIER_TECHNIQUE.md](recherche/DOSSIER_TECHNIQUE.md) : le
   dossier historique (recherches et choix depuis le 20/10). Les précisions
   plus récentes priment sur ses anciennes mentions de validation.

## Décisions de conception

Gare aval débrayable avec garage de 8 places, ligne au standard JC (voie de
155 mm), sièges et pinces JC d'origine conservés, ressorts compris. La voie
réelle d'un 6-CLD D-Line (6,4 m) ferait 200 mm au 1:32 : 155 mm est un
compromis de compatibilité avec les pylônes et la gare retour JC.

## Imprimer et régénérer les essais

Les STL sont prêts dans `essais/rail/` ; les notices donnent l'impression et
les points à vérifier. Les cotes sont en tête des générateurs. Après une
modification, depuis la racine du dépôt :

```text
python essais/rail/generer_rail_essai.py
python essais/rail/generer_rail_virage.py
python essais/banc/generer_banc.py
python outils/audit_projet.py
```

Dépendances : `pip install -r requirements.txt` (numpy, shapely, matplotlib,
trimesh, manifold3d). Ces outils ne lancent pas Fusion.

## Utilisation dans Fusion

Voir [cao/LIRE_EN_PREMIER.txt](cao/LIRE_EN_PREMIER.txt). `cao/JC_Reconstruire`
reconstruit l'implantation de la gare dans un document neuf à partir de
`cao/parametres_projet.json` et des scripts de `cao/scripts_gare/` ; ses
sorties vont dans `cao/constructions/`, non suivi par Git.
`essais/banc/JC_Banc_Essai` crée le banc. Ces deux scripts sont préparés mais
n'ont pas encore été exécutés dans Fusion. Les scripts de `cao/scripts_gare/`
gardent des chemins de la première installation (AppData, Téléchargements) :
les lancer via `JC_Reconstruire`, pas un par un.

## Fichiers gardés seulement en local

Les modèles, catalogues et PDF de tiers ne sont pas recopiés dans le dépôt :
[`references/README.md`](references/README.md) et
[`recherche/documents/`](recherche/documents) donnent leurs liens. Dans le
dossier local, ils restent aux mêmes emplacements, ignorés par Git
(voir `.gitignore`). `python outils/preparer_archives.py` crée à côté du
dossier une sauvegarde ZIP complète, références comprises.

## Attribution

Projet personnel développé avec l'aide de Claude et de Codex. Jägerndorfer
et Doppelmayr désignent les produits étudiés ; ce projet n'est pas un produit
officiel de ces fabricants. Les références externes restent celles de leurs
auteurs et conservent leurs conditions d'utilisation propres. Aucune licence
globale n'a été attribuée à ce projet.
