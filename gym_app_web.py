import streamlit as st
import pandas as pd
import json
import os
from datetime import date

# Configurazione Pagina
st.set_page_config(page_title="GymTrack Pro", page_icon="🏋️", layout="wide")

# --- GESTIONE DATI (JSON locale o Session State) ---
def load_data():
    if os.path.exists("workout_db.json"):
        with open("workout_db.json", "r") as f: return json.load(f)
    return {"workouts": {}, "routine": []}

def save_data(data):
    with open("workout_db.json", "w") as f:
        json.dump(data, f, indent=4)

if 'db' not in st.session_state:
    st.session_state.db = load_data()

db = st.session_state.db

# --- SIDEBAR NAVIGAZIONE ---
st.sidebar.title("🏋️ GymTrack Pro")
menu = st.sidebar.radio("Vai a:", ["Diario Allenamento", "La Mia Scheda", "Storico Dati"])

# --- PAGINA: DIARIO ALLENAMENTO ---
if menu == "Diario Allenamento":
    st.header("📓 Diario del Giorno")
    
    selected_date = str(st.date_input("Seleziona Data", date.today()))
    
    # Import dalla scheda
    if st.button("📥 Importa dalla mia Scheda"):
        if db["routine"]:
            db["workouts"][selected_date] = [
                {"name": r["name"], "sets": r["sets"], "reps": r["reps"], "weight": 0} 
                for r in db["routine"]
            ]
            save_data(db)
            st.success("Scheda importata! Ora aggiorna i pesi.")
        else:
            st.warning("La tua scheda è vuota!")

    # Form inserimento manuale
    with st.expander("➕ Aggiungi Esercizio Singolo"):
        col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
        with col1: name = st.text_input("Esercizio")
        with col2: sets = st.number_input("Sets", min_value=1, step=1)
        with col3: reps = st.number_input("Reps", min_value=1, step=1)
        with col4: weight = st.number_input("Kg", min_value=0.0, step=0.5)
        
        if st.button("Aggiungi al diario"):
            if name:
                if selected_date not in db["workouts"]: db["workouts"][selected_date] = []
                db["workouts"][selected_date].append({"name": name, "sets": sets, "reps": reps, "weight": weight})
                save_data(db)
                st.rerun()

    # Visualizzazione log
    st.subheader(f"Log per il {selected_date}")
    if selected_date in db["workouts"] and db["workouts"][selected_date]:
        for i, ex in enumerate(db["workouts"][selected_date]):
            cols = st.columns([4, 2, 2, 2, 1])
            cols[0].write(f"**{ex['name']}**")
            cols[1].write(f"{ex['sets']} serie")
            cols[2].write(f"{ex['reps']} reps")
            cols[3].write(f"{ex['weight']} kg")
            if cols[4].button("🗑️", key=f"del_{selected_date}_{i}"):
                db["workouts"][selected_date].pop(i)
                save_data(db)
                st.rerun()
    else:
        st.info("Nessun esercizio registrato.")

# --- PAGINA: LA MIA SCHEDA ---
elif menu == "La Mia Scheda":
    st.header("📋 Definizione Scheda Standard")
    st.write("Inserisci qui gli esercizi che fai di solito per importarli velocemente nel diario.")
    
    with st.form("routine_form"):
        col1, col2, col3 = st.columns([3, 1, 1])
        r_name = col1.text_input("Esercizio")
        r_sets = col2.number_input("Sets", min_value=1)
        r_reps = col3.number_input("Reps", min_value=1)
        if st.form_submit_button("Salva in Scheda"):
            db["routine"].append({"name": r_name, "sets": r_sets, "reps": r_reps})
            save_data(db)
            st.success("Esercizio aggiunto alla scheda!")

    for i, r in enumerate(db["routine"]):
        st.text(f"• {r['name']} ({r['sets']}x{r['reps']})")

# --- PAGINA: STORICO ---
elif menu == "Storico Dati":
    st.header("📊 Storico Progressi")
    if db["workouts"]:
        all_data = []
        for d, exercises in db["workouts"].items():
            for ex in exercises:
                all_data.append({"Data": d, **ex})
        df = pd.DataFrame(all_data)
        st.dataframe(df, use_container_width=True)
    else:
        st.write("Ancora nessun dato salvato.")