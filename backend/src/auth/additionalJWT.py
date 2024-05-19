from datetime import datetime

import hashlib

from src.prisma import prisma
from prisma.models import JWT_token


async def validateRevokedJWT (jwt: str) -> bool:
    revokedJWTData: JWT_token | None = await checkRevokedJWTIs(jwt)

    datetimeNow: datetime = datetime.now()

    if revokedJWTData != None:
        if datetimeNow.replace(tzinfo = None) > revokedJWTData.revokation_date.replace(tzinfo = None): return False

    return True


async def checkRevokedJWTIs (jwt: str) -> JWT_token | None:
    jwt_hash: str = hashlib.sha256(jwt.encode('utf-8')).hexdigest()

    revokedJWTData: JWT_token | None = await prisma.jwt_token.find_first(where = {
        'jwt_hash': jwt_hash,
        'revoked': True
    })

    return revokedJWTData