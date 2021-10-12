import traceback

from ..utils.log import logger
from ..utils.config import MAX_RETRYTIME
from ..utils.recognize import Scene, RecognizeError
from ..utils.solver import BaseSolver, StrategyError


class MissionSolver(BaseSolver):
    """
    点击确认完成每日任务和每周任务
    """

    def __init__(self, adb=None, recog=None):
        super(MissionSolver, self).__init__(adb, recog)

    def run(self):
        logger.info('Start: 任务')

        checked = 0

        retry_times = MAX_RETRYTIME
        while retry_times > 0:
            try:
                if self.scene() == Scene.INDEX:
                    self.tap_element('index_mission')
                elif self.scene() == Scene.MISSION_DAILY:
                    checked |= 1
                    collect = self.recog.find('mission_collect')
                    if collect is None:
                        self.sleep(1)
                        collect = self.recog.find('mission_collect')
                    if collect is not None:
                        logger.info('任务：一键收取任务')
                        self.tap(collect)
                    elif checked & 2 == 0:
                        self.tap_element('mission_weekly')
                    else:
                        break
                elif self.scene() == Scene.MISSION_WEEKLY:
                    checked |= 2
                    collect = self.recog.find('mission_collect')
                    if collect is None:
                        self.sleep(1)
                        collect = self.recog.find('mission_collect')
                    if collect is not None:
                        logger.info('任务：一键收取任务')
                        self.tap(collect)
                    elif checked & 1 == 0:
                        self.tap_element('mission_daily')
                    else:
                        break
                elif self.scene() == Scene.MATERIEL:
                    self.tap_element('materiel')
                elif self.scene() == Scene.LOADING:
                    self.sleep(3)
                elif self.get_navigation():
                    self.tap_element('nav_mission')
                elif self.scene() != Scene.UNKNOWN:
                    self.back_to_index()
                else:
                    raise RecognizeError
            except RecognizeError:
                logger.warn('识别出了点小差错 qwq')
                retry_times -= 1
                self.sleep(3)
                continue
            except StrategyError as e:
                logger.error(e)
                logger.debug(traceback.format_exc())
                return
            except Exception as e:
                raise e
            retry_times = MAX_RETRYTIME
