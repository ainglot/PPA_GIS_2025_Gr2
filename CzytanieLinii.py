import arcpy


# =============================================================================
# KONFIGURACJA DANYCH WEJŚCIOWYCH
# =============================================================================
arcpy.env.workspace = r"D:\GIS\Rok_2025_26\PPA_ArcGIS\PPA_Gr2.gdb"
warstwa_liniowa = "GDA2020_OT_SWRS_L"

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
lista_wsp = odczytywanie_wspolrzednych_do_listy(warstwa_liniowa)

def wstawianie_wspolrzednych(nowa_warstwa, uklad_wsp, lista_wsp):
    arcpy.management.CreateFeatureclass(arcpy.env.workspace, nowa_warstwa, "POINT", "", "DISABLED", "DISABLED", uklad_wsp)
    with arcpy.da.InsertCursor(nowa_warstwa, ["SHAPE@X", "SHAPE@Y"]) as cursor:
        for wsp in lista_wsp:
            # cursor.insertRow([wsp[0], wsp[1]])
            cursor.insertRow(wsp)

print(lista_wsp)
print(len(lista_wsp))

wstawianie_wspolrzednych("Centroidy_SWRS_01", warstwa_liniowa, lista_wsp)


print("KONIEC")