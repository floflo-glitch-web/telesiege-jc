# -*- coding: utf-8 -*-
# Gare debrayable 1:32 pour sieges Jagerndorfer D-Line (JC86541 "Waidoffen")
# Vrai modele : Doppelmayr 6-CLD-B Waidoffen (Hochfugen), gare aval.
#
# Version 2 (20/10/2026) - choix "le plus optimise" :
#   - ligne au standard JC (ecartement 155 mm) : pylones, cable et gare retour JC conserves
#   - UNE gare debrayable : motrice + tension + garage (gare aval) ; en haut, gare retour JC
#   - moteur sur la poulie, pneus entraines mecaniquement depuis la poulie (synchro garantie)
#   - garage au rez-de-chaussee, a l arriere (comme le vrai Waidoffen), 2 voies en boucle
#
# Contenu : parametres utilisateur, plan d implantation, elevation, volumes gabarits.
# Repere : X = vers la ligne (0 = axe de la poulie), Y = travers, Z = haut (0 = quai).
# Cote Y < 0 : brin qui ARRIVE en gare ; cote Y > 0 : brin qui REPART (embarquement).
# Les cotes marquees "A RECALER" attendent les mesures du siege / de la pince JC.
# Relancer le script recree un document neuf avec les valeurs ci-dessous.

import math
import os
import adsk.core
import adsk.fusion

MM = 0.1  # Fusion travaille en cm

GALET_STP = (r'C:\Users\blang\Downloads\Gare debrayable JC\references'
             r'\thingiverse_7292017_poulie_JC\files\rolna4.stp')

# nom, expression, unite, commentaire
PARAMS = [
    ('Echelle',       '32',         '',   'Echelle du modele 1:32'),
    ('Voie_ligne',    '155 mm',     'mm', 'Ecartement en ligne = standard JC (pylones JC50100, gare retour JC)'),
    ('Voie_gare',     'Voie_ligne', 'mm', 'Ecartement des rails en gare (200 mm = 6,4 m reel si la ligne est refaite)'),
    ('D_poulie',      'Voie_ligne', 'mm', 'Diametre a fond de gorge = ecartement en ligne'),
    ('Cable_d',       '2 mm',       'mm', 'Cable JC plastique 2 mm'),
    ('L_gare',        '812 mm',     'mm', 'Longueur hors tout : 26 m reel (6-CLD-B a bulle, Doppelmayr USA)'),
    ('W_gare',        '309 mm',     'mm', 'Largeur du batiment : 9,9 m reel'),
    ('Course_tension', '30 mm',     'mm', 'Course du chariot de tension (poulie + moteur) - ~1 m reel'),
    ('L_entree',      '94 mm',      'mm', 'Trompette d entree + debrayage : ~3 m reel'),
    ('L_ralent',      '375 mm',     'mm', 'Ralentisseur 5 -> 1 m/s a ~1 m/s2 : ~12 m reel'),
    ('L_quai',        '150 mm',     'mm', 'Zone d embarquement : ~4,7 m reel'),
    ('L_lanceur',     '375 mm',     'mm', 'Lanceur 1 -> 5 m/s : ~12 m reel'),
    ('L_embray',      '94 mm',      'mm', 'Embrayage + sortie : ~3 m reel'),
    ('H_cable',       '125 mm',     'mm', 'Hauteur du cable au-dessus du quai - A RECALER'),
    ('H_toit',        '200 mm',     'mm', 'Faitage du toit R1 au-dessus du quai - estimation'),
    ('Ep_dalle',      '3 mm',       'mm', 'Epaisseur de la dalle gabarit'),
    ('D_pneu',        '12.5 mm',    'mm', 'Pneu de gare 4.00-8 (~400 mm reel)'),
    ('Pas_pneu',      '13 mm',      'mm', 'Pas des pneus (quasi jointifs) - <= plaque de friction / 2'),
    ('Siege_L',       '120 mm',     'mm', 'Largeur du siege JC (travers) - A RECALER'),
    ('Siege_P',       '60 mm',      'mm', 'Profondeur du siege JC (sens de marche) - A RECALER'),
    ('Siege_H',       '110 mm',     'mm', 'Hauteur cable -> bas du siege - A RECALER'),
    ('Siege_Hs',      '35 mm',      'mm', 'Hauteur cable -> haut de la bulle (zone de la suspente) - A RECALER'),
    ('Pas_sieges',    '1300 mm',    'mm', 'Espacement en ligne : ~41,5 m reel'),
    ('Jeu_mur',       '15 mm',      'mm', 'Jeu mini siege -> mur'),
    ('Marge_arr',     'Voie_gare / 2 + Siege_L / 2 + Jeu_mur - D_poulie / 2', 'mm',
     'Batiment derriere la poulie : au contour les sieges balaient Voie_gare/2 + Siege_L/2'),
    ('N_garage',      '8',          '',   'Nombre de places au garage'),
    ('Pas_garage',    '75 mm',      'mm', 'Pas des sieges gares : profondeur 60 + jeu 15'),
    ('R_garage',      '90 mm',      'mm', 'Demi-entraxe des 2 voies de garage = rayon de la boucle'),
    ('L_garage',      'N_garage / 2 * Pas_garage', 'mm', 'Longueur utile de chaque voie de garage'),
    ('Marge_gar',     '40 mm',      'mm', 'Jeu gare / garage et murs du garage'),
]


def pt(x, y, z=0.0):
    return adsk.core.Point3D.create(x, y, z)


def texte(sk, s, x, y, h):
    """Texte centre sur (x, y) dans le plan de l esquisse (ASCII uniquement)."""
    w = max(len(s) * h * 0.75, h)
    inp = sk.sketchTexts.createInput2(s, h)
    inp.setAsMultiLine(pt(x - w / 2, y - h, 0), pt(x + w / 2, y + h, 0),
                       adsk.core.HorizontalAlignments.CenterHorizontalAlignment,
                       adsk.core.VerticalAlignments.MiddleVerticalAlignment, 0)
    sk.sketchTexts.add(inp)


def plan_offset(comp, expr, nom):
    planes = comp.constructionPlanes
    pin = planes.createInput()
    pin.setByOffset(comp.xYConstructionPlane, adsk.core.ValueInput.createByString(expr))
    pl = planes.add(pin)
    pl.name = nom
    return pl


def boite(comp, plane, x, y, dx, dy, hauteur_expr, nom):
    sk = comp.sketches.add(plane)
    sk.name = nom
    sk.sketchCurves.sketchLines.addTwoPointRectangle(
        pt(x - dx / 2, y - dy / 2), pt(x + dx / 2, y + dy / 2))
    ext = comp.features.extrudeFeatures.addSimple(
        sk.profiles.item(0), adsk.core.ValueInput.createByString(hauteur_expr),
        adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    ext.bodies.item(0).name = nom
    return ext


def dalle(comp, x0, y0, x1, y1, nom):
    sk = comp.sketches.add(comp.xYConstructionPlane)
    sk.name = nom
    sk.sketchCurves.sketchLines.addTwoPointRectangle(pt(x0, y0), pt(x1, y1))
    ext = comp.features.extrudeFeatures.addSimple(
        sk.profiles.item(0), adsk.core.ValueInput.createByString('-Ep_dalle'),
        adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    ext.bodies.item(0).name = nom


def run(_context):
    app = adsk.core.Application.get()
    app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
    design = adsk.fusion.Design.cast(app.activeProduct)
    design.designType = adsk.fusion.DesignTypes.ParametricDesignType
    root = design.rootComponent

    # ---- 1. parametres utilisateur -----------------------------------
    up = design.userParameters
    for nom, expr, unite, com in PARAMS:
        if up.itemByName(nom) is None:
            up.add(nom, adsk.core.ValueInput.createByString(expr), unite, com)

    def v(nom):
        return up.itemByName(nom).value  # cm (ou sans unite)

    rc = v('Voie_ligne') / 2.0          # demi-ecartement du cable
    rg = v('Voie_gare') / 2.0           # demi-ecartement des rails en gare
    R_bat = v('D_poulie') / 2.0 + v('Marge_arr')
    x_back = -R_bat
    x_front = v('L_gare') - R_bat
    x_ligne = x_front + 40 * MM
    W2 = v('W_gare') / 2.0

    # garage (voies en U derriere la gare)
    Rg = v('R_garage')
    x2 = x_back - v('Marge_gar')        # debut des voies de garage (cote gare)
    x1 = x2 - v('L_garage')             # fond des voies droites
    xg_back = x1 - Rg - v('Marge_gar') - v('Siege_P') / 2
    Wg2 = Rg + v('Siege_L') / 2 + 20 * MM

    # ---- 2. composant squelette : plan d implantation ----------------
    occ = root.occurrences.addNewComponent(adsk.core.Matrix3D.create())
    sq = occ.component
    sq.name = 'Squelette gare'

    sk = sq.sketches.add(sq.xYConstructionPlane)
    sk.name = 'Plan - implantation (Z = quai)'
    lines = sk.sketchCurves.sketchLines
    arcs = sk.sketchCurves.sketchArcs
    h_txt = 6 * MM

    lines.addTwoPointRectangle(pt(x_back, -W2), pt(x_front, W2))          # gare
    lines.addTwoPointRectangle(pt(xg_back, -Wg2), pt(x_back, Wg2))        # garage

    # trace du cable (construction)
    a = arcs.addByCenterStartSweep(pt(0, 0), pt(0, rc), math.pi)
    a.isConstruction = True
    for s in (1, -1):
        lines.addByTwoPoints(pt(0, s * rc), pt(x_ligne, s * rc)).isConstruction = True
    lines.addByTwoPoints(pt(xg_back, 0), pt(x_ligne, 0)).isConstruction = True

    # rails de gare : droites + contour (centre poulie)
    arcs.addByCenterStartSweep(pt(0, 0), pt(0, rg), math.pi)
    for s in (1, -1):
        lines.addByTwoPoints(pt(0, s * rg), pt(x_front, s * rg))

    # zones : cote arrivee (Y < 0) depuis l entree vers la poulie
    x = x_front
    for nom, L in (('ENTREE + DEBRAYAGE', v('L_entree')), ('RALENTISSEUR', v('L_ralent'))):
        x2z = x - L
        lines.addByTwoPoints(pt(x2z, -rg - 25 * MM), pt(x2z, -rg + 25 * MM))
        texte(sk, nom, (x + x2z) / 2, -rg - 18 * MM, h_txt)
        x = x2z
    texte(sk, 'ZONE LENTE', x / 2, -rg - 18 * MM, h_txt)

    # zones : cote depart (Y > 0) depuis la poulie vers la ligne
    x = 0.0
    for nom, L in (('EMBARQUEMENT', v('L_quai')), ('LANCEUR', v('L_lanceur')),
                   ('EMBRAYAGE', v('L_embray'))):
        x2z = x + L
        lines.addByTwoPoints(pt(x2z, rg - 25 * MM), pt(x2z, rg + 25 * MM))
        texte(sk, nom, (x + x2z) / 2, rg + 18 * MM, h_txt)
        x = x2z

    # poutres de pneus (schema) : entree + ralentisseur ; lanceur + embrayage
    n_ral = int(round((v('L_entree') + v('L_ralent')) / v('Pas_pneu')))
    n_lan = int(round((v('L_lanceur') + v('L_embray')) / v('Pas_pneu')))
    e = 4 * MM
    lines.addTwoPointRectangle(pt(x_front - v('L_entree') - v('L_ralent'), -rg - e),
                               pt(x_front, -rg + e))
    lines.addTwoPointRectangle(pt(v('L_quai'), rg - e),
                               pt(v('L_quai') + v('L_lanceur') + v('L_embray'), rg + e))
    texte(sk, 'PNEUS x{}'.format(n_ral), x_front - v('L_ralent') / 2, -rg + 12 * MM, h_txt)
    texte(sk, 'PNEUS x{}'.format(n_lan), v('L_quai') + v('L_lanceur') / 2, rg - 12 * MM, h_txt)

    # chariot de tension (poulie + moteur) et moteur
    ct = rc + 12 * MM
    lines.addTwoPointRectangle(pt(-ct, -ct), pt(ct, ct))
    lines.addTwoPointRectangle(pt(-20 * MM, -20 * MM), pt(20 * MM, 20 * MM))
    # la poulie est portee PAR LE HAUT (rien sous la poulie : les sieges y passent au contour)
    texte(sk, 'MOTEUR AU-DESSUS (TOIT)', 0, -30 * MM, h_txt * 0.8)
    texte(sk, 'CHARIOT DE TENSION (TOIT)', 0, ct + 8 * MM, h_txt * 0.8)

    # garage : voies en U + liaisons aux aiguillages du contour
    c45 = math.cos(math.radians(45))
    pA = pt(-rg * c45, -rg * c45)        # aiguillage entree garage (cote arrivee)
    pB = pt(-rg * c45, rg * c45)         # aiguillage sortie garage (cote depart)
    lines.addByTwoPoints(pt(x2, -Rg), pt(x1, -Rg))
    arcs.addByCenterStartSweep(pt(x1, 0), pt(x1, Rg), math.pi)
    lines.addByTwoPoints(pt(x1, Rg), pt(x2, Rg))
    lines.addByTwoPoints(pA, pt(x2, -Rg)).isConstruction = True
    lines.addByTwoPoints(pt(x2, Rg), pB).isConstruction = True
    sk.sketchPoints.add(pA)
    sk.sketchPoints.add(pB)
    texte(sk, 'GARAGE {} PLACES'.format(int(v('N_garage'))), (x1 + x2) / 2, 0, 8 * MM)
    texte(sk, 'AIGUILLAGE ENTREE', pA.x - 30 * MM, pA.y - 10 * MM, h_txt * 0.8)
    texte(sk, 'AIGUILLAGE SORTIE', pB.x - 30 * MM, pB.y + 10 * MM, h_txt * 0.8)

    texte(sk, 'GARE DEBRAYABLE JC 1:32 - WAIDOFFEN 6-CLD-B', x_front / 2, -W2 - 15 * MM, 8 * MM)
    texte(sk, 'ARRIVEE', x_front + 25 * MM, -rc, h_txt)
    texte(sk, 'DEPART', x_front + 25 * MM, rc, h_txt)

    # ---- 3. elevation (plan XZ) --------------------------------------
    ske = sq.sketches.add(sq.xZConstructionPlane)
    ske.name = 'Elevation - quai, cable, toit'

    def p_xz(xm, zm):
        return ske.modelToSketchSpace(pt(xm, 0, zm))

    le = ske.sketchCurves.sketchLines
    hc, ht = v('H_cable'), v('H_toit')
    le.addByTwoPoints(p_xz(xg_back, 0), p_xz(x_front, 0))                # quai + garage
    le.addByTwoPoints(p_xz(xg_back, ht), p_xz(x_front, ht))              # toits
    le.addByTwoPoints(p_xz(-rc, hc), p_xz(x_ligne, hc)).isConstruction = True
    for xx in (xg_back, x_back, x_front):
        le.addByTwoPoints(p_xz(xx, 0), p_xz(xx, ht))
    # entrainement + chariot de tension AU-DESSUS de la poulie, sous le toit
    le.addTwoPointRectangle(p_xz(-ct, hc + 6 * MM), p_xz(ct, ht - 8 * MM))

    # ---- 4. volumes gabarits ------------------------------------------
    occ2 = root.occurrences.addNewComponent(adsk.core.Matrix3D.create())
    gb = occ2.component
    gb.name = 'Gabarits volumes'
    dalle(gb, x_back, -W2, x_front, W2, 'Dalle gare')
    dalle(gb, xg_back, -Wg2, x_back, Wg2, 'Dalle garage')

    pl_c = plan_offset(gb, 'H_cable', 'Plan du cable')
    skp = gb.sketches.add(pl_c)
    skp.name = 'Poulie'
    skp.sketchCurves.sketchCircles.addByCenterRadius(pt(0, 0), rc + 3 * MM)
    ei = gb.features.extrudeFeatures.createInput(
        skp.profiles.item(0), adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    ei.setSymmetricExtent(adsk.core.ValueInput.createByString('6 mm'), True)
    gb.features.extrudeFeatures.add(ei).bodies.item(0).name = 'Poulie (gabarit)'

    skc = gb.sketches.add(pl_c)
    skc.name = 'Trace du cable'
    arc = skc.sketchCurves.sketchArcs.addByCenterStartSweep(pt(0, 0), pt(0, rc), math.pi)
    skc.sketchCurves.sketchLines.addByTwoPoints(arc.startSketchPoint, pt(x_ligne, rc))
    skc.sketchCurves.sketchLines.addByTwoPoints(arc.endSketchPoint, pt(x_ligne, -rc))
    pin = gb.features.pipeFeatures.createInput(
        gb.features.createPath(arc, True), adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    pin.sectionSize = adsk.core.ValueInput.createByString('Cable_d')
    gb.features.pipeFeatures.add(pin).bodies.item(0).name = 'Cable 2 mm'

    # enveloppes de sieges : 3 en gare + le garage plein
    pl_s = plan_offset(gb, 'H_cable - Siege_H', 'Plan bas des sieges')
    dx, dy = v('Siege_P'), v('Siege_L')
    h_bulle = 'Siege_H - Siege_Hs'
    boite(gb, pl_s, x_front - v('L_entree') - v('L_ralent') / 2, -rg, dx, dy, h_bulle,
          'Siege ralentisseur')
    boite(gb, pl_s, v('L_quai') / 2, rg, dx, dy, h_bulle, 'Siege embarquement')
    boite(gb, pl_s, v('L_quai') + v('L_lanceur') / 2, rg, dx, dy, h_bulle, 'Siege lanceur')
    pas = v('Pas_garage')
    n_voie = int(v('N_garage') // 2)
    for i in range(n_voie):
        xs = x2 - pas / 2 - i * pas
        boite(gb, pl_s, xs, -Rg, dx, dy, h_bulle, 'Garage A{}'.format(i + 1))
        boite(gb, pl_s, xs, Rg, dx, dy, h_bulle, 'Garage B{}'.format(i + 1))

    # galet JC de reference (Thingiverse 7292017, CC BY-SA)
    if os.path.exists(GALET_STP):
        im = app.importManager
        im.importToTarget(im.createSTEPImportOptions(GALET_STP), root)
        og = None
        for o in root.occurrences:
            if o.component.name not in ('Squelette gare', 'Gabarits volumes'):
                og = o
        og.component.name = 'Galet JC 16 (rolna4 - Thingiverse 7292017 CC BY-SA)'
        bb = og.boundingBox
        m = adsk.core.Matrix3D.create()   # pose a plat devant l entree de la gare
        m.translation = adsk.core.Vector3D.create(
            x_ligne + 20 * MM - (bb.minPoint.x + bb.maxPoint.x) / 2,
            -(bb.minPoint.y + bb.maxPoint.y) / 2, -bb.minPoint.z)
        og.transform = m
        design.snapshots.add()            # capture de position (sinon annulee au recalcul)

    app.activeViewport.fit()

    print('Squelette v2 cree.')
    print('Gare : X {:.0f} -> {:.0f} mm, largeur {:.0f} mm'.format(
        x_back / MM, x_front / MM, v('W_gare') / MM))
    print('Garage : X {:.0f} -> {:.0f} mm, largeur {:.0f} mm, {} places'.format(
        xg_back / MM, x_back / MM, 2 * Wg2 / MM, 2 * n_voie))
    print('Longueur totale gare + garage : {:.0f} mm'.format((x_front - xg_back) / MM))
    print('Voie ligne {:.0f} mm, voie gare {:.0f} mm, poulie {:.0f} mm, cable a {:.0f} mm'.format(
        2 * rc / MM, 2 * rg / MM, v('D_poulie') / MM, hc / MM))
    print('Pneus : {} cote arrivee, {} cote depart'.format(n_ral, n_lan))
    print('Jeu entre sieges face a face : {:.0f} mm ; siege -> mur : {:.0f} mm'.format(
        (2 * rg - dy) / MM, (W2 - rg - dy / 2) / MM))
