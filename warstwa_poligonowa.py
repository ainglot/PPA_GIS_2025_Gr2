import arcpy


# =============================================================================
# KONFIGURACJA DANYCH WEJŚCIOWYCH
# =============================================================================
arcpy.env.workspace = r"D:\GIS\Rok_2025_26\PPA_ArcGIS\PPA_Gr2.gdb"
warstwa_poligonowa = "Budynek"

# =============================================================================
# DEFINIOWAINE FUNKCJI DLA WARSTWY PUNKTOWEJ
# =============================================================================
def odczytywanie_wspolrzednych_poligonu(warstwa):
    lista_ob = []
    with arcpy.da.SearchCursor(warstwa, ["SHAPE@"]) as cursor:
        for row in cursor:
            # print(row)
            list_pkt = []
            for part in row[0]:
                # print(part)
                for pnt in part:
                    print(pnt)
                    # print(pnt.X, pnt.Y)
                    list_pkt.append([pnt.X, pnt.Y])
            lista_ob.append(list_pkt)
    return lista_ob

odczytywanie_wspolrzednych_poligonu(warstwa_poligonowa)



print("KONIEC")