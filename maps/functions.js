function plotDistrito(map, name) {
    name = name.replace(" ", "%20") + ".json"
    const uri = "https://raw.githubusercontent.com/FernandoBontorin/farmacias-notebooks/master/dados/distritos-shapes/";
    fetch(uri + name)
        .then(response => response.text())
        .then(data => {
            L.polygon(JSON.parse(data).geometry.coordinates.map((e) => {
                return [e[1], e[0]];
            }), {color: 'red'}).addTo(map);
        });
}