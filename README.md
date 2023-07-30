# Generatore turni grest

Questo "progetto" nasce dall'esigenza dei coordinatori del grest di Capralba di poter fare i turni degli animatori in modo rapido e senza perdite di tempo

## Workflow

### Prima fase

La prima fase è la __creazione del file `data.dat`__, un file che contiene le informazioni sulle __fasce orarie__ da coprire, i __giorni__ nei quali c'è il grest, gli __animatori__ che hanno dato la propria disponibilità e, appunto, le __disponibilità__ di ogni animatore

#### Compilazione del form

Ogni animatore compila un [form Wufoo](https://www.wufoo.com/) tra venerdì mattina e domenica pomeriggio, dove inserisce:
* __nome__: se presenti più nomi ne va inserito uno solo
* __cognome__
* __disponibilità__ per le seguenti fasce orarie:
  * pre (dalle 08:00 alle 08:45)
  * mensa (dalle 12:00 alle 13:30)
  * post (dalle 17:00 alle 18:00)

#### Creazione del file data.dat

Domenica sera, tramite gli script presenti nel package __`form`__, vengono effettuate delle richieste HTTP alle API fornite da Wufoo per scaricare le risposte date dagli animatori e popolare il file __`data.dat`__

### Seconda fase

La seconda fase è la __creazione del file `turni.pdf`__, che contiene appunto i turni che ogni animatore deve fare nella settimana di grest

Questa fase è la più lunga poichè richiede prima una fase di __creazione dei turni__, poi una fase di __formattazione dei risultati__, e infine una fase di __compilazione__ per la creazione del file `turni.pdf`

#### Creazione dei turni

Il file `data.dat` creato nella fase precedente viene dato in pasto al programma __`turni.mod`__, che viene compilato tramite __ampl__ da riga di comando

Questa operazione viene eseguita dagli script del package __`template`__, che poi catturano l'output di ampl e lo passano alla successiva fase di formattazione

Il risultato di questa operazione è una __matrice di assegnamento tridimensionale__, che indica, per ogni fascia oraria, quale animatore è presente e in quale giorno

Ogni settimana sono allocabili 28 animatori, due per ognuna delle tre fasce orarie giornaliere per cinque giorni, escluso il turno della mensa del giovedì

Se al form sono presenti meno di 28 risposte, viene aggiunto un vincolo al file `turni.mod` che obbliga ogni animatore a fare almeno un turno, mentre nel caso di superamento delle 28 risposte questo vincolo viene tolto per permettere ad ampl di arrivare ad una soluzione ammissibile

Il vincolo appena citato probabilmente è inutile se andiamo a vedere come è scritta la funzione obiettivo, ma inserirlo come bound su una variabile non ci va a modificare il tempo di esecuzione

#### Formattazione dei risultati

La matrice risultante dal programma `turni.mod` viene salvata, assieme ad altre informazioni, all'interno di una classe presente nel package __`utils`__

L'ultimo compito degli script del package `template` e della classe appena citata è quello di popolare il file __`template.typ`__, che contiene appunto il template base per la creazione della tabella dei turni

La tabella contiene tre righe, una per ogni fascia oraria, e cinque colonne, una per ogni giorno di grest

#### Compilazione

Il file `template.typ` viene compilato tramite [__typst__](https://github.com/typst/typst) per generare il file __`turni.pdf`__

Viene preferito il formato `typ` a quello `md` per la sua semplicità e facilità nella compilazione per generare il file pdf dei turni

### Terza fase

La terza e ultima fase è l'__invio__, tramite bot telegram, dei turni generati alla fase precedente in un canale privato

Mattia oppure Vittorio, dipende chi legge il messaggio per primo, salverà poi il file e lo inoltrerà nel gruppo con tutti gli animatori

Questa fase è la più semplice ed è gestita dagli script presenti nel package __`telegram`__, che inviano, oltre al pdf dei turni, anche il numero di turni che ogni animatore deve fare durante la settimana

## Docker

Nel repository è presente un file __Docker__, che permette l'esecuzione di tutto il workflow su qualsiasi macchina si voglia utilizzare

Ogni volta che il repository viene modificato viene invocato lo script __`build.sh`__, che crea la nuova immagine Docker e la pusha su [Docker Hub](https://hub.docker.com/)

Per runnare poi l'immagine creata viene invocato lo script __`start.sh`__
