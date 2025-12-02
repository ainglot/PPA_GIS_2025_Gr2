import arcpy


# =============================================================================
# KONFIGURACJA DANYCH WEJŚCIOWYCH
# =============================================================================
arcpy.env.workspace = r"D:\GIS\Rok_2025_26\PPA_ArcGIS\PPA_Gr2.gdb"
warstwa_poligonowa = "Budynek"

# =============================================================================
# DEFINIOWAINE FUNKCJI DLA WARSTWY PUNKTOWEJ
# =============================================================================

## [Linia1[pkt1[x1, y1], pkt2[x2, y2]....], Linia2[]...]
## [Poligon1[graniece[pkt1[x1, y1], pkt2[x2, y2]....], dziure[pkt1[x1, y1], pkt2[x2, y2]....]], ...]
def odczytywanie_wspolrzednych_poligonu(warstwa):
    lista_ob = []
    with arcpy.da.SearchCursor(warstwa, ["SHAPE@"]) as cursor:
        for row in cursor:
            # print(row)
            list_part = []
            for part in row[0]:
                # print(part)
                lista_pkt = []
                for pnt in part:
                    print(pnt)
                    if pnt:
                        lista_pkt.append([pnt.X, pnt.Y])
                    else:
                        list_part.append(lista_pkt)
                        lista_pkt = []
                list_part.append(lista_pkt)
            lista_ob.append(list_part)
    return lista_ob

listaPOLIGONU = odczytywanie_wspolrzednych_poligonu(warstwa_poligonowa)

print(listaPOLIGONU)

print("KONIEC")