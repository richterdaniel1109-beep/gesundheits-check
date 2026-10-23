import streamlit as st
import matplotlib.pyplot as plt

# Webseiten-Konfiguration auf "wide" für ein modernes Layout
st.set_page_config(page_title="Gesundheits- & Fitness-Check", page_icon="🏥", layout="wide")

# --- GOOGLE ANALYTICS INTEGRATION (HEADER INJECTION) ---
GA_MEASUREMENT_ID = "G-FSLDQDD6YJ"

ga_html = f"""
<head>
  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id={GA_MEASUREMENT_ID}"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', '{GA_MEASUREMENT_ID}');
  </script>
</head>
"""

# Injiziert den Code direkt in den Kopfbereich der Webseite
st.markdown(ga_html, unsafe_allow_html=True)

# Lädt das Tracking unsichtbar in die App
# -----------------------------------

st.title("🏥 Dein persönlicher Gesundheits- & Fitness-Check")
st.write("Professionelles Tool zur Selbsteinschätzung deiner körperlichen Verfassung und Arbeitsbelastung.")

# --- EINGABEN DIREKT AUF DER HAUPTSEITE (FÜR MOBILE OPTIMIERT) ---
st.markdown("### 📝 Deine Eckdaten & Gewohnheiten")

# Wir nutzen Spalten, damit es auf dem PC schön breit und auf dem Handy untereinander angeordnet wird
col_input1, col_input2 = st.columns(2)

with col_input1:
    name = st.text_input("Wie heißt du?", "Max")
    age = st.number_input("Wie alt bist du?", min_value=1, max_value=120, value=30, step=1)

    # IT-Easter Egg für das Alter 42
    if age == 42:
        st.success("🤖 Alter 42 erkannt: Die Antwort auf das Leben, das Universum und den ganzen Rest! 😉")

    smoker_input = st.radio("Bist du Raucher?", ["Nein", "Ja"])
    is_smoker = True if smoker_input == "Ja" else False

    job = st.selectbox("Was machst du beruflich?", ["IT", "Handwerk", "Tiefbau", "Verkauf", "Friseure", "Schüler"])

with col_input2:
    weight = st.number_input("Gewicht in kg (z.B. 78)", min_value=20.0, max_value=300.0, value=75.0, step=0.5)
    height_cm = st.number_input("Größe in cm (z.B. 175)", min_value=50.0, max_value=250.0, value=175.0, step=1.0)

    # Alkohol-Auswahl
    alk_wahl = st.selectbox("Alkohol-Konsum", [
        "Nie oder sehr selten",
        "1 bis 3 Mal im Monat / zu besonderen Anlässen",
        "1 bis 3 Mal pro Woche",
        "Fast täglich oder täglich"
    ])

    # Sport-Auswahl
    sport_wahl = st.selectbox("Sport & Bewegung", [
        "Sehr aktiv (3+ mal/Woche)",
        "Mäßig aktiv (1-2 mal/Woche)",
        "Eher inaktiv / Wenig Sport"
    ])

# Alkohol-Punkte logik
if alk_wahl == "Nie oder sehr selten":
    alk_punkte = 0
elif alk_wahl == "1 bis 3 Mal im Monat / zu besonderen Anlässen":
    alk_punkte = 1
elif alk_wahl == "1 bis 3 Mal pro Woche":
    alk_punkte = 3
else:
    alk_punkte = 5

# Sport-Punkte logik
if sport_wahl == "Sehr aktiv (3+ mal/Woche)":
    sport_bonus = 15
    sport_punkte_vis = 0
elif sport_wahl == "Mäßig aktiv (1-2 mal/Woche)":
    sport_bonus = 8
    sport_punkte_vis = 1
else:
    sport_bonus = 0
    sport_punkte_vis = 2

# Automatische Umrechnung von cm in Meter für den BMI
height = height_cm / 100

# --- BERECHNUNGEN ---
bmi = weight / (height ** 2)

if bmi < 18.5:
    bmi_punkte = 5
    kategorie = "Untergewicht"
    target_weight = 18.5 * (height ** 2)
    diff = target_weight - weight
    hinweis_gewicht = f"Du müsstest ca. {diff:.1f} kg zunehmen, um den Normalbereich zu erreichen."
elif 18.5 <= bmi < 25:
    bmi_punkte = 0
    kategorie = "Normalgewicht"
    hinweis_gewicht = "Stark, du liegst absolut im grünen Bereich! 🎉"
elif 25 <= bmi < 30:
    bmi_punkte = 5
    kategorie = "Übergewicht"
    target_weight = 24.9 * (height ** 2)
    diff = weight - target_weight
    hinweis_gewicht = f"Du müsstest ca. {diff:.1f} kg abnehmen, um die obere Grenze des Normalgewichts zu erreichen."
else:
    bmi_punkte = 10
    kategorie = "Adipositas (starkes Übergewicht)"
    target_weight = 24.9 * (height ** 2)
    diff = weight - target_weight
    hinweis_gewicht = f"Du müsstest ca. {diff:.1f} kg abnehmen, um die obere Grenze des Normalgewichts zu erreichen."

# Wasserbedarf
faktor_wasser = 35 if age < 65 else 30
wasser_liter = (weight * faktor_wasser) / 1000

# Branchenspezifische Fragen
st.markdown("---")
st.header(f"🧩 Belastungs-Check für den Bereich: {job}")

fragen_liste = []
quelle_info = ""

if job == "IT":
    quelle_info = "Quellen: ArbMedVV, DGUV Empfehlungen (G 37), gesund.bund.de[cite: 3]"
    fragen_liste = [
        ("Sitzen", "Wie viel sitzt du am Tag (Arbeit + Freizeit)?"),
        ("Augen", "Brennen, Trockenheit oder Kopfschmerzen durch Bildschirme?"),
        ("Nacken/Rücken", "Hast du regelmäßige Verspannungen oder Schmerzen?"),
        ("Schlaf", "Probleme beim Einschlafen nach der Bildschirmzeit?"),
        ("Stress", "Termindruck, ständige Erreichbarkeit oder innere Unruhe?")
    ]
elif job == "Handwerk":
    quelle_info = "Quellen: ArbMedVV, DGUV Empfehlungen (G 20, G 46), BG BAU[cite: 3]"
    fragen_liste = [
        ("Rücken", "Spürst du Rückenschmerzen nach der Arbeit oder ausstrahlend?"),
        ("Gelenke", "Schmerzen in Knie, Schultern oder Handgelenken bei Belastung?"),
        ("Gehör", "Ohrensausen oder Pfeifen (Tinnitus) nach der Arbeit?"),
        ("Hände/Nerven", "Kribbeln, Taubheit oder weiße Finger durch Vibrationen?"),
        ("Unfälle", "Hattest du im letzten Jahr Beinahe-Unfälle oder Verletzungen?")
    ]
elif job == "Tiefbau":
    quelle_info = "Quellen: ArbMedVV, DGUV (G 1.1 Quarzstaub, G 20, G 41, G 46)[cite: 3]"
    fragen_liste = [
        ("MSK & Vibration", "Schmerzen durch schwere Lasten oder Hand-Arm-Vibrationen?"),
        ("Gehör", "Beeinträchtigungen des Hörens durch Baulärm?"),
        ("Atmung", "Husten oder gereizte Atemwege durch Staub (z.B. Quarz)?"),
        ("Sicherheit", "Fühlst du dich bei Arbeiten mit Absturzgefahr oder Geräten sicher?"),
        ("Erholung", "Schaffst du es körperlich, dich nach den Schichten zu erholen?")
    ]
elif job == "Verkauf":
    quelle_info = "Quellen: DGUV Empfehlungen, GKV Check-up Richtlinien[cite: 3]"
    fragen_liste = [
        ("Füße/Beine", "Müde, schwere Beine oder Fußschmerzen am Feierabend?"),
        ("Rücken", "Schmerzen im Rücken durch langes Stehen oder schweres Heben?"),
        ("Stimme", "Heiserkeit oder Halsschmerzen nach stressigen Schichten?"),
        ("Infekte", "Wie oft plagen dich Erkältungen im Jahr?"),
        ("Stress", "Belastung durch Kundendruck und schwierige Situationen?")
    ]
elif job == "Friseure":
    quelle_info = "Quellen: BGW, TRGS 530 (Friseurhandwerk), Universitätsklinikum Hamburg-Eppendorf[cite: 3]"
    fragen_liste = [
        ("Haut/Hände", "Trockene Hände, Rötungen oder Ekzeme durch Feuchtarbeit/Chemikalien?"),
        ("Schulter/Nacken", "Verspannungen durch Arbeiten über Kopf (Föhnen, Schneiden)?"),
        ("Beine/Füße", "Schmerzen oder schwere Beine durch dauerhaftes Stehen?"),
        ("Atemwege", "Reizungen durch Sprays, Dauerwellen oder Haarfarben?"),
        ("Stress/Takt", "Belastung durch engen Zeitplan und Geräuschpegel im Salon?")
    ]
elif job == "Schüler":
    quelle_info = "Quellen: Jugendärztliche Untersuchungen, STIKO Impfempfehlungen[cite: 3]"
    fragen_liste = [
        ("Haltung", "Haltungsprobleme oder Rückenschmerzen durch schwere Rucksäcke/Schule?"),
        ("Sehen/Hören", "Probleme an der Tafel zu folgen oder dem Unterricht zu lauschen?"),
        ("Stress", "Belastung durch Leistungsdruck, Prüfungen oder Dauer-Handynutzung?"),
        ("Schlaf", "Schlafprobleme oder morgendliche Erschöpfung?"),
        ("Bewegung", "Zu wenig Ausgleich oder Sport im Alltag?")
    ]

ergebnisse_arbeit = {}
for bereich, frage in fragen_liste:
    antwort = st.radio(frage, ["🟢 Alles super / selten (0 Pkt.)", "🟡 Gelegentlich / mäßig (1 Pkt.)",
                               "🔴 Täglich / stark (2 Pkt.)"], key=bereich)
    if "0 Pkt." in antwort:
        ergebnisse_arbeit[bereich] = 0
    elif "1 Pkt." in antwort:
        ergebnisse_arbeit[bereich] = 1
    else:
        ergebnisse_arbeit[bereich] = 2

# --- AUSWERTUNG ANZEIGEN ---
st.markdown("---")
if st.button("🚀 Gesundheits-Check auswerten", use_container_width=True):
    abzug_fragen = sum(ergebnisse_arbeit.values()) * 3
    abzug_raucher = 15 if is_smoker else 0
    abzug_alkohol = alk_punkte * 3
    abzug_bmi = bmi_punkte
    abzug_alter = int(age * 0.15)

    basis_score = 100 - (abzug_fragen + abzug_raucher + abzug_alkohol + abzug_bmi + abzug_alter)
    fit_score = min(100, max(0, basis_score + sport_bonus))

    st.markdown("---")
    st.header(f"🏆 Auswertung für {name}")

    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Dein Fit-Score", value=f"{fit_score} / 100 Punkte")
    with col2:
        st.metric(label="Empfohlener Wasserbedarf", value=f"{wasser_liter:.1f} Liter / Tag")

    st.subheader("📊 Deine Ergebnisse im Detail:")
    st.write(f"- **BMI:** {bmi:.2f} ({kategorie}) – *{hinweis_gewicht}*")

    # Dashboard als Matplotlib-Diagramm
    kategorien_vis = []
    werte_vis = []

    for k, v in ergebnisse_arbeit.items():
        kategorien_vis.append(f"[Job] {k}")
        werte_vis.append(v)

    kategorien_vis.append("[Life] Alkohol")
    werte_vis.append(0 if alk_punkte == 0 else (1 if alk_punkte <= 2 else 2))

    kategorien_vis.append("[Life] Sport")
    werte_vis.append(sport_punkte_vis)

    kategorien_vis.append("[Life] Rauchen")
    werte_vis.append(2 if is_smoker else 0)

    kategorien_vis.append("[Life] BMI")
    werte_vis.append(0 if bmi_punkte == 0 else (1 if bmi_punkte == 5 else 2))

    farben = ["#2ecc71" if w == 0 else ("#f1c40f" if w == 1 else "#e74c3c") for w in werte_vis]

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.barh(kategorien_vis, werte_vis, color=farben)
    ax.set_xlabel("Belastung (0 = Optimal, 1 = Mäßig, 2 = Kritisch)")
    ax.set_xlim(0, 2.5)
    ax.set_xticks([0, 1, 2])
    ax.set_xticklabels(["0 (Optimal)", "1 (Mäßig)", "2 (Kritisch)"])
    ax.grid(axis='x', linestyle='--', alpha=0.5)

    st.pyplot(fig)

# --- QUELLEN-BOX AM ENDE ---
st.markdown("---")
with st.expander("📚 Offizielle Quellen- & Richtlinienangaben anzeigen"):
    st.write(
        "Dieser Gesundheits-Check orientiert sich an etablierten arbeitsmedizinischen und gesundheitlichen Richtlinien:")
    st.markdown(f"- **Ausgewählter Arbeitsbereich ({job}):** {quelle_info}")
    st.markdown("- **Arbeitsmedizinische Vorsorge:** Verordnung zur arbeitsmedizinischen Vorsorge (ArbMedVV)[cite: 3]")
    st.markdown(
        "- **Berufsgenossenschaftliche Grundsätze:** DGUV-Empfehlungen für arbeitsmedizinische Untersuchungen[cite: 3]")
    st.markdown(
        "- **Gefahrstoffe & Hautschutz:** Technische Regeln für Gefahrstoffe (TRGS 530) sowie BGW-Standards[cite: 3]")
    st.markdown(
        "- **Allgemeine Prävention:** Leitlinien der gesetzlichen Krankenversicherungen (GKV) zum Check-up[cite: 3]")