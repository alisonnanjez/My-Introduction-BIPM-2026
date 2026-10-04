"""Builds journey_map.html, a standalone interactive map for the website.

Install once:   pip install folium
Run:            python make_journey_map.py
My code calculates the curved lines between stops with basic maths instead of the pyproj library from the notebook. The pyproj library wasn't installing properly on my setup, and I didn't need it, because the maths gives the same curved path. The difference from pyproj is too small to see on a map.pyproj treats the Earth as slightly squashed, which is more exact. My version treats it as a perfect sphere, which is accurate enough for a visual map and means one less library to install.
"""

# math provides sin, cos and similar functions. folium is the library that builds the map.
import math
import folium

# A list of places. Each stop is a dictionary (labelled data): name, latitude, longitude, and the text shown when a pin is clicked. This is the part to edit to change your journey.
stops = [
    {"city": "Limuru, Kenya", "lat": -1.1058, "lon": 36.6425,
     "popup": "Born and raised in Limuru 🏡"},
    {"city": "Juja, Kenya", "lat": -1.0912, "lon": 37.0117,
     "popup": "Studied BBIT degree at JKUAT 🎓"},
    {"city": "Nairobi, Kenya", "lat": -1.2921, "lon": 36.8219,
     "popup": "Worked at Absa Bank, KRA, Church World Service, RWS & Mindrift 💼"},
    {"city": "Berlin, Germany", "lat": 52.5200, "lon": 13.4050,
     "popup": "Masters degree at HWR Berlin 🏫"},
]


# Creates the base map. tiles is the web address that supplies the map pictures (Esri's, as in the shared notebook). attr is the credit text shown in the corner. zoom_start=2 is the starting zoom, but it gets overridden by fit_bounds at the end.
m = folium.Map(
    zoom_start=2,
    tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}",
    attr="Tiles &copy; Esri &mdash; Esri, HERE, Garmin, and contributors",
)

# A loop that goes through every stop and puts a blue pin on the map. popup appears on click, tooltip on hover.
for stop in stops:
    folium.Marker(
        [stop["lat"], stop["lon"]],
        popup=stop["popup"],
        tooltip=stop["city"],
        icon=folium.Icon(color="blue", icon="info-sign"),
    ).add_to(m)

# A function that works out 60 points along the shortest path between two places on a globe (a "great circle"). That is why the line from Kenya to Berlin curves. The maths converts degrees to radians, then spreads the points evenly between the two places.
def great_circle_points(lat1, lon1, lat2, lon2, npts=60):
    """Points along the shortest path between two places on the globe."""
    p1, l1, p2, l2 = map(math.radians, (lat1, lon1, lat2, lon2))
    d = 2 * math.asin(math.sqrt(
        math.sin((p2 - p1) / 2) ** 2
        + math.cos(p1) * math.cos(p2) * math.sin((l2 - l1) / 2) ** 2))
    if d == 0:
        return [(lat1, lon1), (lat2, lon2)]
    coords = []
    for i in range(npts + 1):
        f = i / npts
        a = math.sin((1 - f) * d) / math.sin(d)
        b = math.sin(f * d) / math.sin(d)
        x = a * math.cos(p1) * math.cos(l1) + b * math.cos(p2) * math.cos(l2)
        y = a * math.cos(p1) * math.sin(l1) + b * math.cos(p2) * math.sin(l2)
        z = a * math.sin(p1) + b * math.sin(p2)
        coords.append((math.degrees(math.atan2(z, math.hypot(x, y))),
                       math.degrees(math.atan2(y, x))))
    return coords


# zip(stops, stops[1:]) pairs each stop with the next one (1-2, 2-3, 3-4). For each pair it draws a line, so the journey is connected in order.
for start, end in zip(stops, stops[1:]):
    arc = great_circle_points(start["lat"], start["lon"], end["lat"], end["lon"])
    folium.PolyLine(arc, color="darkblue", weight=3, opacity=0.7).add_to(m)

# Zooms the map so every stop is visible at the start. The list comprehension is for building a list of coordinates.
m.fit_bounds([[s["lat"], s["lon"]] for s in stops])

# Writes the finished map to a standalone HTML file.
m.save("journey_map.html")
print("Saved journey_map.html")
