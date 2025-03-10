import tifffile
import numpy as np
from .vis_handler import vis_fire, vis_veg, vis_dnbr
import matplotlib.pyplot as plt
import ee
import sys

sys.path.append('.')

from .config import EE_CREDENTIALS
from .methods import get_ee_product

sys.path.remove('.')

ee.Initialize(EE_CREDENTIALS)

ee_product = get_ee_product(platform="sentinel", sensor="2", product="l1c")
#ee_product = get_ee_product(platform="landsat", sensor="8", product="surface")
im = tifffile.imread('resources/gee/data_dir/examples/sentinel_test_img_fire.tif')
arr = np.array(im)
vis_veg_arr = vis_veg(ee_product, arr, vis_params=None)
plt.imshow(vis_veg_arr)
plt.show()
vis_fire_arr = vis_fire(ee_product, arr, vis_params=None)
plt.imshow(vis_fire_arr)
plt.show()
vis_dnbr_arr = vis_dnbr(ee_product, arr, vis_params=None,comp_image=None)
plt.imshow(vis_dnbr_arr)
plt.show()
