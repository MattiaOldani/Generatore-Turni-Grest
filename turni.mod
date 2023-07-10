# TURNI ANIMATORI

# DATI
set Animatori;															# Animatori
set FasceOrarie;														# Fasce orarie
set Giorni;																# Giorni
param Disponibilita {Giorni, Animatori, FasceOrarie} binary;			# Disponibilita

# VARIABILI
var Assegnamento {Giorni, Animatori, FasceOrarie} binary;				# Assegnamento
var NumeroTurni {Animatori} integer;									# Numero di turni per animatore
var MassimoNumeroTurni integer;											# Massimo assegnamento
var MinimoNumeroTurni integer;											# Minimo assegnamento

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

##################################################

data;

set Animatori := Mattia Vittorio Riccardo Matteo Davide Sam;

set FasceOrarie := 01_Pre 02_Mensa 03_Post;

set Giorni := 01_Lunedi 02_Martedi 03_Mercoledi 04_Giovedi 05_Venerdi;

param Disponibilita:	    01_Pre 02_Mensa 03_Post	:=
01_Lunedi		Mattia		1      1		0
01_Lunedi		Vittorio	0      1		1
01_Lunedi		Riccardo	1      1		1
01_Lunedi		Matteo  	1      1		1
01_Lunedi       Davide      1      1        1
01_Lunedi       Sam         1      1        1
02_Martedi 	    Mattia		1      1		0
02_Martedi		Vittorio	1      1		1
02_Martedi		Riccardo	1      1		1
02_Martedi		Matteo  	1      1		1
02_Martedi      Davide      1      1        1
02_Martedi      Sam         1      1        1
03_Mercoledi	Mattia		1      1		0
03_Mercoledi	Vittorio	1      1		1
03_Mercoledi	Riccardo	1      1		1
03_Mercoledi	Matteo  	1      1		1
03_Mercoledi    Davide      1      1        1
03_Mercoledi    Sam         1      1        1
04_Giovedi		Mattia		1      1		0
04_Giovedi		Vittorio	0      1		1
04_Giovedi		Riccardo	1      1		1
04_Giovedi		Matteo  	1      1		1
04_Giovedi      Davide      1      1        1
04_Giovedi      Sam         1      1        1
05_Venerdi		Mattia		1      1		0
05_Venerdi		Vittorio	1      1		1
05_Venerdi		Riccardo	0      1		1
05_Venerdi		Matteo  	1      1		1
05_Venerdi      Davide      1      1        1
05_Venerdi      Sam         1      1        1;

end;
