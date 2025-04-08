# Féléves Feladat: B-Spline Görbék Interaktív Megjelenítése és Approximációja

## Feladat Leírása

Dolgozzon ki egy eljárást, amellyel adott B-spline görbéhez alacsonyabb rendű B-spline görbe közelítést lehet adni! Vizsgálja meg a közelítés pontosságát!
A felhasználó szabadon hozhat létre és mozgathat kontrollpontokat, illetve csúszkák segítségével állíthatja be a görbe fokszámát. A feladathoz hozzáadtam a az alacsonyabb rendű görbében lévő kontrollpontok ideális újraszámolását legkisebb négyzetek módszerével.

## Funkcionalitás

- **B-spline görbe kirajzolása**: kontrollpontokon áthaladó görbe vizualizálása
- **Kontrollpontok kezelése**:
  - Bal egérgombbal mozgatható
  - Jobb egérgombbal új pont adható hozzá
- **Interaktív csúszkák**:
  - B-spline fokszám (k)
  - Approximáló görbe fokszám (approx\_k)
- **Globális approximáció (legkisebb négyzetek módszere)**
- **Alacsonyabb fokszámú approximáció**
- **Hibamérés**: max és RMS hiba kiszámítása
- **Színes hibavizualizáció**: nagyobb hibák pirosabb vonallal jelennek meg

## Számítási Módszerek

### B-spline görbe kiszámítása

A B-spline görbe kiszámítása az alábbi képlettel történik:

```
N_{i,1}(t) = 1, ha t_i <= t < t_{i+1}
          = 0, egyébként

N_{i,k}(t) = ((t - t_i) / (t_{i+k-1} - t_i)) * N_{i,k-1}(t)
             + ((t_{i+k} - t) / (t_{i+k} - t_{i+1})) * N_{i+1,k-1}(t)
```

Ahol `t` a paraméter, `k` a fokszám, `N_{i,k}` pedig az i. bázisfüggvény.

### Approximáció (Least Squares Method)

A pontos görbe pontjait egy `B` nevű bázis mátrix szorozva egy `P` kontrollpont vektorral adja:

```
P_approx = pinv(B) @ P_target
```

Ahol:

- `pinv(B)` a B mátrix pszeudoinverze
- `P_target` a pontos B-spline mintavételi pontjai
- `P_approx` az approximált kontrollpontok

### Hiba kiszámítása

- **Max hiba**: a legnagyobb euklideszi távolság
- **RMS hiba**: gyök alatt az átlagos négyzetes eltérés

```
max_error = max(||P_original - P_approx||)
rms_error = sqrt(mean((P_original - P_approx)^2))
```

## Használati utasítás

- Bal klikk: pont kiválasztása és mozgatása
- Jobb klikk: új kontrollpont hozzáadása
- S billentyű: legkisebb négyzetek approximáció ki-/bekapcsolása
- A billentyű: alacsonyabb fokú approximáció ki-/bekapcsolása
- Csúszka: `k` és `approx_k` interaktív állítása (minimum érték: 2)

## Használt Technológiák

- **Python** – programozási nyelv
- **Pygame** – grafikus megjelenítés és interaktivitás
- **NumPy** – mátrixműveletekhez és matematikai számításokhoz

## Telepítés
A szükséges függőségek telepítéséhez futtasd az alábbi parancsot:
```bash
pip install -r requirements.txt

