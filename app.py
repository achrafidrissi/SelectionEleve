import streamlit as st
from pyswip import Prolog

# Initialiser Prolog
prolog = Prolog()
prolog.consult("selection_eleves.pl")

# Titre de l'application
st.title("🎓 Système de Sélection des Élèves")

# 📝 Formulaire pour ajouter un élève
st.header("Ajouter un élève")
nom = st.text_input("Nom de l'élève")
revenu = st.number_input("Revenu familial", min_value=0, step=500)
code_postal_eleve = st.number_input("Code postal élève", min_value=1000, step=1)
code_postal_ecole = st.number_input("Code postal école", min_value=1000, step=1)
famille_nombreuse = st.selectbox("Famille nombreuse", ["oui", "non"])
handicap = st.selectbox("Handicap", ["oui", "non"])

if st.button("Ajouter l'élève"):
    query = f"calculer_score('{nom}', {revenu}, {code_postal_eleve}, {code_postal_ecole}, '{famille_nombreuse}', '{handicap}', ScoreTotal)"
    result = list(prolog.query(query))
    if result:
        st.success(f"Élève ajouté avec un score de {result[0]['ScoreTotal']}")

# 📜 Affichage des élèves triés
st.header("Liste des élèves triés")
if st.button("Afficher la liste des élèves"):
    query = "liste_eleves(L)"
    result = list(prolog.query(query))

    if result and "L" in result[0]:
        eleves = result[0]["L"]
        
        # Vérification et nettoyage des données
        cleaned_eleves = []
        for elem in eleves:
            # Supprimer les caractères parasites (",(" et ")") si nécessaire
            elem = elem.strip(",()")
            parts = elem.split(", ")
            
            if len(parts) == 2:
                nom = parts[0].strip("'")  # S'assurer que le nom est une chaîne
                score = float(parts[1])  # Convertir le score en nombre
                cleaned_eleves.append((nom, score))

        # Trier par score décroissant
        cleaned_eleves.sort(key=lambda x: x[1], reverse=True)

        for nom, score in cleaned_eleves:
            st.write(f"📌 {nom} - Score: {score}")
    else:
        st.warning("Aucun élève enregistré.")

