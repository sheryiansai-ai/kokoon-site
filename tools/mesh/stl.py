import numpy as np, struct, sys, json
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components

def read_stl(path):
    with open(path,'rb') as f:
        head=f.read(80); n=struct.unpack('<I',f.read(4))[0]
        data=np.frombuffer(f.read(n*50),dtype=np.uint8).reshape(n,50)
    tri=data[:,12:48].copy().view('<f4').reshape(n,3,3)
    return tri

def merge(tri,eps=1e-3):
    v=tri.reshape(-1,3)
    q=np.round(v/eps).astype(np.int64)
    uq,inv=np.unique(q,axis=0,return_inverse=True)
    verts=np.zeros((len(uq),3)); np.add.at(verts,inv,v); cnt=np.bincount(inv); verts/=cnt[:,None]
    faces=inv.reshape(-1,3)
    return verts,faces

def components(verts,faces):
    n=len(verts)
    a=np.concatenate([faces[:,0],faces[:,1],faces[:,2]]); b=np.concatenate([faces[:,1],faces[:,2],faces[:,0]])
    g=coo_matrix((np.ones(len(a)),(a,b)),shape=(n,n))
    k,lab=connected_components(g,directed=False)
    flab=lab[faces[:,0]]
    return k,lab,flab

def cluster(verts,faces,cell):
    q=np.floor(verts/cell).astype(np.int64)
    uq,inv=np.unique(q,axis=0,return_inverse=True)
    nv=np.zeros((len(uq),3)); np.add.at(nv,inv,verts); nv/=np.bincount(inv)[:,None]
    nf=inv[faces]
    ok=(nf[:,0]!=nf[:,1])&(nf[:,1]!=nf[:,2])&(nf[:,0]!=nf[:,2])
    nf=nf[ok]
    s=np.sort(nf,axis=1); _,ui=np.unique(s,axis=0,return_index=True); nf=nf[np.sort(ui)]
    used=np.unique(nf); remap=-np.ones(len(nv),dtype=np.int64); remap[used]=np.arange(len(used))
    return nv[used], remap[nf]

if __name__=='__main__':
    p=sys.argv[1]
    tri=read_stl(p); print('tris',len(tri))
    v,f=merge(tri); print('verts',len(v),'faces',len(f),'bounds',v.min(0).round(1),v.max(0).round(1))
    k,lab,flab=components(v,f); print('components',k)
    sizes=np.bincount(flab); order=np.argsort(-sizes)
    for i in order[:25]:
        m=flab==i; cv=v[np.unique(f[m])]
        print(' comp',i,'faces',sizes[i],'ext',(cv.max(0)-cv.min(0)).round(1),'min',cv.min(0).round(1),'max',cv.max(0).round(1))
