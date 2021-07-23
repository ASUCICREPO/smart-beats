import arcpy
import sys
import settings as s
from collections import defaultdict


def create_beats():
    args = defaultdict(lambda: None)

    for arg in sys.argv[1].split('<sep1>'):
        key, value = arg.split('<sep2>')
        args[key] = value

    print(args)

    arcpy.env.workspace = "arcgis-workspace/arcgis-workspace.gdb"

    print(f"spatial constraints: {args[s.spatial_constraints]}")
    print(f"Number of zones: {args[s.number_of_zones]}, spatial constraints: {args[s.spatial_constraints]}")

    # arcpy.stats.BuildBalancedZones("data/input/census_wise_crime_counts.shp",
    #                                f"data/output/{args[c.beat_name]}",
    #                                "ATTRIBUTE_TARGET", None, "count 15000 1", None,
    #                                "CONTIGUITY_EDGES_ONLY",
    #                                None, None, None, None, None, '', 100, 50, 0.1, None)

    arcpy.stats.BuildBalancedZones(args[s.input_shapefile_path], f"data/output/{args[s.beat_name]}",
                                   args[s.zone_creation_method],
                                   args[s.number_of_zones], f"{args[s.zone_building_criteria_target]}",
                                   args[s.zone_building_criteria], args[s.spatial_constraints], None, None, None, None,
                                   None, '', 100, 50, 0.1, None)


print("Executing Beats generator")
create_beats()
