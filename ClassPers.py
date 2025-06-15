from typing import Optional, List
from pydantic import BaseModel, Field

class Perssonage(BaseModel):
    """Description du personnage"""
    PersonnagePrincipal : bool = Field(description="Détermine si le personnage est un personnage principal ou pas")
    PersonnageSecondaireMajeur : bool = Field(description="amis, mentors, antagonistes secondaires — ils reviennent souvent et influencent directement l’intrigue ou le héros.")
    PersonnageSecondaireMineur : bool = Field(description="réceptionniste, chauffeur, professeur, etc. — présents dans 1 à 2 scènes, mais servent l’ambiance ou le réalisme.")
    Prenom : str = Field(description="Le prenom du personnage ")
    Nom : Optional[str] = Field(description="Le nom du personnage ")
    Surnom : Optional[str] = Field(description="Un surnom par lequel on appelle le personnages")
    Age : int = Field(description="L'âge du personnage ")
    Faiblesse : str = Field(description="Ce qui rend le personnage vulnérable : difficultés du quotidien, des doutes, des contradictions, des limite, des faiblesses physiques etc...")
    Force : str = Field(description="Ce qui diférencie notre super-héros du reste des personnages, ce qui le rends particulier et fort")
    Caractere : str = Field(description="Est ce qu'il est nerveux, gentil, méchant, attentionner, dur, fou etc...")
    Mission : str = Field(description="Le but du personnages dans l'histoire")
    Amis : Optional[str] = Field(description="Les compagnons de routes du personnages, les personnes qu'ils aiment bien, ça famille, amis etc...")
    Ennemie : Optional[str] = Field(description="Les personnes que le héro n'aime pas, qui se mette sur ça route, qui sont contre lui")
    DescriptionPhysique : str = Field(description="Une courte description physique du personnages, en comprenant les habits et la morphologie")
    HistoireDuPersonnage : str = Field(description="Décrire ici le passé du personnage, qui pourrait expliquer certaine caractèrique chez lui")
    QuotidienDuPersonnage : str = Field(description="Décrire ici le quotidien du personnage, ce qu'il fait au moment au débute l'histoire")

class ListePersonnages(BaseModel):
    """Une liste de personnage pour l'histoire"""
    personnages: List[Perssonage]