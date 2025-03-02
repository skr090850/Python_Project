import pyqrcode
import png
from PIL import Image
url = input("Enter any url = ")
QrCode = pyqrcode.create(url)
QrCode.png("QrCode.png",scale=8)
img=Image.open(r"QrCode.png")
img.show()
