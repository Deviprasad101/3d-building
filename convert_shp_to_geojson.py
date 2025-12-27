import geopandas as gpd

# ------------------------------------
# INPUT / OUTPUT PATHS
# ------------------------------------
shp_path = "data/buildings.shp"
output_geojson = "buildings.geojson"

# ------------------------------------
# LOAD SHAPEFILE
# ------------------------------------
gdf = gpd.read_file(shp_path)

# ------------------------------------
# ENSURE CRS = EPSG:4326 (WEB REQUIRED)
# ------------------------------------
if gdf.crs is None:
    gdf.set_crs(epsg=4326, inplace=True)
else:
    gdf = gdf.to_crs(epsg=4326)

# ------------------------------------
# AUTO CREATE BUILDING ID
# ------------------------------------
gdf["building_id"] = gdf.index + 1

# ------------------------------------
# AUTO HEIGHT (IF NOT PRESENT)
# ------------------------------------
if "height_m" not in gdf.columns:
    gdf = gdf.to_crs(epsg=3857)           # meters for area
    gdf["area_m2"] = gdf.geometry.area
    gdf["height_m"] = (gdf["area_m2"] * 0.05).clip(5, 120)
    gdf = gdf.to_crs(epsg=4326)

# ------------------------------------
# KEEP ONLY REQUIRED FIELDS
# ------------------------------------
gdf = gdf[["geometry", "building_id", "height_m"]]

# ------------------------------------
# SAVE AS GEOJSON
# ------------------------------------
gdf.to_file(output_geojson, driver="GeoJSON")

print("✅ buildings.geojson created successfully")