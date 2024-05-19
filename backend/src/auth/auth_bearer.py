from typing import (
    Dict, 
    cast
)

from datetime import datetime
import hashlib

from fastapi import (
    Request, 
    HTTPException
)
from fastapi.security import (
    HTTPBearer, 
    HTTPAuthorizationCredentials
)

from .auth_handler import decode_jwt

from src.auth.additionalJWT import validateRevokedJWT

from prisma.models import Admissions_committee_secretary
from src.prisma import prisma


class JWTBearer (HTTPBearer):
    def __init__ (self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error = auto_error)


    async def __call__ (self, request: Request) -> str | None:
        credentials: HTTPAuthorizationCredentials | None = await super(JWTBearer, self).__call__(request)

        requestURLPath: str = request.url.path
        __secure_fgp: str | None =  request.cookies.get('__secure_fgp')

        if ( requestURLPath != '/api/sign/in' and requestURLPath != '/api/sign/getActiveClient' ) and __secure_fgp == None: 
            raise HTTPException(status_code = 401, detail = "Cookie __secure_fgp does not exists.")

        if credentials:
            if not credentials.scheme == "Bearer":
                if requestURLPath != '/api/sign/in' and requestURLPath != '/api/sign/getActiveClient': raise HTTPException(status_code = 403, detail = "Invalid authentication scheme.")
                else: return None

            jwtPayload: Dict[ str, str | int | datetime | None ] | None = await self.__verify_jwt(credentials.credentials)

            if jwtPayload == None:
                if requestURLPath != '/api/sign/in' and requestURLPath != '/api/sign/getActiveClient': raise HTTPException(status_code = 403, detail = "Invalid or expired token.")
                else: return None
            elif requestURLPath != '/api/sign/in':
                verifySecure_fgpHashResult: bool = False

                if requestURLPath != '/api/sign/getActiveClient': verifySecure_fgpHashResult = await self.__verifySecure_fgpHash(credentials.credentials, jwtPayload, cast(str, __secure_fgp), True)
                else: verifySecure_fgpHashResult = await self.__verifySecure_fgpHash(credentials.credentials, jwtPayload, cast(str, __secure_fgp), False)

                if verifySecure_fgpHashResult == True: await self.__checkClientExistence(jwtPayload)
                else: return None
                
            return credentials.credentials
        else:
            if requestURLPath != '/api/sign/in' and requestURLPath != '/api/sign/getActiveClient': raise HTTPException(status_code = 403, detail = "Invalid authorization code.")
            else: return None


    async def __verify_jwt (self, jwt: str) -> Dict[ str, str | int | datetime | None ] | None:
        try:
            payload: Dict[ str, str | int | datetime | None ] | None = decode_jwt(jwt)
        except:
            payload = None

        return payload
    

    async def __verifySecure_fgpHash (self, jwt: str, jwtPayload: Dict[ str, str | int | datetime | None ], secure_fgp: str, raiseError: bool = True) -> bool:
        client__secure_fgpHash: str = hashlib.sha256(secure_fgp.encode('utf-8')).hexdigest()

        jwtIsRevoked: bool = await validateRevokedJWT(jwt)

        if client__secure_fgpHash != jwtPayload['__secure_fgpHash'] or jwtIsRevoked == False: 
            if raiseError == True: raise HTTPException(status_code = 401, detail = "Secure fingerprint hash is invalid.")
            else: return False

        return True
    
    
    async def __checkClientExistence (self, jwtPayload: Dict[ str, str | int | datetime | None ]) -> None:
        existingClientData: Admissions_committee_secretary | None = await prisma.admissions_committee_secretary.find_unique(where = { 'id': cast(int, jwtPayload['id']) })

        if existingClientData == None: raise HTTPException(status_code = 401, detail = 'Secretary instance does not exists.')