from rest_framework import serializers
from .models import *

class PostSerializer(serializers.ModelSerializer):

    id = serializers.CharField(read_only=True)
    created_at = serializers.CharField(read_only=True)
    updated_at = serializers.CharField(read_only=True)

    tag = serializers.SerializerMethodField()
    image = serializers.ImageField(use_url=True, required=False)
    comments = serializers.SerializerMethodField(read_only=True)

    def get_comments(self, instance):
        serializer = CommentSerializer(instance.comments, many=True)
        return serializer.data
    
    def get_tag(self, instance):
        #self : MovieSerializer 자체
        #instance : serializer에서 만든 model의 객체
        tags = instance.tag.all()
        return [tag.name for tag in tags]

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "comments",
            "like_cnt"
        ]

class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['post']
    
class PostListSerializer(serializers.ModelSerializer):
    comments_cnt = serializers.SerializerMethodField()
    tag = serializers.SerializerMethodField()

    def get_comments_cnt(self, instance):
        return instance.comments.count()
    
    def get_tag(self, instance):
        tags = instance.tag.all()
        return [tag.name for tag in tags]
    
    class Meta:
        model = Post
        fields = [
            "id",
            "name",
            "created_at",
            "updated_at",
            "image",
            "comments_cnt",
            "tag",
            "like_cnt"
        ]
        read_only_fields = ["id", "created_at", "updated_at", "comments_cnt"]