import base64
import cv2
import numpy as np
import os
import threading
import time
import win32print
import win32ui
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.http import JsonResponse
from PIL import Image, ImageWin


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

class Buffer: 
    _instance = None 
    buffer = 0
    def __new__(cls, *args, **kwargs): 
        if cls._instance is None: 
            cls._instance = super().__new__(cls) 
        return cls._instance 
    def update(self):
        self.buffer+=1
    def get_buffer(self):
        return self.buffer

class PicCount: 
    _instance = None 
    count = 1
    def __new__(cls, *args, **kwargs): 
        if cls._instance is None: 
            cls._instance = super().__new__(cls) 
        return cls._instance 
    def update(self):
        self.count+=1
    def get_count(self):
        return str(self.count)



def update_buffer():
    buffer = Buffer()
    while True:
        buffer.update()
        time.sleep(1)

thread = threading.Thread(target=update_buffer)
thread.start()

def index(request):
    buffer = Buffer()
    m = buffer.get_buffer()
    if request.session.get('slider'):
        request.session.pop('slider')
    if is_ajax(request=request):
      return JsonResponse({'buffer_length': m})

    return render(request, 'index.html', {'buffer_length': m})

def pick_background(request):
    time.sleep(0.5)
    buffer = Buffer()
    buffer.buffer = 0
    if request.method == 'POST':
        selected = request.POST.get('slider')
        request.session['slider'] = selected
        time.sleep(0.5)
        return HttpResponseRedirect('/take_pic')
    return render(request, 'pick_background.html')


def take_pic(request):
    return render(request, 'take_pic.html')

def save_photo(request):
    if request.method == 'POST':
        pic = PicCount()
        img_data = request.POST['imgData']
        img_data = img_data.split(',')[1]
        # decode image data
        img_data = base64.b64decode(img_data)
        with open('./static/image_'+pic.get_count()+'.jpeg', 'wb') as f:
            print(pic.get_count())
            f.write(img_data)
        pic.update()
        return HttpResponse("success")

def pick_pic(request):
    print(122,request.session.get('slider'))
    type_img = request.session.get('slider')  
    pic = PicCount()
    pic.count=1
    return render(request, 'pick_pic.html', {'type': type_img})

def record_pic(request):
    if request.method == 'POST':
        B_img_src = request.POST.getlist('B_img_src[]')
        request.session['B_img_src'] = B_img_src
       
    return HttpResponse("success")

def print_pic(request): 
    img_type = request.session.get('slider')
    B_img_src = request.session.get('B_img_src')
    imgs = [img.split('/')[-1] for img in B_img_src if 'image_' in img]
    img_post_process(imgs,img_type)
    # print_photo()
    folder = os.listdir('./static/')
    rm_pic =[pic for pic in folder if 'image_' in pic]
    for filename in rm_pic:
        file_path = os.path.join('./static/', filename)
        os.remove(file_path)
    return render(request, 'print_pic.html')

def img_post_process(imgs,img_type):
    img_postion_info = get_imgs_postion_info(img_type)
    background = Image.open(os.path.join('./static/assets/images', img_type+'.png'))
    empty = Image.new('RGB', (background.size))
    for idx,img in enumerate(imgs):
        bmp = Image.open (os.path.join('./static/', img))
        w_ = int(img_postion_info[idx][0])
        h_ = int(img_postion_info[idx][1])
        cx = int(img_postion_info[idx][2])
        cy = int(img_postion_info[idx][3])
        bmp = bmp.resize((w_,h_))
        empty.paste(bmp,(int(cx-w_/2),int(cy-h_/2)))

    pic = cv2.cvtColor(np.asarray(empty), cv2.COLOR_RGB2BGR)
    pic = cv2.cvtColor(pic, cv2.COLOR_BGR2BGRA)
    background = cv2.cvtColor(np.asarray(background), cv2.COLOR_RGB2BGR)
    background = cv2.cvtColor(background, cv2.COLOR_BGR2BGRA) 
    h = pic.shape[0]           
    w = pic.shape[1]                  
    for x in range(w):
        for y in range(h):
            r = background[y, x, 2]
            g = background[y, x, 1]  
            b = background[y, x, 0] 
            if r==0 and g==0 and  b==0:
                background[y, x] = pic[y, x]
    # cv2.imwrite('./static/image_fin.png', background)


def print_photo():
    HORZRES = 8
    VERTRES = 10
    PHYSICALWIDTH = 110
    PHYSICALHEIGHT = 111
    printer_name = win32print.GetDefaultPrinterW() 
    hDC = win32ui.CreateDC ()
    hDC.CreatePrinterDC (printer_name)
    printable_area = hDC.GetDeviceCaps (HORZRES), hDC.GetDeviceCaps (VERTRES)
    printer_size = hDC.GetDeviceCaps (PHYSICALWIDTH), hDC.GetDeviceCaps (PHYSICALHEIGHT)
    bmp = Image.open ('./static/image_fin.png')
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
 

def get_imgs_postion_info(img_type):
    position = []
    f = open(os.path.join('./static/position', img_type+'.txt'))
    for line in f.readlines():
        position.append(line.split(','))
    f.close
    return position