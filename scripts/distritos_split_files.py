import json


def distrito_padronizado(distrito: str) -> str:
    return distrito.lower().strip().replace("ã", "a").replace("â", "a").replace("á", "a").replace("é", "e").replace("í",
                                                                                                            "i").replace(
        "ô", "o").replace("ó", "o").replace("ú", "u").replace("ç", "c")


def entrypoint():
    f = open("../dados/formatado_sp_distritos.json", mode="r", encoding="utf-8")
    data = json.loads(f.read())
    f.close()

    for distrito in data["features"]:
        print(distrito["properties"]["name"])
        with open(("./distritos/" + distrito_padronizado(distrito["properties"]["name"]) + ".json"), "w",
                  encoding="utf8") as outfile:
            outfile.write(json.dumps({
                "distrito_pr": distrito_padronizado(distrito["properties"]["name"]),
                "distrito": distrito["properties"]["name"],
                "geometry": {
                    "type": distrito["geometry"]["type"],
                    "coordinates": distrito["geometry"]["coordinates"][0][0]
                }
            }, ensure_ascii=False))


if __name__ == "__main__":
    entrypoint()
