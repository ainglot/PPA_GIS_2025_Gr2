import arcpy


# =============================================================================
# KONFIGURACJA DANYCH WEJŚCIOWYCH
# =============================================================================
arcpy.env.workspace = r"D:\GIS\Rok_2025_26\PPA_ArcGIS\PPA_Gr2.gdb"
warstwa_poligonowa = "Budynki"

geometries = arcpy.management.CopyFeatures(warstwa_poligonowa, arcpy.Geometry())

i = 0
for geo1 in geometries:
    j = 0
    for geo2 in geometries:
        if i < j:
            print(i, j, geo1.touches(geo2))
        j += 1
    i += 1




# Otoczka = []
# for geo in geometries:
#     AREA = geo.area 
#     print(geo.area)
#     if AREA < 300:
#         geo2 = geo.buffer(1)
#         while geo2.area < 300:
#             geo2 = geo2.buffer(1)
#         Otoczka.append(geo2)
#     # else:
#     #     Otoczka.append(geo.buffer(1).convexHull())

# nowy_poligon = "Budynki_otoczka_04"
# arcpy.management.CopyFeatures(Otoczka, nowy_poligon)

print("KONIEC")