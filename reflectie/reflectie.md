# Startdag: 04/05/2023:
de algemene structuur aangemaakt en de opdracht doorgenomen.

# Tweede werkdag: 08/05/2023:

De structuur iets aangepast door de classes in module.py te zetten. Begin van het uitwerken van de klasses. 

Het initieren en koppenen van dit project aan git, vergeten op de eerste dag :( 

Momenteel is de todo-list als volgt:
    * Creeër of download de json dataset (4200 fietsen, 309 Stations, 55k users)
    * Wanneer het programma de eerste keer runt begint de simulatie, is het een tweede keer (of meer) vraag je of ze de simulatie willen verderzetten.
    * genereer html met toestanden van stations, gebruiker of fiets. (komt in _site)
    * maak dit gebruiksvriendelijk via css

In princiepe is de backbone van het programma klaar, zijnde de klasse in de module.py

# Derde dag 10/05/2023:

Plan: Kijken of ik de dataset kan generen en de interface kan maken.

Het maken van de namen is gelukt, de interface komt nog

# Vierde dag 11/05/2023

Redelijk veel aan het script gewerkt om de data op te slaan naar json files en ze terug in het python script te krijgen

Mogenlijk kijk ik straks nog naar het verplaatsen van fiesten ofzo, nog geen idee hoe ik dat moet doen :(

# Dag 5: 13/05/2023

Tijdens het werken aan het project tijdens coderdojo vertelde een medecoath mij dat het een idee is om te kijken naar een sqlite database om de info in op te slagen ipv de json files. Ik heb op deze dag de implementatie gemaakt om alles dat gegenereed wordt in de database te krijgen met succes, echter is er ook een mogenlijke bug gekomen, hier heb ik een issue voor gemaakt op mijn git repo. 

Momenteel is de volgende stap de data uit de db krijgen en in objecten kunnen steken om de dan aan te passen, deze aangepaste data moet dan terug in de database komen. (denk ik, ben nog steeds niet zeker over de visie van de docent hierover) (is ook mogenlijk dit zonder objecten te doen door de entree in de db aan te passen maar dan verlies de opdracht zijn oop gedeelte. dit moet ik dus nog eventjes verduidelijkt krijgen).

buiten de database spullen afkrijgen staat er nog het veranderen op het plan (grotendeels klaar door functies in mijn klasse) samen met het websitegedeelte (ssg implementeren, goede template maken (html en css))

# dag 6: 14/05/2023

Momenteel is het laden van de data in vars gelukt, nu moet ik ze er terug in kunnen opslagen na het aanpassen van een object

begonnen aan het verplaatsen van de fietsen, moet nog kijken of er een goede mannier is om dingen aan elkaar te koppelen. (moet eens kijken naar **fetchall()**)

# dag 7: 24/5/2023

TransporteurInterface klaar, ik ben veel te lang bezig geweest aan kleinde dingen fixen (-1 ipv '-1') :(

# dag 8: 25/5/2023

html stuff, momenteel werk de index.html enkel voor mobile, (gemaakt voor 375x812) #TODO fix

Mannier zoeken om de data van de database in de html te krijgen.