from django.shortcuts import render, get_object_or_404, redirect
from .models import StudyMaterial, User, Comment, Rating, Category
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Avg
from django.core.paginator import Paginator
from .forms import RatingForm, CommentForm, MaterialForm
from django.core.cache import cache
from django.contrib.auth.views import LogoutView

def material_list(request):
    cache_key = f'materials_list_{request.GET.urlencode()}'
    if cached := cache.get(cache_key):
        return cached

    query = request.GET.get('q')
    materials = StudyMaterial.objects.filter(approved=True)

    # Search filter
    if query:
        materials = materials.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )
    
    # Category filter
    category_id = request.GET.get('category')
    if category_id:
        materials = materials.filter(category__id=category_id)
    
    # Rating filter
    min_rating = request.GET.get('min_rating')
    if min_rating:
        materials = materials.annotate(
            avg_rating=Avg('ratings__rating')
        ).filter(avg_rating__gte=min_rating)
    
    # Ordering
    order = request.GET.get('order', '-upload_date')
    materials = materials.order_by(order)

    # Pagination
    paginator = Paginator(materials, 10)  # 10 per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()

    context = {
        'page_obj': page_obj,
        'query': query or '',
        'categories': categories,
        'order': order,
        'selected_category': category_id or '',
        'min_rating': min_rating or '',
    }

    response = render(request, 'materials/list.html', context)
    cache.set(cache_key, response, timeout=60*15)  # 15 minutes
    return response


def material_detail(request, pk):
    material = get_object_or_404(StudyMaterial, pk=pk)
    comments = material.comments.filter(approved=True)

    user_rating = None
    if request.user.is_authenticated:
        try:
            user_rating = Rating.objects.get(material=material, user=request.user)
        except Rating.DoesNotExist:
            pass

    comment_form = CommentForm()
    rating_form = RatingForm(instance=user_rating)

    if request.method == 'POST':
        if 'comment_submit' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid() and request.user.is_authenticated:
                comment = comment_form.save(commit=False)
                comment.material = material
                comment.author = request.user
                comment.save()
                return redirect('material-detail', pk=material.pk)

        elif 'rating_submit' in request.POST and request.user.is_authenticated:
            rating_form = RatingForm(request.POST, instance=user_rating)
            if rating_form.is_valid():
                rating = rating_form.save(commit=False)
                rating.material = material
                rating.user = request.user
                rating.save()
                return redirect('material-detail', pk=material.pk)

    agg = material.ratings.aggregate(avg_rating=Avg('rating'))
    average_rating = agg['avg_rating']
    total_ratings = material.ratings.count()

    return render(request, 'materials/detail.html', {
        'material': material,
        'comments': comments,
        'comment_form': comment_form,
        'rating_form': rating_form,
        'average_rating': round(average_rating, 1) if average_rating else None,
        'total_ratings': total_ratings,
        'user_rating': user_rating,
    })


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('material-list')
    else:
        form = UserCreationForm()
    return render(request, 'auth/signup.html', {'form': form})


@login_required
def upload_material(request):
    if request.method == 'POST':
        form = MaterialForm(request.POST, request.FILES)
        if form.is_valid():
            material = form.save(commit=False)
            material.uploaded_by = request.user
            material.approved = False  # New uploads require approval
            material.save()
            return redirect('material-list')
    else:
        form = MaterialForm()  # empty form on GET

    # Always return a response
    return render(request, 'materials/upload.html', {'form': form})

@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    user_materials = StudyMaterial.objects.filter(uploaded_by=user, approved=True)
    return render(request, 'materials/profile.html', {
        'profile_user': user,
        'materials': user_materials
    })

class CustomLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)