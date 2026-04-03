from django import forms
from .models import Employee, CongeRequest, BulletinPaie, Prediction, Document, ModelePrediction



class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = [
            'name', 'email', 'department', 'poste', 'date_embauche', 'salaire', 'status', 'photo',
            'age', 'gender', 'marital_status', 'distance_from_home', 'education', 'education_field',
            'job_role', 'job_level', 'business_travel', 'overtime',
            'daily_rate', 'hourly_rate', 'monthly_income', 'monthly_rate',
            'percent_salary_hike', 'stock_option_level',
            'total_working_years', 'num_companies_worked', 'years_at_company',
            'years_in_current_role', 'years_since_last_promotion', 'years_with_curr_manager',
            'training_times_last_year',
            'job_satisfaction', 'environment_satisfaction', 'relationship_satisfaction',
            'work_life_balance', 'job_involvement', 'performance_rating',
        ]
        widgets = {
            'date_embauche': forms.DateInput(attrs={'type': 'date'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom complet'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@exemple.com'}),
            'poste': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Développeur'}),
        }

class CongeForm(forms.ModelForm):
    class Meta:
        model = CongeRequest
        fields = ['date_debut', 'date_fin', 'motif']  # 🔥 supprimer employee + status
        widgets = {
            'date_debut': forms.DateInput(attrs={'type': 'date'}),
            'date_fin': forms.DateInput(attrs={'type': 'date'}),
            'motif': forms.Textarea(attrs={'rows': 3}),
        }


class BulletinForm(forms.ModelForm):
    class Meta:
        model = BulletinPaie
        fields = ['employee', 'mois', 'annee', 'salaire_base', 'primes', 'deductions', 'net_a_payer']


class PredictionForm(forms.ModelForm):
    class Meta:
        model = Prediction
        fields = ['employee', 'score', 'resultat', 'status', 'date_prediction']
        widgets = {
            'date_prediction': forms.DateInput(attrs={'type': 'date'}),
        }


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['nom', 'type_doc', 'fichier']
        widgets = {'nom': forms.TextInput(attrs={'class': 'form-control'})}


class ModelePredictionForm(forms.ModelForm):
    class Meta:
        model = ModelePrediction
        fields = ['nom_modele', 'precision', 'date_entrainement', 'fichier_modele', 'description', 'actif']
        widgets = {'date_entrainement': forms.DateInput(attrs={'type': 'date'}),
                   'description': forms.Textarea(attrs={'rows': 3})}
