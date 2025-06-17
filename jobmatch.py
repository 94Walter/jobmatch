import streamlit as st
import pandas as pd
import os
from datetime import date

# File di salvataggio
dir_path = "dati"
os.makedirs(dir_path, exist_ok=True)
aziende_file = os.path.join(dir_path, "aziende.csv")
studenti_file = os.path.join(dir_path, "studenti.csv")

st.set_page_config(page_title="Match Lavoro - POP BI & LiVE", layout="centered")
st.title("🔗 Piattaforma Incontro Domanda-Offerta | POP BI x LiVE")

menu = ["Per le Aziende", "Per gli Studenti", "👁️‍🗨️ Admin - Visualizza Dati"]
scelta = st.sidebar.radio("Seleziona il tuo profilo", menu)

# Funzione per salvataggio
@st.cache_data

def salva_dati(df, file_path):
    if os.path.exists(file_path):
        df_esistente = pd.read_csv(file_path)
        df = pd.concat([df_esistente, df], ignore_index=True)
    df.to_csv(file_path, index=False)

if scelta == "Per le Aziende":
    st.subheader("📌 Inserisci la tua richiesta di personale")
    with st.form("form_azienda"):
        ragione_sociale = st.text_input("Ragione sociale")
        referente = st.text_input("Nome e Cognome del referente")
        email = st.text_input("Email di contatto")
        telefono = st.text_input("Telefono")
        settore = st.selectbox("Settore aziendale", ["Consulenza", "Manifattura", "Retail", "IT", "Altro"])
        descrizione = st.text_area("Descrizione sintetica dell'azienda")
        ruolo = st.text_input("Figura professionale ricercata")
        attivita = st.text_area("Attività previste per il ruolo")
        contratto = st.selectbox("Tipologia di contratto proposta", ["Tempo indeterminato", "Tempo determinato", "Part-time", "Collaborazione occasionale", "Tirocinio extra-curricolare", "Tirocinio curricolare", "Altro"])
        modalita = st.radio("Modalità di lavoro", ["In presenza", "Ibrido", "Da remoto"])
        inizio = st.date_input("Data di inizio desiderata", value=date.today())
        note = st.text_area("Altre esigenze o messaggi aggiuntivi")

        submitted = st.form_submit_button("Invia richiesta")
        if submitted:
            df = pd.DataFrame([{"Ragione Sociale": ragione_sociale,
                                "Referente": referente,
                                "Email": email,
                                "Telefono": telefono,
                                "Settore": settore,
                                "Descrizione": descrizione,
                                "Ruolo Ricercato": ruolo,
                                "Attività previste": attivita,
                                "Tipo contratto": contratto,
                                "Modalità lavoro": modalita,
                                "Data inizio": inizio,
                                "Note": note}])
            salva_dati(df, aziende_file)
            st.success("✅ Richiesta inviata con successo!")

elif scelta == "Per gli Studenti":
    st.subheader("🎓 Inserisci la tua candidatura")
    with st.form("form_studente"):
        nome = st.text_input("Nome e Cognome")
        email = st.text_input("Email")
        telefono = st.text_input("Telefono (opzionale)")
        eta = st.number_input("Età", min_value=16, max_value=99)
        titolo = st.selectbox("Titolo di studio", ["Diploma", "Laurea triennale", "Laurea magistrale", "ITS", "Altro"])
        ateneo = st.text_input("Ateneo / Istituto di provenienza")
        area = st.selectbox("Area di studio", ["Economia", "Ingegneria", "Informatica", "Design", "Scienze Sociali", "Altro"])
        competenze = st.text_area("Competenze possedute (es. Excel, SQL, Power BI)")
        ruolo = st.text_input("Ruolo desiderato")
        settore = st.selectbox("Settore preferito", ["Consulting", "Pubblica Amministrazione", "Industria", "Retail", "Servizi", "Altro"])
        contratto = st.selectbox("Tipo di contratto desiderato", ["Tempo indeterminato", "Tempo determinato", "Part-time", "Collaborazione occasionale", "Tirocinio extra-curricolare", "Tirocinio curricolare", "Altro"])
        disponibilita = st.text_input("Disponibilità temporale (es. subito, da settembre...)" )
        note = st.text_area("Altre preferenze o messaggi")

        submitted = st.form_submit_button("Invia candidatura")
        if submitted:
            df = pd.DataFrame([{"Nome": nome,
                                "Email": email,
                                "Telefono": telefono,
                                "Età": eta,
                                "Titolo di studio": titolo,
                                "Istituto": ateneo,
                                "Area": area,
                                "Competenze": competenze,
                                "Ruolo desiderato": ruolo,
                                "Settore preferito": settore,
                                "Tipo contratto": contratto,
                                "Disponibilità": disponibilita,
                                "Note": note}])
            salva_dati(df, studenti_file)
            st.success("✅ Candidatura inviata con successo!")

elif scelta == "👁️‍🗨️ Admin - Visualizza Dati":
    st.subheader("📊 Pannello Amministrazione - Dati raccolti")
    password = st.text_input("Inserisci la password per accedere", type="password")
    if password == "admin123":
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 📁 Richieste Aziende")
            if os.path.exists(aziende_file):
                df_aziende = pd.read_csv(aziende_file)
                st.dataframe(df_aziende, use_container_width=True)
            else:
                st.info("Nessuna richiesta ancora inserita.")

        with col2:
            st.markdown("### 🧑‍🎓 Candidature Studenti")
            if os.path.exists(studenti_file):
                df_studenti = pd.read_csv(studenti_file)
                st.dataframe(df_studenti, use_container_width=True)
            else:
                st.info("Nessuna candidatura ancora inserita.")
    else:
        st.warning("🔐 Inserisci la password corretta per accedere al pannello.")

# Esportazione dati
st.sidebar.markdown("---")
st.sidebar.subheader("📥 Esporta i dati")
if st.sidebar.button("Scarica richieste aziende"):
    if os.path.exists(aziende_file):
        df = pd.read_csv(aziende_file)
        st.sidebar.download_button("Download Aziende CSV", df.to_csv(index=False), "aziende.csv", "text/csv")
if st.sidebar.button("Scarica profili studenti"):
    if os.path.exists(studenti_file):
        df = pd.read_csv(studenti_file)
        st.sidebar.download_button("Download Studenti CSV", df.to_csv(index=False), "studenti.csv", "text/csv")
