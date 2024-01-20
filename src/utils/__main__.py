import asyncio
import getpass

from passlib.context import CryptContext
from sqlalchemy import insert, select

from core.models.users import User
from core.settings.connections import session

bcrypt = CryptContext(schemes=["bcrypt"])


async def create_superuser():
    while True:
        email = input("Enter email address: ")

        async with session() as conn:
            query = select(User).where(User.email == email)

            result = await conn.execute(query)

            if result.scalar_one_or_none() is not None:
                print("User with this email already exists")
                continue

            break

    first_name = input("Enter firt name (optional): ")
    last_name = input("Enter last name (optional): ")

    while True:
        password1 = getpass.getpass("Enter the password: ")
        password2 = getpass.getpass("Confirm password: ")

        if password1 != password2:
            print("\033[91mPassword must be the same please try again!\033[91m")

            check = input("Do you want rewrite? Y/n ")
            if check.lower() in ["n", "no"]:
                exit()

            continue

        break

    hash_password = bcrypt.hash(password1)

    data = {
        "email": email,
        "first_name": first_name if first_name else "admin",
        "last_name": last_name if last_name else "admin",
        "hashed_password": hash_password,
        "role": "admin",
    }
    async with session() as conn:
        query = insert(User).values(**data)

        await conn.execute(query)

        await conn.commit()

        print("Superuser successfull create")


if __name__ == "__main__":
    try:
        asyncio.run(create_superuser())
    except KeyboardInterrupt:
        exit()
