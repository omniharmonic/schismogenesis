/* anti-memes.is: the memetic field and the scroll story. No dependencies. */
(() => {
  "use strict";

  // ---- config: change these when the debate moves to a subdomain ----
  const CONFIG = {
    debateBase: "https://dialogos-fingerprint.vercel.app",
    surveyPath: "/",
    atlasPath: "/atlas",
    cardPath: "/people#", // + person id: their card, with a way to report a misreading
  };
  const LINKS = {
    survey: CONFIG.debateBase + CONFIG.surveyPath,
    atlas: CONFIG.debateBase + CONFIG.atlasPath,
  };

  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => Array.from(el.querySelectorAll(s));
  const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));
  const lerp = (a, b, t) => a + (b - a) * t;
  const ease = (t) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2);
  const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const safeUrl = (u) => (/^https?:\/\//i.test(u || "") ? u : "#");
  const reduceMQ = matchMedia("(prefers-reduced-motion: reduce)");
  let REDUCE = reduceMQ.matches;
  const finePointer = matchMedia("(pointer: fine)").matches;

  for (const a of $$("[data-link]")) {
    a.href = LINKS[a.dataset.link] || "#";
    if (a.dataset.link in LINKS) { a.target = "_blank"; a.rel = "noopener"; }
  }

  const css = getComputedStyle(document.documentElement);
  const tok = (n) => css.getPropertyValue(n).trim();
  const C = {
    ground: tok("--ground"), ground2: tok("--ground-2"), rule: tok("--rule"), rule2: tok("--rule-2"),
    ink: tok("--ink"), ink2: tok("--ink-2"), ink3: tok("--ink-3"), heat: tok("--heat"), recog: tok("--recog"),
    schools: [tok("--s1"), tok("--s2"), tok("--s3"), tok("--s4")], none: tok("--s0"),
  };
  const rgba = (hex, a) => {
    const h = hex.replace("#", "");
    const n = parseInt(h.length === 3 ? h.split("").map((c) => c + c).join("") : h, 16);
    return `rgba(${(n >> 16) & 255},${(n >> 8) & 255},${n & 255},${a})`;
  };

  // ---------------------------------------------------------------- data
  let DATA = null, QUOTES = null, quotesPromise = null;
  const byId = new Map();
  function loadQuotes() {
    if (!quotesPromise) {
      quotesPromise = fetch("map-quotes.json").then((r) => r.json()).then((q) => (QUOTES = q)).catch(() => (QUOTES = { stances: {}, voices: {} }));
    }
    return quotesPromise;
  }

  fetch("map-data.json").then((r) => r.json()).then(init).catch((e) => {
    console.warn("map data failed to load", e);
    $("#hint").textContent = "The live map didn't load. Reload the page to try again.";
  });

  function schoolColor(label) {
    const i = DATA.schools.findIndex((s) => s.label === label);
    return i >= 0 ? C.schools[i % C.schools.length] : C.none;
  }

  // ---------------------------------------------------------------- field
  const canvas = $("#field");
  const ctx = canvas.getContext("2d");
  let W = 0, H = 0, DPR = 1, TOP = 60;
  const nodes = [];
  let links = [], rivals = [], bfsTree = [];
  const pointer = { x: -1e4, y: -1e4, inside: false, down: false, drag: null, sx: 0, sy: 0, moved: 0 };
  let hover = null, selected = null;
  let scene = { key: "map", p: 0, el: null };
  const region = { x0: 0, x1: 0, y0: 0, y1: 0, init: false };
  const anim = { heat: 0, sep: 0, goat: 0, plural: 0, alpha: 1, rivalA: 0 };
  let schismStatement = null, centroid = {};
  let awake = false, lastT = 0, t0 = performance.now();

  function resize() {
    DPR = Math.min(window.devicePixelRatio || 1, 2);
    W = window.innerWidth; H = window.innerHeight;
    TOP = parseFloat(getComputedStyle($(".top")).height) || 60;
    canvas.width = Math.round(W * DPR); canvas.height = Math.round(H * DPR);
    canvas.style.width = W + "px"; canvas.style.height = H + "px";
    ctx.setTransform(DPR, 0, 0, DPR, 0, 0);
    wake();
  }

  function targetRegion(key) {
    const mobile = W < 760;
    const top = TOP + 18;
    if (mobile) {
      if (key === "map") return { x0: 14, x1: W - 14, y0: top + 6, y1: H * 0.44 };
      if (["contagion", "schism", "scapegoat", "plural"].includes(key)) return { x0: 18, x1: W - 18, y0: top + 10, y1: H * 0.5 };
      return { x0: 14, x1: W - 14, y0: top + 10, y1: H - 24 };
    }
    const gutter = clamp(W * 0.04, 16, 48);
    const right = W >= 1180 ? W - 170 : W - 60;
    if (key === "map") return { x0: Math.max(W * 0.44, gutter + 560), x1: right, y0: top + 16, y1: H - 70 };
    if (["contagion", "schism", "scapegoat", "plural"].includes(key)) return { x0: gutter + 460 + 70, x1: right, y0: top + 30, y1: H - 80 };
    return { x0: 60, x1: W - 60, y0: top + 10, y1: H - 40 };
  }

  function makeFace(img, color) {
    const S = 72;
    const c = document.createElement("canvas"); c.width = c.height = S;
    const x = c.getContext("2d");
    x.beginPath(); x.arc(S / 2, S / 2, S / 2, 0, Math.PI * 2); x.clip();
    // cover-fit
    const r = Math.max(S / img.naturalWidth, S / img.naturalHeight);
    const w = img.naturalWidth * r, h = img.naturalHeight * r;
    x.drawImage(img, (S - w) / 2, (S - h) / 2.6, w, h);
    if (!color) {
      const d = x.getImageData(0, 0, S, S), p = d.data;
      for (let i = 0; i < p.length; i += 4) {
        const l = 0.3 * p[i] + 0.59 * p[i + 1] + 0.11 * p[i + 2];
        const v = clamp((l - 128) * 1.12 + 118, 0, 255);
        p[i] = v * 0.86; p[i + 1] = v * 0.93; p[i + 2] = v * 1.02;
      }
      x.putImageData(d, 0, 0);
    }
    return c;
  }

  function buildGraph() {
    const P = DATA.people;
    const xs = P.map((p) => p.x), ys = P.map((p) => p.y);
    const minx = Math.min(...xs), maxx = Math.max(...xs), miny = Math.min(...ys), maxy = Math.max(...ys);
    P.forEach((p, i) => {
      const n = {
        i, p, id: p.id,
        mx: ((p.x - minx) / (maxx - minx || 1)) * 2 - 1,
        my: -(((p.y - miny) / (maxy - miny || 1)) * 2 - 1),
        x: W * 0.66 + (Math.random() - 0.5) * 20, y: H * 0.5 + (Math.random() - 0.5) * 20,
        vx: 0, vy: 0, tx: 0, ty: 0, alpha: 0, heat: 0, deg: 0, color: schoolColor(p.school),
        gray: null, full: null, order: 1e9, side: 0,
      };
      nodes.push(n); byId.set(p.id, n);
      if (p.face) {
        const img = new Image();
        img.decoding = "async";
        img.onload = () => { try { n.gray = makeFace(img, false); n.full = makeFace(img, true); wake(); } catch (e) { /* ignore */ } };
        img.src = p.face;
      }
    });
    links = DATA.links.map((l) => ({ a: byId.get(l.s), b: byId.get(l.t), w: l.w })).filter((l) => l.a && l.b);
    rivals = DATA.rivals.map((l) => ({ a: byId.get(l.s), b: byId.get(l.t), w: l.w })).filter((l) => l.a && l.b);
    for (const l of links) { l.a.deg++; l.b.deg++; }

    // contagion order: breadth-first from the best-connected person, through real agreement links
    const adj = new Map(nodes.map((n) => [n, []]));
    for (const l of links) { adj.get(l.a).push(l.b); adj.get(l.b).push(l.a); }
    const seed = nodes.slice().sort((a, b) => b.deg - a.deg)[0];
    let k = 0; const seen = new Set([seed]); const q = [seed]; seed.order = k++;
    while (q.length) {
      const u = q.shift();
      for (const v of adj.get(u)) if (!seen.has(v)) { seen.add(v); v.order = k++; v.parent = u; bfsTree.push({ a: u, b: v }); q.push(v); }
    }
    for (const n of nodes) if (!seen.has(n)) n.order = k++ + 3; // isolated people catch it last, out of nowhere
    const maxOrder = Math.max(...nodes.map((n) => n.order));
    for (const n of nodes) n.ord = n.order / maxOrder;

    // schism: the statement that splits the map most evenly
    let best = null, bestScore = -1;
    for (const st of DATA.statements) {
      const sides = DATA.sides[st.id] || {};
      const v = Object.values(sides);
      const yes = v.filter((a) => a > 0).length, no = v.filter((a) => a < 0).length;
      const score = Math.min(yes, no) + 0.01 * (yes + no);
      if (score > bestScore) { bestScore = score; best = { st, yes, no }; }
    }
    schismStatement = best;
    const sides = DATA.sides[best.st.id] || {};
    for (const n of nodes) n.side = sides[n.id] || 0;
    $("#sorter-q").textContent = "“" + best.st.text + "”";
    $("#sorter-yes").textContent = best.yes;
    $("#sorter-no").textContent = best.no;
    $("#sorter-off").textContent = nodes.length - best.yes - best.no;

    // layouts in a [-1, 1] box
    const sun = (list, cx, cy, spread) => {
      list.forEach((n, j) => {
        const a = j * 2.39996, r = spread * Math.sqrt((j + 0.5) / Math.max(list.length, 1));
        n._x = cx + Math.cos(a) * r; n._y = cy + Math.sin(a) * r;
      });
    };
    const yesL = nodes.filter((n) => n.side > 0), noL = nodes.filter((n) => n.side < 0), offL = nodes.filter((n) => !n.side);
    sun(yesL, -0.56, 0, 0.42); yesL.forEach((n) => { n.sx = n._x; n.sy = n._y; });
    sun(noL, 0.56, 0, 0.42); noL.forEach((n) => { n.sx = n._x; n.sy = n._y; });
    offL.forEach((n, j) => { const a = (j / offL.length) * Math.PI * 2 + 0.3; n.sx = Math.cos(a) * 1.04; n.sy = Math.sin(a) * 1.06; });

    // plural: each school around its own centre of mass on the map, pushed apart; thresholds in between
    centroid = {};
    DATA.schools.forEach((s) => {
      const m = s.members.map((id) => byId.get(id)).filter(Boolean);
      let cx = m.reduce((a, n) => a + n.mx, 0) / (m.length || 1), cy = m.reduce((a, n) => a + n.my, 0) / (m.length || 1);
      const d = Math.hypot(cx, cy) || 1; cx = (cx / d) * 0.62; cy = (cy / d) * 0.58;
      centroid[s.label] = { x: cx, y: cy, color: schoolColor(s.label), label: s.label, n: m.length };
    });
    // keep centroids from colliding
    const cs = Object.values(centroid);
    for (let it = 0; it < 60; it++) for (const a of cs) for (const b of cs) if (a !== b) {
      const dx = a.x - b.x, dy = a.y - b.y, d = Math.hypot(dx, dy) || 0.01;
      if (d < 0.95) { a.x += (dx / d) * 0.01; a.y += (dy / d) * 0.01; }
    }
    for (const s of DATA.schools) {
      const list = nodes.filter((n) => n.p.school === s.label);
      const c = centroid[s.label];
      sun(list, c.x, c.y, 0.12 + 0.05 * Math.sqrt(list.length));
      list.forEach((n) => { n.px = n._x; n.py = n._y; });
    }
    nodes.filter((n) => !centroid[n.p.school]).forEach((n) => {
      const bt = (n.p.between || []).map((l) => centroid[l]).filter(Boolean);
      if (bt.length >= 2) { n.px = (bt[0].x + bt[1].x) / 2 + (Math.random() - 0.5) * 0.08; n.py = (bt[0].y + bt[1].y) / 2 + (Math.random() - 0.5) * 0.08; n.threshold = true; }
      else { n.px = n.mx * 0.42; n.py = n.my * 0.42; }
    });

    // scapegoat ring angles
    nodes.forEach((n, j) => { n.ga = (j / nodes.length) * Math.PI * 2 + (j % 3) * 0.04; n.gj = j % 2 ? 0.74 : 1.0; });
    $("#ro-nodes").textContent = String(nodes.length);
  }

  function toScreen(x, y) {
    const cx = (region.x0 + region.x1) / 2, cy = (region.y0 + region.y1) / 2;
    const rx = (region.x1 - region.x0) / 2, ry = (region.y1 - region.y0) / 2;
    return [cx + x * rx, cy + y * ry];
  }
  function fromScreen(x, y) {
    const cx = (region.x0 + region.x1) / 2, cy = (region.y0 + region.y1) / 2;
    const rx = (region.x1 - region.x0) / 2 || 1, ry = (region.y1 - region.y0) / 2 || 1;
    return [(x - cx) / rx, (y - cy) / ry];
  }

  function nodeRadius() {
    const m = Math.min(region.x1 - region.x0, region.y1 - region.y0);
    return clamp(m / 34, 7, 15);
  }

  // where each node wants to be, given the scene and its scroll progress
  function computeTargets() {
    const { key, p } = scene;
    const k = key;
    const sep = k === "schism" ? ease(clamp(p * 1.7 - 0.1)) : k === "scapegoat" ? 1 : 0;
    const goat = k === "scapegoat" ? ease(clamp(p * 1.5 - 0.05)) : 0;
    const plural = ["plural", "dim", "faint"].includes(k) ? 1 : 0;
    anim.sep = sep; anim.goatT = goat; anim.pluralT = plural;
    for (const n of nodes) {
      let x = n.mx, y = n.my;
      if (plural) { x = n.px; y = n.py; }
      else if (k === "schism" || k === "scapegoat") {
        x = lerp(n.mx, n.sx, sep); y = lerp(n.my, n.sy, sep);
        if (k === "scapegoat") {
          const r = lerp(0.95, 0.5, goat) * n.gj;
          const asp = (region.y1 - region.y0) / Math.max(1, region.x1 - region.x0);
          const gx = Math.cos(n.ga) * r * Math.min(1, asp * 1.1), gy = Math.sin(n.ga) * r * 0.86;
          x = lerp(x, gx, ease(clamp(p * 2.2))); y = lerp(y, gy, ease(clamp(p * 2.2)));
        }
      }
      [n.tx, n.ty] = toScreen(x, y);
    }
  }

  function step(dt) {
    const tr = targetRegion(scene.key);
    const rk = region.init && !REDUCE ? 0.07 : 1;
    for (const kk of ["x0", "x1", "y0", "y1"]) region[kk] += (tr[kk] - region[kk]) * rk;
    region.init = true;
    computeTargets();

    const k = scene.key, p = scene.p;
    const goalHeat = k === "contagion" ? clamp(p * 1.35) : k === "schism" || k === "scapegoat" ? 1 : 0;
    const goalAlpha = k === "dim" ? 0.34 : k === "faint" ? 0.2 : 1;
    const goalPlural = ["plural", "dim", "faint"].includes(k) ? 1 : 0;
    const goalGoat = k === "scapegoat" ? anim.goatT : 0;
    const goalRival = k === "schism" ? anim.sep : k === "scapegoat" ? 1 - anim.goatT : 0;
    const s = REDUCE ? 1 : 0.08;
    anim.heat += (goalHeat - anim.heat) * (REDUCE ? 1 : 0.18);
    anim.alpha += (goalAlpha - anim.alpha) * s;
    anim.plural += (goalPlural - anim.plural) * s;
    anim.goat += (goalGoat - anim.goat) * (REDUCE ? 1 : 0.2);
    anim.rivalA += (goalRival - anim.rivalA) * (REDUCE ? 1 : 0.2);

    const R = nodeRadius();
    let energy = 0;
    for (const n of nodes) {
      const wantHeat = anim.heat > 0.02 && n.ord <= anim.heat ? 1 : 0;
      n.heat += (wantHeat - n.heat) * (REDUCE ? 1 : 0.15);
      let wantA = 1;
      if ((k === "schism" || (k === "scapegoat" && anim.goat < 0.3)) && !n.side) wantA = lerp(1, 0.22, anim.sep);
      n.alpha += (wantA - n.alpha) * (REDUCE ? 1 : 0.1);
      if (pointer.drag === n) { n.x = pointer.x; n.y = pointer.y; n.vx = n.vy = 0; continue; }
      if (REDUCE) { n.x = n.tx; n.y = n.ty; continue; }
      n.vx += (n.tx - n.x) * 0.045; n.vy += (n.ty - n.y) * 0.045;
      if (pointer.inside && finePointer && !pointer.drag && n !== hover && n !== selected) {
        const dx = n.x - pointer.x, dy = n.y - pointer.y, d2 = dx * dx + dy * dy;
        if (d2 < 6400 && d2 > 1) { const f = 22 / d2; n.vx += dx * f; n.vy += dy * f; }
      }
    }
    if (!REDUCE) {
      const minD = R * 2.15;
      for (let i = 0; i < nodes.length; i++) {
        const a = nodes[i];
        for (let j = i + 1; j < nodes.length; j++) {
          const b = nodes[j];
          const dx = b.x - a.x, dy = b.y - a.y, d = Math.hypot(dx, dy);
          if (d < minD && d > 0.01) {
            const f = ((minD - d) / d) * 0.22;
            a.vx -= dx * f; a.vy -= dy * f; b.vx += dx * f; b.vy += dy * f;
          }
        }
      }
      for (const n of nodes) {
        if (pointer.drag === n) continue;
        n.vx *= 0.8; n.vy *= 0.8; n.x += n.vx; n.y += n.vy;
        energy += Math.abs(n.vx) + Math.abs(n.vy);
      }
    }
    return energy;
  }

  // ---------------------------------------------------------------- draw
  function drawGrid(t) {
    const g = 32;
    ctx.fillStyle = rgba(C.rule2, 0.55);
    const ox = 0, oy = (window.scrollY * 0.15) % g;
    for (let x = g / 2 + ox; x < W; x += g) for (let y = g / 2 - oy; y < H; y += g) ctx.fillRect(x, y, 1, 1);
    if (pointer.inside && finePointer) {
      ctx.strokeStyle = rgba(C.recog, 0.14); ctx.lineWidth = 1;
      ctx.beginPath(); ctx.moveTo(pointer.x + 0.5, TOP); ctx.lineTo(pointer.x + 0.5, H); ctx.moveTo(0, pointer.y + 0.5); ctx.lineTo(W, pointer.y + 0.5); ctx.stroke();
    }
  }

  function brackets(x, y, r, color) {
    const s = r + 7, l = 6;
    ctx.strokeStyle = color; ctx.lineWidth = 1.5; ctx.beginPath();
    for (const [sx, sy] of [[-1, -1], [1, -1], [1, 1], [-1, 1]]) {
      ctx.moveTo(x + sx * s, y + sy * (s - l)); ctx.lineTo(x + sx * s, y + sy * s); ctx.lineTo(x + sx * (s - l), y + sy * s);
    }
    ctx.stroke();
  }

  function tag(x, y, title, sub, color) {
    ctx.font = "600 13px 'Plex Cond', sans-serif";
    const w1 = ctx.measureText(title).width;
    ctx.font = "400 12px 'Plex Cond', sans-serif";
    const w2 = sub ? ctx.measureText(sub).width : 0;
    const w = Math.max(w1, w2) + 16, h = sub ? 38 : 22;
    let bx = x + 16, by = y - h / 2;
    if (bx + w > W - 10) bx = x - 16 - w;
    by = clamp(by, TOP + 6, H - h - 6);
    ctx.fillStyle = "rgba(14,19,26,0.92)"; ctx.fillRect(bx, by, w, h);
    ctx.fillStyle = color; ctx.fillRect(bx, by, 2, h);
    ctx.strokeStyle = C.rule2; ctx.lineWidth = 1; ctx.strokeRect(bx + 0.5, by + 0.5, w - 1, h - 1);
    ctx.fillStyle = C.ink; ctx.font = "600 13px 'Plex Cond', sans-serif"; ctx.textBaseline = "top";
    ctx.fillText(title, bx + 9, by + 5);
    if (sub) { ctx.fillStyle = C.ink2; ctx.font = "400 12px 'Plex Cond', sans-serif"; ctx.fillText(sub, bx + 9, by + 21); }
  }

  function draw(t) {
    ctx.clearRect(0, 0, W, H);
    drawGrid(t);
    if (!nodes.length) return;
    const A = anim.alpha, R = nodeRadius(), k = scene.key;

    // kin links
    ctx.lineWidth = 1;
    for (const l of links) {
      const hot = Math.min(l.a.heat, l.b.heat);
      const la = Math.min(l.a.alpha, l.b.alpha);
      // during the split the feed hides whatever the two sides share
      const across = anim.sep > 0.05 && (l.a.side !== l.b.side || !l.a.side) ? 1 - anim.sep : 1;
      if (across * la < 0.03) continue;
      const base = 0.13 * (1 - anim.goat) * (1 - 0.6 * anim.sep) * across * la;
      ctx.strokeStyle = hot > 0.5 && anim.plural < 0.5 ? rgba(C.heat, (0.18 + 0.3 * hot) * A * (1 - anim.goat) * across * la) : rgba(C.ink, base * A);
      ctx.beginPath(); ctx.moveTo(l.a.x, l.a.y); ctx.lineTo(l.b.x, l.b.y); ctx.stroke();
    }

    // contagion pulses along the breadth-first tree
    if (anim.heat > 0.01 && anim.plural < 0.5 && !REDUCE && k === "contagion") {
      const ph = ((t - t0) / 1400) % 1;
      ctx.fillStyle = C.heat;
      for (const e of bfsTree) {
        if (e.b.heat < 0.5) continue;
        const x = lerp(e.a.x, e.b.x, ph), y = lerp(e.a.y, e.b.y, ph);
        ctx.globalAlpha = 0.9 * A; ctx.fillRect(x - 1.5, y - 1.5, 3, 3);
      }
      ctx.globalAlpha = 1;
    }

    // rivalry across the split
    if (anim.rivalA > 0.01) {
      for (const l of rivals) {
        if (!l.a.side || !l.b.side || l.a.side === l.b.side) continue;
        const mx = (l.a.x + l.b.x) / 2, my = (l.a.y + l.b.y) / 2 - 40;
        ctx.strokeStyle = rgba(C.heat, 0.28 * anim.rivalA * A); ctx.lineWidth = 1;
        ctx.beginPath(); ctx.moveTo(l.a.x, l.a.y); ctx.quadraticCurveTo(mx, my, l.b.x, l.b.y); ctx.stroke();
      }
    }

    // scapegoat
    let goatXY = null;
    if (anim.goat > 0.01) {
      goatXY = toScreen(0, 0);
      const [gx, gy] = goatXY;
      ctx.lineWidth = 1;
      for (const n of nodes) {
        ctx.strokeStyle = rgba(C.heat, 0.32 * anim.goat * n.alpha);
        ctx.beginPath(); ctx.moveTo(n.x, n.y); ctx.lineTo(gx, gy); ctx.stroke();
      }
      const gr = R * (1.3 + anim.goat * 1.2);
      ctx.fillStyle = C.ground; ctx.strokeStyle = C.heat; ctx.lineWidth = 2;
      ctx.beginPath(); ctx.arc(gx, gy, gr, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
      if (!REDUCE) {
        const pr = gr + 6 + (((t - t0) / 900) % 1) * 22;
        ctx.strokeStyle = rgba(C.heat, 0.5 * (1 - (((t - t0) / 900) % 1)) * anim.goat);
        ctx.beginPath(); ctx.arc(gx, gy, pr, 0, Math.PI * 2); ctx.stroke();
      }
      ctx.fillStyle = C.heat; ctx.font = `400 ${Math.round(gr * 1.2)}px Anton, Impact, sans-serif`; ctx.textAlign = "center"; ctx.textBaseline = "middle";
      ctx.fillText("?", gx, gy + 1); ctx.textAlign = "left";
    }

    // recognition: descriptions waiting to be signed, between every pair of schools
    if (anim.plural > 0.02) {
      const cs = Object.values(centroid);
      ctx.setLineDash([3, 5]); ctx.lineWidth = 1;
      const ph = REDUCE ? 0.5 : ((t - t0) / 3200) % 1;
      for (let i = 0; i < cs.length; i++) for (let j = i + 1; j < cs.length; j++) {
        const [ax, ay] = toScreen(cs[i].x, cs[i].y), [bx, by] = toScreen(cs[j].x, cs[j].y);
        const mx = (ax + bx) / 2 + (by - ay) * 0.12, my = (ay + by) / 2 - (bx - ax) * 0.12;
        ctx.strokeStyle = rgba(C.recog, 0.6 * anim.plural * Math.max(A, 0.5)); ctx.lineWidth = 1.25;
        ctx.beginPath(); ctx.moveTo(ax, ay); ctx.quadraticCurveTo(mx, my, bx, by); ctx.stroke();
        // a note travelling across
        const u = (ph + i * 0.17 + j * 0.29) % 1, v = 1 - u;
        const px = v * v * ax + 2 * v * u * mx + u * u * bx, py = v * v * ay + 2 * v * u * my + u * u * by;
        ctx.setLineDash([]); ctx.fillStyle = rgba(C.recog, 0.9 * anim.plural * Math.max(A, 0.5));
        ctx.fillRect(px - 2, py - 2, 4, 4); ctx.setLineDash([3, 5]);
      }
      ctx.setLineDash([]);
    }

    // nodes
    for (const n of nodes) {
      const a = n.alpha * A;
      const isH = n === hover || n === selected;
      const r = isH ? R * 1.35 : R;
      ctx.globalAlpha = a;
      if (n.heat > 0.05 && anim.plural < 0.5) {
        ctx.fillStyle = rgba(C.heat, 0.22 * n.heat * (1 - anim.goat * 0.5));
        ctx.beginPath(); ctx.arc(n.x, n.y, r + 6, 0, Math.PI * 2); ctx.fill();
      }
      const img = isH ? n.full || n.gray : n.gray;
      if (img) ctx.drawImage(img, n.x - r, n.y - r, r * 2, r * 2);
      else {
        ctx.fillStyle = C.ground2; ctx.beginPath(); ctx.arc(n.x, n.y, r, 0, Math.PI * 2); ctx.fill();
        if (r > 8) { ctx.fillStyle = C.ink2; ctx.font = `600 ${Math.round(r * 0.75)}px 'Plex Cond', sans-serif`; ctx.textAlign = "center"; ctx.textBaseline = "middle"; ctx.fillText(n.p.initials, n.x, n.y + 0.5); ctx.textAlign = "left"; }
      }
      const ring = n.heat > 0.5 && anim.plural < 0.5 ? C.heat : n.color;
      ctx.strokeStyle = ring; ctx.lineWidth = isH ? 2 : 1.5;
      ctx.beginPath(); ctx.arc(n.x, n.y, r, 0, Math.PI * 2); ctx.stroke();
      if (n.threshold && anim.plural > 0.5) {
        ctx.setLineDash([2, 3]); ctx.strokeStyle = rgba(C.recog, 0.8); ctx.beginPath(); ctx.arc(n.x, n.y, r + 4, 0, Math.PI * 2); ctx.stroke(); ctx.setLineDash([]);
      }
      ctx.globalAlpha = 1;
    }

    // faction labels in the plural view
    if (anim.plural > 0.3 && A > 0.5 && W > 520) {
      ctx.font = "600 13px 'Plex Cond', sans-serif"; ctx.textBaseline = "bottom";
      for (const c of Object.values(centroid)) {
        const [x, y] = toScreen(c.x, c.y);
        const list = nodes.filter((n) => n.p.school === c.label);
        const top = Math.min(...list.map((n) => n.y)) - R - 10;
        ctx.fillStyle = rgba(c.color, anim.plural * A);
        const w = ctx.measureText(c.label).width;
        ctx.fillText(c.label, x - w / 2, top);
      }
    }

    // macro caption around the scapegoat
    const macro = $("#macro");
    if (goatXY && anim.goat > 0.35) {
      macro.style.opacity = String(clamp((anim.goat - 0.35) * 2.5));
      macro.style.left = region.x0 + "px"; macro.style.width = (region.x1 - region.x0) + "px";
      macro.style.top = (region.y0 - 6) + "px"; macro.style.height = (region.y1 - region.y0 + 12) + "px";
    } else macro.style.opacity = "0";

    // selection
    const sel = hover || selected;
    if (sel && sel.alpha * A > 0.15) {
      const r = R * 1.35;
      brackets(sel.x, sel.y, r, C.recog);
      tag(sel.x + r, sel.y, sel.p.name, sel.p.school || (sel.p.between ? "Between " + sel.p.between.join(" and ") : "No school yet"), sel.color);
    }
  }

  function frame(t) {
    const dt = Math.min(48, t - lastT); lastT = t;
    readScroll();
    const e = step(dt);
    draw(t);
    const continuous = !REDUCE && (scene.key === "contagion" || anim.goat > 0.01 || anim.plural > 0.02);
    if (e > 0.3 || continuous || pointer.drag) requestAnimationFrame(frame);
    else awake = false;
  }
  function wake() {
    if (!nodes.length) return;
    if (REDUCE) { readScroll(); step(16); draw(performance.now()); return; }
    if (!awake) { awake = true; lastT = performance.now(); requestAnimationFrame(frame); }
  }

  // ---------------------------------------------------------------- scroll
  const sceneEls = $$("[data-scene]");
  const railLinks = $$("[data-rail]");
  let lastRail = "";
  function readScroll() {
    const mid = H * 0.5;
    let cur = sceneEls[0];
    for (const el of sceneEls) { const r = el.getBoundingClientRect(); if (r.top <= mid) cur = el; }
    const r = cur.getBoundingClientRect();
    const span = Math.max(1, r.height - H * 0.5);
    scene = { key: cur.dataset.scene, p: clamp((mid - r.top) / span), el: cur };
    const id = cur.id;
    if (id !== lastRail) {
      lastRail = id;
      for (const a of railLinks) a.classList.toggle("on", a.dataset.rail === (id === "why" ? "turn" : id));
      const names = { top: "map", contagion: "contagion", schism: "schismogenesis", scapegoat: "scapegoat", fixes: "fixes", turn: "anti-mimesis", why: "anti-mimesis", instruments: "instruments", debate: "first release", rules: "rules", join: "invitation" };
      $("#ro-scene").textContent = names[id] || id;
    }
  }
  addEventListener("scroll", wake, { passive: true });
  addEventListener("resize", resize);
  reduceMQ.addEventListener?.("change", (e) => { REDUCE = e.matches; wake(); });

  // ---------------------------------------------------------------- pointer
  function hit(x, y) {
    const R = nodeRadius() * 1.4 + 4;
    let best = null, bd = R * R;
    for (const n of nodes) {
      if (n.alpha * anim.alpha < 0.15) continue;
      const d = (n.x - x) ** 2 + (n.y - y) ** 2;
      if (d < bd) { bd = d; best = n; }
    }
    return best;
  }
  canvas.addEventListener("pointermove", (e) => {
    pointer.x = e.clientX; pointer.y = e.clientY; pointer.inside = true;
    if (pointer.down) pointer.moved += Math.abs(e.movementX || 0) + Math.abs(e.movementY || 0);
    if (!pointer.drag) {
      const h = e.pointerType === "mouse" ? hit(e.clientX, e.clientY) : null;
      if (h !== hover) { hover = h; canvas.style.cursor = h ? "grab" : "default"; }
    }
    if (finePointer) {
      const [wx, wy] = fromScreen(e.clientX, e.clientY);
      const f = (v) => (v < 0 ? "\u2212" : "+") + Math.abs(v * 100).toFixed(1).padStart(5, "0");
      $("#ro-xy").textContent = `${f(wx)} ${f(-wy)}`;
    }
    wake();
  });
  canvas.addEventListener("pointerleave", () => { pointer.inside = false; if (!pointer.drag) hover = null; wake(); });
  canvas.addEventListener("pointerdown", (e) => {
    const h = hit(e.clientX, e.clientY);
    pointer.down = true; pointer.moved = 0; pointer.x = e.clientX; pointer.y = e.clientY;
    pointer.cand = h;
    if (h && e.pointerType !== "touch") { pointer.drag = h; canvas.setPointerCapture(e.pointerId); canvas.style.cursor = "grabbing"; }
    wake();
  });
  canvas.addEventListener("pointerup", (e) => {
    const c = pointer.cand;
    if (c && pointer.moved < 6) openDossier(c.p.id);
    else if (!c && pointer.moved < 6 && selected) closeDossier();
    pointer.down = false; pointer.drag = null; pointer.cand = null; canvas.style.cursor = hover ? "grab" : "default";
    wake();
  });

  // ---------------------------------------------------------------- dossier
  const dz = $("#dossier");
  let dzReturn = null;
  async function openDossier(id, fromEl) {
    const n = byId.get(id); if (!n) return;
    selected = n; dzReturn = fromEl || null;
    const p = n.p;
    dz.style.setProperty("--sw", n.color);
    $("#dz-name").textContent = p.name;
    $("#dz-school").textContent = p.school ? p.school : p.between ? "Between " + p.between.join(" and ") : "Not in a school yet";
    const face = $("#dz-face");
    face.textContent = p.face ? "" : p.initials;
    face.style.backgroundImage = p.face ? `url("${p.face}")` : "none";
    face.setAttribute("role", "img"); face.setAttribute("aria-label", p.face ? "Portrait of " + p.name : "");
    $("#dz-card").href = CONFIG.debateBase + CONFIG.cardPath + encodeURIComponent(p.id);
    const body = $("#dz-body");
    body.innerHTML = `<p class="fine" style="padding-top:12px">Loading their words…</p>`;
    dz.hidden = false;
    wake();
    await loadQuotes();
    if (selected !== n) return;
    const v = (QUOTES.voices || {})[id] || [];
    body.innerHTML = v.length ? v.map((x) => `
      <div class="dz-item">
        <p class="pos">${esc(x.position)}</p>
        <blockquote>“${esc(x.quote)}”</blockquote>
        <a href="${esc(safeUrl(x.url))}" target="_blank" rel="noopener">${esc(x.work || "Source")}</a>
      </div>`).join("") : `<p class="fine" style="padding-top:12px">No quotes on file yet.</p>`;
  }
  function closeDossier() {
    dz.hidden = true; selected = null; wake();
    if (dzReturn) { dzReturn.focus(); dzReturn = null; }
  }
  $("#dz-close").addEventListener("click", closeDossier);
  addEventListener("keydown", (e) => { if (e.key === "Escape" && !dz.hidden) closeDossier(); });

  // ---------------------------------------------------------------- index (keyboard path to every node)
  const ix = $("#index");
  $("#open-index").addEventListener("click", () => { if (ix.showModal) ix.showModal(); else ix.setAttribute("open", ""); });
  $("#ix-close").addEventListener("click", () => ix.close ? ix.close() : ix.removeAttribute("open"));
  ix.addEventListener("click", (e) => { if (e.target === ix) ix.close(); });

  // ---------------------------------------------------------------- page sections fed by data
  function fillPage() {
    const nPeople = DATA.people.length, nSt = DATA.statements.length;
    for (const el of $$('[data-count="people"]')) el.textContent = nPeople;
    for (const el of $$('[data-count="statements"]')) el.textContent = nSt;

    // index list
    const sorted = DATA.people.slice().sort((a, b) => a.name.split(" ").slice(-1)[0].localeCompare(b.name.split(" ").slice(-1)[0]));
    $("#ix-list").innerHTML = sorted.map((p) => `<li><button type="button" data-pid="${esc(p.id)}"><span class="swatch" style="--sw:${schoolColor(p.school)}"></span>${esc(p.name)}</button></li>`).join("");
    $("#ix-list").addEventListener("click", (e) => {
      const b = e.target.closest("[data-pid]"); if (!b) return;
      ix.close(); openDossier(b.dataset.pid, $("#open-index"));
      $("#dz-close").focus();
    });

    // would they sign it?
    const tabs = $(".signit-tabs");
    tabs.innerHTML = DATA.schools.map((s, i) => `<button type="button" role="tab" id="tab-${i}" aria-selected="${i === 0}" tabindex="${i === 0 ? 0 : -1}" style="--sw:${schoolColor(s.label)}"><span class="swatch"></span>${esc(s.label)}</button>`).join("");
    const panel = $(".signit-body");
    const pick = (i) => {
      const s = DATA.schools[i];
      $$("button", tabs).forEach((b, j) => { b.setAttribute("aria-selected", String(i === j)); b.tabIndex = i === j ? 0 : -1; });
      panel.setAttribute("aria-labelledby", "tab-" + i);
      $("#signit-note").textContent = s.note;
      $("#signit-fid").textContent = `Signed by 0 of ${s.members.length} members`;
    };
    tabs.addEventListener("click", (e) => { const b = e.target.closest("button"); if (b) pick($$("button", tabs).indexOf(b)); });
    tabs.addEventListener("keydown", (e) => {
      const bs = $$("button", tabs); let i = bs.indexOf(document.activeElement);
      if (e.key === "ArrowRight") i = (i + 1) % bs.length; else if (e.key === "ArrowLeft") i = (i - 1 + bs.length) % bs.length; else return;
      e.preventDefault(); bs[i].focus(); pick(i);
    });
    pick(0);

    // schools
    $(".schools > h3").textContent = `The ${DATA.schools.length === 4 ? "four" : DATA.schools.length} schools the map finds right now`;
    $(".school-list").innerHTML = DATA.schools.map((s) => `<li><h4><span class="swatch" style="--sw:${schoolColor(s.label)}"></span>${esc(s.label)}</h4><span class="n">${s.members.length} figures</span><p>${esc(s.note)}</p></li>`).join("");

    // footer
    $("#data-version").textContent = `Map data: ${DATA.bundle_version}, ${DATA.season}. ${nPeople} figures, ${nSt} statements.`;
    $("#notes").innerHTML = DATA.notes.map((n) => `<li>${esc(n)}</li>`).join("");
    const cred = Object.entries(DATA.credits).map(([id, c]) => ({ name: byId.get(id)?.p.name || id, c })).sort((a, b) => a.name.localeCompare(b.name));
    $("#credit-n").textContent = cred.length;
    $("#credits").innerHTML = cred.map(({ name, c }) => {
      const lic = c.license_url ? `<a href="${esc(safeUrl(c.license_url))}" target="_blank" rel="noopener">${esc(c.license)}</a>` : esc(c.license);
      return `<li>${esc(name)}: <a href="${esc(safeUrl(c.source))}" target="_blank" rel="noopener">photo</a> by ${esc(c.artist || "unknown")}, ${lic}</li>`;
    }).join("");

    initSplit();
  }

  // ---------------------------------------------------------------- the split board
  function initSplit() {
    const st = DATA.statements;
    const setTitle = Object.fromEntries((DATA.sets || []).map((s) => [s.id, s.title]));
    // open on the same statement the schism scene used
    let i = Math.max(0, st.findIndex((s) => s.id === schismStatement?.st.id));
    let current = null;
    const face = (p) => {
      const col = schoolColor(p.school);
      const bg = p.face ? `background-image:url('${p.face}')` : "";
      return `<li><button type="button" data-pid="${esc(p.id)}" aria-pressed="false" aria-label="${esc(p.name)}" title="${esc(p.name)}" style="--sw:${col};${bg}">${p.face ? "" : esc(p.initials)}</button></li>`;
    };
    function render() {
      const s = st[i];
      $("#split-meta").textContent = `Statement ${i + 1} of ${st.length}. ${setTitle[s.set] || ""}`;
      $("#split-q").textContent = s.text;
      const sides = DATA.sides[s.id] || {};
      const yes = [], no = [];
      for (const [pid, a] of Object.entries(sides)) { const n = byId.get(pid); if (!n) continue; (a > 0 ? yes : no).push(n.p); }
      yes.sort((a, b) => a.name.localeCompare(b.name)); no.sort((a, b) => a.name.localeCompare(b.name));
      $("#split-yes").innerHTML = yes.map(face).join(""); $("#split-no").innerHTML = no.map(face).join("");
      $("#split-yes-n").textContent = yes.length; $("#split-no-n").textContent = no.length;
      $("#split-quote").innerHTML = `<p class="fine">Pick a face to read what they said.</p>`;
      current = null;
    }
    async function show(pid, btn) {
      $$("#split [aria-pressed='true']").forEach((b) => b.setAttribute("aria-pressed", "false"));
      btn.setAttribute("aria-pressed", "true");
      current = pid;
      await loadQuotes();
      if (current !== pid) return;
      const s = st[i]; const row = (QUOTES.stances[s.id] || {})[pid];
      const p = byId.get(pid).p;
      if (!row) { $("#split-quote").innerHTML = `<p class="fine">No quote on file.</p>`; return; }
      const [a, q, url, work] = row;
      $("#split-quote").innerHTML = `<p class="who">${esc(p.name)} <em>${a > 0 ? "agrees" : "disagrees"}</em></p><blockquote>“${esc(q)}”</blockquote><a class="fine" href="${esc(safeUrl(url))}" target="_blank" rel="noopener">${esc(work || "Source")}</a>`;
    }
    $("#split-prev").addEventListener("click", () => { i = (i - 1 + st.length) % st.length; render(); });
    $("#split-next").addEventListener("click", () => { i = (i + 1) % st.length; render(); });
    $("#split").addEventListener("click", (e) => { const b = e.target.closest("[data-pid]"); if (b) show(b.dataset.pid, b); });
    render();
  }

  // ---------------------------------------------------------------- init
  function init(data) {
    DATA = data;
    resize();
    buildGraph();
    fillPage();
    readScroll();
    if (REDUCE) { for (const n of nodes) { n.alpha = 1; } region.init = false; }
    wake();
    // quotes are only needed on interaction; fetch them when the browser is idle
    (window.requestIdleCallback || ((f) => setTimeout(f, 2500)))(() => loadQuotes());
  }
  resize();
})();
