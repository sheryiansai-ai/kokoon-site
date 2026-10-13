import numpy as np, json, struct, sys, gzip, base64
sys.path.insert(0,'tools/mesh'); from stl import *; from pack2 import hard_normals
def feature_edges(v,f,deg=28):
    fn=np.cross(v[f[:,1]]-v[f[:,0]],v[f[:,2]]-v[f[:,0]]); fn/=np.linalg.norm(fn,axis=1)[:,None]+1e-12
    e=np.concatenate([f[:,[0,1]],f[:,[1,2]],f[:,[2,0]]]); e=np.sort(e,axis=1); fid=np.tile(np.arange(len(f)),3)
    key=e[:,0]*len(v)+e[:,1]; order=np.argsort(key,kind='stable'); key=key[order]; fid=fid[order]; e=e[order]
    uk,start,cnt=np.unique(key,return_index=True,return_counts=True)
    out=[]
    one=cnt==1; out.append(e[start[one]])
    two=start[cnt==2]; n1=fn[fid[two]]; n2=fn[fid[two+1]]; cosang=np.einsum('ij,ij->i',n1,n2)
    sharp=cosang<np.cos(np.radians(deg)); out.append(e[two[sharp]])
    E=np.concatenate(out); return E
def build(path,cell,minfaces=50):
    tri=read_stl(path); v,f=merge(tri); k,lab,flab=components(v,f)
    sizes=np.bincount(flab); order=[i for i in np.argsort(-sizes) if sizes[i]>=minfaces]
    parts=[]
    for i in order:
        m=flab==i; fv=f[m]; used=np.unique(fv); remap=-np.ones(len(v),dtype=np.int64); remap[used]=np.arange(len(used))
        pv=v[used]; pf=remap[fv]; c=cell if sizes[i]<150000 else cell*1.6
        pv,pf=cluster(pv,pf,c)
        E=feature_edges(pv,pf); seg=pv[E]  # (n,2,3)
        pv2,pn,pf2=hard_normals(pv,pf)
        parts.append((pv2,pn,pf2,seg))
    return parts
def pack(parts,out):
    meta=[]; blobs=[]
    for pv,pn,pf,seg in parts:
        mn=pv.min(0); mx=pv.max(0); ext=np.maximum(mx-mn,1e-6)
        q=np.round((pv-mn)/ext*65535).astype(np.uint16); n8=np.clip(np.round(pn*127),-127,127).astype(np.int8)
        idx=pf.astype(np.uint16) if len(pv)<65536 else pf.astype(np.uint32)
        sq=np.round((np.clip(seg,mn,mx)-mn)/ext*65535).astype(np.uint16)
        meta.append({'v':len(pv),'f':len(pf),'s':len(seg),'min':mn.round(3).tolist(),'max':mx.round(3).tolist(),'i32':int(idx.dtype==np.uint32)})
        blobs.append(q.tobytes()+n8.tobytes()+(b'\0' if len(pv)%2 else b'')+idx.tobytes()+sq.tobytes())
    js=json.dumps(meta).encode(); data=b'KKM3'+struct.pack('<I',len(js))+js+b''.join(blobs)
    open(out,'wb').write(data); open(out+'.b64','w').write(base64.b64encode(gzip.compress(data,9)).decode())
    print(out,'parts',len(parts),'faces',sum(len(p[2]) for p in parts),'segs',sum(len(p[3]) for p in parts),'bytes',len(data),'gz',len(gzip.compress(data,9)))
U='assets/stl'
pack(build(U+'/sentry-x1_nerf_turret.stl',1.0),'mesh/sentry.wasm')
pack(build(U+'/shadow-arm_flora1.stl',0.6),'mesh/arm.wasm')
