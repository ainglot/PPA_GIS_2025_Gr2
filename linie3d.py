import arcpy


# =============================================================================
# KONFIGURACJA DANYCH WEJŚCIOWYCH
# =============================================================================
arcpy.env.workspace = r"D:\GIS\Rok_2025_26\PPA_ArcGIS\Geobaza ZTM\ZTM197.gdb"
warstwa_linie_ZTM = "ZTM_195_PL92"

# =============================================================================
# DEFINIOWAINE FUNKCJI DLA WARSTWY PUNKTOWEJ
# =============================================================================
def odczytywanie_wspolrzednych_linii_do_listy(warstwa):
    lista_ob = []
    with arcpy.da.SearchCursor(warstwa, ["SHAPE@"]) as cursor:
        for row in cursor:
            list_pkt = []
            for part in row[0]:
                for pnt in part:
                    print(pnt.X, pnt.Y)
                    list_pkt.append([pnt.X, pnt.Y])
            lista_ob.append(list_pkt)
    return lista_ob

def punkt_na_rastrze(punkt, zakres_rastra):
    x, y = punkt
    xmin, ymin, xmax, ymax = zakres_rastra

    return xmin <= x <= xmax and ymin <= y <= ymax

ListaWspLini = odczytywanie_wspolrzednych_linii_do_listy(warstwa_linie_ZTM)

print(ListaWspLini)
arcpy.env.workspace = r"D:\GIS\Rok_2025_26\PPA_ArcGIS\NMT pod ZTM\ZTM197_NMT_TIF"
rasters = arcpy.ListRasters("*", "TIF")

ListaRastrow = []
for RasterIn in rasters:
    print(RasterIn)
    R = arcpy.Raster(RasterIn)
    print(R.extent.XMin, R.extent.YMin, R.extent.XMax, R.extent.YMax)
    ListaRastrow.append([RasterIn, [R.extent.XMin, R.extent.YMin, R.extent.XMax, R.extent.YMax]])

print(ListaRastrow)

PKT = [474113.5, 718874.19] # 63,119999
for ras in ListaRastrow:
    punkt_na_rastrze(punkt, zakres_rastra)

print("KONIEC")