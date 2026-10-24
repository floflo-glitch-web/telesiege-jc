# -*- coding: utf-8 -*-
# Gare debrayable JC 1:32 - etape 2 : poulie motrice, moyeu, moteur, chariot de tension.
# A lancer dans le document cree par JC_Gare_Debrayable (il lit H_cable, D_poulie...).
#
# Principes :
#   - la poulie est SUSPENDUE : moteur au-dessus, arbre vers le bas (rien sous la poulie)
#   - la poulie est abaissee de Delta_poulie sous le rail des pinces (le cable sort de la
#     machoire par le bas au debrayage, les pinces passent au-dessus de la poulie au contour)
#   - pieces imprimables SANS support : poulie en 2 demi-coques (gorge + logement de joint
#     torique), moyeu hexagonal separe, platine/chariot a plat
#   - moteur de reference : JGB37-520 12 V ~22 tr/min (reducteur D37, arbre D6 meplat 5,5,
#     sortie excentree de 7 mm, 6 trous M3 sur D31) - COTES A VERIFIER sur le moteur recu
# Repere local de la poulie : Z = 0 au plan du cable dans la gorge.

import math
import os
import adsk.core
import adsk.fusion

MM = 0.1
DOSSIER_STL = r'C:\Users\blang\Downloads\Gare debrayable JC\STL'

PARAMS = [
    ('Delta_poulie',  '10 mm',  'mm', 'Abaissement de la poulie sous le rail des pinces - A RECALER (pince)'),
    ('Joint_corde',   '3 mm',   'mm', 'Joint torique de gorge : corde 3 mm (ex. 145 x 3 NBR)'),
    ('Mot_D_red',     '37 mm',  'mm', 'JGB37-520 : diametre du reducteur'),
    ('Mot_L_red',     '24 mm',  'mm', 'JGB37-520 : longueur du reducteur (selon rapport)'),
    ('Mot_D_mot',     '33 mm',  'mm', 'JGB37-520 : diametre du moteur 520'),
    ('Mot_L_mot',     '22.7 mm', 'mm', 'JGB37-520 : longueur du moteur'),
    ('Mot_excentr',   '7 mm',   'mm', 'JGB37-520 : excentration de l arbre de sortie'),
    ('Mot_arbre_L',   '15.5 mm', 'mm', 'JGB37-520 : longueur d arbre'),
    ('Mot_PCD',       '31 mm',  'mm', 'JGB37-520 : cercle des 6 trous M3'),
    ('Course_tension', '30 mm', 'mm', 'Course du chariot de tension'),
]


def P(x, y, z=0.0):
    return adsk.core.Point3D.create(x, y, z)


def VI(s):
    return adsk.core.ValueInput.createByString(s)


def plan_z(comp, z_cm, nom):
    pin = comp.constructionPlanes.createInput()
    pin.setByOffset(comp.xYConstructionPlane, adsk.core.ValueInput.createByReal(z_cm))
    pl = comp.constructionPlanes.add(pin)
    pl.name = nom
    return pl


def revolve_rz(comp, pts_rz, nom):
    """Revolution autour de Z d un profil ferme donne en (r, z) en mm."""
    sk = comp.sketches.add(comp.xZConstructionPlane)
    sk.name = 'Profil ' + nom
    q = [sk.modelToSketchSpace(P(r * MM, 0, z * MM)) for r, z in pts_rz]
    ln = sk.sketchCurves.sketchLines
    first = ln.addByTwoPoints(q[0], q[1])
    prev = first
    for i in range(2, len(q)):
        prev = ln.addByTwoPoints(prev.endSketchPoint, q[i])
    ln.addByTwoPoints(prev.endSketchPoint, first.startSketchPoint)
    rin = comp.features.revolveFeatures.createInput(
        sk.profiles.item(0), comp.zConstructionAxis,
        adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    rin.setAngleExtent(False, VI('360 deg'))
    body = comp.features.revolveFeatures.add(rin).bodies.item(0)
    body.name = nom
    return body


def cut(comp, profils, plan_dist_mm, corps, symetrique=True):
    ein = comp.features.extrudeFeatures.createInput(
        profils, adsk.fusion.FeatureOperations.CutFeatureOperation)
    if symetrique:
        ein.setSymmetricExtent(adsk.core.ValueInput.createByReal(plan_dist_mm * MM), True)
    else:
        ein.setDistanceExtent(False, adsk.core.ValueInput.createByReal(plan_dist_mm * MM))
    ein.participantBodies = corps
    return comp.features.extrudeFeatures.add(ein)


def extrude_new(comp, profil, dist_mm, nom):
    f = comp.features.extrudeFeatures.addSimple(
        profil, adsk.core.ValueInput.createByReal(dist_mm * MM),
        adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    b = f.bodies.item(0)
    b.name = nom
    return b


def join(comp, cible, outils):
    oc = adsk.core.ObjectCollection.create()
    for t in outils:
        oc.add(t)
    cin = comp.features.combineFeatures.createInput(cible, oc)
    cin.operation = adsk.fusion.FeatureOperations.JoinFeatureOperation
    comp.features.combineFeatures.add(cin)


def hexagone(sk, af_mm):
    R = af_mm / math.sqrt(3) * MM
    ln = sk.sketchCurves.sketchLines
    pts = [P(R * math.cos(math.radians(30 + 60 * k)), R * math.sin(math.radians(30 + 60 * k)))
           for k in range(6)]
    first = ln.addByTwoPoints(pts[0], pts[1])
    prev = first
    for k in range(2, 6):
        prev = ln.addByTwoPoints(prev.endSketchPoint, pts[k])
    ln.addByTwoPoints(prev.endSketchPoint, first.startSketchPoint)


def plus_grand_profil(sk):
    best = None
    for p in sk.profiles:
        a = p.areaProperties().area
        if best is None or a > best[0]:
            best = (a, p)
    return best[1]


def run(_context):
    app = adsk.core.Application.get()
    design = adsk.fusion.Design.cast(app.activeProduct)
    root = design.rootComponent
    up = design.userParameters
    assert up.itemByName('H_cable') is not None, 'Lancer d abord JC_Gare_Debrayable'
    for nom, expr, unite, com in PARAMS:
        if up.itemByName(nom) is None:
            up.add(nom, VI(expr), unite, com)

    def mm(nom):
        return up.itemByName(nom).value / MM

    Rc = mm('D_poulie') / 2.0           # rayon de l axe du cable
    jc = mm('Joint_corde')
    z_poulie = mm('H_cable') - mm('Delta_poulie')

    # ---- 1. poulie : 2 demi-coques ------------------------------------
    m = adsk.core.Matrix3D.create()
    m.translation = adsk.core.Vector3D.create(0, 0, z_poulie * MM)
    occ = root.occurrences.addNewComponent(m)
    pc = occ.component
    pc.name = 'Poulie motrice D{:.0f}'.format(2 * Rc)

    r_joint_c = Rc - 1.0 - jc / 2.0      # axe du joint (cable pose sur le joint)
    r_fond = r_joint_c - jc / 2.0        # fond du logement de joint
    r_lev = Rc - 0.5                     # bord du logement / debut des flancs
    r_ext = Rc + 3.5                     # flasques
    r_jante = r_fond - 3.5               # interieur de la jante
    h_jante, h_voile, h_log = 4.0, 1.5, jc / 2.0 + 0.1
    r_moy = 18.0
    inf = [(0, -h_jante), (r_moy, -h_jante), (r_moy, -h_voile), (r_jante, -h_voile),
           (r_jante, -h_jante), (r_ext, -h_jante), (r_ext, -3.0), (r_lev, -h_log),
           (r_fond, -h_log), (r_fond, 0), (0, 0)]
    sup = [(r, -z) for r, z in reversed(inf)]
    b_inf = revolve_rz(pc, inf, 'Poulie demi-coque inferieure')
    b_sup = revolve_rz(pc, sup, 'Poulie demi-coque superieure')
    corps = [b_inf, b_sup]

    # rayons : 8 bras de 8 mm, fenetres entre r = 22 et r_jante - 4
    skf = pc.sketches.add(pc.xYConstructionPlane)
    skf.name = 'Fenetres et trous'
    r1, r2 = r_moy + 4.0, r_jante - 4.0
    skf.sketchCurves.sketchCircles.addByCenterRadius(P(0, 0), r1 * MM)
    skf.sketchCurves.sketchCircles.addByCenterRadius(P(0, 0), r2 * MM)
    for k in range(8):
        a = math.radians(45 * k)
        ux, uy, nx, ny = math.cos(a), math.sin(a), -math.sin(a), math.cos(a)
        for s in (-4.0, 4.0):
            p0 = P(((r1 - 3) * ux + s * nx) * MM, ((r1 - 3) * uy + s * ny) * MM)
            p1 = P(((r2 + 3) * ux + s * nx) * MM, ((r2 + 3) * uy + s * ny) * MM)
            skf.sketchCurves.sketchLines.addByTwoPoints(p0, p1)
    fen = adsk.core.ObjectCollection.create()
    for p in skf.profiles:
        ap = p.areaProperties()
        c = ap.centroid
        rr = math.hypot(c.x, c.y) / MM
        if ap.area / (MM * MM) > 600 and r1 + 5 < rr < r2 - 5:
            fen.add(p)
    assert fen.count == 8, 'fenetres trouvees : {}'.format(fen.count)
    cut(pc, fen, 30, corps)

    # trous d assemblage M3 sur 4 bras + hexagone du moyeu
    skt = pc.sketches.add(pc.xYConstructionPlane)
    skt.name = 'Trous M3 + hexagone'
    for k in range(4):
        a = math.radians(90 * k)
        skt.sketchCurves.sketchCircles.addByCenterRadius(
            P(40 * math.cos(a) * MM, 40 * math.sin(a) * MM), 1.6 * MM)
    hexagone(skt, 16.3)
    tous = adsk.core.ObjectCollection.create()
    for p in skt.profiles:
        tous.add(p)
    cut(pc, tous, 30, corps)

    # ---- 2. moyeu hexagonal (imprime debout sur sa collerette) -----------
    z_boss = 12.0                         # haut du moyeu
    pl_bas = plan_z(pc, -6.0 * MM, 'Moyeu bas')
    skc = pc.sketches.add(pl_bas)
    skc.name = 'Moyeu collerette'
    skc.sketchCurves.sketchCircles.addByCenterRadius(P(0, 0), 13.0 * MM)
    hub = extrude_new(pc, skc.profiles.item(0), 2.0, 'Moyeu')
    pl_h = plan_z(pc, -4.0 * MM, 'Moyeu hexagone')
    skh = pc.sketches.add(pl_h)
    skh.name = 'Moyeu hexagone'
    hexagone(skh, 16.0)
    hx = extrude_new(pc, skh.profiles.item(0), 8.0, 'tmp hex')
    pl_b = plan_z(pc, 4.0 * MM, 'Moyeu bossage')
    skb = pc.sketches.add(pl_b)
    skb.name = 'Moyeu bossage'
    skb.sketchCurves.sketchCircles.addByCenterRadius(P(0, 0), 8.0 * MM)
    bs = extrude_new(pc, skb.profiles.item(0), z_boss - 4.0, 'tmp bossage')
    join(pc, hub, [hx, bs])

    # alesage en D (arbre D6, meplat 5,5) depuis le haut, sur 12 mm
    pl_t = plan_z(pc, z_boss * MM, 'Moyeu haut')
    skd = pc.sketches.add(pl_t)
    skd.name = 'Alesage D6'
    skd.sketchCurves.sketchCircles.addByCenterRadius(P(0, 0), 3.1 * MM)
    skd.sketchCurves.sketchLines.addByTwoPoints(P(2.6 * MM, -4 * MM), P(2.6 * MM, 4 * MM))
    pr = adsk.core.ObjectCollection.create()
    pr.add(plus_grand_profil(skd))
    ein = pc.features.extrudeFeatures.createInput(pr, adsk.fusion.FeatureOperations.CutFeatureOperation)
    ein.setDistanceExtent(False, adsk.core.ValueInput.createByReal(-12.0 * MM))
    ein.participantBodies = [hub]
    pc.features.extrudeFeatures.add(ein)

    # vis de pression M3 radiale (avant-trou 2,5) face au meplat
    sks = pc.sketches.add(pc.yZConstructionPlane)
    sks.name = 'Vis de pression'
    sks.sketchCurves.sketchCircles.addByCenterRadius(sks.modelToSketchSpace(P(0, 0, 7.0 * MM)), 1.25 * MM)
    ein = pc.features.extrudeFeatures.createInput(sks.profiles.item(0),
                                                  adsk.fusion.FeatureOperations.CutFeatureOperation)
    ein.setDistanceExtent(False, adsk.core.ValueInput.createByReal(10.0 * MM))
    ein.participantBodies = [hub]
    pc.features.extrudeFeatures.add(ein)

    # ---- 3. moteur (gabarit) + platine / chariot de tension --------------
    z_face = z_boss + 4.0                 # face du reducteur (platine 3 mm + jeu 1 mm)
    ex = mm('Mot_excentr')
    gm = adsk.core.Matrix3D.create()
    gm.translation = adsk.core.Vector3D.create(0, 0, z_poulie * MM)
    occm = root.occurrences.addNewComponent(gm)
    mc = occm.component
    mc.name = 'Moteur JGB37-520 (gabarit)'

    def cylindre(comp, z0, h, r, cx, nom):
        pl = plan_z(comp, z0 * MM, nom)
        sk = comp.sketches.add(pl)
        sk.name = nom
        sk.sketchCurves.sketchCircles.addByCenterRadius(P(cx * MM, 0), r * MM)
        return extrude_new(comp, sk.profiles.item(0), h, nom)

    cylindre(mc, z_face, mm('Mot_L_red'), mm('Mot_D_red') / 2, ex, 'Reducteur')
    cylindre(mc, z_face + mm('Mot_L_red'), mm('Mot_L_mot'), mm('Mot_D_mot') / 2, ex, 'Moteur 520')
    # arbre D6 avec son meplat (5,5 mm sur plat) cote +X
    pla = plan_z(mc, (z_face - mm('Mot_arbre_L')) * MM, 'Arbre D6')
    ska = mc.sketches.add(pla)
    ska.name = 'Arbre D6 meplat'
    ska.sketchCurves.sketchCircles.addByCenterRadius(P(0, 0), 3.0 * MM)
    ska.sketchCurves.sketchLines.addByTwoPoints(P(2.5 * MM, -4 * MM), P(2.5 * MM, 4 * MM))
    extrude_new(mc, plus_grand_profil(ska), mm('Mot_arbre_L'), 'Arbre D6')

    # ---- 3 bis. cable reel en gare : il descend de Delta_poulie vers la poulie ----------
    gb = None
    for o in root.occurrences:
        if o.component.name == 'Gabarits volumes':
            gb = o.component
    if gb is not None:
        for b in list(gb.bRepBodies):
            if b.name in ('Poulie (gabarit)', 'Cable 2 mm'):
                gb.features.removeFeatures.add(b)
        R_bat = up.itemByName('D_poulie').value / 2 + up.itemByName('Marge_arr').value
        x_front = up.itemByName('L_gare').value - R_bat
        x_ligne = x_front + 4.0
        Hc = up.itemByName('H_cable').value
        zp = z_poulie * MM
        rc = Rc * MM
        L_desc = 6.0                                        # descente sur 60 mm
        x_arr = x_front - up.itemByName('L_entree').value  # fin du debrayage (arrivee)
        x_dep = up.itemByName('L_quai').value + up.itemByName('L_lanceur').value  # debut embrayage
        plc = gb.constructionPlanes.createInput()
        plc.setByOffset(gb.xYConstructionPlane, adsk.core.ValueInput.createByReal(zp))
        plz = gb.constructionPlanes.add(plc)
        plz.name = 'Plan de la poulie'
        skc = gb.sketches.add(plz)
        skc.name = 'Cable en gare (3D)'
        q = lambda x, y, z: skc.modelToSketchSpace(P(x, y, z))
        arc = skc.sketchCurves.sketchArcs.addByCenterStartSweep(q(0, 0, zp), q(0, rc, zp), math.pi)
        ln = skc.sketchCurves.sketchLines
        for depart, s, xb in ((arc.startSketchPoint, 1, x_dep), (arc.endSketchPoint, -1, x_arr)):
            l1 = ln.addByTwoPoints(depart, q(xb - L_desc, s * rc, zp))
            l2 = ln.addByTwoPoints(l1.endSketchPoint, q(xb, s * rc, Hc))
            ln.addByTwoPoints(l2.endSketchPoint, q(x_ligne, s * rc, Hc))
        pin = gb.features.pipeFeatures.createInput(
            gb.features.createPath(arc, True), adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        pin.sectionSize = adsk.core.ValueInput.createByString('Cable_d')
        gb.features.pipeFeatures.add(pin).bodies.item(0).name = 'Cable 2 mm (en gare)'

    occk = root.occurrences.addNewComponent(gm)
    kc = occk.component
    kc.name = 'Chariot de tension'
    pl_p = plan_z(kc, (z_face - 3.0) * MM, 'Platine')
    skp = kc.sketches.add(pl_p)
    skp.name = 'Platine moteur'
    skp.sketchCurves.sketchLines.addTwoPointRectangle(P(-35 * MM, -31 * MM), P(35 * MM, 31 * MM))
    plat = extrude_new(kc, skp.profiles.item(0), 3.0, 'Chariot de tension')
    skq = kc.sketches.add(pl_p)
    skq.name = 'Trous platine'
    circ = skq.sketchCurves.sketchCircles
    circ.addByCenterRadius(P(0, 0), 6.25 * MM)                       # bossage de centrage
    for k in range(6):
        a = math.radians(30 + 60 * k)
        circ.addByCenterRadius(P((ex + mm('Mot_PCD') / 2 * math.cos(a)) * MM,
                                 mm('Mot_PCD') / 2 * math.sin(a) * MM), 1.6 * MM)
    circ.addByCenterRadius(P(-30 * MM, 0), 1.6 * MM)                  # accroche du ressort
    tr = adsk.core.ObjectCollection.create()
    for p in skq.profiles:
        tr.add(p)
    cut(kc, tr, 20, [plat])
    # 2 fourreaux de guidage (tige acier D4) le long de X, poses sur la platine
    pl_g = kc.constructionPlanes.createInput()
    pl_g.setByOffset(kc.yZConstructionPlane, adsk.core.ValueInput.createByReal(-35 * MM))
    plg = kc.constructionPlanes.add(pl_g)
    plg.name = 'Fourreaux'
    skg = kc.sketches.add(plg)
    skg.name = 'Fourreaux D9 / D4,3'
    zg = z_face + 3.5                     # enfonce de 1 mm dans la platine (fusion propre)
    for s in (-26.0, 26.0):
        c = skg.modelToSketchSpace(P(-35 * MM, s * MM, zg * MM))
        skg.sketchCurves.sketchCircles.addByCenterRadius(c, 4.5 * MM)
        skg.sketchCurves.sketchCircles.addByCenterRadius(c, 2.15 * MM)
    anneaux = adsk.core.ObjectCollection.create()
    for p in skg.profiles:
        if p.profileLoops.count == 2:
            anneaux.add(p)
    assert anneaux.count == 2, 'anneaux : {}'.format(anneaux.count)
    fin = kc.features.extrudeFeatures.createInput(anneaux, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    fin.setDistanceExtent(False, adsk.core.ValueInput.createByReal(70 * MM))
    ff = kc.features.extrudeFeatures.add(fin)
    join(kc, plat, [ff.bodies.item(i) for i in range(ff.bodies.count)])

    # ---- 4. exports STL des pieces imprimables ----------------------------
    os.makedirs(DOSSIER_STL, exist_ok=True)
    em = design.exportManager
    sorties = []
    for b in list(pc.bRepBodies) + list(kc.bRepBodies):
        f = os.path.join(DOSSIER_STL, b.name.replace(' ', '_') + '.stl')
        o = em.createSTLExportOptions(b, f)
        o.meshRefinement = adsk.fusion.MeshRefinementSettings.MeshRefinementHigh
        em.execute(o)
        sorties.append(f)

    app.activeViewport.fit()
    print('Poulie : axe du cable D{:.1f}, joint corde {:.1f} (axe r={:.2f}, fond r={:.2f}), flasques D{:.1f}'.format(
        2 * Rc, jc, r_joint_c, r_fond, 2 * r_ext))
    print('Plan de la poulie a Z = {:.1f} mm ; face reducteur a Z = {:.1f} mm ; haut moteur a Z = {:.1f} mm'.format(
        z_poulie, z_poulie + z_face, z_poulie + z_face + mm('Mot_L_red') + mm('Mot_L_mot')))
    print('Toit a {:.1f} mm'.format(mm('H_toit')))
    for b in list(pc.bRepBodies) + list(kc.bRepBodies):
        bb = b.boundingBox
        print('  {:32s} {:.1f} x {:.1f} x {:.1f} mm, volume {:.1f} cm3'.format(
            b.name, (bb.maxPoint.x - bb.minPoint.x) / MM, (bb.maxPoint.y - bb.minPoint.y) / MM,
            (bb.maxPoint.z - bb.minPoint.z) / MM, b.volume))
    print('STL :', len(sorties), 'fichiers dans', DOSSIER_STL)
