# Kokoon Labs — Working Context (Oct 2026)

Source: founder brief v2.0, web-copy PDF v3, photos, videos and STL files shared 12 Oct 2026; HD product photos (Photos.zip) shared 13 Oct. Vertical of Sheryians, ~7–8 months of R&D. Independent consumer brand ("A Sheryians company" in legal lines only).

## Working preferences
- Discuss and agree on direction before building anything.
- Always show website work as an inline preview in chat. Don't make the user download files to see it.
- Review the public GitHub Pages URL in the desktop browser pane (emulate 1440×900; if the emulated view keeps shrinking, reset to "desktop" and set the size once). `window.kkLenis` is exposed on the page; `kkLenis.scrollTo(y,{immediate:true})` steps through the build chapter (window.scrollTo gets reverted by Lenis).
- Claude does not type the user's passwords. The user logs in to the lab platform manually in the pane; sessions expire after a few hours.
- Feedback history: draft 1 (lime/black, Chakra Petch, chamfers) = cheap, rejected. Draft 2 italic serif = too professional, pale → rejected. Draft 3 (13 Oct) = purple + yellow, young/electronics energy.

## PUBLIC SITE (the link the team uses)
- **https://sheryiansai-ai.github.io/kokoon-site/** — GitHub Pages from repo `sheryiansai-ai/kokoon-site` (user's own GitHub account). Branches `main` and `gh-pages` identical; Pages serves gh-pages.
- Deploy = `bash scratchpad/deploy.sh "message"` (copies home2 → /home/claude/kokoon-site incl. img/, img/p/, codelab.gif, mesh/*.wasm; wraps index.html in doctype/head; commits with required attribution; pushes main and merges into gh-pages). Live within ~1 minute.
- Artifact mirror (private, older): https://claude.ai/artifact/HeT7b4k1vwhXbdHHTqdMJc

## Decisions
- **Price:** ₹59,000 including GST.
- **Age:** no upper limit. Public wording only: "Designed for ages 14 and up. Younger makers can build alongside an adult." Never print 11/12/13.
- **Logo:** locked and registered. Purple + yellow. Brand primary = purple **#3324C4** (darker shade chosen 12 Oct), hover #271B9E, deep #200070; accent yellow #F5C400 (#FFE566 highlighter). Dark chapters #1A1140 / build pin #130C30. Logo png at home2/img/logo.png.
- **Names:** Sentry X1 (capstone 01, pan-tilt foam-dart turret), Rover Tank (capstone 02), Shadow Arm (capstone 03). Kokoon Core (ESP32-S3 brain board), Kokoon Code Lab (block editor → MicroPython), Kokoon Learn (LMS).
- **Type (draft 3):** Plus Jakarta Sans 700/800, −0.035em for headings and UI (Fauna Robotics uses the commercial "Matter"; Jakarta is the open stand-in). Unbounded 700 only for the accent words (purple on a yellow highlighter). DM Mono for labels, ruler, drawing callouts.
- **Motion (draft 3):** Lenis 1.1.18 smooth scroll (lerp .085), Metic-style drawn guide lines (hero frame, section rules with crosshair, fixed right-edge ruler with yellow marker + %), IntersectionObserver reveals.
- **Homepage order (draft 3):** Hero (photo of Core on plate) → 01 Why now (dark) → 02 Moments (photos) → 03 What changes at home → 04 Three machines (3D viewer) → The build (pinned 1500vh) → 05 The Core (photos) → 06 Hardware gallery → 07 Code Lab (recording) → 08 Box + price → 09 Is this right → 10 Reserve + FAQ → Closing.
- **The build chapter:** 0–.09 assembled hero (ghost "SENTRY X1" title) → .09–.30 explode with tumbling parts + labels → .30–.50 technical drawing (paper background, feature-edge lines, dashed bounding boxes with real mm dimensions, title block KL-SX1-01) → .50–.82 reassembly in three stages (base / motion / purpose) → .82–.93 powered on (pan/tilt tracks cursor, yellow ring light on barrel) → .93–1 camera dive + fade into the Core section. Chapter index top-left. Camera keyframes `KF` in index.html.
- Hand photo of the Core (old) not used; new HD photos are fine, incl. hands.

## Photos (home2/img/p/)
hero (hand placing Core on plate, 4:3), hand (Core held), project/project2 (Core + 4 modules wired on plate), hands2, core (portrait, Core in case), core2 (top view on plate), cell/cell2/cellside (red power pack / plate views), board-logo (Core with logo), plate.

## Code Lab recording
- Lab platform: https://test.kokoon.pre.pixxo.io → Classroom (test.kokoon.post.pixxo.io) → My projects → Open canvas (/editor). Palette items are HTML5-draggable; React Flow canvas. In the pane, native drag doesn't work; `kkDrop(name,x,y)` JS helper (dispatch dragstart/dragover/drop with a shared DataTransfer) adds a block. Clicking "Add sample block" adds a Print block.
- home2/img/codelab.gif (800×498, 4 keyframes crossfaded: empty canvas → Print block → Sensor palette → Touch Sensor added, code grows). A longer recording with servo + loop + connections is pending (session expired mid-capture).

## 3D assets
- Sentry X1: Nerf_turret_for_ar.stl, 14 parts → mesh/sentry.wasm (KKM3). Shadow Arm: robotic_arm_flora1.stl, 20 parts → mesh/arm.wasm. Rover: MODULAR_ROVER_VERSION_2.stl is a print plate of 724 loose parts — unusable; photo render used.
- Pipeline: scratchpad/mesh/stl.py, pack2.py, pack3.py (numpy/scipy only). KKM3 = KKM2 (uint16 positions, int8 hard-edge normals 32°, uint16/32 indices) + feature-edge line segments (28°) used for the drawing phase. Loader parseKKM() accepts KKM2/KKM3; geometry is centred per part so parts pivot on their own centre.
- Rendering: three.js r128 (cdnjs), PMREM studio env, MeshPhysicalMaterial, PCF soft shadows, ACES, sRGB→linear.
- Sentry part map: 0 turntable, 1 flywheel housing, 2 receiver, 3 base chassis, 4 top cover, 5 yoke, 6 pivot shaft, 7 support post, 8 magazine, 9 tilt cradle, 10 pan servo, 11 tilt servo, 12 barrel (points −x in model space), 13 side bracket. Extents in mm (e.g. base 202×202×48).

## Other deliverables
- Brand system artifact (still draft-1 look; update to draft 3): https://claude.ai/artifact/YN4hfVNpgBMbJkNU94TtPt
- Working files: scratchpad/home2/ (index.html, index.v2.html backup, img/, img/p/, mesh/). Site repo clone: /home/claude/kokoon-site.

## Open items
- Offer: PDF describes a ₹30,000 live-class programme; brief says ₹59k kit + LMS. Site keeps ₹59k kit + LMS with soft mentor mention.
- Rover Tank: need an assembled STL.
- Longer Code Lab recording (needs the user logged in to the lab).
- Brand system artifact → draft-3 direction.
- Reservation form has no backend (POST + Razorpay hook marked in index.html).
