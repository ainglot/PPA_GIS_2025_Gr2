import arcpy
from collections import defaultdict
import numpy as np  # opcjonalnie, ale bardzo przydatne
import statistics   # wbudowane w Pythonie

# =============================================================================
# KONFIGURACJA DANYCH WEJŚCIOWYCH
# =============================================================================
arcpy.env.workspace = r"D:\GIS\Rok_2025_26\PPA_ArcGIS\PPA_Gr2.gdb"
warstwa_punktowa = "GDA2020_OT_OIPR_P"

# =============================================================================
# DEFINIOWAINE FUNKCJI DLA WARSTWY PUNKTOWEJ
# =============================================================================
def odczytywanie_wspolrzednych_do_listy(warstwa):
    lista_wsp = []
    with arcpy.da.SearchCursor(warstwa, ["SHAPE@X", "SHAPE@Y"]) as cursor:
        for row in cursor:
            # print(f'{row[0]}, {row[1]}')
            lista_wsp.append([row[0], row[1]])
    return lista_wsp

def aktualizacja_wspolrzednych(warstwa):
    with arcpy.da.UpdateCursor(warstwa, ["SHAPE@X", "SHAPE@Y"]) as cursor:
        for row in cursor:
            # print(f'{row[0]}, {row[1]}')
            row[0] += 100
            row[1] += 100
            cursor.updateRow(row)

def wstawianie_wspolrzednych(warstwa, lista_wsp):
    with arcpy.da.InsertCursor(warstwa, ["SHAPE@X", "SHAPE@Y", "SHAPE@Z"]) as cursor:
        for wsp in lista_wsp:
            # cursor.insertRow([wsp[0], wsp[1]])
            cursor.insertRow(wsp)

# lista_wsp_pkt = odczytywanie_wspolrzednych_do_listy(warstwa_punktowa)[:100]

# ## Tworzenie pustej nowej warstwy
# nowa_warstwa_pkt = "GDA2020_OT_OIPR_P_100pierwszych"
# arcpy.management.CreateFeatureclass(arcpy.env.workspace, nowa_warstwa_pkt, "POINT", "", "DISABLED", "DISABLED", warstwa_punktowa)

# wstawianie_wspolrzednych(nowa_warstwa_pkt, lista_wsp_pkt)

### Przetwarzanie pliku tekstowego do warstwy punktowej
### https://mostwiedzy.pl/pl/open-research-data/3d-point-cloud-as-a-representation-of-silo-tank,615070441641526-0
dx, dy, dz = 470879, 741121, 0
# wczytanie wszystkich współrzędnych do listy list
with open('data.txt', 'r') as f:
    points = [
        [float(v) + dx if i == 0 else 
         float(v) + dy if i == 1 else 
         float(v) + dz 
         for i, v in enumerate(line.split()[:3])]
        for line in f 
        if line.strip() and not line.startswith('#') and len(line.split()) == 3
    ]

# # wynik:
# print(points[:20])

# ## Tworzenie pustej nowej warstwy
# nowa_warstwa_pkt = "Silos04"
# arcpy.management.CreateFeatureclass(arcpy.env.workspace, nowa_warstwa_pkt, "POINT", "", "DISABLED", "ENABLED", warstwa_punktowa)

# wstawianie_wspolrzednych(nowa_warstwa_pkt, points)


# Przykład: Twoja lista punktów
# points = [[x1,y1,z1], [x2,y2,z2], ...]

# 1. Znajdź min i max z
z_values = [p[2] for p in points]
min_z = min(z_values)
max_z = max(z_values)

# 2. Grupowanie co 2 jednostki (przedziały [min_z, min_z+2), [min_z+2, min_z+4), ...)
layers = defaultdict(list)  # klucz: początek przedziału, wartość: lista [x,y]

for x, y, z in points:
    layer_start = (z - min_z) // 2 * 2 + min_z   # zaokrągla w dół do wielokrotności 2
    layers[layer_start].append([x, y])

# 3. Oblicz średnie dla każdego przedziału
result = []
for z_start in sorted(layers):
    z_end = z_start + 2
    xs, ys = zip(*layers[z_start])        # rozpakowujemy osobno x i y
    coords = layers[z_start]

    median_x = statistics.median(xs)
    median_y = statistics.median(ys)
    avg_x = sum(x for x, y in coords) / len(coords)
    avg_y = sum(y for x, y in coords) / len(coords)
    count = len(coords)
    result.append({
        'z_range': (z_start, z_end),
        'center_z': (z_start + z_end) / 2,
        'avg_x': avg_x,
        'avg_y': avg_y,
        'median_x': median_x,
        'median_y': median_y,
        'count': count
    })

nowe_sr_wsp = []
# Wydrukuj ładnie
for r in result:
    print(f"Z: [{r['z_range'][0]:.3f}, {r['z_range'][1]:.3f}) → średnie (x,y) = ({r['avg_x']:.3f}, {r['avg_y']:.3f})  [{r['count']} pkt]")
    # nowe_sr_wsp.append([r['avg_x'], r['avg_y'], r['z_range'][0]+1])
    nowe_sr_wsp.append([r['median_x'], r['median_y'], r['z_range'][0]+1])
print(nowe_sr_wsp)

## Tworzenie pustej nowej warstwy
nowa_warstwa_pkt = "Silos_sr_02"
arcpy.management.CreateFeatureclass(arcpy.env.workspace, nowa_warstwa_pkt, "POINT", "", "DISABLED", "ENABLED", warstwa_punktowa)

wstawianie_wspolrzednych(nowa_warstwa_pkt, nowe_sr_wsp)

print("KONIEC")