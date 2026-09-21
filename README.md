# What public app store data says about Smallpdf

An outside-in look at where Smallpdf sits against iLovePDF and Adobe Acrobat,
built entirely from data anyone can pull: Apple's public lookup API and the
Google Play store pages.

**[Read the report](https://loispatterson.github.io/pdf-app-store-analysis/)**
&nbsp;·&nbsp;
[PDF version](smallpdf-store-analysis.pdf)

## The two findings

**Smallpdf's share is identical on both stores. iLovePDF's is not.** Of the
three largest PDF apps, Smallpdf holds 1.5% of App Store ratings and 1.5% of
Play reviews. iLovePDF holds 18.2% on the App Store and 4.0% on Play, roughly
four times stronger on iOS than on Android, while neither Smallpdf nor Adobe
shows that asymmetry. Whatever iLovePDF is doing on iOS appears specific to iOS.

**Smallpdf's position against iLovePDF varies nearly elevenfold by market**,
from 33.4% in Türkiye and 29.8% in Germany down to 3.0% in Spain and Argentina.
It is not a quality gap, because both apps score 4.7 to 4.9 in every market, and
it is not a localisation gap, because both ship Spanish, French, Italian and
Portuguese. All seven Romance-language markets fall in the bottom ten.

That last observation is reported as a **hypothesis, not a result**. The
grouping was drawn after looking at the ranking, so the permutation test in
`scripts/analyse.py` measures how tight the cluster is, not whether the
explanation is right. Türkiye is the strongest market of all and does not fit
it, and Japan, South Africa and the UAE are weak without being Romance-language.

## Reproducing it

```bash
python3 scripts/pull_app_store.py > data/app-store-ratings.json
python3 scripts/pull_play.py      > data/play-ratings.json
python3 scripts/analyse.py
```

No dependencies beyond the standard library. The pulls take a few minutes,
mostly waiting between requests. `analyse.py` prints every figure quoted in the
report, including the permutation test and the Google Play comparison.

Data in `data/` was captured on **21 September 2026** and is included so the
numbers in the report can be checked without re-pulling.

## What this data cannot tell you

- **Apple publishes ratings, Google publishes reviews.** Shares are consistent
  within a store, which is what makes the comparison usable, but the absolute
  figures are not interchangeable between stores.
- **Play counts are global.** Google localises the star rating but not the
  review count, so Play can test whether satisfaction varies by market and
  cannot test whether reach does.
- **Ratings are a cumulative stock**, not current users and not momentum.
- **Ratings depend on how hard an app prompts for them.** That inflates the
  level, though it should be roughly uniform across countries and so cannot
  explain differences between markets.
- **Smallpdf is web-first.** Its own published data puts 61% of sessions on
  desktop, so all of this describes the mobile surface rather than the business.

Where an independent check was possible it agreed: Similarweb's head-to-head
figure for India puts Smallpdf at 13.27% of the two sites' combined web
traffic, against about 11% from App Store ratings.

One trap worth knowing if you repeat this. The package `com.smallpdf.android`
is **not** Smallpdf. It is an unrelated ad-supported app called "Small PDF
Converter" with about a thousand downloads. The real one is
`com.smallpdf.app.android`.

## Why this exists

Written as part of an application for a Growth & Product Analyst role at
Smallpdf. The value of it is the questions it raises rather than the answers,
and every one of them could be settled in a single query by someone with access
to the real numbers.

Loïs Patterson &middot; [digital twin](https://lois-digital-twin.vercel.app)
