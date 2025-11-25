import arcpy


# =============================================================================
# KONFIGURACJA DANYCH WEJŚCIOWYCH
# =============================================================================
arcpy.env.workspace = r"D:\GIS\Rok_2025_26\PPA_ArcGIS\PPA_Gr2.gdb"
warstwa_2014 = "GDA2014_OT_SWRS_L"
warstwa_2020 = "GDA2020_OT_SWRS_L"

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


lista_2014 = odczytywanie_wspolrzednych_linii_do_listy(warstwa_2014)
lista_2020 = odczytywanie_wspolrzednych_linii_do_listy(warstwa_2020)

from collections import defaultdict

def compare_lines_and_tag_points(lista_2014, lista_2020, tolerance=0.001):
    """
    Porównuje punkty z dwóch warstw (2014 i 2020) z małą tolerancją na błędy zmiennoprzecinkowe.
    Zwraca lista_2020 z dodanym atrybutem 'status' do każdego punktu.
    """
    
    # Słownik: klucz = zaokrąglone współrzędne (x, y), wartość = zbiór lat
    point_to_years = defaultdict(set)
    
    def round_point(p, tol=tolerance):
        return (round(p[0]/tol)*tol, round(p[1]/tol)*tol)  # "grid" co 0.001 m (dostosuj tolerancję)
    
    # Zbieramy wszystkie punkty z obu warstw
    for line in lista_2014:
        for point in line:
            key = round_point(point)
            point_to_years[key].add(2014)
    
    for line in lista_2020:
        for point in line:
            key = round_point(point)
            point_to_years[key].add(2020)
    
    # Teraz tagujemy punkty w lista_2020
    tagged_2020 = []
    for line in lista_2020:
        new_line = []
        for point in line:
            key = round_point(point)
            years = point_to_years[key]
            
            if 2014 in years and 2020 in years:
                status = 'both'
            elif 2014 in years:
                status = '2014_only'   # punkt był w 2014, ale nie ma go dokładnie w 2020 (blisko, ale nie identycznie)
            else:
                status = '2020_only'
            
            # Dodajemy punkt jako dict z atrybutem
            point_dict = {
                'x': point[0],
                'y': point[1],
                'status': status
            }
            new_line.append(point_dict)
        tagged_2020.append(new_line)
    
    return tagged_2020

# print(lista_wsp[-1])
# print(len(lista_wsp))

# thinned_lines = [
#     line if len(line) <= 2 else line[::2] + ([line[-1]] if len(line) % 2 == 0 else [])
#     for line in lista_wsp
# ]

# wstawianie_wspolrzednych("Centroidy_SWRS_01", warstwa_liniowa, lista_wsp)
# wstawianie_wspolrzednych_linii("Linie_SWRS_04", warstwa_liniowa, thinned_lines)

print("KONIEC")