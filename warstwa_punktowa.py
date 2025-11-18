import arcpy

arcpy.env.workspace = r"D:\GIS\Rok_2025_26\PPA_ArcGIS\PPA_Gr2.gdb"
warstwa_punktowa = "GDA2020_OT_OIPR_P"

def odczytywanie_wspolrzednych_do_listy(warstwa):
    lista_wsp = []
    with arcpy.da.SearchCursor(warstwa, ["SHAPE@X", "SHAPE@Y"]) as cursor:
        for row in cursor:
            # print(f'{row[0]}, {row[1]}')
            lista_wsp.append([row[0], row[1]])
    return lista_wsp

print(odczytywanie_wspolrzednych_do_listy(warstwa_punktowa)[:50])

print("KONIEC")