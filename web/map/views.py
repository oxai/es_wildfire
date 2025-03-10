from django.shortcuts import render, HttpResponse
from django.http import JsonResponse

from resources.fpa_fod.data_loader import FpaFodDataLoader
from resources.gee.methods import get_ee_product
from resources.gee.tile_loader import GeeProductTileLoader, TileDateRangeQuery
from resources.gee.vis_handler import get_vis_handler
from resources.gee.vis_handler_utils import get_empty_image
from resources.modis_fire.data_loader import ModisFireDataLoader


gee_loader = GeeProductTileLoader()
fpa_fod_loader = FpaFodDataLoader()
modis_fire_loader = ModisFireDataLoader()


def home(request):
    # return render(request, 'home.html')
    return HttpResponse("API Endpoint")


# Create your views here.
def gee_mapserver(request, platform, sensor, product, method, z, x, y, from_date, until_date):
    print(f"Received map tile request: {platform} {sensor} {product}, x: {x}, y: {y}, zoom: {z}", {from_date} - {until_date})

    ee_product = get_ee_product(
        platform=platform,
        sensor=sensor,
        product=product
    )

    query = TileDateRangeQuery(x=x, y=y, z=z, date_from=from_date, date_to=until_date, reducer="median")

    out = gee_loader.load(ee_product, query, subdir="map")
    if out is None:
        image = get_empty_image()
    else:
        handler = get_vis_handler(ee_product, method)
        image = handler(out, ee_product)

    response = HttpResponse(content_type='image/png')
    image.save(response, "PNG")
    return response


def fpa_fod_fire_location(request, from_date, until_date, min_fire_size):
    df = fpa_fod_loader.get_records_in_range(from_date=from_date, until_date=until_date, min_fire_size=min_fire_size)
    loc = [{"lat": lat, "lng": lng} for lat, lng in zip(df["LATITUDE"], df["LONGITUDE"])]
    return JsonResponse(loc, safe=False)


def modis_fire_location(request, from_date, until_date, confidence):
    df = modis_fire_loader.get_records_in_range(from_date=from_date, until_date=until_date, confidence_thresh=confidence)
    loc = [{"lat": lat, "lng": lng} for lat, lng in zip(df["LATITUDE"], df["LONGITUDE"])]
    return JsonResponse(loc, safe=False)
