heuristica_AQA = {
    'araraquara': 98,
    'jaboticabal': 153,
    'taquaritinga': 148,
    'ribeirao_preto': 149,
    'porto_ferreira': 85,
    'sao_carlos': 71,
    'jau': 91,
    'brotas': 60,
    'pirassununga': 71,
    'rio_claro': 32,
    'limeira': 25,
    'piracicaba': 0  # objetivo
}

heuristica_JAU = {
    'jau': 125,
    'araraquara': 66,
    'jaboticabal': 46,
    'taquaritinga': 65,
    'ribeirao_preto': 0, #objetivo
    'porto_ferreira': 72,
    'sao_carlos': 80,
    'brotas': 110,
    'pirassununga': 85,
    'rio_claro': 120,
    'limeira': 136,
    'piracicaba': 149  
}

arestas = [
    ('jaboticabal', 'ribeirao_preto', 50),
    ('jaboticabal', 'araraquara', 62),
    ('jaboticabal', 'taquaritinga', 25),
    ('taquaritinga', 'araraquara', 56),
    ('araraquara', 'ribeirao_preto', 79),
    ('araraquara', 'jau', 66),
    ('araraquara', 'sao_carlos', 38),
    ('sao_carlos', 'jau', 85),
    ('sao_carlos', 'brotas', 59),
    ('jau', 'brotas', 47),
    ('brotas', 'piracicaba', 71),
    ('ribeirao_preto', 'sao_carlos', 87),
    ('ribeirao_preto', 'porto_ferreira', 77),
    ('porto_ferreira', 'sao_carlos', 47),
    ('porto_ferreira', 'pirassununga', 17),
    ('pirassununga', 'sao_carlos', 52),
    ('pirassununga', 'rio_claro', 57),
    ('pirassununga', 'limeira', 65),
    ('rio_claro', 'sao_carlos', 53),
    ('rio_claro', 'limeira', 28),
    ('rio_claro', 'piracicaba', 35),
    ('limeira', 'piracicaba', 32),
]

cidades = [
    'jau',
    'araraquara',
    'jaboticabal',
    'taquaritinga',
    'ribeirao_preto', 
    'porto_ferreira',
    'sao_carlos',
    'brotas',
    'pirassununga',
    'rio_claro',
    'limeira',
    'piracicaba',
]