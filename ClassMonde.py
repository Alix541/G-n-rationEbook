from typing import Optional, List
from pydantic import BaseModel, Field

from pydantic import BaseModel, Field

class Monde(BaseModel):
    geographie_environnement: Optional[str] = Field(
        description="Type de monde, relief, climat, zones inhabitées, ressources naturelles",
        example="Monde plat divisé en cinq régions climatiques, avec une mer acide au sud et des cristaux d'énergie rares dans les montagnes."
    )

    histoire_temps: Optional[str] = Field(
        description="Origine du monde, grandes périodes historiques, événements fondateurs, rapport au temps",
        example="Créé par un cataclysme magique, le monde est structuré en trois âges cycliques, régis par les lunes."
    )

    politique_pouvoir: Optional[str] = Field(
        description="Systèmes de gouvernement, institutions, corruption, conflits, figures de pouvoir",
        example="Empire central autoritaire gouverné par des oracles, en guerre avec des cités-états autonomes."
    )

    peuples_especes: Optional[str] = Field(
        description="Espèces dominantes, hiérarchies sociales, origines, relations entre groupes, capacités spécifiques",
        example="Trois espèces intelligentes : humains, thérians et synthétiques, vivant en paix fragile après un long conflit."
    )

    culture_croyances: Optional[str] = Field(
        description="Religions, rituels, tabous, langues, arts, traditions",
        example="Culte solaire dominant, langues tribales régionales, danses rituelles et récits gravés dans la pierre."
    )

    valeurs_morale: Optional[str] = Field(
        description="Valeurs dominantes, lois, justice, tabous sociaux et moraux",
        example="L'honneur du clan prime sur tout, la trahison est punie par l'exil éternel."
    )

    magie_technologie: Optional[str] = Field(
        description="Existence de la magie ou de la technologie, source, règles, limites, accès, impact sur la société",
        example="La magie est issue des chants des Anciens, interdite aux castes inférieures sous peine de mort."
    )

    economie_vie_quotidienne: Optional[str] = Field(
        description="Système économique, ressources, monnaies, métiers, classes sociales, mode de vie",
        example="Système de troc renforcé par une monnaie d'énergie stockée dans des cristaux de pouvoir."
    )

    transports_communications: Optional[str] = Field(
        description="Modes de transport, infrastructures, systèmes de communication",
        example="Portails de brume pour les élites, caravaniers pour les autres ; communication par runes gravées."
    )

    urbanisme_architecture: Optional[str] = Field(
        description="Organisation des villes, types de constructions, matériaux utilisés, symboles architecturaux",
        example="Cités construites autour d’arbres titanesques, mêlant bois vivant et métal forgé au feu céleste."
    )

    psychologie_collective: Optional[str] = Field(
        description="Peurs, mythes fondateurs, croyance sur la mort, rapport à l’inconnu",
        example="Peuple hanté par la mémoire des Ténèbres, croit que chaque mort est un retour vers l’Océan-Mémoire."
    )
"""
    role_heros: Optional[str] = Field(
        description="Position du héros dans le monde, capacité à le changer, relation au système en place",
        example="Le héros est l’enfant d’un pacte ancien, seul capable de briser le cycle de domination millénaire."
    )
"""
