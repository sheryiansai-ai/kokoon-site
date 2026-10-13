# STL → KKM3 mesh pipeline

Pure numpy/scipy (no trimesh). Produces the compact binary meshes the site loads (`mesh/*.wasm`).

- `stl.py` — binary STL parse, vertex merge, connected components (= parts), vertex-clustering decimation.
- `pack2.py` — hard-edge normal splitting (32°) and the KKM2 packer.
- `pack3.py` — adds feature-edge line segments (28°) for the technical-drawing phase; writes `KKM3`.

Run from the repo root (edit the input paths at the bottom of pack3.py):

    python3 -I tools/mesh/pack3.py

Format KKM3: magic `KKM3`, uint32 JSON length, JSON meta per part `{v,f,s,min,max,i32}`, then per part:
uint16×3 quantised positions · int8×3 normals (+1 pad byte if v is odd) · uint16/uint32 indices · uint16×6 line segments.
Loader: `parseKKM()` in index.html (accepts KKM2 and KKM3). Files are named `.wasm` only so static hosts serve them.

Sentry X1 part indices (by component size): 0 turntable, 1 flywheel housing, 2 receiver, 3 base chassis, 4 top cover,
5 yoke, 6 pivot shaft, 7 support post, 8 magazine, 9 tilt cradle, 10 pan servo, 11 tilt servo, 12 barrel, 13 side bracket.
