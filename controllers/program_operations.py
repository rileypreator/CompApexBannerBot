from classes.BannerImage import BannerImage

def startup():
    # create a BannerImage object
    banner_image = BannerImage()

    # do any other startup tasks here

    print("Banner sizes:", banner_image.width, " x ", banner_image.height)
