from django.core.management import call_command
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
import sys, io
import os

@api_view(['GET'])
@permission_classes([AllowAny])
def do_migrate(request):
    try:
        old_stdout = sys.stdout
        sys.stdout = mystdout = io.StringIO()
        call_command('makemigrations')
        call_command('migrate')
        sys.stdout = old_stdout
        return Response({
            'DATABASE_URL_IN_ENV': os.environ.get('DATABASE_URL', 'NOT_SET'),
            'output': mystdout.getvalue()
        })
    except Exception as e:
        return Response({'error': str(e), 'url': os.environ.get('DATABASE_URL', 'NOT_SET')}, status=500)
