import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import date

st.set_page_config(page_title="GymTrack Cloud", page_icon="🏋️")

# Inseriamo il link direttamente qui per sicurezza
GOOGLE_SHEET_URL = "https://docs.google.com/spreadsheets/d/1CDkQjdxBGYTTQk8xZE0RP5yVJlYuD-80Uzkz84RWAMs/edit?usp=sharing"

# Inizializza connessione
conn = st.connection("gsheets", type=GSheetsConnection)

def get_data():
    try:
        # Tentiamo la lettura specificando il link direttamente
        df = conn.read(spreadsheet=GOOGLE_SHEET_URL, worksheet="workouts", ttl=0)
        if df is None or df.empty:
            return pd.DataFrame(columns=["Data", "Esercizio", "Sets", "Reps", "Weight"])
        return df
    except Exception as e:
        st.error(f"⚠️ Errore di connessione al foglio: {e}")
        st.info("Verifica che la linguetta in basso al Google Sheet si chiami esattamente: workouts")
        return pd.DataFrame(columns=["Data", "Esercizio", "Sets", "Reps", "Weight"])

# --- INTERFACCIA ---
st.title("🏋️ GymTrack Cloud")

menu = st.sidebar.radio("Menu", ["Diario", "Scheda"])

data = get_data()

if menu == "Diario":
    selected_date = str(st.date_input("Data", date.today()))
    
    with st.form("add_ex"):
        col1, col2, col3, col4 = st.columns([3,1,1,1])
        name = col1.text_input("Esercizio")
        s = col2.number_input("S", min_value=1, step=1)
        r = col3.number_input("R", min_value=1, step=1)
        w = col4.number_input("Kg", min_value=0.0, step=0.5)
        submit = st.form_submit_button("Salva nel Cloud")
        
        if submit and name:
            new_row = pd.DataFrame([{
                "Data": selected_date,
                "Esercizio": name,
                "Sets": s,
                "Reps": r,
                "Weight": w
            }])
            updated_df = pd.concat([data, new_row], ignore_index=True)
            try:
                conn.update(spreadsheet=GOOGLE_SHEET_URL, worksheet="workouts", data=updated_df)
                st.success("✅ Allenamento salvato!")
                st.rerun()
            except Exception as e:
                st.error(f"Errore nel salvataggio: {e}")

    st.subheader(f"Progressi del {selected_date}")
    # Filtriamo i dati per la data selezionata
    if not data.empty:
        filtered = data[data["Data"] == selected_date]
        if not filtered.empty:
            st.dataframe(filtered, use_container_width=True, hide_index=True)
        else:
            st.write("Nessun esercizio per questa data.")
