from typing import Optional, List
from pydantic import BaseModel, Field

class SchemaNarratifClassique(BaseModel):
    situation_initiale: str = Field(..., description="Présentation des personnages, du lieu et du contexte avant le début de l'action.")
    element_perturbateur: str = Field(..., description="Événement qui rompt l'équilibre initial et déclenche l'intrigue.")
    peripeties: str = Field(..., description="Ensemble des actions, obstacles et rebondissements qui compliquent la quête.")
    denouement: str = Field(..., description="Moment où le problème est résolu ou la tension se relâche.")
    situation_finale: str = Field(..., description="Nouvel équilibre trouvé, conséquence finale des événements du récit.")

# ✅ CORRIGER les classes problématiques
class SchemaNarratifInMediasRes(BaseModel):
    debut_action: str = Field(..., description="Le récit commence au cœur de l'action, sans introduction préalable.")
    retours_arriere: str = Field(..., description="Des flashbacks ou retours en arrière qui expliquent le contexte et les événements passés.")
    escalade_conflits: str = Field(..., description="Progression des conflits ou des obstacles qui intensifient la tension dramatique.")
    climax: str = Field(..., description="Le point culminant du récit, moment de tension maximale ou de révélation.")
    resolution: str = Field(..., description="Dénouement et résolution des conflits, retour à un nouvel équilibre.")

class SchemaNarratifFlashback(BaseModel):
    situation_initiale: str = Field(..., description="Présentation d'une situation actuelle qui suscite une question ou un mystère.")
    retour_passe: str = Field(..., description="Plongée dans le passé pour révéler les événements ayant conduit à la situation présente.")
    developpement_passe: str = Field(..., description="Déroulement des événements passés avec leurs conflits et enjeux.")
    retour_present: str = Field(..., description="Retour à la situation actuelle, souvent avec une nouvelle compréhension ou révélation.")
    resolution: str = Field(..., description="Résolution de la problématique initiale à la lumière des informations passées.")

class SchemaNarratifStructure3Actes(BaseModel):
    acte_exposition: str = Field(..., description="Introduction des personnages, du contexte et de la situation initiale.")
    acte_conflit: str = Field(..., description="Développement des conflits, obstacles et tensions qui empêchent le protagoniste d'atteindre son but.")
    acte_resolution: str = Field(..., description="Climax suivi de la résolution des conflits et du retour à un nouvel équilibre.")

class SchemaNarratifCadre(BaseModel):
    situation_initiale: str = Field(..., description="Contexte du narrateur principal, qui introduit le récit secondaire.")
    debut_recit: str = Field(..., description="Introduction du récit enchâssé (personnage ou histoire dans l'histoire).")
    developpement_recit: str = Field(..., description="Péripéties ou progression du récit enchâssé.")
    fin_recit: str = Field(..., description="Clôture du récit intérieur.")
    situation_finale: str = Field(..., description="Retour au récit cadre, souvent modifié par le récit secondaire.")

class SchemaNarratifEpistolaire(BaseModel):
    introduction_narrateur: str = Field(..., description="Présentation du narrateur qui compile ou transmet les lettres.")
    alternance_voix: str = Field(..., description="Successions de points de vue ou d'auteurs via lettres/journaux.")
    evolution_rapports: str = Field(..., description="Relations entre personnages qui évoluent à travers l'écriture.")
    effet_reel: str = Field(..., description="Impression d'intimité et d'authenticité créée par le support épistolaire.")

# ✅ Garder les autres classes qui sont OK
class SchemaActanciel(BaseModel):
    sujet: str = Field(..., description="Personnage principal ou héros qui agit dans le récit.")
    objet: str = Field(..., description="But ou objectif poursuivi par le sujet.")
    adjuvant: str = Field(..., description="Personne, objet ou force qui aide le sujet dans sa quête.")
    opposant: str = Field(..., description="Personne, obstacle ou force qui s'oppose au sujet.")
    destinateur: str = Field(..., description="Source de la mission ou de l'appel à l'action du sujet.")
    destinataire: str = Field(..., description="Celui ou celle qui bénéficie de la quête, parfois le sujet lui-même.")

class SchemaQuinaire(BaseModel):
    situation_initiale: str = Field(..., description="Contexte initial dans lequel les personnages évoluent avant le conflit.")
    complication: str = Field(..., description="Événement qui introduit un déséquilibre ou une problématique.")
    action: str = Field(..., description="Actions entreprises pour résoudre la complication.")
    resolution: str = Field(..., description="Résultat des actions entreprises, début de la solution.")
    situation_finale: str = Field(..., description="État final du récit, équilibre retrouvé ou nouveau statut.")

class SchemaDramatique(BaseModel):
    exposition: str = Field(..., description="Présentation des personnages, du lieu et du contexte.")
    incident_declencheur: str = Field(..., description="Événement qui lance l’intrigue.")
    montee_dramatique: str = Field(..., description="Augmentation progressive de la tension avec conflits et complications.")
    climax: str = Field(..., description="Point culminant du récit où la tension atteint son maximum.")
    denouement: str = Field(..., description="Diminution de la tension après le climax.")
    resolution: str = Field(..., description="Retour à une situation d'équilibre ou conclusion de l’histoire.")

class VoyageDuHeros(BaseModel):
    appel_aventure: str = Field(..., description="Invitation à quitter le monde ordinaire pour une quête.")
    refus_appel: str = Field(..., description="Hésitation ou peur initiale du héros face à l'aventure.")
    rencontre_mentor: str = Field(..., description="Rencontre avec un guide ou mentor qui apporte des conseils ou des outils.")
    passage_seuil: str = Field(..., description="Entrée dans un monde inconnu ou début effectif de la quête.")
    epreuves_allies_ennemis: str = Field(..., description="Rencontres marquantes, combats, soutiens et oppositions.")
    epreuve_centrale: str = Field(..., description="Moment de crise ou épreuve décisive du héros (abysse).")
    recompense: str = Field(..., description="Ce que le héros gagne après avoir surmonté l'épreuve.")
    retour_transforme: str = Field(..., description="Retour dans le monde ordinaire, changé par l'expérience.")

class SchemaNarratifFreytag(BaseModel):
    exposition: str = Field(..., description="Mise en place du contexte, des personnages et des enjeux.")
    montee_dramatique: str = Field(..., description="Accumulation de tensions et de conflits.")
    climax: str = Field(..., description="Point culminant du récit, moment de plus grande intensité.")
    chute: str = Field(..., description="Conséquences du climax, début de la résolution.")
    denouement: str = Field(..., description="Retour à un nouvel équilibre ou conclusion du récit.")

class SchemaNarratifCirculaire(BaseModel):
    situation_initiale: str = Field(..., description="Point de départ du récit.")
    parcours: str = Field(..., description="Suite d’événements formant une boucle narrative.")
    retour_final: str = Field(..., description="Retour au point de départ, avec ou sans évolution du personnage.")

class SchemaNarratifFragmente(BaseModel):
    fragments: str = Field(..., description="Fragments narratifs séparés : souvenirs, scènes disjointes, temporalités multiples.")
    connexion_progressive: str = Field(..., description="Liaisons qui émergent entre les fragments au fil du récit.")
    revelation_finale: str = Field(..., description="Éclaircissement global ou chute révélatrice reliant les fragments.")

class SchemaNarratifHorreur(BaseModel):
    exposition: str = Field(..., description="Présentation du décor, souvent inquiétant.")
    apparition_du_mal: str = Field(..., description="Premiers signes du surnaturel ou de la menace.")
    escalade: str = Field(..., description="Tensions et attaques s’intensifient.")
    affrontement_final: str = Field(..., description="Confrontation ultime avec la menace.")
    chute: str = Field(..., description="Fin souvent ouverte ou ambigüe, avec trace durable de la peur.")

class SchemaNarratifRomanPolicier(BaseModel):
    situation_initiale: str = Field(...,description="Présentation du contexte, de la scène du crime et des premières informations sur l’affaire (qui ? quoi ? quand ? où ?). Certaines questions peuvent rester sans réponse, comme l’identité du criminel ou son mobile.")
    element_declencheur: str = Field(...,description="Événement déclencheur de l’intrigue, généralement un crime (meurtre, vol, enlèvement, etc.).")
    objet: str = Field(...,description="But principal de l’enquête : identifier le coupable. Il peut y avoir des objectifs secondaires comme retrouver une victime, un objet volé ou arrêter des complices.")
    enquete: str = Field(...,description="Déroulement de l’enquête : interrogatoires, collecte d’indices, fausses pistes, analyses scientifiques, nouvelles infractions. L’enquêteur élimine progressivement les hypothèses pour se rapprocher de la vérité.")
    climax: str = Field(...,description="Point culminant de l’enquête : révélation de l’identité du criminel, confrontation et tentative d’arrestation. Toute la tension dramatique atteint son apogée.")
    situation_finale: str = Field(...,description="Conclusion de l’histoire : arrestation (ou non) du coupable, retour à l’ordre, conséquences de l’affaire.")