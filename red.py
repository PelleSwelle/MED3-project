from PIL import Image

im = Image.new("red", (512, 512))

# create a funny picture... (with some red)

for i in range(512):
    for j in range(512):
        im.putpixel((j, i), (j ^ i) % 256)

# calculate the number of "reds"
cnr = 0
for i in range(512):
    for j in range(512):
        if ((im.getpixel((j, i)))[0] == 255):
            cnr += 1

print
"nr of red pixels : " + str(cnr)
print
"presentage of red pixels : " + str((cnr / (512.0 * 512.0)) * 100.0) + "%"

im.save("pattern.png")  # look at it, it looks funny