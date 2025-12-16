import arcpy
import numpy as np

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
                    list_pkt.append([pnt.X, pnt.Y])
            lista_ob.append(list_pkt)
    return lista_ob

def punkt_na_rastrze(punkt, zakres_rastra):
    x, y = punkt
    xmin, ymin, xmax, ymax = zakres_rastra

    return xmin <= x <= xmax and ymin <= y <= ymax

def wstawianie_wspolrzednych(warstwa, lista_wsp):
    with arcpy.da.InsertCursor(warstwa, ["SHAPE@X", "SHAPE@Y", "SHAPE@Z"]) as cursor:
        for wsp in lista_wsp:
            # cursor.insertRow([wsp[0], wsp[1]])
            cursor.insertRow(wsp)

ListaWspLini = odczytywanie_wspolrzednych_linii_do_listy(warstwa_linie_ZTM)

# print(ListaWspLini)
arcpy.env.workspace = r"D:\GIS\Rok_2025_26\PPA_ArcGIS\NMT pod ZTM\ZTM197_NMT_TIF"
rasters = arcpy.ListRasters("*", "TIF")

ListaRastrow = []
for RasterIn in rasters:
    print(RasterIn)
    R = arcpy.Raster(RasterIn)
    print(R.extent.XMin, R.extent.YMin, R.extent.XMax, R.extent.YMax)
    ListaRastrow.append([RasterIn, [R.extent.XMin, R.extent.YMin, R.extent.XMax, R.extent.YMax]])

# print(ListaRastrow)

warstwa_punktow = []
PKT = [474113.5, 718874.19] # 63,119999
for ras in ListaRastrow:
    print(punkt_na_rastrze(PKT, ras[1]))
    if punkt_na_rastrze(PKT, ras[1]):
        R = arcpy.Raster(ras[0])
        R_array = arcpy.RasterToNumPyArray(R, nodata_to_value = np.nan)
        cellSIZE = R.meanCellWidth
        XMIN = ras[1][0]
        YMAX = ras[1][3]
        dx = int((PKT[0] - XMIN)/cellSIZE)
        dy = int((YMAX - PKT[1])/cellSIZE)
        print(dx, dy, R_array[dy, dx])
        if not np.isnan(R_array[dy, dx]):
            warstwa_punktow.append([dx, dy, R_array[dy, dx]])

## Tworzenie pustej nowej warstwy
arcpy.env.workspace = r"D:\GIS\Rok_2025_26\PPA_ArcGIS\Geobaza ZTM\ZTM197.gdb"
nowa_warstwa_pkt = "PunktNaRastrze01"
arcpy.management.CreateFeatureclass(arcpy.env.workspace, nowa_warstwa_pkt, "POINT", "", "DISABLED", "ENABLED", warstwa_linie_ZTM)
wstawianie_wspolrzednych(nowa_warstwa_pkt, warstwa_punktow)

print("KONIEC")