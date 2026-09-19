#!/usr/bin/env python3
"""Bundle src/ into a single self-contained index.html.

No dependencies beyond the Python standard library. Fonts in assets/fonts/
are inlined as base64 so the finished page makes zero network requests.

    python3 build.py            # -> index.html
    python3 build.py out.html   # -> out.html
"""

import base64
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src")
FONTS = os.path.join(ROOT, "assets", "fonts")

# (css font-family, file slug, weights to embed)
FONT_SPEC = [
    ("Big Shoulders Display", "big-shoulders-display", [800, 900]),
    ("IBM Plex Sans", "ibm-plex-sans", [400, 600, 700]),
    ("IBM Plex Mono", "ibm-plex-mono", [400, 600]),
]


def read(name):
    with open(os.path.join(SRC, name), encoding="utf-8") as fh:
        return fh.read()


def font_css():
    rules = []
    for family, slug, weights in FONT_SPEC:
        for weight in weights:
            path = os.path.join(FONTS, "%s-latin-%d-normal.woff2" % (slug, weight))
            with open(path, "rb") as fh:
                b64 = base64.b64encode(fh.read()).decode("ascii")
            rules.append(
                "@font-face{font-family:'%s';font-style:normal;font-weight:%d;"
                "font-display:swap;src:url(data:font/woff2;base64,%s) format('woff2')}"
                % (family, weight, b64)
            )
    return (
        "<style>/* embedded fonts (SIL OFL 1.1): "
        "Big Shoulders Display, IBM Plex Sans, IBM Plex Mono */\n"
        + "\n".join(rules)
        + "\n</style>"
    )


def build():
    html = (
        read("head.html").replace("<!--FONTS-->", font_css())
        + read("style.css")
        + read("body.html")
        + "\n<script>\n(function(){'use strict';\n"
        + read("appA.js")
        + "\n"
        + read("appB.js")
        + "\n})();\n</script>\n</body>\n</html>\n"
    )
    dst = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "index.html")
    with open(dst, "w", encoding="utf-8") as fh:
        fh.write(html)
    print("%d KB -> %s" % (len(html.encode("utf-8")) // 1024, dst))


if __name__ == "__main__":
    build()
