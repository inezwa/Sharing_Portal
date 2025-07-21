from rest_framework import serializers
from .models import StudyMaterial

class MaterialSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name')
    file_url = serializers.SerializerMethodField()
    average_rating = serializers.FloatField(read_only=True)  # Accept annotated average rating
    user_rating = serializers.SerializerMethodField()  # Get current user’s rating for this material
    
    class Meta:
        model = StudyMaterial
        fields = [
            'id', 'title', 'description', 
            'file_url', 'category_name',
            'upload_date', 'average_rating',
            'user_rating',
        ]
    
    def get_file_url(self, obj):
        return obj.file.url if obj.file else None
    
    def get_user_rating(self, obj):
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            rating = obj.ratings.filter(user=request.user).first()
            return rating.rating if rating else None
        return None
