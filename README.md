# IB Adhoc Tasks

Private repo containing the Melbourne Metrics prototype sketches site.

## Running the site locally (for walkthroughs)

The site is a static HTML/CSS/JS page. To show it during a walkthrough, run a local HTTP server from the `docs/` folder.

### One-time setup

None. Python 3 is already installed.

### Each session

Open a terminal, then:

```bash
cd C:/Users/trgal/IB-Adhoc-Tasks/docs && python -m http.server 8000
```

Open this URL in your browser:

```
http://localhost:8000
```

Leave the terminal running during the walkthrough. Press `Ctrl+C` in the terminal to stop the server when you're done.

### Why a local server and not just opening index.html?

A couple of interactions (tile-based view routing, Chart.js dashboard) work more reliably over HTTP than from `file://`. `python -m http.server` is built into Python, no install needed.

### If port 8000 is already in use

Use a different port, e.g. `python -m http.server 8080`, then visit `http://localhost:8080`.

## Folders

- **`docs/`** — static site (HTML, CSS, JS).

## Related

- **Private content:** https://github.com/trgallagher-research/Melbourne-Metrics (walkthrough script, Miro board builder)
