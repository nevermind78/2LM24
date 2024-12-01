import streamlit as st
import pandas as pd
import os 
import plotly.express as px
st.set_page_config(page_title="Notes 2LM", page_icon=":bar_chart:")
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

csv_file_path = st.secrets['csv_file_path']
# CSS pour cacher l'icône de GitHub
st.markdown(
    """
    <style>
    .stApp .main-header a {
        display: none !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)
#csv_file_path ='notes.csv'
# Chargement du fichier CSV en nettoyant les espaces dans la colonne Email
df = pd.read_csv(csv_file_path, delimiter=",", converters={"Email": lambda x: x.strip()})

# Titre de l'application
st.title("NOTES DS Probabilité")
st.header("2LM A.U 2024-2025")

def categorize_notes(note):
    if note < 10:
        return "Insuffisant (<10)"
    elif 10 <= note < 12:
        return "Passable (10-12)"

    elif 12 <= note < 14:
        return "Assez Bien (12-14)"

    elif 14<= note < 16:
        return "Bien(12-14)"
    
    else:
        return "Très bien (>16)"

# Vérification si l'email existe dans le fichier CSV
#df["TP"] = pd.to_numeric(df["TP"], errors='coerce').fillna(0)
df["DS"] = pd.to_numeric(df["DS"], errors='coerce').fillna(0)
df["Catégorie de notes DS"] = df["DS"].apply(categorize_notes)
#df["Catégorie de notes TP"] = df["TP"].apply(categorize_notes)

# CSS pour personnaliser la taille de la police
st.markdown(
    """
    <style>
    .custom-text-input label {
        font-size: 28px !important;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True
)

# Champ de saisie pour l'email de l'étudiant avec une classe personnalisée
email = st.text_input("Saisissez votre email", key="email_input", label_visibility="visible", placeholder="Exemple: nom@example.com")
email= email.lower()
# Appliquer la classe personnalisée pour changer le style
st.markdown(
    """
    <script>
    const emailField = document.querySelector('input[id="email_input"]');
    if (emailField) {
        emailField.classList.add('custom-text-input');
    }
    </script>
    """, unsafe_allow_html=True
)



if email:
    if email in df["Email"].values:
        # Récupération des informations de l'étudiant correspondant à l'email
        etudiant = df[df["Email"] == email]
        nom = etudiant["Name"].values[0]
        groupe = etudiant["GR"].values[0]
        noteDS = etudiant["DS"].values[0]
        #noteTP = etudiant["TP"].values[0]
        # Création d'un dictionnaire contenant les informations de l'étudiant
        etudiant_info = {
                        "Nom": nom,
                        "Groupe": groupe,
                        "DS": noteDS,
                    }
        res = pd.DataFrame.from_dict(etudiant_info, orient='index', columns=['Résultats'])
        res['Résultats'] = res['Résultats'].astype(str)
        # Affichage des informations de l'étudiant dans un tableau
        st.subheader("Résultats de l'étudiant")
        a,b,c = st.columns(3)
        with b:
            st.write(res, unsafe_allow_html=True)
        if noteDS==-1:
            st.warning("-1 : abscent au DS si vous ne régler pas votre situation la note finale au ds sera 0")
        # Calculer les statistiques des notes pour le pie chart
    else:
        st.error("Email non trouvé")

# Bloc avec la possibilité de cacher/afficher les statistiques des groupes
with st.expander("Afficher/Masquer les statistiques des groupes"):
    # Champ de sélection pour choisir un groupe
    groupes = df["GR"].unique()
    groupes.sort()
    groupe_selectionne = st.selectbox("Choisissez un groupe", options=groupes)

    if groupe_selectionne:
        # Filtrer les données pour le groupe sélectionné
        df_groupe = df[df["GR"] == groupe_selectionne]
        # Statistiques du groupe
        moyenne = df_groupe["DS"].mean()
        variance = df_groupe["DS"].var()
        ecart_type = df_groupe["DS"].std()

        # Affichage des statistiques
        col1, col2 = st.columns(2)
        with col2:
            # Boxplot
            fig_box = px.box(df_groupe, y="DS", points="all", title="Boxplot des notes DS")
            st.plotly_chart(fig_box, use_container_width=True)
            st.write(f"- **Moyenne** : {moyenne:.2f}")
            st.write(f"- **Variance** : {variance:.2f}")
            st.write(f"- **Écart-type** : {ecart_type:.2f}")

        # Graphiques
        with col1:
            fig_pie = px.pie(df_groupe, names="Catégorie de notes DS", title="Répartition des catégories")
            st.plotly_chart(fig_pie, use_container_width=True)
            fig_hist = px.histogram(
            df_groupe,
            x="DS",
            nbins=10,  # Vous pouvez ajuster le nombre de bins
            title="Histogramme des notes DS",
            labels={"DS": "Notes DS"},
            color_discrete_sequence=["#636EFA"],
            )
            fig_hist.update_layout(bargap=0.2)  # Ajuste l'espace entre les barres
            st.plotly_chart(fig_hist, use_container_width=True)


            
            
