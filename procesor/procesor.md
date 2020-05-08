### Pamięć podręczna
- **L-1 cache** - pamięć podręczna pierwszego poziomu - przyśpiesza dostep do bloków pamięci wyższego poziomu (pamięć operacyjna lub pamięć podreczna L2, zależne od konstrukcji). 
    * zawsze najmniejsza,
    * najbliżej jąda, najszybsza komunikacja,
     * 2-drożne pamięci L1, rozdzielona pamięć danych i kodu, 
     * długość linii to 64 bajty.
- **L-2 cache** - pamięć drugiego poziomu wykorzystywana jako bufor pomiędzy wolna pamięcia RAM, a jądrem procesor i pamięcią L1.
    * rozmiar  64 KB do 12 MB
     * 2, 4, 8 drożne
     * długość linii to 64-128 bajty.
- **L-3 cache** - pamięć trzeciego poziomu jest wykorzystywana gdy L2 jest niewystarczająca aby pomieścić potrzebne dane. Pozwala na znacząca poprawę wydajności w stosunku do procesorów z dwupoziomową pamięcią cache.
    * rozmiar od kilku do kilkudziesięciu MB

### Laptop
Procesor Intel i5-8250U - ósmej generacji w litografii 14nm
- Liczba rdzeni: 4
- Liczba wątków: 8
- Bazowa częstotliwośc procesora: 1.60GHz
- Maks. częstotliwość turbo: 3,40GHz (**maks. częstotliwość jednego rdzenia**)
- Obsługiwany RAM: 2 kanały DDR4-2400, LPDDR3-2133, max 32GB
- Zintegrowany układ graficzny UHD Intel 620
- Cache: 6 MB Intel SMart Cache - umożliwia dynamiczne współdzielenie pamięci podręcznej ostaniego poziomu pomiędzy wszystikimi rdzeniami.
    * L1 - 256KB
    * L2 - 1MB
    * L3 - 6MB
- Socket: FC_BGA1356

---

### Raspbery Pi
Procesor ARM Cortex-A53:
[INFO](https://en.wikichip.org/wiki/arm_holdings/microarchitectures/cortex-a53)
- Liczba rdzeni: 4
- Częstotliwość: 1.2GHz
- Cache - dwupoziomowy
    * L1 - 8-64 KB
    * L2 - 128KB-2MB