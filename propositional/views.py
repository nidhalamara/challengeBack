from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from propositional.models import Proposition


class CreateProposition(APIView):
    def post(self, request):
        title = request.data.get('title')
        description = request.data.get('description')
        place = request.data.get('place')

        try:
            # Create a new proposition and associate it with the authenticated user
            proposition = Proposition.objects.create(
                title=title,
                description=description,
                place=place,
                user=request.user
            )
        except Exception as e:
            return Response({"error": True, "details": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {
                "id": proposition.id,
                "title": proposition.title,
                "description": proposition.description,
                "place": proposition.place,
                "user": proposition.user.id,
            },
            status=status.HTTP_201_CREATED,
        )
class PropositionDetail(APIView):
    def get(self, request, proposition_id):
        try:
            # Get a specific proposition
            proposition = Proposition.objects.get(id=proposition_id, user=request.user)
        except Proposition.DoesNotExist:
            return Response({"error": "Proposition not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response(
            {
                "id": proposition.id,
                "title": proposition.title,
                "description": proposition.description,
                "place": proposition.place,
                "user": proposition.user.id,
            },
            status=status.HTTP_200_OK,
        )

    def put(self, request, proposition_id):
        title = request.data.get('title')
        description = request.data.get('description')
        place = request.data.get('place')

        try:
            # Update the proposition if it exists
            proposition = Proposition.objects.get(id=proposition_id, user=request.user)
            proposition.title = title if title else proposition.title
            proposition.description = description if description else proposition.description
            proposition.place = place if place else proposition.place
            proposition.save()
        except Proposition.DoesNotExist:
            return Response({"error": "Proposition not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response(
            {
                "id": proposition.id,
                "title": proposition.title,
                "description": proposition.description,
                "place": proposition.place,
                "user": proposition.user.id,
            },
            status=status.HTTP_200_OK,
        )

    def delete(self, request, proposition_id):
        try:
            # Delete the proposition
            proposition = Proposition.objects.get(id=proposition_id, user=request.user)
            proposition.delete()
        except Proposition.DoesNotExist:
            return Response({"error": "Proposition not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response({"message": "Proposition deleted successfully"}, status=status.HTTP_200_OK)
