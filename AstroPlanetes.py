import ephem
from datetime import datetime
from itertools import combinations
import math

# Definir els signes del zodíac
zodiac_signs = [
    (0, "Àries"), (30, "Taure"), (60, "Bessons"), (90, "Cranc"),
    (120, "Lleó"), (150, "Verge"), (180, "Balança"), (210, "Escorpí"),
    (240, "Sagitari"), (270, "Capricorn"), (300, "Aquari"), (330, "Peixos")
]

# Definir aspectes astrològics i llindars d'orbe
aspects = {
    "Conjunció": (0, 10),
    "Oposició": (180, 10),
    "Trígon": (120, 8),
    "Quadratura": (90, 8),
    "Sextil": (60, 6)
}

# Funció per trobar el signe zodiacal i la posició relativa
def get_zodiac_sign(degrees):
    for limit, sign in reversed(zodiac_signs):
        if degrees >= limit:
            return sign, degrees - limit
    return "Desconegut", 0

# Funció per calcular aspectes
def get_aspects(planets):
    aspect_list = []
    for (p1, obj1), (p2, obj2) in combinations(planets.items(), 2):
        lon1 = ephem.Ecliptic(obj1).lon * 180 / ephem.pi
        lon2 = ephem.Ecliptic(obj2).lon * 180 / ephem.pi
        angle = abs(lon1 - lon2)
        if angle > 180:
            angle = 360 - angle
        
        for aspect, (exact_angle, orb) in aspects.items():
            if abs(angle - exact_angle) <= orb:
                aspect_list.append(f"{p1} i {p2}: {aspect} ({angle:.2f}°)")
    return aspect_list

def get_ascendant(date, time, location_lat, location_lon):
    observer = ephem.Observer()
    observer.date = f"{date} {time}"
    observer.lat = str(location_lat)
    observer.lon = str(location_lon)

    # Calcular el punt de l'ascendent (l'horitzó oriental)
    # Utilitzem un objecte com a referència qualsevol estrella com Vega
    observer.elevation = 0  # Elevació a nivell del mar
    observer.pressure = 1010  # Pressió atmosfèrica en mbar
    observer.temp = 10  # Temperatura en Celsius (no molt important però es pot afegir)

    # Usant una estrella com a referència
    star = ephem.star("Vega")  # Així es fa per referenciar una estrella

    # Trobar l'ascendent, és a dir, el moment en què una estrella emergeix per l'horitzó oriental
    ascendant_time = observer.next_rising(star) 

    # Actualitzar la data de l'observador a aquest moment de l'ascendent
    observer.date = ascendant_time

    # Obtenir la longitud eclíptica de l'ascendent en aquest moment
    sun = ephem.Sun(observer)
    ecl = ephem.Ecliptic(sun)
    ascendant_lon = ecl.lon * 180 / ephem.pi  # Convertir la longitud eclíptica en graus

    # Corregir la longitud eclíptica perquè estigui dins el rang [0, 360)
    if ascendant_lon < 0:
        ascendant_lon += 360  # Per assegurar-nos que estigui dins del rang [0, 360)

    return ascendant_lon

# Definir la data, hora i lloc del naixement per calcular l'ascendent
date_of_birth = '1978/09/29'  # Any/Mes/Dia
time_of_birth = '13:30:00'    # Hora en format HH:MM:SS
location_latitude = 41.3784   # Latitud de Barcelona
location_longitude = 2.1925  # Longitud de Barcelona
# Obtenir la data actual en format datetime
data_str = "29-09-1978, 13:30:00"
now = datetime.strptime(data_str, "%d-%m-%Y, %H:%M:%S")
print(data_str)

# Calcular les posicions planetàries
planetes = {
    "Sol": ephem.Sun(now),
    "Lluna": ephem.Moon(now),
    "Mercuri": ephem.Mercury(now),
    "Venus": ephem.Venus(now),
    "Mart": ephem.Mars(now),
    "Júpiter": ephem.Jupiter(now),
    "Saturn": ephem.Saturn(now),
    "Urà": ephem.Uranus(now),
    "Neptú": ephem.Neptune(now),
    "Plutó": ephem.Pluto(now)
}

# Mostrar posicions planetàries
print("Posició dels planetes en el zodíac:")
for planeta, obj in planetes.items():
    ecl = ephem.Ecliptic(obj)  # Convertir a coordenades eclíptiques
    ecl_lon = ecl.lon * 180 / ephem.pi  # Longitud eclíptica en graus
    signe, graus_relatius = get_zodiac_sign(ecl_lon)
    print(f"{planeta}: {signe} ({graus_relatius:.2f}°)")

# Calcular l'ascendent
ascendant_lon = get_ascendant(date_of_birth, time_of_birth, location_latitude, location_longitude)
ascendant_sign, ascendant_degrees = get_zodiac_sign(ascendant_lon)

# Mostrar l'ascendent
print(f"\nL'ascendent està a {ascendant_sign} ({ascendant_degrees:.2f}°)")

# Calcular i mostrar aspectes
print("\nAspectes planetaris:")
aspectes_trobats = get_aspects(planetes)
for aspecte in aspectes_trobats:
    print(aspecte)
    
    
print(now)
mars = ephem.Mars()
observer = ephem.Observer()
observer.date = f"{date_of_birth} {time_of_birth}"
observer.lat = str(location_latitude)
observer.lon = str(location_longitude)
observer.elevation = 0  # Elevació a nivell del mar
observer.pressure = 1010  # Pressió atmosfèrica en mbar
observer.temp = 10  # Temperatura en Celsius (no molt important però es pot afegir)

mars.compute(observer)
print(ephem.constellation(mars))
