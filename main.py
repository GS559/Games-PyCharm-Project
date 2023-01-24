from jproperties import Properties

import gui


def main() -> None:
    # loads the config file
    with open('config.properties', 'rb') as config_file:
        config = Properties()
        config.load(config_file)

    # loads the language pack file
    with open(f'lang/{config["language_pack"].data}.properties', 'rb') as language_pack_file:
        lang = Properties()
        lang.load(language_pack_file)

    # runs the main GUI
    gui.main(config=config, lang=lang)


main()
