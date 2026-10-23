# Gare débrayable Jägerndorfer 1:32 avec garage

Projet de recherche et de conception d'une gare débrayable pour une maquette
Jägerndorfer, avec conservation des sièges et de leurs pinces fonctionnelles
d'origine. Siège de référence : D-Line « Waidoffen » JC86541.

**État au 22 octobre 2026 : recherche des mesures avant la CAO définitive.**
Les rails, la came, les pneus et le garage ne sont pas validés en fonctionnement.
Les STL existants sont des prototypes. Aucun fichier Fusion `.f3d` final validé
n'est actuellement disponible dans le projet.

## Commencer ici

1. [Rapport de recherche dimensionnelle](recherche_mesures_2026-10-22/RECHERCHE%20MESURES%20-%20LIRE%20EN%20PREMIER.txt).
2. [Registre des cotes](recherche_mesures_2026-10-22/REGISTRE_COTES.csv) :
   110 entrées, dont 28 mesures ou observations inconnues explicitement signalées.
3. [Sources et pistes](recherche_mesures_2026-10-22/SOURCES_ET_PISTES.txt).
4. [Mesures qui manquent encore](MESURES%20RESTANTES.txt) (à jour) et la
   [fiche détaillée d'origine](FICHE%20MESURES%20-%20pince%20et%20siege%20JC.txt).
5. [Cotes de la pince estimées sur photo](mesures_photo_2026-10-22/MESURES%20PHOTO%20-%20pince%20JC.txt) :
   échelle donnée par l'axe des galets mesuré à 28 mm.
6. [Avancement courant](AVANCEMENT_PROJET.txt).

Le [dossier historique](DOSSIER_GARE_DEBRAYABLE_JC.md) conserve les recherches et
choix antérieurs. Les précisions du rapport du 22 octobre priment sur les
anciennes mentions de validation ou de recherche terminée.

## Contenu du projet

| Dossier | Contenu |
| --- | --- |
| `recherche_mesures_2026-10-22/` | Recherche, cotes, sources, relevés de fichiers 3D |
| `mesures_photo_2026-10-22/` | Photo de la pince, mesure de 28 mm et cotes estimées à l'échelle |
| `essai_rail_2026-10-22/` | Petit tronçon de rail imprimable pour vérifier ces cotes sur la vraie pince |
| `STL/` | Dix prototypes historiques de la gare et leurs documents |
| `apercus/` | Vues des prototypes |
| `reprise_codex/rapports/` | Audit des STL et du balayage des sièges |
| `reprise_codex/banc_essai/` | Banc manuel réglable, trois STL et notice |
| `reprise_codex/JC_Banc_Essai/` | Script Fusion préparé pour le banc |
| `reprise_codex/JC_Reconstruire/` | Script Fusion préparé pour reconstruire l'implantation |
| `reprise_codex/sources_claude/` | Sources historiques, gabarit et ancien script de pince |
| `references/` | Liens et, dans l'archive complète, téléchargements externes |
| `archives_locales/` | Copie du suivi du Bureau, dans l'archive complète |
| `outils/` | Préparation reproductible des deux archives |

Les sources historiques ont été copiées depuis Fusion et Téléchargements.
Le dossier du projet peut ainsi être conservé sans dépendre d'une autre copie
des scripts située dans AppData. Certains scripts historiques contiennent
encore des chemins locaux : utiliser les scripts de reprise comme points
d'entrée, et non le constructeur historique lancé isolément.

## Deux archives, deux usages

- **`Gare-JC-COMPLET-2026-10-22.zip`** : sauvegarde de tous les fichiers du dossier,
  y compris PDF, modèles téléchargés, images de référence et historique local.
- **`Gare-JC-GITHUB-2026-10-22.zip`** : sources, documentation de recherche,
  relevés, prototypes propres au projet et liens vers les références.
  Les modèles, PDF et images externes sont laissés dans la sauvegarde complète.

Les deux ZIP sont créés à côté du dossier du projet, dans Téléchargements.
Chaque archive contient un inventaire avec les empreintes SHA-256 des fichiers.
Un rapport extérieur aux archives permet également de vérifier leur intégrité.

La version GitHub conserve la liste des références nécessaires : voir
[`references/README.md`](references/README.md). Un téléchargement externe
manquant n'est pas remplacé par une mesure inventée.

## Mettre le projet sur GitHub

Décompresser **la version GITHUB**, puis ajouter son contenu dans le dépôt.
Le `README.md`, les scripts et les sous-dossiers doivent apparaître dans le
dépôt : envoyer seulement le ZIP n'affiche pas les sources à parcourir.

Le dépôt contient un `.gitignore` pour conserver les références externes,
les archives et les fichiers temporaires hors du suivi Git. Ces exclusions
s'appliquent lors d'un ajout avec Git ou GitHub Desktop. Elles ne retirent
pas des fichiers déjà sélectionnés manuellement pour un envoi sur le site.

Le site GitHub accepte 25 MiB au maximum par fichier et 100 fichiers par envoi.
La version GITHUB est contrôlée par l'outil de préparation pour rester sous
ces limites. Référence : [documentation GitHub](https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository).

Aucun dépôt distant n'est créé et aucun fichier n'est publié par l'outil
de préparation.

## Utilisation dans Fusion

Voir [la notice de reprise](reprise_codex/LIRE%20EN%20PREMIER.txt).
Les scripts Fusion sont préparés mais n'ont pas été exécutés ni validés dans
Fusion par cette reprise. Le banc manuel et les contrôles hors Fusion ne
constituent pas une validation du débrayage avec la vraie pince JC.

La voie JC nominale de 155 mm est un compromis de compatibilité. La voie
D-Line réelle de 6,4 m représente 200 mm au 1:32. Les dimensions fonctionnelles
de la pince restent à relever avant de figer la géométrie de la gare.

## Outils locaux facultatifs

Pour les audits hors Fusion, les dépendances sont listées dans
`requirements.txt`. Les scripts Fusion utilisent l'API `adsk` fournie par
Fusion ; elle ne s'installe pas avec ces dépendances Python.

Depuis la racine du projet :

```text
python reprise_codex/audit_projet.py
python reprise_codex/generer_banc.py
python outils/preparer_archives.py
```

L'outil d'archivage utilise seulement la bibliothèque standard de Python.
Il ne lance aucun des scripts CAO et ne supprime pas les fichiers du projet.
Il refuse d'écraser une archive existante : utiliser `--suffixe` pour une
nouvelle sauvegarde.

## Attribution

Projet personnel développé avec l'aide de Claude puis de Codex. Jägerndorfer
et Doppelmayr désignent les produits étudiés ; ce projet n'est pas un produit
officiel de ces fabricants. Les références externes restent celles de leurs
auteurs et conservent leurs conditions d'utilisation propres. Aucune licence
globale n'a été attribuée automatiquement à ce projet.
