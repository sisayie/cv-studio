import json
from django.contrib.auth.models import User
from django.http import HttpResponse
from rest_framework import generics, viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .models import CV
from .serializers import RegisterSerializer, CVSerializer
from .exports import export_json, export_pdf, export_docx

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

class CVViewSet(viewsets.ModelViewSet):
    serializer_class = CVSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return CV.objects.filter(owner=self.request.user)
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    @action(detail=False, methods=["post"], url_path="import")
    def import_cv(self, request):
        payload = request.data
        if not isinstance(payload, dict): return Response({"detail":"Expected a JSON object."}, status=400)
        data = payload.get("data", payload)
        cv = CV.objects.create(
            owner=request.user,
            title=payload.get("title", "Imported CV"),
            language=payload.get("language", "en"),
            template=payload.get("template", "modern"),
            data=data if isinstance(data, dict) else {},
        )
        return Response(self.get_serializer(cv).data, status=status.HTTP_201_CREATED)
    @action(detail=True, methods=["get"], url_path="export")
    def export(self, request, pk=None):
        cv = self.get_object()
        fmt = request.query_params.get("format", "json").lower()
        if fmt == "json": return export_json(cv)
        if fmt == "pdf": return export_pdf(cv)
        if fmt == "docx": return export_docx(cv)
        return Response({"detail":"Supported formats: pdf, docx, json."}, status=400)
