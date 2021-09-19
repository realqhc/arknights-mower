import numpy as np
from .log import logger


def confirm(im):
    """
    检测是否出现确认界面
    """
    x, y, z = im.shape
    l, r = y // 4 * 3 - 10, y // 4 * 3 + 10
    u, d = x // 2 - 10, x // 2 + 10

    for i in range(u, d):
        for j in range(l, r):
            if np.ptp(im[i, j]) != 0:
                return None
    val = np.sum(im[u:d, l:r]) / 400 / 3
    if abs(val - 53) > 3:
        return None

    u = 0
    for i in range(d, x):
        for j in range(l, r):
            if np.ptp(im[i, j]) != 0 or abs(im[i, j, 0] - 13) > 3:
                break
            elif j == r-1:
                u = i
        if u:
            break
    if u == 0:
        return None

    d = 0
    for i in range(u, x):
        for j in range(l, r):
            if np.ptp(im[i, j]) != 0 or abs(im[i, j, 0] - 13) > 3:
                d = i
                break
        if d:
            break

    ret = (y // 2, (u + d) // 2)
    logger.debug(f'detector.confirm: {ret}')
    return ret


def infra_notification(im):
    """
    检测基建内是否存在蓝色通知
    前置条件：已经处于基建内
    """
    x, y, z = im.shape

    r = y
    while np.max(im[:, r-1]) < 100:
        r -= 1
    r -= 1

    u = 0
    for i in range(x):
        if im[i, r, 0] < 100 < im[i, r, 1] < im[i, r, 2]:
            u = i
            break
    if u == 0:
        return None

    d = 0
    for i in range(u, x):
        if not (im[i, r, 0] < 100 < im[i, r, 1] < im[i, r, 2]):
            d = i
            break
    if d == 0:
        return None

    ret = (r - 10, (u + d) // 2)
    logger.debug(f'detector.infra_notification: {ret}')
    return ret
