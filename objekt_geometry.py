import arcpy


# =============================================================================
# KONFIGURACJA DANYCH WEJŚCIOWYCH
# =============================================================================
arcpy.env.workspace = r"D:\GIS\Rok_2025_26\PPA_ArcGIS\PPA_Gr2.gdb"
warstwa_poligonowa = "Budynki"

geometries = arcpy.management.CopyFeatures(warstwa_poligonowa, arcpy.Geometry())

Otoczka = []
for geo in geometries:
    
    Otoczka.append(geo.convexHull())

nowy_poligon = "Budynki_otoczka_01"
arcpy.management.CopyFeatures(Otoczka, nowy_poligon)

print("KONIEC")