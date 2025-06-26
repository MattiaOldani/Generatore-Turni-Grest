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
  - `ANIMATORS_PRE`: numero di animatori al pre;
  - `ANIMATORS_POST`: numero di animatori al post;
  - `ANIMATORS_LUNCH`: numero di animatori in mensa;
  - `ANIMATORS_SHARE_LUNCH`: numero di animatori al pranzo condiviso;
  - `MAX_NUMBER_DAILY_SLOTS`: massimo numero di turni giornalieri;
  - `MAX_REPETITION_SAME_SLOT`: massima ripetizione dello stesso turno;
- per quanto riguarda il package `telegram`:
  - `CHANNEL_ID`: canale nel quale verranno inviati i risultati del workflow;
  - `TELEGRAM_API_KEY`: token fornito da telegram per accedere al bot.

### Prima fase

La prima fase è la __creazione del file `data.dat`__, un file che contiene le informazioni su:
- __fasce orarie__ da coprire;
- __giorni__ nei quali c'è il Grest;
- __animatori__ presenti per quella settimana;
- __disponibilità__ e __necessità__ degli stessi;
- __numero di animatori per turno__;
- __massima ripetizione dello stesso turno__;
- __massimo numero di turni giornalieri__.

#### Compilazione del form

Ogni animatore compila un [form Tally](https://tally.so) tra venerdì mattina e domenica pomeriggio, dove inserisce:
* __nome__;
* __cognome__;
* __disponibilità__ e __necessità__ per le seguenti fasce orarie:
  * pre (dalle 08:00 alle 08:45);
  * mensa (dalle 12:00 alle 13:30);
  * post (dalle 17:00 alle 18:00).

#### Creazione del file data.dat

Domenica sera, tramite gli script presenti nel package __`form`__, vengono effettuate delle richieste HTTP alle API fornite da Tally per scaricare le risposte date dagli animatori e popolare il file __`data.dat`__.

### Seconda fase

La seconda fase è la __creazione del file `turni.pdf`__, il quale conterrà i turni che ogni animatore dovrà svolgere nell nella settimana di Grest.

Questa fase è la più lunga poiché richiede una prima fase di __creazione dei turni__, poi una seconda di __formattazione dei risultati__ e infine una di __compilazione__ per la creazione del file `turni.pdf`.

#### Creazione dei turni

Il file `data.dat`, creato nella fase precedente, viene dato in pasto al programma __`turni.mod`__, che viene compilato tramite __ampl__ da riga di comando.

Questa operazione viene eseguita dagli script del package __`template`__, che successivamente catturano l'output di ampl e lo passano alla successiva fase di formattazione.

Il risultato di questa operazione è una __matrice di assegnamento tridimensionale__, che indica, per ogni fascia oraria, quale animatore è presente e in quale giorno.

#### Formattazione dei risultati

La matrice risultante dal programma `turni.mod` viene salvata, assieme ad altre informazioni, all'interno di una classe presente nel package __`utils`__.

L'ultimo compito degli script del package `template` e della classe appena citata è quello di popolare il file __`template.typ`__, che contiene il template base per la creazione della tabella dei turni.

La tabella contiene tre righe, una per ogni fascia oraria, e cinque colonne, una per ogni giorno di Grest.

#### Compilazione

Il file `template.typ` viene compilato tramite [__typst__](https://github.com/typst/typst) per generare il file __`turni.pdf`__.

Viene preferito il formato `typ` a quello `md` per la sua semplicità e facilità nella compilazione per generare il file PDF dei turni.

### Terza fase

La terza e ultima fase è l'__invio__, tramite bot Telegram, dei turni generati alla fase precedente in un canale privato.

Questa fase è la più semplice ed è gestita dagli script presenti nel package __`telegram`__, che inviano, oltre al PDF dei turni, anche il numero di turni che ogni animatore deve fare durante la settimana.
