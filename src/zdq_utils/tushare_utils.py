import traceback
from loguru import logger
import pandas as pd
import time
import tushare as tus


def tushare_query(execute_fuc: str, **kwargs) -> pd.DataFrame:
    """Query Tushare Pro API with automatic pagination, rate limiting, and retries.

    Args:
        execute_fuc: Tushare Pro interface name (e.g. ``"stock_basic"``, ``"daily"``).
        **kwargs: Query parameters forwarded to ``pro.query(...)``, plus optional
            control parameters:
            - ``ts_limit_cnt`` (int): Page size per request. Defaults to ``4000``.
            - ``ts_max_calls`` (int): Max API calls per minute for rate limiting.
              Defaults to ``500``.
            - ``ts_sleep`` (int | float): Wait seconds before retrying on error.
              Defaults to ``10``.

    Returns:
        pd.DataFrame: Concatenated query results across all pages, or an empty
        DataFrame if no data is returned or all 5 retry attempts fail.
    """
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
