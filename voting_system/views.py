from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView


# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Vote, Project



class VoteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Create a new vote and associate it with the requesting user.
        """
        user = request.user
        data = request.data

        # Create a new vote
        def find_project(idd):
            try:
                if idd is None:
                    return None
                return Project.objects.get(id=idd)
            except Project.DoesNotExist:
                return None
        project = find_project(data.get("project_id"))
        if project is None:
            return Response({"error": "Project not found"}, status=status.HTTP_400_BAD_REQUEST)

        vote = Vote.objects.update_or_create(
            project=project,
            v_user=user,
            status=data.get("status", "active"),
            value=data.get("value"),
        )

        return Response(
            {"message": "Vote created successfully", "vote_id": vote.id},
            status=status.HTTP_201_CREATED,
        )

    def put(self, request):
        """
        Update an existing vote associated with the authenticated user and a project.
        """
        user = request.user
        data = request.data

        # Find the project associated with the vote
        def find_project(idd):
            try:
                if idd is None:
                    return None
                return Project.objects.get(id=idd)
            except Project.DoesNotExist:
                return None

        project = find_project(data.get("project_id"))
        if project is None:
            return Response({"error": "Project not found"}, status=status.HTTP_400_BAD_REQUEST)

        # Find the vote associated with the user and project
        try:
            vote = Vote.objects.get(project=project, v_user=user)
        except Vote.DoesNotExist:
            return Response(
                {"error": "Vote not found for the specified project and user"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Update vote fields
        vote.status = data.get("status", vote.status)
        vote.value = data.get("value", vote.value)

        vote.save()

        return Response(
            {"message": "Vote updated successfully", "vote_id": vote.id},
            status=status.HTTP_200_OK,
        )

    def delete(self, request):
        """
        Delete an existing vote associated with the authenticated user and a project.
        """
        user = request.user
        data = request.data

        # Find the project associated with the vote
        def find_project(idd):
            try:
                return Project.objects.get(id=idd)
            except Project.DoesNotExist:
                return None

        project = find_project(data.get("project_id"))
        if project is None:
            return Response({"error": "Project not found"}, status=status.HTTP_400_BAD_REQUEST)

        # Find the vote associated with the user and project
        try:
            vote = Vote.objects.get(project=project, v_user=user)
        except Vote.DoesNotExist:
            return Response(
                {"error": "Vote not found for the specified project and user"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Delete the vote
        vote.delete()

        return Response(
            {"message": "Vote deleted successfully", "vote_id": vote.id},
            status=status.HTTP_200_OK,
        )

