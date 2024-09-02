import matplotlib.colors as mcolors

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

def static(filename):
    return f'/static/{filename}'



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
