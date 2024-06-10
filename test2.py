from sqlmodel import Field, Session, SQLModel, create_engine, select
from sqlalchemy import event
from basics_relations2 import User, Chats

sqlite_file_name = "testing_relation2.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

@event.listens_for(engine, "connect")
def enable_foreign_keys(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


def create_db_and_tables():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)


def create_instances():
    user_list, chat_list = [], []
    for i in range(7):
        user_list.append(User(id=i, name=f"name{i}", email=f"email{i}", hashed_password=f"password{i}"))

    for i, user in enumerate(user_list):
        chat_list.append(Chats(id=i, description=f"description{i}", owner_id=user.id))


    for i in range(len(user_list)):
        print(f"id:\t{user_list[i].id}, name:\t{user_list[i].name}, email:\t{user_list[i].email}, hashed_password:\t{user_list[i].hashed_password}")
    for i in range(len(chat_list)):
        print(f"id:\t{chat_list[i].id}, description:\t{chat_list[i].description}, owner_id:\t{chat_list[i].owner_id}")

    session = Session(engine)

    for user in user_list:
        session.add(user)
        session.commit()
        session.refresh(user)

    session.commit()


    chat_list.append(Chats(id=7, description="description", owner_id=90))
    chat_list.append(Chats(id=10, description="description", owner_id=100))

    chat_list.append(Chats(id=8, description="description", owner_id=1))
    chat_list.append(Chats(id=9,description="description", owner_id=1))

    for chat in chat_list:
        session.add(chat)
        session.commit()
        session.refresh(chat)
    session.commit()


    session.close()

def verify_instances():
    with Session(engine) as session:
        statement = select(User)
        results = session.exec(statement)
        for user in results:
            print(user)
        
        statement = select(Chats)
        results = session.exec(statement)
        for chat in results:
            print(chat)

        session.close()


def main():
    create_db_and_tables()
    create_instances()
    verify_instances()


if __name__ == "__main__":
    main()