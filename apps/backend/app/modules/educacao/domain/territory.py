from enum import Enum
from typing import Final, Mapping, Sequence


class Provincias(str, Enum):
    HUAMBO = "HUAMBO"


class MunicipiosHuambo(str, Enum):
    BAILUNDO = "BAILUNDO"
    CAALA = "CAALA"
    EKUNHA = "EKUNHA"
    HUAMBO = "HUAMBO"
    KATCHIUNGO = "KATCHIUNGO"
    LONDUIMBALI = "LONDUIMBALI"
    LONGONJO = "LONGONJO"
    MUNDO = "MUNDO"
    TCHICALA_TCHOLOANGA = "TCHICALA_TCHOLOANGA"
    TCHINDJENDJE = "TCHINDJENDJE"
    UKUMA = "UKUMA"


TERRITORY_HIERARCHY: Final[Mapping[Provincias, Mapping[MunicipiosHuambo, Sequence[str]]]] = {
    Provincias.HUAMBO: {
        MunicipiosHuambo.BAILUNDO: (
            "BAILUNDO",
            "BIMBE",
            "HENGE",
            "LUFUI",
            "LUNGE",
        ),
        MunicipiosHuambo.CAALA: ("CAALA", "CALENGA", "CATATA", "CUIMA"),
        MunicipiosHuambo.EKUNHA: ("EKUNHA", "TCHIPEIO"),
        MunicipiosHuambo.HUAMBO: ("HUAMBO", "CALIMA", "CHIPILINDO"),
        MunicipiosHuambo.KATCHIUNGO: (
            "KATCHIUNGO",
            "CHINHAMO",
            "CHIUMBO",
        ),
        MunicipiosHuambo.LONDUIMBALI: (
            "LONDUIMBALI",
            "ALTO HAMA",
            "CUMBILA",
            "GALANGA",
            "USSEQUE",
        ),
        MunicipiosHuambo.LONGONJO: ("LONGONJO", "CHILA", "LEPI"),
        MunicipiosHuambo.MUNDO: ("MUNDO", "KAIMA", "SAMBO"),
        MunicipiosHuambo.TCHICALA_TCHOLOANGA: (
            "TCHICALA-TCHOLOANGA",
            "MBEMBE",
            "SAMBO",
            "SOMBOCALA",
        ),
        MunicipiosHuambo.TCHINDJENDJE: (
            "TCHINDJENDJE",
            "CHIPIA",
            "QUISSALA",
        ),
        MunicipiosHuambo.UKUMA: ("UKUMA", "KAKIUEIA", "MUNDUNDO"),
    }
}
