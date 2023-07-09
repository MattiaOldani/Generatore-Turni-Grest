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
subject to MinimoNumeroAnimatori {g in Giorni, fo in FasceOrarie : g <> 'Giovedi' and fo <> 'Mensa'}:
    sum {a in Animatori} Assegnamento[g,a,fo] = 2;
# Mensa del giovedi senza turno
subject to MensaGiovediNoTurno:
	sum {a in Animatori} Assegnamento['Giovedi',a,'Mensa'] = 0;
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
# Se faccio il pre allora faccio anche la mattina
subject to PreAlloraMattina {g in Giorni, a in Animatori}:
    Assegnamento[g,a,'Pre'] <= Assegnamento[g,a,'Mattino'];
# Se faccio il post allora faccio anche il pomeriggio
subject to PostAlloraPomeriggio {g in Giorni, a in Animatori}:
    Assegnamento[g,a,'Post'] <= Assegnamento[g,a,'Pomeriggio'];

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
Martedi 	Mattia		1	1		0	  1			 1
Martedi		Vittorio	1	0		1	  1			 1
Martedi		Riccardo	1	1		1	  1			 0
Mercoledi	Mattia		1	0		0	  1			 1
Mercoledi	Vittorio	1	1		1	  1			 1
Mercoledi	Riccardo	1	1		1	  0			 1
Giovedi		Mattia		1	1		0	  1			 1
Giovedi		Vittorio	1	0		1	  1			 1
Giovedi		Riccardo	1	1		1	  1			 0
Venerdi		Mattia		1	1		0	  1			 1
Venerdi		Vittorio	1	1		1	  0			 1
Venerdi		Riccardo	0	0		1 	  1			 1;

end;
