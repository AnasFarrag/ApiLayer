from PIL import Image, ImageFont, ImageDraw 


text = 'tssssssssssssssssssssext'
my_image = Image.open("image.jpg")



title_font = ImageFont.truetype('07558_CenturyGothic.ttf' , 200)

image_editable = ImageDraw.Draw(my_image)

image = image_editable.text((15,15), text, (237, 230, 211), font=title_font)
my_image.save("result.jpg")


