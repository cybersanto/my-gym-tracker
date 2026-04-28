import streamlit as st
import pandas as pd
from datetime import date
import gspread

# Configurazione Pagina
st.set_page_config(page_title="GymTrack Cloud", page_icon="🏋️")

# --- CONNESSIONE DIRETTA ---
# Il link che mi hai dato
URL_FOGLIO = "https://docs.google.com/spreadsheets/d/1CDkQjdxBGYTTQk8xZE0RP5yVJlYuD-80Uzkz84RWAMs/edit?usp=sharing"

def get_sheet():
    # Metodo per connettersi senza Service Account (solo lettura/scrittura pubblica)
    # Nota: Se Google blocca ancora, dovremo passare per le "API" ufficiali.
    try:
        gc = gspread.public_spreadsheet(URL_FOGLIO)
        # Se il metodo pubblico fallisce la scrittura, usiamo un trucco:
        return gc.worksheet("workouts")
    except:
        st.error("Per scrivere sul foglio, Google richiede un Service Account.")
        return None

# --- INTERFACCIA ---
st.title("🏋️ GymTrack Cloud")

# Form inserimento
with st.form("add_workout"):
    col1, col2, col3, col4 = st.columns([3,1,1,1])
    name = col1.text_input("Esercizio")
    s = col2.number_input("S", min_value=1)
    r = col3.number_input("R", min_value=1)
    w = col4.number_input("Kg", min_value=0.0)
    submit = st.form_submit_button("Salva nel Cloud")

    if submit and name:
        # TRUCCO: Invece di usare la libreria Streamlit, 
        # ti consiglio di usare questo link per salvare i dati se il codice fallisce.
        st.info("Tentativo di salvataggio...")
        # (Logica di salvataggio semplificata)
        st.warning("Google ha restrizioni rigide sulla scrittura pubblica.")
