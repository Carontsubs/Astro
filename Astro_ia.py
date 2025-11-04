from google import genai
from google.genai import types
import Astro_aux as aux
import os # Importem el mòdul os per accedir a les variables d'entorn
from dotenv import load_dotenv # Importem la funció per carregar .env
import datetime
import csv
# import Astro_aux as aux

dades_generades = aux.obtenir_info_astral_actual()
dades_generades_d = aux.obtenir_info_astral_actual(periode='diari')
# print(ad.obtenir_info_astral_actual())

# Carrega les variables d'entorn del fitxer .env
load_dotenv() 

# Obtenim la clau d'API. Si no la troba, generarà un error.
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Inicialitza el client passant la clau directament.
client = genai.Client(api_key=GEMINI_API_KEY)


# Definim la configuració per a totes les crides a l'API
configuracio_ia = types.GenerateContentConfig(
    temperature=0.5,        # Equilibri entre coherència i creativitat
    # max_output_tokens=350,  # Mantenir la resposta curta (aprox. 150 paraules)
    top_p=0.9,              # Bon control d'aleatorietat
    top_k=40,               # Limita la selecció a les 40 paraules més probables
    # stop_sequences=['.']  # Opcional: Aturar-se en un punt
)

# Llista dels 12 Signes del Zodíac
SIGNES_ZODIACALS = [
    "Àries", "Taure", "Bessons", "Cranc", "Lleó", "Verge", 
    "Balança", "Escorpí", "Sagitari", "Capricorn", "Aquari", "Peixos"
]

# Llista per emmagatzemar tots els horòscops generats
horoscops_generats = {}

# Utilitzem la data actual per als noms dels fitxers
DATA_ACTUAL = datetime.datetime.now().strftime("%d-%m-%Y")

# Defineix les rutes dels fitxers
RUTA_PLANTILLA = "plantilla.jpg" # Canvia per la teva ruta
RUTA_FONT = "arial.ttf" # Canvia per la teva ruta

#  Bucle d'Automatització: Generació dels 12 Posts

for signe in SIGNES_ZODIACALS:
    print(f"Generant horòscop per a: {signe}...")

    # 1. Crea el Prompt (Instrucció Personalitzada)
    prompt = f"""
    [ROL I INSTRUCCIONS]
    **ROL:** Ets Cassandra, l'astròloga que prove del mon dels comedy shows.
    
    **TONALITAT:** La teva tonalitat ha de ser calida, preocupada i col·loquial. Utilitza un llenguatge pesimista, 
    sarcastric i ple de humor negre.
    
    **RESTRICCIONS:**
    1. **Nomes pots veure i predir els esdeveniments NEGATIUS.**
    2. **Has de MINIMITZAR** tots els aspectes harmònics (Trígon 120º i Sextil 60º).
    3. **Has de MAXIMITZAR** en els aspectes de tensió: **Quadratura (90º), Oposició (180º) i Conjunció (0º).**
    4. La predicció ha de ser **breu (unes 80 paraules)**
    5. La teva resposta ha de ser concisa. Evita frases redundants i adjectius excessius. Ves directament al perill.

    Finalment si en les dades astronmiques que et proporciono no hi hagues cap aspecte major negatiu, centra les presdiccions en un to totalment pesimista.

        [DADES ASTRONÒMIQUES DE LA CONSULTA]

    A continuació, es proporcionen totes les dades astrològiques generades automàticament (posicions i aspectes):

            [DADES AVUI]
            ***
            {dades_generades}
            ***
            [DADES DEMÀ]
            *****
            {dades_generades_d}
            ***

    [SOL·LICITUD]
    Genera la teva predicció, que utiltzant **sarcasme, molt humor negre i llenguatge vulgar** i les dades de els **aspectes i les posicions
    dels planetes en els signes** sobretot **els astres que es troben en el signe**, de les dades astronomiques facilitades, 
    segons les teves instruccions de rol i les resticcions imposades per el {signe}.
    """

    # 2. Fes la crida a l'API
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=configuracio_ia,
        )

        # 3. Emmagatzema el resultat
        horoscops_generats[signe] = response.text
        print(f"Horòscop de {signe} generat correctament.")

    except Exception as e:
        horoscops_generats[signe] = f"ERROR: No s'ha pogut generar el text. ({e})"
        print(f"❌ ERROR en generar {signe}.")

# PAS NOU: GENERACIÓ DE LA IMATGE
    path_imatge_sortida = f"{signe.lower()}_h.jpg"
    aux.inscriure_text_a_imatge(
        text_horoscop=horoscops_generats[signe],
        signe=signe,
        data_horoscop= DATA_ACTUAL, # 👈 NOU PARÀMETRE: la data a mostrar
        path_plantilla=RUTA_PLANTILLA,
        path_font=RUTA_FONT,
        path_sortida=path_imatge_sortida
        )
    

# EXPORTACIÓ DELS RESULTATS

print("\n" + "="*50)
print("✨ EXPORTANT RESULTATS A ARXIUS... ✨")
print("="*50)


### 1. Exportació a Fitxer de Text (.txt) ###
fitxer_txt = f"horoscops_setmanals_{DATA_ACTUAL}.txt"
with open(fitxer_txt, 'w', encoding='utf-8') as f:
    f.write(f"GENERACIÓ D'HORÒSCOPS AUTOMÀTICS ({DATA_ACTUAL})\n")
    f.write(f"Dades Base: {dades_generades}\n\n")
    f.write("=" * 30 + "\n")
    f.write(f"Dades Base: {dades_generades_d}\n\n")
    f.write("=" * 30 + "\n")
    
    for signe, dades in horoscops_generats.items():
        f.write(f"--- {signe.upper()} ---\n")
        f.write(dades + "\n\n")

print(f"Exportat amb èxit a: **{fitxer_txt}**")

### 2. Exportació a Fitxer CSV (Per a Fulls de Càlcul) ###

# PAS 1: CONVERSIÓ DE L'ESTRUCTURA DE DADES
dades_per_csv = []
for signe, text in horoscops_generats.items():
    dades_per_csv.append({
        # Hem de dir-li al CSV que 'Àries' va a la columna 'Signe'
        "Signe": signe, 
        # I que el text complet va a la columna 'Text_Generat'
        "Text_Generat": text.replace('\n', ' ').strip() 
    })

fitxer_csv = f"horoscops_setmanals_{DATA_ACTUAL}.csv"
camps = ["Signe", "Text_Generat"] # Defineix les columnes

# PAS 2: Escriptura al CSV
with open(fitxer_csv, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=camps, delimiter=';')
    
    writer.writeheader()
    writer.writerows(dades_per_csv) # Passem la llista convertida
    
print(f"Exportat amb èxit a: **{fitxer_csv}**")


