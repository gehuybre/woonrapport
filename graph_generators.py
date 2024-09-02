import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.io as pio
from utils import genereer_kleurenschema, apply_chart_layout
from data_processors import vind_vlaams_gewest_data

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

