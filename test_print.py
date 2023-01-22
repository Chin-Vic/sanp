

import win32print
import win32ui
from PIL import Image, ImageWin

HORZRES = 8
VERTRES = 10
PHYSICALWIDTH = 110
PHYSICALHEIGHT = 111
PHYSICALOFFSETX = 112
PHYSICALOFFSETY = 113


printer_name = win32print.GetDefaultPrinterW() # 獲得預設印表機
hDC = win32ui.CreateDC ()
hDC.CreatePrinterDC (printer_name)
printable_area = hDC.GetDeviceCaps (HORZRES), hDC.GetDeviceCaps (VERTRES)
printer_size = hDC.GetDeviceCaps (PHYSICALWIDTH), hDC.GetDeviceCaps (PHYSICALHEIGHT)
printer_margins = hDC.GetDeviceCaps (PHYSICALOFFSETX), hDC.GetDeviceCaps (PHYSICALOFFSETY)
bmp = Image.open ('static/assets/images/BB.png')
if bmp.size[0] > bmp.size[1]:
  bmp = bmp.rotate (90)
ratios = [1.0 * printable_area[0] / bmp.size[0], 1.0 * printable_area[1] / bmp.size[1]]
scale = min (ratios)
hDC.StartDoc ('test')
hDC.StartPage ()
dib = ImageWin.Dib (bmp)
scaled_width, scaled_height = [int (scale * i) for i in bmp.size]
x1 = int ((printer_size[0] - scaled_width) / 2)
y1 = int ((printer_size[1] - scaled_height) / 2)
x2 = x1 + scaled_width
y2 = y1 + scaled_height
dib.draw (hDC.GetHandleOutput (), (x1, y1, x2, y2))
hDC.EndPage ()
hDC.EndDoc ()
hDC.DeleteDC ()
