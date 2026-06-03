def _coords(_seed):
    return {
        "ascension_recta": round((_seed * 137.507764) % 360, 3),
        "declinacion": round(((_seed * 73.13579) % 180) - 90, 3),
    }


def _habitabilidad(_indice, _base):
    _valor = _base + ((_indice % 13) - 6) * 0.025
    if _valor < 0:
        return 0.0
    if _valor > 1:
        return 1.0
    return round(_valor, 3)


def _objeto(_nombre, _tipo_objeto, _descripcion, _seed, _propiedades_fisicas, _etiquetas):
    return {
        "nombre": _nombre,
        "tipo_objeto": _tipo_objeto,
        "descripcion": _descripcion,
        "coordenadas": _coords(_seed),
        "propiedades_fisicas": _propiedades_fisicas,
        "etiquetas": _etiquetas,
    }


_estrellas = [
    "Sol", "Sirius", "Canopus", "Rigil Kentaurus", "Toliman", "Proxima Centauri",
    "Arcturus", "Vega", "Capella", "Rigel", "Procyon", "Achernar", "Betelgeuse",
    "Hadar", "Altair", "Acrux", "Aldebaran", "Antares", "Spica", "Pollux",
    "Fomalhaut", "Deneb", "Mimosa", "Regulus", "Adhara", "Shaula", "Castor",
    "Gacrux", "Bellatrix", "Elnath", "Miaplacidus", "Alnilam", "Alnair",
    "Alioth", "Alnitak", "Dubhe", "Mirfak", "Wezen", "Sargas",
    "Kaus Australis", "Avior", "Alkaid", "Menkalinan", "Atria", "Alhena",
    "Peacock", "Alsephina", "Mirzam", "Alphard", "Polaris", "Hamal", "Diphda",
    "Denebola", "Menkent", "Algol", "Kochab", "Almach", "Mizar", "Ras Alhague",
    "Saiph", "Scheat", "Alphecca", "Aludra", "Schedar", "Markab", "Caph",
    "Izar", "Merak", "Enif", "Mirach", "Gienah", "Alcyone", "Maia", "Electra",
    "Merope", "Taygeta", "Pleione", "Celaeno", "61 Cygni", "Barnard Star"
]

_planetas = [
    "Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune",
    "Ceres", "Pluto", "Haumea", "Makemake", "Eris", "Quaoar", "Sedna", "Orcus",
    "Gonggong", "Salacia", "Varda", "Varuna", "Ixion", "Chaos", "Huya",
    "Deucalion", "Altjira", "Albion", "Arrokoth", "Hygiea", "Pallas", "Vesta",
    "Juno", "Euphrosyne", "Interamnia", "Davida", "Herculina", "Eunomia",
    "Cybele", "Sylvia", "Camilla", "Bamberga", "Patientia", "Psyche", "Lutetia",
    "Mathilde", "Eros", "Ida", "Gaspra", "Itokawa", "Bennu", "Ryugu", "Apophis",
    "Kleopatra", "Minerva", "Hermione", "Antiope", "Kalliope", "Eugenia",
    "Themis", "Fortuna", "Astraea", "Hebe", "Iris", "Flora", "Parthenope",
    "Victoria", "Massalia", "Melpomene", "Amphitrite", "Nysa", "Daphne", "Egeria",
    "Hesperia", "Thisbe", "Elektra", "Lamberta", "Juewa", "Eos", "Doris",
    "Lachesis", "Klotho"
]

_lunas = [
    "Phobos", "Deimos", "Io", "Europa", "Ganymede", "Callisto", "Amalthea",
    "Himalia", "Elara", "Pasiphae", "Sinope", "Lysithea", "Carme", "Ananke",
    "Leda", "Thebe", "Adrastea", "Metis", "Callirrhoe", "Themisto", "Megaclite",
    "Taygete", "Chaldene", "Harpalyke", "Kalyke", "Iocaste", "Erinome",
    "Isonoe", "Praxidike", "Autonoe", "Thyone", "Hermippe", "Aitne", "Eurydome",
    "Euanthe", "Euporie", "Orthosie", "Sponde", "Kale", "Pasithee", "Hegemone",
    "Mneme", "Aoede", "Thelxinoe", "Arche", "Kallichore", "Helike", "Carpo",
    "Eukelade", "Cyllene", "Kore", "Herse", "Dia", "Mimas", "Enceladus",
    "Tethys", "Dione", "Rhea", "Titan", "Hyperion", "Iapetus", "Phoebe",
    "Janus", "Epimetheus", "Helene", "Telesto", "Calypso", "Prometheus",
    "Pandora", "Pan", "Ymir", "Paaliaq", "Tarvos", "Ijiraq", "Suttungr",
    "Kiviuq", "Mundilfari", "Albiorix", "Skathi", "Erriapus", "Siarnaq",
    "Thrymr", "Narvi", "Methone", "Pallene", "Polydeuces", "Daphnis", "Aegir",
    "Bebhionn", "Bergelmir", "Bestla", "Farbauti", "Fenrir", "Fornjot", "Hati",
    "Hyrokkin", "Kari", "Loge", "Skoll", "Surtur", "Anthe", "Jarnsaxa", "Greip",
    "Tarqeq", "Aegaeon", "Ariel", "Umbriel", "Titania", "Oberon", "Miranda",
    "Cordelia", "Ophelia", "Bianca", "Cressida", "Desdemona", "Juliet",
    "Portia", "Rosalind", "Cupid", "Belinda", "Perdita", "Puck", "Mab",
    "Francisco", "Caliban", "Stephano", "Trinculo", "Sycorax", "Margaret",
    "Prospero", "Setebos", "Ferdinand", "Triton", "Nereid", "Naiad", "Thalassa",
    "Despina", "Galatea", "Larissa", "Proteus", "Halimede", "Psamathe", "Sao",
    "Laomedeia", "Neso", "Hippocamp", "Charon", "Nix", "Hydra", "Kerberos",
    "Styx", "Hiiaka", "Namaka", "Dysnomia", "Vanth", "Weywot", "S/2003 J 2",
    "S/2003 J 3", "S/2003 J 4", "S/2003 J 5", "S/2003 J 9", "S/2003 J 10",
    "S/2003 J 12", "S/2003 J 15", "S/2003 J 16", "S/2003 J 18", "S/2003 J 19",
    "S/2003 J 23", "S/2004 S 7", "S/2004 S 12", "S/2004 S 13", "S/2004 S 17",
    "S/2004 S 20", "S/2004 S 21", "S/2004 S 22", "S/2004 S 23",
    "S/2004 S 24", "S/2004 S 25", "S/2004 S 26", "S/2004 S 27"
]

_exoplanetas = [
    "51 Pegasi b", "HD 209458 b", "HD 189733 b", "Proxima Centauri b",
    "Proxima Centauri d", "Barnard b", "TRAPPIST-1 b", "TRAPPIST-1 c",
    "TRAPPIST-1 d", "TRAPPIST-1 e", "TRAPPIST-1 f", "TRAPPIST-1 g",
    "TRAPPIST-1 h", "LHS 1140 b", "LHS 1140 c", "GJ 1214 b", "GJ 436 b",
    "GJ 357 b", "GJ 357 c", "GJ 357 d", "GJ 667 Cc", "Gliese 581 c",
    "Gliese 581 d", "Gliese 581 e", "Gliese 581 g", "Gliese 876 b",
    "Gliese 876 c", "Gliese 876 d", "Gliese 876 e", "55 Cancri b",
    "55 Cancri c", "55 Cancri d", "55 Cancri e", "55 Cancri f",
    "Upsilon Andromedae b", "Upsilon Andromedae c", "Upsilon Andromedae d",
    "WASP-12 b", "WASP-17 b", "WASP-18 b", "WASP-19 b", "WASP-43 b",
    "WASP-69 b", "WASP-76 b", "WASP-96 b", "WASP-107 b", "WASP-121 b",
    "WASP-127 b", "KELT-9 b", "KELT-11 b", "HAT-P-1 b", "HAT-P-2 b",
    "HAT-P-7 b", "HAT-P-11 b", "HAT-P-26 b", "HD 40307 b", "HD 40307 c",
    "HD 40307 d", "HD 40307 e", "HD 40307 f", "HD 40307 g", "HD 69830 b",
    "HD 69830 c", "HD 69830 d", "HD 85512 b", "HD 97658 b", "HD 106906 b",
    "Beta Pictoris b", "Beta Pictoris c", "HR 8799 b", "HR 8799 c",
    "HR 8799 d", "HR 8799 e", "PDS 70 b", "PDS 70 c", "AU Microscopii b",
    "AU Microscopii c", "TOI-700 b", "TOI-700 c", "TOI-700 d", "TOI-700 e",
    "TOI-1452 b", "TOI-178 b", "TOI-178 c", "TOI-178 d", "TOI-178 e",
    "TOI-178 f", "TOI-178 g", "TOI-1231 b", "TOI-270 b", "TOI-270 c",
    "TOI-270 d", "K2-18 b", "K2-141 b", "K2-33 b", "K2-3 b", "K2-3 c",
    "K2-3 d", "K2-72 e"
] + [f"Kepler-{_i} b" for _i in range(1, 202)]

_galaxias = [
    "Andromeda Galaxy", "Triangulum Galaxy", "Large Magellanic Cloud",
    "Small Magellanic Cloud", "Sombrero Galaxy", "Whirlpool Galaxy",
    "Pinwheel Galaxy", "Bode Galaxy", "Cigar Galaxy", "Black Eye Galaxy",
    "Sunflower Galaxy", "Sculptor Galaxy", "Cartwheel Galaxy", "Antennae Galaxies",
    "Tadpole Galaxy", "Hoag Object", "Centaurus A", "Maffei 1", "Maffei 2",
    "Barnard Galaxy", "Wolf-Lundmark-Melotte", "Leo I", "Leo II", "Draco Dwarf",
    "Ursa Minor Dwarf", "Sculptor Dwarf", "Fornax Dwarf", "Carina Dwarf",
    "Sextans Dwarf", "Phoenix Dwarf", "Pegasus Dwarf", "Tucana Dwarf",
    "Sagittarius Dwarf Spheroidal", "Canis Major Dwarf", "Pisces Dwarf",
    "Bootes I", "Bootes II", "Coma Berenices Dwarf", "Hercules Dwarf",
    "Leo T", "Segue 1", "Segue 2", "Ursa Major I", "Ursa Major II",
    "Willman 1", "Reticulum II", "Hydrus I", "Tucana II", "Eridanus II",
    "Crater II", "Messier 31", "Messier 32", "Messier 33", "Messier 49",
    "Messier 51", "Messier 58", "Messier 59", "Messier 60", "Messier 61",
    "Messier 63", "Messier 64", "Messier 65", "Messier 66", "Messier 74",
    "Messier 77", "Messier 81", "Messier 82", "Messier 83", "Messier 84",
    "Messier 85", "Messier 86", "Messier 87", "Messier 88", "Messier 89",
    "Messier 90", "Messier 91", "Messier 94", "Messier 95", "Messier 96",
    "Messier 98", "Messier 99", "Messier 100", "Messier 101", "Messier 102",
    "Messier 104", "Messier 105", "Messier 106", "Messier 108", "Messier 109",
    "Messier 110", "NGC 1", "NGC 2", "NGC 16", "NGC 24", "NGC 45", "NGC 55",
    "NGC 95", "NGC 128", "NGC 130", "NGC 147", "NGC 185", "NGC 205",
    "NGC 224", "NGC 247", "NGC 253", "NGC 278", "NGC 300", "NGC 404",
    "NGC 520", "NGC 598", "NGC 613", "NGC 628", "NGC 660", "NGC 772",
    "NGC 891", "NGC 925", "NGC 936", "NGC 1023", "NGC 1055", "NGC 1068",
    "NGC 1097", "NGC 1232", "NGC 1291", "NGC 1300", "NGC 1313", "NGC 1316",
    "NGC 1365", "NGC 1399", "NGC 1404", "NGC 1512", "NGC 1532", "NGC 1566",
    "NGC 1672", "NGC 1705", "NGC 1792", "NGC 1808", "NGC 2146", "NGC 2207",
    "NGC 2403", "NGC 2442", "NGC 2683", "NGC 2775", "NGC 2841", "NGC 2903",
    "NGC 2976", "NGC 3031", "NGC 3034", "NGC 3077", "NGC 3115", "NGC 3184",
    "NGC 3190", "NGC 3198", "NGC 3227", "NGC 3310", "NGC 3351", "NGC 3368",
    "NGC 3370", "NGC 3377", "NGC 3379", "NGC 3384", "NGC 3486", "NGC 3521",
    "NGC 3556", "NGC 3623", "NGC 3627", "NGC 3628", "NGC 4038", "NGC 4039",
    "NGC 4214", "NGC 4236", "NGC 4244", "NGC 4254", "NGC 4258", "NGC 4303",
    "NGC 4314", "NGC 4321", "NGC 4388", "NGC 4395", "NGC 4402", "NGC 4414"
]

_nebulosas = [
    "Orion Nebula", "Horsehead Nebula", "Eagle Nebula", "Lagoon Nebula",
    "Trifid Nebula", "Dumbbell Nebula", "Ring Nebula", "Helix Nebula",
    "Crab Nebula", "Rosette Nebula", "Carina Nebula", "Tarantula Nebula",
    "Veil Nebula", "North America Nebula", "Pelican Nebula", "California Nebula",
    "Cocoon Nebula", "Cone Nebula", "Flame Nebula", "Witch Head Nebula",
    "Medusa Nebula", "Owl Nebula", "Cat's Eye Nebula", "Little Dumbbell Nebula",
    "Saturn Nebula", "Eskimo Nebula", "Red Rectangle Nebula", "Blue Snowball Nebula",
    "Butterfly Nebula", "Ant Nebula", "Retina Nebula", "Stingray Nebula",
    "Ghost of Jupiter Nebula", "Eight-Burst Nebula", "Omega Nebula", "Pacman Nebula",
    "Soul Nebula", "Heart Nebula", "Monkey Head Nebula", "Seagull Nebula",
    "Crescent Nebula", "Bubble Nebula", "Skull Nebula", "Boomerang Nebula",
    "Homunculus Nebula", "Pencil Nebula", "Running Man Nebula", "Thor's Helmet Nebula",
    "Elephant Trunk Nebula", "Iris Nebula", "Wizard Nebula", "Tulip Nebula",
    "Cave Nebula", "Jellyfish Nebula", "Crab Pulsar Wind Nebula", "Little Ghost Nebula",
    "Red Spider Nebula", "Bug Nebula", "Southern Crab Nebula", "Frosty Leo Nebula",
    "NGC 1952", "NGC 1976", "NGC 2024", "NGC 2023", "NGC 2070", "NGC 2174",
    "NGC 2237", "NGC 2244", "NGC 2264", "NGC 2392", "NGC 2440", "NGC 2818",
    "NGC 3132", "NGC 3242", "NGC 3372", "NGC 3587", "NGC 3918", "NGC 5189",
    "NGC 5307", "NGC 5882", "NGC 604", "NGC 6302", "NGC 6334", "NGC 6357",
    "NGC 6543", "NGC 6572", "NGC 6720", "NGC 6751", "NGC 6826", "NGC 6888",
    "NGC 6960", "NGC 6992", "NGC 7000", "NGC 7009", "NGC 7023", "NGC 7293",
    "NGC 7635", "NGC 7662", "IC 405", "IC 410", "IC 417", "IC 434", "IC 4406",
    "IC 4592", "IC 4628", "IC 4703", "IC 5070", "IC 5146", "Barnard 33",
    "Sh2-101", "Sh2-112", "Sh2-132", "Sh2-155", "Sh2-170", "Sh2-171",
    "Sh2-188", "Sh2-240", "Sh2-261", "Sh2-264", "Sh2-276"
]

_sistemas_estelares = [
    "Alpha Centauri System", "Sirius System", "Procyon System", "Luhman 16 System",
    "61 Cygni System", "Kruger 60 System", "Groombridge 34 System",
    "Epsilon Eridani System", "Tau Ceti System", "TRAPPIST-1 System",
    "Kepler-90 System", "Kepler-11 System", "55 Cancri System",
    "Upsilon Andromedae System", "Gliese 667 System", "Gliese 876 System",
    "HD 10180 System", "HR 8799 System", "Beta Pictoris System", "Fomalhaut System",
    "Vega System", "Castor System", "Mizar-Alcor System", "Algol System",
    "Capella System", "Polaris System", "Antares System", "Acrux System",
    "Albireo System", "Gamma Leonis System", "70 Ophiuchi System",
    "Xi Ursae Majoris System", "Mu Cassiopeiae System", "Delta Trianguli System",
    "Zeta Reticuli System", "36 Ophiuchi System", "Eta Cassiopeiae System",
    "Epsilon Indi System", "WISE 1049-5319 System", "Ross 614 System",
    "Wolf 424 System", "Wolf 1061 System", "HD 219134 System", "Gliese 581 System",
    "Gliese 832 System", "YZ Ceti System", "Teegarden Star System",
    "Kapteyn Star System", "Lalande 21185 System", "Ross 128 System",
    "Barnard Star System", "Luyten Star System", "HD 40307 System",
    "HD 69830 System", "HD 189733 System", "HD 209458 System", "TOI-700 System",
    "TOI-178 System", "K2-18 System", "PDS 70 System"
]

OBJETOS_CELESTES_INICIALES = []

for _i, _nombre in enumerate(_estrellas):
    _distancia = 0.000016 if _nombre == "Sol" else round(4.2 + ((_i * 23.7) % 1800), 3)
    OBJETOS_CELESTES_INICIALES.append(
        _objeto(
            _nombre,
            "estrella",
            f"Estrella conocida y registrada en catalogos astronomicos: {_nombre}.",
            1000 + _i,
            {
                "distancia_anios_luz": _distancia,
                "masa_tierra": round(333000 * (0.1 + ((_i * 7) % 250) / 25), 3),
                "radio_tierra": round(109 * (0.15 + ((_i * 5) % 80) / 20), 3),
                "temperatura_kelvin": 2600 + ((_i * 173) % 28000),
            },
            ["estrella", "catalogo_estelar", "objeto_real"],
        )
    )

for _i, _nombre in enumerate(_planetas):
    OBJETOS_CELESTES_INICIALES.append(
        _objeto(
            _nombre,
            "planeta",
            f"Planeta, planeta enano o planeta menor del sistema solar catalogado como {_nombre}.",
            2000 + _i,
            {
                "distancia_anios_luz": round(0.000004 + ((_i + 1) * 0.0000021), 9),
                "masa_tierra": round(0.000001 + ((_i * 0.137) % 318), 6),
                "radio_tierra": round(0.02 + ((_i * 0.031) % 11.2), 6),
                "temperatura_kelvin": 35 + ((_i * 17) % 720),
                "periodo_orbital_dias": round(88 + ((_i * 41.7) % 90560), 3),
                "indice_habitabilidad": _habitabilidad(_i, 0.98 if _nombre == "Earth" else 0.28),
            },
            ["sistema_solar", "planeta", "planeta_enano_o_menor"],
        )
    )

for _i, _nombre in enumerate(_lunas):
    OBJETOS_CELESTES_INICIALES.append(
        _objeto(
            _nombre,
            "luna",
            f"Luna natural conocida dentro del sistema solar: {_nombre}.",
            3000 + _i,
            {
                "distancia_anios_luz": round(0.00000004 + ((_i + 1) * 0.00000032), 9),
                "masa_tierra": round(0.0000001 + ((_i * 0.00019) % 0.025), 8),
                "radio_tierra": round(0.002 + ((_i * 0.011) % 0.42), 6),
                "temperatura_kelvin": 35 + ((_i * 9) % 260),
                "periodo_orbital_dias": round(0.3 + ((_i * 1.73) % 550), 3),
                "indice_habitabilidad": _habitabilidad(_i, 0.18),
            },
            ["sistema_solar", "luna", "satelite_natural"],
        )
    )

for _i, _nombre in enumerate(_exoplanetas):
    OBJETOS_CELESTES_INICIALES.append(
        _objeto(
            _nombre,
            "exoplaneta",
            f"Exoplaneta confirmado o ampliamente catalogado fuera del sistema solar: {_nombre}.",
            4000 + _i,
            {
                "distancia_anios_luz": round(4.2 + ((_i * 31.4) % 5200), 3),
                "masa_tierra": round(0.3 + ((_i * 2.17) % 4200), 6),
                "radio_tierra": round(0.45 + ((_i * 0.19) % 22), 6),
                "temperatura_kelvin": 80 + ((_i * 37) % 2500),
                "periodo_orbital_dias": round(0.5 + ((_i * 3.91) % 4200), 3),
                "indice_habitabilidad": _habitabilidad(_i, 0.42),
            },
            ["exoplaneta", "catalogo_exoplanetas", "busqueda_habitabilidad"],
        )
    )

for _i, _nombre in enumerate(_galaxias):
    OBJETOS_CELESTES_INICIALES.append(
        _objeto(
            _nombre,
            "galaxia",
            f"Galaxia real observada en catalogos astronomicos y estudios extragalacticos: {_nombre}.",
            5000 + _i,
            {
                "distancia_anios_luz": round(50000 + ((_i * 720000) % 260000000), 3),
            },
            ["galaxia", "catalogo_extragalactico", "cielo_profundo"],
        )
    )

for _i, _nombre in enumerate(_nebulosas):
    OBJETOS_CELESTES_INICIALES.append(
        _objeto(
            _nombre,
            "nebulosa",
            f"Nebulosa conocida asociada a gas, polvo interestelar o remanentes estelares: {_nombre}.",
            6000 + _i,
            {
                "distancia_anios_luz": round(500 + ((_i * 410) % 180000), 3),
                "temperatura_kelvin": 20 + ((_i * 211) % 18000),
            },
            ["nebulosa", "gas_y_polvo", "cielo_profundo"],
        )
    )

for _i, _nombre in enumerate(_sistemas_estelares):
    OBJETOS_CELESTES_INICIALES.append(
        _objeto(
            _nombre,
            "sistema_estelar",
            f"Sistema estelar conocido, binario, multiple o con planetas catalogados: {_nombre}.",
            7000 + _i,
            {
                "distancia_anios_luz": round(4.2 + ((_i * 8.3) % 1200), 3),
                "temperatura_kelvin": 2400 + ((_i * 113) % 9000),
            },
            ["sistema_estelar", "estrellas_multiples", "catalogo_estelar"],
        )
    )

del _coords
del _habitabilidad
del _objeto
del _estrellas
del _planetas
del _lunas
del _exoplanetas
del _galaxias
del _nebulosas
del _sistemas_estelares
del _i
del _nombre
del _distancia
