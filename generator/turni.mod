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
# Numero di animatori richiesti per pre e post
param AnimatoriPrePost;
# Numero di animatori richiesti per la mensa
param AnimatoriMensa;
# Numero di animatori richiesti al pranzo condiviso
param AnimatoriPranzoCondiviso;
# Massimo numero di ripetizioni dello stesso turno
param MassimaRipetizioneStessoTurno;
# Numero di turni che ogni animatore fa al massimo in un giorno
param MassimoNumeroTurniGiornalieri;

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
# Presenza di <AnimatoriPrePost> animatori a pre e post
subject to NumeroAnimatoriPrePost {g in Giorni, fo in FasceOrarie : fo = '01_Pre' or fo = '03_Post'}:
    sum {a in Animatori} Assegnamento[g,a,fo] = AnimatoriPrePost;
# Presenza di <AnimatoriMensa> animatori alla mensa
subject to NumeroAnimatoriMensa {g in Giorni : g <> '04_Giovedi'}:
    sum {a in Animatori} Assegnamento[g,a,'02_Mensa'] = AnimatoriMensa;
# Presenza di <AnimatoriPranzoCondiviso> animatori al pranzo condiviso
subject to NumeroAnimatoriPranzoCondiviso:
	sum {a in Animatori} Assegnamento['04_Giovedi',a,'02_Mensa'] = AnimatoriPranzoCondiviso;
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
# Ogni animatore ripete al massimo <MassimaRipetizioneStessoTurno> volte lo stesso turno
subject to MassimaRipetizionePerSettimana {a in Animatori, fo in FasceOrarie}:
    sum {g in Giorni} Assegnamento[g,a,fo] <= MassimaRipetizioneStessoTurno;
# Ogni animatore può fare al massimo <MassimoNumeroTurniGiornalieri> turni al giorno
subject to MassimaRipetizionePerGiorno {a in Animatori, g in Giorni}:
    sum {fo in FasceOrarie} Assegnamento[g,a,fo] <= MassimoNumeroTurniGiornalieri;

# OBIETTIVO
# Minimizzare la differenza tra massimo e minimo numero di turni
minimize z : MassimoNumeroTurni - MinimoNumeroTurni;

end;
