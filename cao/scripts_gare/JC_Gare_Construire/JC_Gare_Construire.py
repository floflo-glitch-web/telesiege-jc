# -*- coding: utf-8 -*-
# Gare debrayable JC 1:32 - reconstruction complete dans un document neuf :
#   1. JC_Gare_Debrayable (squelette, parametres, plan, garage)
#   2. JC_Gare_Mecanique  (poulie, moyeu, moteur, chariot de tension)
#   3. JC_Gare_Structure  (charpente, brides, tiges, vitrage du toit R1)
#   4. JC_Gare_Habillage  (nervures du toit, pieds et tetes de poteaux)
# Les STL des pieces imprimables vont dans Downloads\Gare debrayable JC\STL.

import os

BASE = os.path.join(os.environ['APPDATA'], 'Autodesk', 'Autodesk Fusion 360', 'API', 'Scripts')
ETAPES = ['JC_Gare_Debrayable', 'JC_Gare_Mecanique', 'JC_Gare_Structure', 'JC_Gare_Habillage']


def run(context):
    for nom in ETAPES:
        chemin = os.path.join(BASE, nom, nom + '.py')
        ns = {'__name__': nom}
        with open(chemin, encoding='utf-8') as f:
            exec(compile(f.read(), chemin, 'exec'), ns)
        print('==== ' + nom)
        ns['run'](context)
