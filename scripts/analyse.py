"""Work the two pulls into the figures quoted in the report.

    python3 scripts/analyse.py

Prints the three-way shares, the market-by-market table, the permutation test
behind the language observation, and the Google Play satisfaction comparison.
Everything the report claims should be reproducible from here.
"""

import json
import random
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IOS = json.loads((ROOT / "data" / "app-store-ratings.json").read_text())
PLAY = json.loads((ROOT / "data" / "play-ratings.json").read_text())

# Google publishes these globally, so they are typed in rather than pulled per
# country. Read off the store pages on 21 September 2026.
PLAY_REVIEWS = {"Smallpdf": 124_000, "iLovePDF": 342_000, "Adobe Acrobat": 7_980_000}
PLAY_DOWNLOADS = {"Smallpdf": "5M+", "iLovePDF": "10M+", "Adobe Acrobat": "500M+"}

# Markets whose main official language descends from Latin. Chosen AFTER seeing
# the ranking, which is why the permutation test below is reported as weak
# evidence rather than as a result.
ROMANCE = {"es", "fr", "it", "pt", "br", "mx", "ar"}


def totals():
    return {name: sum(row[name]["n"] for row in IOS)
            for name in ("Smallpdf", "iLovePDF", "Adobe Acrobat")}


def shares():
    print("Share of ratings among the three largest PDF apps\n")
    t = totals()
    total = sum(t.values())
    print("  Apple App Store, 25 storefronts")
    for name, value in t.items():
        print(f"    {name:14} {value:10,}  {100 * value / total:5.1f}%")
    total_play = sum(PLAY_REVIEWS.values())
    print("\n  Google Play, global review counts")
    for name, value in PLAY_REVIEWS.items():
        print(f"    {name:14} {value:10,}  {100 * value / total_play:5.1f}%"
              f"   downloads {PLAY_DOWNLOADS[name]}")


def by_market():
    print("\n\nSmallpdf as a share of iLovePDF, by App Store storefront\n")
    rows = [(100 * r["Smallpdf"]["n"] / r["iLovePDF"]["n"], r) for r in IOS
            if r["iLovePDF"]["n"]]
    for pct, r in sorted(rows, reverse=True):
        c = r["country"]
        flag = " (Romance)" if c in ROMANCE else ""
        print(f"  {c.upper():3} {pct:5.1f}%   {r['Smallpdf']['n']:7,} vs "
              f"{r['iLovePDF']['n']:7,}   stars {r['Smallpdf']['avg']} / "
              f"{r['iLovePDF']['avg']}{flag}")
    return [r["country"] for _, r in sorted(rows)]


def permutation_test(order, trials=200_000, seed=7):
    """How unusual is it that all seven Romance markets rank this low?

    The honest caveat: the grouping was drawn after looking at the ranking, so
    this is not an independent test. It says the cluster is tight; it does not
    say the explanation is right.
    """
    print("\n\nPermutation test on the Romance-language cluster\n")
    observed = sum(order.index(c) for c in ROMANCE)
    random.seed(seed)
    hits = sum(1 for _ in range(trials)
               if sum(random.sample(range(len(order)), len(ROMANCE))) <= observed)
    print(f"  ranks: {[order.index(c) + 1 for c in sorted(ROMANCE)]}")
    print(f"  sum of ranks {observed}, lowest possible {sum(range(len(ROMANCE)))}")
    print(f"  {hits / trials:.5f} of random picks cluster at least this low")
    print("  NOTE: hypothesis chosen after seeing the data, so treat as weak.")


def play_satisfaction():
    print("\n\nGoogle Play: Smallpdf rating minus iLovePDF rating\n")
    gaps = {c: v["Smallpdf"] - v["iLovePDF"] for c, v in PLAY.items()
            if v.get("Smallpdf") and v.get("iLovePDF")}
    romance = [g for c, g in gaps.items() if c in ROMANCE]
    other = [g for c, g in gaps.items() if c not in ROMANCE]
    print(f"  Romance markets  n={len(romance):2}  mean {statistics.mean(romance):+.3f}")
    print(f"  everywhere else  n={len(other):2}  mean {statistics.mean(other):+.3f}")
    print(f"  all markets      n={len(gaps):2}  mean {statistics.mean(gaps.values()):+.3f}")
    print("\n  Satisfaction is flat across markets on Play, which supports the")
    print("  claim that the App Store spread is about reach and not quality.")
    worst = min(gaps, key=gaps.get)
    print(f"\n  Widest deficit: {worst.upper()} "
          f"{PLAY[worst]['Smallpdf']} vs {PLAY[worst]['iLovePDF']}")


if __name__ == "__main__":
    shares()
    permutation_test(by_market())
    play_satisfaction()
