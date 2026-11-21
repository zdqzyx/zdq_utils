import traceback
from loguru import logger
import pandas as pd
import time
import tushare as tus


def tushare_query(execute_fuc, **kwargs):
    '''
    kwargs中： ts_limit_cnt：分页大小， ts_max_calls:每分钟最大调用次数， ts_sleep：如果失败sleep大小
    '''
    pro = tus.pro_api()
    df = pd.DataFrame()
    # 根据ts_max_calls计算每调用一次sleep多少秒
    CALL_INTERVAL = round(60/kwargs.get('ts_max_calls', 500), 2) + 0.02
    for i in range(5):
        try:
            all_data = []
            offset = 0
            limit = kwargs.get('ts_limit_cnt', 4000)
            while True:
                # 分页获取
                df = pro.query(execute_fuc, offset=offset, limit=limit, **kwargs)
                if df is None or df.empty:
                    break
                all_data.append(df)
                # 不满一页说明结束
                if len(df) < limit:
                    break
                offset += limit
                time.sleep(CALL_INTERVAL)
            if len(all_data)>0:
                df = pd.concat(all_data, ignore_index=True)
        except Exception as e:
            logger.warning(traceback.format_exc())
            logger.warning("tushare timeout!!! execute_fuc={},{}".format(execute_fuc, kwargs))
            time.sleep(kwargs.get('ts_sleep', 10))
        else:
            return df
    return df
