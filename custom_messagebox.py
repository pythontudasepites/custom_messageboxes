"""A modul függvényei segítségével felugró üzenetablakokat hozhatunk létre. Attól függően, hogy a felhasználó felé tartalmilag
milyen üzenetet kívánunk közölni, négy fő ablaktípust jeleníthetünk meg: tájékoztató, figyelmeztető, hibajelző és kérdésfeltevő.

Az üzenetablakok szerkezete, felépítése sok hasonlóságot mutat. Amiben eltérnek az az üzenetfajtához illő ikongrafika, valamint
a nyomógombok száma és felirata.

A showinfo(), showwarning(), showerror() függvényekkel létrehozható tájékoztató, figyelmeztető és hibajelző ablakok mindegyike
egyetlen, OK feliratú gombot tartalmaz, minthogy ezeknél a felhasználónak csak tudomásul kell venni az üzenetet.

A kérdésfeltevő ablakok esetén azonban legalább két gomb jelenik meg. Ugyanis, ahogy a neve is utal rá, ez az ablak
választ vár, vagyis a felhasználónak az üzenet elolvasása után a felkínált gombok felirata által adott alternatívák alapján
döntést kell hozni, és ennek megfelelő gombot kell lenyomni. Ennek hatására az ablak bezárul és az ablakot megjelenítő függvény
valamilyen értékkel visszatér. Az askquestion() a megnyomott gombot azonosító karakterláncot (szimbolikus nevet) adja vissza.
A többiek, amelyek eldöntendő (igen/nem) jellegű kérdést tesznek fel, két gombot jelenítenek meg és a választól függően egy
logikai értéket (True, False) adnak vissza. Kivétel az askyesnocancel(), minthogy ez három opciót kínál, a logikai értékek
mellett a None is lehet visszatérési érték, ha a MÉGSE (Cancel) a választás.

A függvények paraméterezése hasonló módon történik: az ablak címét és a fő üzenet szövegét a title és message pozicionális
argumentumokkal adhatjuk meg. Ezek mellett néhány kulcsszavas argumentum is használható:
  - detail: a fő üzenetet kiegészítő, részletező vagy magyarázó szöveg, amely a fő üzenet alatt jelenik meg.
  - default: egy megjelenített nyomógomb szimbólikus nevét kell megadni. Az ablak megjelenésekor ez a gomb kap fókuszt,
    és az Enter lenyomására is aktiválódik. Ha nincs megadva, alapértelmezés szerint a bal szélső gomb lesz fókuszban.
    Az érvényes szimbólikus nevek: 'ok', 'yes', 'no', 'cancel', 'retry', 'abort', 'ignore'.
  - parent: azt az ablakobjektumot adhatjuk meg, amely felett az üzenetablak megjelenik.
  - command: egy függvényt rendelhetünk hozzá, amely az ablak bezárásakor kerül meghívásra. Ez a függvény a lenyomott gomb
    szimbolikus nevét kapja argumentumként.
  - type: ezzel lehet beállítani az ablak típusát, ami meghatározza a megjelenő nyomógombok számát és feliratát.
    A megadható értékek: "ok", "okcancel", "yesno", "yesnocancel", "retrycancel", "abortretryignore".
    A type konfigurációs opció valójában csak a kérdésfeltevő ablakoknál érdekes, mert a többinél egyetlen OK gomb van.
    Továbbá, minthogy az askokcancel(), askretrycancel(), askyesno() és askyesnocancel() függvényeknél egyértelmű, hogy
    hány és milyen feliratú gomb fog megjelenni, ezért a type argumentum beállításának csak az askquestion() függvénynél
    van értelme. Ennél az alapértelmezett érték a "yesno".
  - message_font: a fő üzenet betűtípusa.
  - message_fg_color: a fő üzenet betűszíne.
  - message_bg_color: a fő üzenet háttérszíne.
  - detail_font: a részletező üzenetszöveg betűtípusa.
  - detail_fg_color: a részletező üzenetszöveg betűszíne.
  - detail_bg_color: a részletező üzenetszöveg háttérszíne.
  - button_captions: egy listát vagy tuple-t fogad, amelyben fel lehet sorolni az adott típusú ablakhoz tartozó
    nyomógombok feliratát. Az elemek sorrendje a gombok balról jobbra vett elhelyezési sorrendjével kell, hogy megegyezzen.
    Ha ez az argumentum nincs megadva, akkor az alapértelmezett feliratok láthatók. Ezeket kérdésfeltevő ablakok esetén
    egy modulkonstans tartalmazza az egyes kérdéstípusokhoz. A másik három ablakfajta esetén az alapértelmezett felirat az 'OK'.

A működéshez Python 3.10+ szükséges.
"""
import tkinter as tk
import winsound

__all__ = ["showinfo", "showwarning", "showerror",
           "askquestion", "askokcancel", "askyesno", "askyesnocancel", "askretrycancel"]

QUESTION_TYPES_TO_DEFAULT_BUTTONCAPTIONS = {'okcancel': ['OK', 'MÉGSE'], 'yesno': ['IGEN', 'NEM'],
                                            'yesnocancel': ['IGEN', 'NEM', 'MÉGSE'], 'retrycancel': ['ÚJRA', 'MÉGSE'],
                                            'abortretryignore': ['MEGSZAKÍTÁS', 'ÚJRA', 'KIHAGYÁS']}


class MessageBox:
    """Üzenetablakok létrehozára szolgáló alaposztály, amely alosztályainak példánya egy alkalmazásspecifikus
    üzenetablak, amit a show() metódussal lehet megjeleníteni hangjelzés kíséretében. Az ablak mindaddig látható
    marad míg egy nyomógomb lenyomásra nem kerül.
    Az üzenetablak három részből áll: a fő és kiegészítő üzenetek szövegét tartalmazó rész, az ettől balra
    megjelenő ikongrafika, és ezek alatt, vízszintesen húzódó sáv, amelyen egy vagy több nyomógomb helyezkedik el.
    A hangjelzést a _make_sound(), az ikongrafikát a _create_icon_graphics(), a nyomógombokat a _create_buttons()
    metódus állítja elő. Mindegyik igény szerint felülírható az alosztályokban amennyiben az alapértelmezett
    működésük az adott üzenetablak-fajtához nem megfelelő.
    A konstruktor paramétereinek jelentése a modul leírásában található.
    """

    def __init__(self, title: str = '', message: str = '', *, detail: str = '', default: str = '', type: str = '',
                 parent=None, command=None, button_captions: list | tuple = (),
                 message_font=('Times', 14, 'bold'), message_bg_color=None, message_fg_color=None,
                 detail_font=('Helvetica', 11), detail_bg_color=None, detail_fg_color=None):

        self.title, self.message_text, self.detail, self.default, self.type = title, message, detail, default, type
        self.parent, self.command, self._button_captions = parent, command, button_captions
        self.message_font, self.msg_bg_color, self.msg_fg_color = message_font, message_bg_color, message_fg_color
        self.detail_font, self.detail_bg_color, self.detail_fg_color = detail_font, detail_bg_color, detail_fg_color
        self.response = ''
        self._canvas_side = 50

        self._build_messagebox_window()

    @staticmethod
    def _make_sound():
        """Az üzenetablak megjelenésére figyelmeztető hangjelzést ad."""
        winsound.MessageBeep()

    def _build_messagebox_window(self):
        """Létrehozza az üzenetablakot és benne, külön keretekben, az üzenetszövegeket megjelenítő címke elemeket,
        az ikon grafikát, valamint a nyomógombokat.
        """
        common_bgcolor = 'gray97'
        self._toplevel = tk.Toplevel(bg=common_bgcolor)
        self._toplevel.title(self.title)
        # Mivel a TopLevel ablak - ellentétben a grafikus elemekkel - már a létrehozásakor megjelenik, ezért azt
        # elrejtjük, és majd csak a show() metódus hívásakor jelenítjük meg.
        self._toplevel.withdraw()
        # Beállítjuk, hogy a TopLevel ablak mindig a szülőablaka fölött jelenjen meg. Ezzel egyúttal az is elérjük, hogy
        # csak a bezárás (X) icon jelenik meg az ablak bal felső sarkában.
        self._toplevel.transient(self._toplevel.master if not self.parent else self.parent)
        self._toplevel.focus_force()
        # Mivel modális ablakot akarunk létrehozni minden eseményt csak a TopLevel fogadhat.
        self._toplevel.grab_set()

        # A TopLevel ablakot három zónára osztjuk egy-egy kerettel.
        # A három keretet egy alapkeret tartalmazza, amivel meghatározhatók az ablak széleitől vett térközök.
        self._base_frame = tk.Frame(self._toplevel, bg=common_bgcolor)
        self._msgtype_icon_frame = tk.Frame(self._base_frame, bg=common_bgcolor)
        self._msg_text_frame = tk.Frame(self._base_frame, bg=common_bgcolor)
        self._button_frame = tk.Frame(self._toplevel, bd=1, relief=tk.GROOVE)

        # A keretek lehelyezése.
        self._base_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10, 0))
        self._button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 0))
        self._msgtype_icon_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, anchor='n')
        self._msg_text_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 0))

        self._msg_icon_canvas = tk.Canvas(self._msgtype_icon_frame, width=self._canvas_side, height=self._canvas_side,
                                          highlightthickness=0, bg=common_bgcolor)

        msg_label = tk.Label(self._msg_text_frame, text=self.message_text, justify=tk.LEFT, anchor='w',
                             font=self.message_font,
                             bg=self.msg_bg_color if self.msg_bg_color else common_bgcolor,
                             fg=self.msg_fg_color)

        detail_label = tk.Label(self._msg_text_frame, text=self.detail, justify=tk.LEFT, anchor='w',
                                font=self.detail_font, fg=self.detail_fg_color,
                                bg=self.detail_bg_color if self.detail_bg_color else common_bgcolor)

        # A grafikus elemek lehelyezése a keretekben.
        self._msg_icon_canvas.pack()
        msg_label.pack(fill=tk.BOTH, expand=True, anchor=tk.W)
        detail_label.pack(fill=tk.BOTH, expand=True, anchor=tk.W, pady=(15, 0))

        self._create_icon_graphics()
        self._create_buttons()

    def _on_buttonpress(self, event: tk.Event = None):
        """A gombok megnyomásának eseménykezelője."""
        self.response = event.widget.winfo_name()
        if self.command:
            self.command(self.response)
        self._toplevel.destroy()

    def _create_icon_graphics(self):
        """Alapértelmezett ikongrafikát hoz létre. Alosztályban, a speciális üzenetablakhoz illeszkedően igény
        szerint felülírható.
        """
        center_x, center_y = self._canvas_side / 2, self._canvas_side / 2
        r1 = min(center_x, center_y) * 0.7
        r2 = r1 * 0.85
        self._msg_icon_canvas.create_oval(center_x - r1, center_y - r1, center_x + r1, center_y + r1, fill='white', width=0)
        self._msg_icon_canvas.create_oval(center_x - r2, center_y - r2, center_x + r2, center_y + r2, fill='blue', width=0)

        line1_endpoints = center_x, center_y - r2 * 0.6, center_x, center_y - r2 * 0.6 + 5
        self._msg_icon_canvas.create_line(line1_endpoints, fill='white', width=5)
        line2_endpoints = center_x, center_y - r2 * 0.1, center_x, center_y + r2 * 0.7
        self._msg_icon_canvas.create_line(line2_endpoints, fill='white', width=5)

    def _create_buttons(self):
        """Egy OK nyomógombot hoz létre, ami a tájékoztató, figyelmeztető és hibajelző üzenetablakoknál megfelelő.
        Azonban kérdésfeltevő üzenetablak esetén ez nem elegendő, ezért az azt megvalósító alosztályban ezt a
        metódust felül kell írni.
        """
        btn_width = 10  # A nyomógomb szélessége karakterben.
        button = tk.Button(self._button_frame, name='ok', text='OK' if not (caption := self._button_captions) else caption[0],
                           width=btn_width, bg='gray90', takefocus=True)
        button.pack(side=tk.RIGHT, padx=10, pady=8)
        button.event_add('<<CloseMessageBox>>', '<ButtonPress 1>', '<Return>')
        button.bind('<<CloseMessageBox>>', self._on_buttonpress)
        self._toplevel.after(100, button.focus_set)

    def show(self):
        """Megjeleníti az üzenetablakot egy jelzőhang kíséretében, és várja, hogy a felhasználó megnyomjon egy gombot.
        Amennyiben a konstruktorban a 'command' paraméternek megadtunk egy függvényt, akkor az a gomb megnyomása után
        meg lesz hívva a nyomógomb szimbolikus nevével mint argumentummal, majd a metódus ezzel az értékkel tér vissza.
        """
        self._make_sound()
        # Legyen a TopLevel ablak szélessége fixen 12cm. Meghatározzuk a pixelben mért szélességet.
        top_width = self._toplevel.winfo_pixels('1c') * 12
        # A TopLevel ablakszélességének, a Canvas oldalméretének és az szövegkeret térközének (padx) ismeretében
        # meghatározzuk és beállítjuk az üzenetsorokat tartalmazó címkék sortöréshossz (wraplength) értékét.
        # A számolt elvi érték helyett a renderelési pontatlanságok miatt egy kicsivel kisebb értéket alkalmazunk.
        frm_padx = frm_padx[0] if isinstance(frm_padx := self._msg_text_frame.pack_info().get('padx'), tuple) else frm_padx
        for label in self._msg_text_frame.winfo_children():
            label.configure(wraplength=(top_width - self._canvas_side - frm_padx) * 0.95)

        # Lekérjük a TopLevel ablak aktuálisan igényelt magasságát.
        self._toplevel.update_idletasks()
        top_height = self._toplevel.winfo_reqheight()
        # A képernyő közepének koordinátái, ahová az ablakot helyezni fogjuk.
        top_x, top_y = (self._toplevel.winfo_screenwidth() // 2 - top_width // 2,
                        self._toplevel.winfo_screenheight() // 2 - top_height // 2)
        # Beállítjuk, hogy a TopLevel ablak a képernyő közepén a meghatározott méretekkel jelenjen majd meg.
        self._toplevel.geometry(f'{top_width}x{top_height}+{top_x}+{top_y}')
        # Rögzítjuk az ablak méreteit, amit utána nem lehet változtatni.
        self._toplevel.resizable(False, False)
        # Megjelenítjük az ablakot.
        self._toplevel.deiconify()
        # Megállítjuk a kód további futását, amíg az ablak be nem záródik vagy a bal felső X ikonra kattintással, vagy
        # valamelyik nyomógomb hatására.
        self._toplevel.wait_window()
        # A lenyomott gomb feliratának kisbetűs formájával térünk vissza.
        return self.response


class InfoMessageBox(MessageBox):
    """Az osztály példánya egy tájékoztató üzenetablakot valósít meg."""
    pass


class WarningMessageBox(MessageBox):
    """Az osztály példánya egy figyelmeztető üzenetablakot valósít meg."""
    def _create_icon_graphics(self):
        center_x, center_y = self._canvas_side / 2, self._canvas_side / 2
        # Háromszög.
        dy = self._canvas_side * (1 - 3 ** 0.5 / 2) / 2
        triangle_vertices = (self._canvas_side / 2, self._canvas_side * (1 - 3 ** 0.5 / 2) - dy,
                             0, self._canvas_side - dy, self._canvas_side, self._canvas_side - dy)
        self._msg_icon_canvas.create_polygon(triangle_vertices, fill='yellow', outline='black')
        line1_endpoints = center_x, center_y * 0.65, center_x, center_y * 1.4
        # Felkiáltójel.
        self._msg_icon_canvas.create_line(line1_endpoints, fill='black', width=5)
        line2_endpoints = center_x, center_y * 1.5, center_x, center_y * 1.5 + 5
        self._msg_icon_canvas.create_line(line2_endpoints, fill='black', width=5)


class ErrorMessageBox(MessageBox):
    """Az osztály példánya egy hibaüzenetet közlő ablakot valósít meg."""
    def _create_icon_graphics(self):
        center_x, center_y = self._canvas_side / 2, self._canvas_side / 2
        r1 = min(center_x, center_y) * 0.7
        r2 = r1 * 0.85
        self._msg_icon_canvas.create_oval(center_x - r1, center_y - r1, center_x + r1, center_y + r1, fill='white', width=0)
        self._msg_icon_canvas.create_oval(center_x - r2, center_y - r2, center_x + r2, center_y + r2, fill='red', width=0)
        # Az X létrehozása.
        line1_endpoints = center_x - r2 * 0.5, center_y - r2 * 0.5, center_x + r2 * 0.5, center_y + r2 * 0.5
        self._msg_icon_canvas.create_line(line1_endpoints, fill='white', width=6)
        line2_endpoints = center_x + r2 * 0.5, center_y - r2 * 0.5, center_x - r2 * 0.5, center_y + r2 * 0.5
        self._msg_icon_canvas.create_line(line2_endpoints, fill='white', width=6)


class QuestionMessageBox(MessageBox):
    """Az osztály példánya egy kérdésfeltevő üzenetablakot valósít meg.
    A konstruktor 'type' argumentumával lehet beállítani az ablak típusát, ami meghatározza a megjelenő nyomógombok
    számát és feliratát. A megadható értékeket a modul leírása tartalmazza.
    Egy nyomógomb megnyomása után az ablak bezárul és az ablakpéldány 'response' attribútumának értéke
    az adott gomb szimbólikus értéke lesz. Ezeket a modul leírása ismerteti.
    A show() metódus is ezzel az értékkel tér vissza.
    """

    def __init__(self, title: str = '', message: str = '', **options):
        # Az egyes kérdéstípusok és az azokhoz megjelenített nyomógombok alapértelmezett feliratainak összerendelése.
        self._types_to_default_buttoncaptions = QUESTION_TYPES_TO_DEFAULT_BUTTONCAPTIONS
        super().__init__(title, message, **options)

    def _create_icon_graphics(self):
        """Kérdőjelet ábrázoló grafika létrehozása."""
        center_x, center_y = self._canvas_side / 2, self._canvas_side / 2
        r_circle = self._canvas_side / 2 * 0.95
        self._msg_icon_canvas.create_oval(center_x - r_circle, center_y - r_circle, center_x + r_circle, center_y + r_circle,
                                          fill='blue', width=2, outline='white')
        thickness = 4  # A kérdőjel vastagsága.
        arc_center_x, arc_center_y = self._canvas_side / 2, self._canvas_side / 2 * 2 / 3
        r_arc = r_circle * 0.30
        self._msg_icon_canvas.create_arc(arc_center_x - r_arc, arc_center_y - r_arc,
                                         arc_center_x + r_arc, arc_center_y + r_arc,
                                         start=-90, extent=270, fill='white', outline='white', style=tk.ARC, width=4)
        line1_endpoints = arc_center_x, arc_center_y + r_arc, arc_center_x, arc_center_y + r_arc * 2.5
        self._msg_icon_canvas.create_line(line1_endpoints, fill='white', width=thickness)
        line2_endpoints = center_x, self._canvas_side * 0.75, center_x, self._canvas_side * 0.75 + thickness
        self._msg_icon_canvas.create_line(line2_endpoints, fill='white', width=thickness)

    def _create_buttons(self):
        """A megadott kérdéstípushoz a nyomógombok létrehozása."""
        if not self.type:
            self.type = 'yesno'  # Az alapértelmezett kérdésfeltevő ablaktípus beállítása.

        # A különböző kérdésfeltevő üzenetablaktípusokhoz meghatározunk szimbólikus neveket, amelyek
        # egyrészt az adott típushoz megjelenő nyomógombok nevei lesznek, másrészt egy nyomógomb lenyomása után
        # az annak megfelelő szimbolikus név lesz az ablakpéldány 'response' attribútumának értéke, valamint a show()
        # metódus is ezzel tér vissza.
        types_to_buttonnames = {'okcancel': ['ok', 'cancel'], 'yesno': ['yes', 'no'],
                                'yesnocancel': ['yes', 'no', 'cancel'], 'retrycancel': ['retry', 'cancel'],
                                'abortretryignore': ['abort', 'retry', 'ignore']}

        # A gombokat tartalmazó belső segédkeret ahhoz, hogy az üzenetablak jobb széléhez tudjuk igazítani a nyomógombokat.
        btn_inner_frame = tk.Frame(self._button_frame)
        btn_inner_frame.pack(side=tk.RIGHT, anchor='e', padx=10, pady=8)
        # A megadott kérdésfeltevő üzenetablaktípusokhoz tartozó nyomógombok létrehozása, lehelyezése és a
        # gomblenyomáskor meghívandó eseménykezeló hozzárendelése.
        btn_width = 12  # A nyomógombok szélessége karakterben.
        for button_name in types_to_buttonnames[self.type]:
            button = tk.Button(btn_inner_frame, name=button_name, width=btn_width, bg='gray90', takefocus=True)
            button.pack(side=tk.LEFT, padx=(10, 0))
            button.event_add('<<CloseMessageBox>>', '<ButtonPress 1>', '<Return>')
            button.bind('<<CloseMessageBox>>', self._on_buttonpress)
            if button_name == (self.default if self.default else types_to_buttonnames[self.type][0]):
                self._toplevel.after(100, button.focus_set)

        captions = self._button_captions if self._button_captions else self._types_to_default_buttoncaptions[self.type]
        for button, caption in zip(btn_inner_frame.winfo_children(), captions):
            button.config(text=caption)


# A különböző fajtájú üzenetablakokat létrehozó függvények.

def showinfo(title: str = '', message: str = '', **options) -> str:
    """Tájékoztató üzenetablakot jelenít meg a megadott címmel és üzenettel."""
    msg_box = InfoMessageBox(title, message, **options)
    return msg_box.show()


def showwarning(title: str = '', message: str = '', **options) -> str:
    """Figyelmeztető üzenetablakot jelenít meg a megadott címmel és üzenettel."""
    msg_box = WarningMessageBox(title, message, **options)
    return msg_box.show()


def showerror(title: str = '', message: str = '', **options) -> str:
    """Hibára figyelmeztető üzenetablakot jelenít meg a megadott címmel és üzenettel."""
    msg_box = ErrorMessageBox(title, message, **options)
    return msg_box.show()


def askquestion(title: str = '', message: str = '', *, type: str = 'yesno', **options) -> str:
    """A megadott címmel és üzenetszöveggel olyan üzenetablakot jelenít meg, amely a 'type' argumentum
    által meghatározott nyomógombokat tartalmazza mint választási lehetőségeket.
    A lenyomott gombot azonosító karakterláncot (szimbólikus nevet) adja vissza.
    """
    msg_box = QuestionMessageBox(title, message, type=type, **options)
    return msg_box.show()


def askokcancel(title: str = '', message: str = '', **options) -> bool:
    """A megadott címmel és üzenetszöveggel olyan üzenetablakot jelenít meg, amely az OK és a MÉGSE
    (vagy a 'button_captions' argumentummal meghatározott) feliratú gombokat tartalmazza mint választási lehetőséget.
    Az OK lenyomása után True értéket, egyébként False értéket ad vissza.
    """
    msg_box = QuestionMessageBox(title, message, type='okcancel', **options)
    return True if msg_box.show() == 'ok' else False


def askretrycancel(title: str = '', message: str = '', **options) -> bool:
    """A megadott címmel és üzenetszöveggel olyan üzenetablakot jelenít meg, amely az ÚJRA és a MÉGSE
    (vagy a 'button_captions' argumentummal meghatározott) feliratú gombokat tartalmazza mint választási lehetőséget.
    Az ÚJRA lenyomása után True értéket, egyébként False értéket ad vissza.
    """
    msg_box = QuestionMessageBox(title, message, type='retrycancel', **options)
    return True if msg_box.show() == 'retry' else False


def askyesno(title: str = '', message: str = '', **options) -> bool:
    """A megadott címmel és üzenetszöveggel olyan üzenetablakot jelenít meg, amely az IGEN és a NEM
    (vagy a 'button_captions' argumentummal meghatározott) feliratú gombokat tartalmazza mint választási lehetőséget.
    Az IGEN lenyomása után True értéket, egyébként False értéket ad vissza.
    """
    msg_box = QuestionMessageBox(title, message, type='yesno', **options)
    return True if msg_box.show() == 'yes' else False


def askyesnocancel(title: str = '', message: str = '', **options) -> bool | None:
    """A megadott címmel és üzenetszöveggel olyan üzenetablakot jelenít meg, amely a IGEN, NEM és MÉGSE
    (vagy a 'button_captions' argumentummal meghatározott) feliratú gombokat tartalmazza mint választási lehetőséget.
    Az IGEN lenyomása után True, a NEM esetén False, egyébként NONE értéket ad vissza.
    """
    msg_box = QuestionMessageBox(title, message, type='yesnocancel', **options)
    res = msg_box.show()
    return True if res == 'yes' else (False if res == 'no' else None)
