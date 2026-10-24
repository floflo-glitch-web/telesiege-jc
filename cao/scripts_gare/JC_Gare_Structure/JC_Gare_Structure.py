# -*- coding: utf-8 -*-
# Gare debrayable JC 1:32 - etape 3 : charpente + toit R1.
# A lancer apres JC_Gare_Debrayable puis JC_Gare_Mecanique (meme document).
#
# Regles de degagement (sieges JC ~120 x 60 mm, voie 155 mm) :
#   - en ligne droite, le seul couloir libre est au centre (|y| < 17,5 mm) : poteaux ronds D16
#     au milieu, a 77,5 mm du cable (> 65 mm conseilles sur Alpinforum)
#   - au contour, l interieur des sieges passe a 17,5 mm de l axe SOUS la poulie : rien en dessous,
#     tout est suspendu a une poutre centrale au-dessus du moteur
#   - les brides des tiges du chariot restent a < 67 mm de l axe (pinces a ~77,5 mm au contour)
# Achats : poutre = tube alu carre 15 x 15, poteaux = tube alu rond D16, tiges acier D4.

import math
import os
import adsk.core
import adsk.fusion

MM = 0.1
DOSSIER_STL = r'C:\Users\blang\Downloads\Gare debrayable JC\STL'

PARAMS = [
    ('Z_poutre',     '181 mm', 'mm', 'Dessous de la poutre centrale (au-dessus du moteur)'),
    ('Poutre_c',     '15 mm',  'mm', 'Poutre centrale : tube alu carre 15 x 15'),
    ('Col_D',        '16 mm',  'mm', 'Poteaux : tube alu rond D16'),
    ('X_col1',       '250 mm', 'mm', 'Poteau central 1 (entre les voies)'),
    ('X_col2',       '520 mm', 'mm', 'Poteau central 2 (entre les voies)'),
    ('X_bride',      '56 mm',  'mm', 'Brides des tiges du chariot, de part et d autre de l axe'),
    ('Tige_D',       '4 mm',   'mm', 'Tiges acier du chariot de tension'),
    ('Tige_L',       '130 mm', 'mm', 'Longueur des tiges'),
    ('Z_avant_toit', '150 mm', 'mm', 'Bas des pans du toit R1 (sieges a < 90 mm)'),
    ('R_toit',       '45 mm',  'mm', 'Rayon des aretes arrondies du toit R1'),
    ('Ep_toit',      '0.5 mm', 'mm', 'Vitrage du toit : feuille PET transparente 0,5 mm'),
    ('Debord_toit',  '5 mm',   'mm', 'Debord du toit au-dela des murs'),
]


def P(x, y, z=0.0):
    return adsk.core.Point3D.create(x, y, z)


def plan_offset(comp, base, d_cm, nom):
    pin = comp.constructionPlanes.createInput()
    pin.setByOffset(base, adsk.core.ValueInput.createByReal(d_cm))
    pl = comp.constructionPlanes.add(pin)
    pl.name = nom
    return pl


def extr(comp, profils, d_cm, nom=None, op=adsk.fusion.FeatureOperations.NewBodyFeatureOperation,
         participants=None):
    ein = comp.features.extrudeFeatures.createInput(profils, op)
    ein.setDistanceExtent(False, adsk.core.ValueInput.createByReal(d_cm))
    if participants:
        ein.participantBodies = participants
    f = comp.features.extrudeFeatures.add(ein)
    if nom and f.bodies.count:
        f.bodies.item(0).name = nom
    return f


def run(_context):
    app = adsk.core.Application.get()
    design = adsk.fusion.Design.cast(app.activeProduct)
    root = design.rootComponent
    up = design.userParameters
    assert up.itemByName('Delta_poulie') is not None, 'Lancer d abord JC_Gare_Mecanique'
    for nom, expr, unite, com in PARAMS:
        if up.itemByName(nom) is None:
            up.add(nom, adsk.core.ValueInput.createByString(expr), unite, com)

    def v(nom):
        return up.itemByName(nom).value      # cm

    R_bat = v('D_poulie') / 2 + v('Marge_arr')
    x_back, x_front = -R_bat, v('L_gare') - R_bat
    W2 = v('W_gare') / 2
    z_p = v('Z_poutre')
    c = v('Poutre_c')
    z_tige = v('H_cable') - v('Delta_poulie') + 19.5 * MM   # = axe des fourreaux du chariot
    y_tige = 26 * MM

    occ = root.occurrences.addNewComponent(adsk.core.Matrix3D.create())
    ch = occ.component
    ch.name = 'Charpente'

    # ---- poutre centrale -------------------------------------------------
    pl = plan_offset(ch, ch.xYConstructionPlane, z_p, 'Dessous poutre')
    sk = ch.sketches.add(pl)
    sk.name = 'Poutre centrale'
    sk.sketchCurves.sketchLines.addTwoPointRectangle(
        P(x_back - 23 * MM, -c / 2), P(x_front - 10 * MM, c / 2))
    extr(ch, sk.profiles.item(0), c, 'Poutre centrale (tube alu 15x15)')

    # ---- poteaux -----------------------------------------------------------
    skc = ch.sketches.add(plan_offset(ch, ch.xYConstructionPlane, 3 * MM, 'Bas des tubes'))
    skc.name = 'Poteaux'
    for xc in (v('X_col1'), v('X_col2'), x_back - 15 * MM):
        skc.sketchCurves.sketchCircles.addByCenterRadius(P(xc, 0), v('Col_D') / 2)
    noms = ['Poteau central 1 (tube D16)', 'Poteau central 2 (tube D16)', 'Poteau arriere (tube D16)']
    for i in range(skc.profiles.count):
        f = extr(ch, skc.profiles.item(i), z_p - 6 * MM)   # tube entre pied (3 mm) et tete (3 mm)
        b = f.bodies.item(0)
        xc = b.boundingBox.minPoint.x + v('Col_D') / 2
        b.name = noms[0] if abs(xc - v('X_col1')) < 0.1 else (noms[1] if abs(xc - v('X_col2')) < 0.1 else noms[2])

    # ---- brides des tiges (imprimables, a plat) -----------------------------
    brides = []
    for s, nom in ((1, 'Bride avant'), (-1, 'Bride arriere')):
        x0 = s * v('X_bride') - 3 * MM
        plb = plan_offset(ch, ch.yZConstructionPlane, x0, nom)
        skb = ch.sketches.add(plb)
        skb.name = nom
        q = lambda yy, zz: skb.modelToSketchSpace(P(x0, yy, zz))
        skb.sketchCurves.sketchLines.addTwoPointRectangle(q(-31 * MM, z_tige - 5.5 * MM), q(31 * MM, z_p))
        for yy in (-y_tige, y_tige):
            skb.sketchCurves.sketchCircles.addByCenterRadius(q(yy, z_tige), 2.05 * MM)
        skb.sketchCurves.sketchCircles.addByCenterRadius(q(0, z_tige), 1.6 * MM)   # ressort
        best = max(list(skb.profiles), key=lambda p: p.areaProperties().area)
        b = extr(ch, best, 6 * MM, nom).bodies.item(0)
        brides.append(b)
        # trou vertical M3 pour la fixation sous la poutre
        plh = plan_offset(ch, ch.xYConstructionPlane, z_p, nom + ' vis')
        skv = ch.sketches.add(plh)
        skv.name = nom + ' vis'
        skv.sketchCurves.sketchCircles.addByCenterRadius(P(s * v('X_bride'), 0), 1.6 * MM)
        extr(ch, skv.profiles.item(0), -10 * MM, op=adsk.fusion.FeatureOperations.CutFeatureOperation,
             participants=[b])

    # ---- tiges acier D4 ------------------------------------------------------
    plt = plan_offset(ch, ch.yZConstructionPlane, -v('Tige_L') / 2, 'Tiges')
    skt = ch.sketches.add(plt)
    skt.name = 'Tiges D4'
    for yy in (-y_tige, y_tige):
        skt.sketchCurves.sketchCircles.addByCenterRadius(
            skt.modelToSketchSpace(P(-v('Tige_L') / 2, yy, z_tige)), v('Tige_D') / 2)
    for i in range(skt.profiles.count):
        extr(ch, skt.profiles.item(i), v('Tige_L'), 'Tige acier D4 (achat)')

    # ---- toit R1 : coque arrondie, gare + garage ------------------------------
    occt = root.occurrences.addNewComponent(adsk.core.Matrix3D.create())
    tt = occt.component
    tt.name = 'Toit R1'
    z_e, z_t = v('Z_avant_toit'), v('H_toit')
    R, e = v('R_toit'), v('Ep_toit')

    def coque(x0, x1, hw, nom):
        plr = plan_offset(tt, tt.yZConstructionPlane, x0, nom)
        sk = tt.sketches.add(plr)
        sk.name = nom
        q = lambda yy, zz: sk.modelToSketchSpace(P(x0, yy, zz))
        L = sk.sketchCurves.sketchLines
        A = sk.sketchCurves.sketchArcs
        k = math.cos(math.radians(45))
        for s in (-1, 1):                                   # pans + aretes arrondies
            L.addByTwoPoints(q(s * hw, z_e), q(s * hw, z_t - R))
            A.addByThreePoints(q(s * hw, z_t - R), q(s * (hw - R + R * k), z_t - R + R * k),
                               q(s * (hw - R), z_t))
            L.addByTwoPoints(q(s * (hw - e), z_e), q(s * (hw - e), z_t - R))
            A.addByThreePoints(q(s * (hw - e), z_t - R),
                               q(s * (hw - R + (R - e) * k), z_t - R + (R - e) * k),
                               q(s * (hw - R), z_t - e))
            L.addByTwoPoints(q(s * hw, z_e), q(s * (hw - e), z_e))
        L.addByTwoPoints(q(-(hw - R), z_t), q(hw - R, z_t))
        L.addByTwoPoints(q(-(hw - R), z_t - e), q(hw - R, z_t - e))
        assert sk.profiles.count >= 1, 'profil du toit non ferme'
        pr = max(list(sk.profiles), key=lambda p: p.areaProperties().area)
        b = extr(tt, pr, x1 - x0, nom).bodies.item(0)
        b.opacity = 0.35
        return b

    hw_g = v('R_garage') + v('Siege_L') / 2 + 20 * MM
    x2 = x_back - v('Marge_gar')
    xg_back = x2 - v('L_garage') - v('R_garage') - v('Marge_gar') - v('Siege_P') / 2
    coque(x_back, x_front, W2 + v('Debord_toit'), 'Vitrage toit gare (PET 0,5 mm)')
    coque(xg_back, x_back, hw_g + v('Debord_toit'), 'Vitrage toit garage (PET 0,5 mm)')

    # ---- STL des pieces imprimables --------------------------------------------
    os.makedirs(DOSSIER_STL, exist_ok=True)
    em = design.exportManager
    for b in brides:
        o = em.createSTLExportOptions(b, os.path.join(DOSSIER_STL, b.name.replace(' ', '_') + '.stl'))
        o.meshRefinement = adsk.fusion.MeshRefinementSettings.MeshRefinementHigh
        em.execute(o)

    # ---- controles de degagement ------------------------------------------------
    rmax = 0.0
    for b in brides:
        bb = b.boundingBox
        for xx in (bb.minPoint.x, bb.maxPoint.x):
            for yy in (bb.minPoint.y, bb.maxPoint.y):
                rmax = max(rmax, math.hypot(xx, yy))
    print('Charpente + toit crees. Gare X {:.1f} -> {:.1f} mm'.format(x_back / MM, x_front / MM))
    print('Poutre a Z {:.0f}-{:.0f} mm, toit {:.0f}-{:.0f} mm'.format(
        z_p / MM, (z_p + c) / MM, z_e / MM, z_t / MM))
    print('Brides : rayon maxi {:.1f} mm (axe du cable a {:.1f} mm)'.format(rmax / MM, v('Voie_gare') / 2 / MM))
    print('Tiges a Z {:.1f} mm, y = +/-{:.0f} mm'.format(z_tige / MM, y_tige / MM))
    print('Jeu poteau central / interieur des sieges : {:.1f} mm'.format(
        (v('Voie_gare') / 2 - v('Siege_L') / 2 - v('Col_D') / 2) / MM))
    print('Jeu siege au contour / mur arriere : {:.1f} mm'.format(
        (R_bat - v('Voie_gare') / 2 - v('Siege_L') / 2) / MM))
