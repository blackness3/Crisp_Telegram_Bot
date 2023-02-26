import os
import pkgutil

pkgpath = os.path.dirname(__file__)
pkgname = os.path.basename(pkgpath)
content = []

for _,file,_ in pkgutil.iter_modules([pkgpath]):
    abfile = os.path.join(pkgpath,file)
    __import__(pkgname+'.'+file)
    content.append(file)