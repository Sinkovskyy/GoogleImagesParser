from googleImagesParser import GoogleImagesParser


gip = GoogleImagesParser(headless = False,timeLimit=1.5)
gip.download_images("son wallpaper",50,{3840,2160},ignore_bad_quality_img=True)


