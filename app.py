import streamlit as st

st.set_page_config(page_title="Mes cours de maths - Terminale", page_icon="📚", layout="wide")

# --- Empêche les navigateurs (Chrome, etc.) de proposer/forcer une
# traduction automatique de la page (ex: "second degré" -> "deuxième degré") ---
st.markdown(
    """
    <meta name="google" content="notranslate">
    <script>
        document.documentElement.setAttribute('translate', 'no');
        document.documentElement.classList.add('notranslate');
    </script>
    """,
    unsafe_allow_html=True
)

# ============================================================
# CONFIGURATION — c'est ICI que tu ajoutes tes fichiers
# ============================================================

# URL de base de ton site GitHub Pages (racine du dépôt)
BASE_URL = "https://maelmoignet-pixel.github.io/cours-terminal"

# Un chapitre = un dossier sur GitHub Pages
CHAPITRES = {
    "Suites numériques": {
        "dossier": "suites",
        "icone": "🔢",
        "description": "Modes de génération, sens de variation, suites arithmétiques et géométriques, raisonnement par récurrence, limites.",
        "cours_fichier": "suites.html",
    },
    # Ajoute tes futurs chapitres ici, en suivant le même modèle :
    # "Probabilités : expériences répétées": {
    #     "dossier": "probabilites",
    #     "icone": "🎲",
    #     "description": "Répétition d'expériences indépendantes, schéma de Bernoulli.",
    #     "cours_fichier": "probabilites.html",
    # },
}

# Les 4 catégories de documents proposées sous chaque chapitre
# (en plus du cours lui-même)
CATEGORIES = {
    "eval_2025": {"label": "Évaluations 2025", "icone": "📝"},
    "ds_2025": {"label": "DS 2025", "icone": "🧪"},
    "eval_2026": {"label": "Évaluations 2026", "icone": "📝"},
    "ds_2026": {"label": "DS 2026", "icone": "🧪"},
}

# Les fichiers déposés dans chaque catégorie, PAR CHAPITRE.
# Structure : FICHIERS[dossier_chapitre][categorie] = liste de documents
# Chaque document : {"nom": "Nom affiché", "fichier": "nom-du-fichier.html"}
#
# Pour ajouter un nouveau DS ou une nouvelle éval : ajoute une ligne
# dans la liste correspondante. Le fichier html correspondant doit être
# déposé dans le dossier du chapitre sur GitHub Pages, par exemple :
#   cours-terminal/suites/eval-2025-1.html
FICHIERS = {
    "suites": {
        "eval_2025": [],
        "ds_2025": [],
        "eval_2026": [],
        "ds_2026": [],
    },
}


# Icône affichée sur le bouton selon le type de fichier
def icone_fichier(nom_fichier):
    return "📄" if nom_fichier.lower().endswith(".pdf") else "🌐"


def label_ouvrir(nom_fichier):
    return "Ouvrir le PDF ➜" if nom_fichier.lower().endswith(".pdf") else "Ouvrir ➜"


# ============================================================
# NAVIGATION (état de session)
# ============================================================

if "view" not in st.session_state:
    st.session_state.view = "accueil"      # "accueil" | "chapitre" | "categorie"
if "chapitre_courant" not in st.session_state:
    st.session_state.chapitre_courant = None
if "categorie_courante" not in st.session_state:
    st.session_state.categorie_courante = None


def aller_accueil():
    st.session_state.view = "accueil"
    st.session_state.chapitre_courant = None
    st.session_state.categorie_courante = None


def aller_chapitre(nom_chapitre):
    st.session_state.view = "chapitre"
    st.session_state.chapitre_courant = nom_chapitre
    st.session_state.categorie_courante = None


def aller_categorie(nom_chapitre, cle_categorie):
    st.session_state.view = "categorie"
    st.session_state.chapitre_courant = nom_chapitre
    st.session_state.categorie_courante = cle_categorie


# ============================================================
# EN-TÊTE (toujours visible)
# ============================================================

st.markdown(
    """
    <div style="text-align: center; padding: 10px 0 10px 0;">
        <h1 style="margin-bottom: 0;">📚 Mes cours de mathématiques</h1>
        <p style="font-size: 18px; color: #4a4a4a; margin-top: 5px;">
            par <strong>Maël Moignet</strong>
        </p>
        <p style="font-size: 15px; color: #7a7a7a; margin-top: -8px;">
            🎓 Lycée Naval de Brest — Terminale
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# --- Fil d'Ariane + bouton Accueil ---
col_home, col_fil = st.columns([1, 5])
with col_home:
    st.button("🏠 Accueil", on_click=aller_accueil, use_container_width=True)
with col_fil:
    fil = "Accueil"
    if st.session_state.chapitre_courant:
        fil += f" › {st.session_state.chapitre_courant}"
    if st.session_state.categorie_courante:
        fil += f" › {CATEGORIES[st.session_state.categorie_courante]['label']}"
    st.markdown(f"<div style='padding-top:10px; color:#666;'>{fil}</div>", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ============================================================
# PLAN DU SITE (barre latérale, toujours visible)
# ============================================================

with st.sidebar:
    st.markdown("## 🗺️ Plan du site")
    st.button("🏠 Accueil", key="sb_accueil", on_click=aller_accueil, use_container_width=True)
    st.markdown("---")
    for nom_chapitre, infos in CHAPITRES.items():
        with st.expander(f"{infos['icone']} {nom_chapitre}", expanded=(st.session_state.chapitre_courant == nom_chapitre)):
            st.button(
                "📖 Cours",
                key=f"sb_cours_{infos['dossier']}",
                on_click=lambda n=nom_chapitre: aller_chapitre(n),
                use_container_width=True,
            )
            for cle_cat, cat_infos in CATEGORIES.items():
                st.button(
                    f"{cat_infos['icone']} {cat_infos['label']}",
                    key=f"sb_{infos['dossier']}_{cle_cat}",
                    on_click=lambda n=nom_chapitre, c=cle_cat: aller_categorie(n, c),
                    use_container_width=True,
                )

# ============================================================
# VUE 1 : ACCUEIL — liste des chapitres
# ============================================================

if st.session_state.view == "accueil":
    st.subheader("Choisis un chapitre :")

    for nom, infos in CHAPITRES.items():
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(f"### {infos['icone']} {nom}")
            st.write(infos["description"])
        with col2:
            st.button("Ouvrir ➜", key=f"acc_{infos['dossier']}", on_click=aller_chapitre, args=(nom,), use_container_width=True)
        st.write("---")

# ============================================================
# VUE 2 : CHAPITRE — le cours + les 4 dossiers
# ============================================================

elif st.session_state.view == "chapitre":
    nom_chapitre = st.session_state.chapitre_courant
    infos = CHAPITRES[nom_chapitre]
    dossier = infos["dossier"]

    st.subheader(f"{infos['icone']} {nom_chapitre}")
    st.write(infos["description"])
    st.write("")

    url_cours = f"{BASE_URL}/{dossier}/{infos['cours_fichier']}"
    st.link_button("📖 Ouvrir le cours", url_cours, use_container_width=True)

    st.write("")
    st.markdown("#### Documents complémentaires")

    cols = st.columns(2)
    for i, (cle_cat, cat_infos) in enumerate(CATEGORIES.items()):
        nb_docs = len(FICHIERS.get(dossier, {}).get(cle_cat, []))
        with cols[i % 2]:
            label = f"{cat_infos['icone']} {cat_infos['label']} ({nb_docs})"
            st.button(label, key=f"chap_{dossier}_{cle_cat}", on_click=aller_categorie, args=(nom_chapitre, cle_cat), use_container_width=True)

# ============================================================
# VUE 3 : CATÉGORIE — liste des fichiers déposés (éval/DS)
# ============================================================

elif st.session_state.view == "categorie":
    nom_chapitre = st.session_state.chapitre_courant
    cle_cat = st.session_state.categorie_courante
    infos = CHAPITRES[nom_chapitre]
    dossier = infos["dossier"]
    cat_infos = CATEGORIES[cle_cat]

    st.subheader(f"{cat_infos['icone']} {cat_infos['label']} — {nom_chapitre}")

    # Navigation rapide vers les autres catégories du même chapitre
    nav_cols = st.columns(len(CATEGORIES))
    for i, (autre_cle, autre_infos) in enumerate(CATEGORIES.items()):
        with nav_cols[i]:
            disabled = (autre_cle == cle_cat)
            st.button(
                f"{autre_infos['icone']} {autre_infos['label']}",
                key=f"nav_{dossier}_{autre_cle}",
                on_click=aller_categorie,
                args=(nom_chapitre, autre_cle),
                use_container_width=True,
                disabled=disabled,
            )

    st.markdown("---")

    documents = FICHIERS.get(dossier, {}).get(cle_cat, [])

    if not documents:
        st.info("Aucun document déposé pour le moment dans cette catégorie.")
    else:
        for doc in documents:
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"**{doc['nom']}**")
            with col2:
                url_doc = f"{BASE_URL}/{dossier}/{doc['fichier']}"
                st.link_button("Ouvrir ➜", url_doc, use_container_width=True)
            st.write("---")

    st.button("⬅ Retour au chapitre", on_click=aller_chapitre, args=(nom_chapitre,))

# ============================================================
# PIED DE PAGE
# ============================================================

st.markdown(
    """
    <div style="text-align: center; margin-top: 40px; color: #999; font-size: 13px;">
        Site réalisé par Maël Moignet — Lycée Naval de Brest
    </div>
    """,
    unsafe_allow_html=True
)
