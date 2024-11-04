# Biweekly 04.11.2024
## Attendees

- [x] @juliuspor
- [x] @sm1lla
- [x] @joh-dah
- [x] @elenagensch
- [x] @cdfhalle

## Paper Findings
- LLMs: Prompt Engineering
- Microsoft Paper: Code Plan
- RAG approach 

wir brauchen daten (evaluierung, und für approaches), überlegen was brauchen wir
- static approach, LLM , hybrid, begruenden warum nicht static/hybrid notwendig
- legen wir uns schon fest wie lösung einbinden? erstmal fokus was laufen würde
- metriken überlegen auch notwendig um abzuwenden (code generation paper nochmal anschauen)
- Synopsis Table Kategorien sollten wir uns darauf einigen

## PM Meeting Vorbereitung
- Fragen sammeln in Google docs
- Fragen, ob es Daten gibt

## Actions
- [ ] @elena notes, @smilla agenda
- [x] @elena erinnerung an martin repository fuer spark connect projeke (elena)
- [ ] @all Synopsis Table, Kategorien überlegen
- [ ] @all: Slides für Vorstellung von Ansätzen: beste jew zusammenfassen
  	Ziel: Vorstellung Approach, Wertung der Methode im Paper (Limitations + Strengths), Wie passt auf unser Problem (Synopsis Table)
   @elena Hybrid API Migration, 
  	@julius CodePlan: Repository-Level Coding using LLMs and Planning
  	@smilla @conrad RAG approach und ältere Ansätze (static wie congruity)
  	@johanna LLM und schlaue Prompts

# Biweekly 01.01.0001

| Name            | About                       | Title         | Agenda | Timekeeping | Notes |
|-----------------|-----------------------------|---------------|-----------|-----------|-----------|
| Meeting template| Meeting template for keylime| Meeting dd/mm/yy | @xyz | @xyz | @xyz |

## Attendees

- [ ] @juliuspor
- [ ] @sm1lla
- [ ] @joh-dah
- [ ] @elenagensch
- [ ] @cdfhalle

## Topics

* 

## Actions

- [ ] 

## Meeting notes

*
---
# Next Steps 31.10.2024
* Open Source Projekte von Martin anschauen um besseres verständniss vom probleminstanzen zu bekommen
* Fragen für den PM ausdenken
* Meeting mit PM am Donnerstag festlegen
* weitere paper herraussuchen, verstehen und vor/nachteile herausarbeiten
* Lösungsansätze herausarbeiten (probleme detecten, probleme fixen)

---
# Weekly with Chris 31.10.2024

| Name            | About                       | Title         | Agenda | Timekeeping | Notes |
|-----------------|-----------------------------|---------------|-----------|-----------|-----------|
| Weekly with Chris | tbd | Weekly with Chris 1 | @juliusspor | @sm1lla | @joh-dah |

## Attendees

- [x] @juliuspor
- [x] @sm1lla
- [x] @joh-dah
- [x] @elenagensch
- [ ] @cdfhalle
- [x] Chris

## Topics

* 

## Actions

- [ ] Next meeting everyone 2 mins expectations for the project. what do we want from it?

## Meeting notes

* For meeting with PM SWOT analysis
* Get inspirations for questions from paper
* Look into testing APIs
* Outcome is veeery open
* would be great to have some reasearch and development experience not only engineering stuff

---
# Weekly with Martin 31.10.2024

| Name            | About                       | Title         | Agenda | Timekeeping | Notes |
|-----------------|-----------------------------|---------------|-----------|-----------|-----------|
| Weekly with Martin | tbd | Weekly with Martin 1 | @juliusspor | @sm1lla | @joh-dah |

## Attendees

- [x] @juliuspor
- [x] @sm1lla
- [x] @joh-dah
- [x] @elenagensch
- [ ] @cdfhalle
- [x] Martin
- [ ] Chris

## Topics

* See slides

## Actions

- [ ] Martin schickt hat ne liste mit beliebten open source projekten - was sind die gaps darinn, damit die mit SC funktionieren?

## Meeting notes

* es gibt sachen, die man besser mit rdds lösen kann, sind aber sehr spezielle use cases
* wollen es für 90% der leute besser machen. die leute die dann doch die alte api verwenden wollen müssen halt spark connect abschalten und die nachteile in kauf nehmen
* man halt alternative varianten für die dinge gebaut, die nicht mehr funktionieren (nicht bei allem, aber bei den meist genutzen sachen)
* möglichst wenig breaking changes, nur kompatible änderungen. müssen wir nicht beachten
* Großteil der user bei Python, also fokus auch auf pyspark
* es soll kein tool bei rauskommen. Wir sollen verschiedene wege herausarbeiten, die die transition einfacher machen
* --> Problemverständniss im Kern korrekt!

* Wer hat das größte Problem mit diesem Api Change? -> Plan ist mit spark 4 spark connect als default zu etablieren. Getting started ist gar nicht mal das hauptproblem. Der case mit bestehenden Kunden, die ihren code vor ein paar jahren geschrieben haben ist wichtiger
* Ziel ist es für bestehende Kunden die Migration einfacher zu machen
* wenn man eine migration macht, soll man in code refactoring investieren oder in einer ebene, die diese übersetzung macht

Was wäre der gewünschte outcome für das projekt?
Verstehen, kann ich was besseres für diese api kompatibilität finden, als alles umzuschreiben?
Software bauen, die deinen code parsed und den übersetzt? Wie macht man das at scale? Ein Tool für alle kunden -> wie hilft man bei der migration?
* Teilweise bloße Übersetzung nicht möglich, code muss umstrukturiert werden
* Problem ggf. weniger regelbasiert lösen

Step 1: Kunden müssen verstehen: Sind sie überhaupt betroffen? Müssen sie was machen? Oder können sie direkt umstellen?
Step 2: Tatsächlich bei der Migration helfen, falls der Code nicht komplett kompatibel ist

Letztendlich liegt es bei uns wo der fokus liegt
Nächste woche Forschungsansätze anreißen, martin in entscheidungsfindungsprozess miteinbeziehen

Was macht Jakob? (Der PM)
* Mit Kunden zu arbeiten und requirements herauszuarbeiten um sachen von single cluster auf shared cluster rüber zu bringen
* Was sind die gaps zwischen diesen arhcitekturen?
* Wie können wir möglichst einfach Kunden dazu kriegen andere Clusterarchitetur anzunehmen um die benefits nutzen zu können
* https://www.databricks.com/dataaisummit/session/unity-catalog-lakeguard-data-governance-multi-user-apachetm-spark



---
# Biweekly 31.10.2024

| Name            | About                       | Title         | Agenda | Timekeeping | Notes |
|-----------------|-----------------------------|---------------|-----------|-----------|-----------|
| Biweekly | tbd | Biweekly 3 | (@juliusspor) | (@sm1lla) | @joh-dah |

## Attendees

- [x] @juliuspor
- [x] @sm1lla
- [x] @joh-dah
- [x] @elenagensch
- [ ] @cdfhalle

## Topics

* Paper findings discussion
* Preperation für Meeting mit Chris 
* Slides für meeting Martin (paar sachen müssen ergänzt werden)

## Actions

- [ ] Look for in production examples for issues with the transition to spark connect e.g "PySparkNotImplementedError: [NOT_IMPLEMENTED] sparkContext() is not implemented."
- [ ] Add questions for meeting with martin

## Meeting notes

* Zur Literatur: Hauptsächlich 2 Ansätze
* a) LLMs nutzen um Code umzuschreiben
* b) Mapping erstellen (mit llms oder ohne) 

---
# Biweekly 29.10.2024

| Name            | About                       | Title         | Labels | Assignees |
|-----------------|-----------------------------|---------------|--------|-----------|
| Biweekly | prepare meeting with Martin and discuss current progress | Biweekly 2 | - | @cdfhalle |

## Attendees

- [x] @juliuspor
- [x] @sm1lla
- [x] @joh-dah
- [x] @elenagensch
- [x] @cdfhalle

## Topics

## Actions

- [x] @cdfhalle meeting template anpassen (agenda: @juliusspor, timekeeping: @sm1lla, notes: @joh-dah)
- [ ] @joh-dah macht when to meet für paint in style in Schöneberg
- [ ] @juliusspor erstellt slide deck und schickt es an Martin
- [ ] @sm1lla schreibt nachricht in den Slack und fragt nach Treffen mit dem Product Manager
- [ ] @all nach weiteren papern suchen
- [ ] @all weiter in spark connect einsteigen, Fragen überlegen
- [ ] @all über synopsis table nachdenken

## Meeting notes

* Wir wollen Orga rollen verteilen
  * 1 Person die mitschreibt
  * 1 Person die sich um die Agenda kümmert
  * 1 Person die time management macht, bei größeren Meetings
  * 1 Porzellan malen orga
* Am Donnerstag Chris wegen Teambuilding event updaten
* Was haben wir herausgefunden:
  * Frage: Warum genau nutzen menschen rdd's / ist ein wechsel zu dataframes immer sinnvoll?
  * Was geht eigentlich bei congruity ab? Nutzt das irgendwer?
  * Was verändert sich noch bei der Migration zu Spark Connect? RDDs, Spark Context, ...?
  * Um welche API von Spark geht es eigentlich? Fokussieren wir uns auf Python oder müssen wir noch mehr berücksichtigen?
  * Problem mit Congruity: Was wenn sich dinge in der Zukunft ändern
* Google Slides aufsetzen mit Fragen für Martin und ihm vor Donnerstag zukommen lassen
* Paper im Zotero waren etwas am thema vorbei
  * ggf tags dran machen damit nicht jeder das gleiche lesen muss
* Donnerstags Meeting nach vorne verschoben, weil @sm1lla und @cdfhalle danach Vorlesung haben
---
# Biweekly 24.10.2024

| Name            | About                       | Title         | Labels | Assignees |
|-----------------|-----------------------------|---------------|--------|-----------|
| Biweekly | understanding the problem | Biweekly 1 | - | @cdfhalle |

## Attendees

- [x] @juliuspor
- [x] @sm1lla
- [x] @joh-dah
- [x] @elenagensch
- [x] @cdfhalle

## Topics

* whats the difference between apache and apache connect, and what problems pop up during migration to connect

## Actions

- bis Montag:
  - Fragen überlegen die man noch nicht verstanden hat
  - Problembeispiele sammeln für Kompatibilität

- am Montag: 
  - Problem strukturieren
  - Martin Meeting vorbereiten

