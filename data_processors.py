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


