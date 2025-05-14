
# B-Spline Görbék Interaktív Megjelenítése és Approximációja

## Feladat Leírása

Dolgozzon ki egy eljárást, amellyel adott B-spline görbéhez alacsonyabb rendű B-spline görbe közelítést lehet adni! Vizsgálja meg a közelítés pontosságát! A felhasználó szabadon hozhat létre és mozgathat kontrollpontokat, illetve csúszkák segítségével állíthatja be a görbe fokszámát. A feladathoz hozzáadtam az alacsonyabb rendű görbében lévő kontrollpontok ideális újraszámolását legkisebb négyzetek módszerével.

## Funkcionalitás

- **B-spline görbe kirajzolása**: Kontrollpontokon áthaladó görbe vizualizálása
- **Kontrollpontok kezelése**:
  - Bal egérgombbal mozgatható
  - Jobb egérgombbal új pont adható hozzá
  - A kiválasztott kontrollpont törölhető a `Delete` vagy `Backspace` billentyűvel.
- **Interaktív csúszkák**:
  - B-spline fokszám (k)
  - Approximáló görbe fokszám (approx_k)
  - Globális approximáció (legkisebb négyzetek módszere)
  - Alacsonyabb fokszámú approximáció
- **Hibamérés**: Max és RMS hiba kiszámítása
- **Színes hibavizualizáció**: Nagyobb hibák pirosabb vonallal jelennek meg

## Számítási Módszerek

### B-spline görbe kiszámítása
A B-spline görbe pontjai a Cox-de Boor rekurziós képlet alapján kerülnek kiszámításra a bázisfüggvények (Ni,k​(t)) és a kontrollpontok súlyozott összegeként:

$$ C(t) = \sum_{i=0}^{n-1} P_i N_{i,k}(t) $$

Ahol:
- \(P_i\) az i. kontrollpont.
- \(N_{i,k}(t)\) az i. bázisfüggvény k renddel.
- \(t\) a paraméter.
- \(n\) a kontrollpontok száma.

A bázisfüggvények rekurzív definíciója:
- \( N_{i,1}(t) = 1 \text{ ha } t_i \leq t < t_{i+1} \), egyébként 0.
- \( N_{i,k}(t) = \frac{t - t_i}{t_{i+k-1} - t_i} N_{i,k-1}(t) + \frac{t_{i+k} - t}{t_{i+k} - t_{i+1}} N_{i+1,k-1}(t) \)

A megvalósítás egyenletesen elosztott csomópontokat használ a [0, 1] intervallumon.

### Approximáció (Least Squares Method)
Ez a módszer a legkisebb négyzetek elve alapján illeszt egy `approx_k` rendű B-spline görbét az eredeti görbére. Az eredeti görbéről vett mintapontokat használ célként, és egy lineáris egyenletrendszert old meg a közelítő görbe új kontrollpontjainak meghatározására a pszeudoinverz segítségével.

$$ P_{\text{approx}} = B^+ P_{\text{target}} $$

Ahol:
- \( B^+ \) a bázisfüggvények mátrixának pszeudoinverze.
- \( P_{\text{target}} \) az eredeti görbéről vett mintavételi pontok koordinátáit tartalmazó vektor.
- \( P_{\text{approx}} \) az approximált görbe kontrollpontjainak koordinátáit tartalmazó vektor.

### Hiba kiszámítása
A közelítés pontosságát az azonos \( t \) paraméterértékhez tartozó pontpárok euklideszi távolságával mérjük. Mind az eredeti, mind a közelítő görbét ugyanazon a paraméterlistán értékeljük ki, és a felelő pontok közötti távolságokat aggregáljuk:

- **Maximális hiba**: A legnagyobb euklideszi távolság a felelő pontpárok között.
- **RMS hiba**: A felelő pontpárok közötti euklideszi távolságok négyzetének átlagából vont négyzetgyök.

$$ \text{Max hiba} = \max_j |C_{\text{approx}}(t_j) - C_{\text{target}}(t_j)| $$

$$ \text{RMS hiba} = \sqrt{\frac{1}{N} \sum_{j=1}^{N} |C_{\text{approx}}(t_j) - C_{\text{target}}(t_j)|^2} $$

Ahol \( t_j \) a kiértékeléshez használt paraméterértékek listája, és \( N \) a kiértékelt pontok száma.



## Használati utasítás

### Indítás
Futtassa a `main.py` fájlt.

### Vezérlés
- **Bal egérgomb**: Pont kiválasztása és mozgatása.
- **Jobb egérgomb**: Új kontrollpont hozzáadása a kattintás helyén.
- **Delete vagy Backspace billentyű**: A kiválasztott kontrollpont törlése. (A kiválasztáshoz lenyomva kell tartani a bal egérgombot)
- **G billentyű**: A Legkisebb Négyzetek módszerrel számított approximáció megjelenítésének ki-/bekapcsolása.
- **A billentyű**: Az eredeti pontokkal, alacsonyabb renden számított approximáció megjelenítésének ki-/bekapcsolása (hibavizualizációval).
- **Csúszkák**: Az ablak alján lévő csúszkákkal interaktívan állítható az eredeti görbe (Original k) és az approximáló görbék (Approx k) rendje.

## Használt Technológiák

- **Python** – Programozási nyelv
- **Pygame** – Grafikus megjelenítés és interaktivitás
- **NumPy** – Mátrixműveletekhez és matematikai számításokhoz (különösen a pszeudoinverzhez és a pontok kezeléséhez)

## Telepítés
A szükséges függőségek telepítéséhez futtasd az alábbi parancsot:
```bash
pip install -r requirements.txt
```




