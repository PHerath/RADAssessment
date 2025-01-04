from fastapi import FastAPI, Request
from starlette.responses import JSONResponse
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

from exception.exception import CrudException, NoDataFoundException, BadRequestException


def add_exception_handler(app: FastAPI):
    @app.exception_handler(Exception)
    async def handle_generic_exception(_request: Request, exc: Exception):
        return JSONResponse(status_code=HTTP_400_BAD_REQUEST,
                            content={'success': False,
                                     'message': str(exc)})

    @app.exception_handler(NoDataFoundException)
    async def handle_not_data_found_exception(_request: Request, exc: NoDataFoundException):
        return JSONResponse(status_code=HTTP_404_NOT_FOUND,
                            content={'success': False,
                                     'message': exc.message})

    @app.exception_handler(CrudException)
    async def handle_crud_exception(_request: Request, exc: CrudException):
        return JSONResponse(status_code=HTTP_400_BAD_REQUEST,
                            content={'success': False,
                                     'message': exc.message})

    @app.exception_handler(BadRequestException)
    async def handle_bad_request_exception(_request: Request, exc: BadRequestException):
        return JSONResponse(status_code=HTTP_400_BAD_REQUEST,
                            content={'success': False,
                                     'message': exc.message})
