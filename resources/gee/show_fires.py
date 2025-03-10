from tifffile import imread
import os
import ee

from resources.gee.config import EE_CREDENTIALS
from resources.gee.methods import get_ee_product
from resources.gee.vis_handler import vs_fire, vs_firethresh, vs_nbr, vis_default
import matplotlib.pyplot as plt

data_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "data_dir")

ee.Initialize(EE_CREDENTIALS)

ee_product = get_ee_product(
    platform="sentinel",
    sensor="2",
    product="l1c"
)


for root, dirs, files in os.walk(
        os.path.join(data_dir, "sentinel-2_l1c_fpa_fod_2015-08-01_2015-12-31_13_256x256_w_fire"), topdown=False
):

    for name in files:
        fig, axs = plt.subplots(1, 3)

        image = imread(os.path.join(root, name))
        out = vs_fire(ee_product, image, {})
        axs[0].imshow(out)

        out = vis_default(ee_product, image, ee_product['vis_params'])
        axs[1].imshow(out)

        out = vs_firethresh(ee_product, image, {})
        axs[2].imshow(out)

        plt.show()
