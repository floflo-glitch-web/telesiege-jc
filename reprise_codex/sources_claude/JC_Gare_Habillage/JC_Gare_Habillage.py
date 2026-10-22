# -*- coding: utf-8 -*-
# Gare debrayable JC 1:32 - etape 4 : nervures du toit R1 + pieds et tetes de poteaux.
# A lancer apres JC_Gare_Structure (meme document).
#
# Toit R1 comme le vrai : nervures (arcs) sous un vitrage transparent (feuille PET 0,5 mm).
# Chaque nervure = 2 DEMI-NERVURES imprimees a plat (~160 x 50 x 3 mm, tout plateau),
# posees sur la poutre centrale (encoche) et collees sous le vitrage.
# Poteaux en tube alu D16 : pied imprime (vis dans le socle) + tete imprimee (berceau de la poutre 15x15).

import math
import os
import adsk.core
import adsk.fusion

MM = 0.1
DOSSIER_STL = r'C:\Users\blang\Downloads\Gare debrayable JC\STL'

PARAMS = [
    ('Pas_nervures', '40 mm', 'mm', 'Pas des nervures du toit R1 (~1,3 m reel)'),
    ('Nerv_ep',      '3 mm',  'mm', 'Epaisseur des nervures (sens X)'),
    ('Nerv_h',       '5 mm',  'mm', 'Hauteur de la bande des nervures'),
]


def P(x, y, z=0.0):
    return adsk.core.Point3D.create(x, y, z)


def plan_offset(comp, base, d_cm, nom):
    pin = comp.constructionPlanes.createInput()
    pin.setByOffset(base, adsk.core.ValueInput.createByReal(d_cm))
    pl = comp.constructionPlanes.add(pin)
    pl.name = nom
    return pl


def extr(comp, profil, d_cm, nom, op=adsk.fusion.FeatureOperations.NewBodyFeatureOperation, part=None):
    ein = comp.features.extrudeFeatures.createInput(profil, op)
    ein.setDistanceExtent(False, adsk.core.ValueInput.createByReal(d_cm))
    if part:
        ein.participantBodies = part
    f = comp.features.extrudeFeatures.add(ein)
    if nom and f.bodies.count:
        f.bodies.item(0).name = nom
    return f


def run(_context):
    app = adsk.core.Application.get()
    design = adsk.fusion.Design.cast(app.activeProduct)
    root = design.rootComponent
    up = design.userParameters
    assert up.itemByName('Z_poutre') is not None, 'Lancer d abord JC_Gare_Structure'
    for nom, expr, unite, com in PARAMS:
        if up.itemByName(nom) is None:
            up.add(nom, adsk.core.ValueInput.createByString(expr), unite, com)

    def v(nom):
        return up.itemByName(nom).value

    R_bat = v('D_poulie') / 2 + v('Marge_arr')
    x_back, x_front = -R_bat, v('L_gare') - R_bat
    W2 = v('W_gare') / 2
    z_e, z_t, R, e = v('Z_avant_toit'), v('H_toit'), v('R_toit'), v('Ep_toit')
    z_p, c = v('Z_poutre'), v('Poutre_c')
    hw_g = v('R_garage') + v('Siege_L') / 2 + 20 * MM
    x2 = x_back - v('Marge_gar')
    xg_back = x2 - v('L_garage') - v('R_garage') - v('Marge_gar') - v('Siege_P') / 2
    ep, h = v('Nerv_ep'), v('Nerv_h')

    occ = root.occurrences.addNewComponent(adsk.core.Matrix3D.create())
    hb = occ.component
    hb.name = 'Habillage (nervures, pieds, tetes)'
    a_imprimer = []

    # ---- 1. nervures : demi-nervure gauche + droite, puis reseau le long de X ----
    def demi_nervure(x0, hw, s, nom):
        """Demi-arc sous le vitrage, cote s (+1 / -1), de y = 0 a y = s * hw."""
        pl = plan_offset(hb, hb.yZConstructionPlane, x0, nom)
        sk = hb.sketches.add(pl)
        sk.name = nom
        q = lambda yy, zz: sk.modelToSketchSpace(P(x0, yy, zz))
        L = sk.sketchCurves.sketchLines
        A = sk.sketchCurves.sketchArcs
        k = math.cos(math.radians(45))
        ro, ri = R - e, R - e - h                       # rayons du bord exterieur / interieur
        yo, yi = hw - e, hw - e - h
        L.addByTwoPoints(q(0, z_t - e), q(s * (hw - R), z_t - e))
        A.addByThreePoints(q(s * (hw - R), z_t - e), q(s * (hw - R + ro * k), z_t - R + ro * k),
                           q(s * yo, z_t - R))
        L.addByTwoPoints(q(s * yo, z_t - R), q(s * yo, z_e))
        L.addByTwoPoints(q(s * yo, z_e), q(s * yi, z_e))
        L.addByTwoPoints(q(s * yi, z_e), q(s * yi, z_t - R))
        A.addByThreePoints(q(s * yi, z_t - R), q(s * (hw - R + ri * k), z_t - R + ri * k),
                           q(s * (hw - R), z_t - e - h))
        L.addByTwoPoints(q(s * (hw - R), z_t - e - h), q(0, z_t - e - h))
        L.addByTwoPoints(q(0, z_t - e - h), q(0, z_t - e))
        pr = max(list(sk.profiles), key=lambda p: p.areaProperties().area)
        b = extr(hb, pr, ep, nom).bodies.item(0)
        # encoche pour la poutre centrale
        plo = plan_offset(hb, hb.xYConstructionPlane, z_p, nom + ' encoche')
        sko = hb.sketches.add(plo)
        sko.name = nom + ' encoche'
        y_in = s * (c / 2 + 0.2 * MM)
        sko.sketchCurves.sketchLines.addTwoPointRectangle(P(x0 - 1 * MM, 0), P(x0 + ep + 1 * MM, y_in))
        extr(hb, sko.profiles.item(0), c + 0.2 * MM, None,
             op=adsk.fusion.FeatureOperations.CutFeatureOperation, part=[b])
        return b

    def reseau(corps, x0, x1, nom):
        n = int(math.floor(((x1 - x0) - ep) / v('Pas_nervures') + 1e-6)) + 1
        oc = adsk.core.ObjectCollection.create()
        for b in corps:
            oc.add(b)
        pin = hb.features.rectangularPatternFeatures.createInput(
            oc, hb.xConstructionAxis, adsk.core.ValueInput.createByReal(n),
            adsk.core.ValueInput.createByReal(v('Pas_nervures')),
            adsk.fusion.PatternDistanceType.SpacingPatternDistanceType)
        pin.quantityTwo = adsk.core.ValueInput.createByReal(1)   # sinon 3 par defaut = doublons
        hb.features.rectangularPatternFeatures.add(pin)
        return n

    hw_s = W2 + v('Debord_toit')
    g1 = demi_nervure(x_back + 2 * MM, hw_s, -1, 'Demi-nervure gare')
    g2 = demi_nervure(x_back + 2 * MM, hw_s, 1, 'Demi-nervure gare (droite)')
    n_g = reseau([g1, g2], x_back + 2 * MM, x_front - 2 * MM, 'gare')
    hw_gg = hw_g + v('Debord_toit')
    r1 = demi_nervure(xg_back + 2 * MM, hw_gg, -1, 'Demi-nervure garage')
    r2 = demi_nervure(xg_back + 2 * MM, hw_gg, 1, 'Demi-nervure garage (droite)')
    n_r = reseau([r1, r2], xg_back + 2 * MM, x_back - 2 * MM, 'garage')
    a_imprimer += [g1, r1]

    # ---- 2. pieds et tetes de poteaux -------------------------------------------
    xs = [v('X_col1'), v('X_col2'), x_back - 15 * MM]
    rs = v('Col_D') / 2 + 0.15 * MM                     # alesage du tube (jeu 0,15)
    # pied : collerette D36 x 3 + douille D22 x 15, 3 trous de vis a bois D3,5
    pl0 = hb.xYConstructionPlane
    skp = hb.sketches.add(pl0)
    skp.name = 'Pieds - collerettes'
    for xc in xs:
        skp.sketchCurves.sketchCircles.addByCenterRadius(P(xc, 0), 18 * MM)
    pieds = []
    for i in range(skp.profiles.count):
        pieds.append(extr(hb, skp.profiles.item(i), 3 * MM, 'Pied de poteau').bodies.item(0))
    pl3 = plan_offset(hb, hb.xYConstructionPlane, 3 * MM, 'Pieds - douilles')
    skd = hb.sketches.add(pl3)
    skd.name = 'Pieds - douilles'
    for xc in xs:
        skd.sketchCurves.sketchCircles.addByCenterRadius(P(xc, 0), 11 * MM)
        skd.sketchCurves.sketchCircles.addByCenterRadius(P(xc, 0), rs)
    for p in skd.profiles:
        if p.profileLoops.count == 2:
            d = extr(hb, p, 15 * MM, 'tmp').bodies.item(0)
            cx = (d.boundingBox.minPoint.x + d.boundingBox.maxPoint.x) / 2
            cible = min(pieds, key=lambda b: abs((b.boundingBox.minPoint.x + b.boundingBox.maxPoint.x) / 2 - cx))
            oc = adsk.core.ObjectCollection.create()
            oc.add(d)
            ci = hb.features.combineFeatures.createInput(cible, oc)
            ci.operation = adsk.fusion.FeatureOperations.JoinFeatureOperation
            hb.features.combineFeatures.add(ci)
    skv = hb.sketches.add(pl0)
    skv.name = 'Pieds - trous de vis'
    for xc in xs:
        for kk in range(3):
            a = math.radians(90 + 120 * kk)
            skv.sketchCurves.sketchCircles.addByCenterRadius(
                P(xc + 14.5 * MM * math.cos(a), 14.5 * MM * math.sin(a)), 1.75 * MM)
    trous = adsk.core.ObjectCollection.create()
    for p in skv.profiles:
        trous.add(p)
    ein = hb.features.extrudeFeatures.createInput(trous, adsk.fusion.FeatureOperations.CutFeatureOperation)
    ein.setDistanceExtent(False, adsk.core.ValueInput.createByReal(5 * MM))
    ein.participantBodies = pieds
    hb.features.extrudeFeatures.add(ein)
    a_imprimer.append(pieds[0])

    # tete : douille D22 x 15 (vers le bas) + plateau 24 x 22 x 3 + berceau en U pour la poutre
    z_pl = z_p - 3 * MM
    pld = plan_offset(hb, hb.xYConstructionPlane, z_pl - 15 * MM, 'Tetes - douilles')
    skt = hb.sketches.add(pld)
    skt.name = 'Tetes - douilles'
    for xc in xs:
        skt.sketchCurves.sketchCircles.addByCenterRadius(P(xc, 0), 11 * MM)
        skt.sketchCurves.sketchCircles.addByCenterRadius(P(xc, 0), rs)
    tetes = []
    for p in skt.profiles:
        if p.profileLoops.count == 2:
            tetes.append(extr(hb, p, 15 * MM, 'Tete de poteau').bodies.item(0))
    plp = plan_offset(hb, hb.xYConstructionPlane, z_pl, 'Tetes - plateaux')
    skq = hb.sketches.add(plp)
    skq.name = 'Tetes - plateaux et berceaux'
    wi = c / 2 + 0.15 * MM                                   # demi-largeur interieure du berceau
    for xc in xs:
        skq.sketchCurves.sketchLines.addTwoPointRectangle(P(xc - 12 * MM, -11 * MM), P(xc + 12 * MM, 11 * MM))
    for i in range(skq.profiles.count):
        pr = skq.profiles.item(i)
        cx = pr.areaProperties().centroid.x
        cible = min(tetes, key=lambda b: abs((b.boundingBox.minPoint.x + b.boundingBox.maxPoint.x) / 2 - cx))
        extr(hb, pr, 3 * MM, None, op=adsk.fusion.FeatureOperations.JoinFeatureOperation, part=[cible])
    plu = plan_offset(hb, hb.xYConstructionPlane, z_p, 'Tetes - joues')
    sku = hb.sketches.add(plu)
    sku.name = 'Tetes - joues du berceau'
    for xc in xs:
        for s in (-1, 1):
            sku.sketchCurves.sketchLines.addTwoPointRectangle(
                P(xc - 12 * MM, s * wi), P(xc + 12 * MM, s * (wi + 3 * MM)))
    for i in range(sku.profiles.count):
        pr = sku.profiles.item(i)
        cx = pr.areaProperties().centroid.x
        cible = min(tetes, key=lambda b: abs((b.boundingBox.minPoint.x + b.boundingBox.maxPoint.x) / 2 - cx))
        extr(hb, pr, 8 * MM, None, op=adsk.fusion.FeatureOperations.JoinFeatureOperation, part=[cible])
    # trou M3 horizontal a travers les joues et la poutre
    skm = hb.sketches.add(hb.xZConstructionPlane)        # plan Y = 0, perce les 2 joues
    skm.name = 'Tetes - trous M3'
    for xc in xs:
        skm.sketchCurves.sketchCircles.addByCenterRadius(
            skm.modelToSketchSpace(P(xc, 0, z_p + 4.5 * MM)), 1.6 * MM)
    tm = adsk.core.ObjectCollection.create()
    for p in skm.profiles:
        tm.add(p)
    ein = hb.features.extrudeFeatures.createInput(tm, adsk.fusion.FeatureOperations.CutFeatureOperation)
    ein.setSymmetricExtent(adsk.core.ValueInput.createByReal(2 * (wi + 4 * MM)), True)
    ein.participantBodies = tetes
    hb.features.extrudeFeatures.add(ein)
    a_imprimer.append(tetes[0])

    # ---- 3. STL ----------------------------------------------------------------
    os.makedirs(DOSSIER_STL, exist_ok=True)
    em = design.exportManager
    for b in a_imprimer:
        o = em.createSTLExportOptions(b, os.path.join(DOSSIER_STL, b.name.replace(' ', '_') + '.stl'))
        o.meshRefinement = adsk.fusion.MeshRefinementSettings.MeshRefinementHigh
        em.execute(o)

    # largeur developpee du vitrage (feuille PET a decouper)
    def dev(hw):
        return 2 * (z_t - R - z_e) + math.pi * R + 2 * (hw - R)
    print('Nervures : gare {} x 2 demi, garage {} x 2 demi, pas {:.0f} mm'.format(
        n_g, n_r, v('Pas_nervures') / MM))
    bb = g1.boundingBox
    print('Demi-nervure gare : {:.1f} x {:.1f} x {:.1f} mm'.format(
        (bb.maxPoint.y - bb.minPoint.y) / MM, (bb.maxPoint.z - bb.minPoint.z) / MM,
        (bb.maxPoint.x - bb.minPoint.x) / MM))
    print('Vitrage PET a decouper : gare {:.0f} x {:.0f} mm, garage {:.0f} x {:.0f} mm'.format(
        dev(hw_s) / MM, (x_front - x_back) / MM, dev(hw_gg) / MM, (x_back - xg_back) / MM))
    print('Tubes D16 : 3 x {:.0f} mm'.format((z_p - 6 * MM) / MM))
    print('STL :', ', '.join(b.name for b in a_imprimer))
