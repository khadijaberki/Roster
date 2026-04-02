
# IMPORTS

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import joblib
from xgboost import XGBClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE

#  création DOSSIERS RESULTATS

os.makedirs("figures", exist_ok=True)
os.makedirs("outputs", exist_ok=True)


#  CHARGER DATASET

df = pd.read_csv("dataset.csv", sep=',')

print("\nAperçu dataset :")
print(df.head())
# STATISTIQUES DESCRIPTIVES
print(df.shape)
print("\nStatistiques descriptives des variables numériques :")

stats = df.describe()

print(stats)

# sauvegarde dans un fichier pour le rapport
stats.to_csv("outputs/statistiques_descriptives.csv")

print("Fichier statistiques_descriptives.csv généré dans outputs/")
# VISUALISATION (EDA)

plt.figure(figsize=(6,4))
sns.countplot(x='Attrition', data=df)
plt.title("Nombre d'employés qui quittent l'entreprise")
plt.savefig("figures/01_attrition_global.png")
plt.close()

plt.figure(figsize=(6,4))
sns.countplot(x='OverTime', hue='Attrition', data=df)
plt.title("Impact des heures supplémentaires")
plt.savefig("figures/02_overtime_attrition.png")
plt.close()

plt.figure(figsize=(7,5))
sns.boxplot(x='Attrition', y='MonthlyIncome', data=df)
plt.title("Salaire mensuel vs départ")
plt.savefig("figures/03_salary_attrition.png")
plt.close()

plt.figure(figsize=(7,5))
sns.histplot(data=df, x="Age", hue="Attrition", kde=True)
plt.title("Distribution de l'age")
plt.savefig("figures/04_age_distribution.png")
plt.close()

# ANALYSE DE VARIANCE

print("\nAnalyse de variance des variables numériques :")
#selectionne les variables numeriques 
numeric_df = df.select_dtypes(include=['int64','float64'])
#calcule la variance de chaque variable 
variance = numeric_df.var().sort_values()

print(variance)

# graphique variance

plt.figure(figsize=(10,6))
variance.plot(kind='bar')
plt.title("Variance des variables numériques")
plt.ylabel("Variance")
#change legend horizontal 
plt.xticks(rotation=90)
# legend dans l'abscisse doit etre visible completement 
plt.tight_layout()
plt.savefig("figures/08_variance_variables.png")
plt.close()
# nettoyage
#supprimes les colonnes inutiles
#employeecount :valeur constante
#employeenumber:identifiant
#over18:
print(df.isnull().sum)
df = df.drop(['EmployeeCount','EmployeeNumber','Over18','StandardHours'], axis=1)

#transformes la variable cible en format numérique
df['Attrition'] = df['Attrition'].map({'Yes':1, 'No':0})
#transformes les variables catégorielles en variables numériques
df = pd.get_dummies(df, drop_first=True)
# MATRICE DE CORRELATION

plt.figure(figsize=(14,10))
corr = df.corr()

sns.heatmap(corr,
            #donner les couleurs à la valeur de correlation 
            cmap="coolwarm",
            #centre la valeur 
            center=0,
            #donner les relation sous forme des carrée
            square=True)

plt.title("Matrice de corrélation des variables")
plt.tight_layout()
plt.savefig("figures/09_correlation_matrix.png")
plt.close()

#  X et y
#Séparation X et y
# axis0: ligne
# AXIS1:colonne
#variable explicative
X = df.drop('Attrition', axis=1)
#cible
y = df['Attrition']

#Division Train / Test
#  SPLIT

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)


#  SMOTE pour équilibrage

sm = SMOTE(random_state=42)
X_train_resampled, y_train_resampled = sm.fit_resample(X_train, y_train)

print("\nAvant équilibrage :")
print(y_train.value_counts())
print("\nAprès équilibrage :")
print(y_train_resampled.value_counts())


#  NORMALISATION

scaler = StandardScaler()
#normaliser les donnees de l'entrainement 
X_train_scaled = scaler.fit_transform(X_train_resampled)
#applique la meme transformation aux donne de test
X_test_scaled = scaler.transform(X_test)


#  FONCTION EVALUATION

def evaluate_model(name, model, Xtr, Xte):
    model.fit(Xtr, y_train_resampled)
    pred = model.predict(Xte)
    print(f"\n--- {name} ---")
    print("Accuracy :", accuracy_score(y_test, pred))
    print(classification_report(y_test, pred))
    return model, pred


#  MODELES
#Modèle statistique linéaire
#Calcule une probabilité entre 0 et 1
lr, pred_lr = evaluate_model(
    "LOGISTIC REGRESSION",
    LogisticRegression(max_iter=8000, class_weight="balanced"),
    X_train_scaled, X_test_scaled
)
#Modèle basé sur des règles "SI… ALORS…
#
dt, pred_dt = evaluate_model(
    "DECISION TREE",
    DecisionTreeClassifier(max_depth=10, class_weight="balanced", random_state=42),
    X_train_resampled, X_test
)
#Ensemble de plusieurs arbres
rf, pred_rf = evaluate_model(
    "RANDOM FOREST",
    RandomForestClassifier(n_estimators=300, class_weight="balanced", random_state=42),
    X_train_resampled, X_test
)
#Cherche la meilleure frontière pour séparer les classes
svm, pred_svm = evaluate_model(
    "SVM",
    SVC(class_weight="balanced", probability=True),
    X_train_scaled, X_test_scaled
)

knn, pred_knn = evaluate_model(
    "KNN",
    KNeighborsClassifier(n_neighbors=7),
    X_train_scaled, X_test_scaled
)

xgb, pred_xgb = evaluate_model(
    "XGBOOST",
    XGBClassifier(n_estimators=400, learning_rate=0.05, max_depth=6, eval_metric='logloss'),
    X_train_resampled, X_test
)

mlp, pred_mlp = evaluate_model(
    "MLP NEURAL NETWORK",
    MLPClassifier(hidden_layer_sizes=(64,32), max_iter=500, random_state=42),
    X_train_scaled, X_test_scaled
)

#  MATRICE DE CONFUSION (Meilleur modèle : LOGISTIC REGRESSION)

best_model = lr
X_test_best = X_test_scaled  # pour les modèles normalisés
y_pred = best_model.predict(X_test_best)

cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(6,5))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
plt.xlabel("Prédit")
plt.ylabel("Réel")
plt.title("Matrice de Confusion (Logistic Regression)")
plt.savefig("figures/05_confusion_matrix.png")
plt.close()


# REEL VS PREDIT

results = pd.DataFrame({"Reel": y_test.values, "Predit": y_pred})
plt.figure(figsize=(7,5))
sns.countplot(x="Reel", hue="Predit", data=results)
plt.title("Comparaison Réel vs Prédit (Logistic Regression)")
plt.savefig("figures/06_real_vs_pred.png")
plt.close()

#  PROBABILITÉ DE DEPART
#fctquifaitelaprobabilitedeclasse0et1
proba = best_model.predict_proba(X_test_best)[:,1]

plt.figure(figsize=(7,5))
#20:barre
sns.histplot(proba, bins=20, kde=True)
plt.title("Probabilité de départ des employés (Logistic Regression)")
plt.xlabel("Risque de quitter l'entreprise")
plt.ylabel("Nombre d'employés")
plt.savefig("figures/07_risk_probability.png")
plt.close()


#  EMPLOYÉS À RISQUE

high_risk = pd.DataFrame(X_test.copy())
#creer  attribut probabilite depart 
high_risk["probabilite_depart"] = proba
high_risk = high_risk[high_risk["probabilite_depart"] > 0.7]

high_risk.to_csv("outputs/employes_risque_depart.csv", index=False)

#  SAUVEGARDE DU MODELE


joblib.dump(lr, "outputs/modele_logistic_regression.pkl")
joblib.dump(scaler, "outputs/scaler.pkl")

print(" Modèle Logistic Regression sauvegardé dans outputs/modele_logistic_regression.pkl")
print(" Scaler sauvegardé dans outputs/scaler.pkl")
print("\n Fichier généré : outputs/employes_risque_depart.csv")
print(" Graphiques générés dans dossier figures/")
