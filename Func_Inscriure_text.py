from PIL import Image, ImageDraw, ImageFont # Cal importar si no està globalment
import textwrap # Cal importar si no està globalment
import datetime

def inscriure_text_a_imatge(
    text_horoscop: str, 
    signe: str, 
    data_horoscop: str, # 👈 NOU PARÀMETRE: la data a mostrar
    path_plantilla: str, 
    path_font: str, 
    path_sortida: str
):
    """Superposa el text d'un horòscop a una imatge de plantilla, incloent-hi la data."""
    

    # 1. Càrrega i Configuració Inicial
    try:
        img = Image.open(path_plantilla).convert("RGB")
        img = img.rotate(90, expand=True)
    except FileNotFoundError:
        print(f"Error: La plantilla d'imatge no es troba a {path_plantilla}")
        return

    try:
        # Defineix les mides de la font
        font_titol_mida = 18
        font_data_mida = 10 # 👈 Mida més petita per a la data
        font_cos_mida = 12
        font_titol = ImageFont.truetype(path_font, font_titol_mida)
        font_data = ImageFont.truetype(path_font, font_data_mida) # 👈 Nova font per a la data
        font_cos = ImageFont.truetype(path_font, font_cos_mida)
    except FileNotFoundError:
        print(f"Error: El fitxer de font no es troba a {path_font}")
        return

    dibuix = ImageDraw.Draw(img)
    
    # 🌟 DEFINICIÓ DE COLORS
    color_text = (255, 255, 255) # Blanc
    
    # 2. Definició de Zones 
    w, h = img.size
    centre_x = w // 2
    
    # 3. Dibuixa el Títol (Signe del Zodíac)
    titol = f"HORÒSCOP {signe.upper()}"
    posicio_y_titol = 55 

    try:
        titol_w = font_titol.getlength(titol)
    except AttributeError:
        bbox = dibuix.textbbox((0, 0), titol, font=font_titol)
        titol_w = bbox[2] - bbox[0]
    except Exception:
          titol_w = len(titol) * (font_titol_mida // 2) 

    posicio_x_titol = centre_x - int(titol_w // 2)
    
    dibuix.text(
        (posicio_x_titol, posicio_y_titol), 
        titol, 
        font=font_titol, 
        fill=color_text
    )
    
    # --- 🆕 NOU: 3b. Dibuixa la Data ---
    
    posicio_y_data = posicio_y_titol + font_titol_mida + 5 # Just sota del títol + un petit marge
    
    try:
        data_w = font_data.getlength(data_horoscop)
    except AttributeError:
        bbox_data = dibuix.textbbox((0, 0), data_horoscop, font=font_data)
        data_w = bbox_data[2] - bbox_data[0]
    except Exception:
          data_w = len(data_horoscop) * (font_data_mida // 2) 
          
    posicio_x_data = centre_x - int(data_w // 2)
    
    dibuix.text(
        (posicio_x_data, posicio_y_data), 
        data_horoscop, 
        font=font_data, # 👈 Utilitza la font més petita
        fill=color_text
    )
    # ---------------------------------

    # 4. Processament del Cos del Text
    
    # La posició inicial 'y_text' es mou a sota de la data
    line_limit = 35 
    linies = textwrap.wrap(text_horoscop, width=line_limit)

    # Posició inicial per al cos del text
    y_text = posicio_y_data + font_data_mida + 10 # Es comença a dibuixar el cos del text més avall
    line_spacing = 16

    # 5. Dibuixa cada línia del Cos
    for linia in linies:
        try:
            line_w = font_cos.getlength(linia)
        except AttributeError:
            bbox_line = dibuix.textbbox((0, 0), linia, font=font_cos)
            line_w = bbox_line[2] - bbox_line[0]

        # Text centrat
        dibuix.text(
            (centre_x - int(line_w // 2), y_text), 
            linia, 
            font=font_cos, 
            fill=color_text
        )
        y_text += line_spacing 

    # 6. Guardar la imatge resultant
    img.save(path_sortida, quality=90)
    print(f"Imatge guardada correctament a: {path_sortida}")

# Utilitzem la data actual per als noms dels fitxers
DATA_ACTUAL = datetime.datetime.now().strftime("%d-%m-%Y")

RUTA_PLANTILLA = "plantilla.jpg" # Canvia per la teva ruta
RUTA_FONT = "arial.ttf" # Canvia per la teva ruta

path_imatge_sortida = f"Prova_h.jpg"
inscriure_text_a_imatge(
        text_horoscop="Això funciona, text de prova per afegir data al titol",
        signe="Aries",
        data_horoscop= DATA_ACTUAL,
        path_plantilla=RUTA_PLANTILLA,
        path_font=RUTA_FONT,
        path_sortida=path_imatge_sortida
        )