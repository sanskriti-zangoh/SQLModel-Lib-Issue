# ---INFO-----------------------------------------------------------------------
"""
Module for Help Model.
"""
# ---DEPENDENCIES---------------------------------------------------------------
from sqlmodel import Field, SQLModel, Relationship, Column, ForeignKey, Integer


# ---MODELS---------------------------------------------------------------------

class VSQLModel(SQLModel):
    model_config = {
        "validate_assignment": True,
    }

class User(VSQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    email: str
    hashed_password: str = Field(default=None, nullable=True)

    chats: list["Chats"] = Relationship(back_populates="user")

class Chats(VSQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    description: str
    
    owner_id: int = Field(sa_column=Column("owner_id", Integer,ForeignKey("user.id", onupdate="CASCADE")))
    user: "User" = Relationship(back_populates="chats")



if __name__ == "__main__":
    user_list, chat_list = [], []
    for i in range(7):
        user_list.append(User(id=i, name=f"name{i}", email=f"email{i}", hashed_password=f"password{i}"))

    for user in user_list:
        chat_list.append(Chats(id=i, description=f"description{i}", owner_id=user.id))

    # chat_list.append(Chats(id=7, description="description", owner_id=90))

    # test for error handling





