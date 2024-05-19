from typing import (
    Dict,
    cast
)
from datetime import (
    datetime, 
    timedelta
)
import hashlib
import string
import random

from fastapi import (
    HTTPException,
    Response
)

from src.prisma import prisma
from prisma.models import (
    Admissions_committee_secretary,
    JWT_token
)

from argon2 import PasswordHasher

from python_ms import ms

from ..auth.auth_handler import (
    sign_jwt, 
    decode_jwt
)

from src.auth.additionalJWT import checkRevokedJWTIs

from ..config.config import settings

from ..pydanticClasses.signData import SignIn_request_pydantic

from ..services.common_service import CommonService


class SignService:
    def __init__ (self):
        pass


    async def signIn (self, signData: SignIn_request_pydantic, existingSecretaryData: Admissions_committee_secretary, jwt: str | None, response: Response, commonService: CommonService) -> str:
        if jwt != None: await self.__addRevokedJWT(jwt)

        clientLogin: str = signData.login.strip()
        clientPassword: str = signData.password.strip()

        if existingSecretaryData.login == clientLogin:
            passwordHasher = PasswordHasher()

            try:
                passwordIsValid: bool = passwordHasher.verify(existingSecretaryData.password, clientPassword)
            except:
                passwordIsValid = False

            if passwordIsValid == True:
                lastSignInDate: int | None = None

                if existingSecretaryData.lastSignInDate != None: lastSignInDate = existingSecretaryData.lastSignInDate.time().microsecond * 1000

                jwtPayload: Dict[ str, str | int | datetime | None ] = {
                    'id': existingSecretaryData.id,
                    'login': existingSecretaryData.login,
                    'lastSignInDate': lastSignInDate,
                    '__secure_fgpHash': ''
                }

                __secure_fgpData: Dict[str, str] = self.__generate__secure_fgp()

                jwtPayload['__secure_fgpHash'] = __secure_fgpData['__secure_fgpHash']

                await prisma.admissions_committee_secretary.update({ 'lastSignInDate': datetime.now() }, where = {
                    'id': existingSecretaryData.id
                })

                newJwt: str = sign_jwt(jwtPayload)

                await self.__saveJWT(newJwt)

                response.set_cookie(key = '__secure_fgp', value = __secure_fgpData['__secure_fgp'], **commonService.cookieParameters)

                return newJwt
            else: raise HTTPException(status_code = 401, detail = "Password is invalid.")
        else: raise HTTPException(status_code = 400, detail = "Login and existing secretary login does not mathing.")


    async def signOut (self, jwt: str) -> None:
        return await self.__addRevokedJWT(jwt)


    async def getActiveClient (self, jwt: str, raiseError = True) -> Dict[ str, str | int | datetime | None ] | None:
        jwtPayload: Dict[ str, str | int | datetime | None ] = cast(Dict[ str, str | int | datetime | None ], decode_jwt(jwt))

        existingSecretaryData: Admissions_committee_secretary | None = await prisma.admissions_committee_secretary.find_unique(where = { 'login': cast(str, jwtPayload['login']) })

        if existingSecretaryData == None: 
            if raiseError == True: raise HTTPException(status_code = 401, detail = "Secretary instance does not exists.")
            else: return None

        return jwtPayload


    async def __saveJWT (self, jwt: str) -> None:
        jwt_hash: str = hashlib.sha256(jwt.encode('utf-8')).hexdigest()

        JWT_EXPIRESIN_TIME: str = settings['JWT_EXPIRESIN_TIME']

        expires_date: datetime = datetime.now() + timedelta(milliseconds = ms.parse_time(JWT_EXPIRESIN_TIME))

        await prisma.jwt_token.create(data = { 
            'jwt_hash': jwt_hash,
            'expires_date': expires_date,
            'revokation_date': expires_date
        })


    async def __addRevokedJWT (self, jwt: str) -> None:
        revokedJWTData: JWT_token | None = await checkRevokedJWTIs(jwt)

        if revokedJWTData == None:
            jwt_hash: str = hashlib.sha256(jwt.encode('utf-8')).hexdigest()

            revokation_date: datetime = datetime.now()

            await prisma.jwt_token.update(where = { 'jwt_hash': jwt_hash }, 
                data = {
                    'revokation_date': revokation_date, 
                    'revoked': True 
                }
            )


    def __generate__secure_fgp (self) -> Dict[ str, str ]:
        __secure_fgp: str = ''.join(random.choices(string.ascii_letters, k = 50))
        __secure_fgpHash: str = hashlib.sha256(__secure_fgp.encode('utf-8')).hexdigest()

        return {
            '__secure_fgp': __secure_fgp,
            '__secure_fgpHash': __secure_fgpHash
        }