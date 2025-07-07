# Generatore turni Grest

Questo progetto nasce dall'esigenza dei coordinatori del Grest di Capralba di poter organizzare i turni degli animatori in modo rapido e senza perdite di tempo.

Sto scherzando, ho fatto questo perché sono tremendamente pigro.

## Workflow

### Fase preliminare

La fase preliminare di tutto il workflow è il __setup dell'environment__, che viene effettuato modificando il file __`environment.json`__.

Devono essere inserite le seguenti variabili d'ambiente:
- per quanto riguarda il package `form`:
  - `FORM_API_KEY`: token fornito da Tally per accedere alle API;
  - `FORM_ENDPOINT`: link al quale trovare le risposte del form;
  - `PRE_ANIMATORS`: numero di animatori al pre;
  - `POST_ANIMATORS`: numero di animatori al post;
  - `LUNCH_ANIMATORS`: numero di animatori in mensa;
  - `SHARE_LUNCH_ANIMATORS`: numero di animatori al pranzo condiviso;
  - `MAX_NUMBER_DAILY_SLOTS`: massimo numero di turni giornalieri;
  - `MAX_REPETITION_SAME_SLOT`: massima ripetizione dello stesso turno;
- per quanto riguarda il package `telegram`:
  - `CHANNEL_ID`: canale nel quale verranno inviati i risultati del workflow;
  - `TELEGRAM_API_KEY`: token fornito da telegram per accedere al bot.

Nel repository è presente anche il file `turni_obbligatori.txt`, che durante le settimane viene popolato con i nomi degli animatori che devono fare dei turni obbligatori.

### Prima fase

La prima fase è la __popolazione del modello__ di PLI che permette di calcolare l'assegnamento degli __animatori__ nelle varia __fasce orarie__ dei vari __giorni__ di grest.

#### Compilazione del form

Ogni animatore compila un [form Tally](https://tally.so) tra venerdì mattina e domenica pomeriggio, dove inserisce:
* __nome__;
* __cognome__;
* __disponibilità__ e __necessità__ per le seguenti fasce orarie:
  * __pre__ (dalle 08:00 alle 08:45);
  * __mensa__ (dalle 12:00 alle 13:30);
  * __post__ (dalle 17:00 alle 18:00).

#### Popolamento del modello

Domenica sera vengono effettuate delle richieste HTTP alle API fornite da Tally per scaricare le risposte date dagli animatori e popolare il modello di PLI, usando anche i dati inseriti nel file `environment.json`.

### Seconda fase

La seconda fase è la __creazione del file `turni.pdf`__, il quale conterrà i turni che ogni animatore dovrà svolgere nell nella settimana di Grest.

#### Calcolo dei turni

Il modello precedentemente creato viene passato ad un __SAT-solver__ che calcola l'assegnamento migliore degli animatori. Quest'ultimo è una __matrice di assegnamento tridimensionale__, che indica, per ogni fascia oraria, quale animatore è presente e in quale giorno.

#### Formattazione dei risultati

La matrice risultante viene interrogata dagli script del package `template` per popolare il file __`template.typ`__, che contiene il template base per la creazione della tabella dei turni.

La tabella contiene tre righe, una per ogni fascia oraria, e cinque colonne, una per ogni giorno di Grest.

#### Compilazione

Il file `template.typ` viene compilato tramite [__typst__](https://github.com/typst/typst) per generare il file __`turni.pdf`__.

Viene preferito il formato `typ` a quello `md` per la sua semplicità e facilità nella compilazione per generare il file PDF dei turni.

### Terza fase

La terza e ultima fase è l'__invio__, tramite bot Telegram, dei turni generati alla fase precedente in un canale privato.

Questa fase è la più semplice ed è gestita dagli script presenti nel package __`telegram`__, che inviano, oltre al PDF dei turni, anche il numero di turni che ogni animatore deve fare durante la settimana e gli animatori che la settimana successiva devono fare obbligatoriamente almeno un turno.
