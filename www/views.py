from django.http import HttpResponse
from moviepy.editor import TextClip, ColorClip, CompositeVideoClip
from moviepy.config import change_settings
import tempfile
import os
from .models import RequestLog


# change_settings({"IMAGEMAGICK_BINARY": r"E:\ImageMagick-7.1.1-Q16-HDRI\magick.exe"})  # Windows
change_settings({"IMAGEMAGICK_BINARY": "/usr/bin/convert"})  # Linux

def create_video(request):
    text = request.GET.get('text', 'Hello')
    if not text:
        return HttpResponse("Text parameter is required", status=400)

    # сохранить запрос в БД
    RequestLog.objects.create(text=text)

    #текстовый клип
    fontsize = 30
    text_clip = TextClip(text, fontsize=fontsize, color='white', bg_color='black', size=(2000, 100))
    text_width = text_clip.w

    screen_width = 300  #ширина экрана видео
    max_duration = 3  #максимальная длительность видео

    
    speed = (text_width + screen_width) / max_duration

    #создание кадра с текстом
    def make_frame(t):
        position = int(speed * t)
        frame = text_clip.get_frame(t)
        start_position = max(0, position - screen_width)
        end_position = min(text_width, position + screen_width)
        
        return frame[:, start_position:end_position]

    #статичный фон
    background_clip = ColorClip(size=(screen_width, 100), color=(0, 0, 0))  # Черный фон

    #видео с бегущим текстом
    video = CompositeVideoClip([background_clip.set_duration(max_duration), text_clip.set_make_frame(make_frame)], size=(screen_width, 100))
    video = video.set_duration(max_duration)  # Устанавливаем фиксированную длительность

    #temp-файл
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_file:
        temp_file.close()
        video.write_videofile(temp_file.name, fps=24)
        
        
        with open(temp_file.name, 'rb') as f:
            response = HttpResponse(f.read(), content_type='video/mp4')
            response['Content-Disposition'] = 'attachment; filename="my_video.mp4"'
            
        os.remove(temp_file.name)
        return response