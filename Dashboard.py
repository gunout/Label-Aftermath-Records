# dashboard_aftermath_records.py
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import re
from datetime import datetime
import warnings
import base64
import io
warnings.filterwarnings('ignore')

# Configuration de la page
st.set_page_config(
    page_title="ANALYSE STRATÉGIQUE - AFTERMATH ENTERTAINMENT",
    page_icon="🎧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé avec thème Aftermath (noir, or, premium)
st.markdown("""
<style>
    .main {
        color: #ffffff !important;
        background-color: #000000 !important;
    }
    
    .stApp {
        background-color: #000000 !important;
        color: #ffffff !important;
    }
    
    .main-header {
        font-size: 3rem;
        color: #FFD700 !important;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 700;
        border-bottom: 3px solid #FFD700;
        padding-bottom: 1rem;
        text-shadow: 0 0 20px rgba(255, 215, 0, 0.5);
        background: linear-gradient(90deg, #000000, #333300, #000000);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Arial Black', sans-serif;
    }
    
    .academic-card {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%);
        border: 1px solid #444444;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        box-shadow: 0 4px 15px rgba(255, 215, 0, 0.1);
        color: #ffffff !important;
        transition: all 0.3s ease;
    }
    
    .academic-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(255, 215, 0, 0.3);
        border-color: #FFD700;
    }
    
    .dre-card { 
        border-left: 5px solid #FFD700; 
        background: linear-gradient(135deg, #1a1a0a 0%, #2d2d1a 100%);
    }
    .eminem-card { 
        border-left: 5px solid #00FF00; 
        background: linear-gradient(135deg, #0a1a0a 0%, #1a2d1a 100%);
    }
    .kendrick-card { 
        border-left: 5px solid #4169E1; 
        background: linear-gradient(135deg, #0a0a1a 0%, #1a1a2d 100%);
    }
    .thegame-card { 
        border-left: 5px solid #FF4500; 
        background: linear-gradient(135deg, #1a0a0a 0%, #2d1a1a 100%);
    }
    .fifty-card { 
        border-left: 5px solid #C0C0C0; 
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
    }
    .busta-card { 
        border-left: 5px solid #9370DB; 
        background: linear-gradient(135deg, #0a0a1a 0%, #1a1a2d 100%);
    }
    
    .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        color: #FFD700 !important;
        margin: 0.5rem 0;
        text-shadow: 0 0 10px rgba(255, 215, 0, 0.5);
        font-family: 'Arial Black', sans-serif;
    }
    
    .section-title {
        color: #ffffff !important;
        border-bottom: 2px solid #FFD700;
        padding-bottom: 0.5rem;
        margin: 2rem 0 1rem 0;
        font-size: 1.6rem;
        font-weight: 600;
        text-shadow: 0 0 10px rgba(255, 215, 0, 0.2);
        font-family: 'Arial Black', sans-serif;
    }
    
    .subsection-title {
        color: #ffffff !important;
        border-left: 4px solid #FFD700;
        padding-left: 1rem;
        margin: 1.5rem 0 1rem 0;
        font-size: 1.3rem;
        font-weight: 600;
        font-family: 'Arial', sans-serif;
    }
    
    .stMarkdown {
        color: #ffffff !important;
    }
    
    p, div, span, h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
    }
    
    .secondary-text {
        color: #cccccc !important;
    }
    
    .light-text {
        color: #999999 !important;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
        background-color: #0a0a0a;
        border-radius: 8px;
        padding: 4px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #1a1a1a;
        border-radius: 5px;
        color: #ffffff !important;
        font-weight: 500;
        border: 1px solid #444444;
        transition: all 0.3s ease;
        font-family: 'Arial', sans-serif;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #2d2d2d;
        border-color: #FFD700;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #FFD700 !important;
        color: #000000 !important;
        font-weight: 600;
        border-color: #FFD700;
    }
    
    .card-content {
        color: #ffffff !important;
    }
    
    .card-secondary {
        color: #cccccc !important;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        color: #000000;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(255, 215, 0, 0.3);
        font-family: 'Arial', sans-serif;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #FFE44D 0%, #FFD700 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 215, 0, 0.5);
    }
    
    .stDataFrame {
        background-color: #0a0a0a;
        color: #ffffff;
    }
    
    .stSelectbox > div > div {
        background-color: #1a1a1a;
        color: #ffffff;
    }
    
    .stSlider > div > div > div {
        background-color: #FFD700;
    }
    
    /* Style pour les graphiques Plotly */
    .js-plotly-plot .plotly .modebar {
        background-color: rgba(10, 10, 10, 0.8) !important;
    }
    
    .js-plotly-plot .plotly .modebar-btn {
        background-color: transparent !important;
        color: #ffffff !important;
    }
    
    /* Aftermath Badge */
    .aftermath-badge {
        display: inline-block;
        background: #000000;
        color: #FFD700;
        padding: 5px 15px;
        border-radius: 20px;
        border: 2px solid #FFD700;
        font-weight: bold;
        font-size: 0.9rem;
        margin: 0 5px 10px 0;
        font-family: 'Arial', sans-serif;
    }
    
    /* Production Quality Indicator */
    .quality-indicator {
        display: inline-block;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        margin-right: 5px;
    }
    
    .quality-10 { background-color: #00FF00; }
    .quality-9 { background-color: #90EE90; }
    .quality-8 { background-color: #FFD700; }
    .quality-7 { background-color: #FFA500; }
    .quality-6 { background-color: #FF4500; }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: #0a0a0a;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #444444;
        border-radius: 6px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #555555;
    }
    
    /* Premium effect */
    .premium-glow {
        position: relative;
        overflow: hidden;
    }
    
    .premium-glow::before {
        content: '';
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        background: linear-gradient(45deg, #FFD700, #FFA500, #FFD700);
        z-index: -1;
        border-radius: 12px;
        opacity: 0.5;
    }
</style>
""", unsafe_allow_html=True)

class AftermathAnalyzer:
    def __init__(self):
        # Définition de la palette de couleurs pour Aftermath
        self.color_palette = {
            'DR. DRE': '#FFD700',        # Or
            'EMINEM': '#00FF00',         # Vert (Shady Records)
            'KENDRICK LAMAR': '#4169E1', # Bleu royal
            'THE GAME': '#FF4500',       # Orange rougeâtre
            '50 CENT': '#C0C0C0',        # Argent
            'BUSTA RHYMES': '#9370DB',   # Violet
            'ANDERSON .PAAK': '#FF69B4', # Rose
            'Période Classique': '#FFD700',
            'Période Moderne': '#4169E1'
        }
        
        # Couleurs pour les types de données
        self.data_colors = {
            'Ventes': '#FFD700',
            'Albums': '#4169E1',
            'Artistes': '#00FF00',
            'Revenus': '#FF4500',
            'Production': '#9370DB'
        }
        
        self.initialize_data()
        
    def initialize_data(self):
        """Initialise les données complètes sur Aftermath Entertainment"""
        
        # Données principales sur le label
        self.label_data = {
            'fondation': 1996,
            'fondateur': 'Dr. Dre',
            'statut': 'Label indépendant (filiale de Interscope/Universal)',
            'siege': 'Los Angeles, Californie, USA',
            'specialisation': 'Hip-hop de qualité, production premium',
            'philosophie': "Perfectionnisme, qualité sonore, excellence artistique",
            'distribution': 'Interscope Records, Universal Music Group'
        }

        # Données des artistes principaux
        self.artists_data = {
            'DR. DRE': {
                'debut': 1996,
                'genre': 'G-funk, West Coast hip-hop',
                'albums_aftermath': 2,
                'ventes_totales': 15000000,
                'succes_principal': '2001 (1999)',
                'statut': 'Fondateur et producteur exécutif',
                'impact': 'Producteur légendaire, perfectionniste sonore',
                'annees_activite': '1996-présent',
                'albums_principaux': ['2001', 'Compton'],
                'chiffre_affaires_estime': 80000000,
                'public_cible': 'Puristes, audiophiles',
                'tournees': 'Occasionnelles'
            },
            'EMINEM': {
                'debut': 1998,
                'genre': 'Hip-hop, Rap hardcore',
                'albums_aftermath': 11,
                'ventes_totales': 220000000,
                'succes_principal': 'The Marshall Mathers LP (2000)',
                'statut': 'Artiste le plus vendu du label',
                'impact': 'Artiste hip-hop le plus vendu de l\'histoire',
                'annees_activite': '1998-2024',
                'albums_principaux': ['The Marshall Mathers LP', 'The Eminem Show', 'Recovery'],
                'chiffre_affaires_estime': 500000000,
                'public_cible': 'Global, multigénérationnel',
                'tournees': 'Mondiales'
            },
            'KENDRICK LAMAR': {
                'debut': 2012,
                'genre': 'Hip-hop, Rap conscient',
                'albums_aftermath': 4,
                'ventes_totales': 25000000,
                'succes_principal': 'To Pimp a Butterfly (2015)',
                'statut': 'Artiste critique, lauréat Pulitzer',
                'impact': 'Renaissance du rap conscient',
                'annees_activite': '2012-présent',
                'albums_principaux': ['good kid, m.A.A.d city', 'To Pimp a Butterfly', 'DAMN.'],
                'chiffre_affaires_estime': 120000000,
                'public_cible': 'Critiques, intellectuels, grand public',
                'tournees': 'Mondiales'
            },
            'THE GAME': {
                'debut': 2004,
                'genre': 'Gangsta rap, West Coast hip-hop',
                'albums_aftermath': 3,
                'ventes_totales': 8000000,
                'succes_principal': 'The Documentary (2005)',
                'statut': 'Artiste West Coast réussi',
                'impact': 'Renaissance West Coast années 2000',
                'annees_activite': '2004-2008',
                'albums_principaux': ['The Documentary', 'Doctor\'s Advocate'],
                'chiffre_affaires_estime': 40000000,
                'public_cible': 'Fans de West Coast, street rap',
                'tournees': 'Nationales'
            },
            '50 CENT': {
                'debut': 2002,
                'genre': 'Hip-hop, Gangsta rap',
                'albums_aftermath': 2,
                'ventes_totales': 30000000,
                'succes_principal': 'Get Rich or Die Tryin\' (2003)',
                'statut': 'Phénomène commercial',
                'impact': 'Succès mainstream phénoménal',
                'annees_activite': '2002-2014',
                'albums_principaux': ['Get Rich or Die Tryin\'', 'The Massacre'],
                'chiffre_affaires_estime': 150000000,
                'public_cible': 'Mainstream, urbain',
                'tournees': 'Mondiales'
            },
            'BUSTA RHYMES': {
                'debut': 1998,
                'genre': 'Hip-hop, East Coast rap',
                'albums_aftermath': 1,
                'ventes_totales': 2000000,
                'succes_principal': 'Extinction Level Event (1998)',
                'statut': 'Artiste vétéran',
                'impact': 'Style unique et énergique',
                'annees_activite': '1998-2001',
                'albums_principaux': ['Extinction Level Event'],
                'chiffre_affaires_estime': 10000000,
                'public_cible': 'Fans de rap East Coast',
                'tournees': 'Nationales'
            },
            'ANDERSON .PAAK': {
                'debut': 2016,
                'genre': 'R&B, Soul, Hip-hop',
                'albums_aftermath': 1,
                'ventes_totales': 3000000,
                'succes_principal': 'Oxnard (2018)',
                'statut': 'Artiste éclectique moderne',
                'impact': 'Fusion R&B/Hip-hop',
                'annees_activite': '2016-présent',
                'albums_principaux': ['Oxnard'],
                'chiffre_affaires_estime': 15000000,
                'public_cible': 'Alternative, R&B moderne',
                'tournees': 'Mondiales'
            }
        }

        # Données chronologiques détaillées
        self.timeline_data = [
            {'annee': 1996, 'evenement': 'Fondation après le départ de Death Row', 'type': 'Structure', 'importance': 10},
            {'annee': 1998, 'evenement': 'Signature d\'Eminem', 'type': 'Artiste', 'importance': 10},
            {'annee': 1999, 'evenement': 'Sortie de 2001 (Dr. Dre)', 'type': 'Album', 'importance': 10},
            {'annee': 2000, 'evenement': 'The Marshall Mathers LP (Eminem)', 'type': 'Album', 'importance': 10},
            {'annee': 2002, 'evenement': 'Signature de 50 Cent', 'type': 'Artiste', 'importance': 9},
            {'annee': 2003, 'evenement': 'Get Rich or Die Tryin\' (50 Cent)', 'type': 'Album', 'importance': 9},
            {'annee': 2005, 'evenement': 'The Documentary (The Game)', 'type': 'Album', 'importance': 8},
            {'annee': 2011, 'evenement': 'Découverte de Kendrick Lamar', 'type': 'Artiste', 'importance': 9},
            {'annee': 2012, 'evenement': 'good kid, m.A.A.d city (Kendrick Lamar)', 'type': 'Album', 'importance': 9},
            {'annee': 2015, 'evenement': 'To Pimp a Butterfly (Kendrick Lamar)', 'type': 'Album', 'importance': 10},
            {'annee': 2015, 'evenement': 'Compton (Dr. Dre)', 'type': 'Album', 'importance': 8},
            {'annee': 2017, 'evenement': 'DAMN. (Kendrick Lamar) - Pulitzer', 'type': 'Album', 'importance': 10},
            {'annee': 2018, 'evenement': 'Signature d\'Anderson .Paak', 'type': 'Artiste', 'importance': 7},
            {'annee': 2022, 'evenement': 'Mr. Morale & The Big Steppers (Kendrick)', 'type': 'Album', 'importance': 9}
        ]

        # Données financières et commerciales
        self.financial_data = {
            'DR. DRE': {
                'ventes_albums': 15000000,
                'chiffre_affaires': 80000000,
                'rentabilite': 85,
                'cout_production_moyen': 3000000,
                'budget_marketing_moyen': 5000000,
                'roi': 600,
                'qualite_production': 10
            },
            'EMINEM': {
                'ventes_albums': 220000000,
                'chiffre_affaires': 500000000,
                'rentabilite': 95,
                'cout_production_moyen': 2000000,
                'budget_marketing_moyen': 8000000,
                'roi': 1200,
                'qualite_production': 9
            },
            'KENDRICK LAMAR': {
                'ventes_albums': 25000000,
                'chiffre_affaires': 120000000,
                'rentabilite': 90,
                'cout_production_moyen': 1500000,
                'budget_marketing_moyen': 3000000,
                'roi': 800,
                'qualite_production': 10
            },
            'THE GAME': {
                'ventes_albums': 8000000,
                'chiffre_affaires': 40000000,
                'rentabilite': 80,
                'cout_production_moyen': 800000,
                'budget_marketing_moyen': 2000000,
                'roi': 400,
                'qualite_production': 8
            },
            '50 CENT': {
                'ventes_albums': 30000000,
                'chiffre_affaires': 150000000,
                'rentabilite': 90,
                'cout_production_moyen': 1000000,
                'budget_marketing_moyen': 5000000,
                'roi': 1000,
                'qualite_production': 9
            },
            'BUSTA RHYMES': {
                'ventes_albums': 2000000,
                'chiffre_affaires': 10000000,
                'rentabilite': 70,
                'cout_production_moyen': 500000,
                'budget_marketing_moyen': 1000000,
                'roi': 200,
                'qualite_production': 8
            },
            'ANDERSON .PAAK': {
                'ventes_albums': 3000000,
                'chiffre_affaires': 15000000,
                'rentabilite': 75,
                'cout_production_moyen': 600000,
                'budget_marketing_moyen': 1200000,
                'roi': 250,
                'qualite_production': 9
            }
        }

        # Données de stratégie marketing
        self.marketing_data = {
            'DR. DRE': {
                'strategie': 'Perfectionnisme sonore, exclusivité, image légendaire',
                'cibles': 'Audiophiles, puristes, industrie musicale',
                'canaux': ['Production de luxe', 'Collaborations élites', 'Événements privés'],
                'budget_ratio': 25,
                'succes': 'Légendaire',
                'innovations': 'Marketing du silence (attente entre albums)'
            },
            'EMINEM': {
                'strategie': 'Controverses maîtrisées, storytelling intense, global',
                'cibles': 'Global, adolescents à adultes',
                'canaux': ['MTV', 'Radio mondiale', 'Médias traditionnels'],
                'budget_ratio': 30,
                'succes': 'Historique',
                'innovations': 'Marketing viral des paroles'
            },
            'KENDRICK LAMAR': {
                'strategie': 'Artiste critique, messages sociaux, exclusivité médiatique',
                'cibles': 'Intellectuels, activistes, grand public qualifié',
                'canaux': ['Prix littéraires', 'Presse qualité', 'Réseaux sociaux mystère'],
                'budget_ratio': 22,
                'succes': 'Exceptionnel',
                'innovations': 'Marketing par absence médiatique'
            },
            'THE GAME': {
                'strategie': 'Street credibility, West Coast revival, features prestigieuses',
                'cibles': 'Fans West Coast, street culture',
                'canaux': ['Mixtapes', 'Radio locale LA', 'Feuds publicitaires'],
                'budget_ratio': 20,
                'succes': 'Très bon',
                'innovations': 'Marketing par conflits médiatiques'
            },
            '50 CENT': {
                'strategie': 'Bad boy entrepreneur, viral marketing mixtapes',
                'cibles': 'Mainstream, aspirants entrepreneurs',
                'canaux': ['Mixtapes gratuites', 'Business ventures', 'TV réalité'],
                'budget_ratio': 28,
                'succes': 'Exceptionnel',
                'innovations': 'Street-to-boardroom marketing'
            },
            'BUSTA RHYMES': {
                'strategie': 'Énergie unique, collaborations variées, vétéran respecté',
                'cibles': 'Fans East Coast, vétérans hip-hop',
                'canaux': ['Features', 'Clips énergiques', 'Apparences TV'],
                'budget_ratio': 18,
                'succes': 'Bon',
                'innovations': 'Marketing par énergie scénique'
            },
            'ANDERSON .PAAK': {
                'strategie': 'Artiste éclectique, fusion genres, image positive',
                'cibles': 'Alternative, R&B moderne, festivals',
                'canaux': ['Festivals', 'Collaborations cross-genre', 'YouTube'],
                'budget_ratio': 21,
                'succes': 'Très bon',
                'innovations': 'Marketing par collaborations éclectiques'
            }
        }

        # Données de production
        self.production_data = {
            'DR. DRE': {
                'albums_produits': 2,
                'duree_contrat': 28,
                'rythme_sorties': '14 ans',
                'qualite_production': 10,
                'autonomie_artistique': 10,
                'support_label': 10,
                'temps_moyen_production': 36  # mois
            },
            'EMINEM': {
                'albums_produits': 11,
                'duree_contrat': 26,
                'rythme_sorties': '2-3 ans',
                'qualite_production': 9,
                'autonomie_artistique': 9,
                'support_label': 10,
                'temps_moyen_production': 24
            },
            'KENDRICK LAMAR': {
                'albums_produits': 4,
                'duree_contrat': 12,
                'rythme_sorties': '3 ans',
                'qualite_production': 10,
                'autonomie_artistique': 9,
                'support_label': 9,
                'temps_moyen_production': 36
            },
            'THE GAME': {
                'albums_produits': 3,
                'duree_contrat': 4,
                'rythme_sorties': '2 ans',
                'qualite_production': 8,
                'autonomie_artistique': 7,
                'support_label': 8,
                'temps_moyen_production': 18
            },
            '50 CENT': {
                'albums_produits': 2,
                'duree_contrat': 12,
                'rythme_sorties': '2 ans',
                'qualite_production': 9,
                'autonomie_artistique': 8,
                'support_label': 9,
                'temps_moyen_production': 18
            },
            'BUSTA RHYMES': {
                'albums_produits': 1,
                'duree_contrat': 3,
                'rythme_sorties': '3 ans',
                'qualite_production': 8,
                'autonomie_artistique': 7,
                'support_label': 7,
                'temps_moyen_production': 24
            },
            'ANDERSON .PAAK': {
                'albums_produits': 1,
                'duree_contrat': 6,
                'rythme_sorties': '6 ans',
                'qualite_production': 9,
                'autonomie_artistique': 8,
                'support_label': 8,
                'temps_moyen_production': 30
            }
        }

        # Données de gestion et management
        self.management_data = {
            'structure': {
                'type': 'Label boutique premium',
                'effectif': 25,
                'departements': ['Production', 'A&R', 'Marketing', 'Business Dev', 'Legal'],
                'processus_decision': 'Centralisé (Dr. Dre)',
                'culture_entreprise': 'Perfectionnisme, qualité, exclusivité'
            },
            'ressources_humaines': {
                'turnover': 'Très faible',
                'expertise': 'Production sonore d\'élite',
                'reseautage': 'Industrie mondiale premium',
                'formation': 'Apprentissage par mentorat Dre'
            },
            'finances': {
                'model_economique': 'Qualité over quantity, long-term artist development',
                'marge_nette': '30-35%',
                'investissement_artistes': 'Long terme, développement approfondi',
                'risque': 'Élevé (perfectionnisme coûteux)'
            },
            'relations_artistes': {
                'approche': 'Paternaliste, développement artistique complet',
                'contrats': 'Artist-friendly mais exigeants',
                'communication': 'Directe, professionnelle',
                'loyaute': 'Extrêmement forte'
            }
        }

    def display_header(self):
        """Affiche l'en-tête du dashboard"""
        st.markdown('<h1 class="main-header">🎧 AFTERMATH ENTERTAINMENT - DASHBOARD STRATÉGIQUE</h1>', unsafe_allow_html=True)
        st.markdown('<p style="text-align: center; color: #cccccc; font-size: 1.2rem; margin-bottom: 2rem; font-family: Arial, sans-serif;">Label de hip-hop américain - Analyse complète 1996-2024</p>', unsafe_allow_html=True)
        
        # Métriques principales
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_ventes = sum(self.financial_data[artist]['ventes_albums'] for artist in self.financial_data)
            st.markdown(f"""
            <div class="academic-card dre-card">
                <div style="color: {self.color_palette['DR. DRE']}; font-size: 1rem; font-weight: 600; text-align: center;">📀 VENTES TOTALES</div>
                <div class="metric-value" style="color: {self.color_palette['DR. DRE']}; text-align: center;">{total_ventes/1000000:.0f}M</div>
                <div style="color: #cccccc; text-align: center;">Albums vendus mondialement</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            total_artistes = len(self.artists_data)
            st.markdown(f"""
            <div class="academic-card eminem-card">
                <div style="color: {self.color_palette['EMINEM']}; font-size: 1rem; font-weight: 600; text-align: center;">🎤 ARTISTES</div>
                <div class="metric-value" style="color: {self.color_palette['EMINEM']}; text-align: center;">{total_artistes}</div>
                <div style="color: #cccccc; text-align: center;">Artistes principaux</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            total_albums = sum(self.artists_data[artist]['albums_aftermath'] for artist in self.artists_data)
            st.markdown(f"""
            <div class="academic-card kendrick-card">
                <div style="color: {self.color_palette['KENDRICK LAMAR']}; font-size: 1rem; font-weight: 600; text-align: center;">💿 ALBUMS</div>
                <div class="metric-value" style="color: {self.color_palette['KENDRICK LAMAR']}; text-align: center;">{total_albums}</div>
                <div style="color: #cccccc; text-align: center;">Produits par le label</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            chiffre_affaires_total = sum(self.financial_data[artist]['chiffre_affaires'] for artist in self.financial_data)
            st.markdown(f"""
            <div class="academic-card thegame-card">
                <div style="color: {self.color_palette['THE GAME']}; font-size: 1rem; font-weight: 600; text-align: center;">💰 CHIFFRE D'AFFAIRES</div>
                <div class="metric-value" style="color: {self.color_palette['THE GAME']}; text-align: center;">{chiffre_affaires_total/1000000:.0f}M$</div>
                <div style="color: #cccccc; text-align: center;">Estimé sur la période</div>
            </div>
            """, unsafe_allow_html=True)

    def create_artist_analysis(self):
        """Analyse complète des artistes"""
        st.markdown('<h3 class="section-title">🎤 ANALYSE DU PORTFOLIO ARTISTES</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="subsection-title">📊 Performance Commerciale</div>', unsafe_allow_html=True)
            self.create_sales_comparison_chart()
        
        with col2:
            st.markdown('<div class="subsection-title">📈 Rentabilité et Qualité</div>', unsafe_allow_html=True)
            self.create_quality_roi_chart()
        
        # Analyse détaillée par artiste
        st.markdown('<div class="subsection-title">🔍 Analyse Détailée par Artiste</div>', unsafe_allow_html=True)
        self.create_detailed_artist_analysis()

    def create_sales_comparison_chart(self):
        """Graphique de comparaison des ventes"""
        artists = list(self.artists_data.keys())
        ventes = [self.financial_data[artist]['ventes_albums'] for artist in artists]
        
        # Convertir en millions pour meilleure lisibilité
        ventes_millions = [v/1000000 for v in ventes]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=artists,
            y=ventes_millions,
            marker_color=[self.color_palette[artist] for artist in artists],
            text=[f"{v:.1f}M" for v in ventes_millions],
            textposition='auto',
            textfont=dict(color='white', size=14, weight='bold')
        ))
        
        fig.update_layout(
            title='Ventes Totalisées par Artiste (en millions)',
            xaxis_title='Artistes',
            yaxis_title="Albums vendus (millions)",
            paper_bgcolor='#1a1a1a',
            plot_bgcolor='#0a0a0a',
            font=dict(color='#ffffff', size=14),
            height=400,
            showlegend=False,
            xaxis=dict(tickfont=dict(size=12), gridcolor='#333333'),
            yaxis=dict(tickfont=dict(size=12), gridcolor='#333333')
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def create_quality_roi_chart(self):
        """Graphique qualité vs ROI"""
        artists = list(self.financial_data.keys())
        roi = [self.financial_data[artist]['roi'] for artist in artists]
        qualite = [self.financial_data[artist]['qualite_production'] for artist in artists]
        
        fig = go.Figure()
        
        for i, artist in enumerate(artists):
            fig.add_trace(go.Scatter(
                x=[roi[i]],
                y=[qualite[i]],
                mode='markers+text',
                marker=dict(
                    size=80, 
                    color=self.color_palette[artist], 
                    opacity=0.9,
                    line=dict(width=3, color='#ffffff')
                ),
                text=[artist],
                textposition="middle center",
                textfont=dict(color='white', size=12, weight='bold'),
                name=artist,
                showlegend=True
            ))
        
        fig.update_layout(
            title='ROI vs Qualité de Production',
            xaxis_title='Retour sur Investissement (%)',
            yaxis_title='Qualité de Production (1-10)',
            paper_bgcolor='#1a1a1a',
            plot_bgcolor='#0a0a0a',
            font=dict(color='#ffffff', size=14),
            height=400,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                bgcolor='rgba(26, 26, 26, 0.9)',
                bordercolor='#FFD700',
                borderwidth=1,
                font=dict(color='white', size=10)
            ),
            xaxis=dict(range=[150, 1300], tickfont=dict(size=12), gridcolor='#333333'),
            yaxis=dict(range=[7, 10.5], tickfont=dict(size=12), gridcolor='#333333')
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def create_detailed_artist_analysis(self):
        """Analyse détaillée par artiste"""
        artists = list(self.artists_data.keys())
        tabs = st.tabs(artists)
        
        for i, artist in enumerate(artists):
            with tabs[i]:
                couleur = self.color_palette[artist]
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Informations générales
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, {couleur}20 0%, {couleur}05 100%); padding: 1rem; border-radius: 8px; border-left: 5px solid {couleur}; margin-bottom: 1rem;">
                        <div style="color: {couleur}; font-weight: bold; font-size: 1.5rem; margin-bottom: 0.5rem;">{artist}</div>
                        <div style="color: #cccccc; font-size: 1.1rem; font-weight: 500;">{self.artists_data[artist]['genre']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Métriques clés
                    st.metric("Albums chez Aftermath", self.artists_data[artist]['albums_aftermath'])
                    st.metric("Ventes totales", f"{self.financial_data[artist]['ventes_albums']/1000000:.1f}M")
                    st.metric("Qualité production", f"{self.financial_data[artist]['qualite_production']}/10")
                    
                    # Succès principal
                    st.markdown(f"""
                    <div style="background: #1a1a1a; padding: 1rem; border-radius: 8px; margin-top: 1rem; border: 1px solid #333333;">
                        <div style="font-weight: bold; color: {couleur}; margin-bottom: 0.5rem;">Succès Principal:</div>
                        <div style="color: #ffffff; font-style: italic; font-size: 1.1rem;">{self.artists_data[artist]['succes_principal']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    # Caractéristiques commerciales
                    st.markdown(f"""
                    <div style="background: #1a1a1a; padding: 1rem; border-radius: 8px; border: 1px solid #333333;">
                        <div style="font-weight: bold; color: {couleur}; margin-bottom: 0.5rem;">Performance Commerciale:</div>
                        <ul style="color: #ffffff; font-weight: 500;">
                            <li>Rentabilité: {self.financial_data[artist]['rentabilite']}%</li>
                            <li>ROI: {self.financial_data[artist]['roi']}%</li>
                            <li>Coût production: {self.financial_data[artist]['cout_production_moyen']/1000:.0f}k$</li>
                            <li>Budget marketing: {self.financial_data[artist]['budget_marketing_moyen']/1000:.0f}k$</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Graphique radar des caractéristiques
                    categories = ['Ventes', 'Qualité', 'ROI', 'Innovation']
                    valeurs = [
                        min(100, self.financial_data[artist]['ventes_albums'] / 2200000),  # Normalisé
                        self.financial_data[artist]['qualite_production'] * 10,
                        min(100, self.financial_data[artist]['roi'] / 13),
                        100 if self.marketing_data[artist]['innovations'] in ['Marketing du silence', 'Marketing viral', 'Marketing par absence'] else
                        80 if self.marketing_data[artist]['innovations'] in ['Street-to-boardroom', 'Marketing par conflits'] else
                        70
                    ]
                    
                    fig = go.Figure()
                    
                    fig.add_trace(go.Scatterpolar(
                        r=valeurs + [valeurs[0]],
                        theta=categories + [categories[0]],
                        fill='toself',
                        line=dict(color=couleur, width=3),
                        marker=dict(size=8, color=couleur),
                        name=artist
                    ))
                    
                    fig.update_layout(
                        polar=dict(
                            bgcolor='#1a1a1a',
                            radialaxis=dict(
                                visible=True, 
                                range=[0, 100],
                                gridcolor='#333333',
                                tickfont=dict(color='#ffffff', size=12),
                                linecolor='#444444'
                            ),
                            angularaxis=dict(
                                gridcolor='#333333',
                                tickfont=dict(color='#ffffff', size=12),
                                linecolor='#444444'
                            )
                        ),
                        paper_bgcolor='#0a0a0a',
                        font=dict(color='#ffffff', size=14),
                        showlegend=False,
                        height=300,
                        title=f"Profil Artistique - {artist}"
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)

    def create_production_analysis(self):
        """Analyse de la production"""
        st.markdown('<h3 class="section-title">🏭 ANALYSE DE LA PRODUCTION</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="subsection-title">⏱️ Temps de Production</div>', unsafe_allow_html=True)
            self.create_production_timeline()
        
        with col2:
            st.markdown('<div class="subsection-title">⚙️ Qualité vs Support</div>', unsafe_allow_html=True)
            self.create_quality_support_chart()
        
        # Analyse des coûts
        st.markdown('<div class="subsection-title">💰 Investissement vs Retour</div>', unsafe_allow_html=True)
        self.create_investment_return_analysis()

    def create_production_timeline(self):
        """Timeline des temps de production"""
        artists = list(self.production_data.keys())
        temps_production = [self.production_data[artist]['temps_moyen_production'] for artist in artists]
        albums = [self.production_data[artist]['albums_produits'] for artist in artists]
        
        fig = go.Figure()
        
        for i, artist in enumerate(artists):
            fig.add_trace(go.Scatter(
                x=[temps_production[i]],
                y=[albums[i]],
                mode='markers+text',
                marker=dict(
                    size=60, 
                    color=self.color_palette[artist], 
                    opacity=0.9,
                    line=dict(width=2, color='#ffffff')
                ),
                text=[artist],
                textposition="middle center",
                textfont=dict(color='white', size=10, weight='bold'),
                name=artist
            ))
        
        fig.update_layout(
            title='Temps de Production vs Nombre d\'Albums',
            xaxis_title='Temps moyen de production (mois)',
            yaxis_title="Nombre d'albums produits",
            paper_bgcolor='#1a1a1a',
            plot_bgcolor='#0a0a0a',
            font=dict(color='#ffffff', size=14),
            height=400,
            showlegend=False,
            xaxis=dict(tickfont=dict(size=12), gridcolor='#333333'),
            yaxis=dict(tickfont=dict(size=12), gridcolor='#333333')
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def create_quality_support_chart(self):
        """Graphique qualité vs support"""
        artists = list(self.production_data.keys())
        qualite = [self.production_data[artist]['qualite_production'] for artist in artists]
        support = [self.production_data[artist]['support_label'] for artist in artists]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=qualite,
            y=support,
            mode='markers+text',
            marker=dict(
                size=60,
                color=[self.color_palette[artist] for artist in artists],
                opacity=0.9
            ),
            text=artists,
            textposition="top center",
            textfont=dict(color='white', size=10, weight='bold')
        ))
        
        fig.update_layout(
            title='Qualité de Production vs Support du Label',
            xaxis_title='Qualité de Production (1-10)',
            yaxis_title='Support du Label (1-10)',
            paper_bgcolor='#1a1a1a',
            plot_bgcolor='#0a0a0a',
            font=dict(color='#ffffff', size=14),
            height=400,
            showlegend=False,
            xaxis=dict(range=[7, 10.5], tickfont=dict(size=12), gridcolor='#333333'),
            yaxis=dict(range=[6, 10.5], tickfont=dict(size=12), gridcolor='#333333')
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def create_investment_return_analysis(self):
        """Analyse investissement vs retour"""
        artists = list(self.financial_data.keys())
        investissements = [self.financial_data[artist]['cout_production_moyen'] + self.financial_data[artist]['budget_marketing_moyen'] for artist in artists]
        revenus = [self.financial_data[artist]['chiffre_affaires'] for artist in artists]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='Investissement Total',
            x=artists,
            y=investissements,
            marker_color='#FFD700',
            text=[f"{v/1000:.0f}k$" for v in investissements],
            textposition='auto',
            textfont=dict(color='white', size=10, weight='bold')
        ))
        
        fig.add_trace(go.Bar(
            name='Revenus Générés',
            x=artists,
            y=revenus,
            marker_color='#4169E1',
            text=[f"{v/1000000:.1f}M$" for v in revenus],
            textposition='auto',
            textfont=dict(color='white', size=10, weight='bold')
        ))
        
        fig.update_layout(
            barmode='group',
            title='Investissement vs Revenus par Artiste',
            xaxis_title='Artistes',
            yaxis_title='Montant ($)',
            paper_bgcolor='#1a1a1a',
            plot_bgcolor='#0a0a0a',
            font=dict(color='#ffffff', size=14),
            height=400,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                bgcolor='rgba(26, 26, 26, 0.9)',
                bordercolor='#FFD700',
                borderwidth=1,
                font=dict(color='white', size=12)
            ),
            xaxis=dict(tickfont=dict(size=10), gridcolor='#333333'),
            yaxis=dict(tickfont=dict(size=10), gridcolor='#333333')
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def create_marketing_analysis(self):
        """Analyse des stratégies marketing"""
        st.markdown('<h3 class="section-title">🎯 ANALYSE DES STRATÉGIES MARKETING</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="subsection-title">📢 Stratégies par Artiste</div>', unsafe_allow_html=True)
            self.create_marketing_strategies_chart()
        
        with col2:
            st.markdown('<div class="subsection-title">🎪 Canaux de Distribution</div>', unsafe_allow_html=True)
            self.create_marketing_channels_analysis()
        
        # Analyse détaillée par stratégie
        st.markdown('<div class="subsection-title">🔍 Innovations Marketing</div>', unsafe_allow_html=True)
        self.create_marketing_innovations_analysis()

    def create_marketing_strategies_chart(self):
        """Graphique des stratégies marketing"""
        artists = list(self.marketing_data.keys())
        budget_ratios = [self.marketing_data[artist]['budget_ratio'] for artist in artists]
        succes = [10 if self.marketing_data[artist]['succes'] == 'Historique' else 
                 9 if self.marketing_data[artist]['succes'] == 'Légendaire' else
                 8 if self.marketing_data[artist]['succes'] == 'Exceptionnel' else
                 7 if self.marketing_data[artist]['succes'] == 'Très bon' else
                 6 for artist in artists]
        
        fig = go.Figure()
        
        for i, artist in enumerate(artists):
            fig.add_trace(go.Scatter(
                x=[budget_ratios[i]],
                y=[succes[i]],
                mode='markers+text',
                marker=dict(
                    size=80, 
                    color=self.color_palette[artist], 
                    opacity=0.9,
                    line=dict(width=3, color='#ffffff')
                ),
                text=[artist],
                textposition="middle center",
                textfont=dict(color='white', size=10, weight='bold'),
                name=artist
            ))
        
        fig.update_layout(
            title='Budget Marketing vs Succès Commercial',
            xaxis_title='Ratio Budget Marketing (%)',
            yaxis_title='Niveau de Succès (1-10)',
            paper_bgcolor='#1a1a1a',
            plot_bgcolor='#0a0a0a',
            font=dict(color='#ffffff', size=14),
            height=400,
            showlegend=False,
            xaxis=dict(range=[17, 35], tickfont=dict(size=12), gridcolor='#333333'),
            yaxis=dict(range=[5, 11], tickfont=dict(size=12), gridcolor='#333333')
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def create_marketing_channels_analysis(self):
        """Analyse des canaux marketing"""
        # Compter les canaux les plus utilisés
        canaux_count = {}
        for artist_data in self.marketing_data.values():
            for canal in artist_data['canaux']:
                canaux_count[canal] = canaux_count.get(canal, 0) + 1
        
        canaux = list(canaux_count.keys())
        counts = list(canaux_count.values())
        
        fig = go.Figure(go.Bar(
            x=counts,
            y=canaux,
            orientation='h',
            marker_color='#9370DB',
            text=counts,
            textposition='auto',
            textfont=dict(color='white', size=12, weight='bold')
        ))
        
        fig.update_layout(
            title='Canaux Marketing les Plus Utilisés',
            xaxis_title="Nombre d'artistes utilisant le canal",
            yaxis_title='Canaux Marketing',
            paper_bgcolor='#1a1a1a',
            plot_bgcolor='#0a0a0a',
            font=dict(color='#ffffff', size=14),
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def create_marketing_innovations_analysis(self):
        """Analyse des innovations marketing"""
        innovations = {}
        for artist, data in self.marketing_data.items():
            innovation = data['innovations']
            if innovation not in innovations:
                innovations[innovation] = []
            innovations[innovation].append(artist)
        
        # Afficher les innovations
        col1, col2 = st.columns(2)
        
        with col1:
            for i, (innovation, artists_list) in enumerate(list(innovations.items())[:len(innovations)//2]):
                st.markdown(f"""
                <div class="academic-card">
                    <h4 style="color: #FFD700; text-align: center; font-weight: bold;">✨ {innovation.upper()}</h4>
                    <p style="color: #cccccc; text-align: center;">Utilisé par:</p>
                    <div style="text-align: center;">
                        {', '.join(artists_list)}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            for i, (innovation, artists_list) in enumerate(list(innovations.items())[len(innovations)//2:]):
                st.markdown(f"""
                <div class="academic-card">
                    <h4 style="color: #FFD700; text-align: center; font-weight: bold;">✨ {innovation.upper()}</h4>
                    <p style="color: #cccccc; text-align: center;">Utilisé par:</p>
                    <div style="text-align: center;">
                        {', '.join(artists_list)}
                    </div>
                </div>
                """, unsafe_allow_html=True)

    def create_management_analysis(self):
        """Analyse de la gestion et management"""
        st.markdown('<h3 class="section-title">🏢 ANALYSE DE LA GESTION</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="subsection-title">📊 Structure Organisationnelle</div>', unsafe_allow_html=True)
            self.create_org_structure()
        
        with col2:
            st.markdown('<div class="subsection-title">💼 Modèle Économique Premium</div>', unsafe_allow_html=True)
            self.create_economic_model()
        
        # Analyse SWOT
        st.markdown('<div class="subsection-title">🔍 Analyse SWOT du Label</div>', unsafe_allow_html=True)
        self.create_swot_analysis()

    def create_org_structure(self):
        """Structure organisationnelle"""
        # Créer un graphique pour la structure organisationnelle
        fig = go.Figure()
        
        # Niveaux hiérarchiques
        niveaux = ['Fondation', 'Production', 'Artistes', 'Support']
        
        # Positions
        positions_x = [1, 2, 3, 4]
        positions_y = [4, 3, 2, 1]
        
        fig.add_trace(go.Scatter(
            x=positions_x,
            y=positions_y,
            mode='markers+text',
            marker=dict(
                size=[60, 40, 50, 30],
                color=['#FFD700', '#4169E1', '#00FF00', '#9370DB'],
                opacity=0.9,
                line=dict(width=2, color='#ffffff')
            ),
            text=niveaux,
            textposition="middle center",
            textfont=dict(color='white', size=12, weight='bold'),
            showlegend=False
        ))
        
        # Ajouter les lignes de connexion
        for i in range(len(positions_x)-1):
            fig.add_shape(type="line", 
                         x0=positions_x[i], y0=positions_y[i],
                         x1=positions_x[i+1], y1=positions_y[i+1],
                         line=dict(color="#ffffff", width=2, dash="dash"))
        
        fig.update_layout(
            title='Structure Hiérarchique - Approche Top-Down',
            paper_bgcolor='#1a1a1a',
            plot_bgcolor='#0a0a0a',
            font=dict(color='#ffffff', size=14),
            height=350,
            showlegend=False,
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def create_economic_model(self):
        """Modèle économique"""
        # Créer un graphique pour le modèle économique
        categories = ['Revenus', 'Coûts Production', 'Marketing', 'Marge']
        valeurs = [100, 45, 25, 30]  # Valeurs en pourcentage
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=categories,
            y=valeurs,
            marker_color=['#FFD700', '#4169E1', '#00FF00', '#9370DB'],
            text=[f"{v}%" for v in valeurs],
            textposition='auto',
            textfont=dict(color='white', size=12, weight='bold')
        ))
        
        fig.update_layout(
            title='Répartition Économique - Modèle Premium',
            xaxis_title='Catégories',
            yaxis_title='Pourcentage (%)',
            paper_bgcolor='#1a1a1a',
            plot_bgcolor='#0a0a0a',
            font=dict(color='#ffffff', size=14),
            height=300,
            showlegend=False,
            xaxis=dict(tickfont=dict(size=12), gridcolor='#333333'),
            yaxis=dict(tickfont=dict(size=12), gridcolor='#333333')
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def create_swot_analysis(self):
        """Analyse SWOT"""
        # Créer un graphique radar pour l'analyse SWOT
        categories = ['Forces', 'Faiblesses', 'Opportunités', 'Menaces']
        valeurs = [10, 6, 8, 5]  # Scores sur 10
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=valeurs + [valeurs[0]],
            theta=categories + [categories[0]],
            fill='toself',
            line=dict(color='#FFD700', width=3),
            marker=dict(size=8, color='#FFD700'),
            name='Analyse SWOT'
        ))
        
        fig.update_layout(
            polar=dict(
                bgcolor='#1a1a1a',
                radialaxis=dict(
                    visible=True, 
                    range=[0, 10],
                    gridcolor='#333333',
                    tickfont=dict(color='#ffffff', size=12),
                    linecolor='#444444'
                ),
                angularaxis=dict(
                    gridcolor='#333333',
                    tickfont=dict(color='#ffffff', size=12),
                    linecolor='#444444'
                )
            ),
            paper_bgcolor='#0a0a0a',
            font=dict(color='#ffffff', size=14),
            showlegend=False,
            height=400,
            title="Analyse SWOT - Label Premium"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Afficher les détails de l'analyse SWOT
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div class="academic-card dre-card">
                <h4 style="color: #FFD700; text-align: center; font-weight: bold;">FORCES</h4>
                <ul style="color: #ffffff; font-weight: 500;">
                    <li>Dr. Dre - producteur légendaire</li>
                    <li>Qualité sonore inégalée</li>
                    <li>Artistes d'élite (Eminem, Kendrick)</li>
                    <li>Réputation d'excellence</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="academic-card eminem-card">
                <h4 style="color: #00FF00; text-align: center; font-weight: bold;">FAIBLESSES</h4>
                <ul style="color: #ffffff; font-weight: 500;">
                    <li>Sorties très espacées</li>
                    <li>Coûts de production élevés</li>
                    <li>Portefeuille limité d'artistes</li>
                    <li>Dépendance aux superstars</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="academic-card kendrick-card">
                <h4 style="color: #4169E1; text-align: center; font-weight: bold;">OPPORTUNITÉS</h4>
                <ul style="color: #ffffff; font-weight: 500;">
                    <li>Audio haute résolution</li>
                    <li>Formation production premium</li>
                    <li>Collaborations luxe</li>
                    <li>Expansion internationale</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div class="academic-card thegame-card">
                <h4 style="color: #FF4500; text-align: center; font-weight: bold;">MENACES</h4>
                <ul style="color: #ffffff; font-weight: 500;">
                    <li>Concurrence streaming low-cost</li>
                    <li>Changement des habitudes d'écoute</li>
                    <li>Vieillissement des stars</li>
                    <li>Économie de l'attention</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

    def create_timeline_analysis(self):
        """Analyse chronologique"""
        st.markdown('<h3 class="section-title">📅 ANALYSE CHRONOLOGIQUE</h3>', unsafe_allow_html=True)
        
        # Créer un DataFrame pour la timeline
        df_timeline = pd.DataFrame(self.timeline_data)
        
        fig = go.Figure()
        
        # Ajouter les événements par type
        for event_type in df_timeline['type'].unique():
            df_type = df_timeline[df_timeline['type'] == event_type]
            fig.add_trace(go.Scatter(
                x=df_type['annee'],
                y=df_type['importance'],
                mode='markers+text',
                marker=dict(
                    size=df_type['importance'] * 8,
                    color=self.data_colors.get(event_type, '#ffffff'),
                    opacity=0.8,
                    line=dict(width=2, color='#ffffff')
                ),
                text=df_type['evenement'],
                textposition="top center",
                textfont=dict(color='white', size=10),
                name=event_type,
                showlegend=True
            ))
        
        fig.update_layout(
            title='Timeline Événements Clés - Philosophie "Quality over Quantity"',
            xaxis_title='Année',
            yaxis_title='Importance (1-10)',
            paper_bgcolor='#1a1a1a',
            plot_bgcolor='#0a0a0a',
            font=dict(color='#ffffff', size=14),
            height=500,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                bgcolor='rgba(26, 26, 26, 0.9)',
                bordercolor='#FFD700',
                borderwidth=1,
                font=dict(color='white', size=12)
            ),
            xaxis=dict(range=[1995, 2023], tickfont=dict(size=12), gridcolor='#333333'),
            yaxis=dict(range=[0, 11], tickfont=dict(size=12), gridcolor='#333333')
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def create_conclusions(self):
        """Conclusions et recommandations"""
        st.markdown('<h3 class="section-title">📝 CONCLUSIONS ET RECOMMANDATIONS</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="academic-card dre-card">
                <h4 style="color: #FFD700; text-align: center; font-weight: bold;">🎯 POINTS CLÉS</h4>
                <ul style="color: #ffffff; font-weight: 500;">
                    <li>Aftermath = excellence sonore et artistique</li>
                    <li>Modèle "quality over quantity" réussi</li>
                    <li>Découverte et développement de superstars</li>
                    <li>Influence majeure sur l'industrie musicale</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="academic-card eminem-card">
                <h4 style="color: #00FF00; text-align: center; font-weight: bold;">💡 LEÇONS APPRISES</h4>
                <ul style="color: #ffffff; font-weight: 500;">
                    <li>La patience est rentable (14 ans entre albums Dre)</li>
                    <li>L'excellence attire l'excellence</li>
                    <li>Le développement artistique paye à long terme</li>
                    <li>La réputation vaut plus que la quantité</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="academic-card kendrick-card">
                <h4 style="color: #4169E1; text-align: center; font-weight: bold;">🚀 RECOMMANDATIONS STRATÉGIQUES</h4>
                <ul style="color: #ffffff; font-weight: 500;">
                    <li>Développer une académie de production</li>
                    <li>Explorer l'audio haute résolution</li>
                    <li>Créer des collaborations intergénérationnelles</li>
                    <li>Capitaliser sur le streaming premium</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="academic-card thegame-card">
                <h4 style="color: #FF4500; text-align: center; font-weight: bold;">🔮 PERSPECTIVES D'AVENIR</h4>
                <ul style="color: #ffffff; font-weight: 500;">
                    <li>Transition vers école de production premium</li>
                    <li>Développement de technologies audio</li>
                    <li>Expansion dans le contenu éducatif</li>
                    <li>Positionnement comme référence qualité</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

    def run(self):
        """Fonction principale pour exécuter le dashboard"""
        self.display_header()
        
        # Créer les onglets principaux
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "🎤 Artistes", 
            "🏭 Production", 
            "🎯 Marketing", 
            "🏢 Gestion", 
            "📅 Timeline", 
            "📝 Conclusions"
        ])
        
        with tab1:
            self.create_artist_analysis()
        
        with tab2:
            self.create_production_analysis()
        
        with tab3:
            self.create_marketing_analysis()
        
        with tab4:
            self.create_management_analysis()
        
        with tab5:
            self.create_timeline_analysis()
        
        with tab6:
            self.create_conclusions()
        
        # Footer
        st.markdown("""
        <div style="text-align: center; margin-top: 3rem; padding: 2rem; background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%); border-radius: 10px; border: 1px solid #444444;">
            <p style="color: #FFD700; font-weight: bold; font-size: 1.2rem; font-family: 'Arial Black', sans-serif;">AFTERMATH ENTERTAINMENT - Dashboard Stratégique</p>
            <p style="color: #cccccc; margin-top: 0.5rem; font-family: Arial, sans-serif;">Analyse complète 1996-2024 | Label de hip-hop premium</p>
            <div style="margin-top: 1rem;">
                <span class="aftermath-badge">DR. DRE</span>
                <span class="aftermath-badge">EMINEM</span>
                <span class="aftermath-badge">KENDRICK LAMAR</span>
            </div>
            <p style="color: #999999; margin-top: 1rem; font-size: 0.9rem;">© 2024 - Tous droits réservés | Philosophie: Quality Over Quantity</p>
        </div>
        """, unsafe_allow_html=True)

# Point d'entrée principal
if __name__ == "__main__":
    analyzer = AftermathAnalyzer()
    analyzer.run()
