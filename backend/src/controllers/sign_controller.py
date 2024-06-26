from typing import (
    Annotated, 
    Dict
)
from datetime import datetime

from fastapi import (
    Depends, 
    HTTPException,
    Response
)
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.security import HTTPBearer

from fastapi_controllers import (
    Controller, 
    get,
    post,
    put
)

from src.prisma import prisma
from prisma.models import Admissions_committee_secretary

from ..auth.auth_bearer import JWTBearer

from ..pydanticClasses.signData import SignIn_request_pydantic

from ..services.sign_service import SignService
from ..services.common_service import CommonService

security = HTTPBearer()


class SignController (Controller):
    __signService: SignService
    __commonService: CommonService


    def __init__ (self, signService: SignService = Depends(SignService), commonService: CommonService = Depends(CommonService)) -> None:
        self.__signService = signService
        self.__commonService = commonService
    

    @post('/in', response_class = PlainTextResponse)
    async def signIn (self, jwt: Annotated[str | None, Depends(JWTBearer())], signData: SignIn_request_pydantic, response: Response) -> str:
        existingSecretaryData: Admissions_committee_secretary | None = await prisma.admissions_committee_secretary.find_unique(where = { 'login': signData.login })

        if existingSecretaryData == None: raise HTTPException(status_code = 400, detail = "Secretary does not exists.")

        return await self.__signService.signIn(signData, existingSecretaryData, jwt, response, self.__commonService)
    

    @put('/out')
    async def signOut (self, jwt: Annotated[str, Depends(JWTBearer())]) -> None:
        return await self.__signService.signOut(jwt)


    @get('/getActiveClient', response_class = JSONResponse)
    async def getActiveClient (self, jwt: Annotated[str | None, Depends(JWTBearer())]) -> Dict[ str, str | int | datetime | None ] | None:
        if jwt == None: return None

        return await self.__signService.getActiveClient(jwt)