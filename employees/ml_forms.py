from django import forms
from .models import Employee

BUSINESS_TRAVEL_CHOICES = [
    ('Travel_Rarely', 'Rarement'),
    ('Travel_Frequently', 'Fréquemment'),
    ('Non-Travel', 'Jamais'),
]

DEPARTMENT_CHOICES = [
    ('Sales', 'Sales'),
    ('Research & Development', 'Research & Development'),
    ('Human Resources', 'Human Resources'),
]

EDUCATION_FIELD_CHOICES = [
    ('Life Sciences', 'Life Sciences'),
    ('Medical', 'Medical'),
    ('Marketing', 'Marketing'),
    ('Technical Degree', 'Technical Degree'),
    ('Human Resources', 'Human Resources'),
    ('Other', 'Other'),
]

GENDER_CHOICES = [
    ('Male', 'Homme'),
    ('Female', 'Femme'),
]

JOB_ROLE_CHOICES = [
    ('Sales Executive', 'Sales Executive'),
    ('Research Scientist', 'Research Scientist'),
    ('Laboratory Technician', 'Laboratory Technician'),
    ('Manufacturing Director', 'Manufacturing Director'),
    ('Healthcare Representative', 'Healthcare Representative'),
    ('Manager', 'Manager'),
    ('Sales Representative', 'Sales Representative'),
    ('Research Director', 'Research Director'),
    ('Human Resources', 'Human Resources'),
]

MARITAL_STATUS_CHOICES = [
    ('Single', 'Célibataire'),
    ('Married', 'Marié(e)'),
    ('Divorced', 'Divorcé(e)'),
]

OVERTIME_CHOICES = [
    ('No', 'Non'),
    ('Yes', 'Oui'),
]

SCALE_1_4 = [(str(i), str(i)) for i in range(1, 5)]
SCALE_1_5 = [(str(i), str(i)) for i in range(1, 6)]
SCALE_0_3 = [(str(i), str(i)) for i in range(0, 4)]


class MLPredictionForm(forms.Form):
    employee = forms.ModelChoiceField(
        queryset=Employee.objects.all(),
        label="Employé",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    # Infos personnelles
    Age = forms.IntegerField(label="Âge", min_value=18, max_value=65,
                             widget=forms.NumberInput(attrs={'class': 'form-control'}))
    Gender = forms.ChoiceField(label="Genre", choices=GENDER_CHOICES,
                               widget=forms.Select(attrs={'class': 'form-control'}))
    MaritalStatus = forms.ChoiceField(label="Statut Marital", choices=MARITAL_STATUS_CHOICES,
                                      widget=forms.Select(attrs={'class': 'form-control'}))
    DistanceFromHome = forms.IntegerField(label="Distance domicile-travail (km)", min_value=1, max_value=100,
                                          widget=forms.NumberInput(attrs={'class': 'form-control'}))

    # Éducation
    Education = forms.ChoiceField(label="Niveau d'éducation (1=Lycée → 5=Doctorat)",
                                  choices=SCALE_1_5,
                                  widget=forms.Select(attrs={'class': 'form-control'}))
    EducationField = forms.ChoiceField(label="Domaine d'éducation", choices=EDUCATION_FIELD_CHOICES,
                                       widget=forms.Select(attrs={'class': 'form-control'}))

    # Poste
    Department = forms.ChoiceField(label="Département", choices=DEPARTMENT_CHOICES,
                                   widget=forms.Select(attrs={'class': 'form-control'}))
    JobRole = forms.ChoiceField(label="Rôle", choices=JOB_ROLE_CHOICES,
                                widget=forms.Select(attrs={'class': 'form-control'}))
    JobLevel = forms.ChoiceField(label="Niveau de poste (1-5)", choices=SCALE_1_5,
                                 widget=forms.Select(attrs={'class': 'form-control'}))
    BusinessTravel = forms.ChoiceField(label="Déplacements professionnels",
                                       choices=BUSINESS_TRAVEL_CHOICES,
                                       widget=forms.Select(attrs={'class': 'form-control'}))
    OverTime = forms.ChoiceField(label="Heures supplémentaires", choices=OVERTIME_CHOICES,
                                 widget=forms.Select(attrs={'class': 'form-control'}))

    # Rémunération
    MonthlyIncome = forms.IntegerField(label="Revenu Mensuel ($)", min_value=1000,
                                       widget=forms.NumberInput(attrs={'class': 'form-control'}))
    DailyRate = forms.IntegerField(label="Taux Journalier ($)", min_value=100,
                                   widget=forms.NumberInput(attrs={'class': 'form-control'}))
    HourlyRate = forms.IntegerField(label="Taux Horaire ($)", min_value=10,
                                    widget=forms.NumberInput(attrs={'class': 'form-control'}))
    MonthlyRate = forms.IntegerField(label="Taux Mensuel ($)", min_value=1000,
                                     widget=forms.NumberInput(attrs={'class': 'form-control'}))
    PercentSalaryHike = forms.IntegerField(label="Augmentation Salaire (%)", min_value=0, max_value=100,
                                           widget=forms.NumberInput(attrs={'class': 'form-control'}))
    StockOptionLevel = forms.ChoiceField(label="Options d'actions (0-3)", choices=SCALE_0_3,
                                         widget=forms.Select(attrs={'class': 'form-control'}))

    # Expérience
    TotalWorkingYears = forms.IntegerField(label="Années d'expérience totale", min_value=0,
                                           widget=forms.NumberInput(attrs={'class': 'form-control'}))
    NumCompaniesWorked = forms.IntegerField(label="Nombre d'entreprises précédentes", min_value=0,
                                            widget=forms.NumberInput(attrs={'class': 'form-control'}))
    YearsAtCompany = forms.IntegerField(label="Années dans l'entreprise", min_value=0,
                                        widget=forms.NumberInput(attrs={'class': 'form-control'}))
    YearsInCurrentRole = forms.IntegerField(label="Années dans le rôle actuel", min_value=0,
                                            widget=forms.NumberInput(attrs={'class': 'form-control'}))
    YearsSinceLastPromotion = forms.IntegerField(label="Années depuis dernière promotion", min_value=0,
                                                 widget=forms.NumberInput(attrs={'class': 'form-control'}))
    YearsWithCurrManager = forms.IntegerField(label="Années avec manager actuel", min_value=0,
                                              widget=forms.NumberInput(attrs={'class': 'form-control'}))
    TrainingTimesLastYear = forms.IntegerField(label="Formations cette année", min_value=0, max_value=10,
                                               widget=forms.NumberInput(attrs={'class': 'form-control'}))

    # Satisfaction
    JobSatisfaction = forms.ChoiceField(label="Satisfaction au travail (1-4)", choices=SCALE_1_4,
                                        widget=forms.Select(attrs={'class': 'form-control'}))
    EnvironmentSatisfaction = forms.ChoiceField(label="Satisfaction environnement (1-4)", choices=SCALE_1_4,
                                                widget=forms.Select(attrs={'class': 'form-control'}))
    RelationshipSatisfaction = forms.ChoiceField(label="Satisfaction relations (1-4)", choices=SCALE_1_4,
                                                 widget=forms.Select(attrs={'class': 'form-control'}))
    WorkLifeBalance = forms.ChoiceField(label="Équilibre vie pro/perso (1-4)", choices=SCALE_1_4,
                                        widget=forms.Select(attrs={'class': 'form-control'}))
    JobInvolvement = forms.ChoiceField(label="Implication au travail (1-4)", choices=SCALE_1_4,
                                       widget=forms.Select(attrs={'class': 'form-control'}))
    PerformanceRating = forms.ChoiceField(label="Évaluation performance (1-4)", choices=SCALE_1_4,
                                          widget=forms.Select(attrs={'class': 'form-control'}))
