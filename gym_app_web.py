import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import date

st.set_page_config(page_title="GymTrack Pro", page_icon="🏋️")

# --- CONNESSIONE A GOOGLE SHEETS ---
conn = st.connection("gsheets", type=GSheetsConnection)

# Funzione per leggere i dati
def get_data():
    return conn.read(worksheet="workouts", ttl=0) # ttl=0 forza l'aggiornamento live

# --- INTERFACCIA ---
st.title("🏋️ GymTrack Cloud")

menu = st.sidebar.radio("Menu", ["Diario", "Scheda"])

if menu == "Diario":
    selected_date = str(st.date_input("Data", date.today()))
    
    # Form per nuovo esercizio
    with st.form("add_ex"):
        col1, col2, col3, col4 = st.columns([3,1,1,1])
        name = col1.text_input("Esercizio")
        s = col2.number_input("S", min_value=1)
        r = col3.number_input("R", min_value=1)
        w = col4.number_input("Kg", min_value=0.0)
        submit = st.form_submit_button("Salva nel Cloud")
        
        if submit and name:
            # Carica dati esistenti, aggiungi riga e salva
            df_existing = get_data()
            new_row = pd.DataFrame([{
                "Data": selected_date,
                "Esercizio": name,
                "Sets": s,
                "Reps": r,
                "Weight": w
            }])
            updated_df = pd.concat([df_existing, new_row], ignore_index=True)
            conn.update(worksheet="workouts", data=updated_df)
            st.success("Salvato su Google Sheets!")
            st.rerun()

    # Visualizzazione
    st.subheader("I tuoi progressi")
    data = get_data()
    # Filtra per la data selezionata
    filtered_data = data[data["Data"] == selected_date]
    st.dataframe(filtered_data, use_container_width=True, hide_index=True)
