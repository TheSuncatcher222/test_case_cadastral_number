from asyncio import sleep as async_sleep
import random

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

from models import CadastralNumber

app: FastAPI = FastAPI(
    title='Сторонний сервис для валидации кадастрового номера',
)


@app.post(path='/validate_cadastral/')
async def validate_cadastral(cadastral: CadastralNumber) -> JSONResponse:
    """
    Производит валидацию указанного кадастрового номера.
    На процесс валидации уходит разное количество времени от 0 до 60 секунд.
    Сервис может вернуть "True" или "False, либо разорвать соединение.
    """
    # INFO: по условию ТЗ сервер может "думать" до 60 секунд.
    #       В качестве упрощения, время ожидания сокращено до 5 секунд.
    server_delay: int = random.choice(range(1,5))
    await async_sleep(server_delay)
    return_error: bool = random.choices((True, False,), weights=(0.8, 0.2,))[0]
    if not return_error:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "detail": "Server is unavaliable. Sorry. We fixing it."
            },
    )
    cadastral_status: bool = random.choice((True, False,))
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "status": cadastral_status,
            "cadastral_number": cadastral.number
        },
    )

if __name__ == '__main__':
    """Запуск сервера через Uvicorn на порту 8000."""
    import uvicorn
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
