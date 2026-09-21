"""Pull Google Play star ratings per country for the same three apps.

Play behaves differently from the App Store, and the difference decides what
can be asked of it:

  * review counts and download buckets are GLOBAL. Setting gl=es returns the
    same 124K reviews as gl=us, so Play cannot measure reach by market.
  * the star rating IS localised. Smallpdf reads 4.5 in the US, 4.2 in Germany
    and 4.8 in Brazil.

So Play can test whether satisfaction varies by market, which is the useful
half, and cannot test whether reach does.

    python3 scripts/pull_play.py > data/play-ratings.json

One trap worth recording. The obvious-looking package com.smallpdf.android is
NOT Smallpdf: it is an unrelated ad-supported app called "Small PDF Converter"
with about a thousand downloads. Smallpdf's real package is
com.smallpdf.app.android, published by Smallpdf AG. Always check the title and
developer on the page you land on rather than trusting a plausible package name.
"""

import json
import re
import sys
import time
import urllib.request

APPS = {
    "Smallpdf": "com.smallpdf.app.android",
    "iLovePDF": "com.ilovepdf.www",
    "Adobe Acrobat": "com.adobe.reader",
}

COUNTRIES = [
    "us", "gb", "de", "fr", "es", "it", "nl", "br", "mx", "ca", "au", "in",
    "jp", "pl", "se", "ch", "at", "be", "pt", "tr", "id", "ph", "za", "ae", "ar",
]

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
RATING = re.compile(r"([0-9]\.[0-9])\s*star")


def rating(package, country):
    url = f"https://play.google.com/store/apps/details?id={package}&gl={country}&hl=en"
    req = urllib.request.Request(url, headers={"user-agent": UA})
    page = urllib.request.urlopen(req, timeout=25).read().decode("utf-8", "replace")
    match = RATING.search(page)
    return float(match.group(1)) if match else None


def main():
    out = {}
    for country in COUNTRIES:
        row = {}
        for name, package in APPS.items():
            try:
                row[name] = rating(package, country)
            except Exception as exc:                  # noqa: BLE001
                print(f"{country}/{name}: {exc}", file=sys.stderr)
                row[name] = None
            time.sleep(0.25)
        out[country] = row
        print(country, row, file=sys.stderr)
    json.dump(out, sys.stdout, indent=1)


if __name__ == "__main__":
    main()
