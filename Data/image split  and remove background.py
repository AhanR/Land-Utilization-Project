from rembg import remove
from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
from patchify import patchify
import tifffile as tiff
input_path='E:\Project AHAN\Vandalur_Satellite image.png'
oututpath='filename.png'
input=Image.open('/Vandalur_Satellite image.png',"rb")
output=remove(input)
output.save(oututpath)
