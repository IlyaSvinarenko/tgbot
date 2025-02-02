from aiogram.types import InputFile
from pytube import YouTube
import logging
from io import BytesIO


def download_video(link: str):
    try:
        yt = YouTube(link)

        # Выбираем лучший поток (например, с наибольшим разрешением)
        stream = yt.streams.filter(file_extension='mp4').get_highest_resolution()

        # Скачиваем видео в память
        video_stream = stream.stream_to_buffer()

        # Создаем объект InputFile из BytesIO
        video_byte_arr = BytesIO(video_stream)
        video_byte_arr.seek(0)  # Убираем возможное смещение указателя

        # Создаем объект InputFile
        input_file = InputFile(video_byte_arr, filename="video.mp4")

        logging.info(f"Video from {link} sent successfully.")
        return input_file
    except Exception as e:
        logging.error(f"Error downloading or sending video: {e}")
        return e