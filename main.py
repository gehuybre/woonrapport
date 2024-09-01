import json

import matplotlib.colors as mcolors
import plotly.io as pio
from jinja2 import Template


def genereer_kleurenschema(startkleur='#7fe0de', eindkleur='#313131', aantal_kleuren=5):
    """
    Genereer een lijst van kleuren gebaseerd op een lineair kleurverloop tussen de startkleur en de eindkleur.
    """
    # Zorg ervoor dat aantal_kleuren minimaal 2 is om deling door nul te voorkomen
    if aantal_kleuren < 2:
        aantal_kleuren = 2

    # Zet de hexadecimale kleurcodes om naar RGB
    start_rgb = mcolors.hex2color(startkleur)
    eind_rgb = mcolors.hex2color(eindkleur)

    # Genereer de kleuren met een lineair kleurverloop
    kleuren = [mcolors.rgb2hex(
        [(start_rgb[j] + (float(i) / (aantal_kleuren - 1)) * (eind_rgb[j] - start_rgb[j])) for j in range(3)]
    ) for i in range(aantal_kleuren)]

    return kleuren

def genereer_css(kleuren):
    """
    Genereert de CSS content met de opgegeven kleuren.
    """
    return f"""
    body {{ 
        font-family: 'Georama', sans-serif; 
        line-height: 1.6; 
        color: #313131; 
        max-width: 800px; 
        margin: 0 auto; 
        padding: 20px;
        background-color: #ffffff;
    }}
    .gemeente-rapport {{
        background-color: rgba(255, 255, 255, 0); /* Transparante achtergrond */
        padding: 30px;
        margin-bottom: 40px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }}
    h1 {{ 
        color: #313131; 
        font-size: 32px; 
        border-bottom: 2px solid {kleuren[0]}; /* Gebruik de eerste kleur uit het gegenereerde schema */
        padding-bottom: 10px; 
    }}
    h2 {{ 
        color: #313131; 
        font-size: 24px; 
        margin-top: 30px; 
        border-bottom: 2px solid {kleuren[1]}; /* Gebruik de tweede kleur uit het gegenereerde schema */
    }}
    .highlight {{
        background-color: {kleuren[0]}; /* Gebruik de eerste kleur uit het gegenereerde schema */
        padding: 2px 5px;
        font-weight: bold;
    }}
    .donut {{
        width: 60px; /* Iets grotere breedte voor de donut */
        height: 60px; /* Iets grotere hoogte voor de donut */
        border-radius: 50%; /* Zorgt voor een cirkelvorm */
        background: conic-gradient({kleuren[0]}, {kleuren[2]}); /* Kleurverloop van startkleur naar donkerdere eindkleur */
        position: relative; /* Positie om het middengat te centreren */
        margin-right: 10px;
    }}
    .donut::before {{
        content: '';
        width: 30px; /* Iets grotere grootte van het middengat om de donut dikker te maken */
        height: 30px; /* Iets grotere grootte van het middengat om de donut dikker te maken */
        background-color: #f0f0f0; /* Kleur van het middengat, moet overeenkomen met de achtergrond van de footer */
        border-radius: 50%;
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%); /* Centreer het gat */
    }}
    .logo-container {{
        display: flex;
        align-items: center;
        background-color: #f0f0f0; /* Lichtgrijze achtergrond voor de footer */
        padding: 10px 20px;
        justify-content: flex-start; /* Zorgt ervoor dat de inhoud links uitgelijnd is */
        width: 100%; /* Zorgt ervoor dat de container de volledige breedte benut */
    }}
    .logo-text {{
        color: #313131;
        font-size: 2em; /* Grotere tekstgrootte voor de naam */
        font-family: Georama, sans-serif;
        display: flex;
        flex-direction: column;
        align-items: flex-start; /* Links uitlijnen van de tekst */
        font-weight: 800; 
        line-height: 1.1; /* Verkleint de verticale ruimte tussen tekstregels */
        text-align: left; /* Zorgt ervoor dat de tekst links uitgelijnd is */
        width: fit-content; /* Zorgt ervoor dat de container alleen de ruimte inneemt die nodig is voor de tekst */
    }}
    .sub-text {{
        font-size: 0.8em; /* Kleiner lettertype voor de ondertitel */
        color: #313131;
        font-weight: 800; 
        width: 100%; /* Zorgt ervoor dat de breedte van de subtekst dezelfde is als de container van de logo-tekst */
        text-align: left; /* Zorgt ervoor dat de subtekst links uitgelijnd is */
    }}
    footer {{
        margin-top: 40px;
        padding-top: 20px;
        background-color: #f0f0f0; /* Lichtgrijze achtergrond voor de footer */
        font-size: 14px;
        display: flex;
        align-items: center;
        padding: 20px;
    }}
    .bronvermelding {{
        text-align: center; /* Center de bronvermelding */
        font-style: italic;
        font-size: 12px;
        margin-top: 10px;
        color: #313131;
    }}
    .aanbevelingen-sectie {{
        background-color: #f7f7f7; /* Lichtgrijze achtergrond om het te onderscheiden */
        border-left: 4px solid {kleuren[0]}; /* Gebruik een linkerbalk in de startkleur om het te laten opvallen */
        padding: 15px 20px;
        margin-top: 20px;
        margin-bottom: 30px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1); /* Subtiele schaduw voor een licht 3D-effect */
    }}
    .aanbevelingen-sectie h3 {{
        color: #313131; /* Donkerder kleur voor de koptekst */
        font-family: 'Georama', sans-serif;
        font-size: 1.4em;
        font-weight: 800; /* Dikkere tekst voor de koptekst */
        margin-bottom: 10px;
    }}
    .aanbevelingen-tekst {{
        font-size: 1em; /* Normale tekstgrootte voor de inhoud */
        color: #555555; /* Iets donkerder grijs voor de tekst */
        line-height: 1.6;
        font-style: italic; /* Cursief voor een onderscheidende stijl */
    }}
    ul.aanbevelingen-tekst {{
    font-size: 1em; /* Normale tekstgrootte voor de inhoud */
    color: #555555; /* Iets donkerder grijs voor de tekst */
    line-height: 2;
    font-style: italic; /* Cursief voor een onderscheidende stijl */
    padding-left: 20px; /* Inspringen voor de lijst */
    margin-top: 1;
    margin-bottom: 1;
}}

    """

def apply_chart_layout(fig, title, yaxis_title, aantal_kleuren=5):
    # Genereer een kleurenschema
    kleuren = genereer_kleurenschema(startkleur='#7fe0de', eindkleur='#313131', aantal_kleuren=aantal_kleuren)

    # Stel de layout in
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=16)
        ),
        yaxis_title=yaxis_title,
        font=dict(family='Arial, sans-serif', size=12),
        plot_bgcolor='white',  # Witte achtergrond voor een minimalistisch ontwerp
        showlegend=True,
        legend=dict(
            orientation="h",  # Horizontale oriëntatie van de legende
            yanchor="top",
            y=-0.2,  # Plaats de legende onder de grafiek
            xanchor="center",
            x=0.5
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='LightGray'  # Subtiele rasterlijnen
        ),
        xaxis=dict(
            showgrid=False  # Geen rasterlijnen voor de x-as
        )
    )

    # Pas kleuren toe op de grafiek
    for i, trace in enumerate(fig.data):
        if hasattr(trace, 'marker') and 'color' not in trace.marker:
            trace.marker.color = kleuren[i % len(kleuren)]  # Gebruik een kleur uit het gegenereerde schema

    return fig




# Stap 1: Data inladen
with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)


# Helper functies
def vind_vlaams_gewest_data(alle_data):
    """
    Zoekt de gegevens voor 'Vlaams Gewest' in de lijst van alle gegevens.
    """
    for item in alle_data:
        if item.get("Gemeente") == "Vlaams Gewest":
            return item
    return None  # Retourneer None als 'Vlaams Gewest' niet wordt gevonden



def bereken_vastgoedprijs_stijging(gemeente_data):
    start_prijs = float(gemeente_data["Mediaanprijs huizen, 2014(in euro)"].replace(',', ''))
    eind_prijs = float(gemeente_data["Mediaanprijs huizen, 2023(in euro)"].replace(',', ''))
    stijging = ((eind_prijs - start_prijs) / start_prijs) * 100
    return start_prijs, eind_prijs, stijging

def bereken_vastgoedprijs_stijging_vlaams(vlaams_data):
    start_prijs_vlaams = float(vlaams_data["Mediaanprijs huizen, 2014(in euro)"].replace(',', ''))
    eind_prijs_vlaams = float(vlaams_data["Mediaanprijs huizen, 2023(in euro)"].replace(',', ''))
    stijging_vlaams = ((eind_prijs_vlaams - start_prijs_vlaams) / start_prijs_vlaams) * 100
    return start_prijs_vlaams, eind_prijs_vlaams, stijging_vlaams



def bereken_huishoudensgroei(gemeente_data):
    """Berekent de absolute en procentuele groei van het aantal huishoudens tussen 2023 en 2040 voor een gegeven gemeente."""
    bevolking_2023 = int(gemeente_data["Aantal huishoudens-2023"].replace(',', ''))
    bevolking_2040 = int(gemeente_data["Aantal huishoudens-2040"].replace(',', ''))
    groei = ((bevolking_2040 - bevolking_2023) / bevolking_2023) * 100
    return bevolking_2023, bevolking_2040, groei


def bereken_huishoudensgroei_vlaams(vlaams_data):
    """Berekent de absolute en procentuele groei van het aantal huishoudens tussen 2023 en 2040 voor het Vlaams Gewest."""
    bevolking_2023_vlaams = int(vlaams_data["Aantal huishoudens-2023"].replace(',', ''))
    bevolking_2040_vlaams = int(vlaams_data["Aantal huishoudens-2040"].replace(',', ''))
    groei_vlaams = ((bevolking_2040_vlaams - bevolking_2023_vlaams) / bevolking_2023_vlaams) * 100
    return bevolking_2023_vlaams, bevolking_2040_vlaams, groei_vlaams

def bereken_eenpersoonshuishoudensgroei(gemeente_data):
    """
    Berekent de absolute en procentuele groei van het aantal eenpersoonshuishoudens tussen 2023 en 2040 voor een gegeven gemeente.
    """
    eenpersoonshuishoudens_2023 = int(gemeente_data["Aantal eenpersoonshuishoudens 2023"].replace(',', ''))
    eenpersoonshuishoudens_2040 = int(gemeente_data["Aantal eenpersoonshuishoudens 2040"].replace(',', ''))
    groei = ((eenpersoonshuishoudens_2040 - eenpersoonshuishoudens_2023) / eenpersoonshuishoudens_2023) * 100
    return eenpersoonshuishoudens_2023, eenpersoonshuishoudens_2040, groei

def bereken_eenpersoonshuishoudensgroei_vlaams(vlaams_data):
    """
    Berekent de absolute en procentuele groei van het aantal eenpersoonshuishoudens tussen 2023 en 2040 voor het Vlaams Gewest.
    """
    eenpersoonshuishoudens_2023_vlaams = int(vlaams_data["Aantal eenpersoonshuishoudens 2023"].replace(',', ''))
    eenpersoonshuishoudens_2040_vlaams = int(vlaams_data["Aantal eenpersoonshuishoudens 2040"].replace(',', ''))
    groei_vlaams = ((eenpersoonshuishoudens_2040_vlaams - eenpersoonshuishoudens_2023_vlaams) / eenpersoonshuishoudens_2023_vlaams) * 100
    return eenpersoonshuishoudens_2023_vlaams, eenpersoonshuishoudens_2040_vlaams, groei_vlaams

def bereken_wateroverlast_en_hittestress_stijging(gemeente_data):
    """
    Berekent de stijging van kwetsbare personen blootgesteld aan hittestress en gebouwen met mogelijke wateroverlast
    voor een gegeven gemeente.
    """
    hittestress_2030 = float(gemeente_data.get("Kwetsbare personen blootgesteld aan hittestress Hoog impact 2030", 0))
    hittestress_2050 = float(gemeente_data.get("Kwetsbare personen blootgesteld aan hittestress Hoog impact 2050", 0))
    wateroverlast_huidig = float(gemeente_data.get("Aandeel gebouwen met mogelijke wateroverlast in huidig klimaat", 0))
    wateroverlast_2050 = float(gemeente_data.get("Aandeel gebouwen met mogelijke wateroverlast in 2050", 0))

    stijging_hittestress = ((hittestress_2050 - hittestress_2030) / hittestress_2030) * 100 if hittestress_2030 else 0
    stijging_wateroverlast = ((wateroverlast_2050 - wateroverlast_huidig) / wateroverlast_huidig) * 100 if wateroverlast_huidig else 0

    return hittestress_2030, hittestress_2050, stijging_hittestress, wateroverlast_huidig, wateroverlast_2050, stijging_wateroverlast

def bereken_wateroverlast_en_hittestress_stijging_vlaams(vlaams_data):
    """
    Berekent de stijging van kwetsbare personen blootgesteld aan hittestress en gebouwen met mogelijke wateroverlast
    voor het Vlaamse Gewest.
    """
    hittestress_2030_vlaams = float(vlaams_data.get("Kwetsbare personen blootgesteld aan hittestress Hoog impact 2030", 0))
    hittestress_2050_vlaams = float(vlaams_data.get("Kwetsbare personen blootgesteld aan hittestress Hoog impact 2050", 0))
    wateroverlast_huidig_vlaams = float(vlaams_data.get("Aandeel gebouwen met mogelijke wateroverlast in huidig klimaat", 0))
    wateroverlast_2050_vlaams = float(vlaams_data.get("Aandeel gebouwen met mogelijke wateroverlast in 2050", 0))

    stijging_hittestress_vlaams = ((hittestress_2050_vlaams - hittestress_2030_vlaams) / hittestress_2030_vlaams) * 100 if hittestress_2030_vlaams else 0
    stijging_wateroverlast_vlaams = ((wateroverlast_2050_vlaams - wateroverlast_huidig_vlaams) / wateroverlast_huidig_vlaams) * 100 if wateroverlast_huidig_vlaams else 0

    return hittestress_2030_vlaams, hittestress_2050_vlaams, stijging_hittestress_vlaams, wateroverlast_huidig_vlaams, wateroverlast_2050_vlaams, stijging_wateroverlast_vlaams



def genereer_huishoudens_grafiek(gemeente, gemeente_data):
    # Definieer de jaren voor de grafiek (om de 4 jaar)
    jaren = [str(jaar) for jaar in range(2023, 2041, 4)]

    # Keer de volgorde van de jaren om zodat het meest recente jaar bovenaan komt
    jaren = jaren[::-1]

    # Haal de aantallen huishoudens per jaar op voor de opgegeven gemeente
    aantallen_huishoudens = [int(gemeente_data[f"Aantal huishoudens-{jaar}"].replace(',', '')) for jaar in jaren]
    aantallen_eenpersoonshuishoudens = [int(gemeente_data[f"Aantal eenpersoonshuishoudens {jaar}"].replace(',', '')) for jaar in jaren]

    # Genereer kleurenschema met de gewenste kleuren
    kleuren = genereer_kleurenschema(startkleur='#7fe0de', eindkleur='#313131', aantal_kleuren=2)

    # Maak een nieuwe figuur voor de side-by-side grafiek
    fig = make_subplots(rows=1, cols=2, subplot_titles=(f"Aantal huishoudens", f"Aantal eenpersoonshuishoudens"))

    # Voeg de balkgrafiek toe voor de bevolkingsgroei
    fig.add_trace(go.Bar(
        x=aantallen_huishoudens,
        y=jaren,
        text=[f"{aantal}" for aantal in aantallen_huishoudens],  # Voeg de aantallen toe als tekstlabels op de balken
        textposition='inside',  # Plaats de tekstlabels binnen de balken
        insidetextanchor='middle',  # Centreer de tekstlabels in het midden van de balk
        textfont=dict(size=12, color='white'),  # Vergroot de tekst en maak deze wit voor contrast
        orientation='h',  # Maak de balken horizontaal
        name=f'Bevolkingsgroei in {gemeente}',
        marker_color=kleuren[0]  # Gebruik de eerste kleur uit het gegenereerde schema
    ), row=1, col=1)

    # Voeg de balkgrafiek toe voor het aantal eenpersoonshuishoudens
    fig.add_trace(go.Bar(
        x=aantallen_eenpersoonshuishoudens,
        y=jaren,
        text=[f"{aantal}" for aantal in aantallen_eenpersoonshuishoudens],  # Voeg de aantallen toe als tekstlabels op de balken
        textposition='inside',  # Plaats de tekstlabels binnen de balken
        insidetextanchor='middle',  # Centreer de tekstlabels in het midden van de balk
        textfont=dict(size=12, color='white'),  # Vergroot de tekst en maak deze wit voor contrast
        orientation='h',  # Maak de balken horizontaal
        name=f'Eenpersoonshuishoudens in {gemeente}',
        marker_color=kleuren[1]  # Gebruik de tweede kleur uit het gegenereerde schema
    ), row=1, col=2)

    # Pas de gestandaardiseerde layout toe zonder dat de assen bij 0 beginnen
    apply_chart_layout(
        fig,
        f"Aantal Huishoudens in {gemeente} (2023-2040)",
        'Aantal huishoudens',
        aantal_kleuren=2  # Stel het aantal kleuren in dat je nodig hebt
    )

    # Zorg ervoor dat de y-as niet bij 0 begint
    fig.update_layout(
        yaxis=dict(rangemode='normal')  # Zorgt ervoor dat de y-as niet vanaf 0 begint
    )

    return pio.to_html(fig, full_html=False, include_plotlyjs='cdn')



def genereer_vastgoedprijs_grafiek(gemeente, gemeente_data, alle_data):
    jaren = ["2014", "2023"]

    # Haal de gegevens voor de Vlaamse vastgoedprijzen op
    vlaams_data = vind_vlaams_gewest_data(alle_data)

    # Zorg ervoor dat de prijzen als floats worden behandeld
    prijzen_gemeente = [float(gemeente_data[f"Mediaanprijs huizen, {jaar}(in euro)"].replace(',', '')) for jaar in jaren]
    prijzen_vlaams = [float(vlaams_data[f"Mediaanprijs huizen, {jaar}(in euro)"].replace(',', '')) for jaar in jaren]

    # Genereer kleurenschema met de gewenste kleuren
    kleuren = genereer_kleurenschema(startkleur='#7fe0de', eindkleur='#313131', aantal_kleuren=2)

    fig = go.Figure()

    # Trace voor de prijzen in 2014
    fig.add_trace(go.Bar(
        x=[gemeente, 'Vlaams Gewest'],
        y=[prijzen_gemeente[0], prijzen_vlaams[0]],
        name='2014',
        marker_color=kleuren[0],  # Gebruik de eerste kleur uit het gegenereerde schema
        text=[f"€{prijzen_gemeente[0]:,.0f}", f"€{prijzen_vlaams[0]:,.0f}"],  # Voeg de labels toe
        textposition='auto'  # Plaats de tekst automatisch op de juiste plek op de balk
    ))

    # Trace voor de prijzen in 2023
    fig.add_trace(go.Bar(
        x=[gemeente, 'Vlaams Gewest'],
        y=[prijzen_gemeente[1], prijzen_vlaams[1]],
        name='2023',
        marker_color=kleuren[1],  # Gebruik de tweede kleur uit het gegenereerde schema
        text=[f"€{prijzen_gemeente[1]:,.0f}", f"€{prijzen_vlaams[1]:,.0f}"],  # Voeg de labels toe
        textposition='auto'  # Plaats de tekst automatisch op de juiste plek op de balk
    ))

    # Pas de gestandaardiseerde layout toe, automatisch kleuren toepassen
    apply_chart_layout(
        fig,
        f"Vastgoedprijs Stijging in {gemeente} vs. Vlaams Gewest",
        'Prijs (in euro)',
        aantal_kleuren=2  # Stel het aantal kleuren in dat je nodig hebt
    )

    return pio.to_html(fig, full_html=False, include_plotlyjs='cdn')


from plotly.subplots import make_subplots
import plotly.graph_objs as go


def genereer_epc_grafiek(data_gemeente, data_vlaams, gemeente):
    """
    Genereert een side-by-side grafiek van EPC-labels voor zowel de gemeente als het Vlaamse Gewest.
    """
    # Gebruik de directe velden uit de data
    jaren = ['2023']  # Alleen data voor 2023 beschikbaar
    kleuren = genereer_kleurenschema(aantal_kleuren=4)

    # Bereken de gegevens voor de grafiek
    categorieen = ['A/A+', 'B', 'C', 'D/E/F']
    data_series_gemeente = {
        'A/A+': float(data_gemeente.get('Categorie A+-2023 EPC', 0)) + float(
            data_gemeente.get('Categorie A-2023 EPC', 0)),
        'B': float(data_gemeente.get('Categorie B-2023 EPC', 0)),
        'C': float(data_gemeente.get('Categorie C-2023 EPC', 0)),
        'D/E/F': float(data_gemeente.get('Categorie D-2023 EPC', 0)) + float(
            data_gemeente.get('Categorie E-2023 EPC', 0)) + float(data_gemeente.get('Categorie F-2023 EPC', 0))
    }

    data_series_vlaams = {
        'A/A+': float(data_vlaams.get('Categorie A+-2023 EPC', 0)) + float(data_vlaams.get('Categorie A-2023 EPC', 0)),
        'B': float(data_vlaams.get('Categorie B-2023 EPC', 0)),
        'C': float(data_vlaams.get('Categorie C-2023 EPC', 0)),
        'D/E/F': float(data_vlaams.get('Categorie D-2023 EPC', 0)) + float(
            data_vlaams.get('Categorie E-2023 EPC', 0)) + float(data_vlaams.get('Categorie F-2023 EPC', 0))
    }

    # Maak een nieuwe figuur voor de side-by-side grafiek
    fig = make_subplots(rows=1, cols=2, subplot_titles=(f"EPC-labels in {gemeente}", "EPC-labels in Vlaams Gewest"))

    # Voeg de balkgrafiek toe voor de gemeente
    fig.add_trace(go.Bar(
        x=categorieen,
        y=[data_series_gemeente[cat] for cat in categorieen],
        name=f'EPC in {gemeente}',
        marker_color=kleuren,
        text=[f"{data_series_gemeente[cat]:.1f}%" for cat in categorieen],
        # Voeg de percentages toe als tekstlabels op de balken
        textposition='auto'  # Plaats de tekst automatisch op de juiste plek op de balk
    ), row=1, col=1)

    # Voeg de balkgrafiek toe voor het Vlaamse Gewest
    fig.add_trace(go.Bar(
        x=categorieen,
        y=[data_series_vlaams[cat] for cat in categorieen],
        name='EPC in Vlaams Gewest',
        marker_color=kleuren,
        text=[f"{data_series_vlaams[cat]:.1f}%" for cat in categorieen],
        # Voeg de percentages toe als tekstlabels op de balken
        textposition='auto'  # Plaats de tekst automatisch op de juiste plek op de balk
    ), row=1, col=2)

    # Pas de gestandaardiseerde layout toe
    apply_chart_layout(
        fig,
        f'Verdeling EPC-labels in {gemeente} vs. Vlaams Gewest',
        'Percentage'
    )

    # Zorg ervoor dat de subplots goed uitgelijnd zijn
    fig.update_layout(
        barmode='group',
        showlegend=False  # Verberg de legenda omdat we een aparte titel per subplot hebben
    )

    return pio.to_html(fig, full_html=False, include_plotlyjs='cdn')

def genereer_klimaatimpact_grafiek(data_gemeente, data_vlaams, gemeente):
    # Definieer een vast kleurenschema voor de 4 balken
    kleuren = ['#7fe0de', '#6bc1c3', '#55a6a9', '#418b8f']

    # Haal de benodigde gegevens op voor de gemeente
    hittestress_2030_gemeente = float(data_gemeente["Kwetsbare personen blootgesteld aan hittestress Hoog impact 2030"])
    hittestress_2050_gemeente = float(data_gemeente["Kwetsbare personen blootgesteld aan hittestress Hoog impact 2050"])
    wateroverlast_huidig_gemeente = float(data_gemeente["Aandeel gebouwen met mogelijke wateroverlast in huidig klimaat"])
    wateroverlast_2050_gemeente = float(data_gemeente["Aandeel gebouwen met mogelijke wateroverlast in 2050"])

    # Haal de benodigde gegevens op voor Vlaams Gewest
    hittestress_2030_vlaams = float(data_vlaams["Kwetsbare personen blootgesteld aan hittestress Hoog impact 2030"])
    hittestress_2050_vlaams = float(data_vlaams["Kwetsbare personen blootgesteld aan hittestress Hoog impact 2050"])
    wateroverlast_huidig_vlaams = float(data_vlaams["Aandeel gebouwen met mogelijke wateroverlast in huidig klimaat"])
    wateroverlast_2050_vlaams = float(data_vlaams["Aandeel gebouwen met mogelijke wateroverlast in 2050"])

    # Maak een nieuwe figuur voor de side-by-side grafiek
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=(f"Klimaatimpact in {gemeente}", "Klimaatimpact in Vlaams Gewest")
    )

    # Voeg de balken toe voor de gemeente
    fig.add_trace(go.Bar(
        x=["Hittestress 2030"],
        y=[hittestress_2030_gemeente],
        name='Kwetsbare personen blootgesteld aan hittestress, 2030',
        marker_color=kleuren[0],
        showlegend=True,
        text=[f"{hittestress_2030_gemeente:.0f}%"],  # Voeg labels toe met 0 decimalen
        textposition='auto'
    ), row=1, col=1)

    fig.add_trace(go.Bar(
        x=["Hittestress 2050"],
        y=[hittestress_2050_gemeente],
        name='Kwetsbare personen blootgesteld aan hittestress, 2050',
        marker_color=kleuren[1],
        showlegend=True,
        text=[f"{hittestress_2050_gemeente:.0f}%"],
        textposition='auto'
    ), row=1, col=1)

    fig.add_trace(go.Bar(
        x=["Wateroverlast Huidig"],
        y=[wateroverlast_huidig_gemeente],
        name='Aandeel gebouwen met mogelijke wateroverlast in huidig klimaat',
        marker_color=kleuren[2],
        showlegend=True,
        text=[f"{wateroverlast_huidig_gemeente:.0f}%"],
        textposition='auto'
    ), row=1, col=1)

    fig.add_trace(go.Bar(
        x=["Wateroverlast 2050"],
        y=[wateroverlast_2050_gemeente],
        name='Aandeel gebouwen met mogelijke wateroverlast in 2050',
        marker_color=kleuren[3],
        showlegend=True,
        text=[f"{wateroverlast_2050_gemeente:.0f}%"],
        textposition='auto'
    ), row=1, col=1)

    # Voeg de balken toe voor het Vlaamse Gewest
    fig.add_trace(go.Bar(
        x=["Hittestress 2030"],
        y=[hittestress_2030_vlaams],
        name='Hittestress 2030',
        marker_color=kleuren[0],
        showlegend=False,
        text=[f"{hittestress_2030_vlaams:.0f}%"],
        textposition='auto'
    ), row=1, col=2)

    fig.add_trace(go.Bar(
        x=["Hittestress 2050"],
        y=[hittestress_2050_vlaams],
        name='Hittestress 2050',
        marker_color=kleuren[1],
        showlegend=False,
        text=[f"{hittestress_2050_vlaams:.0f}%"],
        textposition='auto'
    ), row=1, col=2)

    fig.add_trace(go.Bar(
        x=["Wateroverlast Huidig"],
        y=[wateroverlast_huidig_vlaams],
        name='Wateroverlast Huidig',
        marker_color=kleuren[2],
        showlegend=False,
        text=[f"{wateroverlast_huidig_vlaams:.0f}%"],
        textposition='auto'
    ), row=1, col=2)

    fig.add_trace(go.Bar(
        x=["Wateroverlast 2050"],
        y=[wateroverlast_2050_vlaams],
        name='Wateroverlast 2050',
        marker_color=kleuren[3],
        showlegend=False,
        text=[f"{wateroverlast_2050_vlaams:.0f}%"],
        textposition='auto'
    ), row=1, col=2)

    # Pas de layout aan om de achtergrond transparant te maken en de legenda correct weer te geven
    fig.update_layout(
        legend=dict(
            orientation="v",
            xanchor="center",
            x=0.5,
            yanchor="bottom",
            y=-0.4,
            itemclick="toggleothers"
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='LightGray'
        ),
        xaxis=dict(
            showticklabels=False
        ),
        xaxis2=dict(
            showticklabels=False
        ),
        margin=dict(b=100),
        plot_bgcolor='rgba(0,0,0,0)',  # Maakt de achtergrond transparant
        paper_bgcolor='rgba(0,0,0,0)'  # Maakt de volledige figuurachtergrond transparant
    )

    return pio.to_html(fig, full_html=False, include_plotlyjs='cdn')

def genereer_rapport_html(gemeente, gemeente_data, css_content, alle_data):
    # Bereken de vastgoedprijsstijging voor de gemeente
    start_prijs, eind_prijs, stijging = bereken_vastgoedprijs_stijging(gemeente_data)

    # Haal de Vlaamse gewestdata op
    vlaams_data = vind_vlaams_gewest_data(alle_data)
    start_prijs_vlaams, eind_prijs_vlaams, stijging_vlaams = bereken_vastgoedprijs_stijging_vlaams(vlaams_data)

    # Zorg ervoor dat deze berekeningen worden gedaan vóór de HTML rendering
    bevolking_2023, bevolking_2040, groei = bereken_huishoudensgroei(gemeente_data)
    bevolking_2023_vlaams, bevolking_2040_vlaams, groei_vlaams = bereken_huishoudensgroei_vlaams(vlaams_data)

    # Bereken de groei van eenpersoonshuishoudens voor de gemeente en Vlaanderen
    eenpersoonshuishoudens_2023, eenpersoonshuishoudens_2040, groei_eenpersoonshuishoudens = bereken_eenpersoonshuishoudensgroei(gemeente_data)
    eenpersoonshuishoudens_2023_vlaams, eenpersoonshuishoudens_2040_vlaams, groei_eenpersoonshuishoudens_vlaams = bereken_eenpersoonshuishoudensgroei_vlaams(vlaams_data)

    # Bereken de wateroverlast en hittestress stijging voor de gemeente en Vlaanderen
    (hittestress_2030, hittestress_2050, stijging_hittestress,
     wateroverlast_huidig, wateroverlast_2050, stijging_wateroverlast) = bereken_wateroverlast_en_hittestress_stijging(
        gemeente_data)

    (hittestress_2030_vlaams, hittestress_2050_vlaams, stijging_hittestress_vlaams,
     wateroverlast_huidig_vlaams, wateroverlast_2050_vlaams,
     stijging_wateroverlast_vlaams) = bereken_wateroverlast_en_hittestress_stijging_vlaams(vlaams_data)

    # Genereer de grafieken
    vastgoed_grafiek = genereer_vastgoedprijs_grafiek(gemeente, gemeente_data, alle_data)
    huishoudens_grafiek = genereer_huishoudens_grafiek(gemeente, gemeente_data)
    epc_grafiek = genereer_epc_grafiek(gemeente_data, vlaams_data, gemeente)
    klimaatimpact_grafiek = genereer_klimaatimpact_grafiek(gemeente_data, vlaams_data, gemeente)

    # HTML template voor het rapport

    html_template = Template("""
    <!DOCTYPE html>
    <html lang='nl'>
    <head>
        <meta charset='UTF-8'>
        <meta name='viewport' content='width=device-width, initial-scale=1.0'>
        <title>Hoe houden we wonen betaalbaar in {{ gemeente }}?</title>
        <link href="https://fonts.googleapis.com/css2?family=Georama:wght@400;600&display=swap" rel="stylesheet">
        <style>
            {{ css_content }}
        </style>
    </head>
    <body>
        <h1>Hoe houden we wonen betaalbaar in {{ gemeente }}?</h1>
        
<h2>Stijgende huizenprijzen in {{ gemeente }}: blijft het betaalbaar?</h2>
<p>De prijs van een huis in {{ gemeente }} is gestegen van €{{ start_prijs | int }} in 2014 naar €{{ eind_prijs | int }} in 2023, een stijging van {{ stijging | round(0) | int }}%.</p>
<p>Ter vergelijking: in het Vlaams Gewest zijn de vastgoedprijzen in dezelfde periode gestegen van €{{ start_prijs_vlaams | int }} naar €{{ eind_prijs_vlaams | int }}, een stijging van {{ stijging_vlaams | round(0) | int }}%.</p>

{% if stijging > stijging_vlaams %}
<p>In {{ gemeente }} zijn de prijzen sterker gestegen dan het Vlaamse gemiddelde, wat aangeeft dat de lokale markt nog minder toegankelijk wordt, vooral voor jonge gezinnen die voor het eerst een huis willen kopen. Hogere prijzen maken het voor hen steeds moeilijker om betaalbare woonruimte te vinden en een eigen woning te verwerven in uw gemeente.</p>
{% else %}
<p>Hoewel de prijsstijging in {{ gemeente }} lager is dan het Vlaamse gemiddelde, blijven de vastgoedprijzen toenemen. Dit maakt het vinden van betaalbare woningen steeds uitdagender, vooral voor jonge gezinnen die voor het eerst een huis willen kopen.</p>
{% endif %}

{% if eind_prijs > eind_prijs_vlaams %}
<p>Bovendien is de absolute prijs van een huis in {{ gemeente }} in 2023 €{{ (eind_prijs - eind_prijs_vlaams) | int }} hoger dan het Vlaamse gemiddelde, wat de betaalbaarheid van wonen nog verder onder druk zet.</p>
{% endif %}

<p>Schaarse bouwgronden en complexe vergunningsprocedures maken nieuwe projecten duurder, wat de situatie verder bemoeilijkt. De behoefte aan een voldoende woningaanbod in alle segmenten is daarom cruciaal om de druk op zowel de koop- als huurmarkten te verlichten. Het bevorderen van eigenaarschap blijft ook essentieel, aangezien meer eigenaars de druk op de huurmarkt kunnen verminderen. Daarnaast kunnen maatregelen om de doorstroming te bevorderen, zoals het verlagen van de registratierechten voor een tweede aankoop, een positieve impact hebben op de markt.</p>

<p>Een geïntegreerd en samenhangend beleid is nodig om op lange termijn de betaalbaarheid van woningen in uw gemeente te waarborgen. Er moet speciale aandacht zijn voor energie-efficiëntie, aangezien dit niet alleen de energiekosten voor bewoners verlaagt, maar ook de waarde van het vastgoed verhoogt. Verder is het van belang om kwalitatieve leefomgevingen te creëren die bijdragen aan het welzijn van de inwoners. Dit vraagt om een intensieve samenwerking tussen lokale overheden, projectontwikkelaars, en andere belanghebbenden.</p>

<div class="grafiek-container">{{ vastgoed_grafiek | safe }}</div>
<div class="aanbevelingen-sectie">
    <h3>Aanbevelingen vanuit Embuild Vlaanderen</h3>
    <ul class="aanbevelingen-tekst">
        <li>Stimuleer actief kernversterking en verdichting, niet alleen door bouwmogelijkheden te schrappen, maar ook door hogere dichtheden te bevorderen in kernen en goed gelegen gebieden.</li>
        <li>Zet in op efficiëntere processen, bijvoorbeeld door digitalisering, om de doorlooptijd en dus de bouwkosten te verminderen.</li>
    </ul>
</div>
<h2>Steeds meer en kleinere huishoudens</h2>
<p>De bevolking van {{ gemeente }} zal naar verwachting groeien van {{ bevolking_2023 }} huishoudens in 2023 naar {{ bevolking_2040 }} huishoudens in 2040, een toename van {{ groei | round(0) }}%.</p>

{% if groei > groei_vlaams %}
<p>In {{ gemeente }} is de groei van het aantal huishoudens sterker dan het Vlaamse gemiddelde van {{ groei_vlaams | round(0) }}%. Dit kan de druk op de woningmarkt verhogen en de betaalbaarheid van woningen verder onder druk zetten. Vooral de stijging van het aantal eenpersoonshuishoudens, dat naar verwachting ook sneller zal groeien, maakt het nodig om betaalbare, kleinere woningen aan te bieden die aan de behoeften van deze doelgroep voldoen.</p>
{% else %}
<p>Hoewel de groei van het aantal huishoudens in {{ gemeente }} lager is dan het Vlaamse gemiddelde van {{ groei_vlaams | round(0) }}%, blijft de vraag naar woningen stijgen. Zelfs bij een iets lagere groei betekent dit dat er meer woningen nodig zijn om aan de vraag te voldoen. Vooral de toenemende vraag naar woningen voor kleinere huishoudens, zoals eenpersoonshuishoudens, moet worden aangepakt om de markt in balans te houden.</p>
{% endif %}

<p>Daarnaast groeit het aantal eenpersoonshuishoudens in {{ gemeente }} naar verwachting van {{ eenpersoonshuishoudens_2023 }} in 2023 naar {{ eenpersoonshuishoudens_2040 }} in 2040, een stijging van {{ groei_eenpersoonshuishoudens | round(0) }}%. {% if groei_eenpersoonshuishoudens > groei_eenpersoonshuishoudens_vlaams %} Deze groei ligt boven het Vlaamse gemiddelde van {{ groei_eenpersoonshuishoudens_vlaams | round(0) }}%, wat aangeeft dat er meer vraag zal zijn naar kleinere, betaalbare woningen in uw gemeente. {% else %} Hoewel deze groei iets lager is dan het Vlaamse gemiddelde van {{ groei_eenpersoonshuishoudens_vlaams | round(0) }}%, blijft het aandeel eenpersoonshuishoudens stijgen, wat de noodzaak benadrukt om voldoende kleine en betaalbare woningen te ontwikkelen. {% endif %}</p>

<p>De gezinsverdunning, oftewel de afname van de gemiddelde gezinsgrootte, heeft belangrijke implicaties voor de betaalbaarheid van wonen in uw gemeente. Een toename van eenpersoonshuishoudens betekent dat meer mensen alleen een woning moeten kunnen betalen, wat de vraag naar kleinere, betaalbare woningen vergroot. Bovendien kan de verdunning leiden tot meer vraag naar sociale huisvesting en aangepaste woonvormen, zoals studio's, appartementen en co-housing. Dit vereist een diverse woningmarkt die aan de verschillende behoeften van bewoners voldoet.</p>

<p>Gezinsverdunning betekent ook dat nieuwe projecten rekening moeten houden met meer diversiteit in woonvormen en -typen. Investeringen in de bouw van kleinere woningen en het herbestemmen van bestaande panden kunnen helpen om de betaalbaarheid van wonen te waarborgen. De behoefte aan een voldoende woningaanbod in alle segmenten blijft dus cruciaal om de druk op zowel de koop- als huurmarkten te verlichten.</p>

<div class="grafiek-container">
    {{ huishoudens_grafiek | safe }}
</div>
<div class="aanbevelingen-sectie">
    <h3>Aanbevelingen vanuit Embuild Vlaanderen</h3>
    <ul class="aanbevelingen-tekst">
        <li>Overweeg versoepeling om meer flexibiliteit toe te laten, zoals het toestaan van meergezinswoningen of kangoeroewoningen in bepaalde zones.</li>
        <li>Eigen gebouwen kunnen dienen als uithangbord voor duurzame praktijken, bijvoorbeeld door energieprestaties te verbeteren met behulp van een EnergiePrestatieContract.</li>
        <li>Door de oprichting van publieke-private partnerschappen (PPP's) kunnen gemeenten samenwerken met de private sector en burgers om grootschalige duurzaamheidsprojecten te ontwikkelen en te financieren.</li>
    </ul>
</div>



        <h2>EPC-labels in {{ gemeente }}</h2>
        <p>Hieronder ziet u de verdeling van EPC-labels voor bestaande woningen in {{ gemeente }} vergeleken met het Vlaamse Gewest.</p>
        <div class="grafiek-container">{{ epc_grafiek | safe }}</div>
        <div class="aanbevelingen-sectie">
    <h3>Aanbevelingen vanuit Embuild Vlaanderen</h3>
    <ul class="aanbevelingen-tekst">
        <li>Door het aankoopbeleid te richten op duurzame producten en diensten kunnen nieuwe, duurzame oplossingen worden gestimuleerd .</li>
        <li>Help burgers om zelf ook te investeren door in te zetten op burgerparticipatie, energiecoöperaties of door mobiele energiehuizen in te zetten die advies geven over duurzame praktijken.</li>
        <li>Pas infrastructuur aan voor fietsen en lopen, openbaar vervoer te verbeteren en het gebruik van elektrische voertuigen te ondersteunen door voldoende laadpalen te installeren.</li>
    </ul>
</div>

<h2>Klimaatimpact in {{ gemeente }}</h2>
<p>De onderstaande grafiek toont de vergelijking van klimaatimpact variabelen tussen {{ gemeente }} en het Vlaamse Gewest.</p>
<div class="grafiek-container">{{ klimaatimpact_grafiek | safe }}</div>

<h2>Klimaatimpact in {{ gemeente }}: risico's en kansen</h2>
<p>Het aantal kwetsbare personen blootgesteld aan hittestress in {{ gemeente }} stijgt van {{ hittestress_2030 | round(0) | int }}% in 2030 naar {{ hittestress_2050 | round(0) | int }}% in 2050, een toename van {{ stijging_hittestress | round(0) | int }}%.</p>
<p>Ter vergelijking, in het Vlaams Gewest stijgt het aantal kwetsbare personen blootgesteld aan hittestress van {{ hittestress_2030_vlaams | round(0) | int }}% naar {{ hittestress_2050_vlaams | round(0) | int }}%, een toename van {{ stijging_hittestress_vlaams | round(0) | int }}%.</p>

<p>Het aandeel gebouwen met mogelijke wateroverlast in {{ gemeente }} neemt toe van {{ wateroverlast_huidig | round(0) | int }}% in het huidige klimaat naar {{ wateroverlast_2050 | round(0) | int }}% in 2050, een stijging van {{ stijging_wateroverlast | round(0) | int }}%.</p>
<p>In het Vlaams Gewest zien we een toename van {{ wateroverlast_huidig_vlaams | round(0) | int }}% naar {{ wateroverlast_2050_vlaams | round(0) | int }}%, een stijging van {{ stijging_wateroverlast_vlaams | round(0) | int }}%.</p>

{% if stijging_hittestress > stijging_hittestress_vlaams or stijging_wateroverlast > stijging_wateroverlast_vlaams %}
<p>De klimaatimpact in {{ gemeente }} lijkt groter dan het Vlaamse gemiddelde, wat wijst op een grotere kwetsbaarheid voor zowel hittestress als wateroverlast. Het is daarom belangrijk dat er lokaal wordt ingezet op klimaatadaptieve maatregelen.</p>
{% else %}
<p>Hoewel de toename in {{ gemeente }} lager is dan het Vlaamse gemiddelde, blijft de stijging van hittestress en wateroverlast zorgwekkend. Lokale aanpassingen kunnen helpen de risico's te beheersen.</p>
{% endif %}

<p>De bouwsector kan een belangrijke partner zijn in het verminderen van klimaatimpact door duurzame bouwpraktijken te promoten, zoals groene daken, permeabele bestrating en energiebesparende maatregelen.</p>

<div class="grafiek-container">{{ overstromingsrisico_grafiek | safe }}</div>

            <div class="aanbevelingen-sectie">
            <h3>Aanbevelingen vanuit Embuild Vlaanderen</h3>
    <ul class="aanbevelingen-tekst">
        <li>Investeer in infrastructuur die bestand is tegen extreme weersomstandigheden zoals hittegolven, overstromingen en droogte, bijvoorbeeld door groene daken, permeabele bestrating en regenwateropvangsystemen te implementeren.</li>
        <li>De integratie van klimaatmaatregelen in andere beleidsdomeinen zoals gezondheid, huisvesting en economische ontwikkeling, kan de effectiviteit versterken.</li>
    </ul>
</div>

        <!-- Voeg hier meer secties en grafieken toe voor andere analyses -->
    <footer>
        <div class="logo-container">
            <div class="donut"></div>
            <div class="logo-text">
                Vlaamse Woonbalans
                <span class="sub-text">Gemeenterapport {{gemeente}}</span>
            </div>
        </div>
    </footer>
</body>
</html>
""")

    # Genereer de HTML-inhoud
    html_content = html_template.render(
        gemeente=gemeente,
        start_prijs=start_prijs,
        eind_prijs=eind_prijs,
        stijging=stijging,
        start_prijs_vlaams=start_prijs_vlaams,
        eind_prijs_vlaams=eind_prijs_vlaams,
        stijging_vlaams=stijging_vlaams,
        vastgoed_grafiek=vastgoed_grafiek,
        bevolking_2023=bevolking_2023,
        bevolking_2040=bevolking_2040,
        groei=groei,
        groei_vlaams=groei_vlaams,
        eenpersoonshuishoudens_2023=eenpersoonshuishoudens_2023,
        eenpersoonshuishoudens_2040=eenpersoonshuishoudens_2040,
        groei_eenpersoonshuishoudens=groei_eenpersoonshuishoudens,
        groei_eenpersoonshuishoudens_vlaams=groei_eenpersoonshuishoudens_vlaams,
        huishoudens_grafiek=huishoudens_grafiek,
        klimaatimpact_grafiek=klimaatimpact_grafiek,
        hittestress_2030=hittestress_2030,
        hittestress_2050=hittestress_2050,
        stijging_hittestress=stijging_hittestress,
        wateroverlast_huidig=wateroverlast_huidig,
        wateroverlast_2050=wateroverlast_2050,
        stijging_wateroverlast=stijging_wateroverlast,
        hittestress_2030_vlaams=hittestress_2030_vlaams,
        hittestress_2050_vlaams=hittestress_2050_vlaams,
        stijging_hittestress_vlaams=stijging_hittestress_vlaams,
        wateroverlast_huidig_vlaams=wateroverlast_huidig_vlaams,
        wateroverlast_2050_vlaams=wateroverlast_2050_vlaams,
        stijging_wateroverlast_vlaams=stijging_wateroverlast_vlaams,
        epc_grafiek=epc_grafiek,
        css_content=css_content
    )

    return html_content


def main():
    # Genereer het kleurenschema
    kleuren = genereer_kleurenschema()

    # Genereer de CSS-content
    css_content = genereer_css(kleuren)

    # Maak rapporten enkel voor de eerste twee gemeenten (exclusief "Vlaams Gewest")
    gemeenten_verwerkt = 0

    for gemeente_data in data:
        gemeente = gemeente_data["Gemeente"]
        if gemeente == "Vlaams Gewest":
            continue  # Sla de algemene Vlaamse gegevens over

        if gemeenten_verwerkt >= 2:
            break  # Stop na de eerste twee gemeenten

        # Genereer het rapport met de CSS-content
        html_content = genereer_rapport_html(gemeente, gemeente_data, css_content, data)

        # Sla het rapport op
        output_path = f'report_{gemeente}.html'
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"Rapport voor {gemeente} opgeslagen in {output_path}")
        gemeenten_verwerkt += 1


if __name__ == "__main__":
    main()

