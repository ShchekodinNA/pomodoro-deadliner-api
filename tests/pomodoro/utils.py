from tests.utils import IMockDbManager, get_uuid4_as_str
from src.database import Base
from src.pomodoro.models import PomodoroSetting
# from src.auth.models import User
# class MockDBPomodoroSettingManager(IMockDbManager):
#     async def _get_unique_object(self, **kwagrs) -> Base:
#         """kwargs:
#         user_obj (User): instance_to_create_pomodoro_Setting
#         """
#         user = 