import arcpy
import sys
import settings as s
from collections import defaultdict


def create_beats():
    args = defaultdict(lambda: None)

    for arg in sys.argv[1].split('<param>'):
        key, value = arg.split('<=>')
        args[key] = value

    print(f'Build-balanced zones arguments: {args}')

    arcpy.env.workspace = "arcgis-workspace/arcgis-workspace.gdb"

    print(f"Zone creation method: {args[s.zone_creation_method]}, Number of zones: {args[s.number_of_zones]}, Zone building criteria target: {args[s.zone_building_criteria_target]}")
    print(f"Zone creation method: {args[s.zone_creation_method]}, Number of zones: {args[s.number_of_zones]}, Zone building criteria target: {args[s.zone_building_criteria_target]}")

    # arcpy.stats.BuildBalancedZones("data/input/census_wise_crime_counts.shp", f"data/output/{args[c.beat_name]}",
    #                                "ATTRIBUTE_TARGET",
    #                                None, "count 15000 1",
    #                                None, "CONTIGUITY_EDGES_ONLY", None, None, None, None,
    #                                None, '', 100, 50, 0.1, None)

    arcpy.stats.BuildBalancedZones(args[s.input_shapefile_path], f"data/output/{args[s.beat_name]}",
                                   args[s.zone_creation_method],
                                   args[s.number_of_zones], args[s.zone_building_criteria_target],
                                   args[s.zone_building_criteria], "CONTIGUITY_EDGES_ONLY", None, None, None, None,
                                   None, '', 100, 50, 0.1, None)


print("Executing Beats generator")
create_beats()
