from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from django.http import JsonResponse
import time
import os
import base64
import threading
from PIL import Image

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
        img_type = request.session.get('slider')
        B_img_src = request.POST.getlist('B_img_src[]')
        imgs = [img.split('/')[-1] for img in B_img_src if 'image_' in img]
        final = img_post_process(imgs,img_type)
        print_photo(final)
    return HttpResponse("success")

def print_pic(request): 
    folder = os.listdir('./static/')
    rm_pic =[pic for pic in folder if 'image_' in pic]
    for filename in rm_pic:
        file_path = os.path.join('./static/', filename)
        os.remove(file_path)
    return render(request, 'print_pic.html')

def img_post_process(imgs,img_type):
    img_postion_info = get_imgs_postion_info(img_type)
    for img in imgs:
        bmp = Image.open (os.path.join('./static/images', img))



def print_photo(imgs):
    pass 

def get_imgs_postion_info(img_type):
    f = open(os.path.join('./static/position', img_type+'.txt'))
    for line in f.readlines():
        print(line)
    f.close