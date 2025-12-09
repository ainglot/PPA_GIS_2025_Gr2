import arcpy
import numpy as np

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
NoData = np.nan #wartość NoData - w tym rastrze minimalna wartość jest większa niż 0, można tak wykonać

# =============================================================================
# KONWERSJA RASTRA DO TABLICY NUMPY
# =============================================================================
R_array = arcpy.RasterToNumPyArray(R, nodata_to_value = NoData)
print(f"Min numpy: {np.nanmin(R_array)}, MAX: {np.nanmax(R_array)}")
print(f"Min numpy: {np.nanargmin(R_array)}, MAX: {np.nanargmax(R_array)}")
print(f"Liczba wierszy i liczba kolumn {R_array.shape}")

# =============================================================================
# ZNALEZIENIE POZYCJI MIN I MAX (indeksy w tablicy NumPy!)
# =============================================================================
# np.nanargmin zwraca indeks w "spłaszczonej" tablicy → trzeba go rozłożyć na wiersz i kolumnę
min_idx = np.unravel_index(np.nanargmin(R_array), R_array.shape)  # (wiersz, kolumna)
max_idx = np.unravel_index(np.nanargmax(R_array), R_array.shape)  # (wiersz, kolumna)

row_min, col_min = min_idx
row_max, col_max = max_idx

# =============================================================================
# PRZELICZENIE INDEKSÓW NUMPY NA WSPÓŁRZĘDNE GEOGRAFICZNE (środek piksela!)
# =============================================================================
def array_to_map_coordinates(array_row, array_col, lower_left_point, cell_size):
    """
    Konwertuje indeksy [wiersz, kolumna] w tablicy NumPy na współrzędne X, Y (środek piksela)
    """
    X = lower_left_point.X + (array_col * cell_size) + (cell_size / 2.0)
    # W NumPy wiersz 0 = góra rastra → trzeba odjąć od całkowitej liczby wierszy
    Y = lower_left_point.Y + ((R.height - 1 - array_row) * cell_size) + (cell_size / 2.0)
    return X, Y

# Współrzędne minimum
X_min, Y_min = array_to_map_coordinates(row_min, col_min, LewyDolnyPunkt, RozdzielczoscPrzestrzenna)

# Współrzędne maksimum
X_max, Y_max = array_to_map_coordinates(row_max, col_max, LewyDolnyPunkt, RozdzielczoscPrzestrzenna)

# =============================================================================
# WYŚWIETLENIE WYNIKÓW
# =============================================================================
print("\n" + "="*60)
print("           WYNIKI – POZYCJE MINIMUM I MAKSIMUM")
print("="*60)
print(f"Minimum wartości: {np.nanmin(R_array):.3f}")
print(f"   Piksel: wiersz = {row_min}, kolumna = {col_min}")
print(f"   Współrzędne środka piksela: X = {X_min:.3f}, Y = {Y_min:.3f} (EPSG:2180)")

print(f"\nMaksimum wartości: {np.nanmax(R_array):.3f}")
print(f"   Piksel: wiersz = {row_max}, kolumna = {col_max}")


# =============================================================================
# OBLICZENIA NA TABLICY NUMPY
# =============================================================================
# R_array[100:500, 100:200] = 100 # W lewym gónym rógó rastra "wycinamy" prostokąt

# =============================================================================
# ZAMIANA TABLICY NUMPY NA RASTER I ZAPISANIE DO NOWEGO PLIKU
# =============================================================================
# outR = arcpy.NumPyArrayToRaster(R_array, LewyDolnyPunkt, RozdzielczoscPrzestrzenna, value_to_nodata = NoData)
# # zapisać nowy raster trzeba podać - dane (R_array), współrzędne lewego dolnego naroża, rozdzielczość przestrzenną i jaką wartość przyjmuje NoData
# outR.save("NowyRaster05")
print("KONIEC")