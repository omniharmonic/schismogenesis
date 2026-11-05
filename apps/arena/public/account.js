// The account page ("You"): sign in, or, when signed in, your name, picture and bio, whether to
// show yourself on the map, your ways in, and leaving.
import { esc } from "./map.js";
import { LOGIN_NAME, api, getMe, initials, saveAnswers, signInHTML, takeSignInHash, toast, wireSignIn, xAvailable } from "./auth.js";
import "./site-config.js";

const el = document.getElementById("account");

const local = {
  get() { try { return JSON.parse(localStorage.getItem("fp.answers")); } catch { return null; } },
  set(v) { try { localStorage.setItem("fp.answers", JSON.stringify(v)); } catch { /* private mode */ } },
};

// answers this browser has for the current season go up to the account after a sign-in
async function uploadLocal(account) {
  const saved = local.get();
  if (!saved?.answers || !Object.keys(saved.answers).length) return;
  let season = null;
  try { season = (await (await fetch("/fingerprint.json")).json()).season; } catch { return; }
  if (saved.season !== season) return;
  const sheet = account?.sheet;
  if (sheet?.season === season && Date.parse(sheet.updated_at || "") >= Date.parse(saved.updated_at || "")) return;
  try { await saveAnswers(saved.answers); } catch { /* the survey page tries again next time */ }
}

async function signedIn() {
  const account = await getMe();
  if (!account) { toast("Couldn't sign in"); return; }
  await uploadLocal(account);
  toast("Signed in");
  render(await getMe() || account);
}

async function renderSignedOut() {
  const x = await xAvailable();
  el.innerHTML = `<p class="serif lede">Sign in to come back on any device and change your answers, and, if you want, to put your picture on the map.</p>
    <p class="muted">Pick any way in. They all reach the same account, and you can add more later.</p>
    ${signInHTML({ id: "acc", x })}
    <p class="small muted">Signing in is optional. Without it, your answers stay in this browser only. <a href="/privacy.html">Privacy</a></p>`;
  wireSignIn(el.querySelector(".signin"), {
    onSignedIn: async (how) => { if (how !== "key-new") await signedIn(); else { const a = await getMe(); if (a) await uploadLocal(a); } },
    onKeySaved: () => signedIn(),
  });
}

function avatarHTML(a) {
  return a.avatar_url
    ? `<img class="acc-avatar" src="${esc(a.avatar_url)}" alt="" referrerpolicy="no-referrer">`
    : `<span class="acc-avatar" aria-hidden="true">${esc(initials(a.display_name))}</span>`;
}

function render(a) {
  a.logins ||= [];
  const hasFace = a.logins.some((l) => l.kind === "bsky" || l.kind === "x");
  const sheet = a.sheet;
  el.innerHTML = `
    <div class="acc-head">${avatarHTML(a)}<div><p class="acc-name">${esc(a.display_name || "No name yet")}</p>
      <p class="small muted">${sheet ? `Answers saved ${new Date(sheet.updated_at).toLocaleDateString(undefined, { day: "numeric", month: "long", year: "numeric" })}` : "No answers saved yet"}</p></div></div>

    <section class="acc-section" aria-labelledby="acc-map">
      <h2 id="acc-map">On the map</h2>
      <label class="switch-row" for="show-on-map">
        <span><b>Show me on the map</b><br><span class="small muted">${hasFace ? "Puts your picture, name and bio on the public map, near the thinkers you agree with most." : "Puts your picture, name and bio on the public map once you add a Bluesky or X sign-in below: that's where the picture comes from."}</span></span>
        <input type="checkbox" role="switch" id="show-on-map" ${a.show_on_map ? "checked" : ""}>
      </label>
      <p class="small muted">Either way, once ten people have added answers, yours count as one plain, unnamed dot among everyone's. This switch only decides whether your picture, name and bio are shown.</p>
    </section>

    <section class="acc-section" aria-labelledby="acc-about">
      <h2 id="acc-about">Name and bio</h2>
      <form id="profile-form">
        <label class="small" for="acc-display">Name</label>
        <input type="text" id="acc-display" maxlength="80" autocomplete="nickname" value="${esc(a.display_name || "")}">
        <label class="small" for="acc-bio" style="display:block;margin-top:12px">Bio <span class="muted">(up to 160 characters)</span></label>
        <textarea id="acc-bio" maxlength="160" rows="3">${esc(a.bio || "")}</textarea>
        <div class="row" style="margin-top:12px"><button class="primary" type="submit">Save</button><span class="small muted" id="bio-count"></span></div>
      </form>
      <p class="small muted">Shown only when “Show me on the map” is on.</p>
    </section>

    <section class="acc-section" aria-labelledby="acc-answers">
      <h2 id="acc-answers">Your answers</h2>
      <p>${sheet ? "Your answers save to this account as you change them." : "Take the survey while signed in and your answers save here."}</p>
      <div class="row"><button class="primary" id="change">${sheet ? "Change my answers" : "Take the survey"}</button></div>
    </section>

    <section class="acc-section" aria-labelledby="acc-logins">
      <h2 id="acc-logins">Ways in</h2>
      <ul class="acc-logins">${a.logins.map((l) => `<li><b>${esc(LOGIN_NAME[l.kind] || l.kind)}</b>${l.handle ? ` <span class="muted">${l.kind === "bsky" || l.kind === "x" ? "@" : ""}${esc(l.handle)}</span>` : ""}</li>`).join("")}</ul>
      <details class="acc-add"><summary>Add another way in</summary>
        <p class="small muted">Sign in another way while you're signed in here and it joins this account.</p>
        <div id="add-way"></div></details>
    </section>

    <section class="acc-section" aria-labelledby="acc-leave">
      <h2 id="acc-leave">Leave</h2>
      <div class="row"><button id="signout">Sign out</button><button class="danger" id="delete">Delete my account</button></div>
      <p class="small muted">Deleting removes your account, your ways in, your saved answers and anything shown on the map. It can't be undone.</p>
    </section>`;

  const sw = document.getElementById("show-on-map");
  sw.onchange = async () => {
    sw.disabled = true;
    try { await api("/api/me", { method: "PATCH", body: { show_on_map: sw.checked } }); toast(sw.checked ? "You're on the map" : "Hidden from the map"); }
    catch (e) { sw.checked = !sw.checked; toast(e.message); }
    finally { sw.disabled = false; }
  };

  const bio = document.getElementById("acc-bio"), count = document.getElementById("bio-count");
  const left = () => { count.textContent = `${160 - bio.value.length} left`; };
  bio.oninput = left; left();
  document.getElementById("profile-form").onsubmit = async (e) => {
    e.preventDefault();
    const display_name = document.getElementById("acc-display").value.trim(), text = bio.value.trim();
    try {
      await api("/api/me", { method: "PATCH", body: { display_name, bio: text } });
      a.display_name = display_name; a.bio = text;
      el.querySelector(".acc-name").textContent = display_name || "No name yet";
      toast("Saved");
    } catch (err) { toast(err.message); }
  };

  document.getElementById("change").onclick = async () => {
    // put the saved answers in this browser, then resume the survey with them
    if (sheet?.answers) {
      local.set({ season: sheet.season, answers: sheet.answers, index: 0, updated_at: sheet.updated_at });
    }
    location.href = "/#change";
  };

  const addEl = document.getElementById("add-way");
  el.querySelector(".acc-add").addEventListener("toggle", async (e) => {
    if (!e.target.open || addEl.childElementCount) return;
    addEl.innerHTML = signInHTML({ id: "add", x: await xAvailable() });
    wireSignIn(addEl.querySelector(".signin"), {
      onSignedIn: async (how) => { if (how !== "key-new") { toast("Added"); render(await getMe() || a); } },
      onKeySaved: async () => { toast("Added"); render(await getMe() || a); },
    });
  });

  document.getElementById("signout").onclick = async () => {
    try { await api("/api/auth/logout", { method: "POST", body: {} }); } catch { /* the cookie may already be gone */ }
    toast("Signed out");
    renderSignedOut();
  };
  document.getElementById("delete").onclick = async () => {
    if (!confirm("Delete your account? This removes your saved answers, your ways in and anything shown on the map. It can't be undone.")) return;
    try { await api("/api/me", { method: "DELETE" }); } catch (e) { toast(e.message); return; }
    toast("Account deleted");
    renderSignedOut();
  };
}

async function main() {
  const back = takeSignInHash();
  const account = await getMe();
  if (back && !back.ok) toast(back.message);
  if (account) {
    if (back?.ok) { await uploadLocal(account); toast("Signed in"); }
    render(account);
  } else {
    if (back?.ok) toast("Couldn't sign in");
    renderSignedOut();
  }
}

main();
