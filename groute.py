import requests
import datetime
import configparser

config = configparser.ConfigParser()
config.read('.env')
API_KEY = config['KEYS']['GOOGLE_ROUTES_API_KEY']
ORIGIN = "1 Washington Sq, San Jose, CA 95192"

MAX_MILES = 50


class grouteInputOrder:
  def __init__(self, order_id: int, address: str) -> None:
    self.address = address
    self.order_id = order_id


class grouteOutputOrder:
  def __init__(self, order_id: int, index: int, lat: int, lon: int, eta: int) -> None:
    self.order_id = order_id
    self.index = index
    self.lat = lat
    self.lon = lon
    self.eta = eta


class grouteResponse:
  def __init__(self, polyline: str, legs: list[grouteOutputOrder]) -> None:
    self.polyline = polyline
    self.legs = legs


def _get_time_str() -> str:
  utc_time = datetime.datetime.now(datetime.timezone.utc)

  # Offset the time by 10 minutes because groutes wants a future time
  offset_time = utc_time + datetime.timedelta(minutes=10)

  formatted_offset_time = offset_time.strftime("%Y-%m-%dT%H:%M:%SZ")

  return formatted_offset_time


def plan_path(orders: list[grouteInputOrder]) -> grouteResponse:
  headers = {
    'Content-Type': 'application/json',
    'X-Goog-Api-Key': API_KEY,
    'X-Goog-FieldMask': 'routes.legs.duration,routes.legs.endLocation,routes.polyline.encodedPolyline,routes.optimized_intermediate_waypoint_index',
  }
  json_data = {
      'origin': {'address': ORIGIN},
      'destination': {'address': ORIGIN},
      'intermediates': [{"address": w.address} for w in orders],
      'travelMode': 'DRIVE',
      'routingPreference': 'TRAFFIC_AWARE',
      'departureTime': _get_time_str(),
      'computeAlternativeRoutes': False,
      'optimizeWaypointOrder': True,
      'languageCode': 'en-US',
      'units': 'IMPERIAL',
  }

  # Durations are in seconds, the order of the legs is the same as the order returned in optimzedorder.
  resp = requests.post('https://routes.googleapis.com/directions/v2:computeRoutes', headers=headers, json=json_data)
  if resp.status_code != 200:
    raise Exception()

  resp_json = resp.json()

  print(resp_json)

  encoded_polyline = resp_json['routes'][0]['polyline']['encodedPolyline']
  waypoint_order = resp_json['routes'][0]['optimizedIntermediateWaypointIndex']

  output_orders = []
  eta_sum = 0
  for index, io in enumerate(resp_json['routes'][0]['legs'][:-1]):
    o_id = orders[waypoint_order[index]].order_id
    o_index = index
    o_lat = io["endLocation"]["latLng"]["latitude"]
    o_lon = io["endLocation"]["latLng"]["longitude"]
    eta_sum += int(io["duration"][:-1])
    output_orders.append(grouteOutputOrder(o_id, o_index, o_lat, o_lon, eta_sum))

  return grouteResponse(encoded_polyline, output_orders)


# input_orders = [
#   grouteInputOrder(0, "221 E San Fernando St, San Jose, CA 95112"),
#   grouteInputOrder(1, "5575 Nicasio Valley Rd, Nicasio, CA 94946"),
#   grouteInputOrder(2, "163 W Santa Clara St, San Jose, CA 95113"),
#   grouteInputOrder(3, "291 N 4th St, San Jose, CA 95112"),
# ]

# res = plan_path(input_orders)
# for l in res.legs:
#   print(l.order_id, l.index, l.eta, l.lat, l.lon)
# print(res.polyline)


def distance_check(destination_address: str) -> bool:
  url = f'https://maps.googleapis.com/maps/api/distancematrix/json?origins={ORIGIN}&destinations={destination_address}&key={API_KEY}'
  data = requests.get(url).json()
  print(data)
  try:
    meters = data['rows'][0]['elements'][0]['distance']['value']
  except KeyError: # There will be a KeyError if the address was not able to be parsed.
    return False
  
  miles = 0.000621371 * meters
  
  return miles <= MAX_MILES
