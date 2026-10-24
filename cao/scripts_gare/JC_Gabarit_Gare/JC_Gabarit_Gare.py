# -*- coding: utf-8 -*-
# Gabarit parametrique - gare debrayable Jagerndorfer 1:32
#
# Cree les parametres utilisateur du systeme JC, puis une esquisse
# du trace du cable en gare (les deux brins + le contour).
# Toutes les cotes en aval doivent referencer ces parametres.

import math
import traceback
import adsk.core
import adsk.fusion

MM = 0.1  # Fusion travaille en cm en interne : 1 mm = 0.1

# nom, valeur, commentaire
PARAMS = [
    ('JC_entraxe',     '155 mm',  'Entraxe des deux brins (Spurweite JC 1:32)'),
    ('JC_cable_d',     '3 mm',    'Diametre du cable PP - A VERIFIER au pied a coulisse'),
    ('JC_rayon_contour', 'JC_entraxe / 2', 'Rayon du contour = demi-entraxe'),
    ('JC_pas_sieges',  '1300 mm', 'Pas des sieges (Waidoffen 41.5 m / 32)'),
    ('JC_long_gare',   '390 mm',  'Longueur hors-tout gare motrice JC'),
    ('JC_larg_gare',   '240 mm',  'Largeur hors-tout gare motrice JC'),
    ('JC_haut_gare',   '210 mm',  'Hauteur hors-tout gare motrice JC'),
]


def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        design = adsk.fusion.Design.cast(app.activeProduct)

        if not design:
            ui.messageBox(
                "Ouvre un document de conception (Design), puis relance le script.")
            return

        # ---- 1. parametres utilisateur -------------------------------
        params = design.userParameters
        crees = []
        for nom, expr, commentaire in PARAMS:
            if params.itemByName(nom) is None:
                params.add(nom,
                           adsk.core.ValueInput.createByString(expr),
                           'mm',
                           commentaire)
                crees.append(nom)

        # ---- 2. esquisse du trace du cable ---------------------------
        root = design.rootComponent
        sk = root.sketches.add(root.xYConstructionPlane)
        sk.name = 'JC - trace cable en gare'

        lines = sk.sketchCurves.sketchLines
        arcs = sk.sketchCurves.sketchArcs
        circles = sk.sketchCurves.sketchCircles
        pt = adsk.core.Point3D.create

        entraxe = 155 * MM
        rayon = entraxe / 2.0
        longueur = 390 * MM

        # les deux brins, montee et descente
        lines.addByTwoPoints(pt(0.0,  rayon, 0.0), pt(longueur,  rayon, 0.0))
        lines.addByTwoPoints(pt(0.0, -rayon, 0.0), pt(longueur, -rayon, 0.0))

        # le contour : demi-tour du cable autour de la poulie
        arcs.addByCenterStartSweep(pt(0.0, 0.0, 0.0),
                                   pt(0.0, rayon, 0.0),
                                   math.pi)

        # poulie de contour, en construction
        poulie = circles.addByCenterRadius(pt(0.0, 0.0, 0.0), rayon)
        poulie.isConstruction = True

        # axe de gare, en construction
        axe = lines.addByTwoPoints(pt(-rayon, 0.0, 0.0),
                                   pt(longueur, 0.0, 0.0))
        axe.isConstruction = True

        # ---- 3. compte rendu -----------------------------------------
        if crees:
            liste = '\n  - '.join(crees)
            msg_p = "Parametres crees :\n  - {}".format(liste)
        else:
            msg_p = "Parametres deja presents, rien a creer."

        ui.messageBox(
            "Gabarit JC 1:32 en place.\n\n"
            "{}\n\n"
            "Esquisse : \"{}\"\n"
            "  entraxe des brins   155 mm\n"
            "  rayon de contour     77.5 mm\n"
            "  longueur de gare    390 mm\n\n"
            "Modifie les valeurs dans Modifier > Changer les parametres.".format(
                msg_p, sk.name))

    except:
        if ui:
            ui.messageBox('Echec du script :\n{}'.format(traceback.format_exc()))
