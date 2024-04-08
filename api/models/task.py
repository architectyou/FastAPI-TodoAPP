from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from api.db import Base

class Task(Base) :
    __tablename__="tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String(1024))

    # cascade에서 delete를 지정하면 DELETE / tasks/{task_id} 인터페이스에서 Task를 삭제할 때
    # 외부 키에 지정된 동일한 id의 done 이 있으면 자동으로 삭제됨.
    done = relationship("Done", back_populates="task", cascade="delete")

class Done(Base) :
    __tablename__="dones"

    id = Column(Integer, ForeignKey("tasks.id"), primary_key=True)
    task = relationship("Task", back_populates="done")