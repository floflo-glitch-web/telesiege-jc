# -*- coding: utf-8 -*-
"""
=============================================================================
 PINCE JAEGERNDORFER 1:32 (type AK / D-Line)
 Galets porteurs reposant sur le rail de gare - modele de controle
=============================================================================

 UTILISATION
   Fusion 360 > onglet UTILITAIRES > Modules complementaires
   > Scripts et modules complementaires > onglet Scripts
   > "+" > Creer > Python > nommer "pince_jc_galets"
   > cliquer sur l'icone dossier pour ouvrir le fichier cree
   > remplacer tout son contenu par ce fichier > Executer

 PARAMETRES
   Le script cree des parametres utilisateur Fusion.
   Pour changer une cote : Modifier > Modifier les parametres,
   puis RELANCER le script (il cree une nouvelle occurrence a chaque
   execution, les anciennes restent visibles pour comparaison).

 AVERTISSEMENT SUR LES COTES
   Une seule valeur est etablie : rope_dia = 2 mm.
   Toutes les autres sont des ESTIMATIONS. Elles sont la pour donner
   une geometrie plausible a regarder, pas pour etre prises pour argent
   comptant. Mesure ta pince et corrige-les.
=============================================================================
"""

import adsk.core
import adsk.fusion
import traceback

MM = 0.1  # 1 mm = 0.1 cm  (Fusion travaille en centimetres en interne)

# ---------------------------------------------------------------------------
#  nom             defaut     statut + role
# ---------------------------------------------------------------------------
PARAMS = [
    ('rope_dia',     '2 mm',   'ETABLI - cable acier 2 mm (pince AK/D-Line)'),
    ('roller_dia',   '3.2 mm', 'ESTIMATION - diametre du galet porteur'),
    ('roller_width', '2 mm',   'ESTIMATION - largeur du galet'),
    ('axle_dia',     '1 mm',   'ESTIMATION - diametre de l axe de galet'),
    ('roller_pitch', '12 mm',  'ESTIMATION - entraxe des 2 galets (sens de marche)'),
    ('axle_height',  '10 mm',  'ESTIMATION - hauteur axe galet au-dessus de l axe du cable'),
    ('rail_width',   '4 mm',   'A DEFINIR - largeur du rail de gare'),
    ('rail_thk',     '2 mm',   'A DEFINIR - epaisseur du rail de gare'),
    ('rail_len',     '120 mm', 'Longueur du troncon de rail modelise'),
    ('body_thk',     '1.5 mm', 'ESTIMATION - epaisseur du corps de pince'),
    ('body_gap',     '0.5 mm', 'Jeu lateral entre le rail et le corps de pince'),
]


def ensure_params(design):
    """Cree les parametres utilisateur s'ils n'existent pas. Renvoie {nom: valeur_cm}."""
    ups = design.userParameters
    values = {}
    for name, default, comment in PARAMS:
        p = ups.itemByName(name)
        if p is None:
            p = ups.add(name,
                        adsk.core.ValueInput.createByString(default),
                        'mm',
                        comment)
        values[name] = p.value  # toujours en cm
    return values


def cylinder_along_y(comp, x, z, dia, length):
    """Cylindre d'axe Y, centre sur Y=0, positionne en (x, z)."""
    sk = comp.sketches.add(comp.xZConstructionPlane)
    sk.sketchCurves.sketchCircles.addByCenterRadius(
        adsk.core.Point3D.create(x, z, 0), dia / 2.0)
    ext = comp.features.extrudeFeatures.createInput(
        sk.profiles.item(0),
        adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    ext.setSymmetricExtent(adsk.core.ValueInput.createByReal(length), True)
    return comp.features.extrudeFeatures.add(ext)


def cylinder_along_x(comp, y, z, dia, length):
    """Cylindre d'axe X, centre sur X=0, positionne en (y, z)."""
    sk = comp.sketches.add(comp.yZConstructionPlane)
    sk.sketchCurves.sketchCircles.addByCenterRadius(
        adsk.core.Point3D.create(y, z, 0), dia / 2.0)
    ext = comp.features.extrudeFeatures.createInput(
        sk.profiles.item(0),
        adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    ext.setSymmetricExtent(adsk.core.ValueInput.createByReal(length), True)
    return comp.features.extrudeFeatures.add(ext)


def _rect(sk, x0, y0, x1, y1):
    sk.sketchCurves.sketchLines.addTwoPointRectangle(
        adsk.core.Point3D.create(x0, y0, 0),
        adsk.core.Point3D.create(x1, y1, 0))


def box_on_xy(comp, x0, x1, y0, y1, z_start, thickness):
    """Pave extrude selon Z, depuis z_start."""
    sk = comp.sketches.add(comp.xYConstructionPlane)
    _rect(sk, x0, y0, x1, y1)
    ext = comp.features.extrudeFeatures.createInput(
        sk.profiles.item(0),
        adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    ext.startExtent = adsk.fusion.OffsetStartDefinition.create(
        adsk.core.ValueInput.createByReal(z_start))
    ext.setDistanceExtent(False, adsk.core.ValueInput.createByReal(thickness))
    return comp.features.extrudeFeatures.add(ext)


def plate_on_xz(comp, x0, x1, z0, z1, y_start, thickness):
    """Plaque extrudee selon Y, depuis y_start."""
    sk = comp.sketches.add(comp.xZConstructionPlane)
    _rect(sk, x0, z0, x1, z1)
    ext = comp.features.extrudeFeatures.createInput(
        sk.profiles.item(0),
        adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    ext.startExtent = adsk.fusion.OffsetStartDefinition.create(
        adsk.core.ValueInput.createByReal(y_start))
    ext.setDistanceExtent(False, adsk.core.ValueInput.createByReal(thickness))
    return comp.features.extrudeFeatures.add(ext)


def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        design = adsk.fusion.Design.cast(app.activeProduct)
        if not design:
            ui.messageBox("Ouvre d'abord un document Design dans Fusion, puis relance le script.")
            return

        design.designType = adsk.fusion.DesignTypes.ParametricDesignType
        v = ensure_params(design)
        root = design.rootComponent

        # ---- nouvelle occurrence a chaque execution -------------------------
        n = 1
        for occ in root.occurrences:
            if occ.component.name.startswith('Pince_galets_v'):
                n += 1
        occ = root.occurrences.addNewComponent(adsk.core.Matrix3D.create())
        comp = occ.component
        comp.name = 'Pince_galets_v{}'.format(n)

        # ---- geometrie deduite ---------------------------------------------
        rail_top = v['axle_height'] - v['roller_dia'] / 2.0
        rail_bottom = rail_top - v['rail_thk']
        rope_top = v['rope_dia'] / 2.0
        clearance = rail_bottom - rope_top          # garde verticale cable / rail
        body_y = v['rail_width'] / 2.0 + v['body_gap']
        axle_span = 2.0 * (body_y + v['body_thk'])
        half_pitch = v['roller_pitch'] / 2.0

        # ---- corps -----------------------------------------------------------
        # 1. rail de gare
        rail = box_on_xy(comp,
                         -v['rail_len'] / 2.0, v['rail_len'] / 2.0,
                         -v['rail_width'] / 2.0, v['rail_width'] / 2.0,
                         rail_bottom, v['rail_thk'])
        rail.bodies.item(0).name = 'rail_de_gare'

        # 2. galets porteurs + axes
        for i, sign in enumerate((-1.0, 1.0)):
            g = cylinder_along_y(comp, sign * half_pitch, v['axle_height'],
                                 v['roller_dia'], v['roller_width'])
            g.bodies.item(0).name = 'galet_{}'.format(i + 1)

            a = cylinder_along_y(comp, sign * half_pitch, v['axle_height'],
                                 v['axle_dia'], axle_span)
            a.bodies.item(0).name = 'axe_galet_{}'.format(i + 1)

        # 3. corps de pince (plaque laterale, schematique)
        body = plate_on_xz(comp,
                           -(half_pitch + 4 * MM), half_pitch + 4 * MM,
                           0.0, v['axle_height'],
                           body_y, v['body_thk'])
        body.bodies.item(0).name = 'corps_pince_schematique'

        # 4. cable
        rope = cylinder_along_x(comp, 0.0, 0.0, v['rope_dia'], v['rail_len'])
        rope.bodies.item(0).name = 'cable'

        app.activeViewport.fit()

        # ---- rapport de controle -------------------------------------------
        def mm(x):
            return x / MM

        alerte = ''
        if clearance <= 0:
            alerte = ("\n\n>>> COLLISION : avec ces valeurs le rail traverse le cable.\n"
                      "    Augmente axle_height, ou reduis roller_dia / rail_thk.")
        elif clearance < 0.5 * MM:
            alerte = "\n\n>>> Garde tres faible (< 0,5 mm). A verifier sur la piece."

        msg = (
            "{} cree.\n\n"
            "--- GEOMETRIE DEDUITE ---\n"
            "Dessus du rail (Z)        : {:.2f} mm\n"
            "Dessous du rail (Z)       : {:.2f} mm\n"
            "Garde verticale cable/rail: {:.2f} mm\n"
            "Entraxe des galets        : {:.2f} mm\n\n"
            "--- EQUIVALENCE ECHELLE 1 (x32) ---\n"
            "Galet   {:.2f} mm  ->  {:.0f} mm reels\n"
            "Cable   {:.2f} mm  ->  {:.0f} mm reels\n"
            "Entraxe {:.2f} mm  ->  {:.2f} m reels\n\n"
            "Repere : un galet porteur de vraie pince fait environ 100 a 150 mm,\n"
            "soit 3,1 a 4,7 mm a l'echelle 1:32.{}"
        ).format(
            comp.name,
            mm(rail_top), mm(rail_bottom), mm(clearance), mm(v['roller_pitch']),
            mm(v['roller_dia']), mm(v['roller_dia']) * 32,
            mm(v['rope_dia']), mm(v['rope_dia']) * 32,
            mm(v['roller_pitch']), mm(v['roller_pitch']) * 32 / 1000.0,
            alerte
        )
        ui.messageBox(msg, 'Pince JC 1:32 - controle des cotes')

    except:
        if ui:
            ui.messageBox('Echec :\n{}'.format(traceback.format_exc()))
