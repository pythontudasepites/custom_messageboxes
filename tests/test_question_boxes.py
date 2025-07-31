import tkinter as tk
from custom_messagebox import askquestion, askokcancel, askyesno, askyesnocancel, askretrycancel

root = tk.Tk()

res_q = askquestion('KÉRDÉS', 'Valamiért megszakadt a számítási művelet.\nMit kívánsz tenni?',
                    detail='Ha a MEGSZAKÍTÁS lehetőséget választod, akkor a számolás nem folytatódik.\n'
                           'Ha az ÚJRA gombot nyomod meg, akkor egy másik adattal újra lesz elvégezve a számítás.\n'
                           'Ha a KIHAGYÁS opciót választod, akkor ez a műveletrész nem lesz végrehajtva, de a többi igen.',
                    type='abortretryignore',
                    message_fg_color='blue', message_bg_color='orange', message_font=('Cambria', 14, 'bold'),
                    detail_fg_color='black', detail_bg_color='light yellow', detail_font=('Georgia', 12))

res_ync = askyesnocancel('Változások mentése'.upper(), message='A dokumentum módosult.\nA bezárás előtt '
                                                               'el szeretnéd menteni ezeket a változtatásokat?',
                         detail='Válaszlehetőségek:\n\n - Igen: A bezárás előtt a dokumentumban végzett változtatások '
                                'el lesznek mentve.\n\n - Nem: A változtatások el lesznek vetve, és a '
                                'dokumentum mentés nélkül be lesz zárva.\n\n - Mégse: A dokumentum nem lesz bezárva és '
                                'mentve, így folytathatod a szerkesztést vagy más műveletet hajthatsz végre.',
                         default='cancel',
                         message_font=('Segoe UI', 14, 'bold'), detail_font=('Times New Roman', 14))

res_rc = askretrycancel('Hálózati hiba'.upper(), message='Nem sikerült csatlakozni a szerverhez.\nÚjrapróbálod most?',
                        detail='Válaszlehetőségek:\n\nRETRY: Újra megpróbálod a kapcsolódást a szerverhez.\n\n'
                               'CANCEL: Megszakítod a kapcsolódási kísérletet, és visszatérsz az alkalmazás előző állapotába.',
                        button_captions=['RETRY', 'CANCEL'],
                        detail_bg_color='white')

res_oc = askokcancel('Művelet befejezve'.upper(), message='A fájl feltöltése sikeres volt. Most online is megtekintheti.\n'
                                                          'Meg szeretné nyitni?',
                     detail='A fájl megnyitásához nyomja meg az OK gombot. A MÉGSE gombbal visszatérhet az alkalmazásba.',
                     message_font=('DejaVu Serif', 16, 'bold'), message_fg_color='saddle brown', message_bg_color='beige')

res_yn = askyesno('Kilépés megerősítés'.upper(), message='Biztosan kilépsz az alkalmazásból?',
                  detail='Mielőtt kilépsz, ellenőrizd, hogy minden szükséges adatot elmentettél.',
                  message_font=('Courier', 20, 'bold'),
                  detail_fg_color='blue', detail_bg_color='gold', detail_font=('Arial black', 12))

root.destroy()
root.mainloop()
