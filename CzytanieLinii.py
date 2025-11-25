import arcpy


# =============================================================================
# KONFIGURACJA DANYCH WEJŚCIOWYCH
# =============================================================================
arcpy.env.workspace = r"D:\GIS\Rok_2025_26\PPA_ArcGIS\PPA_Gr2.gdb"
warstwa_liniowa = "GDA2020_OT_SWRS_L"

# =============================================================================
# DEFINIOWAINE FUNKCJI DLA WARSTWY PUNKTOWEJ
# =============================================================================
def odczytywanie_wspolrzednych_linii_do_listy(warstwa):
    lista_ob = []
    with arcpy.da.SearchCursor(warstwa, ["SHAPE@"]) as cursor:
        for row in cursor:
            print(row)
            list_pkt = []
            for part in row[0]:
                print(part)
                for pnt in part:
                    print(pnt.X, pnt.Y)
                    list_pkt.append([pnt.X, pnt.Y])
            lista_ob.append(list_pkt)
    return lista_ob
lista_wsp = odczytywanie_wspolrzednych_linii_do_listy(warstwa_liniowa)

def wstawianie_wspolrzednych_linii(nowa_warstwa, uklad_wsp, lista_obiektow):
    arcpy.management.CreateFeatureclass(arcpy.env.workspace, nowa_warstwa, "POLYLINE", "", "DISABLED", "DISABLED", uklad_wsp)
    with arcpy.da.InsertCursor(nowa_warstwa, ["SHAPE@"]) as cursor:
        pnt = arcpy.Point()
        array = arcpy.Array()
        for ob in lista_obiektow:
            for pkt in ob:
                pnt.X = pkt[0]
                pnt.Y = pkt[1]
                array.add(pnt)
            pol = arcpy.Polyline(array)
            array.removeAll()
            # cursor.insertRow([wsp[0], wsp[1]])
            cursor.insertRow([pol])

print(lista_wsp[-1])
print(len(lista_wsp))

# wstawianie_wspolrzednych("Centroidy_SWRS_01", warstwa_liniowa, lista_wsp)
wstawianie_wspolrzednych_linii("Linie_SWRS_01", warstwa_liniowa, lista_wsp)

print("KONIEC")