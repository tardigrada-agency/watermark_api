from starlette.background import BackgroundTask
from fastapi import FastAPI, File, UploadFile
from hachoir.metadata import extractMetadata
from fastapi.responses import FileResponse
from hachoir.parser import createParser
import subprocess as sp
from typing import List
import aiofiles
import modes
import os

app = FastAPI()


@app.post("/watermark_on_photo/{size}/{color}/{logo_type}/{mode}")
async def watermark_on_photo(size: int, color: str, logo_type: str, mode: str, file: UploadFile = File(...)):
    try:
        remove_photo(file.filename)
        with open(f'temp/{file.filename}', 'wb') as out_file:
            content = await file.read()  # async read
            out_file.write(content)  # async write
        img_size = get_size_size(f'temp/{file.filename}')
        logo_size = get_size_size(f'logo/{color}_{logo_type}.png')
        mode = modes.modes[mode]

        sp.call([
            'ffmpeg', '-i', f'temp/{file.filename}', '-i', f'logo/{color}_{logo_type}.png',
            # Меняем прозрачность и размер логотипа
            '-filter_complex', f'[1]format=yuva444p,curves=lighter,'
                               f'colorchannelmixer=aa={mode["opacity"](logo_size, img_size, size)},'
            # Меняем размер логотипа
            f'scale={mode["scale"](logo_size, img_size, size)}:-1[in2];'
            # Позиционируем логотип
            f'[0][in2]overlay='
            # рассчитываем отступы относительно разрешения фото и логотипа
            f'{mode["x"](logo_size, img_size, size)}:'
            f'{mode["y"](logo_size, img_size, size)}',
            # Указываем выходной файл
            '-q:v', '1',  f'temp/{get_filename(file.filename)}_logo.jpg'])

        return FileResponse(f'temp/{get_filename(file.filename)}_logo.jpg', background=BackgroundTask(remove_photo,
                                                                                                      file.filename))
    except Exception as err:
        return {'error': True,
                'status': err}


@app.post("/watermark_on_video/{size}/{color}/{logo_type}/{mode}")
async def watermark_on_video(size: int, color: str, logo_type: str, mode: str, file: UploadFile = File(...)):
    try:
        remove_video(file.filename)
        with open(f'temp/{file.filename}', 'wb') as out_file:
            content = await file.read()  # async read
            out_file.write(content)  # async write
        img_size = get_size_size(f'temp/{file.filename}')
        logo_size = get_size_size(f'logo/{color}_{logo_type}.png')
        mode = modes.modes[mode]

        sp.call([
            'ffmpeg', '-i', f'temp/{file.filename}', '-i', f'logo/{color}_{logo_type}.png',
            # Меняем прозрачность и размер логотипа
            '-filter_complex', f'[1]format=yuva444p,curves=lighter,'
                               f'colorchannelmixer=aa={mode["opacity"](logo_size, img_size, size)},'
            # Меняем размер логотипа
                               f'scale={mode["scale"](logo_size, img_size, size)}:-1[in2];'
            # Позиционируем логотип
                               f'[0][in2]overlay='
            # рассчитываем отступы относительно разрешения фото и логотипа
                               f'{mode["x"](logo_size, img_size, size)}:'
                               f'{mode["y"](logo_size, img_size, size)}',
            # Указываем выходной файл
            '-q:v', '1', f'temp/{get_filename(file.filename)}_logo.mp4'])

        return FileResponse(f'temp/{get_filename(file.filename)}_logo.mp4', background=BackgroundTask(remove_video,
                                                                                                  file.filename))
    except Exception as err:
        return {'error': True,
                'status': err}


def remove_video(filename: str):
    remove_file(f'temp/{get_filename(filename)}.mp4')
    remove_file(f'temp/{get_filename(filename)}_logo.mp4')


def remove_photo(filename: str):
    remove_file(f'temp/{get_filename(filename)}.jpg')
    remove_file(f'temp/{get_filename(filename)}_logo.jpg')


def remove_file(filename: str):
    if os.path.isfile(filename):
        os.remove(filename)


def get_filename(path: str) -> str:
    base = os.path.basename(path)
    return os.path.splitext(base)[0]


def get_size_size(file_path: str) -> list or Exception:
    """
    Получает разрешение файла
    :param file_path: Путь к файлу
    :return: Количество пикселей по высоте, количество пикселей по ширине
    """
    parser = createParser(file_path)
    with parser:
        try:
            metadata = extractMetadata(parser)
        except Exception as err:
            return err
    return [metadata.getValues('width')[0], metadata.getValues('height')[0]]