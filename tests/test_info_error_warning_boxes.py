import tkinter as tk
from custom_messagebox import showinfo, showwarning, showerror

root = tk.Tk()

showinfo('TÁJÉKOZTATÁS', 'A mai előadás elmarad.', detail='Ennek oka, hogy a színészek többsége beteg lett.')

showerror('HIBAÜZENET', 'Figyelem, hiba történt az adatbevitel során, ami a rendszer helytelen '
                        'működéséhez vezethet.',
          detail='A hiba oka az, hogy nem figyeltél eléggé.\nDe ne keseredj el, ez mással is '
                 'elő szokott fordulni.\nGondosan nézd át a bemenő adatokat és szűrd ki a nem megfelelőket.',
          message_font=('Georgia', 14, 'bold italic'), message_fg_color='maroon',
          detail_font=('Cambria', 12), button_captions=('ÉRTETTEM',))

showwarning('FIGYELMEZTETÉS', 'Mielőtt megnyitod a fájlt, győződj meg róla, hogy vírusmentes.',
            detail='Ha ismeretlen forrásból származik a fájl, fennáll a veszélye, hogy vírust tartalmaz, ami '
                   'megnyitás után kárt tehet a számítógépben vagy az alkalmazásokban.',
            message_bg_color='black', message_fg_color='yellow', message_font=('Noto', 16, 'bold'),
            detail_bg_color='silver', detail_fg_color='blue', detail_font=('Times New Roman', 14, 'bold italic'))

root.destroy()
root.mainloop()
