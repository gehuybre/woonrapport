import json
import os
import shutil
from jinja2 import Environment, FileSystemLoader

# Import functions from separate files
from graph_generators import (
    genereer_vastgoedprijs_grafiek,
    genereer_huishoudens_grafiek,
    genereer_epc_grafiek,
    genereer_klimaatimpact_grafiek
)
from data_processors import (
    vind_vlaams_gewest_data,
    bereken_vastgoedprijs_stijging,
    bereken_vastgoedprijs_stijging_vlaams,
    bereken_huishoudensgroei,
    bereken_huishoudensgroei_vlaams,
    bereken_eenpersoonshuishoudensgroei,
    bereken_eenpersoonshuishoudensgroei_vlaams,
    bereken_wateroverlast_en_hittestress_stijging,
    bereken_wateroverlast_en_hittestress_stijging_vlaams
)
from utils import genereer_kleurenschema, static

# Set up base directory and template directory
base_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(base_dir, 'templates')

# Set up Jinja2 environment
env = Environment(loader=FileSystemLoader(template_dir))
env.globals['static'] = static

def genereer_rapport_html(gemeente, gemeente_data, alle_data):
    # Genereer het kleurenschema
    kleuren = genereer_kleurenschema()

    # Haal de Vlaamse gewestdata op
    vlaams_data = vind_vlaams_gewest_data(alle_data)

    # Bereken vastgoedprijzen
    start_prijs, eind_prijs, stijging = bereken_vastgoedprijs_stijging(gemeente_data)
    start_prijs_vlaams, eind_prijs_vlaams, stijging_vlaams = bereken_vastgoedprijs_stijging_vlaams(vlaams_data)

    # Bereken huishoudensgroei
    bevolking_2023, bevolking_2040, groei = bereken_huishoudensgroei(gemeente_data)
    bevolking_2023_vlaams, bevolking_2040_vlaams, groei_vlaams = bereken_huishoudensgroei_vlaams(vlaams_data)

    # Bereken eenpersoonshuishoudensgroei
    eenpersoonshuishoudens_2023, eenpersoonshuishoudens_2040, groei_eenpersoonshuishoudens = bereken_eenpersoonshuishoudensgroei(gemeente_data)
    eenpersoonshuishoudens_2023_vlaams, eenpersoonshuishoudens_2040_vlaams, groei_eenpersoonshuishoudens_vlaams = bereken_eenpersoonshuishoudensgroei_vlaams(vlaams_data)

    # Bereken klimaatimpact
    hittestress_2030, hittestress_2050, stijging_hittestress, wateroverlast_huidig, wateroverlast_2050, stijging_wateroverlast = bereken_wateroverlast_en_hittestress_stijging(gemeente_data)
    hittestress_2030_vlaams, hittestress_2050_vlaams, stijging_hittestress_vlaams, wateroverlast_huidig_vlaams, wateroverlast_2050_vlaams, stijging_wateroverlast_vlaams = bereken_wateroverlast_en_hittestress_stijging_vlaams(vlaams_data)

    # Genereer de grafieken
    vastgoed_grafiek = genereer_vastgoedprijs_grafiek(gemeente, gemeente_data, alle_data)
    huishoudens_grafiek = genereer_huishoudens_grafiek(gemeente, gemeente_data)
    epc_grafiek = genereer_epc_grafiek(gemeente_data, vlaams_data, gemeente)
    klimaatimpact_grafiek = genereer_klimaatimpact_grafiek(gemeente_data, vlaams_data, gemeente)

    # Load and render the template
    template = env.get_template('rapport_template.html')
    html_content = template.render(
        gemeente=gemeente,
        kleuren=kleuren,
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
        epc_grafiek=epc_grafiek
    )
    return html_content

def main():
    # Load data
    with open('data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Define output directory
    output_dir = 'output'
    os.makedirs(output_dir, exist_ok=True)

    # Generate reports for the first two municipalities (excluding "Vlaams Gewest")
    gemeenten_verwerkt = 0

    for gemeente_data in data:
        gemeente = gemeente_data["Gemeente"]
        if gemeente == "Vlaams Gewest":
            continue

        if gemeenten_verwerkt >= 3:
            break

        # Generate the report
        html_content = genereer_rapport_html(gemeente, gemeente_data, data)

        if html_content is None:
            print(f"Failed to generate report for {gemeente}. Skipping...")
            continue

        # Save the report in the 'output' directory
        output_path = os.path.join(output_dir, f'report_{gemeente}.html')
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        # Copy static files to the output directory
        static_output_dir = os.path.join(output_dir, 'static')
        os.makedirs(static_output_dir, exist_ok=True)

        # Copy CSS files
        css_dir = os.path.join(base_dir, 'css')
        css_output_dir = os.path.join(static_output_dir, 'css')
        os.makedirs(css_output_dir, exist_ok=True)
        for css_file in os.listdir(css_dir):
            shutil.copy(os.path.join(css_dir, css_file), css_output_dir)

        # Copy JS files
        js_dir = os.path.join(base_dir, 'js')
        js_output_dir = os.path.join(static_output_dir, 'js')
        os.makedirs(js_output_dir, exist_ok=True)
        for js_file in os.listdir(js_dir):
            shutil.copy(os.path.join(js_dir, js_file), js_output_dir)

        # Copy gemeentegrenzen2.json
        shutil.copy('gemeentegrenzen2.json', output_dir)

        print(f"Report for {gemeente} saved in {output_path}")
        gemeenten_verwerkt += 1

    print("Script execution completed.")

if __name__ == "__main__":
    main()