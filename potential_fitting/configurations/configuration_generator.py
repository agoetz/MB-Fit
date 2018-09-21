# external package imports
import os

# absolute module imports
from potential_fitting.molecule import xyz_to_molecules
from potential_fitting.utils import SettingsReader, files, system

def generate_1b_configurations(settings_path, geo_path, normal_modes_path, dim_null, configurations_path):
    """
    Generates a set of 1b configurations for a molecule given its optimized geometry and normal modes.

    Args:
        settings_path       - Local path to the ".ini" file with relevant settings.
        geo_path            - Local path to the optimized geometry ".xyz" file.
        normal_modes_path   - Local path to the normal modes file as generated by generate_normal_modes().
        dim_null            - The null dimension of this molecule, as returned by generate_normal_modes().
        configurations_path - Local path to the file to write the configurations to.

    Returns:
        None.
    """

    print("Running normal distribution configuration generator...")
    
    settings = SettingsReader(settings_path)

    # read the optimized geometry    
    molecule = xyz_to_molecules(geo_path, settings)[0]

    input_path = files.init_file(os.path.join(settings.get("files", "log_path"), "config_generator", molecule.get_name() + ".in"))

    # construct the input file for the Fortran configurations generator code
    with open(input_path, "w") as input_file:
        input_file.write("'" + geo_path + "'\n") # path to optimized geometry
        input_file.write("'" + normal_modes_path + "'\n") # path to normal modes
        input_file.write(str(3 * molecule.get_num_atoms()) + " " + str(dim_null) + "\n") # dim followed by dimnull
        input_file.write(settings.get("config_generator", "random") + " " + settings.get("config_generator", "num_configs") + "\n") # random method followed by number of configs
        input_file.write("'" + config_path + "'\n") # path to output file
        input_file.write(settings.get("config_generator", "geometric") + " " + settings.get("config_generator", "linear") + "\n") # whether to use geometric progression followed by whether to use linear progression
        input_file.write(".true.") # provide verbose output
    
    log_path = files.init_file(os.path.join(settings.get("files", "log_path"), "config_generator", molecule.get_name() + ".log"))

    system.call("generate_configs_normdistrbn", "<", input_path, ">", log_path)

    print("Normal Distribution Configuration generation complete.")
