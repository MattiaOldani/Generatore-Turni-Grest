# TURNI ANIMATORI

# DATI
set Animatori;															# Animatori
set FasceOrarie;														# Fasce orarie
set Giorni;																# Giorni
param Disponibilita {Giorni, Animatori, FasceOrarie} binary;			# Disponibilita

# VARIABILI
var Turni {Giorni, Animatori, FasceOrarie} binary;						# Assegnamento [binaria]
var NumeroTurni {Animatori} integer;									# Numero di turni per animatore
var MassimoNumeroTurni integer;											# Massimo assegnamento
var MinimoNumeroTurni integer;											# Minimo assegnamento

# VINCOLI
# Presenza di 2 animatori per turno
subject to MinimoNumero {g in Giorni, fo in FasceOrarie}:
    sum {a in Animatori} Turni[g,a,fo] = 2;
# Definizione del numero di turni
subject to DefinizioneNumeroTurni {a in Animatori}:
    NumeroTurni[a] = sum {g in Giorni, fo in FasceOrarie} Turni[g,a,fo];
# Definizione del massimo numero di turni
subject to DefinizioneMassimoNumeroTurni {a in Animatori}:
    MassimoNumeroTurni >= NumeroTurni[a];
# Definizione del minimo numero di turni
subject to DefinizioneMinimoNumeroTurni {a in Animatori}:
    MinimoNumeroTurni <= NumeroTurni[a];
# Faccio turno solo se sono disponibile
subject to Dispo {g in Giorni, a in Animatori, fo in FasceOrarie}:
    Turni[g,a,fo] <= Disponibilita[g,a,fo];

# OBIETTIVO
# Minimizzare la differenza tra massimo e minimo numero di turni
minimize z : MassimoNumeroTurni - MinimoNumeroTurni;

##################################################

data;

set Animatori := Mattia Vittorio Riccardo;

set FasceOrarie := Pre Mattino Mensa Pomeriggio Post;

set Giorni := Lunedi Martedi Mercoledi Giovedi Venerdi;

param Disponibilita:	Pre Mattino Mensa Pomeriggio Post	:=
Lunedi		Mattia		1	1		0	  0			 1
Lunedi		Vittorio	0	1		1	  1			 1
Lunedi		Riccardo	1	1		1	  1			 1
Martedi 	Mattia		0	1		0	  1			 1
Martedi		Vittorio	1	0		1	  1			 1
Martedi		Riccardo	1	1		1	  1			 0
Mercoledi	Mattia		1	0		0	  1			 1
Mercoledi	Vittorio	1	1		1	  1			 1
Mercoledi	Riccardo	1	1		1	  0			 1
Giovedi		Mattia		1	1		0	  1			 1
Giovedi		Vittorio	1	0		1	  1			 1
Giovedi		Riccardo	0	1		1	  1			 0
Venerdi		Mattia		1	1		0	  1			 1
Venerdi		Vittorio	1	1		1	  0			 1
Venerdi		Riccardo	0	0		1 	  1			 1;

end;
