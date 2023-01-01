
import os
from PIL import Image
from flask import url_for, current_app

def add_profile_pic(pic_upload, username):

    filename = pic_upload.filename # pobranie nazwy podanej przez usera
    #my picutre . jpg
    ext_type =  filename.split('.')[-1]# pobranie extension type - jpg lub png
    #username.jpg
    #zmiana pliku mypicture.jpg na username.jpg
    storage_filename = str(username)+ '.'+ext_type # nazwa przechowywanego pliku na serwerze, nazwa od usera w stringu

    #miejsce do przechowywania
    filepath = os.path.join(current_app.root_path, 'static\profile_pics', storage_filename)
    #rootpath oznacza diesel_api

    #przechowywanie 1 wielkości
    output_size =(200,200)
    pic = Image.open(pic_upload)#otworzenie
    pic.thumbnail(output_size)#zmniejszenie
    pic.save(filepath)#zapisanie

    return storage_filename







