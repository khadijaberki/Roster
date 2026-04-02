from django.db import models
from django.contrib.auth.models import User
from datetime import date


class Department(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name


class Employee(models.Model):
    STATUS_CHOICES   = [('actif', 'Actif'), ('inactif', 'Inactif')]
    GENDER_CHOICES   = [('Male', 'Homme'), ('Female', 'Femme')]
    MARITAL_CHOICES  = [('Single', 'Célibataire'), ('Married', 'Marié(e)'), ('Divorced', 'Divorcé(e)')]
    TRAVEL_CHOICES   = [('Non-Travel', 'Jamais'), ('Travel_Rarely', 'Rarement'), ('Travel_Frequently', 'Fréquemment')]
    OVERTIME_CHOICES = [('No', 'Non'), ('Yes', 'Oui')]
    EDU_FIELD_CHOICES = [
        ('Life Sciences','Life Sciences'),('Medical','Medical'),('Marketing','Marketing'),
        ('Technical Degree','Technical Degree'),('Human Resources','Human Resources'),('Other','Other'),
    ]
    JOBROLE_CHOICES = [
        ('Sales Executive','Sales Executive'),('Research Scientist','Research Scientist'),
        ('Laboratory Technician','Laboratory Technician'),('Manufacturing Director','Manufacturing Director'),
        ('Healthcare Representative','Healthcare Representative'),('Manager','Manager'),
        ('Sales Representative','Sales Representative'),('Research Director','Research Director'),
        ('Human Resources','Human Resources'),
    ]

    user             = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    name             = models.CharField(max_length=200)
    email            = models.EmailField(unique=True)
    department       = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    poste            = models.CharField(max_length=200)
    date_embauche    = models.DateField()
    salaire          = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status           = models.CharField(max_length=10, choices=STATUS_CHOICES, default='actif')
    photo            = models.ImageField(upload_to='employees/', blank=True, null=True)
    # ML fields
    age                        = models.IntegerField(default=30)
    gender                     = models.CharField(max_length=10, choices=GENDER_CHOICES, default='Male')
    marital_status             = models.CharField(max_length=10, choices=MARITAL_CHOICES, default='Single')
    distance_from_home         = models.IntegerField(default=5)
    education                  = models.IntegerField(default=3)
    education_field            = models.CharField(max_length=50, choices=EDU_FIELD_CHOICES, default='Life Sciences')
    job_role                   = models.CharField(max_length=50, choices=JOBROLE_CHOICES, default='Research Scientist')
    job_level                  = models.IntegerField(default=2)
    business_travel            = models.CharField(max_length=20, choices=TRAVEL_CHOICES, default='Travel_Rarely')
    overtime                   = models.CharField(max_length=3, choices=OVERTIME_CHOICES, default='No')
    daily_rate                 = models.IntegerField(default=800)
    hourly_rate                = models.IntegerField(default=66)
    monthly_income             = models.IntegerField(default=6500)
    monthly_rate               = models.IntegerField(default=14000)
    percent_salary_hike        = models.IntegerField(default=15)
    stock_option_level         = models.IntegerField(default=1)
    total_working_years        = models.IntegerField(default=8)
    num_companies_worked       = models.IntegerField(default=2)
    years_at_company           = models.IntegerField(default=5)
    years_in_current_role      = models.IntegerField(default=3)
    years_since_last_promotion = models.IntegerField(default=1)
    years_with_curr_manager    = models.IntegerField(default=3)
    training_times_last_year   = models.IntegerField(default=3)
    job_satisfaction           = models.IntegerField(default=3)
    environment_satisfaction   = models.IntegerField(default=3)
    relationship_satisfaction  = models.IntegerField(default=3)
    work_life_balance          = models.IntegerField(default=3)
    job_involvement            = models.IntegerField(default=3)
    performance_rating         = models.IntegerField(default=3)

    def __str__(self):
        return self.name

    def to_ml_dict(self):
        dept_map = {
            'Informatique':'Research & Development','Marketing':'Sales',
            'Administratif':'Human Resources','Commercial':'Sales',
            'Research & Development':'Research & Development',
            'Sales':'Sales','Human Resources':'Human Resources',
        }
        dept_name = self.department.name if self.department else 'Research & Development'
        return {
            'Age': self.age, 'DailyRate': self.daily_rate,
            'DistanceFromHome': self.distance_from_home, 'Education': self.education,
            'EnvironmentSatisfaction': self.environment_satisfaction, 'HourlyRate': self.hourly_rate,
            'JobInvolvement': self.job_involvement, 'JobLevel': self.job_level,
            'JobSatisfaction': self.job_satisfaction, 'MonthlyIncome': self.monthly_income,
            'MonthlyRate': self.monthly_rate, 'NumCompaniesWorked': self.num_companies_worked,
            'PercentSalaryHike': self.percent_salary_hike, 'PerformanceRating': self.performance_rating,
            'RelationshipSatisfaction': self.relationship_satisfaction, 'StockOptionLevel': self.stock_option_level,
            'TotalWorkingYears': self.total_working_years, 'TrainingTimesLastYear': self.training_times_last_year,
            'WorkLifeBalance': self.work_life_balance, 'YearsAtCompany': self.years_at_company,
            'YearsInCurrentRole': self.years_in_current_role,
            'YearsSinceLastPromotion': self.years_since_last_promotion,
            'YearsWithCurrManager': self.years_with_curr_manager,
            'BusinessTravel': self.business_travel,
            'Department': dept_map.get(dept_name, 'Research & Development'),
            'EducationField': self.education_field, 'Gender': self.gender,
            'JobRole': self.job_role, 'MaritalStatus': self.marital_status, 'OverTime': self.overtime,
        }


# ── Nouveau: Document ──────────────────────────────────────────────────────────
class Document(models.Model):
    TYPE_CHOICES = [
        ('contrat', 'Contrat'), ('cv', 'CV'), ('diplome', 'Diplôme'),
        ('autre', 'Autre'),
    ]
    employee   = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='documents')
    nom        = models.CharField(max_length=200)
    type_doc   = models.CharField(max_length=20, choices=TYPE_CHOICES, default='autre')
    fichier    = models.FileField(upload_to='documents/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee.name} – {self.nom}"


# ── Nouveau: ModelePrediction ──────────────────────────────────────────────────
class ModelePrediction(models.Model):
    nom_modele       = models.CharField(max_length=100, default='Logistic Regression')
    precision        = models.FloatField(default=0.0)
    date_entrainement = models.DateField()
    fichier_modele   = models.CharField(max_length=200, default='modele_logistic_regression.pkl')
    description      = models.TextField(blank=True)
    actif            = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nom_modele} ({self.precision*100:.1f}%)"

    class Meta:
        verbose_name = "Modèle de Prédiction"


# ── Congé ──────────────────────────────────────────────────────────────────────
class CongeRequest(models.Model):
    STATUS_CHOICES = [('En attente','En attente'),('Approuvé','Approuvé'),('Refusé','Refusé')]
    employee   = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date_debut = models.DateField()
    date_fin   = models.DateField()
    motif      = models.TextField(blank=True)
    status     = models.CharField(max_length=20, choices=STATUS_CHOICES, default='En attente')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee.name} - {self.date_debut}"

    @property
    def nb_jours(self):
        return (self.date_fin - self.date_debut).days + 1


# ── Paie ───────────────────────────────────────────────────────────────────────
class BulletinPaie(models.Model):
    employee     = models.ForeignKey(Employee, on_delete=models.CASCADE)
    mois         = models.CharField(max_length=20)
    annee        = models.IntegerField()
    salaire_base = models.DecimalField(max_digits=10, decimal_places=2)
    primes       = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deductions   = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    net_a_payer  = models.DecimalField(max_digits=10, decimal_places=2)
    created_at   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee.name} - {self.mois}/{self.annee}"


# ── Prédiction ─────────────────────────────────────────────────────────────────
class Prediction(models.Model):
    STATUS_CHOICES = [('Satisfaisant','Satisfaisant'),('À surveiller','À surveiller'),('En attente','En attente')]
    employee   = models.ForeignKey(Employee, on_delete=models.CASCADE)
    modele     = models.ForeignKey(ModelePrediction, on_delete=models.SET_NULL, null=True, blank=True)
    score      = models.IntegerField()
    resultat   = models.CharField(max_length=60)
    status     = models.CharField(max_length=20, choices=STATUS_CHOICES, default='En attente')
    date_prediction = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee.name} - {self.score}%"
from django.db import models
from django.contrib.auth.models import User

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification pour {self.user.username}"