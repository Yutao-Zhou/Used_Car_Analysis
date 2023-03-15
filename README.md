# Used Car Data Analysis and Visualization Web Application
Personal Project for analyzing used car market.

[![mbti](usedCar.gif)](https://youtu.be/hZshFOEoQIE)

- Build with streamlit, dealing large data set(365K data points) with Desk, Pandas, and NumPy for data filtering and cache
data.
- Visualize data with scatter plot on heat map (with more than 100 selectable base maps), pie chart, scatter plot with trend
line, with packages e.g. plotly, leafmap, pydeck.
- Added VIN lookup function with Get from NHTSA (National Highway Traffic Safety Administration)'s API.
- Designed AI key phrase extraction from listing description with spacy, and visualization with wordcloud with VIN query
results (VIN query, key phrase generation, and word cloud should take less than 5 seconds, usually 2 seconds).
- Implemented geocoding and filtering data with user input distance from user query location with geoencoder in GeoPy
(Entire query should take 3 seconds depends on setting usually less than 0.5 second).
- Added Login page with cookie. Hosting web application on a personal server with domain re-direction (2 month so far
without offline or interference).
- Tested google map API with REQUEST for geocoding but abandoned for cost ($5 per 1000 query).
- deployed website to google cloud platform with docker and yaml files but abandoned it for daily limit of outgoing internet traffic for app engine with free account.


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