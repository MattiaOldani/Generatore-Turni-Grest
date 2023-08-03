# Generatore turni Grest

Questo "progetto" nasce dall'esigenza dei coordinatori del Grest di Capralba di poter organizzare i turni degli animatori in modo rapido e senza perdite di tempo.

# Workflow

## Prima fase

La prima fase è la __creazione del file `data.dat`__, un file che contiene le informazioni su:
- __fasce orarie__ da coprire;
- __giorni__ nei quali c'è il Grest;
- __animatori__ presenti per quella settimana;
- __disponibilità__ degli stessi;
- __numero di animatori per turno__;
- __massima ripetizione dello stesso turno__;
- __massimo numero di turni giornalieri__.

### Compilazione del form

Ogni animatore compila un [form Wufoo](https://www.wufoo.com/) tra venerdì mattina e domenica pomeriggio, dove inserisce:
* __nome__;
* __cognome__;
* __disponibilità__ per le seguenti fasce orarie:
  * pre (dalle 08:00 alle 08:45);
  * mensa (dalle 12:00 alle 13:30);
  * post (dalle 17:00 alle 18:00).

### Creazione del file data.dat

Domenica sera, tramite gli script presenti nel package __`form`__, vengono effettuate delle richieste HTTP alle API fornite da Wufoo per scaricare le risposte date dagli animatori e popolare il file __`data.dat`__.

Il file __`form.py`__, presente nel package `form`, va modificato inserendo i seguenti campi:
- `ENDPOINT`: link al quale trovare le risposte del form;
- `FORM_API_KEY`: token fornito da Wufoo per accedere alle API;
- `ANIMATORS_PER_SLOT`: numero di animatori per turno;
- `MAX_REPETITION_SAME_SLOT`: massima ripetizione dello stesso turno;
- `MAX_NUMBER_DAILY_SLOTS`: massimo numero di turni giornalieri.

## Seconda fase

La seconda fase è la __creazione del file `turni.pdf`__, il quale conterrà i turni che ogni animatore dovrà svolgere nell nella settimana di Grest.

Questa fase è la più lunga poiché richiede una prima fase di __creazione dei turni__, poi una seconda di __formattazione dei risultati__ e infine una di __compilazione__ per la creazione del file `turni.pdf`.

### Creazione dei turni

Il file `data.dat`, creato nella fase precedente, viene dato in pasto al programma __`turni.mod`__, che viene compilato tramite __ampl__ da riga di comando.

Questa operazione viene eseguita dagli script del package __`template`__, che successivamente catturano l'output di ampl e lo passano alla successiva fase di formattazione.

Il risultato di questa operazione è una __matrice di assegnamento tridimensionale__, che indica, per ogni fascia oraria, quale animatore è presente e in quale giorno.

### Formattazione dei risultati

La matrice risultante dal programma `turni.mod` viene salvata, assieme ad altre informazioni, all'interno di una classe presente nel package __`utils`__.

L'ultimo compito degli script del package `template` e della classe appena citata è quello di popolare il file __`template.typ`__, che contiene il template base per la creazione della tabella dei turni.

La tabella contiene tre righe, una per ogni fascia oraria, e cinque colonne, una per ogni giorno di Grest.

### Compilazione

Il file `template.typ` viene compilato tramite [__typst__](https://github.com/typst/typst) per generare il file __`turni.pdf`__.

Viene preferito il formato `typ` a quello `md` per la sua semplicità e facilità nella compilazione per generare il file PDF dei turni.

## Terza fase

La terza e ultima fase è l'__invio__, tramite bot Telegram, dei turni generati alla fase precedente in un canale privato.

Questa fase è la più semplice ed è gestita dagli script presenti nel package __`telegram`__, che inviano, oltre al PDF dei turni, anche il numero di turni che ogni animatore deve fare durante la settimana.

Il file __`telegram.py`__, presente nel package `telegram`, va modificato inserendo i seguenti campi:
- `API_KEY`: token fornito da telegram per accedere al bot;
- `CHANNEL_ID`: canale nel quale verrano inviate le informazione scritte poco fa.

# Docker

Nel repository è presente un file __Docker__, che permette l'esecuzione di tutto il workflow su qualsiasi macchina si voglia utilizzare.

Prima di eseguire tutto il deploy è necessario settare le variabili dei package `form` e `telegram`.

## Build

Viene richiesta l'ultima versione upstream di __typst__ nella root del progetto, scaricabile tramite __`git`__ dal loro [repository](https://github.com/typst/typst).

Per creare l'immagine Docker invocare lo script __`build.sh`__, che la andrà poi a pushare su [Docker Hub](https://hub.docker.com/) in un repository privato.

Questo script va modificato inserendo le [proprie credenziali](https://docs.docker.com/engine/reference/commandline/login/) di Docker Hub per avere la propria versione di questa immagine sia in locale che su Docker Hub; se non si volesse eseguire il push in un proprio repository Docker Hub, rimuovere l'istruzione di `docker push`.

## Run

Per runnare l'immagine creata viene invocato lo script __`start.sh`__, anch'esso da modificare con le proprie credenziali.
