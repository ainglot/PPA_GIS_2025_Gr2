# Skrypty ArcPy do analizy GIS (PPA Gr2)

Witaj! 👋  
To repozytorium zawiera trzy skrypty Python (ArcPy) wykorzystywane podczas zajęć z Przetwarzania i Analizy Danych Przestrzennych na Politechnice Gdańskiej (grupa 2).

## Zawartość

- **analiza_zmian.py**  
  Analizuje zmiany pokrycia terenu między latami 2014 a 2020.  
  - Tworzy warstwy połączone (Merge) i przecięcia (Intersect)  
  - Oblicza powierzchnię i procent zmian dla każdej klasy  
  - Generuje wykresy słupkowe i kołowe, zapisuje jako JPG  
  - Wymagania: `arcpy`, `matplotlib`

- **import_shapefiles.py**  
  Masowy, bezpieczny import shapefile'ów do geobazy plikowej (.gdb).  
  - Automatycznie czyści nazwy plików (kropki → podkreślenia)  
  - Sprawdza, czy warstwa już istnieje – importuje tylko nowe  
  - Szczegółowe logowanie i obsługa błędów  

- **warstwa_punktowa.py** **NOWOŚĆ**  
  Przetwarzanie chmur punktów 3D (np. z naziemnego skaningu laserowego) na uproszczoną warstwę punktową z średnimi/medianami współrzędnych w poziomach wysokościowych.  
  ### Główne funkcjonalności:
  - Wczytywanie dużych plików tekstowych XYZ (np. `data.txt`)  
  - Przesunięcie układu współrzędnych o wektor DX/DY/DZ  
  - Grupowanie punktów w poziome „warstwy” co 2 metry wysokości (Z)  
  - Obliczanie dla każdej warstwy:  
    - średnie i mediany X/Y  
    - liczba punktów w przedziale  
    - środkowa wysokość Z  
  - Tworzenie nowej warstwy punktowej w geobazie z punktami reprezentującymi średnie/mediany każdej warstwy  
  ### Zastosowanie:
  Idealny do analizy obiektów pionowych (np. silosów, wież, kominów, elewacji) – redukuje miliony punktów chmury do kilkudziesięciu charakterystycznych punktów na poziomach.

  **Przykład użycia w skrypcie**:  
  Przetwarzanie chmury punktów silosu (`Silos04`) → warstwa `Silos_sr_02` z punktami co 2 m wysokości.

## Jak uruchomić

1. Zainstaluj **ArcGIS Pro** (wersja ≥ 3.0)  
2. Otwórz projekt z geobazą `PPA_Gr2.gdb`  
3. Edytuj ścieżki w skryptach (workspace, nazwy warstw, ścieżka do pliku `data.txt` jeśli używasz `warstwa_punktowa.py`)  
4. Uruchom skrypt w **Python Window** w ArcGIS Pro lub jako zewnętrzny plik `.py`

## Wymagania

- Python 3.11.11 + ArcPy 3.5.2 (domyślnie z ArcGIS Pro)
- Biblioteki wbudowane + opcjonalnie: `numpy`, `statistics`, `collections`
- Dane wejściowe:
  - Geobaza `.gdb`
  - Shapefile'y (dla `import_shapefiles.py`)
  - Pliki tekstowe XYZ (dla `warstwa_punktowa.py`)

## Autor

- **Adam Inglot** – GIS Developer, adiunkt PG  
- Kontakt: [ainglotpg@gmail.com](mailto:ainglotpg@gmail.com)  
- LinkedIn: [linkedin.com/in/adam-inglot](https://linkedin.com/in/adaminglot)

## Licencja

**MIT License** – możesz dowolnie używać, modyfikować i rozpowszechniać.

---

Dzięki za wizytę w repozytorium! 🚀  
Jeśli masz pomysły na nowe funkcjonalności lub znalazłeś błąd – otwórz Issue lub Pull Request.  
Powodzenia na kolokwium z PPA! 😉