import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="GymTrack Easy", page_icon="💪")

st.title("🏋️ Il Mio Diario Gym")

# Funzione per caricare/salvare i dati usando il database di Streamlit
@st.cache_data(ttl=600)
def load_data():
    if "my_data" not in st.session_state:
        # Prova a leggere il file se esiste già nel cloud storage
        try:
            return pd.read_csv("gym_progress.csv")
        except:
            return pd.DataFrame(columns=["Data", "Esercizio", "Sets", "Reps", "Kg"])
    return st.session_state.my_data

data = load_data()

# --- FORM DI INSERIMENTO ---
with st.form("gym_form", clear_on_submit=True):
    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
    es = col1.text_input("Esercizio")
    s = col2.number_input("S", min_value=1, step=1)
    r = col3.number_input("R", min_value=1, step=1)
    k = col4.number_input("Kg", min_value=0.0, step=0.5)
    
    if st.form_submit_button("Salva nel Cloud"):
        if es:
            nuovo = pd.DataFrame([[str(date.today()), es, s, r, k]], 
                                columns=["Data", "Esercizio", "Sets", "Reps", "Kg"])
            data = pd.concat([data, nuovo], ignore_index=True)
            # Salva fisicamente il file
            data.to_csv("gym_progress.csv", index=False)
            st.session_state.my_data = data
            st.success("Salvato!")
            st.rerun()

# --- VISUALIZZAZIONE ---
st.subheader("I tuoi record")
st.dataframe(data, use_container_width=True, hide_index=True)

# Tasto per scaricare i dati sul telefono (per sicurezza tua)
st.download_button("Scarica Backup Excel/CSV", 
                   data.to_csv(index=False), 
                   "i_miei_allenamenti.csv", "text/csv")
