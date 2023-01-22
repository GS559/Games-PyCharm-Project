from jproperties import Properties

import gui


def main() -> None:

    # loads the config file
    with open('config.properties', 'rb') as config_file:
        config = Properties()
        config.load(config_file)

    # runs the main GUI
    gui.main(config=config)

main()