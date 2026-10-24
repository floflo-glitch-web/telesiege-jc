# -*- coding: utf-8 -*-
"""Reprise locale du constructeur Claude. Pas de dependance au dossier AppData.

Les sources archivees restent intactes. Cree un document neuf et une archive locale.
Les jeux ci-dessous sont des corrections de GABARIT provisoire, pas des cotes JC.
"""
from pathlib import Path
from datetime import datetime
import json
import math
import traceback
import adsk.core
import adsk.fusion

BASE=Path(__file__).resolve().parents[1]
PROJET=BASE.parent
ETAPES=['JC_Gare_Debrayable','JC_Gare_Mecanique','JC_Gare_Structure','JC_Gare_Habillage']


def run(context):
    app=adsk.core.Application.get()
    stamp=datetime.now().strftime('%Y%m%d_%H%M%S')
    sortie=BASE/'constructions'/stamp
    sortie.mkdir(parents=True,exist_ok=True)
    p=json.loads((BASE/'parametres_projet.json').read_text('utf-8'))['cotes']
    overrides={
        'Voie_ligne':f"{p['voie_ligne_mm']} mm",'Voie_gare':f"{p['voie_gare_mm']} mm",
        'L_gare':f"{p['longueur_gare_mm']} mm",'W_gare':f"{p['largeur_gare_mm']} mm",
        'Siege_L':f"{p['largeur_siege_mm']} mm",'Siege_P':f"{p['profondeur_siege_mm']} mm",
        'H_cable':f"{p['hauteur_cable_mm']} mm",'Siege_H':f"{p['hauteur_siege_mm']} mm",
        'Jeu_mur':f"{p['jeu_mur_souhaite_mm']} mm",'R_garage':f"{p['rayon_garage_mm']} mm",
        'N_garage':str(p['places_garage']),'Pas_garage':f"{p['pas_garage_mm']} mm",
        'Marge_gar':f"{p['marge_garage_mm']} mm",
        # Coin du siege en virage : garder la vraie marge avec le gabarit rectangulaire.
        'Marge_arr': 'sqrt((Voie_gare/2 + Siege_L/2)^2 + (Siege_P/2)^2) + Jeu_mur - D_poulie/2',
    }
    rapport={'date':stamp,'statut':'INCOMPLET','etapes':[],
      'hypotheses':'Siege JC original non mesure ; pince, rails, came, pneus et garage non fonctionnels',
      'corrections_gabarits':['Marge arriere gare tenant compte du coin du siege en virage',
        'Controle de la place moteur suivant le reducteur choisi'],
      'non_resolu':['Charge radiale admissible du moteur','Pas et glissement des pneus',
        'Rails et came selon vraie pince','Fixation portante du toit du garage','Trajet des aiguillages']}
    try:
        for nom in ETAPES:
            chemin=BASE/'scripts_gare'/nom/(nom+'.py')
            ns={'__name__':nom,'__file__':str(chemin)}
            exec(compile(chemin.read_text('utf-8-sig'),str(chemin),'exec'),ns)
            if 'PARAMS' in ns:
                ns['PARAMS']=[(n,overrides.get(n,e),u,c) for n,e,u,c in ns['PARAMS']]
            if 'GALET_STP' in ns:
                ns['GALET_STP']=str(PROJET/'references'/'thingiverse_7292017_poulie_JC'/'files'/'rolna4.stp')
            if 'DOSSIER_STL' in ns:
                ns['DOSSIER_STL']=str(sortie/'STL')
            # Le moteur exact n'est pas choisi : conserver 24 mm de Claude avec alerte.
            ns['run'](context)
            rapport['etapes'].append(nom)
        d=adsk.fusion.Design.cast(app.activeProduct)
        app.activeDocument.name='JC - implantation provisoire - reprise'
        archive=sortie/'Gare_JC_implantation_provisoire.f3d'
        if not d.exportManager.execute(d.exportManager.createFusionArchiveExportOptions(str(archive))):
            raise RuntimeError('Echec export F3D')
        rapport['parametres']=[dict(nom=q.name,expression=q.expression,unite=q.unit,commentaire=q.comment)
                                for q in d.userParameters]
        rapport.update(statut='GENERE_DANS_FUSION_SANS_VALIDATION_FONCTIONNELLE',archive_locale=str(archive))
        app.userInterface.messageBox('Implantation provisoire creee.\nArchive locale : '+str(archive)+
              '\nLa pince et le debrayage restent a mesurer et essayer.')
    except Exception:
        rapport['erreur']=traceback.format_exc()
        app.userInterface.messageBox(rapport['erreur'])
    finally:
        (sortie/'rapport_execution.json').write_text(json.dumps(rapport,ensure_ascii=False,indent=2),'utf-8')


def stop(context):
    pass
