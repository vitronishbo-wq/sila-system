from enum import Enum

class NationalityMode(str, Enum):
    JUS_SOLI = 'jus_soli'
    JUS_SANGUINIS = 'jus_sanguinis'
    NATURALIZED = 'naturalized'