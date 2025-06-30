import streamlit as st
import pandas as pd
import calendar
import datetime
import json
import os

# File paths for persistence
NAMES_FILE = 'names.json'
SMART_FILE = 'smartwork.json'

# Utility functions for persistence
def load_json(filepath):
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return json.load(f)
    return {}

def save_json(data, filepath):
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)

# Load persisted data
names = load_json(NAMES_FILE).get('names', [])
smartwork = load_json(SMART_FILE)

# Sidebar: Gestione dei nomi
st.sidebar.header("Gestione Persone")
new_name = st.sidebar.text_input("Aggiungi nuovo nome:")
if st.sidebar.button("Aggiungi") and new_name.strip():
    if new_name not in names:
        names.append(new_name)
        save_json({'names': names}, NAMES_FILE)
        st.sidebar.success(f"Nome '{new_name}' aggiunto con successo!")
    else:
        st.sidebar.warning("Nome già presente.")

st.sidebar.subheader("Persone Registrate:")
for n in names:
    st.sidebar.write(f"- {n}")

st.title("Calendario Smartworking (Luglio-Dicembre 2025)")

# Genera calendario mese per mese
year = 2025
months = list(range(7, 13))  # Luglio=7 a Dicembre=12

for month in months:
    st.header(f"{calendar.month_name[month]} {year}")
    cal = calendar.monthcalendar(year, month)
    dates_checked = 0

    # Display calendar with checkbox per giorno
    cols = st.columns(7)
    # Set headers lun-dom (Italian)
    weekdays = ['Lun', 'Mar', 'Mer', 'Gio', 'Ven', 'Sab', 'Dom']
    for idx, w in enumerate(weekdays):
        cols[idx].write(f"**{w}**")

    # Iterate weeks
    for week in cal:
        cols = st.columns(7)
        for i, day in enumerate(week):
            if day:
                date_str = f"{year}-{month:02d}-{day:02d}"
                checked = smartwork.get(date_str, False)
                val = cols[i].checkbox(str(day), value=checked, key=date_str)
                smartwork[date_str] = val
                if val:
                    dates_checked += 1
            else:
                cols[i].write("")

    st.write(f"**Giorni di smartworking segnati: {dates_checked}**")

# Salva dati smartworking
if st.button("Salva modifiche"):
    save_json(smartwork, SMART_FILE)
    st.success("Dati di smartworking salvati con successo!")

st.write("\n---\nPowered by Streamlit")
