# -*- coding: utf-8 -*-
"""Script Fusion autonome : creer le banc depuis la recette de solides partagee."""
import json
import math
from pathlib import Path
from datetime import datetime
import traceback
import adsk.core
import adsk.fusion

MM = 0.1
BASE = Path(__file__).resolve().parents[1]


def primitive(comp, op):
    p = op['origin']
    if op['type']=='box':
        base=comp.xYConstructionPlane; axis=2
    else:
        axis={'X':0,'Y':1,'Z':2}[op['axis']]
        base=[comp.yZConstructionPlane,comp.xZConstructionPlane,comp.xYConstructionPlane][axis]
    normal=[base.geometry.normal.x,base.geometry.normal.y,base.geometry.normal.z][axis]
    pin=comp.constructionPlanes.createInput()
    pin.setByOffset(base,adsk.core.ValueInput.createByReal(p[axis]*MM/normal))
    plane=comp.constructionPlanes.add(pin)
    sk=comp.sketches.add(plane)
    pt=lambda xyz: sk.modelToSketchSpace(adsk.core.Point3D.create(*(v*MM for v in xyz)))
    if op['type']=='box':
        q=[p[0]+op['size'][0],p[1]+op['size'][1],p[2]]
        sk.sketchCurves.sketchLines.addTwoPointRectangle(pt(p),pt(q))
        length=op['size'][2]
    else:
        sk.sketchCurves.sketchCircles.addByCenterRadius(pt(p),op['radius']*MM)
        length=op['height']/normal
    ei=comp.features.extrudeFeatures.createInput(sk.profiles.item(0),
                            adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    ei.setDistanceExtent(False,adsk.core.ValueInput.createByReal(length*MM))
    body=comp.features.extrudeFeatures.add(ei).bodies.item(0)
    sk.isVisible=False;plane.isLightBulbOn=False
    return body


def run(context):
    app=adsk.core.Application.get()
    out=BASE
    rapport={'statut':'INCOMPLET','date':datetime.now().isoformat()}
    try:
        data=json.loads((out/'banc_recette.json').read_text('utf-8'))
        doc=app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
        doc.name='JC - banc manuel reglable - prototype'
        d=adsk.fusion.Design.cast(app.activeProduct)
        d.designType=adsk.fusion.DesignTypes.ParametricDesignType
        d.unitsManager.defaultLengthUnits='mm'
        root=d.rootComponent
        prototypes={};first_occ={};native={}
        for nom,ops in data['parts'].items():
            occ=root.occurrences.addNewComponent(adsk.core.Matrix3D.create())
            comp=occ.component;comp.name=nom
            cible=None
            for o in ops:
                b=primitive(comp,o)
                if cible is None:
                    cible=b
                else:
                    coll=adsk.core.ObjectCollection.create();coll.add(b)
                    ci=comp.features.combineFeatures.createInput(cible,coll)
                    ci.operation=(adsk.fusion.FeatureOperations.CutFeatureOperation if o['operation']=='cut'
                                  else adsk.fusion.FeatureOperations.JoinFeatureOperation)
                    comp.features.combineFeatures.add(ci)
            if comp.bRepBodies.count!=1:
                raise RuntimeError(nom+' : doit former un seul corps')
            comp.bRepBodies.item(0).name=nom
            prototypes[nom]=comp;first_occ[nom]=occ
            native[nom]={'volume_mm3':comp.bRepBodies.item(0).volume*1000}
        used=set()
        for o in data['instances']:
            nom=o['part'];m=adsk.core.Matrix3D.create()
            m.setToRotation(math.radians(o['rotation_z']),adsk.core.Vector3D.create(0,0,1),adsk.core.Point3D.create(0,0,0))
            m.translation=adsk.core.Vector3D.create(*(v*MM for v in o['translation']))
            if nom not in used:
                first_occ[nom].transform2=m;used.add(nom)
            else:
                root.occurrences.addExistingComponent(prototypes[nom],m)
        d.snapshots.add()
        if (out/'controle_banc.json').exists():
            offline=json.loads((out/'controle_banc.json').read_text('utf-8'))
            for nom,val in native.items():
                ref=offline[nom]['volume_mm3']
                val['ecart_relatif_volume']=abs(val['volume_mm3']-ref)/ref
                if val['ecart_relatif_volume']>0.01:
                    raise RuntimeError('Volume Fusion incoherent avec STL pour '+nom)
        stamp=datetime.now().strftime('%Y%m%d_%H%M%S')
        archive=out/('Banc_JC_'+stamp+'.f3d')
        if not d.exportManager.execute(d.exportManager.createFusionArchiveExportOptions(str(archive))):
            raise RuntimeError('Echec export archive locale du banc')
        rapport.update(statut='GENERE_DANS_FUSION',pieces=native,archive_locale=str(archive),
            limite='Banc seul : aucune compatibilite physique pince/came encore validee')
        app.activeViewport.fit()
        app.userInterface.messageBox('Banc manuel cree dans un nouveau document.\nArchive locale : '+str(archive))
    except Exception:
        rapport['erreur']=traceback.format_exc()
        app.userInterface.messageBox(rapport['erreur'])
    finally:
        (out/'rapport_execution_Fusion.json').write_text(json.dumps(rapport,ensure_ascii=False,indent=2),'utf-8')


def stop(context):
    pass
