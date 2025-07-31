# Egyéni igényre szabható üzenetablakok

## A **`custom_messagebox`** modul ***`showinfo()`***, ***`showwarning()`***, ***`showerror()`***, ***`askyesno()`***, ***`askyesnocancel()`***, ***`askokcancel()`***, ***`askretrycancel()`***  és ***`askquestion()`*** függvényei segítségével egyéni igény szerinti kinézetű felugró üzenetablakokat hozhatunk létre. <br><br>Attól függően, hogy a felhasználó felé tartalmilag milyen üzenetet kívánunk közölni, négy fő ablaktípust jeleníthetünk meg: tájékoztató, figyelmeztető, hibajelző és kérdésfeltevő.

### Az üzenetablakokat létrehozó függvények jellemzői és paraméterezése
Az üzenetablakok szerkezete és kinézete hasonló. Az ablak felső részén a címsor, alul vízszintesen pedig egy vagy több nyomógomb látható. E kettő közötti terület bal felső részben  az üzenetfajtához illő ikongrafika, ettől jobbra az üzenetszöveget megjelenítő terület.

A **`showinfo()`**, **`showwarning()`** és **`showerror()`** függvényekkel létrehozható tájékoztató, figyelmeztető és hibajelző ablakok mindegyike egyetlen, OK feliratú gombot tartalmaz, minthogy ezeknél a felhasználónak csak tudomásul kell venni az üzenetet.

A kérdésfeltevő ablakok esetén legalább két gomb jelenik meg. Ugyanis, ahogy a neve is utal rá, ez az ablak választ vár, vagyis a felhasználónak az üzenet elolvasása után a felkínált gombok felirata által adott alternatívák alapján döntést kell hozni, és ennek megfelelő gombot kell lenyomni. Ennek hatására az ablak bezárul és az ablakot megjelenítő függvény valamilyen értékkel visszatér. Az **`askquestion()`** a megnyomott gombot azonosító karakterláncot (szimbolikus nevet) adja vissza. Az **`askyesno()`**,  **`askokcancel()`** és **`askretrycancel()`** eldöntendő (igen/nem) jellegű kérdést tesznek fel, ezért két gombot jelenítenek meg és a választól függően egy logikai értéket (`True`, `False`) adnak vissza. Az **`askyesnocancel()`**, minthogy ez három opciót kínál, a logikai értékek mellett a `None` is lehet visszatérési érték, ha a MÉGSE (Cancel) a választás.

A függvények paraméterezése hasonló módon történik: az ablak címét és a fő üzenet szövegét a `title` és `message` pozicionális argumentumokkal adhatjuk meg. 
Ezek mellett az alábbi kulcsszavas argumentumok használhatók:
  - `detail`: a fő üzenetet kiegészítő, részletező vagy magyarázó szöveg, amely a fő üzenet alatt jelenik meg.
  - `default`: egy megjelenített nyomógomb szimbólikus nevét kell megadni. Az ablak megjelenésekor ez a gomb kap fókuszt,
    és az Enter lenyomására is aktiválódik. Ha nincs megadva, alapértelmezés szerint a bal szélső gomb lesz fókuszban.
    Az érvényes szimbólikus nevek: 'ok', 'yes', 'no', 'cancel', 'retry', 'abort', 'ignore'.
  - `parent`: azt az ablakobjektumot adhatjuk meg, amely felett az üzenetablak megjelenik.
  - `command`: egy függvényt rendelhetünk hozzá, amely az ablak bezárásakor kerül meghívásra. Ez a függvény a lenyomott gomb
    szimbolikus nevét kapja argumentumként.
  - `type`: ezzel lehet beállítani az ablak típusát, ami meghatározza a megjelenő nyomógombok számát és feliratát.
    A megadható értékek: "ok", "okcancel", "yesno", "yesnocancel", "retrycancel", "abortretryignore".
    A type konfigurációs opció valójában csak a kérdésfeltevő ablakoknál érdekes, mert a többinél egyetlen OK gomb van.
    Továbbá, minthogy az askokcancel(), askretrycancel(), askyesno() és askyesnocancel() függvényeknél egyértelmű, hogy
    hány és milyen feliratú gomb fog megjelenni, ezért a type argumentum beállításának csak az askquestion() függvénynél
    van értelme. Ennél az alapértelmezett érték a "yesno".
  - `message_font`: a fő üzenet betűtípusa.
  - `message_fg_color`: a fő üzenet betűszíne.
  - `message_bg_color`: a fő üzenet háttérszíne.
  - `detail_font`: a részletező üzenetszöveg betűtípusa.
  - `detail_fg_color`: a részletező üzenetszöveg betűszíne.
  - `detail_bg_color`: a részletező üzenetszöveg háttérszíne.
  - `button_captions`: egy listát vagy tuple-t fogad, amelyben fel lehet sorolni az adott típusú ablakhoz tartozó
    nyomógombok feliratát. Az elemek sorrendje a gombok balról jobbra vett elhelyezési sorrendjével kell, hogy megegyezzen.
    Ha ez az argumentum nincs megadva, akkor az alapértelmezett feliratok láthatók. Ezeket kérdésfeltevő ablakok esetén
    egy modulkonstans tartalmazza az egyes kérdéstípusokhoz. A másik három ablakfajta esetén az alapértelmezett felirat az 'OK'.

A működéshez Python 3.10+ szükséges.

### Motiváció

A Python szabványos könyvtár `tkinter.messagebox` almoduljának függvényei segítségével felugró üzenetablakokat hozhatunk létre. Attól függően, hogy a felhasználó felé tartalmilag milyen jellegű üzenetet kívánunk közölni, négy fő ablaktípust jeleníthetünk meg: *tájékoztató*, *figyelmeztető*, *hibajelző* és *kérdésfeltevő*. Ezen ablakok szerkezete, felépítése sok hasonlóságot mutat. Amiben eltérnek az az üzenetfajtához illő ikongrafika, valamint a nyomógombok száma és felirata.

A `showinfo()`, `showwarning()`, `showerror()` függvényekkel létrehozható tájékoztató, figyelmeztető és hibajelző ablakok mindegyike egyetlen, OK feliratú gombot tartalmaz, minthogy ezeknél a felhasználónak csak tudomásul kell venni az üzenetet.

A kérdésfeltevő ablak esetén azonban legalább két gomb jelenik meg. Ugyanis, ahogy a neve is utal rá, ez az ablak választ vár, vagyis a felhasználónak az üzenet elolvasása után a felkínált gombok szövege által adott alternatívák alapján döntést kell hozni, és ennek megfelelő gombot kell lenyomni. Ennek hatására az ablak bezárul és az ablakot megjelenítő függvény valamilyen értékkel visszatér. Az `askquestion()` a megnyomott gombot azonosító karakterláncot (szimbolikus nevet) adja vissza. A többiek, amelyek eldöntendő (igen/nem) jellegű kérdést tesznek fel, két gombot jelenítenek meg és a választól függően egy logikai értéket (`True`, `False`) adnak vissza. Az `askyesnocancel()` esetén, minthogy három opciót kínál, a logikai értékek mellett a `None` is lehet visszatérési érték, ha a MÉGSE (Cancel) a választás.

A függvények paraméterezése hasonló: az ablak címét és a fő üzenet szövegét a `title` és `message` pozicionális argumentumokkal adhatjuk meg. Ezek mellett néhány kulcsszavas argumentum is használható:  

- a `detail` argumentummal a főüzenetet kiegészítő, részletező vagy magyarázó szöveg adható meg, amely a fő üzenet alatt jelenik meg.
- a `default` paraméterhez egy érvényes nyomógomb szimbólikus nevét rendelhetjük. Az ablak megjelenésekor ez a nyomógomb lesz fókuszban és az egérkattintáson felül az Enter lenyomására is aktiválódik. Ha ez az argumentum nincs megadva, akkor a bal szélső gomb lesz fókuszban.
- a `parent` argumentumnak azt az ablakobjektumot adhatjuk meg, amely felett az üzenetablak megjelenik.
- az `icon` paraméterrel beállítható, hogy a négy üzenetfajtához tartozó ikon közül melyik jelenjen meg. Mivel a létrehozófüggvények eleve az odaillő ikont használják, ezért e paraméternek nincs gyakorlati jelentősége.
- a `command` paraméternek egy függvényt lehet adni, ami az ablak bezárásakor lesz meghívva. E függvény a lenyomott gomb szimbolikus nevét kapja argumentumként. Korlát, hogy csak macOS platformon működik.
- a `type` argumentummal lehet beállítani az ablak típusát, ami meghatározza a megjelenő nyomógombok számát és feliratát. A megadható értékek: „ok”, „okcancel”, „yesno”, „yesnocancel”, „retrycancel”, „abortretryignore”. Ez a konfigurációs opció valójában csak a kérdésfeltevő ablakoknál érdekes, mert a többinél egyetlen OK gomb van. Továbbá, minthogy az `askokcancel()`, `askretrycancel()`, `askyesno()` és `askyesnocancel()` függvényeknél egyértelmű, hogy hány és milyen feliratú gomb fog megjelenni, ezért a `type` argumentum beállításának csak az `askquestion()` függvénynél van értelme. Itt egyébként az alapértelmezett érték a „yesno”.

A `tkinter.messagebox` üzenetablakai használhatók, de testreszabhatóságuk korlátozott: nem lehet módosítani az üzenetszövegek betűtípusát, -méretét, -vastagságát vagy -dőlését, és nem állítható sem a betűszín, sem a háttérszín. Ahogy korábban már említettük, a `command` argumentum sem működik minden platformon.

Ezért, ha alkalmazásunkban jobban olvasható, színesebb üzenetablakokra van szükség, érdemes egy olyan saját modult készíteni, amely hasonló funkcionalitású függvényeket kínál, de olyan üzenetablakokat jelenít meg, amelyek mentesek az említett korlátoktól.

## Tervezési és megvalósítási alapelvek

Az elején azért is foglaltuk össze a `tkinter.messagebox` üzenetablakok és létrehozófüggvényeik jellemzőit és paraméterezését, mert a saját készítésű változatokban is ezeket  alkalmazzuk, de a paraméterkészletet kibővítjük úgy, hogy mind a fő szöveg, mind a részletező szöveg betűtípusát, -méretét, kinézetét (vastagság, dőlés, aláhúzás) és színét, valamint a szöveg háttérszínét is meg lehessen a függvényhíváskor határozni, és a `command` paraméter is használható legyen.

Első lépésben a saját üzenetablak tartalmi elrendezését tervezzük meg. Ezt mutatja a következő ábra, amin látható, hogy a felső címsor alatti területet három zónára osztjuk: bal oldalon az ikongrafika, ettől jobbra a szövegeket tartalmazó terület. Ezek alatt pedig egy vízszintes sávban a nyomógombok helyezhetők el egymás után az ablak jobb széléhez igazítva.

![msgbox_desing.jpg](https://github.com/pythontudasepites/custom_messageboxes/blob/main/images/msgbox_desing.jpg)

Ami a tervezett elrendezés megvalósítását illeti, maga az üzenetablak egy `Toplevel` példány lesz, mert ezzel lehet a gyökérablaktól független ablakot megjeleníteni. Az egyes zónákat/részterületeket egy-egy keret (Frame widget) különíti el. Nem feltétlenül szükséges, de célszerű ezeket a kereteket egy főkeretben elrendezni és a főkeretet elhelyezni a `Toplevel` ablakban, mert így az ablak széleitől vett térközök beállítása egyszerűsödik.

Az üzenetablakot egy **`MessageBox`** nevű osztállyal építjük fel. Ebben egy `_build_messagebox_window()` nevű metódus felel az említett elrendezés megvalósításáért. Szó volt róla, hogy az eltérő üzenetfajtákra szánt ablakok elrendezése hasonló, csak az ikongrafikában és a nyomógombok számában és azok feliratában van eltérés. Ezért ezeket külön metódusok valósítják meg a `MessageBox` osztályban: az ikongrafikát a `_create_icon_graphics()`, a nyomógombokat a `_create_buttons()` metódus állítja elő és helyezi el. Ezeket hívja meg a `_build_messagebox_window()` metódus.

A `_create_icon_graphics()` metódusban az ikongrafika alapértelmezett megvalósítása a tájékoztató üzenet ikonja. Ezt nem egy megfelelő képfájl segítségével, hanem saját tervezésű egyszerű Canvas grafikával rajzoltatjuk ki. Így kevesebb függőség lesz és jogdíjkérdések sem merülnek fel. A `_create_buttons()` metódus a tájékoztató üzenetablaknak megfelelően egyetlen, OK feliratú gombot hoz létre és helyez el.

Az egyes üzenetfajákhoz tartozó ablakokat a `MessageBox` osztály alosztályai (**`InfoMessageBox`**, **`WarningMessageBox`**, **`ErrorMessageBox`** és **`QuestionMessageBox`**) valósítják meg. Az első három mindegyike egyetlen OK gombot jelenít meg, ami a szülőosztályban már implementált. Ezért ezek csak a  `_create_icon_graphics()` metódust írják felül a megfelelő ikongrafika megjelenítéséhez. A `QuestionMessageBox` osztályban azonban ez nem elég, mert a kérdéstípustól függően kell a megfelelő számú és feliratú gombot létrehozni és elhelyezni. Ezért ebben az osztályban a `_create_buttons()` metódust is felül kell írni.

Az üzenetablakok felugrását hangjelzés kíséri, amit a `MessageBox` osztály `_make_sound()` metódusa állít elő.

Az üzenetablakpéldányokat a `show()` metódus meghívásával lehet megjeleníteni. E metódus visszatérési értéke a a választott nyomógomb szimbólikus neve.

A `tkinter.messagebox` modulhoz hasonlóan a különböző típusú üzenetablakok létrehozására nem az előbb felsorolt osztályok közvetlen példányosítását kínáljuk, hanem erre szolgáló függvényeket. Tehát a saját egyéni modulunkban is definiáljuk a **`showinfo()`**, **`showwarning()`**, **`showerror()`**, **`askquestion()`**, **`askokcancel()`**, **`askretrycancel()`**, **`askyesno()`** és **`askyesnocancel()`** függvényeket. És ezek neveit egy listában felsorolva a modul `__all__` attribútumához rendeljük, jelezve, hogy ezek a nevek vannak nyilvános használatra szánva.

E függvényeknek a már említett `title`, `message`, `detail`, `default`, `parent`, `command` és `type` argumentumokon kívül megadhatók a `message_font`, `message_fg_color`, `message_bg_color`, `detail_font`, `detail_fg_color`, `detail_bg_color` és `button_captions` kulcsszavas argumentumok. Az új paraméterek közül az első hárommal meghatározható a fő üzenet betűtípusa, betűszíne és háttérszíne. A következő hárommal ugyanezen jellemzők állíthatók be a részletező szövegre vonatkozóan. A `button_captions` paraméter egy listát vagy tuple-t fogad, amelyben fel lehet sorolni az adott típusú ablakhoz tartozó nyomógombok feliratát. Az elemek sorrendje a gombok balról jobbra vett elhelyezési sorrendjével kell, hogy megegyezzen. Ha ez az argumentum nincs megadva, akkor az alapértelmezett feliratok láthatók. Ezeket kérdésfeltevő ablakok esetén egy modulkonstans tartalmazza az egyes kérdéstípusokhoz. A másik három ablakfajta esetén az alapértelmezett felirat az ‘OK’.

A osztályok és függvények definícióit a **`custom_messagebox`** nevű modul tartalmazza. A részletes kommentek segítik a működés megértését.

## Alkalmazási példák

Az alábbi képernyőképeken egyéni megjelenésű tájékoztató, hibajelző és figyelmeztető, valamint a különböző kérdésfeltevő üzenetablakok láthatók. Ez ezeket előállító tesztkódok a *tests* könyvtárban találhatók.
### Tájékoztató, hibajelző és figyelmeztető üzenetablakok
![info_error_warning_msgboxes.jpg](https://github.com/pythontudasepites/custom_messageboxes/blob/main/images/info_error_warning_msgboxes.jpg)

### Kérdésfeltevő üzenetablakok

![question_msgboxes.jpg](https://github.com/pythontudasepites/custom_messageboxes/blob/main/images/question_msgboxes.jpg)


