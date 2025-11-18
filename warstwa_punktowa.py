import arcpy

arcpy.env.workspace = r"D:\GIS\Rok_2025_26\PPA_ArcGIS\PPA_Gr2.gdb"
warstwa_punktowa = "GDA2020_OT_OIPR_P"

with arcpy.da.SearchCursor(warstwa_punktowa, ["SHAPE@X", "SHAPE@Y"]) as cursor:
    for row in cursor:
        print(f'{row[0]}, {row[1]}')

print("KONIEC")