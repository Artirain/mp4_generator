from django.http import HttpResponse
from moviepy.editor import TextClip, CompositeVideoClip #Классы из библиотеки MoviePy для работы с видео и текстом.
from moviepy.config import change_settings
import tempfile
import os
from .models import RequestLog  # импорт модели

change_settings({"IMAGEMAGICK_BINARY": r"E:\ImageMagick-7.1.1-Q16-HDRI\magick.exe"})

def create_video(request):
    text = request.GET.get('text', 'Hello') #если параметр не указан, по умолчанию будет "Hello"
    if not text:
        return HttpResponse("Text parameter is required", status=400)

    # сохраняем запрос в базе данных
    RequestLog.objects.create(text=text)

    # создаем видео с размером больше 100x100 для анимации
    fontsize = 20
    text_clip = TextClip(text, fontsize=fontsize, color='white', bg_color='pink', size=(300, 100))
    text_clip = text_clip.set_duration(3) #продолжительность текста в 3 секунды
    
    # перемещаем текст по горизонтали
    def frame(t):
        frame = text_clip.get_frame(t)
        frame_width = text_clip.w
        position = int(t * 100) % frame_width
        return frame[:, position:position + 100]

    # создаем видео с бегущим текстом в 100x100 пикселей
    video = CompositeVideoClip([text_clip.set_make_frame(frame)], size=(100, 100))
    video = video.set_duration(3)

    # создаем временный файл
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_file:
        temp_file.close()
        video.write_videofile(temp_file.name, fps=24)
        
        # Отправляем файл как
        with open(temp_file.name, 'rb') as f:
            response = HttpResponse(f.read(), content_type='video/mp4')
            response['Content-Disposition'] = 'attachment; filename="my_video.mp4"' #заголовок для загрузки файла
            
        os.remove(temp_file.name)
        return response
