from googleImagesParser import GoogleImagesParser
import requests
import io
gip = GoogleImagesParser()
# urls = gip.get_images_url("blue sky",20)

r = requests.get("https://pbs.twimg.com/profile_images/575359604592263168/ZXQ1nLVp_400x400.jpeg")
r = r.raw
file = io.StringIO(r)

gip.download_image(file,"test work")

