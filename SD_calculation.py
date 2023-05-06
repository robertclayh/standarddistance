import arcpy
from arcpy import env
from arcpy.sa import *

# Set the workspace environment
env.workspace = "C:/data"

# Input shapefiles
point_shapefile = "project_locations.shp"  # Shapefile with points representing project locations
polygon_shapefile = "federal_entities.shp"  # Shapefile with polygons representing federal entities

# Output shapefiles
standard_distance_output = "standard_distance.shp"  # Output shapefile with standard distance circles
polygon_output = "federal_entities_output.shp"  # Output shapefile with added proportion field

# Set the case field for the Standard Distance tool
case_field = "FederalEntity"  # Field in the shapefile reporting the federal entity implementing the project

# Calculate the standard distance for each federal entity
arcpy.StandardDistance_stats(point_shapefile, standard_distance_output, "StdDist", case_field)

# Add a field to the federal entities shapefile to store the proportion of the standard distance circle area
arcpy.AddField_management(polygon_shapefile, "Proportion", "DOUBLE")

# Join the standard distance shapefile to the federal entities shapefile based on the case field
arcpy.SpatialJoin_analysis(polygon_shapefile, standard_distance_output, polygon_output, match_option="INTERSECT", join_operation="JOIN_ONE_TO_ONE")

# Calculate the area of the standard distance circle for each federal entity
arcpy.AddField_management(polygon_output, "CircleArea", "DOUBLE")
arcpy.CalculateField_management(polygon_output, "CircleArea", "!StdDist! * !StdDist! * 3.14159265359", "PYTHON_9.3")

# Calculate the area of the polygon for each federal entity
arcpy.AddField_management(polygon_output, "PolygonArea", "DOUBLE")
arcpy.CalculateField_management(polygon_output, "PolygonArea", "!SHAPE.area!", "PYTHON_9.3")

# Calculate the proportion of the standard distance circle area to the polygon area for each federal entity
arcpy.CalculateField_management(polygon_output, "Proportion", "!CircleArea! / !PolygonArea!", "PYTHON_9.3")

print("Standard distance and proportion calculation completed.")
