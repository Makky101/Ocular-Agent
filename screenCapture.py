import mss
import numpy as np
from PIL import Image
from io import BytesIO

class screenTake:
    """Screen capture utility.
    Captures the primary monitor and returns PNG bytes that can be attached to
    LLM multimodal requests.
    """

    @staticmethod
    def screenCapture():
        """Capture monitor 1 and return image bytes in PNG format.

        Returns:
            bytes | None: PNG-encoded screenshot bytes, or None on failure.
        """
        try:
            with mss.mss() as sct:
                # mss index 1 is typically the primary display.
                monitor = sct.monitors[1]         
                screenshot = sct.grab(monitor) 
                # Drop alpha channel because RGB is enough for model input.
                arr = np.array(screenshot)[:,:,:3]  
                img = Image.fromarray(arr)
                
            buffer = BytesIO()
            img.save(buffer, format="PNG")

            # Raw PNG bytes are returned and later embedded in data URL payload.
            image_bytes = buffer.getvalue()

            return image_bytes
        except Exception as e:
            raise RuntimeError(f"error at screenCapture: {e}")
