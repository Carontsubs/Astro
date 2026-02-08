import ephem
from datetime import datetime, timedelta
import math
import pytz

# Diccionaris
sign_elements = {
    'Aries': 'Foc',
    'Leo': 'Foc',
    'Sagittarius': 'Foc',
    'Taurus': 'Terra',
    'Virgo': 'Terra',
    'Capricorn': 'Terra',
    'Gemini': 'Aire',
    'Libra': 'Aire',
    'Aquarius': 'Aire',
    'Cancer': 'Aigua',
    'Scorpio': 'Aigua',
    'Pisces': 'Aigua'
}
sign_modalities = {
    'Aries': 'Cardinal',
    'Leo': 'Fixe',
    'Sagittarius': 'Mutable',
    'Taurus': 'Fixe',
    'Virgo': 'Mutable',
    'Capricorn': 'Cardinal',
    'Gemini': 'Mutable',
    'Libra': 'Cardinal',
    'Aquarius': 'Fixe',
    'Cancer': 'Cardinal',
    'Scorpio': 'Fixe',
    'Pisces': 'Mutable'
}

# Funcións
def get_zodiac_sign(longitude):
    zodiac_signs = [
        "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
        "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
    ]
    return zodiac_signs[int(longitude // 30)]

def find_lunar_nodes(start_date, end_date, step_hours=1):

    observer = ephem.Observer()
    observer.date = start_date
    
    lunar_nodes = []
    
    current_date = ephem.Date(start_date)
    last_latitude = None  # Última latitud eclíptica de la Lluna
    last_diff = None
    
    while current_date < ephem.Date(end_date):
        moon = ephem.Moon(current_date)
        
        # Latitud eclíptica de la Lluna (geocèntrica)
        moon_latitude = math.degrees(moon.hlat) # Convertim de radians a graus
        if last_latitude is not None:
            diff_latitude = moon_latitude - last_latitude    

            # Comprovem si ha creuat l'eclíptica (canvi de signe a hlat)
            if last_latitude < 0 and moon_latitude > 0:
                type = "Node Ascendent"
                lunar_nodes.append((current_date, type))
            elif last_latitude > 0 and moon_latitude < 0:
                type = "Node Descendent"
                lunar_nodes.append((current_date, type))

            # Detectar màxims i mínims (canvi de direcció)
            if last_diff is not None and last_diff * diff_latitude < 0:
                type = "Latitud Màxima" if last_diff > 0 else "Latitud Mínima"
                lunar_nodes.append((current_date, type))
            
            last_diff = diff_latitude

        # Actualitzar valors
        last_latitude = moon_latitude
        current_date = ephem.Date(current_date + step_hours * ephem.hour)
    
    return lunar_nodes

def track_planetary_signs(start_date, end_date, step_hours=1):
    planetes_info = []
    date = start_date
    planets = [ephem.Sun(), ephem.Moon()]
    
    last_signs = {p.name: None for p in planets}
    # Càlcul de la Lluna i el Sol
    
    while date <= end_date:
        for planet in planets:
            planet.compute(date)
                    # Obtenim el signe zodiacal i element

            # Obtenim la longitud eclíptica per tots els planetes
            if isinstance(planet, (ephem.Sun, ephem.Moon)):
                longitude = ephem.Ecliptic(planet).lon * 180 / ephem.pi  # Lluna i Sol (geocèntric)
            else:
                longitude = ephem.Ecliptic(planet).lon * 180 / ephem.pi  # Restants planetes (heliocèntric)

            sign = get_zodiac_sign(longitude)
            sign_element = sign_elements.get(sign, "Desconegut")
            sign_modalitie = sign_modalities.get(sign, "Desconegut")
            
            # Només comparem si el valor de last_signs no és None
            if last_signs[planet.name] is None:
                last_signs[planet.name] = sign
            if last_signs[planet.name] != sign:
                planetes_info.append((planet.name, sign, date.strftime('%Y-%m-%d %Hh'), sign_element, sign_modalitie, round(planet.phase), planet.hlat*10))
                last_signs[planet.name] = sign

        # Avançar al següent moment
        date += timedelta(hours=step_hours)
    
    return planetes_info

def calcular_distancia_lluna_terra(start_date, end_date):

    # Inicialitzar l'observador
    observer = ephem.Observer()

    # Inicialitzar la data actual com la data d'inici
    current_date = start_date

    distancies = []
    # Iterar per cada dia dins del període
    while current_date <= end_date:
        # Configurar la data per l'observador
        observer.date = current_date.strftime("%Y-%m-%d")  # Formatar la data per Ephem

        # Obtenir la Lluna
        moon = ephem.Moon(observer)

        # Distància entre la Lluna i la Terra (en km)
        distancia_lluna_terra = moon.earth_distance * 149597870.7  # Convertir a km
        
        # Emmagatzemar la distància i la data
        distancies.append((current_date, distancia_lluna_terra))
        
         
        # Passar al següent dia
        current_date += timedelta(days=1)

    return distancies

def determinar_tendencia(distancies):
    
    tendències = []
    tendència_precedent = None
    # data_precedent = len(distancies[0])

    # Comprovem la tendència comparant les distàncies de dos dies consecutius
    for i in range(1, len(distancies)):
        data_precedent, distancia_precedent = distancies[i-1]
        data_actual, distancia_actual = distancies[i]
        
        if distancia_actual < distancia_precedent:
            nova_tendència = "La Lluna es comença a acostar "
        elif distancia_actual > distancia_precedent:
            nova_tendència = "La Lluna es comença a allunyar"
        else:
            continue  # Si no hi ha canvi, no afegir res

        # Emmagatzemar només si la tendència és diferent de la anterior
        if tendència_precedent != nova_tendència:
            tendències.append((data_precedent, nova_tendència, distancia_precedent))
            tendència_precedent = nova_tendència

    return tendències

def lluna_plena_nova(start_date, end_date, step_hours=1):
    
    observer = ephem.Observer()
    observer.date = start_date
    
    llunes = []
    
    current_date = ephem.Date(start_date)

    while current_date < ephem.Date(end_date):
        moon = ephem.Moon(current_date)
        longitude = ephem.Ecliptic(moon).lon * 180 / ephem.pi  # Lluna i Sol (geocèntric)
        signe = get_zodiac_sign(longitude)
        
        if moon.phase > 99.5:
            type = "Lluna Plena"
            llunes.append((current_date, type, signe))
        elif moon.phase < 0.5:
            type = "Lluna Nova"
            llunes.append((current_date, type, signe))

        # Actualitzar valors
        current_date = ephem.Date(current_date + step_hours * ephem.hour)
    
    return llunes


# Exemple d'ús amb dates actuals
barcelona_tz = pytz.timezone('Europe/Madrid')
start_date = barcelona_tz.localize(datetime.now())
end_date = barcelona_tz.localize(datetime.now() + timedelta(weeks=8))
print()
print(start_date, end_date)

# Calcular 
distancies = calcular_distancia_lluna_terra(start_date, end_date)
tendències = determinar_tendencia(distancies)
nodes = find_lunar_nodes(start_date, end_date)
planetes_info = track_planetary_signs(start_date, end_date)
llunes = lluna_plena_nova(start_date,end_date)

# Imprimir
print()
lluna_previa = None
for data, lluna,signe in llunes:
    if lluna_previa != lluna:
        print(data, lluna, signe)
        lluna_previa = lluna
print()        

for data, tipus in nodes:
    print(data, tipus)
print()

for data, tendència, distancia in tendències[1:]:
    print(f"Data: {data} | {tendència} | Distancia: {round(distancia/1000)}")
print()

print(f"{'Planet':<10}{'Sign Entrant':<15}{'Data':<20}{'Element':<10}{'Modalitie':<12}{'Fase':<10}{'Latitutd*100'}")
print("-" * 120)
# Formatació de cada línia
for planeta, signe, data, element, modalitat, fase, latitud in planetes_info:
    print(f"{planeta:<10}{signe:<15}{data:<20}{element:<10}{modalitat:<12}{fase:<10}{round(latitud, 2)}")