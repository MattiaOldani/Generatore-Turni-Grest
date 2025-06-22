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
# Necessità di ogni animatore nei vari giorni e nelle varie fasce orarie
param Necessita {Giorni, Animatori, FasceOrarie} binary;
# Se gli animatori hanno necessità di qualche turno
param HannoNecessita {Animatori} binary;
# Numero di animatori richiesti per il pre
param AnimatoriPre;
# Numero di animatori richiesti per il post
param AnimatoriPost;
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
# Turni fatti da animatori con necessità
var NumeriTurniNecessita {Animatori} integer >= 0;

# VINCOLI
# Presenza di <AnimatoriPre> animatori al pre
subject to NumeroAnimatoriPre {g in Giorni}:
    sum {a in Animatori} Assegnamento[g,a,'01_Pre'] = AnimatoriPre;
# Presenza di <AnimatoriPost> animatori al post
subject to NumeroAnimatoriPost {g in Giorni}:
    sum {a in Animatori} Assegnamento[g,a,'03_Post'] = AnimatoriPost;
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
    MassimoNumeroTurni >= (1 - HannoNecessita[a]) * NumeroTurni[a];
# Definizione del minimo numero di turni
subject to DefinizioneMinimoNumeroTurni {a in Animatori}:
    MinimoNumeroTurni <= NumeroTurni[a];
# Definizione del numero di turni di chi ha necessità
subject to DefinizioneNumeroTurniNecessita {a in Animatori}:
    NumeriTurniNecessita[a] = HannoNecessita[a] * (
        (sum {g1 in Giorni, fo1 in FasceOrarie} Assegnamento[g1,a,fo1])
        -
        (sum {g2 in Giorni, fo2 in FasceOrarie} Necessita[g2,a,fo2])
    );
# Non diamo turni a chi ha delle necessità
subject to PerdonoDivino:
    sum {a in Animatori} NumeriTurniNecessita[a] = 0;
# Se ho necessità devo essere messo in quel turno
subject to SoddisfareLeNecessita {g in Giorni, a in Animatori, fo in FasceOrarie : Necessita[g,a,fo] = 1}:
    Assegnamento[g,a,fo] = Necessita[g,a,fo];
# Faccio turno solo se sono disponibile
subject to Candidatura {g in Giorni, a in Animatori, fo in FasceOrarie}:
    Assegnamento[g,a,fo] <= Disponibilita[g,a,fo] + Necessita[g,a,fo];
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
