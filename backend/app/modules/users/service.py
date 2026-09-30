from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.modules.users.models import User


async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(
        select(User).where(User.email == email)
    )
    return result.scalar_one_or_none()


async def create_user(db: AsyncSession, name: str, email: str, hashed_password: str):
    user = User(
        name=name,
        email=email,
        hashed_password=hashed_password
    )

    db.add(user)
    await db.commit()
    await db.refresh(user)

    return user

