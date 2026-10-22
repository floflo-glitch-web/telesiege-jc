"""Controle hors Fusion des STL et des jeux balayes ; ne valide pas la pince."""
from pathlib import Path
import ast
import hashlib
import json
import math

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon as PatchPolygon
import numpy as np
import trimesh
from shapely.geometry import Polygon
from shapely.ops import unary_union

BASE = Path(__file__).resolve().parent
PROJET = BASE.parent


def empreinte(angle, rayon, largeur, profondeur, xc=0):
    # Au contour la largeur du siege est radiale, la profondeur tangentielle.
    r = np.array([math.cos(angle), math.sin(angle)])
    t = np.array([-r[1], r[0]])
    centre = np.array([xc, 0.0]) + rayon * r
    return Polygon([centre + a * largeur / 2 * r + b * profondeur / 2 * t
                    for a, b in ((-1,-1),(1,-1),(1,1),(-1,1))])


def main():
    p = json.loads((BASE/'parametres_projet.json').read_text('utf-8'))['cotes']
    W, D = p['largeur_siege_mm'], p['profondeur_siege_mm']
    r = p['voie_gare_mm']/2
    jeu = p['jeu_mur_souhaite_mm']
    # Formules de la version Claude : marge arriere basee sur rayon + largeur/2.
    mur = -(r+W/2+jeu)
    front = p['longueur_gare_mm'] + mur
    rayon_balayage = math.hypot(r+W/2, D/2)
    Rg = p['rayon_garage_mm']
    x2 = mur-p['marge_garage_mm']
    x1 = x2-p['places_garage']/2*p['pas_garage_mm']
    fond_gar = x1-Rg-p['marge_garage_mm']-D/2
    rayon_gar = math.hypot(Rg+W/2, D/2)
    rapports = {
      'date': '2026-10-21',
      'statut': 'Audit hors Fusion ; enveloppes supposees 120x60 ; aucune validation du debrayage',
      'jeux_mm': {
        'arriere_gare_balayage': -mur-rayon_balayage,
        'lateral_gare_balayage': p['largeur_gare_mm']/2-rayon_balayage,
        'arriere_garage_balayage': x1-rayon_gar-fond_gar,
        'plancher_sous_siege': p['hauteur_cable_mm']-p['hauteur_siege_mm'],
        'poteau_D16_en_ligne_droite': r-W/2-8,
      },
      'recommandations_implantation_mm': {
        'mur_arriere_gare_x_max_pour_15mm': -(rayon_balayage+jeu),
        'largeur_gare_min_pour_15mm_des_deux_cotes': 2*(rayon_balayage+jeu),
        'fond_garage_x_max_pour_15mm': x1-rayon_gar-jeu,
      },
      'cinematique': {
        'poulie_tr_min_pour_150mm_s': 60*p['vitesse_ligne_mm_s']/(math.pi*p['voie_ligne_mm']),
        'intervalle_si_pas_ligne_1300mm_s': 1300/p['vitesse_ligne_mm_s'],
        'pas_a_vitesse_gare_35mm_s': 1300*p['vitesse_gare_mm_s']/p['vitesse_ligne_mm_s'],
        'patin_longueur_min_pour_2_pneus_pas13_sans_marge': 2*p['pas_pneu_mm'],
      },
      'limites': [
        'Les valeurs utilisent une enveloppe centree sur le trajet de la pince : le vrai decalage suspente/pince manque.',
        'Assise, bulle et repose-pieds ne sont pas un solide rectangulaire reel. Resultats conservatifs pour le gabarit choisi.',
        'Aucun tangage, roulis ou oscillation du siege pris en compte.',
        'Aucun essai avec pince, pneus ou cable : absence de collision statique ne prouve pas le fonctionnement.',
        'Le maillage Spittal constitue une reference de fixation, pas les cotes du siege JC original.',
        'La force de tension est a mesurer ; le portage direct de la poulie sur le moteur attend une charge radiale admissible.',
      ],
      'stl_claude': [], 'sources_archivees': []
    }
    for f in sorted((PROJET/'STL').glob('*.stl')):
        m=trimesh.load_mesh(f)
        rapports['stl_claude'].append(dict(nom=f.name,sha256=hashlib.sha256(f.read_bytes()).hexdigest(),
          ferme=bool(m.is_watertight),volume_mm3=round(float(m.volume),3),
          dimensions_mm=np.round(m.extents,3).tolist(),corps_connexes=len(m.split())))
    for f in sorted((BASE/'sources_claude').rglob('*')):
        if f.is_file():
            if f.suffix=='.py': ast.parse(f.read_text('utf-8-sig'),filename=str(f))
            rapports['sources_archivees'].append(dict(chemin=str(f.relative_to(BASE)),
                       sha256=hashlib.sha256(f.read_bytes()).hexdigest()))
    out=BASE/'rapports'
    out.mkdir(exist_ok=True)
    (out/'audit_projet.json').write_text(json.dumps(rapports,ensure_ascii=False,indent=2),'utf-8')
    lignes=['AUDIT DE REPRISE - 21/10/2026',
      'Calculs sur enveloppes provisoires : ne vaut pas validation mecanique.',
      'Les 10 STL Claude sont conserves sans modification.']
    lignes += [f'{k} : {v:.2f} mm' for k,v in rapports['jeux_mm'].items()]
    lignes += ['','Corrections conseillees pour le gabarit suppose :']
    lignes += [f'{k} : {v:.2f} mm' for k,v in rapports['recommandations_implantation_mm'].items()]
    lignes += ['','STL : '+str(len(rapports['stl_claude']))+' fichiers verifies.']
    lignes += [f"{s['nom']} : ferme={s['ferme']}, {s['corps_connexes']} solide(s)" for s in rapports['stl_claude']]
    lignes += ['','Limites :']+rapports['limites']
    (out/'audit_projet.txt').write_text('\n'.join(lignes)+'\n','utf-8-sig')
    fig,axs=plt.subplots(1,2,figsize=(13,6),layout='constrained')
    for ax,rr,xc,xb,xf,hw,titre in (
       (axs[0],r,0,mur,front,p['largeur_gare_mm']/2,'Contour de la gare'),
       (axs[1],Rg,x1,fond_gar,x2,Rg+W/2+20,'Boucle du garage')):
        swept=unary_union([empreinte(a,rr,W,D,xc) for a in np.linspace(math.pi/2,3*math.pi/2,721)])
        for geo in getattr(swept,'geoms',[swept]):
            ax.add_patch(PatchPolygon(np.asarray(geo.exterior.coords),fc='#dbeafe',ec='#2563eb',lw=1))
        ax.plot([xb,xb],[-hw,hw],color='#dc2626',lw=2,label='Mur actuel')
        for a in np.linspace(math.pi/2,3*math.pi/2,7):
            pp=empreinte(a,rr,W,D,xc)
            ax.plot(*pp.exterior.xy,color='#64748b',lw=.8)
        th=np.linspace(math.pi/2,3*math.pi/2,150)
        ax.plot(xc+rr*np.cos(th),rr*np.sin(th),'k--',lw=1,label='Trajet de la pince')
        rgmax=math.hypot(rr+W/2,D/2)
        xmin=xc-rgmax
        g=xmin-xb
        ax.annotate(f'Jeu arriere : {g:.1f} mm',xy=(xb+g/2,0),xytext=(xc+10,30),
                    arrowprops={'arrowstyle':'->'},fontsize=10,color='#b91c1c')
        ax.set(xlim=(xc-rgmax-35,xc+rr+45),ylim=(-hw-25,hw+25),title=titre,xlabel='X (mm)',ylabel='Y (mm)')
        ax.set_aspect('equal');ax.grid(alpha=.15);ax.legend(loc='lower right',fontsize=8)
    fig.suptitle('Reprise JC : volume balaye par un gabarit 120 x 60 mm\nPince, decalage du siege et oscillations encore a mesurer',fontsize=12)
    fig.savefig(out/'controle_contours.png',dpi=150)
    plt.close(fig)
    print('\n'.join(lignes[:11]))


if __name__=='__main__':
    main()
