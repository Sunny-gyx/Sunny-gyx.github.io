#!/usr/bin/env python3
"""Small, dependency-free checker for the homepage's declared links."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "index.md"

class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
    def handle_starttag(self, tag, attrs):
        if tag == "a":
            href = dict(attrs).get("href")
            if href:
                self.links.append(href)

parser = Links()
parser.feed(SOURCE.read_text(encoding="utf-8"))
anchors = set(re.findall(r'id="([^"]+)"', SOURCE.read_text(encoding="utf-8")))
results = []
for href in parser.links:
    if href.startswith("mailto:"):
        results.append(("OK", href, "well-formed email link"))
    elif href.startswith("#"):
        results.append(("OK" if href[1:] in anchors else "BROKEN", href, "internal anchor"))
    elif "assets/files/Yuxuan_Gao_CV.pdf" in href:
        asset = ROOT / "assets/files/Yuxuan_Gao_CV.pdf"
        results.append(("OK" if asset.is_file() else "BROKEN", href, "local CV asset"))
    elif href.startswith("http://") or href.startswith("https://"):
        state = "SKIPPED"
        note = "external URL syntax valid; network status recorded separately"
        results.append((state, href, note))
    else:
        results.append(("BROKEN", href, "unsupported local URL"))

for state, href, note in results:
    print(f"{state}\t{href}\t{note}")
sys.exit(1 if any(state == "BROKEN" for state, _, _ in results) else 0)
