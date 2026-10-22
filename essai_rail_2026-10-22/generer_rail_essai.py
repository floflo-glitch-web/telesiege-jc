"""Petit troncon de rail d'ESSAI pour verifier les cotes de la pince JC relevees sur photo.

Toutes les cotes viennent de mesures_photo_2026-10-22/ (estimations photo).
Modifier COTES puis relancer : python essai_rail_2026-10-22/generer_rail_essai.py
Repere du STL : X le long du cable, Y en travers (cable a Y = 0), Z vers le haut.
v1 : ecart des galets et position du cable valides par l'essai (22/10).
v2 : les traits des rails deviennent des gorges ou roulent les galets.
"""
from pathlib import Path
import json
import manifold3d as mf
import trimesh

BASE = Path(__file__).resolve().parent
VERSION = 'v2'

COTES = dict(
    longueur=50.0,              # le long du cable
    epaisseur_plaque=3.0,
    hauteur_rail=3.0,           # dessus de plaque -> fond de gorge (surface de roulement)
    gorge=dict(largeur_machoire=2.8,  # galet cote machoire, environ 1,5 mm sur photo
               largeur_oppose=3.6,    # galet oppose, le plus large : environ 2,1 mm sur photo
               bord=1.2,        # epaisseur de chaque bord
               bord_exterieur=1.0,
               bord_interieur=0.5),  # bas : le corps de la pince passe a moins d'1 mm cote machoire
    galet_machoire_y=6.3,       # centre du galet cote machoire depuis l'axe du cable
    entraxe_galets=24.6,
    cable_au_dessus_rail=7.75,  # fond de gorge -> cable : 4,2 + 3,55 (rayon galet 7,1)
    fente_suspente_y=18.0,      # axe de la suspente a hauteur de plaque
    fente_suspente_largeur=10.0,
    fente_suspente_longueur=38.0,
    plaque_y_min=-4.0,          # depasse sous le cable pour porter le trait de repere
    plaque_y_marge=4.0,         # au-dela du rail oppose
    rampe_entree=dict(profondeur=1.0, longueur=3.0),
    rainure=dict(largeur=0.6, profondeur=0.4),   # trait de repere du cable sur la plaque
)


def boite(x0, y0, z0, x1, y1, z1):
    return mf.Manifold.cube([x1 - x0, y1 - y0, z1 - z0]).translate([x0, y0, z0])


def rails(c):
    """(centre Y, largeur de gorge, cote exterieur) : rail cote machoire puis rail oppose."""
    y1, g = c['galet_machoire_y'], c['gorge']
    return ((y1, g['largeur_machoire'], -1), (y1 + c['entraxe_galets'], g['largeur_oppose'], 1))


def rail_essai(c):
    L, e, h, g = c['longueur'], c['epaisseur_plaque'], c['hauteur_rail'], c['gorge']
    (y1, _, _), (y2, lg2, _) = rails(c)
    ymax = y2 + lg2 / 2 + g['bord'] + c['plaque_y_marge']
    piece = boite(0, c['plaque_y_min'], 0, L, ymax, e)
    top = e + h
    for yr, lg, cote_ext in rails(c):
        w = lg + 2 * g['bord']
        rail = boite(0, yr - w / 2, e - 0.01, L, yr + w / 2, top)
        for cote, haut in ((cote_ext, g['bord_exterieur']), (-cote_ext, g['bord_interieur'])):
            y_in, y_out = yr + cote * lg / 2, yr + cote * w / 2
            rail = rail + boite(0, min(y_in, y_out), top - 0.01, L, max(y_in, y_out), top + haut)
        # rampe d'entree cote ouvert (X = 0) : fond de gorge et bords
        r = c['rampe_entree']
        z_haut = top + max(g['bord_exterieur'], g['bord_interieur'])
        tri = mf.CrossSection([[(-0.01, top - r['profondeur']), (r['longueur'], z_haut + 0.01), (-0.01, z_haut + 0.01)]])
        coin = mf.Manifold.extrude(tri, w + 2).rotate([90, 0, 0]).translate([0, yr + w / 2 + 1, 0])
        piece = piece + rail - coin
    # fente de la suspente, ouverte cote X = 0
    ys, ws = c['fente_suspente_y'], c['fente_suspente_largeur']
    piece = piece - boite(-1, ys - ws / 2, -1, c['fente_suspente_longueur'], ys + ws / 2, e + 1)
    # trait de repere du cable (a la verticale de l'axe du cable)
    r = c['rainure']
    piece = piece - boite(-1, -r['largeur'] / 2, e - r['profondeur'], L + 1, r['largeur'] / 2, e + 1)
    if piece.status() != mf.Error.NoError:
        raise RuntimeError(piece.status())
    return piece, dict(rail_machoire_y=y1, rail_oppose_y=y2, dessus_rail_z=e + h,
                       cable_z=e + h + c['cable_au_dessus_rail'], encombrement=[L, ymax - c['plaque_y_min'], e + h])


def apercu(m, info, c, chemin):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.patches import Circle, Rectangle, Polygon
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    fig = plt.figure(figsize=(13, 5.8), layout='constrained')
    ax = fig.add_subplot(1, 2, 1, projection='3d')
    ax.add_collection3d(Poly3DCollection(m.triangles, facecolors='#60a5fa', edgecolors='#1e3a8a', linewidths=0.05))
    ax.set(xlim=(0, 50), ylim=(-5, 45), zlim=(0, 20), xlabel='X le long du câble', ylabel='Y en travers', zlabel='Z')
    ax.set_box_aspect([50, 50, 20]); ax.view_init(elev=32, azim=-60)
    ax.set_title('Tronçon d’essai (STL)')
    bx = fig.add_subplot(1, 2, 2)
    e, h, g = c['epaisseur_plaque'], c['hauteur_rail'], c['gorge']
    yb0, yb1 = c['plaque_y_min'], info['rail_oppose_y'] + g['largeur_oppose'] / 2 + g['bord'] + c['plaque_y_marge']
    ys, ws = c['fente_suspente_y'], c['fente_suspente_largeur']
    bx.add_patch(Rectangle((yb0, 0), ys - ws / 2 - yb0, e, fc='#93c5fd', ec='#1e3a8a'))
    bx.add_patch(Rectangle((ys + ws / 2, 0), yb1 - ys - ws / 2, e, fc='#93c5fd', ec='#1e3a8a'))
    for yr, lg, cote_ext in rails(c):
        w = lg + 2 * g['bord']
        bx.add_patch(Rectangle((yr - w / 2, e), w, h, fc='#93c5fd', ec='#1e3a8a'))
        for cote, haut in ((cote_ext, g['bord_exterieur']), (-cote_ext, g['bord_interieur'])):
            y0 = min(yr + cote * lg / 2, yr + cote * w / 2)
            bx.add_patch(Rectangle((y0, e + h), g['bord'], haut, fc='#93c5fd', ec='#1e3a8a'))
    zc = info['cable_z']; za = zc - 4.2
    for yr, lw in ((info['rail_machoire_y'], 1.5), (info['rail_oppose_y'], 2.1)):
        bx.add_patch(Rectangle((yr - lw / 2, za - 3.55), lw, 7.1, fc='#e5e7eb', ec='#4b5563'))
    bx.plot([4.8, 32.8], [za, za], color='#374151', lw=4)
    bx.add_patch(Circle((0, zc), 1.25, fc='#111827'))
    bx.add_patch(Circle((19.8, zc + 12.2), 2.95, fc='#e5e7eb', ec='#4b5563'))
    bx.add_patch(Polygon([(15.2, za - 2), (19.2, za - 2), (19.6, -6), (15.6, -6)], fc='#374151', alpha=0.85))
    bx.axhline(info['dessus_rail_z'], color='#16a34a', lw=0.6, ls='--')
    bx.annotate('câble Ø 2,5\n(trait de repère dessous)', (0, zc), (-11, zc + 7), arrowprops=dict(arrowstyle='->'), fontsize=9)
    bx.annotate('', (info['rail_machoire_y'], -10), (info['rail_oppose_y'], -10), arrowprops=dict(arrowstyle='<->', color='#2563eb'))
    bx.text(18.6, -9.6, f"entraxe rails {c['entraxe_galets']:.1f}".replace('.', ','), ha='center', color='#2563eb', fontsize=9)
    bx.annotate('', (-7, info['dessus_rail_z']), (-7, zc), arrowprops=dict(arrowstyle='<->', color='#16a34a'))
    bx.text(-7.4, (info['dessus_rail_z'] + zc) / 2, f"{c['cable_au_dessus_rail']:.2f}".replace('.', ','), ha='right', va='center', color='#16a34a', fontsize=9)
    bx.annotate('', (0, -6.5), (info['rail_machoire_y'], -6.5), arrowprops=dict(arrowstyle='<->', color='#db2777'))
    bx.text(3.1, -6.1, f"{c['galet_machoire_y']:.1f}".replace('.', ','), ha='center', color='#db2777', fontsize=9)
    bx.text(21, -4.5, 'suspente dans la fente', ha='left', fontsize=8)
    bx.set(xlim=(-14, 42), ylim=(-12, 32), aspect='equal', xlabel='Y en travers (mm)', ylabel='Z (mm)')
    bx.set_title(f'Coupe {VERSION} : gorges de 2,8 (côté mâchoire) et 3,6 (galet le plus large)')
    bx.grid(alpha=0.2)
    fig.savefig(chemin, dpi=130)
    plt.close(fig)


def main():
    m, info = rail_essai(COTES)
    t = m.to_mesh()
    mesh = trimesh.Trimesh(vertices=t.vert_properties[:, :3], faces=t.tri_verts, process=True)
    assert mesh.is_watertight and mesh.volume > 0 and len(mesh.split()) == 1
    mesh.export(BASE / f'Rail_essai_JC_{VERSION}.stl')
    apercu(mesh, info, COTES, BASE / 'apercu_rail_essai.png')
    (BASE / 'rail_essai.json').write_text(json.dumps(dict(
        version=VERSION, cotes=COTES, positions={k: (round(v, 2) if isinstance(v, float) else [round(x, 2) for x in v])
                                for k, v in info.items()},
        volume_mm3=round(float(mesh.volume), 1),
        dimensions_mm=[round(float(v), 2) for v in mesh.extents],
        statut='Piece d essai ; ecart des galets valide par l essai v1, gorges a essayer'),
        ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Rail_essai_JC_{VERSION}.stl :', [round(float(v), 2) for v in mesh.extents], 'mm,', round(float(mesh.volume)), 'mm3')


if __name__ == '__main__':
    main()
