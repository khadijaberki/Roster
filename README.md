# 💼 RH App – Application de Gestion des Ressources Humaines

Application Django complète de gestion RH avec tableau de bord, gestion des employés, congés, paie et prédictions.

---

## ⚡ Installation Rapide

### 1. Cloner / Extraire le projet
```bash
cd rh_app
```

### 2. Créer un environnement virtuel
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Migrations de la base de données
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Peupler avec des données de démonstration
```bash
python seed_data.py
```

### 6. Lancer le serveur
```bash
python manage.py runserver
```

### 7. Accéder à l'application
- **Application** : http://127.0.0.1:8000/
- **Admin Django** : http://127.0.0.1:8000/admin/
- **Identifiants** : `admin` / `admin123`

---

## 📁 Structure du Projet

```
rh_app/
├── rh_app/              # Configuration Django
│   ├── settings.py
│   └── urls.py
├── employees/           # Application principale
│   ├── models.py        # Modèles: Employee, Congé, Paie, Prédiction
│   ├── views.py         # Vues et logique métier
│   ├── forms.py         # Formulaires
│   ├── urls.py          # Routes URL
│   └── admin.py         # Interface admin
├── templates/           # Templates HTML
│   ├── base.html        # Layout principal (sidebar + topbar)
│   ├── registration/
│   │   └── login.html
│   └── employees/
│       ├── dashboard.html
│       ├── employee_list.html
│       ├── conge_list.html
│       ├── paie_list.html
│       └── prediction_list.html
├── static/
│   └── css/style.css    # Styles CSS (design bleu professionnel)
├── seed_data.py         # Script de données de démonstration
├── requirements.txt
└── manage.py
```

---

## 🎯 Fonctionnalités

| Module         | Fonctionnalités                                               |
|----------------|---------------------------------------------------------------|
| **Dashboard**  | Stats globales, graphique par département, congés récents     |
| **Employés**   | Liste, recherche, ajout, modification, suppression            |
| **Congés**     | Demandes, approbation/refus, suivi par statut                 |
| **Paie**       | Bulletins de paie avec salaire, primes, déductions            |
| **Prédictions**| Score RH, résultats de prédiction, statut                     |

---

## 🛠️ Technologies

- **Backend** : Django 4.2
- **Base de données** : SQLite (développement) / PostgreSQL (production)
- **Frontend** : HTML/CSS vanilla + Chart.js
- **Authentification** : Django Auth intégré

---

## 🚀 Mise en Production

1. Changer `SECRET_KEY` dans `settings.py`
2. Mettre `DEBUG = False`
3. Configurer `ALLOWED_HOSTS`
4. Utiliser PostgreSQL
5. Exécuter `python manage.py collectstatic`
