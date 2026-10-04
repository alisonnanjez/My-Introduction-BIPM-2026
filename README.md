# My Introduction

A personal "About Me" website with a kind of Wikipedia-style layout, collapsible
sections, and an interactive map of my work and education journey.

**Live site:** https://yourusername.github.io/your-repo/

## Features
- Collapsible sections built with `<details>` and `<summary>`
- Tables for work and education history
- Interactive journey map (Kenya to Berlin) generated with Python
- Styling kept in one external CSS file

## Built with
- HTML and CSS
- Python with [folium](https://python-visualization.github.io/folium/)
  (which uses Leaflet.js) for the map

## Project structure
| File | Purpose |
|---|---|
| `index.html` | Main page (content) |
| `style.css` | All styling |
| `make_journey_map.py` | Script that generates the map |
| `journey_map.html` | The generated map, embedded in the page |
| `Photos/`, `About Alison Photos/` | Images used on the page |

## How to run
1. Open `index.html` in a browser (or visit the live site).
2. To change the map, edit the `stops` list in `make_journey_map.py`, then run:
   `pip install folium` and `python make_journey_map.py`

## Credits
- Map tiles © Esri, HERE, Garmin and contributors
- Map library: Leaflet, via folium

## Author
Alison Wekesa