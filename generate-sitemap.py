#!/usr/bin/env python3
"""Generiert sitemap.xml aus allen .html-Dateien im Repo-Root."""
import os, glob
from datetime import date

DOMAIN = "https://entruempelung-deutschland.com"
EXCLUDE = {"danke.html"}
TODAY = date.today().isoformat()

# Priority map
PRIORITY = {
    "index.html": ("1.0", "weekly"),
}
DEFAULT_CITY   = ("0.8", "monthly")
DEFAULT_PAGE   = ("0.6", "monthly")

files = sorted(glob.glob("*.html"))

urls = []
for f in files:
    if f in EXCLUDE:
        continue
    slug = f.replace(".html", "")
    loc = f"{DOMAIN}/{f}" if f != "index.html" else DOMAIN + "/"
    pri, freq = PRIORITY.get(f, DEFAULT_CITY if f.startswith("entrumpelung-") else DEFAULT_PAGE)
    urls.append((loc, freq, pri))

xml = ['<?xml version="1.0" encoding="UTF-8"?>']
xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
for loc, freq, pri in urls:
    xml.append(f"""  <url>
    <loc>{loc}</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>{freq}</changefreq>
    <priority>{pri}</priority>
  </url>""")
xml.append("</urlset>")

with open("sitemap.xml", "w", encoding="utf-8") as out:
    out.write("\n".join(xml) + "\n")

print(f"sitemap.xml: {len(urls)} URLs")
