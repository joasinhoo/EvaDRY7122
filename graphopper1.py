import requests
import urllib.parse

route_url = "https://graphhopper.com/api/1/route?"
key = "9db0905d-f6d0-4a77-b9e3-9b90d159e108"

def geocoding(location, key):
    while location == "":
        location = input("Ingrese la ubicación otra vez ")

    geocode_url = "https://graphhopper.com/api/1/geocode?" 
    url = geocode_url + urllib.parse.urlencode({"q":location, "limit": "1", "key":key})
    
    replydata = requests.get(url)
    json_data = replydata.json()
    json_status = replydata.status_code

    if json_status == 200 and len(json_data["hits"]) != 0:
        lat = json_data["hits"][0]["point"]["lat"]
        lng = json_data["hits"][0]["point"]["lng"]
        name = json_data["hits"][0]["name"]
        value = json_data["hits"][0]["osm_value"]
        
        if "country" in json_data["hits"][0]:
            country = json_data["hits"][0]["country"]
        else:
            country = ""
        
        if "state" in json_data["hits"][0]:
            state = json_data["hits"][0]["state"]
        else:
            state = ""
        
        if len(state) != 0 and len(country) != 0:
            new_loc = name + ", " + state + ", " + country
        elif len(state) != 0:
            new_loc = name + ", " + country
        else:
            new_loc = name
        
        print("URL de API de Geocodificación para " + new_loc + " (Tipo de Ubicación: " + value + ")\n" + url)
    else:
        lat = "null"
        lng = "null"
        new_loc = location
        if json_status != 200:
            print("Estado de la API de Geocodificación: " + str(json_status) + "\nMensaje de error: " + json_data.get("message", "Error desconocido"))
    
    return json_status, lat, lng, new_loc

def main():
    while True:
        loc1 = input("Ubicación de inicio 'q' para salir: ")
        if loc1.lower() == "q":
            break
        orig = geocoding(loc1, key)
        loc2 = input("Destino 'q' para salir: ")
        if loc2.lower() == "q":
            break
        dest = geocoding(loc2, key)
        print("*******************************************")
        if orig[0] == 200 and dest[0] == 200:
            op = "&point=" + str(orig[1]) + "%2C" + str(orig[2])
            dp = "&point=" + str(dest[1]) + "%2C" + str(dest[2])
            paths_url = route_url + urllib.parse.urlencode({"key": key}) + op + dp
            paths_status = requests.get(paths_url).status_code
            paths_data = requests.get(paths_url).json()
            print("Estado de la API de Enrutamiento: " + str(paths_status) + "\nURL de la API de Enrutamiento:\n" + paths_url)
            print("*******************************************")
            print("Instrucciones desde " + orig[3] + " hasta " + dest[3])
            print("*******************************************")
            if paths_status == 200:
                km = (paths_data["paths"][0]["distance"]) / 1000
                print("Distancia Recorrida: {0:.1f} km".format(km))
                sec = int(paths_data["paths"][0]["time"] / 1000 % 60)
                min = int(paths_data["paths"][0]["time"] / 1000 / 60 % 60)
                hr = int(paths_data["paths"][0]["time"] / 1000 / 60 / 60)
                print("Duración Viaje: {0:02d}:{1:02d}:{2:02d}".format(hr, min, sec))
                
                eficiencia_combustible = 10  # km por litro
                consumo_combustible = km / eficiencia_combustible
                print("Consumo de Combustible: {0:.2f} litros".format(consumo_combustible))
                
                print("*******************************************")
                print("Instrucciones de Ruta:")
                print("*******************************************")
                
                for each in range(len(paths_data["paths"][0]["instructions"])):
                    path = paths_data["paths"][0]["instructions"][each]["text"]
                    distance = paths_data["paths"][0]["instructions"][each]["distance"]
                    print("{0} ( {1:.1f} km )".format(path, distance/1000))
                
                print("*******************************************")
        
        print("\n\n")

if __name__ == "__main__":
    main()