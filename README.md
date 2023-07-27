# Generatore turni grest

Questo "progetto" nasce dall'esigenza dei coordinatori del grest di Capralba di poter fare i turni degli animatori in modo rapido e senza perdite di tempo

Sicuramente ci sono moltissime imperfezioni, soprattutto per quanto riguarda la gestione dei programmi python e dei suoi package, però per ora funziona, quindi si gode

Sicuramente un giorno questo progetto verrà sistemato a dovere, sia per la parte di python, sia per la parte di Docker, che però non è stata ancora inserita

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

Domenica sera lo script __`form.py`__ effettua delle richieste HTTP alle API fornite da Wufoo per scaricare le risposte date dagli animatori e popolare il file __`data.dat`__

### Seconda fase

La seconda fase è la __creazione del file `turni.pdf`__, che contiene appunto i turni che ogni animatore deve fare nella settimana di grest

Questa fase è la più lunga poichè richiede prima una fase di __creazione dei turni__, poi una fase di __formattazione dei risultati__, e infine una fase di __compilazione__ per la creazione del file `turni.pdf`

#### Creazione dei turni

Il file `data.dat` creato nella fase precedente viene dato in pasto al programma __`turni.mod`__, che viene compilato tramite __ampl__ da riga di comando

Questa operazione viene eseguita all'interno dello script __`template.py`__, per poter catturare l'output di ampl e per poter poi passare alla successiva fase di formattazione

Il risultato di questa operazione è una __matrice di assegnamento tridimensionale__, che indica, per ogni fascia oraria, quale animatore è presente e in quale giorno

#### Formattazione dei risultati

Sempre tramite lo script `template.py` la matrice risultante dal programma `turni.mod` viene salvata, assieme ad altre informazioni, all'interno di una classe presente nel file __`turns.py`__

La parte finale dello script utilizza la classe appena citata per popolare il file __`template.typ`__, che contiene appunto il template base per la creazione della tabella dei turni

La tabella contiene tre righe, una per ogni fascia oraria, e cinque colonne, una per ogni giorno di grest

#### Compilazione

Il file `template.typ` viene compilato tramite [__typst__](https://github.com/typst/typst) da riga di comando per generare il file __`turni.pdf`__

Viene preferito il formato `typ` a quello `md` per la sua semplicità e facilità nella compilazione per generare il file pdf dei turni

### Terza fase

La terza e ultima fase è l'__invio__, tramite bot telegram, dei turni generati alla fase precedente in un canale privato

Mattia oppure Vittorio, dipende chi legge il messaggio per primo, salverà poi il file e lo inoltrerà nel gruppo con tutti gli animatori

Questa fase è la più semplice ed è gestita da poche righe di codice presenti nel file __`telegram.py`__
