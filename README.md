# MP4 Generator
MP4 Generator — это веб-приложение на Django, которое генерирует скачиваемое MP4 видео с бегущей строкой. Вы можете настроить отображаемый текст в видео, передав его в качестве параметра URL.

# Основные функции
Генерация MP4 видео с настраиваемым бегущим текстом.
Изменение текста через параметр URL.
Загрузка сгенерированного видео напрямую через браузер.

# Демонстрация
Вы можете создать видео, перейдя по следующей ссылке:
   http://your-domain.com/video/?text=ваштекст

Замените "ваштекст" на текст, который вы хотите видеть в видео.

# Установка
Необходимые компоненты
Python 3.8 или выше
Django 3.2 или выше
PostgreSQL (для сохранения запросов в базу данных)
ImageMagick (для рендеринга текста в видео)