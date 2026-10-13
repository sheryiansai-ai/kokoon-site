import numpy as np, json, struct, sys, gzip, base64
sys.path.insert(0,'mesh'); from stl import *
def hard_normals(v,f,thresh_deg=32):
    fn=np.cross(v[f[:,1]]-v[f[:,0]],v[f[:,2]]-v[f[:,0]]); area=np.linalg.norm(fn,axis=1)+1e-12; fn/=area[:,None]
    cos_t=np.cos(np.radians(thresh_deg))
    corners=f.reshape(-1); face_of=np.repeat(np.arange(len(f)),3)
    order=np.argsort(corners,kind='stable'); corners=corners[order]; face_of=face_of[order]
    starts=np.searchsorted(corners,np.arange(len(v)+1))
    newpos=[]; newnrm=[]; newidx=np.zeros(len(f)*3,dtype=np.int64)
    for vi in range(len(v)):
        s,e=starts[vi],starts[vi+1]
        if s==e: continue
        fs=face_of[s:e]; ns=fn[fs]; ws=area[fs]
        clusters=[]  # (sum normal, member list)
        for k in range(len(fs)):
            placed=False
            for c in clusters:
                cn=c[0]/ (np.linalg.norm(c[0])+1e-12)
                if np.dot(cn,ns[k])>=cos_t: c[0]+=ns[k]*ws[k]; c[1].append(k); placed=True; break
            if not placed: clusters.append([ns[k]*ws[k],[k]])
        for c in clusters:
            nid=len(newpos); newpos.append(v[vi]); n=c[0]/(np.linalg.norm(c[0])+1e-12); newnrm.append(n)
            for k in c[1]: newidx[order[s+k]]=nid
    return np.array(newpos),np.array(newnrm),newidx.reshape(-1,3)
def build(path,cell,minfaces=50):
    tri=read_stl(path); v,f=merge(tri); k,lab,flab=components(v,f)
    sizes=np.bincount(flab); order=[i for i in np.argsort(-sizes) if sizes[i]>=minfaces]
    parts=[]
    for i in order:
        m=flab==i; fv=f[m]; used=np.unique(fv); remap=-np.ones(len(v),dtype=np.int64); remap[used]=np.arange(len(used))
        pv=v[used]; pf=remap[fv]
        c=cell if sizes[i]<150000 else cell*1.6
        pv,pf=cluster(pv,pf,c)
        pv,pn,pf=hard_normals(pv,pf)
        parts.append((pv,pn,pf))
    return parts
def pack(parts,out):
    meta=[]; blobs=[]
    for pv,pn,pf in parts:
        mn=pv.min(0); mx=pv.max(0); ext=np.maximum(mx-mn,1e-6)
        q=np.round((pv-mn)/ext*65535).astype(np.uint16)
        n8=np.clip(np.round(pn*127),-127,127).astype(np.int8)
        idx=pf.astype(np.uint16) if len(pv)<65536 else pf.astype(np.uint32)
        meta.append({'v':len(pv),'f':len(pf),'min':mn.round(3).tolist(),'max':mx.round(3).tolist(),'i32':int(idx.dtype==np.uint32)})
        blobs.append(q.tobytes()+n8.tobytes()+(b'\0' if len(pv)%2 else b'')+idx.tobytes())
    js=json.dumps(meta).encode()
    data=b'KKM2'+struct.pack('<I',len(js))+js+b''.join(blobs)
    open(out,'wb').write(data); open(out+'.b64','w').write(base64.b64encode(gzip.compress(data,9)).decode())
    print(out,'parts',len(parts),'faces',sum(len(p[2]) for p in parts),'bytes',len(data),'gz',len(gzip.compress(data,9)))
U='/root/.claude/uploads/ee76e161-46c9-511c-ab6f-6ae2f078eee8'
for name,fn,hi,lo in [('sentry','d45ecef6-Nerf_turret_for_ar.stl',1.0,2.4),('arm','364c8c17-robotic_arm_flora1.stl',0.6,1.4)]:
    pack(build(U+'/'+fn,hi),f'mesh/{name}.kkm'); pack(build(U+'/'+fn,lo),f'mesh/{name}_lo.kkm')
