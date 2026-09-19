# Caterpillar Future Concept

An independent, speculative redesign of a heavy-equipment manufacturer's landing page,
built as a demonstration of what a website looks like when **AI agents and human visitors
are treated as equal first-class users**.

The whole thing is one self-contained HTML file. No build server, no CDN, no network
requests, no cookies, no tracking. Open it from a `file://` URL on a plane and every
feature still works.

> **Disclaimer.** This is an independent design exercise. It is not affiliated with,
> endorsed by, or connected to Caterpillar Inc. Every figure, headline, product
> summary and news item on the page is fictional and simulated. All artwork is
> original and generated procedurally in the browser — no photography or trademarked
> imagery is included.

---

## Quick start

```bash
git clone <your-fork-url>
cd caterpillar-concept
python3 build.py        # writes index.html (~330 KB, zero dependencies)
open index.html         # or: python3 -m http.server 8000
```

`index.html` is committed, so you can also just open it directly after cloning, or
publish the repo to GitHub Pages and it works as-is.

---

## What's interesting about it

### A machine-readable interface, not just an accessible one

Most "agent-friendly" pages mean well-formed HTML and good ARIA. This one goes further:
every user-facing action on the page is a **named tool with a JSON schema**, and those
tools are published through three channels at once.

| Channel | How to reach it |
| --- | --- |
| **WebMCP** | `navigator.modelContext` — tools auto-register when the browser supports it |
| **JavaScript** | `window.CatAgent.call(name, args)` — returns a promise resolving to structured data |
| **Declarative** | `<form toolname="ask_cat">` — usable without running any script |
| **Manifest** | `script#agent-manifest` — JSON description of every section, tool and policy |
| **llms.txt** | `template#llms-txt-src` — plain-text orientation for a crawling model |

The critical property is that the human UI and the agent API are the *same code path*.
A button click, a voice command and `CatAgent.call()` all invoke the same implementation,
so an agent can never drift out of sync with what a person sees.

```js
await CatAgent.call('get_page_markdown')            // whole page as clean Markdown
await CatAgent.call('navigate', { section: 'news' }) // scroll + focus + highlight
await CatAgent.call('generate_theme', { description: 'midnight ocean' })
await CatAgent.call('ask_cat', { question: 'Who should I talk to about press?' })
```

### The tools

Seventeen of them, covering reading, navigation, search, appearance and state:

`list_sections` · `navigate` · `search_site` · `get_page_summary` · `get_page_markdown` ·
`set_theme` · `generate_theme` · `set_motion` · `set_text_size` · `filter_news` ·
`summarize_article` · `persona_briefing` · `read_aloud` · `toggle_agent_vision` ·
`get_fleet_pulse` · `get_state` · `ask_cat`

`get_page_markdown` is the one that matters most in practice: an agent reads the entire
page in a single call instead of walking the DOM node by node.

`toggle_agent_vision` is the inverse — it overlays the page's semantic roles and
interactive controls so a *human* can see what the agent sees.

### Themes as a first-class, generative feature

Six hand-built presets (`iron`, `daylight`, `mars`, `lunar`, `mine`, `contrast`) plus a
generator that turns free text into a palette. Every colour on the page — including the
procedurally drawn artwork and the canvas simulation — reads from twelve CSS custom
properties, so a theme change repaints everything atomically through a View Transition
circular wipe.

The generator won't ship an unreadable palette: `tune()` iteratively walks lightness in
HSL until it hits **12:1 contrast for body text, 5.2:1 for secondary text and 5:1 for
links**, which is comfortably past WCAG AA. That constraint is what makes "make it look
like a sunset" a safe thing to let a stranger's agent do to your page.

### Original procedural artwork

Every illustration is an SVG drawn at runtime by the `ART` factory in `src/appA.js` —
eight scene types (careers, investors, media, sustainability, culture, quarry, field AI,
STEM, keynote, HQ, excavator). They aren't images with a filter on top; the geometry is
generated and the fills are theme tokens, so they genuinely recolour rather than tint.

### The digital twin

A `<canvas>` running a procedurally generated quarry with twelve autonomous haulers
following Bézier routes. Hovering a truck pulls up its telemetry. It pauses via
`IntersectionObserver` when scrolled out of view, so it costs nothing when you aren't
looking at it.

### Conversation and voice

An on-page concierge with a local intent router — regex-driven, no network — that handles
theme changes, motion, text size, news filters, persona switches, site search and section
navigation. When the page is embedded somewhere with a `sample` capability it can hand
harder questions to Claude; otherwise it degrades to the local router without complaint.

Speech recognition drives input and speech synthesis reads sections aloud, both behind
feature detection.

### Accessibility as a constraint, not a checkbox

- Zero axe-core violations across all seven themes
- Every decorative effect is `aria-hidden` and disabled by `Motion: Calm`
- `prefers-reduced-motion`, `prefers-contrast` and `prefers-color-scheme` are honoured
  **before first paint**, by a small inline script in `<head>`
- Three text sizes; full keyboard navigation including the drag carousel
- No horizontal overflow at 390 px or 768 px

---

## Repository layout

```
build.py            Bundler — concatenates src/, inlines fonts as base64
index.html          Built output (committed; regenerate with build.py)
src/
  head.html         Metadata, agent manifest, JSON-LD, pre-paint theme script
  style.css         ~450 lines: six theme token sets, layout, keyframes
  body.html         Semantic markup for every section
  appA.js           Utilities, procedural art factory, theme engine, canvas twin
  appB.js           Tool registry, concierge, intent router, speech, export, state
assets/fonts/       Big Shoulders Display, IBM Plex Sans, IBM Plex Mono (SIL OFL 1.1)
```

Editing is done in `src/`; `index.html` is generated. Re-run `python3 build.py` after
any change.

---

## Design notes

**Why one file?** Because the interesting claim — that a page can be fully legible to an
agent — is much stronger if there's nothing to install and nothing to fetch. It also
means the page keeps working when the CDN, the font host and the analytics endpoint are
all unreachable, which is a better default than the industry currently ships.

**Why simulated data?** Real figures would date instantly and imply endorsement. The
manifest declares the simulation explicitly under `policies`, so an agent reading the
page knows not to quote the numbers as fact.

**What has no tool, deliberately.** Cookie consent and social-feed consent. An agent
should not be able to accept terms on a person's behalf, so there is no API surface for
it — only a human can click those.

---

## Licence

Code and artwork: MIT (see `LICENSE`).
Bundled fonts: SIL Open Font Licence 1.1, redistributed under its terms.

"Caterpillar" and "Cat" are trademarks of Caterpillar Inc., used here only nominatively
to identify the subject of a design study. No trademarked logos or imagery are included.
