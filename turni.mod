# TURNI ANIMATORI

# DATI
# Insieme delle fasce orarie da coprire
set FasceOrarie;
# Insieme dei giorni di grest
set Giorni;
# Insieme degli animatori che hanno risposto al form
set Animatori;
# Disponibilità di ogni animatore nei vari giorni e nelle varie fasce orarie
param Disponibilita {Giorni, Animatori, FasceOrarie} binary;

# VARIABILI
# Assegnamento di ogni animatore ad una fascia oraria in un certo giorno
var Assegnamento {Giorni, Animatori, FasceOrarie} binary;
# Numero di turni settimanali per animatore
var NumeroTurni {Animatori} integer;
# Massimo numero di turni fatti da un animatore
var MassimoNumeroTurni integer;
# Minimo numero di turni fatti da un animatore
var MinimoNumeroTurni integer;

# VINCOLI
# Presenza di 2 animatori per turno, esclusa la mensa del giovedi
subject to MinimoNumeroAnimatori {g in Giorni, fo in FasceOrarie : g <> '04_Giovedi' or fo <> '02_Mensa'}:
    sum {a in Animatori} Assegnamento[g,a,fo] = 2;
subject to MensaGiovediNoTurno:
	sum {a in Animatori} Assegnamento['04_Giovedi',a,'02_Mensa'] = 0;
# Definizione del numero di turni
subject to DefinizioneNumeroTurni {a in Animatori}:
    NumeroTurni[a] = sum {g in Giorni, fo in FasceOrarie} Assegnamento[g,a,fo];
# Definizione del massimo numero di turni
subject to DefinizioneMassimoNumeroTurni {a in Animatori}:
    MassimoNumeroTurni >= NumeroTurni[a];
# Definizione del minimo numero di turni
subject to DefinizioneMinimoNumeroTurni {a in Animatori}:
    MinimoNumeroTurni <= NumeroTurni[a];
# Faccio turno solo se sono disponibile
subject to Candidatura {g in Giorni, a in Animatori, fo in FasceOrarie}:
    Assegnamento[g,a,fo] <= Disponibilita[g,a,fo];
# Ogni animatore ripete al massimo 2 volte lo stesso turno
subject to MassimaRipetizionePerSettimana {a in Animatori, fo in FasceOrarie}:
    sum {g in Giorni} Assegnamento[g,a,fo] <= 2;
# Ogni animatore può fare al massimo 1 turno al giorno
subject to MassimaRipetizionePerGiorno {a in Animatori, g in Giorni}:
    sum {fo in FasceOrarie} Assegnamento[g,a,fo] <= 1;

# OBIETTIVO
# Minimizzare la differenza tra massimo e minimo numero di turni
minimize z : MassimoNumeroTurni - MinimoNumeroTurni;

end;
