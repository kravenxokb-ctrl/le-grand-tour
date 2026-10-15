import streamlit as st
from supabase import create_client

# ============================================================
# CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Le Grand Tour",
    page_icon="🚴",
    layout="wide",
)

GOAL = 1000.0
LAP_DISTANCE = 5.51

MILESTONES = [
    ("Maubuisson", 0),
    ("Bruges", 42),
    ("Langon", 118),
    ("Montauban", 224),
    ("Toulouse", 278),
    ("Castelnaudary", 340),
    ("Carcassonne", 383),
    ("Narbonne", 443),
    ("Montpellier", 541),
    ("Marseille", 706),
    ("Toulon", 771),
    ("Cannes", 895),
    ("Monaco", 1000),
]

# ============================================================
# CONNEXION SUPABASE
# ============================================================

@st.cache_resource
def get_supabase():
    return create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_KEY"],
    )


supabase = get_supabase()


# ============================================================
# FONCTIONS
# ============================================================

def get_distance():
    response = (
        supabase
        .table("challenge")
        .select("distance")
        .eq("id", 1)
        .single()
        .execute()
    )

    return float(response.data["distance"])


def add_lap():
    current = get_distance()
    new_distance = min(current + LAP_DISTANCE, GOAL)

    (
        supabase
        .table("challenge")
        .update({"distance": new_distance})
        .eq("id", 1)
        .execute()
    )


def reset_distance():
    (
        supabase
        .table("challenge")
        .update({"distance": 0})
        .eq("id", 1)
        .execute()
    )


# ============================================================
# CALCUL DE LA SITUATION
# ============================================================

distance = get_distance()

progress = min(distance / GOAL, 1.0)
remaining = max(GOAL - distance, 0)

current_city = "Maubuisson"
next_city = "Bruges"

for i in range(len(MILESTONES) - 1):

    city, km = MILESTONES[i]
    next_name, next_km = MILESTONES[i + 1]

    if distance >= next_km:

        current_city = next_name

        if i + 2 < len(MILESTONES):
            next_city = MILESTONES[i + 2][0]
        else:
            next_city = "Monaco"

    else:

        current_city = city
        next_city = next_name
        break


# ============================================================
# TITRE
# ============================================================

st.title("🚴 LE GRAND TOUR")

st.caption("Tour de Gassies · Défi collectif")

st.divider()


# ============================================================
# DISTANCE PRINCIPALE
# ============================================================

st.metric(
    "Distance collective parcourue",
    f"{distance:.2f} km",
    f"{progress * 100:.1f} %",
)

st.progress(
    progress,
    text=f"{progress * 100:.1f} % de l'objectif"
)


col1, col2 = st.columns(2)

with col1:
    st.caption("Départ")
    st.write("**Maubuisson — 0 km**")

with col2:
    st.caption("Objectif")
    st.write("**Monaco — 1 000 km**")


st.divider()


# ============================================================
# STATISTIQUES
# ============================================================

st.subheader("📍 Situation")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Reste",
        f"{remaining:.2f} km"
    )

with col2:
    st.metric(
        "Étape actuelle",
        current_city
    )

with col3:
    st.metric(
        "Prochaine ville",
        next_city
    )


st.divider()


# ============================================================
# PARCOURS
# ============================================================

st.subheader("🗺️ LE PARCOURS · 1 000 KM")

for city, km in MILESTONES:

    if distance >= km:
        status = "🟢"

    elif city == current_city:
        status = "🚴"

    else:
        status = "⚪"

    st.write(
        f"{status} **{city}** — {km} km"
    )


st.divider()


# ============================================================
# AJOUTER UN TOUR
# ============================================================

st.subheader("🚴 Ajouter un tour")

st.write(
    "Chaque tour ajoute **5,51 km** au compteur collectif."
)

if st.button(
    "🚴 +5,51 km",
    use_container_width=True,
    type="primary",
):
    add_lap()
    st.rerun()


st.divider()


# ============================================================
# RESET
# ============================================================

with st.expander("⚙️ Réinitialisation"):

    st.warning(
        "Cette action remet le compteur collectif à 0 km."
    )

    if st.button(
        "Réinitialiser le compteur",
        use_container_width=True,
    ):
        reset_distance()
        st.rerun()


st.divider()


# ============================================================
# PIED DE PAGE
# ============================================================

st.caption(
    "LE GRAND TOUR · Défi collectif · "
    "Maubuisson → Monaco · 1 000 km"
)