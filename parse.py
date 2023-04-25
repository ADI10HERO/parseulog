import argparse
import pyulog
import matplotlib.pyplot as plt
import os

from utils import get_battery_data_index


def parse_dir(dirpath, savepath):
    os.makedirs(savepath, exist_ok=True)

    for root, _, files in os.walk(dirpath):
        for file in files:
            # Construct the full path to the file
            input_file = os.path.join(root, file)

            # Call the generate_plot function to create and save the plot
            parse_ulog_file(
                input_file,
                plot=False,
                plot_dir=os.path.join(savepath, file)[:-4] + ".png",
            )


def parse_ulog_file(filepath, plot=False, plot_dir=None):
    """
    A wrapper function to parse a ULog file using pyulog parser.

    Parameters:
    filepath (str): The path of the ULog file to be parsed.

    Returns:
    data (dict): A dictionary containing the parsed data from the ULog file.
    """
    data = {}
    try:
        ulog = pyulog.ULog(filepath)
    except Exception as e:
        print("Error opening ULog file: {}".format(str(e)))
        return None

    index = get_battery_data_index(ulog.data_list)

    data["battery"] = {}
    data["battery"]["voltage"] = ulog.data_list[index].data["voltage_v"]
    data["battery"]["current"] = ulog.data_list[index].data["current_a"]
    data["battery"]["level"] = ulog.data_list[index].data["remaining"] * 100
    data["battery"]["timestamp"] = ulog.data_list[index].data["timestamp"]

    if plot:
        # Generate the plot
        fig, ax = plt.subplots()
        ax.plot(
            data["battery"]["timestamp"], data["battery"]["voltage"], label="Voltage"
        )
        ax.plot(
            data["battery"]["timestamp"], data["battery"]["current"], label="Current"
        )
        ax.plot(
            data["battery"]["timestamp"], data["battery"]["level"], label="Remaining %"
        )
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Voltage (V) / Current (A) / Remaining %age")
        ax.set_title("Battery Data")
        ax.legend()
        plt.show()
    elif plot_dir is not None:
        fig, ax = plt.subplots()
        ax.plot(
            data["battery"]["timestamp"], data["battery"]["voltage"], label="Voltage"
        )
        ax.plot(
            data["battery"]["timestamp"], data["battery"]["current"], label="Current"
        )
        ax.plot(
            data["battery"]["timestamp"], data["battery"]["level"], label="Remaining %"
        )
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Voltage (V) / Current (A) / Remaining %age")
        ax.set_title("Battery Data")
        ax.legend()
        plt.savefig(plot_dir)
    else:
        # Print the data
        print("Battery voltage: {} V".format(data["battery"]["voltage"]))
        print("Battery current: {} A".format(data["battery"]["current"]))
        print("Battery level: {} %".format(data["battery"]["level"]))
        print("Battery timestamp: {} s".format(data["battery"]["timestamp"]))

    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Wrapper function for parsing ULog files using pyulog parser."
    )
    parser.add_argument(
        "filepath", type=str, help="The path of the ULog file to be parsed"
    )
    parser.add_argument(
        "--dir",
        action="store_true",
        help="Whether the whole directory needs to be parsed",
    )
    parser.add_argument(
        "--plot", action="store_true", help="Whether to generate a plot of the data"
    )
    args = parser.parse_args()

    if args.dir:
        parse_dir(args.filepath, "plots")
    else:
        parsed_data = parse_ulog_file(args.filepath, args.plot)

    if parsed_data and not args.plot:
        # If the data was printed, save it to a text file
        with open("battery_data.txt", "w") as f:
            f.write("Battery voltage: {} V\n".format(parsed_data["battery"]["voltage"]))
            f.write("Battery current: {} A\n".format(parsed_data["battery"]["current"]))
            f.write("Battery level: {} %\n".format(parsed_data["battery"]["level"]))
