"""Pull ratings counts and averages for the three largest PDF apps, per storefront.

Apple's public lookup API reports these per country, so the same app returns a
different figure for each storefront. That is what makes a market-by-market
comparison possible at all: Google Play, by contrast, publishes review counts
globally and only localises the star rating.

    python3 scripts/pull_app_store.py > data/app-store-ratings.json

What the numbers are, and are not:

  * They are RATINGS, from the tap-a-star prompt, not written reviews. They are
    one or two orders of magnitude larger.
  * They are a cumulative stock since the app launched in that storefront, with
    nothing resetting them. An app that was strong three years ago and is fading
    now still looks strong here.
  * They depend on how hard an app prompts for them. If one app prompts more
    often its count inflates independently of install base. That effect should
    be roughly uniform across countries, so it can inflate the level without
    explaining differences between markets.
"""

import json
import sys
import time
import urllib.request

APPS = {
    "Smallpdf": 1485259500,
    "iLovePDF": 1207332399,
    "Adobe Acrobat": 469337564,
}

STOREFRONTS = [
    "us", "gb", "de", "fr", "es", "it", "nl", "br", "mx", "ca", "au", "in",
    "jp", "pl", "se", "ch", "at", "be", "pt", "tr", "id", "ph", "za", "ae", "ar",
]

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"


def lookup(app_id, country):
    url = f"https://itunes.apple.com/lookup?id={app_id}&country={country}"
    req = urllib.request.Request(url, headers={"user-agent": UA})
    results = json.loads(urllib.request.urlopen(req, timeout=20).read())["results"]
    if not results:
        return {"n": 0, "avg": 0.0}          # app not sold in this storefront
    app = results[0]
    return {
        "n": app.get("userRatingCount", 0),
        "avg": round(app.get("averageUserRating", 0.0), 2),
    }


def main():
    rows = []
    for country in STOREFRONTS:
        row = {"country": country}
        for name, app_id in APPS.items():
            try:
                row[name] = lookup(app_id, country)
            except Exception as exc:                  # noqa: BLE001
                print(f"{country}/{name}: {exc}", file=sys.stderr)
                row[name] = {"n": 0, "avg": 0.0}
            time.sleep(0.1)                           # be polite to the API
        rows.append(row)
        print(country, {k: v["n"] for k, v in row.items() if k != "country"},
              file=sys.stderr)
    json.dump(rows, sys.stdout, indent=1)


if __name__ == "__main__":
    main()
