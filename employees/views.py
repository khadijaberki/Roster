import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Count
from django.http import JsonResponse
from .models import Employee, CongeRequest, BulletinPaie, Prediction, Department, Document, ModelePrediction, Notification
from .forms import EmployeeForm, CongeForm, BulletinForm, PredictionForm, DocumentForm, ModelePredictionForm
from .ml_forms import MLPredictionForm
from datetime import date
from django.contrib.auth import authenticate, login, logout


def is_admin(user):
    return user.is_superuser

def is_rh(user):
    return user.is_staff or user.is_superuser


# ══════════════════════════════════════════════════════════════
#  UTILITAIRE — Envoyer une notification
# ══════════════════════════════════════════════════════════════
def notifier_rh(message):
    """Envoie une notification à tous les utilisateurs RH (is_staff, non superuser)"""
    rh_users = User.objects.filter(is_staff=True, is_superuser=False)
    for rh in rh_users:
        Notification.objects.create(user=rh, message=message)


def notifier_user(user, message):
    """Envoie une notification à un utilisateur spécifique"""
    if user:
        Notification.objects.create(user=user, message=message)


# ══════════════════════════════════════════════════════════════
#  LOGIN / LOGOUT
# ══════════════════════════════════════════════════════════════
def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('dashboard')
        elif request.user.is_staff:
            return redirect('page_rh')
        else:
            return redirect('espace_employe')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role     = request.POST.get('role')

        if not role:
            messages.error(request, 'Veuillez sélectionner un rôle.')
            return render(request, 'registration/login.html')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if role == 'admin':
                if user.is_superuser:
                    login(request, user)
                    return redirect('dashboard')
                else:
                    messages.error(request, "Ce compte n'a pas les droits d'administrateur.")

            elif role == 'rh':
                if user.is_staff and not user.is_superuser:
                    login(request, user)
                    return redirect('page_rh')
                else:
                    messages.error(request, "Ce compte n'a pas les droits RH.")

            elif role == 'employe':
                try:
                    emp = user.employee  # lève RelatedObjectDoesNotExist si pas lié
                    if emp is not None:
                        login(request, user)
                        return redirect('espace_employe')
                    else:
                        messages.error(request, "Ce compte n'est pas lié à un employé.")
                except Exception:
                    messages.error(request, "Ce compte n'est pas lié à un employé.")

            else:
                messages.error(request, "Rôle invalide.")
        else:
            messages.error(request, 'Identifiant ou mot de passe incorrect.')

    return render(request, 'registration/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


# ══════════════════════════════════════════════════════════════
#  DASHBOARD ADMIN
# ══════════════════════════════════════════════════════════════
@login_required
def dashboard(request):
    employees   = Employee.objects.all()
    conges      = CongeRequest.objects.all()
    bulletins   = BulletinPaie.objects.all()
    predictions = Prediction.objects.all()
    dept_stats  = Department.objects.annotate(emp_count=Count('employee'))

    total_rh  = User.objects.filter(employee__isnull=True, is_superuser=False).count()
    total_emp = employees.count() or 1
    dept_data = [
        {'name': d.name, 'count': d.emp_count, 'pct': round(d.emp_count / total_emp * 100)}
        for d in dept_stats if d.emp_count > 0
    ]

    context = {
        'total_employees':    employees.count(),
        'total_rh':           total_rh,
        'total_conges':       conges.filter(status='En attente').count(),
        'total_bulletins':    bulletins.count(),
        'total_predictions':  predictions.count(),
        'recent_conges':      conges.order_by('-created_at')[:3],
        'recent_predictions': predictions.order_by('-created_at')[:3],
        'dept_data':          dept_data,
    }
    return render(request, 'employees/dashboard.html', context)


# ══════════════════════════════════════════════════════════════
#  PAGE RH  ← recent_employees ajouté ici
# ══════════════════════════════════════════════════════════════
@login_required
def page_rh(request):
    """Tableau de bord pour le RH."""
    if not request.user.is_staff:
        return redirect('login')

    employees   = Employee.objects.all()
    conges      = CongeRequest.objects.all()
    bulletins   = BulletinPaie.objects.all()
    predictions = Prediction.objects.all()
    dept_stats  = Department.objects.annotate(emp_count=Count('employee'))
    total_emp   = employees.count() or 1
    dept_data   = [
        {'name': d.name, 'count': d.emp_count, 'pct': round(d.emp_count / total_emp * 100)}
        for d in dept_stats if d.emp_count > 0
    ]

    context = {
        'total_employees':    employees.count(),
        'total_conges':       conges.filter(status='En attente').count(),
        'total_bulletins':    bulletins.count(),
        'total_predictions':  predictions.count(),
        'recent_conges':      conges.order_by('-created_at')[:3],
        'recent_bulletins':   bulletins.order_by('-annee', '-mois')[:3],
        'recent_predictions': predictions.order_by('-created_at')[:3],
        'recent_employees':   employees.select_related('department').order_by('-date_embauche')[:5],  # ← AJOUTÉ
        'dept_data':          dept_data,
    }
    return render(request, 'employees/page_rh.html', context)


# ══════════════════════════════════════════════════════════════
#  EMPLOYÉS
# ══════════════════════════════════════════════════════════════
@login_required
def employee_list(request):
    q = request.GET.get('q', '')
    employees = Employee.objects.select_related('department').all()
    if q:
        employees = employees.filter(name__icontains=q)
    return render(request, 'employees/employee_list.html', {'employees': employees, 'q': q})


@login_required
def employee_add(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            emp      = form.save(commit=False)
            username = request.POST.get('username')
            password = request.POST.get('password')
            if username and password:
                if User.objects.filter(username=username).exists():
                    messages.error(request, f"L'identifiant '{username}' existe déjà.")
                    return render(request, 'employees/employee_form.html', {'form': form, 'title': 'Ajouter un Employé'})
                user     = User.objects.create_user(username=username, password=password)
                emp.user = user
            emp.save()
            notifier_rh(f"➕ Nouvel employé ajouté : {emp.name} — poste : {emp.poste}")
            messages.success(request, f'Employé ajouté. Identifiant: {username} | Mot de passe: {password}')
            return redirect('employee_list')
    else:
        form = EmployeeForm()
    return render(request, 'employees/employee_form.html', {'form': form, 'title': 'Ajouter un Employé'})


@login_required
def employee_edit(request, pk):
    emp = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES, instance=emp)
        if form.is_valid():
            form.save()
            notifier_rh(f"✏️ Fiche de l'employé modifiée : {emp.name}")
            if emp.user:
                notifier_user(emp.user, "✏️ Votre profil a été mis à jour par les RH.")
            messages.success(request, 'Employé mis à jour.')
            return redirect('employee_list')
    else:
        form = EmployeeForm(instance=emp)
    return render(request, 'employees/employee_form.html', {'form': form, 'title': 'Modifier Employé'})


@login_required
def employee_delete(request, pk):
    emp = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        emp.delete()
        messages.success(request, 'Employé supprimé.')
        return redirect('employee_list')
    return render(request, 'employees/confirm_delete.html', {'obj': emp, 'type': 'employé'})


@login_required
def employee_detail(request, pk):
    emp         = get_object_or_404(Employee, pk=pk)
    docs        = emp.documents.all()
    conges      = CongeRequest.objects.filter(employee=emp).order_by('-created_at')
    bulletins   = BulletinPaie.objects.filter(employee=emp).order_by('-annee', '-mois')
    predictions = Prediction.objects.filter(employee=emp).order_by('-created_at')
    return render(request, 'employees/employee_detail.html', {
        'emp': emp, 'docs': docs, 'conges': conges,
        'bulletins': bulletins, 'predictions': predictions,
    })


@login_required
def employee_data_api(request, pk):
    emp  = get_object_or_404(Employee, pk=pk)
    data = emp.to_ml_dict()
    data['name'] = emp.name
    return JsonResponse(data)


# ══════════════════════════════════════════════════════════════
#  DOCUMENTS
# ══════════════════════════════════════════════════════════════
@login_required
def document_add(request, emp_pk):
    emp = get_object_or_404(Employee, pk=emp_pk)
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc          = form.save(commit=False)
            doc.employee = emp
            doc.save()
            notifier_rh(f"📄 Nouveau document ajouté pour {emp.name} : {doc.nom}")
            messages.success(request, 'Document ajouté.')
            return redirect('employee_detail', pk=emp_pk)
    else:
        form = DocumentForm()
    return render(request, 'employees/document_form.html', {'form': form, 'emp': emp})


@login_required
def document_delete(request, pk):
    doc    = get_object_or_404(Document, pk=pk)
    emp_pk = doc.employee.pk
    if request.method == 'POST':
        doc.fichier.delete(save=False)
        doc.delete()
        messages.success(request, 'Document supprimé.')
    return redirect('employee_detail', pk=emp_pk)


# ══════════════════════════════════════════════════════════════
#  CONGÉS
# ══════════════════════════════════════════════════════════════
@login_required
def conge_list(request):
    conges = CongeRequest.objects.select_related('employee').order_by('-created_at')
    return render(request, 'employees/conge_list.html', {'conges': conges})


@login_required
def conge_add(request):
    if request.method == 'POST':
        form = CongeForm(request.POST)
        if form.is_valid():
            conge = form.save(commit=False)

            # 🔥 lier automatiquement l'utilisateur
            conge.employee = request.user.employee

            # 🔥 statut automatique
            conge.status = "En attente"

            conge.save()

            notifier_rh(
                f"Nouvelle demande de congé : {conge.employee.name} du {conge.date_debut} au {conge.date_fin}"
            )

            messages.success(request, 'Demande de congé envoyée avec succès.')
            return redirect('conge_list')
    else:
        form = CongeForm()

    return render(request, 'employees/conge_form.html', {
        'form': form,
        'title': 'Nouvelle Demande de Congé'
    })
@login_required
def conge_update_status(request, pk, status):
    conge        = get_object_or_404(CongeRequest, pk=pk)
    conge.status = status
    conge.save()
    if conge.employee.user:
        emoji = "✅" if status == "Approuvé" else "❌"
        notifier_user(
            conge.employee.user,
            f"{emoji} Votre demande de congé du {conge.date_debut} au {conge.date_fin} a été {status}."
        )
    messages.success(request, f'Statut: {status}')
    return redirect('conge_list')


# ══════════════════════════════════════════════════════════════
#  PAIE
# ══════════════════════════════════════════════════════════════
@login_required
def paie_list(request):
    bulletins = BulletinPaie.objects.select_related('employee').order_by('-annee', '-mois')
    return render(request, 'employees/paie_list.html', {'bulletins': bulletins})


@login_required
def paie_add(request):
    if request.method == 'POST':
        form = BulletinForm(request.POST)
        if form.is_valid():
            bulletin = form.save()
            if bulletin.employee.user:
                notifier_user(
                    bulletin.employee.user,
                    f"💰 Votre bulletin de paie de {bulletin.mois}/{bulletin.annee} est disponible."
                )
            messages.success(request, 'Bulletin créé.')
            return redirect('paie_list')
    else:
        form = BulletinForm()
    return render(request, 'employees/paie_form.html', {'form': form, 'title': 'Nouveau Bulletin'})


@login_required
def paie_delete(request, pk):
    bulletin = get_object_or_404(BulletinPaie, pk=pk)
    if request.method == 'POST':
        bulletin.delete()
        messages.success(request, 'Bulletin supprimé.')
    return redirect('paie_list')


# ══════════════════════════════════════════════════════════════
#  PRÉDICTIONS
# ══════════════════════════════════════════════════════════════
@login_required
def prediction_list(request):
    predictions = Prediction.objects.select_related('employee').order_by('-created_at')
    return render(request, 'employees/prediction_list.html', {'predictions': predictions})


@login_required
def prediction_delete(request, pk):
    prediction = get_object_or_404(Prediction, pk=pk)
    if request.method == 'POST':
        prediction.delete()
        messages.success(request, 'Prédiction supprimée.')
    return redirect('prediction_list')


@login_required
def prediction_add(request):
    form   = MLPredictionForm(request.POST or None)
    result = None
    if request.method == 'POST' and form.is_valid():
        try:
            from .ml_predictor import predict_attrition
            data              = form.cleaned_data
            resultat, score, status = predict_attrition(data)
            modele            = ModelePrediction.objects.filter(actif=True).first()
            Prediction.objects.create(
                employee=data['employee'], score=score,
                resultat=resultat, status=status,
                date_prediction=date.today(), modele=modele,
            )
            result = {'employee': data['employee'], 'resultat': resultat, 'score': score, 'status': status}
            if data['employee'].user:
                notifier_user(
                    data['employee'].user,
                    f"🔮 Une prédiction a été effectuée sur votre profil : {resultat} ({score}%)"
                )
            messages.success(request, f"Prédiction: {resultat} ({score}%)")
        except FileNotFoundError:
            messages.error(request, "Modèle ML introuvable.")
        except Exception as e:
            messages.error(request, f"Erreur: {str(e)}")
    return render(request, 'employees/prediction_add.html', {'form': form, 'result': result})


# ══════════════════════════════════════════════════════════════
#  MODÈLE PRÉDICTION
# ══════════════════════════════════════════════════════════════
@login_required
def modele_list(request):
    modeles = ModelePrediction.objects.all().order_by('-date_entrainement')
    return render(request, 'employees/modele_list.html', {'modeles': modeles})


@login_required
def modele_add(request):
    if request.method == 'POST':
        form = ModelePredictionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Modèle enregistré.')
            return redirect('modele_list')
    else:
        form = ModelePredictionForm()
    return render(request, 'employees/modele_form.html', {'form': form, 'title': 'Nouveau Modèle'})


@login_required
def modele_delete(request, pk):
    modele = get_object_or_404(ModelePrediction, pk=pk)
    if request.method == 'POST':
        modele.delete()
        messages.success(request, 'Modèle supprimé.')
    return redirect('modele_list')


# ══════════════════════════════════════════════════════════════
#  ADMIN — Gestion des comptes RH
# ══════════════════════════════════════════════════════════════
@login_required
@user_passes_test(is_admin)
def admin_rh_list(request):
    rh_users = User.objects.filter(is_staff=True, is_superuser=False)
    return render(request, 'employees/admin_rh_list.html', {'rh_users': rh_users})


@login_required
@user_passes_test(is_admin)
def admin_rh_add(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email    = request.POST.get('email')
        password = request.POST.get('password')
        if User.objects.filter(username=username).exists():
            messages.error(request, "Ce nom d'utilisateur existe déjà.")
        else:
            user          = User.objects.create_user(username=username, email=email, password=password)
            user.is_staff = True
            user.save()
            messages.success(request, f'Compte RH "{username}" créé.')
        return redirect('admin_rh_list')
    return render(request, 'employees/admin_rh_add.html')


@login_required
@user_passes_test(is_admin)
def admin_rh_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'Compte RH supprimé.')
    return redirect('admin_rh_list')


# ══════════════════════════════════════════════════════════════
#  ESPACE EMPLOYÉ
# ══════════════════════════════════════════════════════════════
@login_required
def espace_employe(request):
    try:
        employee = request.user.employee
    except:
        messages.error(request, "Aucun profil employé associé à ce compte.")
        return redirect('dashboard')

    conges        = CongeRequest.objects.filter(employee=employee).order_by('-created_at')
    documents     = Document.objects.filter(employee=employee)
    bulletins     = BulletinPaie.objects.filter(employee=employee).order_by('-annee', '-mois')
    departments   = Department.objects.all()
    conge_form    = CongeForm()
    document_form = DocumentForm()
    employee_form = EmployeeForm(instance=employee)

    if request.method == 'POST':

        if 'demande_conge' in request.POST:
            conge_form = CongeForm(request.POST)
            if conge_form.is_valid():
                conge          = conge_form.save(commit=False)
                conge.employee = employee
                conge.status   = 'En attente'
                conge.save()
                notifier_rh(f"🏖️ {employee.name} a soumis une demande de congé du {conge.date_debut} au {conge.date_fin}.")
                messages.success(request, 'Demande envoyée ✅')
                return redirect('/mon-espace/?tab=conge')

        elif 'add_document' in request.POST:
            nom      = request.POST.get('nom', '').strip()
            type_doc = request.POST.get('type_document', '')
            fichier  = request.FILES.get('fichier')
            if nom and type_doc and fichier:
                Document(employee=employee, nom=nom, type_doc=type_doc, fichier=fichier).save()
                notifier_rh(f"📄 {employee.name} a ajouté un document : {nom}")
                messages.success(request, 'Document ajouté ✅')
            else:
                messages.error(request, 'Veuillez remplir tous les champs du document.')
            return redirect('/mon-espace/?tab=document')

        elif 'update_nom' in request.POST:
            employee.name = request.POST.get('name')
            if request.FILES.get('photo'):
                employee.photo = request.FILES['photo']
            employee.save()
            notifier_rh(f"✏️ {employee.name} a modifié son profil.")
            messages.success(request, 'Profil modifié ✅')
            return redirect('espace_employe')

        elif 'update_info' in request.POST:
            employee_form = EmployeeForm(request.POST, request.FILES, instance=employee)
            if employee_form.is_valid():
                employee_form.save()
                notifier_rh(f"✏️ {employee.name} a mis à jour ses informations personnelles.")
                messages.success(request, 'Informations mises à jour ✅')
                return redirect('espace_employe')

    return render(request, 'employees/espace_employe.html', {
        'employee':      employee,
        'conges':        conges,
        'documents':     documents,
        'bulletins':     bulletins,
        'conge_form':    conge_form,
        'document_form': document_form,
        'employee_form': employee_form,
        'departments':   departments,
    })


# ══════════════════════════════════════════════════════════════
#  SUPPRESSION DOCUMENT (espace employé)
# ══════════════════════════════════════════════════════════════
def delete_document(request, doc_id):
    doc = get_object_or_404(Document, id=doc_id)
    doc.delete()
    return redirect('/mon-espace/?tab=document')


# ══════════════════════════════════════════════════════════════
#  NOTIFICATIONS API
# ══════════════════════════════════════════════════════════════
@login_required
def notifications_api(request):
    """Retourne les notifications non lues de l'utilisateur connecté"""
    notifs = Notification.objects.filter(
        user=request.user, is_read=False
    ).order_by('-created_at')[:20]

    data = [{
        'id':         n.id,
        'message':    n.message,
        'created_at': n.created_at.strftime('%d/%m/%Y %H:%M'),
    } for n in notifs]

    return JsonResponse({'notifications': data, 'count': len(data)})


@login_required
def notifications_mark_read(request):
    """Marque toutes les notifications comme lues"""
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    return JsonResponse({'status': 'ok'})