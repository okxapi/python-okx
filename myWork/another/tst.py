import csv
import time

import requests


def get_data(user_name):
    url = "https://www.okx.com/priapi/v5/ecotrade/public/community/user/trade-records"
    import time

    # 获取当前时间戳（毫秒级）
    current_time = int(time.time() * 1000)

    # 计算2天前的时间戳（2天 = 2 * 24 * 60 * 60 * 1000毫秒）
    two_days_ago = current_time - 2 * 24 * 60 * 60 * 1000

    params = {
        "uniqueName": user_name,
        "startModify": str(two_days_ago),  # 开始时间：2天前
        "endModify": str(current_time),  # 结束时间：当前时间
        "limit": "120",
        "t": str(current_time)  # 请求时间戳：当前时间
    }

    headers = {
        "accept": "application/json",
        "accept-language": "zh-CN,zh;q=0.9",
        "app-type": "web",
        "authorization": "eyJraWQiOiIxMzYzODYiLCJhbGciOiJFUzI1NiJ9.eyJqdGkiOiJleDExMDE3NDY4MDgzODI4NDI4MDNCQUMzQjRBRkMyMUY4MU9xSFIiLCJ1aWQiOiI5QjA5NkFTck9JTU94Qk11TXVMR3R3PT0iLCJzdGEiOjAsIm1pZCI6IjQvRUVJdzY3T3dpQ1dTV3NRcjVSVkE9PSIsInBpZCI6IjQvRUVJdzY3T3dpQ1dTV3NRcjVSVkE9PSIsIm5kZSI6MSwiaWF0IjoxNzQ3OTMxMzIyLCJleHAiOjE3NDkxNDA5MjIsImJpZCI6MCwiZG9tIjoid3d3Lm9reC5jb20iLCJlaWQiOjE0LCJpc3MiOiJva2NvaW4iLCJkaWQiOiJNTmRuV0NtT2NDY0JqUVU5QU1HbmNIK3VtNEZHMWRTUzJMaUJBUUtDZ3hnTzlLWHpNVkYxemtycnk5TkFMR01vIiwibGlkIjoiOUIwOTZBU3JPSU1PeEJNdU11TEd0dz09IiwidWZiIjoiUFR5QThXMDl6RlVKQkdKNllSTkdZdz09IiwidXBiIjoiYitQU3dGSmtSZ1FTQjRRUTRxNVBVQT09Iiwia3ljIjozLCJreWkiOiJzVmtQSHhqTUdvYWFzajZndFcxUHgvdWtMOHJucWlSb2dwekV6TS9PNG9GTzhxa2IxYkx0YWYySVJVS2tMN3hFN3lkRi9ZTkNHUVcvNXlpNFZCelQzUT09IiwiY3BrIjoiaEJ2M21IRmNvSURMblNyRnp0R1NOWkxPb1pTazVtQThIcFBwT0w4UTVOVk1YU3dwSE1PUGtTYUxqKytXbzhiQWs4aGJtVE1tNEpiQyt0dHF1Y1EvNXhoNTJkQ1hwRkQ2S1laU0ZRcEdGVlU2RGNRT0NxcWpYOHZpOTN2aWZiSFhGQVZMZ0J3ckpISzVxcCtOTGZ0VkZoaDZKaXJPWC8rMHVpdHhmWCtKNllRPSIsInZlciI6MSwiY2x0IjoyLCJ1aWQiOiIrcFVPNlVUWVhEbEhLWUE0bXBnbUtLVXdtc0tDeGhFMERxNGFQeHMvZnA0PSIsInN1YiI6IkE0NUQzQUY5N0YzNzNFMjAzRDcyQzAyNTVENEMyRkU3In0.XUSCqZKqtVg4vnKZC1cXhagEOrzpo4ai6FrQXiY-YMUt_NY0mv8RgmwIWKpqjeiZzLn7PfzrEd7dZasNvTbuWA",
        "devid": "76a4bddf-148c-45e1-90fb-716d5532c8f8",
        "priority": "u=1, i",
        "sec-ch-ua": "\"Chromium\";v=\"136\", \"Google Chrome\";v=\"136\", \"Not.A/Brand\";v=\"99\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"macOS\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "x-cdn": "https://www.okx.com",
        "x-client-signature": "{P1363}flatz6A8QZGTWpPdN6WMAZcg3wUoiH5CXxm3HTAjDwRDohQrfqRhXO0vBE6jJREGH31wwZeslYD5t5j+NCSn6Q==",
        "x-client-signature-version": "1.3",
        "x-id-group": "2140179315570050004-c-26",
        "x-locale": "zh_CN",
        "x-request-timestamp": "1747931583535",
        "x-simulated-trading": "undefined",
        "x-site-info": "=0HNxojI5RXa05WZiwiIMFkQPx0Rfh1SPJiOiUGZvNmIsIyRTJiOi42bpdWZyJye",
        "x-utc": "8",
        "x-zkdex-env": "0",
        "cookie": "devId=76a4bddf-148c-45e1-90fb-716d5532c8f8; locale=zh_CN; fingerprint_id=76a4bddf-148c-45e1-90fb-716d5532c8f8; okg.currentMedia=xl; first_ref=https%3A%2F%2Fwww.okx.com%2Fzh-hans; finger_test_cookie=1746808367966; isLogin=1; ok_login_type=OKX_GLOBAL; ftID=undefined; x-lid=undefined; OptanonAlertBoxClosed=2025-05-09T16:33:04.076Z; ok_prefer_udTimeZone=2; preferLocale=zh_CN; _ym_uid=1746808394918974456; _ym_d=1746808394; amp_21c676=wYaaw6iBBo0NRkMt3wUbZ3...1iqrc4mj6.1iqrcb843.5.2.7; intercom-device-id-ny9cf50h=da80e8eb-fdf2-4890-9e35-2ae608937258; _tk=CZDst3yIKMRvI48tbFCkQA==; ok_prefer_udColor=0; ok-exp-time=1747931320902; ok_prefer_currency=0%7C1%7Cfalse%7CUSD%7C2%7C%24%7C1%7C1%7C%E7%BE%8E%E5%85%83; OptanonConsent=isGpcEnabled=0&datestamp=Fri+May+23+2025+00%3A28%3A42+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=202405.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&landingPath=NotLandingPage&groups=C0004%3A1%2CC0002%3A1%2CC0003%3A1%2CC0001%3A1&AwaitingReconsent=false&geolocation=US%3BTX; token=eyJraWQiOiIxMzYzODYiLCJhbGciOiJFUzI1NiJ9.eyJqdGkiOiJleDExMDE3NDY4MDgzODI4NDI4MDNCQUMzQjRBRkMyMUY4MU9xSFIiLCJ1aWQiOiI5QjA5NkFTck9JTU94Qk11TXVMR3R3PT0iLCJzdGEiOjAsIm1pZCI6IjQvRUVJdzY3T3dpQ1dTV3NRcjVSVkE9PSIsInBpZCI6IjQvRUVJdzY3T3dpQ1dTV3NRcjVSVkE9PSIsIm5kZSI6MSwiaWF0IjoxNzQ3OTMxMzIyLCJleHAiOjE3NDkxNDA5MjIsImJpZCI6MCwiZG9tIjoid3d3Lm9reC5jb20iLCJlaWQiOjE0LCJpc3MiOiJva2NvaW4iLCJkaWQiOiJNTmRuV0NtT2NDY0JqUVU5QU1HbmNIK3VtNEZHMWRTUzJMaUJBUUtDZ3hnTzlLWHpNVkYxemtycnk5TkFMR01vIiwibGlkIjoiOUIwOTZBU3JPSU1PeEJNdU11TEd0dz09IiwidWZiIjoiUFR5QThXMDl6RlVKQkdKNllSTkdZdz09IiwidXBiIjoiYitQU3dGSmtSZ1FTQjRRUTRxNVBVQT09Iiwia3ljIjozLCJreWkiOiJzVmtQSHhqTUdvYWFzajZndFcxUHgvdWtMOHJucWlSb2dwekV6TS9PNG9GTzhxa2IxYkx0YWYySVJVS2tMN3hFN3lkRi9ZTkNHUVcvNXlpNFZCelQzUT09IiwiY3BrIjoiaEJ2M21IRmNvSURMblNyRnp0R1NOWkxPb1pTazVtQThIcFBwT0w4UTVOVk1YU3dwSE1PUGtTYUxqKytXbzhiQWs4aGJtVE1tNEpiQyt0dHF1Y1EvNXhoNTJkQ1hwRkQ2S1laU0ZRcEdGVlU2RGNRT0NxcWpYOHZpOTN2aWZiSFhGQVZMZ0J3ckpISzVxcCtOTGZ0VkZoaDZKaXJPWC8rMHVpdHhmWCtKNllRPSIsInZlciI6MSwiY2x0IjoyLCJ1aWQiOiIrcFVPNlVUWVhEbEhLWUE0bXBnbUtLVXdtc0tDeGhFMERxNGFQeHMvZnA0PSIsInN1YiI6IkE0NUQzQUY5N0YzNzNFMjAzRDcyQzAyNTVENEMyRkU3In0.XUSCqZKqtVg4vnKZC1cXhagEOrzpo4ai6FrQXiY-YMUt_NY0mv8RgmwIWKpqjeiZzLn7PfzrEd7dZasNvTbuWA; _gid=GA1.2.1828670278.1747931325; tmx_session_id=hxslq7huu6i_1747931325142; fp_s=0; ok_site_info==0HNxojI5RXa05WZiwiIMFkQPx0Rfh1SPJiOiUGZvNmIsIyRTJiOi42bpdWZyJye; __cf_bm=4djqteaKqLJpdH8U86fNU55CAxS6bEPDtcRRXnvB2uk-1747931503-1.0.1.1-2DxOj6BfFO5OpXvCfrTAkf6T3ZPScvWaXi_tkHAUN1iPy6HhRGja9wI0EySy0pjAQ6ng6wISiIa9l1N6kRGwkhAJruVh_lOn3BhKWObVwpU; intercom-session-ny9cf50h=aWNvaWZpQ2o5RExjOVh2dXc0MFhKT3BtM1hGQ1MzN21PMFM4ZXNYOVpCVUNjcjlFSnA2Mkp1N3dkbXdXd0ExbHVoS1FDaEs3Wk1vaHMrdmtTY25SL1dFZGVYcU9MbEhTUGw5MXU0dmJFaU09LS1Pb093TG5lanMvR0paZnNqalFKZG9BPT0=--5e3d9268d5a0fe30bfe0dee64753e71b90358b92; _ym_isad=1; _ym_visorc=b; ok-ses-id=2JkdmgaTbuFDLexm+29nCfEjLlgWUfFQeLlR7WUJzx/VVHkHWm324kWpi0rM38PmEKa1Z/Xv2xBAJTofOQwhGSFUOqEdyQ8ijvRCasIZ8MyhKmrguzoJzuWArvqYvywD; _ga=GA1.1.710215270.1746808388; _ga_G0EKWWQGTZ=GS2.1.s1747931324$o7$g1$t1747931566$j60$l0$h0; _monitor_extras={\"deviceId\":\"JLtW9lQb0xBpyGDdtNc17-\",\"eventId\":346,\"sequenceNumber\":346}; traceId=2131179315734290005; ok_prefer_exp=1",
        "Referer": "https://www.okx.com/zh-hans/copy-trading/account/A433B32040FEC14F?tab=trade",
        "Referrer-Policy": "strict-origin-when-cross-origin"
    }

    response = requests.get(url, params=params, headers=headers)

    # 打印响应内容（根据需求处理）
    print(response.text)
    response_json = response.json()
    return response_json


def save_trade_records_to_csv(new_data, file_path="trade_records.csv"):
    """
    将新交易记录增量写入CSV文件，并根据ordId去重

    参数：
    new_data (list): 新交易记录列表（字典格式，需包含ordId字段）
    file_path (str): CSV文件路径（默认当前目录下的trade_records.csv）
    """
    # 1. 读取现有文件中的ordId（用于去重）
    existing_ord_ids = set()
    new_records = []

    # 尝试读取现有文件（若文件不存在则跳过）
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                existing_ord_ids.add(row["ordId"])
    except FileNotFoundError:
        pass  # 文件不存在时首次写入

    # 2. 过滤新数据中的重复记录（根据ordId）
    for record in new_data:
        ord_id = record.get("ordId")
        if ord_id and ord_id not in existing_ord_ids:
            new_records.append(record)
            existing_ord_ids.add(ord_id)  # 标记为已存在，避免后续重复

    # 3. 写入新数据到CSV文件（追加模式）
    if new_records:
        # 获取表头（若文件不存在则根据新数据生成）
        headers = new_records[0].keys() if new_records else []

        # 以追加模式打开文件（若文件不存在则创建）
        with open(file_path, "a", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=headers)

            # 若文件为空，则写入表头
            if not existing_ord_ids:
                writer.writeheader()

            # 写入去重后的新记录
            writer.writerows(new_records)

        print(f"成功写入 {len(new_records)} 条新记录到 {file_path}")
    else:
        print("无新记录需要写入（已全部去重）")


try:
    with open("user", "r") as f:
        params = [line.strip() for line in f if line.strip()]  # 去除空行
except FileNotFoundError:
    print("错误: user文件未找到!")
    exit(1)

# 遍历参数并定期处理
while True:
    for param in params:
        a = get_data(param)
        new_data = a.get("data", [])
        save_trade_records_to_csv(new_data)
    time.sleep(60)  # 处理完所有参数后等待60秒
