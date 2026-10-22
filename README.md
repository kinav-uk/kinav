# Kinav

Free tools and guides for families caring for an older parent in England.

- `app/` – the website (a mobile web app). Edit `page.html`, `app.js`, `content.js`, then run `python3 -I app/build.py` to make `index.html`.
- `app/data/` – care listings built from public CQC data (Good and Outstanding only).
- `update/` – scripts that download CQC data and rebuild `app/data/`.
- `.github/workflows/update-and-publish.yml` – every Monday GitHub downloads the latest CQC data, rebuilds the listings and republishes the site. It also republishes whenever changes are pushed. If the CQC download fails, the live site keeps the previous week's data and GitHub emails the owner.

Contains CQC data, published under the Open Government Licence.
