# Kokoon Labs — website project

Pre-purchase website for **Kokoon Origin** (₹59,000 incl. GST robotics kit + Kokoon Learn LMS + Kokoon Code Lab) by Kokoon Labs, the robotics-education vertical of Sheryians. Owner: Adarsh (sheryiansai@gmail.com). This repo is both the **live site** (GitHub Pages) and the **working context** for Claude Code. Read this file fully before touching anything.

## Status (14 Oct 2026)
- Draft 3 of the homepage is live: https://sheryiansai-ai.github.io/kokoon-site/
- Adarsh's verdict: "20% done, moving in the right direction." Not happy with the font yet, and not happy with the landing page as a whole. Development is **paused for a strategy rethink** — see `docs/strategy-2026-10-14.md` before proposing any build.
- Working rule: **discuss and agree on direction before building.** Show work as a preview (open the HTML in a browser, screenshot it); don't make him download files to see it.
- He writes in Hinglish; replying in Hinglish is fine. Keep replies short, bottom line first.

## Repo layout
```
index.html            live homepage (self-contained: CSS + HTML + JS in one file; three.js r128 and Lenis from CDN)
img/                  site images; img/p/ = HD product photos (Oct 13 shoot); img/codelab.gif = Code Lab recording
mesh/                 sentry.wasm, arm.wasm = KKM3 binary meshes built from the STLs (named .wasm only so hosts serve them)
docs/context.md       detailed working context: decisions, colours, type, chapter timeline, part maps, open items
docs/strategy-2026-10-14.md  the direction discussion that paused development (parent-first, then kid; videos; fonts)
docs/brand-brief-v2.txt      founder's brand strategy brief (source of truth for positioning)
docs/web-copy-v3.txt/.pdf    website copy document (source of most on-page copy and the names)
tools/deploy.sh       commit + push main and gh-pages
tools/mesh/           STL → KKM3 pipeline (numpy/scipy only). See tools/mesh/README.md
assets/stl/           the two usable print files (Sentry X1 turret, Shadow Arm). Rover STL is a print plate, unusable.
archive/              draft 1 and draft 2 homepages, for reference only
```

## Deploy
`bash tools/deploy.sh "message"` — commits everything, pushes `main`, merges into `gh-pages`, pushes. Pages serves `gh-pages`; live in ~1 minute. Every edit the team should see goes through this; the public link never changes.

## How index.html is built
- One file. Sections in order: nav → hero → 01 Why now (dark) → 02 Moments → 03 What changes at home → 04 Three machines (3D viewer) → `#build` pinned chapter (1500vh) → 05 The Core → 06 Hardware gallery → 07 Code Lab → 08 Box + price → 09 Is this right → 10 Reserve + FAQ → closing → footer.
- Type: Plus Jakarta Sans (headings/UI), Unbounded (accent words only), DM Mono (labels). **Font is under review** — candidates in the strategy doc.
- Colour: purple `#3324C4` primary, yellow `#F5C400` accent, dark `#1A1140`, build pin `#130C30`, paper `#F4F2FB`. Logo is locked (img/logo.png).
- Motion: Lenis 1.1.18 smooth scroll (`window.kkLenis` is exposed — use `kkLenis.scrollTo(y,{immediate:true})` when scripting; plain `window.scrollTo` gets reverted), IntersectionObserver reveals (`.rv`), drawn section rules (`.sec.in::before`), fixed right ruler (`.ruler`/`.rulerm`).
- 3D: `parseKKM()` loads KKM2/KKM3; `assemble()` centres each part on its own pivot; `Studio()` = renderer + PMREM env + lights. Viewer in `#machines`; the big chapter in `#build` driven by scroll progress `p` 0–1:
  0–.09 assembled hero (ghost title) · .09–.30 explode + labels · .30–.50 technical drawing (paper, feature-edge lines, mm dimension boxes, title block) · .50–.82 reassembly in 3 stages (`WIN`) · .82–.93 powered on (pan/tilt tracks cursor, ring light on barrel) · .93–1 dive + `#fade`. Camera keyframes in `KF` = [t, distance×, height×, angle, look-at×, fov]. Sentry part map and extents are in docs/context.md.
- Reservation form has no backend; the hook point is marked `/* Connect to your backend here */`.

## Reviewing
Open `index.html` locally (any static server; `python3 -m http.server`) or the live URL. Check 1440×900 and 375×812. The build chapter is best checked by stepping `p` with `kkLenis.scrollTo(build.offsetTop + p*(build.offsetHeight-innerHeight),{immediate:true})`. Headless Playwright works for the non-3D sections; WebGL needs a real browser.

## Decisions that are settled (don't reopen without Adarsh)
- Price ₹59,000 incl. GST. Age wording: "Designed for ages 14 and up. Younger makers can build alongside an adult." Never print 11/12/13.
- Names: Sentry X1, Rover Tank, Shadow Arm, Kokoon Core, Kokoon Code Lab, Kokoon Learn. Legal line: "A Sheryians company".
- Logo locked; purple + yellow brand. Rejected looks: draft 1 (lime/black, chamfers — "cheap"), draft 2 italic serif ("too professional"), pale palettes.
- Parents buy a feeling: AI already writes the code, the future is hardware, "your child will build something real". Feeling first, product later.

## Open items
- Strategy rethink (parent-first → kid energy → parent pays); video plan; font choice. See strategy doc.
- Longer Code Lab recording (needs login to https://test.kokoon.pre.pixxo.io → Classroom → Open canvas; Adarsh logs in himself — never type his password).
- Rover Tank needs an assembled STL.
- Brand-system doc still reflects draft 1.
- Offer ambiguity: web-copy PDF describes a ₹30k live-class programme; brief says ₹59k kit + LMS. Site uses ₹59k kit + LMS.
