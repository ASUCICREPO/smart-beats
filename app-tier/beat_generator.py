import arcpy
import sys
import shapefile
import settings as s
import utils as u
from collections import defaultdict

args = defaultdict(lambda: None)


def create_beats():
    for arg in sys.argv[1].split('<param>'):
        key, value = arg.split('<=>')
        args[key] = value

    print(f'Build-balanced zones arguments: {args}')
    get_beats_threshold()

    arcpy.env.workspace = "arcgis-workspace/arcgis-workspace.gdb"

    print(
        f"Zone creation method: {args[s.zone_creation_method]}, Number of zones: {args[s.number_of_zones]}, Zone "
        f"building criteria target: {args[s.zone_building_criteria_target]}")

    if args[s.zone_creation_method] == "ATTRIBUTE_TARGET":
        run_build_balanced_zones()
    else:
        if args[s.number_of_zones]:
            beats_count_calibrator(int(args[s.number_of_zones]), get_beats_threshold())
        else:
            print("Number of zones provided is Null.")

    # arcpy.stats.BuildBalancedZones("data/input/census_wise_crime_counts.shp", f"data/output/{args[c.beat_name]}",
    #                                "ATTRIBUTE_TARGET",
    #                                None, "count 15000 1",
    #                                None, "CONTIGUITY_EDGES_ONLY", None, None, None, None,
    #                                None, '', 100, 50, 0.1, None)


def get_beats_threshold():
    input_sf = shapefile.Reader(args[s.input_shapefile_path])
    return len(input_sf.shapes()) - 1


def run_build_balanced_zones(n_test=None):
    output_path = f"data/output/{args[s.beat_name]}"

    arcpy.stats.BuildBalancedZones(args[s.input_shapefile_path], output_path,
                                   args[s.zone_creation_method],
                                   n_test, args[s.zone_building_criteria_target],
                                   args[s.zone_building_criteria], "CONTIGUITY_EDGES_ONLY", None, None, None, None,
                                   None, '', 100, 50, 0.1, None)

    print(f"Output shapefile path: {output_path}.shp")
    sf = shapefile.Reader(f"{output_path}.shp")
    zones_set = set()

    for r in sf.records():
        zones_set.add(r[2])

    total_zones = len(zones_set)

    print(f"***Total zones calculated = {total_zones}***")

    return total_zones


def beats_count_calibrator(n, total_beats_threshold):
    offset = 0
    trials = 20

    while trials > 0:
        print(f"Trial number: {trials}")

        n_test = min(n + offset, total_beats_threshold)

        print(f"n_test value: {n_test}")

        total_zones = run_build_balanced_zones(n_test)
        error = n - total_zones

        print(f"xx error val: {error} xx")

        if error == 0:
            break
        else:
            offset += error
            print(f"New offset value: {offset}")

        trials -= 1
        if trials > 0:
            u.delete_file(f"data/output/{args[s.beat_name]}", 0)


print("Executing Beats generator")
create_beats()
