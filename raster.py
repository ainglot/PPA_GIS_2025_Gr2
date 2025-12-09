import arcpy

# =============================================================================
# KONFIGURACJA DANYCH WEJŚCIOWYCH
# =============================================================================
arcpy.env.workspace = r"D:\GIS\Rok_2025_26\PPA_ArcGIS\NMT"
RasterIn = "81008_1561328_N-34-50-C-d-3-3.asc"
arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(2180) #przypisanie układu współrzędnych do rastra wyjściowego

# =============================================================================
# WCZYTYWANIE RASTRA PRZEZ ARCPY DO OBIEKTU "RASTER"
# =============================================================================
R = arcpy.Raster(RasterIn)
print(f"Min rastra: {R.minimum}, Max: {R.maximum}")
print(f"Rozdzielczość przestrzenna: {R.meanCellWidth}")

# =============================================================================
# POBIERAMY PARAMETRY RASTRA
# =============================================================================
LewyDolnyPunkt = arcpy.Point(R.extent.XMin, R.extent.YMin) #przechowanie współrzędnych do lokalizacji rastra wyjściowego
RozdzielczoscPrzestrzenna = R.meanCellWidth #rozdzielczość przestrzenna rastra
NoData = -10 #wartość NoData - w tym rastrze minimalna wartość jest większa niż 0, można tak wykonać

# =============================================================================
# KONWERSJA RASTRA DO TABLICY NUMPY
# =============================================================================
R_array = arcpy.RasterToNumPyArray(R, nodata_to_value = NoData)

# =============================================================================
# OBLICZENIA NA TABLICY NUMPY
# =============================================================================
R_array[100:200, 100:200] = -10 # W lewym gónym rógó rastra "wycinamy" prostokąt

# =============================================================================
# ZAMIANA TABLICY NUMPY NA RASTER I ZAPISANIE DO NOWEGO PLIKU
# =============================================================================
outR = arcpy.NumPyArrayToRaster(R_array, LewyDolnyPunkt, RozdzielczoscPrzestrzenna, value_to_nodata = NoData)
# zapisać nowy raster trzeba podać - dane (R_array), współrzędne lewego dolnego naroża, rozdzielczość przestrzenną i jaką wartość przyjmuje NoData
outR.save("NowyRaster01")
print("KONIEC")