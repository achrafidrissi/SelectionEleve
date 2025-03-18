:- dynamic eleve/6.

% Critères prioritaires : Revenu familial
points_revenu(Revenu, Points) :-
    (Revenu =< 2000 -> Points is 2;
    Revenu =< 4000 -> Points is 1;
    Points is 0).

% Critères prioritaires : Proximité école
points_proximite(CodePostalEleve, CodePostalEcole, Points) :-
    (CodePostalEleve =:= CodePostalEcole -> Points is 3;
    abs(CodePostalEleve - CodePostalEcole) =:= 1 -> Points is 2;
    Points is 0).

% Critères complémentaires
points_famille_nombreuse(oui, 1.5).
points_famille_nombreuse(non, 0).

points_handicap(oui, 1.5).
points_handicap(non, 0).

% Calcul total du score
calculer_score(Nom, Revenu, CodePostalEleve, CodePostalEcole, FamilleNombreuse, Handicap, ScoreTotal) :-
    points_revenu(Revenu, PointsRevenu),
    points_proximite(CodePostalEleve, CodePostalEcole, PointsProximite),
    points_famille_nombreuse(FamilleNombreuse, PointsFamille),
    points_handicap(Handicap, PointsHandicap),
    ScoreTotal is PointsRevenu + PointsProximite + PointsFamille + PointsHandicap,
    assertz(eleve(Nom, Revenu, CodePostalEleve, FamilleNombreuse, Handicap, ScoreTotal)).

% Récupérer tous les élèves
liste_eleves(L) :-
    findall((NomStr, Score), 
            (eleve(Nom, _, _, _, _, Score), atom_string(Nom, NomStr)), 
            L).
