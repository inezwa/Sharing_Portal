# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from django.db.models import Avg
# from .models import StudyMaterial
# from .serializers import MaterialSerializer

# @api_view(['GET'])
# def material_api(request):
#     queryset = StudyMaterial.objects.filter(approved=True)
    
#     # Apply filters
#     if category_id := request.GET.get('category'):
#         queryset = queryset.filter(category__id=category_id)
    
#     if min_rating := request.GET.get('min_rating'):
#         queryset = queryset.annotate(
#             avg_rating=Avg('ratings__rating')
#         ).filter(avg_rating__gte=min_rating)
    
#     serializer = MaterialSerializer(queryset, many=True)
#     return Response(serializer.data)