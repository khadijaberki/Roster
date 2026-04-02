#!/usr/bin/env python
"""
Script de peuplement de la base de données avec des données de démonstration.
Exécuter: python seed_data.py
"""
import os
import sys
import django
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rh_app.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.contrib.auth.models import User
from employees.models import Department, Employee, CongeRequest, BulletinPaie, Prediction

print("🌱 Peuplement de la base de données...")

# Superuser
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@rh.ma', 'admin123')
    print("✅ Superuser créé: admin / admin123")

# Departments
depts = {}
for name in ['Informatique', 'Marketing', 'Administratif', 'Commercial']:
    d, _ = Department.objects.get_or_create(name=name)
    depts[name] = d
print("✅ Départements créés")

# Employees
employees_data = [
    ('Alice Durant',   'alice@rh.ma',  'Informatique',  'Développeur',         date(2020,3,15),  8500),
    ('Benoît Lefèvre', 'benoit@rh.ma', 'Informatique',  'Chef de Projet',      date(2019,7,1),   11000),
    ('Clara Moreau',   'clara@rh.ma',  'Marketing',     'Responsable Marketing',date(2021,1,10), 9000),
    ('David Lambert',  'david@rh.ma',  'Commercial',    'Commercial',          date(2022,4,20),  7500),
    ('Emma Dubois',    'emma@rh.ma',   'Commercial',    'Conseillère Vente',   date(2023,2,5),   7000),
    ('Fatima Zohra',   'fatima@rh.ma', 'Administratif', 'Assistante RH',       date(2020,9,1),   8000),
    ('Karim Alami',    'karim@rh.ma',  'Informatique',  'Data Analyst',        date(2021,6,15),  9500),
]

created_emps = []
for name, email, dept, poste, date_emb, salaire in employees_data:
    emp, _ = Employee.objects.get_or_create(
        email=email,
        defaults={
            'name': name,
            'department': depts[dept],
            'poste': poste,
            'date_embauche': date_emb,
            'salaire': salaire,
            'status': 'actif',
        }
    )
    created_emps.append(emp)
print(f"✅ {len(created_emps)} employés créés")

# Congés
conges_data = [
    (created_emps[2], date(2025,12,20), date(2025,12,30), 'Vacances de Noël',  'Approuvé'),
    (created_emps[3], date(2025,12,20), date(2025,12,31), 'Congé annuel',      'En attente'),
    (created_emps[4], date(2025,12,28), date(2026,1,12),  'Congé médical',     'Refusé'),
    (created_emps[0], date(2026,1,5),   date(2026,1,15),  'Formation externe', 'En attente'),
    (created_emps[5], date(2026,2,1),   date(2026,2,14),  'Congé maternité',   'Approuvé'),
]

for emp, dd, df, motif, status in conges_data:
    CongeRequest.objects.get_or_create(
        employee=emp, date_debut=dd, date_fin=df,
        defaults={'motif': motif, 'status': status}
    )
print("✅ Demandes de congé créées")

# Bulletins de paie
for emp in created_emps[:5]:
    for mois in ['Janvier', 'Février', 'Mars']:
        BulletinPaie.objects.get_or_create(
            employee=emp, mois=mois, annee=2026,
            defaults={
                'salaire_base': emp.salaire,
                'primes': 500,
                'deductions': 200,
                'net_a_payer': emp.salaire + 300,
            }
        )
print("✅ Bulletins de paie créés")

# Prédictions
predictions_data = [
    (created_emps[1], 75, 'Promotion',  'Satisfaisant',  date(2023,3,8)),
    (created_emps[2], 83, 'Promotion',  'Satisfaisant',  date(2025,5,8)),
    (created_emps[4], 50, 'Évaluation', 'À surveiller',  date(2000,8,25)),
    (created_emps[0], 91, 'Promotion',  'Satisfaisant',  date(2026,1,15)),
    (created_emps[3], 38, 'Départ',     'À surveiller',  date(2026,2,20)),
]

for emp, score, resultat, status, date_pred in predictions_data:
    Prediction.objects.get_or_create(
        employee=emp, date_prediction=date_pred,
        defaults={'score': score, 'resultat': resultat, 'status': status}
    )
print("✅ Prédictions créées")

print("\n🎉 Base de données peuplée avec succès !")
print("   Identifiants: admin / admin123")
print("   Lancez: python manage.py runserver")

# ModelePrediction
from employees.models import ModelePrediction
ModelePrediction.objects.get_or_create(
    nom_modele='Logistic Regression',
    defaults={
        'precision': 87.2,
        'date_entrainement': date(2025, 3, 1),
        'fichier_modele': 'modele_logistic_regression.pkl',
        'description': 'Modèle entraîné sur IBM HR Analytics Dataset avec SMOTE + StandardScaler.',
        'actif': True,
    }
)
print("✅ Modèle ML enregistré")
