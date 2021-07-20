import arcpy
import sys
import constants as c
from collections import defaultdict


def create_beats():
    args = defaultdict()

    for arg in sys.argv[1].split('<sep>'):
        key, value = arg.split('=')
        args[key] = value

    print(args)

    arcpy.env.workspace = "arcgis-workspace/arcgis-workspace.gdb"

    # arcpy.stats.BuildBalancedZones("data/input/census_wise_crime_counts.shp",
    #                                f"data/output/{args[c.beat_name]}",
    #                                "ATTRIBUTE_TARGET", None, "count 15000 1", None,
    #                                "CONTIGUITY_EDGES_ONLY",
    #                                None, None, None, None, None, '', 100, 50, 0.1, None)

    arcpy.stats.BuildBalancedZones(args[c.input_shapefile_path], f"data/output/{args[c.beat_name]}",
                                   args[c.zone_creation_method],
                                   args[c.number_of_zones], f"{args[c.zone_building_criteria_target]}",
                                   args[c.zone_building_criteria], args[c.spatial_constraints], None, None, None, None,
                                   None, '', 100, 50, 0.1, None)


print("Executing Beats generator")
create_beats()
