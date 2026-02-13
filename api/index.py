import os
import sys
from django.core.wsgi import get_wsgi_application

# Добавляем директорию проекта в путь Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pro_core.settings')

application = get_wsgi_application()