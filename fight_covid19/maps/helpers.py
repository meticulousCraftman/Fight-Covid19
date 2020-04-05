import requests
from django.conf import settings
from django.db.models import Q

from fight_covid19.maps.models import HealthEntry
from fight_covid19.maps.utils import GeoLocation


def get_stats():
    data = dict()
    statewise = dict()  # To store total stats of the state
    last_updated = dict()
    total_people = HealthEntry.objects.all().order_by("user").distinct("user_id")
    data["sickPeople"] = sick_people = total_people.filter(
        Q(fever=True) | Q(cough=True) | Q(difficult_breathing=True)
    ).count()
    data["totalPeople"] = total_people.count()
    data["shortnessOfBreath"] = total_people.filter(Q(difficult_breathing=True)).count()
    data["fever"] = total_people.filter(Q(fever=True)).count()

    r = requests.get(settings.COVID19_STATS_API)
    if r.status_code == 200:
        r_data = r.json()
        india_stats = r_data
        total_stats = dict()  # To store total stats of the country
        total_stats.update(india_stats["statewise"][0])
        data.update(total_stats)
        last_updated = india_stats["tested"][-1]
        try:
            total_stats["deltaactive"] = india_stats["statewise"][0]["delta"]["active"]
            for i in india_stats["statewise"][1:]:
                statewise[i["state"]] = i
                statewise[i["state"]]["deltaactive"] = i["delta"]["active"]

        except Exception:
            pass
    return data, statewise, last_updated


def get_map_markers():
    points = (
        HealthEntry.objects.all()
        .order_by("user", "-creation_timestamp")
        .distinct("user")
        .values("user_id", "latitude", "longitude")
    )
    return list(points)


def get_range_coords(deg_lat, deg_long, radius=5):
    """
    Takes coordinates in degrees with optional radius value (default=5)
    Returns a list of min & max longitudes and latitudes
    """
    location = GeoLocation.from_degrees(deg_lat, deg_long)
    sw_pos, ne_pos = location.distance(radius)
    # X => long
    # Y => lat
    return {
        "min_lon": sw_pos.deg_lon,
        "min_lat": sw_pos.deg_lat,
        "max_lon": ne_pos.deg_lon,
        "max_lat": ne_pos.deg_lat,
    }
