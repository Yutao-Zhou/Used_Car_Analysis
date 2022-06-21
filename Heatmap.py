import dask.dataframe as dd
import leafmap.foliumap as leafmap
import streamlit as st

def state2Coor(stateName):
    if (type(stateName) == list and len(stateName) > 1) or stateName == "All States":
        return 39.155726, -98.030561, 3.5
    else:
        path = "./statelatlong.csv"
        dask = dd.read_csv(path, dtype = {"State":str, "Name": str, "Latitude": float, "Longitude": float})
        df = dask.compute()
        if type(stateName) == list and len(stateName) == 1:
            stateName = stateName[0]
        stateDf = df.loc[df['Name'] == stateName]
        latitude = float(stateDf['Latitude'])
        Longitude = float(stateDf['Longitude'])
        return latitude, Longitude, 5

def heatmap(data, stateName):
    with st.spinner("Loading 2D Heatmap"):
        latitude, longitude, zoom = state2Coor(stateName)
        m = leafmap.Map(center = [latitude, longitude], zoom = zoom, tiles = "stamentoner")
        m.add_heatmap(
            data,
            latitude = "lat",
            longitude = "long",
            value = "price",
            name = "Listing cars heatmap",
            radius = 20,
        )
        basemap = st.selectbox("Choose a basemap", (["Default", "OpenStreetMap", "ROADMAP", "SATELLITE",\
        "TERRAIN", "HYBRID", "FWS NWI Wetlands", "FWS NWI Wetlands Raster", "NLCD 2019 CONUS Land Cover",\
        "NLCD 2016 CONUS Land Cover", "NLCD 2013 CONUS Land Cover", "NLCD 2011 CONUS Land Cover", \
        "NLCD 2008 CONUS Land Cover", "NLCD 2006 CONUS Land Cover", "NLCD 2004 CONUS Land Cover", \
        "NLCD 2001 CONUS Land Cover", "USGS NAIP Imagery", "USGS NAIP Imagery False Color", \
        "USGS NAIP Imagery NDVI", "USGS Hydrography", "USGS 3DEP Elevation", "ESA WorldCover 2020",\
        "ESA WorldCover 2020 S2 FCC", "ESA WorldCover 2020 S2 TCC", "BasemapAT.basemap", "BasemapAT.grau",\
        "BasemapAT.highdpi", "BasemapAT.orthofoto", "BasemapAT.overlay", "BasemapAT.surface", \
        "BasemapAT.terrain", "CartoDB.DarkMatter", "CartoDB.DarkMatterNoLabels", "CartoDB.DarkMatterOnlyLabels",\
        "CartoDB.Positron", "CartoDB.PositronNoLabels", "CartoDB.PositronOnlyLabels", "CartoDB.Voyager", \
        "CartoDB.VoyagerLabelsUnder", "CartoDB.VoyagerNoLabels", "CartoDB.VoyagerOnlyLabels", "CyclOSM", \
        "Esri.AntarcticBasemap", "Esri.ArcticOceanBase", "Esri.ArcticOceanReference", "Esri.DeLorme", \
        "Esri.NatGeoWorldMap", "Esri.OceanBasemap", "Esri.WorldGrayCanvas", "Esri.WorldImagery",\
        "Esri.WorldPhysical", "Esri.WorldShadedRelief", "Esri.WorldStreetMap", "Esri.WorldTerrain", \
        "Esri.WorldTopoMap", "FreeMapSK", "Gaode.Normal", "Gaode.Satellite", "GeoportailFrance.orthos", \
        "GeoportailFrance.parcels", "GeoportailFrance.plan", "HikeBike.HikeBike", "HikeBike.HillShading", \
        "JusticeMap.americanIndian", "JusticeMap.asian", "JusticeMap.black", "JusticeMap.hispanic", \
        "JusticeMap.income", "JusticeMap.multi", "JusticeMap.nonWhite", "JusticeMap.plurality", \
        "JusticeMap.white", "MtbMap", "NASAGIBS.BlueMarble", "NASAGIBS.BlueMarble3031", \
        "NASAGIBS.BlueMarble3413", "NASAGIBS.ModisAquaBands721CR", "NASAGIBS.ModisAquaTrueColorCR", \
        "NASAGIBS.ModisTerraAOD", "NASAGIBS.ModisTerraBands367CR", "NASAGIBS.ModisTerraBands721CR", \
        "NASAGIBS.ModisTerraChlorophyll", "NASAGIBS.ModisTerraLSTDay", "NASAGIBS.ModisTerraSnowCover", \
        "NASAGIBS.ModisTerraTrueColorCR", "NASAGIBS.ViirsEarthAtNight2012", "NASAGIBS.ViirsTrueColorCR", \
        "NLS", "OPNVKarte", "OneMapSG.Default", "OneMapSG.Grey", "OneMapSG.LandLot", "OneMapSG.Night", \
        "OneMapSG.Original", "OpenAIP", "OpenFireMap", "OpenRailwayMap", "OpenSeaMap", "OpenSnowMap.pistes",\
        "OpenStreetMap.BZH", "OpenStreetMap.BlackAndWhite", "OpenStreetMap.CH", "OpenStreetMap.DE",\
        "OpenStreetMap.France", "OpenStreetMap.HOT", "OpenStreetMap.Mapnik", "OpenTopoMap", "SafeCast", \
        "Stadia.AlidadeSmooth", "Stadia.AlidadeSmoothDark", "Stadia.OSMBright", "Stadia.Outdoors", \
        "Stamen.Terrain", "Stamen.TerrainBackground", "Stamen.TerrainLabels", "Stamen.Toner", \
        "Stamen.TonerBackground", "Stamen.TonerHybrid", "Stamen.TonerLabels", "Stamen.TonerLines", \
        "Stamen.TonerLite", "Stamen.TopOSMFeatures", "Stamen.TopOSMRelief", "Stamen.Watercolor", \
        "Strava.All", "Strava.Ride", "Strava.Run", "Strava.Water", "Strava.Winter", \
        "SwissFederalGeoportal.JourneyThroughTime", "SwissFederalGeoportal.NationalMapColor", \
        "SwissFederalGeoportal.NationalMapGrey", "SwissFederalGeoportal.SWISSIMAGE", "USGS.USImagery", \
        "USGS.USImageryTopo", "USGS.USTopo", "WaymarkedTrails.cycling", "WaymarkedTrails.hiking", \
        "WaymarkedTrails.mtb", "WaymarkedTrails.riding", "WaymarkedTrails.skating", "WaymarkedTrails.slopes",\
        "nlmaps.grijs", "nlmaps.luchtfoto", "nlmaps.pastel", "nlmaps.standaard", "nlmaps.water"]), help = "Choose to change basemap")
        if basemap != "Default":
            m.add_basemap(basemap = basemap)
        m.to_streamlit()