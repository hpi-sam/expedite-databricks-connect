# Biweekly 12.12.2024  

## Attendees  
- [ ] @juliuspor  
- [x] @sm1lla  
- [ ] @joh-dah  
- [x] @elenagensch  
- [x] @cdfhalle  

## Topics  
- **High priority**: Discuss deliverables for video next Tuesday.  
- Embedding functions in Conrad.  
- Vectorize: Compare RAG embedding models, evaluate differences (Llama 70B, OpenAI embedding).  
- Retriever from RAG: Benchmark papers—most retrievers are embedding models, ranking models, or Salesforce SFR embedding.  
- Experiment with adding context to generated code.  
- Code context experiments are in WandB reports (some configurations slightly outperform or perform similarly to setups without RAG).
- stackoverflow code now in json, no experiments yet
- Evaluate CSVs via pickle.  
- Hybrid API migration paper: started to apply to our problem, sketch out code.
- The responsibility to note what one is working on lies with each individual. Please document it in the meeting log yourself.

## Actions
-  stackoverflow, code experiments: @elenagensch
- @cdfhalle
- @joh-dah
- @sm1lla
- @juliuspor

# Biweekly 10.12.2024

| Name            | About                       | Title         | Agenda         | Timekeeping | Notes        |
|------------------|-----------------------------|---------------|----------------|-------------|--------------|
| Meeting Template |  | Meeting 01/01/0001 | |    | @elenagensch |

## Agenda
- OpenAI credits: Julius will write an email.
- Linter feedback as inline comments in the code, PR to be created.
- Conrad suggests "Chain of Thought."
- Julius will try using Google for solutions.
- Discuss deliverables for Martin on Thursday (code video + final presentation).

## Attendees

- [x] @juliuspor  
- [ ] @sm1lla  
- [x] @joh-dah  
- [x] @elenagensch  
- [x] @cdfhalle  

## Topics

- **OpenAI Credits**: Julius will write and send an email regarding this.
- **Linter Feedback Prompt engineering**: Feedback is added as inline comments in the code, followed by creating a PR.
- **Chain of Thought**: potential approach for better logical reasoning - @cdfhalle.
- **Google Searches**:  explore solutions using Google for prompts - @juliuspor.
- **Deliverables**: Code video and final presentation to be discussed on Thursday.

# Biweekly 01.01.0001

| Name            | About                       | Title         | Agenda | Timekeeping | Notes |
|-----------------|-----------------------------|---------------|-----------|-----------|-----------|
| Meeting template| Meeting template for keylime | Meeting dd/mm/yy | @xyz | @xyz | @xyz |

## Agenda
- Sollen wir noch konkretere TODOs festlegen
- Meeting mit Marting
- Todos bis Donnerstag
- 

## Attendees

- [x] @juliuspor
- [x] @sm1lla
- [x] @joh-dah
- [x] @elenagensch
- [x] @cdfhalle

## Topics

* 

## Actions

- [ ] 

## Meeting notes

*

# Meeting with Martin 05.12.2024

## Agenda
-  Present progress
  
## Attendees

- [ ] @juliuspor
- [x] @sm1lla
- [x] @joh-dah
- [ ] @elenagensch
- [x] @cdfhalle


## Meeting notes


- Finding out which kind of errors
  - use python interpreter to check if it is syntactically correct?
  - import all imports and then eval code

- Martin's idea for more examples:
    - use unit tests from pyspark for rdds etc
- record small demo video 3-5 minutes, little presentation and go through code and example
    - for beginning of January
- final presentation in Databricks office 

Internal discussion with Chris:
- get runtime errors by running code by executing code just to find out if this would help
- track for individual examples the distribution of how often they fail
    - track what makes the code complex
- how is the code split? - are there different ways of splitting it?
- try OpenAI model -> which subscription necessary?
- Elena's card receipt for team building

# Biweekly 05.12.2024

| Name            | About                       | Title         | Agenda | Timekeeping | Notes |
|-----------------|-----------------------------|---------------|-----------|-----------|-----------|
| Meeting template| Meeting template for keylime | Meeting dd/mm/yy | @juliuspor | @xyz | @cdfhalle |

## Agenda
- conda und den umgang mit main auf github

## Attendees

- [ ] @juliuspor
- [x] @sm1lla
- [x] @joh-dah
- [x] @elenagensch
- [x] @cdfhalle

## Topics

* 

## Actions

- [ ] 

## Meeting notes

* Johanna hat statische Analyzer hinzugefügt: Mypy und Flake8
* Johanna hat Prints formatiert
* Smilla hat alles auf wandb geändert
* ...und experimente laufen lassen
  * no Rag funktioniert am besten
  * no Rag no Error funktioniert am zweitbesten
* Zur benutztung von Main smillas PR lesen
* Conrad hat Assistant Klasse geschrieben, Conda environment gefixt und Logging eingebaut (noch nicht gemerged)
* Bei Änderungen an der environment.yml am besten form mergen noch einmal versuchen ein Environment mit der yml zu erstellen.
  * Außerdem aufpassen beim mergen.
* Bei kleineren Änderungen zumindest nachricht in den Telegram
* Bei größeren Änderungen pull request auf machen
* Bei dingen vermutlich viele Konflikte erzeugen pull request reviewen lassen
* Was kann man noch machen?
  * Embedding Funktion checken / Retriever Anschauen
  * Stack Overflow Code verwenden
  * Modell selbst den Vectorstore durchsuchen lassen
  * (mehr) Experimente Machen, schauen was hilft und was nicht
    * Konkret anschauen, welche Beispiele gelöst werden
  * Prompt engineering
    * Linter output neben den Code Zeilen die den Error produzieren

---
# Biweekly 03.12.2024

| Name            | About                       | Title         | Agenda | Timekeeping | Notes |
|-----------------|-----------------------------|---------------|-----------|-----------|-----------|
| Biweekly | Biweekly | Meeting dd/mm/yy | @juliuspor | @xyz | @cdfhalle |

## Agenda
- White Box 
- Fehlendes Internet 
- Sonstiges 
- Themen für Donnerstag

## Attendees

- [x] @juliuspor
- [x] @sm1lla
- [x] @joh-dah
- [x] @elenagensch
- [x] @cdfhalle

## Topics
* 

## Actions

- [ ] Johanna's Pull request reviewen
- [ ] Stack Overflow Code in Rag integrieren
- [ ] Conrad läd 8Bit llama herunter

## Meeting notes

* Julius: Research zum thema white box uncertainty estimation für llms
  * Ergebnis: Black box ist vermutlich besser --> Sample consistency
    * n outputs generieren und ergebnis vergleichen + ggf. leichte variation der Promt
* Fehlendes Internet -> Smilla ist enttäuscht
* Johanna hat das Repository aufgeräumt
  * Aufteilung in Evaluation, Linter, Vectorstore
  * Main File ausführen und configurieren mit config.py
* Smilla schaut nochmal wie leicht es ist die aktueller repo Struktur mit W&B zu nutzen
* Vectorstore für Dokumentation und Code liegt im share ordner
* Experimente mit Rag (Smilla)
  * mini ablation study hat gezeigt, dass die fehlermeldungen aktuell garnicht so viel nutzen
* Elena hat neue Repositories in zum Vectorstore hinzugefügt
  * Es gibt wenige Beispiele die auf JVM zugreifen --> wenig context für das LLM
* Was kann man noch ausprobieren
  * besseres embedding model / retrieval
  * llm googlen lassen
  * stack overflow integrieren
  * interaktives
  * Code complexity ausrechnen
* Julius ist Donnerstag nicht da

---
# Biweekly 26.11.2024

## Agenda
- Fortschritt letzte Woche
- Pläne diese Woche 
- Generelle timeline

## Attendees

- [x] @juliuspor
- [x] @sm1lla
- [x] @joh-dah
- [x] @elenagensch
- [x] @cdfhalle


## Actions
- [ ] Julius: Überlegen wie man complexity, uncertainty und accuracy messen?
- [ ] Johanna: Linter einbauen und versuchen Ergebnisse zu verbessern, über Evaluierung philosophieren
- [ ] Elena: Rag mit Code und Linter nutzen um zu überprüfen ob der Code aus dem RAG noch Fehlermeldungen enthält
- [ ] Smilla: Beispiele schreiben, Rag optimieren, andere Modelle ausprobieren (CodeLlama, GPT, größeres Llama)
- [ ] Conrad: Rag mit Code verbessern

## Meeting notes
- Wann möchten wir fertig werden? Ende Februar anpeilen (notfalls Report noch später fertig)
- Smilla: mit docs tainiert
- Elena:
  - Vectorstore mit verschiedenen Kategorien von Daten (source in den Metadaten setzen)
  - 2 Beispiele erstellt
- Conrad:
  - Paper angeschaut zu Code Migration und Code Generation
  - interessantes Paper mit ähnlichem Anwendungsfall, zur Evaluierung wurde sich Code Migration ausgedacht
  - Llama 405B kann jetzt gehostet und über API genutzt werden
- Julius:
  - mehr Matcher zum Linter hinzugefügt, jetzt sind alle Funktionen drin
  - Beispiel erstellt
- Johanna:
  - ausprobiert Output von LLM wird nochmal reingeben mit neuen Fehlermeldungen
  - erstmal nicht besser geworden
- Frage: sollen wir das LLM-generierte Beispiel auch nochmal auf syntaktische Fehler checken?
  - können wir mal ausprobieren
- Complexity, Uncertainty und Accuracy
  - Wie kann man diese Sachen messen?

---

# Weekly 21.11.2024 with Chris
## Notes
- Maybe make our examples a bit more complicated
- Use LLM to generate new test case code snippets
- Call LLM multiple times to evaluate the difference
- Stick to smaller examples first
- How well does the LLM know if it's hallucinating or doesn't know?
- uncertainty, complexity, accuracy (3x3) grid

## Actions
Alle:
- Ein Test Case für die Evaluierung

Julius:
- Linter

Smilla:
- Dokumentationen in RAG
- Ausprobieren RAG mit Evaluierung verbinden

Elena:
- Code in RAG
- GGf. Tags im rag um zwischen alten/neuen code zu unterscheinden

Johanna:
- iterativer aufruf vom Rag, ergebniss wieder als input nehmen

Conrad:
- probieren, LLM als server zu hosten?
- sonst wo gerade hilfe gebraucht wird
  

# Meeting with Martin 21.11.2024
## Agenda
- Google Presentation

## Notes
- Get code snippets from StackOverflow and rewrite them ourselves in SparkConnect
- Investigate StackOverflow API to get rdd code --> Parse them with the Linter
  - Dataframes are supported fully
  - Search for everything sparkcontext/spark ml gets weird
---> Can you somehow use StackOverflow as a source?
- Interesting part: Most likely not gonna need to refactor whole codebase
    - Main thing you pass in lambda functions in rdd
- dont think you have to refactor 1000 lines vs 100 lines (Martin doesn't know though)
    - is it enough if we identify the smaller pieces?
        - Question: is the context even relevant? if not, then we don't need to take the context into account and have smaller input for LLM
    - Idea: make code more complex to test whether that is relevant!
    - Also: rewriting might depend on intent of the engineer

Martin sees two kinds of ways to look at the problem  
1. Just look at the problem (Linter approach)
2. Also look at the context and take it into account


# Biweekly 21.11.2024
## Agenda
- Linter Fortschritt
- Conda-README & Code-Beispiele
- API-Credits & RAG-Doku
- Best Practices für Code-Gen in RAG
- Meeting mit Martin

## Notes
- RAG code funktioniert mit neuem Model
- Research best practices zu code-gen für RAG fehlt noch
- Langchain community: crawler für github repos (pull reqs, code)
- Iterative LLM calls untersuchen
- Martin fragen nach Repositories
- Martin fragen nach Kunden Repos

## Next steps
- RAG approach improven und erweitern
- Code in RAG einbauen
- Mehr Dokumentationsseiten im RAG einbauen
- Linter im RAG benutzen
- Iterativer LLM call testen
- Evaluation Gedanken machen
  
- [ ] Julius: Linter Matcher erweitern
- [ ] Elena: 
- [ ] Smilla: Chrisitan fragen wegen API credits
- [ ] Conrad: 
- [ ] Johanna: 


# Biweekly 19.11.2024
## Agenda
1. Zugang KIZ cluster
2. Fortschritt Linter
3. Fortschritt Daten - Evaluierung und RAG
4. Fortschritt RAG bauen (inkl LLAMA)
5. Teambuilding

## Notes
- Gute Beispiele zum Übersetzen: Spark by example
- Smilla: Mit Llama Code generieren und vergleichen mit richtigem Code (0/6 momentan)
- Elena: Suche: Sourcegraph nicht hilfreich
- Conrad: Tutorial zum Thema RAG (Langchain), Llama 2b nicht optimal, RAG Input nicht optimal
- Fragen: Welche Daten sollten in RAG rein geladen werden? (Docu, Code vorher nachher, Websiteinhalte)

## Next steps
- [ ] Julius: Linter verbessern und hochladen + readme 
- [ ] Elena: Fügt Readme für Conda Sachen hinzu, Suche nach Code Beispielen
- [ ] Smilla: Fragen für API Credits, Dokumentationen in RAG einbauen: researchen
- [ ] Conrad: Research: Best practices für code generation RAG
- [ ] Johanna: - TBD 


# Weekly with Chris 14.11.2024

## Agenda
1. Update was wir machen
2. Wie Evaluieren wir am Ende
3. 1o1 Meetings abmachen
4. Tisch, Bildschirme Mikrofone
5. Server zugang

## Meeting note
* Professor giese can pay for chat GPT (chris says)
* For Data: Doc von Jakob, pyspark documentation
* What should we focus on? Where do we set the boundry? What is to complex to solve with LLM?
* Vorschlag von Chris: Erst ein model machen, dass einschätzt wie komplex die ändeung wäre. Aber unklar wie das umgesetzt wird
* Confidence feststellen indem mehrere solutions vorgeschlagen werden und die Varianz berechnet wird. Hohe varianz in den antworten = geringe confidence

## Actions
- [ ] Felix Boether schreiben, dass zugang zum delab auch nice wäre
- [ ] Open ticket for FM team or write chris
- [ ] Chris einladen zum porzellan malen
- [ ] ggf. nochmal meeting mit Jakob machen, falls wir da fragen etc haben
- [ ] 


# Biweekly 14.11.2024
## Notes
* Meeting mit Martin absagen
* Für Meeting mit Chris:
  1. Update was wir machen
  2. Wie Evaluieren wir am Ende
  3. 1o1 Meetings abmachen
  4. Tisch, Bildschirme Mikrofone
  5. Server zugang
  
### Linter
* Nur verwendbar mit Databricks access
* Versuchen lokal zu installieren

### LLM/RAG zum laufen bringen
* mit google colab hosten
* groq https://groq.com/
* auf alten cluster zugängen ausprobieren

### Wie evaluieren
* einfache Beispiele erstellen
* mit Sourcegraph beispiele finden

### Welche Daten in RAG?

## Next steps
- [ ] Meeting mit Martin absagen
- [ ] Julius Linter anschauen, ggf lokal zum laufen bringen
- [ ] Alle die Lust haben: LLM zum laufen bringen
- [ ] Johanna, Conrad: Daten für RAG
- [ ] Elena, Smilla und allen den langweilig ist: Daten, Daten, Daten

# Biweekly 12.11.2024
## Attendees

- [x] @juliuspor
- [x] @sm1lla
- [x] @joh-dah
- [x] @elenagensch
- [x] @cdfhalle (zu späääät)

## Notes

- recap vom meeting mit martin

1. anfangen mit RAG Approach rumzuexperimentieren
2. Databricks Linter anschauen
3. Promt engineering experimente und auswertung   

## Next steps
- [ ] Julius Linter anschauen
- [ ] Johanna Tabelle für experimente erstellen
- [ ] Chris zu unseren meetings einladen
- [ ] Alle: Promt engineering und Rag approach

# Meeting mit Jakob 07.11.2024
## Attendees

- [ ] @juliuspor
- [x] @sm1lla
- [x] @joh-dah
- [ ] @elenagensch
- [x] @cdfhalle
- [x] Jakob

      
  

### 2 Probleme
- neuer Code wird geschrieben, nicht alles aus dem Internet funktioniert
  - Vorteil: sind oft in Databricks Editor, der Vorschläge machen kann und lernen gerade erst
- Legacy Code 
  - schwieriger zu migrieren
  - eher in IDE, nicht Notebook in Databricks Editor
  - geht oft an Platform Team, dass nicht selbst den Code geschrieben hat, die Leute sind nicht mehr da
  - diese Leute sind wichtiger für Databricks (da ist das money)

### Was gibt es schon?
- Linter, der sagt, wenn etwas nicht kompatibel ist (gibt es aber nur in Python)
- in Notebook kann dann Databricks Assistant mache Probleme schon fixen
  - Jakob hat bei allen API call ausprobiert ob das Databricks LLM die Probleme fixen kann, ca 50% ging sofort, manchmal noch mehrmals nachfragen
  - er gibt uns ein Dokument, in dem er das festgehalten hat
  - promt für LLM ist hier ist die Zelle und die Fehlermeldung
  - Databricks Assistant ist einfaches LLM (GPT oder Llama)
    
### Welche Verbesserung würde Databricks bzw. den Kunden helfen?
- bessere Integration
  - Migration geht einfach in kleinem Notebook aber nicht so einfach in größerem Projekt
  - wär also cool, etwas zu haben, was man auch in der IDE nutzen kann
  - die meisten Projekte sind ein Workflow (Liste von Jobs), da wäre es gut, wenn man da gleich wüsste, ob der kompatibel ist oder nicht ohne ihn auszuprobieren und bestenfalls dann auch gleich Veränderungsvorschläge
- statt generischem LLM, dass nicht so viel Wissen über den spezifischen Migration Prozess hat, wäre spezifischere Lösung super (der Databricks Assistant kann zB nicht alle Probleme fixen
- am besten auch noch Confidence einschätzen
  - wie confident ist das LLM mit den Änderungsvorschlägen
  - manchmal gibt es Sachen, die man gar nicht migrieren kann, da sollte man dann auch confident sagen können, dass es nicht funktioniert

### Fazit 
- fertiges Produkt etc nicht das Ziel, aber ein Konzept davon haben, wie das am Ende in den Workflow integriert (User Story im Kopf haben)

### Weiteres
- Jakob hat uns auch ein pdf geschickt, in dem typische Probleme bei der Migration und potenzielle Fixes aufgelistet werden
  
# Weekly mit Martin und Jakob 07.11
## Attendees
- [x] @juliuspor
- [x] @sm1lla
- [x] @joh-dah
- [x] @elenagensch
- [x] @cdfhalle
- [x] Martin
- [ ] Chris
- [x] Jakob

## Data
Martin **Liste open source projekte:**
quinn	Yes, updated	38822
sparkaid		31788
findspark		19164
sparknlp		10996
sparkmeasure		10044
sparkdl		7784
geospark		5961
joblibspark		2643
pysparkling		2127
spark_tensorflow_distributor		941
sparknlp_jsl		834
spark_df_profiling		800
pyspark_test		605
sparkxgb		213
handyspark		205
geomesa_pyspark		150
labelspark		71
sparkocr		43
spark_sklearn		9
pyspark2pmml		4

- zu den Repos:
  -  ML algorithmen gehen noch gar nciht mit spark connect,
  -  xjboost resourece editor und pytorch spark distributor (wie viele nodes muss ich), benutzt classic apis ohne dass es sinn ergibt
- Jakob 3 Jahre Product Manager, Applikationen umbauen, wenn APIs nicht mehr verfuegbar fuer KUnden, 
# Biweekly 07.11.2024
## Attendees

- [x] @juliuspor
- [x] @sm1lla
- [x] @joh-dah
- [x] @elenagensch
- [x] @cdfhalle 

## Aproaches
check presentation slides 
- older approaches: Tools: Adapter/Wrapper (sehr statisch), statistische Methoden (overfitting) oder haendisches Mapping
- LLMs kritische Stellen markieren oder Code refactoring
- Amazon: will ich Tool was alles schreibt oder in den Prozess integriert werden, Beispiel von Agent Java8 zu Java17

- Problem bzw Frage COd Stueck fuer Stueck migrieren oder CodePlan

Synopsis Table: bewertet man in einem Loesungsansatz verschiedene Modelle oder grober: recent reearch fokus auf LLM

Entscheidung Wrapper oder CLients selbst migrieren, 
was gebe ich als kontext rein, wie interagieren mit dem Tool(z.B linter-based approach, scan des repos, PR vorschlag, oder pair programming AI assistant), wie kann man weiteres knowledge reinbringen, 

Prototyping auf kleines stueck code
Folie: Type of Tool hinzufuegen

## Next steps
- [ ] Tisch fragen
## Presentation: 

Approaches Ansaetze: Code Wrapper, Individual Migration: fuer uns Richtung LLM interessant, siehe genaue aproaches in Presentation

Martins Kommentare:
- UCX hat Linter fuer Migration gebaut, teilweise opensource (UCX, unity catalog migration tool): https://github.com/databrickslabs/ucx/blob/main/src/databricks/labs/ucx/source_code/linters/spark_connect.py 
- Open source LLMs probieren? Martin: LLAMA & friends sind sehr gut: also auf jeden Fall mal ausprobieren
- keine AWS credits, deswegen ist es schwierig Zugang zu Databricks
- pydequ: Zugriff auf JVM (geht nicht in spark connect), es gibt kein replacement, Blog-Artikel: was ist mein client code in python und was ist mein backend code in scala

# Biweekly 07.11.2024
## Attendees

- [x] @juliuspor
- [x] @sm1lla
- [x] @joh-dah
- [x] @elenagensch
- [x] @cdfhalle 

## Aproaches
check presentation slides 
- older approaches: Tools: Adapter/Wrapper (sehr statisch), statistische Methoden (overfitting) oder haendisches Mapping
- LLMs kritische Stellen markieren oder Code refactoring
- Amazon: will ich Tool was alles schreibt oder in den Prozess integriert werden, Beispiel von Agent Java8 zu Java17

- Problem bzw Frage COd Stueck fuer Stueck migrieren oder CodePlan

Synopsis Table: bewertet man in einem Loesungsansatz verschiedene Modelle oder grober: recent reearch fokus auf LLM

Entscheidung Wrapper oder CLients selbst migrieren, 
was gebe ich als kontext rein, wie interagieren mit dem Tool(z.B linter-based approach, scan des repos, PR vorschlag, oder pair programming AI assistant), wie kann man weiteres knowledge reinbringen, 

Prototyping auf kleines stueck code
Folie: Type of Tool hinzufuegen

## Next steps
- [ ] Tisch fragen

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

