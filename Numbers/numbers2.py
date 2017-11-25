import json


configFile = "./config.json"


# Load json config file
def loadJson():
    with open(configFile) as json_file:
        jsonData = json.load(json_file)
    return jsonData
###


def main():
    pass


if __name__ == '__main__':
    main()
