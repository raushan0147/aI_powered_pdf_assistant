from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.users.service import get_user_by_email ,create_user

from app.core.security import hash_password , verify_password ,create_access_token




async def register_controller(data, db: AsyncSession):
    existing_user = await get_user_by_email(db, data.email)

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    hashed_pass = hash_password(data.password)

    user = await create_user(
        db=db, name=data.name, email=data.email, hashed_password=hashed_pass
    )

    return {
        "message": "User registered successfully",
        "user": {"id": user.id, "name": user.name, "email": user.email},
    }



async def login_controller(data, db: AsyncSession):
    user = await get_user_by_email(db, data.email)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(data={"user_id": user.id, "email": user.email})

    return {"access_token": token, "token_type": "bearer"}
