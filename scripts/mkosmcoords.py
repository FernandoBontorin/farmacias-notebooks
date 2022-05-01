import csv


def get_coord_text(x, y):
    return f"""                            [
                                {x},
                                {y}
                            ],"""


def entrypoint():
    """
    get console.log() latitude and longetude point (from osm-boundaries) and convert to geojson code style
    :return:
    """
    file = open("../dados/handcraftedcampolimpo.csv", mode="r", encoding="utf-8")
    csvreader = csv.reader(file)
    for row in csvreader:
        print(get_coord_text(row[1], row[0]))
    file.close()


if __name__ == "__main__":
    entrypoint()
