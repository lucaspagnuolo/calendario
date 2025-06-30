import streamlit as st
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
for p in persons:
    smartwork.setdefault(p, {})

# Sidebar: selezione persona
st.sidebar.header("Seleziona Persona")
selected = st.sidebar.selectbox("Persona:", persons)

# Sidebar: riepilogo totale
st.sidebar.header("Conteggio Totale per Persona")
for p in persons:
    total = sum(1 for v in smartwork[p].values() if v)
    st.sidebar.write(f"{p}: {total} giorni totali")

# Salvataggio dati
if st.sidebar.button("Salva Modifiche"):
    save_json(smartwork, SMART_FILE)
    st.sidebar.success("Dati salvati con successo!")

# Main title
st.title("Calendario Smartworking (Luglio-Dicembre 2025)")

year = 2025
months = list(range(7, 13))  # Luglio=7 a Dicembre=12

# Loop sui mesi
for month in months:
    st.header(f"{calendar.month_name[month]} {year}")
    cal = calendar.monthcalendar(year, month)
    monthly_count = 0

    # Header giorni settimana
    days = ['Lun', 'Mar', 'Mer', 'Gio', 'Ven', 'Sab', 'Dom']
    cols = st.columns(7)
    for idx, d in enumerate(days):
        cols[idx].write(f"**{d}**")

    # Checkbox per giorno
    for week in cal:
        cols = st.columns(7)
        for i, d in enumerate(week):
            if d:
                date_str = f"{year}-{month:02d}-{d:02d}"
                key = f"{selected}_{date_str}"
                checked = smartwork[selected].get(date_str, False)
                val = cols[i].checkbox(str(d), value=checked, key=key)
                smartwork[selected][date_str] = val
                if val:
                    monthly_count += 1
            else:
                cols[i].write("")

    # Mostra conteggio mensile
    if monthly_count > 11:
        st.error(f"{selected} ha selezionato {monthly_count} giorni in {calendar.month_name[month]}, oltre il limite di 11.")
    else:
        st.success(f"{selected} ha segnato {monthly_count} giorni in {calendar.month_name[month]}")

# Espander per vedere tutti i giorni selezionati
all_days = st.expander("Visualizza giorni per persona")
with all_days:
    for p in persons:
        st.subheader(p)
        dates = sorted([d for d, v in smartwork[p].items() if v])
        if dates:
            # Raggruppa per mese
            grouped = {}
            for d in dates:
                m = int(d.split('-')[1])
                grouped.setdefault(calendar.month_name[m], []).append(d)
            for m, ds in grouped.items():
                st.write(f"**{m}:** {', '.join(ds)}")
        else:
            st.write("Nessun giorno selezionato")

st.write("---\nPowered by Streamlit")
