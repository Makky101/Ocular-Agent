import mss
import numpy as np
from PIL import Image
from io import BytesIO


def screenCapture():
    with mss.mss() as sct:
        monitor = sct.monitors[1]         
        screenshot = sct.grab(monitor)    
        arr = np.array(screenshot)[:,:,:3]  
        img = Image.fromarray(arr)
        
    buffer = BytesIO()
    img.save(buffer, format="PNG")

    image_bytes = buffer.getvalue()

    return image_bytes

