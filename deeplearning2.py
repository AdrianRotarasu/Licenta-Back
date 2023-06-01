import pytesseract as pt
from PIL import Image

# ...

def modify(path, filename):
    results = modelYolov8(path)
    cods = results[0].boxes.xyxy
    image = Image.open(path)

    for cord in cods:
        xmin, ymin, xmax, ymax = map(int, cord)
        
        crop = image.crop((xmin, ymin, xmax, ymax))
        cropped_image = crop.filter(ImageFilter.GaussianBlur(20))
        image.paste(cropped_image, (xmin, ymin))
  
        text = pt.image_to_string(cropped_image)
        print(text)
  
    image.save('./static/modified_uploads/{}'.format(filename))
    return text