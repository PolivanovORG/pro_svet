# Техническое задание на создание сайта для борьбы с зависимостями

## 1. Общее описание

Создание веб-платформы на Django для помощи пользователям в борьбе с различными формами зависимостей через систему мотивации, отслеживания прогресса и образовательного контента.

## 2. Функциональные требования

### 2.1. Структура зависимостей
- **Предустановленные зависимости (8-9 штук):**
  - Игровая зависимость
  - Шопоголизм
  - Думскролинг (ТикТок и шортсы)
  - Зависимость от телевидения/стриминга
  - Пищевая зависимость
  - Алкоголь, Наркотки и Никотин (Химическая зависимость)
  - Лудомания
  - Порнография

### 2.2. Главная страница
- Отображение всех 8-9 зависимостей в виде карточек
- Каждая карточка содержит:
  - Название зависимости
  - Краткое описание
  - Кнопка "Подробнее"

### 2.3. Страницы зависимостей
- Подробная статья о каждой зависимости
- В конце статьи две кнопки:
  - "У меня нет этой зависимости"
  - "Определить уровень зависимости"

### 2.4. Система уровней просветления
- **Начальный уровень:** 0 XP
- **Награды за отсутствие зависимости:** +100 XP
- **Система лечения:**
  - Легкий уровень: 150 дней воздержания
  - Средний уровень: 350 дней воздержания
  - Тяжелый уровень: 700 дней воздержания
- **Опыт за воздержание:** +10 XP за каждый день
- **Штрафы:** -10 XP за каждый день срыва (2+ дней подряд)

### 2.5. Уведомления и мотивация
- **Цитата дня:** Ежедневная мотивирующая цитата
- **Условия отправки:**
  - Не отправлять, если пользователь не заходил более 3 дней
  - Отправлять только активным пользователям
- **Система предупреждений:** Уведомления о срывах

### 2.6. Визуальная система
- **Динамическая цветовая схема:**
  - Начальный уровень: черный фон, белый текст
  - Прогресс: плавный переход к белому фону, черному тексту
  - Полная трансформация при достижении высоких уровней
- **Индикация уровня:** Визуальные элементы, показывающие прогресс

### 2.7. Дополнительные функции
- **Создание собственной зависимости:**
  - Ограничение: 1 зависимость на пользователя
  - Только для личного использования
- **Полезные привычки:**
  - Система отслеживания положительных привычек
  - Бонусный опыт за выполнение
- **Поддержка разработчика:**
  - Кнопка доната
  - Информация о проекте

## 3. Страницы сайта

### 3.1. Главная страница
```
/
- Список зависимостей
- Быстрый доступ к профилю
- Статистика (если авторизован)
```

### 3.2. Страницы зависимостей
```
/dependencies/[slug]/
- Полная статья
- Кнопки действий
- Связанные зависимости
```

### 3.3. Профиль пользователя
```
/profile/
- Личная статистика
- Календарь воздержания
- Текущий уровень и опыт
- Список зависимостей пользователя
- Настройки уведомлений
```

### 3.4. Авторизация и регистрация
```
/login-register/
- Стандартная форма входа/регистрации
- Восстановление пароля
```

### 3.5. Административная панель
```
/admin/
- Управление зависимостями
- Статистика пользователей
- Управление цитатами
- Настройка системы уровней
```

## 4. Технические требования

### 4.1. Бэкенд (Django)

### 4.2. Фронтенд
- **HTML/CSS/JavaScript/Tailwind**
- **Chart.js** для визуализации прогресса
- **AJAX** для динамических обновлений

### 4.3. База данных
- **SQLite** (для разработки)

## 5. Бизнес-логика

### 5.1. Расчет опыта

### 5.2. Система уровней

### 5.3. Уведомления

## 6. Пользовательские сценарии

### 6.1. Новый пользователь
1. Регистрация на сайте
2. Изучение зависимостей на главной
3. Выбор зависимостей для отслеживания
4. Прохождение тестов на определение уровня
5. Начало лечения с получением календаря

### 6.2. Активный пользователь
1. Ежедневный вход на сайт
2. Отметка дней воздержания
3. Получение цитат дня
4. Отслеживание прогресса в профиле
5. Получение опыта и повышение уровня

### 6.3. Пользователь с срывом
1. Фиксация срыва в системе
2. Получение штрафных очков
3. Получение мотивирующих уведомлений
4. Возможность перезапуска лечения

## 7. Дополнительные возможности

### 7.1. Социальные функции
- Достижения и награды

### 7.2. Мобильная версия
- Адаптивный дизайн
- Push-уведомления
- Офлайн-режим для отметок

### 7.3. Аналитика
- Статистика по зависимостям
- Прогресс пользователей
- Эффективность лечения

## 8. Этапы разработки

### Этап 1: Базовая структура (2 недели)
- Настройка Django проекта
- Создание моделей базы данных
- Базовые шаблоны и стили

### Этап 2: Аутентификация и профиль (1 неделя)
- Система регистрации и входа
- Профиль пользователя
- Базовая статистика

### Этап 3: Система зависимостей (2 недели)
- Создание страниц зависимостей
- Тесты на определение уровня
- Календарь воздержания

### Этап 4: Система уровней и опыта (1 неделя)
- Расчет опыта
- Визуализация уровней
- Динамическая цветовая схема

### Этап 5: Уведомления и мотивация (1 неделя)
- Система цитат дня
- Push-уведомления
- Система предупреждений

### Этап 6: Тестирование и оптимизация (1 неделя)
- Тестирование функциональности
- Оптимизация производительности
- Исправление багов

## 9. Критерии приемки

- [ ] Все 8-9 зависимостей отображаются на главной
- [ ] Страницы зависимостей содержат полную информацию
- [ ] Система уровней работает корректно
- [ ] Уведомления отправляются по расписанию
- [ ] Цветовая схема меняется динамически
- [ ] Создание собственных зависимостей работает
- [ ] Система штрафов за срывы функционирует
- [ ] Адаптивный дизайн на всех устройствах
- [ ] Безопасность и защита данных пользователей

## 10. Технологический стек

## 11. Настройка проекта

### Установка зависимостей
```bash
pip install -r req.txt
pip install python-decouple
```

### Переменные окружения
Для настройки проекта используйте файл `.env` или переменные окружения. Создайте файл `.env` в корне проекта на основе шаблона `.env.example`:

```bash
cp .env.example .env
```

Затем измените значения в файле `.env` под свои нужды:

- `SECRET_KEY` - секретный ключ Django (должен быть длинным и случайным)
- `DEBUG` - режим отладки (True/False)
- `ALLOWED_HOSTS` - список разрешенных хостов, разделенных запятыми

Пример содержимого `.env`:
```
SECRET_KEY=ваш-секретный-ключ-здесь
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com
```

### Запуск проекта
```bash
python manage.py runserver
```

## 12. Настройка CI/CD

Проект использует GitHub Actions для автоматизации процесса CI/CD. Конфигурационный файл находится в `.github/workflows/django.yml`.

### Настройка секретов в GitHub

Для безопасного деплоя настройте следующие секреты в настройках репозитория на GitHub (`Settings` → `Secrets and variables` → `Actions`):

- `SECRET_KEY` - секретный ключ Django для продакшена (должен быть длинным и случайным)
- `DEBUG` - режим отладки (по умолчанию False для продакшена)
- `ALLOWED_HOSTS` - разрешенные хосты для продакшена

### Автоматические проверки

При каждом пуше в ветки `main` и `master`, а также при создании Pull Request выполняются следующие проверки:

- Запуск тестов
- Проверка миграций
- Проверка качества кода с помощью flake8

### Генерация SECRET_KEY

Для генерации безопасного SECRET_KEY в продакшене используйте следующий скрипт:

```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

Или в командной строке:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Совместимость версий Python

Проект использует Django 5.0+, который требует Python 3.10 или выше. При локальной разработке и деплое убедитесь, что используете Python 3.10 или выше.

GitHub Actions проверяет совместимость на версиях Python 3.10 и 3.12.

## 13. Настройка CD (Continuous Deployment)

Для автоматического деплоя приложения можно использовать GitHub Actions с различными провайдерами хостинга.

### Деплой на Vercel

1. Создайте аккаунт на [Vercel](https://vercel.com)
2. Установите CLI: `npm i -g vercel`
3. Свяжите проект: `vercel link`
4. Добавьте следующие секреты в GitHub:
   - `VERCEL_TOKEN` - токен API Vercel
   - `VERCEL_ORG_ID` - ID вашей организации в Vercel
   - `VERCEL_PROJECT_ID` - ID вашего проекта в Vercel
5. Убедитесь, что в корне проекта есть файл `vercel.json` для правильной конфигурации Django-приложения

Пример workflow для деплоя на Vercel (`.github/workflows/deploy-vercel.yml`):

```yaml
name: Deploy to Vercel

on:
  push:
    branches: [ main, master ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Setup Node.js
      uses: actions/setup-node@v4
      with:
        node-version: '18'
        
    - name: Install Vercel CLI
      run: npm install -g vercel
      
    - name: Deploy to Vercel
      run: |
        vercel --token=${{ secrets.VERCEL_TOKEN }} --prod --force
      env:
        VERCEL_ORG_ID: ${{ secrets.VERCEL_ORG_ID }}
        VERCEL_PROJECT_ID: ${{ secrets.VERCEL_PROJECT_ID }}
```

#### Особенности деплоя Django на Vercel

Для правильного деплоя Django-приложения на Vercel необходимо:

1. В корне проекта создать файл `vercel.json` с конфигурацией приложения
2. Убедиться, что все зависимости указаны в `requirements.txt`
3. Настроить статические файлы через `collectstatic`
4. Использовать экземпляр WSGI для обработки запросов

Файл `vercel.json` в этом проекте уже настроен для корректной работы Django-приложения.

### Деплой на Heroku

1. Создайте аккаунт на [Heroku](https://heroku.com)
2. Установите CLI: `heroku login`
3. Создайте приложение: `heroku create your-app-name`
4. Добавьте следующие секреты в GitHub:
   - `HEROKU_API_KEY` - API ключ Heroku
   - `HEROKU_APP_NAME` - название вашего приложения на Heroku

Пример workflow для деплоя на Heroku (`.github/workflows/deploy-heroku.yml`):

```yaml
name: Deploy to Heroku

on:
  push:
    branches: [ main, master ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.12'
        
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        
    - name: Deploy to Heroku
      uses: akhileshns/heroku-deploy@v3.12.12
      with:
        heroku_api_key: ${{ secrets.HEROKU_API_KEY }}
        heroku_app_name: ${{ secrets.HEROKU_APP_NAME }}
        heroku_email: your-email@example.com
        usedocker: false
        requirements_file: requirements.txt
```

### Деплой на PythonAnywhere

1. Создайте аккаунт на [PythonAnywhere](https://pythonanywhere.com)
2. Добавьте следующие секреты в GitHub:
   - `PYTHONANYWHERE_USERNAME` - ваш username на PythonAnywhere
   - `PYTHONANYWHERE_API_KEY` - API ключ (можно получить в Account → API token)
   - `PYTHONANYWHERE_HOSTNAME` - ваш hostname (обычно username.pythonanywhere.com)

Пример workflow для деплоя на PythonAnywhere (`.github/workflows/deploy-pythonanywhere.yml`):

```yaml
name: Deploy to PythonAnywhere

on:
  push:
    branches: [ main, master ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Deploy to PythonAnywhere
      run: |
        curl -X POST https://www.pythonanywhere.com/api/v0/user/${{ secrets.PYTHONANYWHERE_USERNAME }}/files/path/to/your/project \
          -H "Authorization: Token ${{ secrets.PYTHONANYWHERE_API_KEY }}" \
          -F "content=<." -F "path=."
          
    - name: Restart application
      run: |
        curl -X POST https://www.pythonanywhere.com/api/v0/user/${{ secrets.PYTHONANYWHERE_USERNAME }}/webapps/${{ secrets.PYTHONANYWHERE_HOSTNAME }}/reload/ \
          -H "Authorization: Token ${{ secrets.PYTHONANYWHERE_API_KEY }}"
```

### Деплой на собственный сервер через SSH

Если вы хотите деплоить на собственный сервер, добавьте следующие секреты в GitHub:
- `SSH_HOST` - адрес вашего сервера
- `SSH_USERNAME` - имя пользователя для SSH
- `SSH_PRIVATE_KEY` - приватный SSH ключ
- `DEPLOY_PATH` - путь до директории проекта на сервере

Пример workflow для деплоя на собственный сервер (`.github/workflows/deploy-ssh.yml`):

```yaml
name: Deploy to Server via SSH

on:
  push:
    branches: [ main, master ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Deploy to server
      uses: appleboy/scp-action@v0.1.4
      with:
        host: ${{ secrets.SSH_HOST }}
        username: ${{ secrets.SSH_USERNAME }}
        key: ${{ secrets.SSH_PRIVATE_KEY }}
        source: "."
        target: "${{ secrets.DEPLOY_PATH }}"
        strip_components: 1
        
    - name: Run deployment commands
      uses: appleboy/ssh-action@v0.1.5
      with:
        host: ${{ secrets.SSH_HOST }}
        username: ${{ secrets.SSH_USERNAME }}
        key: ${{ secrets.SSH_PRIVATE_KEY }}
        script: |
          cd ${{ secrets.DEPLOY_PATH }}
          source venv/bin/activate  # или путь к вашему виртуальному окружению
          pip install -r requirements.txt
          python manage.py collectstatic --noinput
          python manage.py migrate
          sudo systemctl restart gunicorn  # или ваш способ перезапуска приложения
```

---

**Дата создания:** 12 февраля 2026
**Версия:** 1.0
**Статус:** Активно для разработки