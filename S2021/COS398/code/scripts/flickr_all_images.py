import json 
import flickrapi
import math
import geopandas
from shapely.geometry import Point

api_key = u'e2687aab57bab0c1a5f39a811e15b36c'
api_secret = u'1bee25dbc5f73387'

flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')

states = geopandas.read_file('../us-states-data/usa-states-census-2014.shp')
states = states.drop(columns = ["STATENS", "AFFGEOID", "GEOID", "AWATER", "region", "STUSPS", "STATEFP", "ALAND", "LSAD"])
states = states.iloc[:-9]
states = states.drop(1)
states = states.reset_index(drop = True)

for mo in range(1, 13):
    observations_by_state = {}
    for i in range(states.shape[0]):
        observations_by_state[states.iloc[i, 0]] = 0
    for year in range(2010, 2015):
        for pageNum in range(40):
            if pageNum % 1 == 0:
                print("Currently on month {}, year {}, page {}".format(mo, year, pageNum))
            try:
                photos = flickr.photos.search(
                    has_geo = True,
                    bbox = "-125, 22, -57, 52",
                    min_taken_date="{}-{}-01 00:00:00".format(year, mo),
                    max_taken_date="{}-{}-28 00:00:00".format(year, mo),
                    page = pageNum,
                    per_page = 100)
            except:
                print("Error searching photos")
                continue
            for pic in photos["photos"]["photo"]:
                try:
                    photo_info = flickr.photos.getInfo(photo_id = pic["id"])
                except:
                    print("Error getting geo tag information")
                    continue
                lat = float(photo_info["photo"]["location"]["latitude"])
                lon = float(photo_info["photo"]["location"]["longitude"])
                p1 = Point(lon, lat)
                #Convert from lat, lon to state
                for index, row in states.iterrows():
                    stateGeo = row["geometry"]
                    stateName = row["NAME"]
                    if stateGeo.contains(p1):
                        observations_by_state[stateName] += 1
                        break

    
    j = json.dumps(observations_by_state)
    f = open("../flickr_all_images_by_state_mo{}.json".format(mo),"w")
    f.write(j)
    f.close()