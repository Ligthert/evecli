# evecli
A python tool that queries the EVE XML API

- Primair zoek ik een cli interface voor de EVE SDE/XML of CREST API. Het leuke is als ik vanalles uit kan lezen op een dag omdat het SDE zowat als encyclopedie functioneerd, maar voor nu is het uitprinten van de Training Queue met daarin de skill, van/naar welk level, duur en eindtijd (in de tijdzone van de machine waar het wordt uitgevoerd) voldoende.
- De tool heeft een cli interface waar het op basis van parameters info laat zien en de pogramma weer verlaat:
  - `-f/--file <configfile>`: Dit laad een _custom_ configuratie bestand in [Optioneel]
  - `-k/--key <keyID>`: Een custom keyID [optioneel]
  - `-v/--verification <code>`: Een custom verification Code [optioneel]
  - `-c/--character <character>`: Een custom character ID [optioneel]
  - `-o/--output [table,csv,json,xml]`: Print de infomatie in een bepaalde format. De default is een human readable table, maar een dump naar een ander format zoals csv, json of xml moet ook kunnen. [optioneel]
  - `-w/--write`: Dit schrijgt op gegeven variabelen weg naar de config bestand.
- Standaard leest de tool een config-file uit in `~/.$toolnaam/config.yaml` en laad dit in indien nodig.
- Mag deze niet bestaan, maar als alle opgegeven informatie correct is en de `-w` is gespecificeerd, dan wordt de configfile in yaml in een simpel formaat weggeschreven naar `~/.$toolnaam/config.yaml`.
- Mag de login-informatie opgegeven in de parameters of uitgelezen uit het bestand incorrect zijn, dan dient de programma de sluiten:
  - Een textuele uitleg moet geprint worden wat begint met "ERROR:" gevolgt door de preciese fout waarom het stuk loopt (bij: API is down, stukke internet incorrecte gegevens, character bestaat niet etc etc)
  - Een Exit code groter dan 0 moet meegegeven worden
- Bestanden van SDE kunnen in `~/.$toolnaam/` plat opgeslagen worden of de hele ding unzipped daar worden (voor future proofing). Het mooiste is als de tool automagisch bestanden download bij het eerste uitvoeren. Je kan bij EVEmon afkijken hoe die dat doen en van welke URLs.
