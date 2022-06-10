# Used_Car_Analysis
 Personal Project for analyzing used car market in California.
1. Download csv dataset that containg used car listing

Dataset DataFrame:  
 Column:  
'id', 'url', 'region', 'region_url', 'price', 'year', 'manufacturer',
       'model', 'condition', 'cylinders', 'fuel', 'odometer', 'title_status',
       'transmission', 'VIN', 'drive', 'size', 'type', 'paint_color',
       'image_url', 'description', 'county', 'state', 'lat', 'long',
       'posting_date'

2. Filter data classify by county and calculate average used car price in each county  
3. Get county by longtitude and latitude data with reverse geoencoding API.

Geoencoding API return example:  
[
  {
    "address_components": [
      {
        "long_name": "Santa Barbara",
        "short_name": "Santa Barbara",
        "types": [
          "locality",
          "political"
        ]
      },
      {
        "long_name": "Santa Barbara County",
        "short_name": "Santa Barbara County",
        "types": [
          "administrative_area_level_2",
          "political"
        ]
      },
      {
        "long_name": "California",
        "short_name": "CA",
        "types": [
          "administrative_area_level_1",
          "political"
        ]
      },
      {
        "long_name": "United States",
        "short_name": "US",
        "types": [
          "country",
          "political"
        ]
      }
    ],
    "formatted_address": "Santa Barbara, CA, USA",
    "geometry": {
      "bounds": {
        "northeast": {
          "lat": 34.4611451,
          "lng": -119.6399201
        },
        "southwest": {
          "lat": 34.336029,
          "lng": -119.859791
        }
      },
      "location": {
        "lat": 34.4208305,
        "lng": -119.6981901
      },
      "location_type": "APPROXIMATE",
      "viewport": {
        "northeast": {
          "lat": 34.4611451,
          "lng": -119.6399201
        },
        "southwest": {
          "lat": 34.336029,
          "lng": -119.859791
        }
      }
    },
    "place_id": "ChIJ1YMtb8cU6YARSHa612Q60cg",
    "types": [
      "locality",
      "political"
    ]
  }
]

4. Data visualization on map with pydeck