from prisma import Prisma

prisma = Prisma(log_queries = True)

# venv/Scripts/activate
# prisma generate --schema=./src/prisma/schema.prisma
# prisma migrate dev --schema=./src/prisma/schema.prisma