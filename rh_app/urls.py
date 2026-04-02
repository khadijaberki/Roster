from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from employees import views as employees_views  # ✅ import de la vue custom


def smart_redirect(request):
    """Redirige selon le rôle de l'utilisateur."""
    if not request.user.is_authenticated:
        return redirect('login')
    if request.user.is_superuser:
        return redirect('dashboard')
    if request.user.is_staff and not request.user.is_superuser:  # ✅ RH → page_rh
        return redirect('page_rh')
    # Employé normal
    return redirect('espace_employe')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', smart_redirect),
    path('', include('employees.urls')),
    # ✅ login pointe vers la vue custom (avec sélection de rôle)
    path('login/', employees_views.login_view, name='login'),
    path('logout/', employees_views.logout_view, name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
