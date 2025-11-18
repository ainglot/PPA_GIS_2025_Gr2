import arcpy

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
    with arcpy.da.InsertCursor(warstwa, ["SHAPE@X", "SHAPE@Y"]) as cursor:
        for wsp in lista_wsp:
            cursor.insertRow([wsp[0], wsp[1]])

# lista_wsp_pkt = odczytywanie_wspolrzednych_do_listy(warstwa_punktowa)[:100]

# ## Tworzenie pustej nowej warstwy
# nowa_warstwa_pkt = "GDA2020_OT_OIPR_P_100pierwszych"
# arcpy.management.CreateFeatureclass(arcpy.env.workspace, nowa_warstwa_pkt, "POINT", "", "DISABLED", "DISABLED", warstwa_punktowa)

# wstawianie_wspolrzednych(nowa_warstwa_pkt, lista_wsp_pkt)

### Przetwarzanie pliku tekstowego do warstwy punktowej
### https://mostwiedzy.pl/pl/open-research-data/3d-point-cloud-as-a-representation-of-silo-tank,615070441641526-0

# wczytanie wszystkich współrzędnych do listy list
with open('data.txt', 'r') as f:
    points = [[float(v) for v in line.split()[:3]] for line in f if line.strip() and not line.startswith('#') and len(line.split()) == 3]

# wynik:
print(points[:20])

## Tworzenie pustej nowej warstwy
nowa_warstwa_pkt = "Silos02"
arcpy.management.CreateFeatureclass(arcpy.env.workspace, nowa_warstwa_pkt, "POINT", "", "DISABLED", "DISABLED", warstwa_punktowa)

wstawianie_wspolrzednych(nowa_warstwa_pkt, points)



print("KONIEC")