import streamlit as st
import pandas as pd
import calendar
import json
import os

# File paths for persistence
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

# Define persons
persons = ['Luca', 'Luna', 'Andrea']

# Load persisted data: { person: { date_str: bool } }
smartwork = load_json(SMART_FILE)
# Ensure all persons exist
for p in persons:
    smartwork.setdefault(p, {})

# Sidebar: selezione persona
st.sidebar.header("Seleziona Persona")
selected = st.sidebar.selectbox("Persona:", persons)

# Sidebar: riepilogo conteggi
st.sidebar.header("Conteggio Smartworking")
for p in persons:
    count = sum(1 for v in smartwork[p].values() if v)
    st.sidebar.write(f"{p}: {count} giorni")

# Main title
st.title("Calendario Smartworking (Luglio-Dicembre 2025)")

# Calendario mese per mese
year = 2025
months = list(range(7, 13))  # Luglio=7 a Dicembre=12

# Track count for selected
selected_count = 0

for month in months:
    st.header(f"{calendar.month_name[month]} {year}")
    cal = calendar.monthcalendar(year, month)

    # Display weekdays header
    days = ['Lun', 'Mar', 'Mer', 'Gio', 'Ven', 'Sab', 'Dom']
    cols = st.columns(7)
    for idx, day in enumerate(days):
        cols[idx].write(f"**{day}**")

    # Iterate weeks
    for week in cal:
        cols = st.columns(7)
        for i, d in enumerate(week):
            if d:
                date_str = f"{year}-{month:02d}-{d:02d}"
                # Checkbox for selected person
                key = f"{selected}_{date_str}"
                checked = smartwork[selected].get(date_str, False)
                val = cols[i].checkbox(str(d), value=checked, key=key)
                smartwork[selected][date_str] = val
                if val:
                    selected_count += 1
            else:
                cols[i].write("")

# Message if over limit
if selected_count > 11:
    st.error(f"Attenzione: {selected} ha selezionato {selected_count} giorni, oltre il limite di 11.")

st.write(f"**{selected} ha segnato {selected_count} giorni di smartworking**")

# Mostra giorni degli altri
st.subheader("Giorni di smartworking degli altri")
for p in persons:
    if p != selected:
        dates = sorted([d for d, v in smartwork[p].items() if v])
        if dates:
            st.write(f"**{p}:** {', '.join(dates)}")
        else:
            st.write(f"**{p}:** nessun giorno selezionato")

# Salvataggio dati
if st.sidebar.button("Salva Modifiche"):
    save_json(smartwork, SMART_FILE)
    st.sidebar.success("Dati salvati con successo!")

st.write("---\nPowered by Streamlit")
