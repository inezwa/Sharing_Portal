from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q, Avg
from .models import StudyMaterial, Category
from .serializers import MaterialSerializer

@api_view(['GET'])
def material_search_api(request):
    # Start with approved materials and annotate avg_rating always
    queryset = StudyMaterial.objects.filter(approved=True).annotate(
        avg_rating=Avg('ratings__rating')
    )
    
    # Search filter
    if query := request.GET.get('q'):
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        )
    
    # Category filter
    if category := request.GET.get('category'):
        queryset = queryset.filter(category__id=category)
    
    # Min rating filter (apply after annotation)
    if min_rating := request.GET.get('min_rating'):
        try:
            min_rating_value = float(min_rating)
            queryset = queryset.filter(avg_rating__gte=min_rating_value)
        except ValueError:
            pass  # ignore invalid min_rating values
    
    # Pagination params
    page_size = int(request.GET.get('page_size', 10))
    page = int(request.GET.get('page', 1))
    total = queryset.count()
    
    # Slice queryset for page
    results = queryset[(page - 1) * page_size : page * page_size]
    
    serializer = MaterialSerializer(results, many=True)
    return Response({
        'results': serializer.data,
        'total': total,
        'page': page,
        'page_size': page_size,
    })
