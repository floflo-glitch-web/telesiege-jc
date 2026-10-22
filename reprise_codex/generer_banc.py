"""Banc MANUEL reglable pour mise au point du rail JC, sans inventer la pince.

La recette de solides est partagee par l'export STL hors Fusion et le constructeur
Fusion. Les petits profils de contact restent des lamelles metalliques a ajuster.
"""
from pathlib import Path
import json
import math
import numpy as np
import manifold3d as mf
import trimesh

BASE = Path(__file__).resolve().parent
SORTIE = BASE/'banc_essai'


def box(x,y,z,dx,dy,dz,op='add'):
    return dict(type='box',origin=[x,y,z],size=[dx,dy,dz],operation=op)


def cyl(x,y,z,r,h,axis='Z',op='cut'):
    return dict(type='cylinder',origin=[x,y,z],radius=r,height=h,axis=axis,operation=op)


def recette():
    base=[box(0,0,0,180,140,6)]
    for x in (28,152):
        base += [box(x-1.75,25,-1,3.5,90,8,'cut'),
                 cyl(x,25,-1,1.75,8),cyl(x,115,-1,1.75,8)]
    for x in (8,172):
        for y in (8,132): base.append(cyl(x,y,-1,2.2,8))
    pied=[box(0,0,0,20,32,5),box(0,0,5,20,5,155),
          box(0,5,5,3,18,22),box(17,5,5,3,18,22),
          cyl(10,22,-1,1.75,7),
          box(8.25,-1,100,3.5,7,45,'cut'),
          cyl(10,-1,100,1.75,7,'Y'),cyl(10,-1,145,1.75,7,'Y')]
    tete=[box(0,0,0,20,4,20),box(0,4,16,20,16,4),
          box(0,4,9,3,8,7),box(17,4,9,3,8,7),
          cyl(10,-1,10,1.75,6,'Y')]
    for x in (4,16): tete.append(cyl(x,13,15,1.2,6))
    instances=[dict(part='Socle',translation=[0,0,0],rotation_z=0)]
    for cx in (28,152):
        instances += [dict(part='Montant',translation=[cx-10,35,6],rotation_z=0),
                      dict(part='Montant',translation=[cx+10,105,6],rotation_z=180),
                      dict(part='Porte_lamelle',translation=[cx-10,40,120],rotation_z=0),
                      dict(part='Porte_lamelle',translation=[cx+10,100,120],rotation_z=180)]
    return dict(schema=1,unites='mm',titre='Banc MANUEL reglable JC - PROTOTYPE',
        statut='Pince non mesuree : lamelles et position a regler sur la vraie pince',
        parts={'Socle':base,'Montant':pied,'Porte_lamelle':tete},instances=instances,
        quantites={'Socle':1,'Montant':4,'Porte_lamelle':4},
        capacites=dict(encombrement_mm=[180,140,166],
            axe_rail_hauteur_mm=[116,161],note='Hauteur du dessus des porte-lamelles ; +/- epaisseur de la lamelle et des cales. Ajuster pour garder le repose-pieds au-dessus du socle.'),
        lamelles=dict(matiere='acier ou laiton, bords polis',exemple_mm=[156,8,0.5],
            statut="Exemple d'approvisionnement, largeur/profondeur de contact non determinees"))


def solid_from_ops(ops):
    res=None
    for o in ops:
        if o['type']=='box':
            s=mf.Manifold.cube(o['size'])
        else:
            s=mf.Manifold.cylinder(o['height'],o['radius'],o['radius'],96)
            if o['axis']=='Y': s=s.rotate((-90,0,0))
            if o['axis']=='X': s=s.rotate((0,90,0))
        s=s.translate(o['origin'])
        if res is None: res=s
        elif o['operation']=='cut': res=res-s
        else: res=res+s
    if res.status()!=mf.Error.NoError: raise RuntimeError(res.status())
    return res


def mesh(m):
    t=m.to_mesh()
    return trimesh.Trimesh(vertices=t.vert_properties[:,:3],faces=t.tri_verts,process=True)


def main():
    spec=recette()
    SORTIE.mkdir(exist_ok=True)
    (SORTIE/'banc_recette.json').write_text(json.dumps(spec,indent=2,ensure_ascii=False),'utf-8')
    meshes={}
    native={}
    rapport={}
    couleurs={'Socle':[168,180,193,255],'Montant':[37,99,235,255],'Porte_lamelle':[245,158,11,255]}
    for nom,ops in spec['parts'].items():
        native[nom]=solid_from_ops(ops)
        m=mesh(native[nom]); meshes[nom]=m
        assert m.is_watertight and m.volume>0, nom
        assert len(m.split())==1, nom+' : pieces deconnectees'
        m.export(SORTIE/(nom+'.stl'))
        rapport[nom]=dict(quantite=spec['quantites'][nom],volume_mm3=float(m.volume),
            dimensions_mm=m.extents.tolist(),ferme=bool(m.is_watertight),corps_connexes=len(m.split()))
    scene=trimesh.Scene()
    assembly=[]
    for i,o in enumerate(spec['instances']):
        s=native[o['part']].rotate((0,0,o['rotation_z'])).translate(o['translation'])
        assembly.append((f"{o['part']}_{i}",s))
        t=trimesh.transformations.rotation_matrix(math.radians(o['rotation_z']),[0,0,1])
        t[:3,3]=o['translation']
        m=meshes[o['part']].copy();m.apply_transform(t)
        m.visual.face_colors=couleurs[o['part']]
        scene.add_geometry(m,node_name=f"{o['part']}_{i}")
    # Test des volumes des pieces du montage du banc uniquement.
    collisions=[]
    for i,(na,a) in enumerate(assembly):
        for nb,b in assembly[i+1:]:
            vol=(a^b).volume()
            if vol>1e-4: collisions.append(dict(a=na,b=nb,volume_mm3=vol))
    assert not collisions,collisions
    rapport['montage']=dict(interferences=collisions,nb_pieces=len(assembly),
        portee='Banc sans vis, lamelles ni pince : ne valide pas le contact avec une pince JC')
    # Lames de reference ajoutees uniquement dans la vue, jamais proposees en STL plastique.
    for y in (49,83):
        lame=trimesh.creation.box(extents=[156,8,.5])
        lame.apply_translation([90,y+4,140.25]);lame.visual.face_colors=[180,185,190,255]
        scene.add_geometry(lame,node_name=f'Lamelle_metal_reference_{y}')
    scene.export(SORTIE/'banc_assemblage.glb')
    (SORTIE/'controle_banc.json').write_text(json.dumps(rapport,ensure_ascii=False,indent=2),'utf-8')
    # Vue isometrique legere, sans moteur de rendu externe.
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    fig=plt.figure(figsize=(10,7));ax=fig.add_subplot(projection='3d')
    for node in scene.geometry.values():
        c=np.asarray(node.visual.face_colors[0])/255
        ax.add_collection3d(Poly3DCollection(node.triangles,facecolors=[c],edgecolors='none',alpha=.98))
    ax.set(xlim=(-5,185),ylim=(-5,145),zlim=(0,175),xlabel='X (mm)',ylabel='Y (mm)',zlabel='Z (mm)')
    ax.set_box_aspect([190,150,175]);ax.view_init(elev=27,azim=-54)
    ax.set_title('Banc manuel JC : rails reglables en largeur et en hauteur\nLamelles metalliques representees a titre indicatif')
    fig.tight_layout();fig.savefig(SORTIE/'apercu_banc.png',dpi=150);plt.close(fig)
    print('Banc : 3 STL, 9 pieces, recette native Fusion, assemblage GLB ; volumes fermes, 0 interference entre pieces du banc.')


if __name__=='__main__': main()
