import base64

open_icon = open('icon.ico', "rb")
b64str = base64.b64encode(open_icon.read())
open_icon.close()
write_data = "img = %s" % b64str
f = open("com/sxl/txtdownloader/icon.py", "w+")
f.write(write_data)
f.close()
