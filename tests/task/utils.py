from tests.utils import IMockDbManager, get_uuid4_as_str, AsyncSession
from tests.auth.utils import MockDbUserManager
from src.database import Base
from src.task.models import Tag, Task, M2MTask2Tag
from src.auth.models import User


class MockDbTagManager(IMockDbManager):
    async def _get_unique_object(self, **kwagrs) -> Base:
        """Kwargs:
        user_obj: (User), if not passsed eror
        """
        user = kwagrs.get("user_obj")
        if user is None or not isinstance(user, User):
            raise ValueError("Pass instance of user object")
        tag = Tag(name=get_uuid4_as_str(), user_id=user.id)
        return tag


class MockDbTaskManager(IMockDbManager):
    async def _get_unique_object(self, **kwagrs) -> Base:
        """Kwargs
        user_obj: (User), if not passsed eror
        """
        user = kwagrs.get("user_obj")
        if user is None or not isinstance(user, User):
            raise ValueError("Pass instance of user object")
        task = Task(name=get_uuid4_as_str(), priority_id=1, user_id=user.id)
        return task


class MockDbTag2TaskManager(IMockDbManager):
    async def _get_unique_object(self, **kwagrs) -> Base:
        """Kwargs:
        tag_obj: (Tag), else error)
        task_obj: (Task), else erorr
        """
        tag: Tag = kwagrs["tag_obj"]
        task: Task = kwagrs["task_obj"]
        if not isinstance(tag, Tag) or not isinstance(task, Task):
            raise TypeError("Wrong kwargs types")
        m2m = M2MTask2Tag(task_id=task.id, tag_id=tag.id)
        return m2m


class UniteManagerOfTaskTestModule:
    def __init__(self, session: AsyncSession) -> None:
        self.user_manager = MockDbUserManager(session)
        self.tag_manager = MockDbTagManager(session)
        self.task_manager = MockDbTaskManager(session)
        self.tag_to_task_manager = MockDbTag2TaskManager(session)
