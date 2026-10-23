"""Troncon de rail d'ESSAI en VIRAGE, avec le profil valide du rail droit (v5/v6).

Reprend les cotes de generer_rail_essai.py. Le virage suit le rayon du cable autour
de la poulie (155 mm de diametre), le cas le plus serre prevu en gare.
Hypothese : machoire vers l'interieur du virage, galets et suspente vers l'exterieur,
comme sur la poulie JC ou la pince passe a l'exterieur de la jante.
Relancer : python essai_rail_2026-10-22/generer_rail_virage.py
Repere : centre du virage a l'origine, entree droite le long de Y < 0, Z vers le haut.
"""
from pathlib import Path
import json
import math
import manifold3d as mf
import trimesh
from generer_rail_essai import COTES

BASE = Path(__file__).resolve().parent
VERSION = 'v1'

VIRAGE = dict(
    rayon_cable=77.5,           # rayon du cable autour de la poulie JC (155 / 2)
    angle=60.0,                 # degres
    entree_droite=15.0,         # ligne droite avant le virage, cote entree
    gorge_virage=2.0,           # 1,4 en ligne droite : les deux petits galets en tandem
                                # forment une corde et se mettent en biais dans la courbe
    pont_fin=8.0,               # plaque pleine a la fin de la fente de suspente (mm a son rayon)
    segments=720,               # facettes pour 360 degres
)


def rect(u0, z0, u1, z1, R):
    return mf.CrossSection.square([u1 - u0, z1 - z0]).translate([R + u0, z0])


def profil(c, R, lg):
    """Coupe (rayon, Z) du troncon pour une largeur de gorge des petits galets lg."""
    e, h, g, k = c['epaisseur_plaque'], c['hauteur_rail'], c['gorge'], c['contre_rail']
    top = e + h
    y1 = c['galet_machoire_y']
    y2 = y1 + c['entraxe_galets']
    y_paroi = c['bout_axe_oppose_y'] + k['jeu_bout_axe']
    z_bas = top + c['gros_galet_diametre'] + k['jeu_dessus']
    z_haut = z_bas + k['epaisseur']
    y_int = y2 - c['gros_galet_largeur'] / 2 - 0.15
    w = lg + 2 * g['bord']
    pieces = [
        rect(c['plaque_y_min'], 0, y_paroi + k['epaisseur_paroi'] + c['plaque_y_marge'], e, R),
        rect(y1 - w / 2, e - 0.01, y1 + w / 2, top, R),                          # rail des petits galets
        rect(y1 - w / 2, top - 0.01, y1 - lg / 2, top + g['bord_exterieur'], R),  # bord cote cable
        rect(y1 + lg / 2, top - 0.01, y1 + w / 2, top + g['bord_interieur'], R),  # bord cote suspente
        rect(y2 - c['plancher_c_interieur'], e - 0.01, y_paroi + 0.01, top, R),   # fond plat du C
        rect(y_paroi, e - 0.01, y_paroi + k['epaisseur_paroi'], z_haut, R),       # paroi
        rect(y_int, z_bas, y_paroi + 0.01, z_haut, R),                            # contre-rail
    ]
    cs = pieces[0]
    for p in pieces[1:]:
        cs = cs + p
    return cs, dict(top=top, y1=y1, y2=y2, w=w, y_paroi=y_paroi, z_bas=z_bas, z_haut=z_haut, y_int=y_int)


def droite(cs, longueur):
    """Extrusion de la coupe le long de Y, de -longueur a 0 (entree du virage)."""
    return mf.Manifold.extrude(cs, longueur + 0.01).rotate([90, 0, 0]).translate([0, 0.01, 0])


def coin_entree(y_entree, x0, x1, z_pied, z_sommet, longueur):
    """Coupe en biais a l'entree (Y = y_entree), sur la largeur radiale x0 -> x1."""
    tri = mf.CrossSection([[(y_entree - 0.01, z_pied), (y_entree + longueur, z_sommet), (y_entree - 0.01, z_sommet)]])
    return mf.Manifold.extrude(tri, x1 - x0).rotate([90, 0, 90]).translate([x0, 0, 0])


def rail_virage(c, v):
    R, L0 = v['rayon_cable'], v['entree_droite']
    seg = v['segments']
    cs_arc, d = profil(c, R, v['gorge_virage'])
    cs_droit, _ = profil(c, R, c['gorge']['largeur_machoire'])
    piece = mf.Manifold.revolve(cs_arc, seg, v['angle']) + droite(cs_droit, L0)
    e, g, k = c['epaisseur_plaque'], c['gorge'], c['contre_rail']
    y0 = -L0
    # rampes d'entree : gorge des petits galets et fond du C ; evasement du contre-rail
    r = c['rampe_entree']
    w0 = c['gorge']['largeur_machoire'] + 2 * g['bord']
    piece = piece - coin_entree(y0, R + d['y1'] - w0 / 2 - 1, R + d['y1'] + w0 / 2 + 1,
                                d['top'] - r['profondeur'], d['top'] + g['bord_exterieur'] + 0.01, r['longueur'])
    # coupes arretees a 0,02 mm de la paroi : pas de face confondue avec elle
    piece = piece - coin_entree(y0, R + d['y2'] - c['plancher_c_interieur'] - 0.01, R + d['y_paroi'] - 0.02,
                                d['top'] - r['profondeur'], d['top'] + 0.01, r['longueur'])
    ev = k['evasement']
    evas = mf.CrossSection([[(y0 - 0.01, d['z_bas'] - 0.01), (y0 + ev['longueur'], d['z_bas'] - 0.01),
                             (y0 - 0.01, d['z_bas'] + ev['hauteur'])]])
    piece = piece - mf.Manifold.extrude(evas, d['y_paroi'] - d['y_int'] + 0.98).rotate([90, 0, 90]).translate([R + d['y_int'] - 1, 0, 0])
    # fente de la suspente : ouverte a l'entree, fermee sur les derniers millimetres du virage
    ys, ws = c['fente_suspente_y'], c['fente_suspente_largeur']
    fente = rect(ys - ws / 2, -1, ys + ws / 2, e + 1, R)
    angle_fente = v['angle'] - math.degrees(v['pont_fin'] / (R + ys))
    piece = piece - mf.Manifold.revolve(fente, seg, angle_fente) - droite(fente, L0 + 1).translate([0, 0.5, 0])
    # trait de repere du cable, au rayon du cable
    rr = c['rainure']
    trait = rect(-rr['largeur'] / 2, e - rr['profondeur'], rr['largeur'] / 2, e + 1, R)
    piece = piece - mf.Manifold.revolve(trait, seg, v['angle'] + 1) - droite(trait, L0 + 1)
    if piece.status() != mf.Error.NoError:
        raise RuntimeError(piece.status())
    d.update(rayon_gorge_petits_galets=R + d['y1'], rayon_centre_gros_galet=R + d['y2'],
             rayon_paroi=R + d['y_paroi'], angle_fente=round(angle_fente, 1))
    return piece, d


def apercu(mesh, d, c, v, chemin):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    import numpy as np
    fig = plt.figure(figsize=(13, 6), layout='constrained')
    ax = fig.add_subplot(1, 2, 1, projection='3d')
    ax.add_collection3d(Poly3DCollection(mesh.triangles, facecolors='#60a5fa', edgecolors='none'))
    b = mesh.bounds
    ax.set(xlim=(b[0][0], b[1][0]), ylim=(b[0][1], b[1][1]), zlim=(0, 40), xlabel='X', ylabel='Y', zlabel='Z')
    ax.set_box_aspect([b[1][0] - b[0][0], b[1][1] - b[0][1], 40]); ax.view_init(elev=35, azim=-140)
    ax.set_title('Tronçon d’essai en virage (STL)')
    bx = fig.add_subplot(1, 2, 2)
    R, L0, a = v['rayon_cable'], v['entree_droite'], math.radians(v['angle'])
    t = np.linspace(0, a, 200)
    traces = ((R, 'câble (trait)', '#111827', '--'),
              (d['rayon_gorge_petits_galets'], f"petits galets, gorge {v['gorge_virage']:.1f}".replace('.', ','), '#db2777', '-'),
              (d['rayon_centre_gros_galet'], 'gros galet (C)', '#2563eb', '-'),
              (d['rayon_paroi'], 'paroi du C', '#1e3a8a', ':'))
    for r, nom, col, ls in traces:
        bx.plot(np.r_[r, r * np.cos(t)], np.r_[-L0, r * np.sin(t)], color=col, ls=ls, lw=1.6,
                label=f'{nom} : R {r:.1f}'.replace('.', ','))
    bx.plot(0, 0, 'k+'); bx.annotate('centre de la poulie', (0, 0), (8, -12), fontsize=8)
    bx.annotate('entrée', (R + 18, -L0), (R + 30, -L0 - 12), arrowprops=dict(arrowstyle='->'), fontsize=9)
    bx.set(aspect='equal', xlabel='X (mm)', ylabel='Y (mm)', xlim=(-10, 125), ylim=(-35, 110))
    bx.legend(loc='upper left', bbox_to_anchor=(0.0, 0.72), fontsize=7.5); bx.grid(alpha=0.2)
    bx.set_title('Vue de dessus : rayons des rails (mâchoire à l’intérieur du virage)')
    fig.savefig(chemin, dpi=130)
    plt.close(fig)


def main():
    m, d = rail_virage(COTES, VIRAGE)
    t = m.to_mesh()
    mesh = trimesh.Trimesh(vertices=t.vert_properties[:, :3], faces=t.tri_verts, process=True)
    assert mesh.is_watertight and mesh.volume > 0 and len(mesh.split()) == 1
    nom = f'Rail_virage_JC_{VERSION}.stl'
    mesh.export(BASE / nom)
    apercu(mesh, d, COTES, VIRAGE, BASE / 'apercu_rail_virage.png')
    (BASE / 'rail_virage.json').write_text(json.dumps(dict(
        version=VERSION, virage=VIRAGE, positions={k: round(x, 2) for k, x in d.items()},
        volume_mm3=round(float(mesh.volume), 1), dimensions_mm=[round(float(x), 2) for x in mesh.extents],
        statut='Piece d essai en virage ; profil valide en ligne droite, gorge elargie en courbe a essayer'),
        ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(nom, ':', [round(float(x), 1) for x in mesh.extents], 'mm,', round(float(mesh.volume)), 'mm3')


if __name__ == '__main__':
    main()
