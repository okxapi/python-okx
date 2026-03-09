"""
测试交易信号检测器
"""
import unittest
from examples.signal_detector import (
    SignalDetector,
    SignalScheduler,
    SignalType,
    Candlestick,
    SignalResult
)


def create_mock_candles(
    base_price: float = 100.0,
    count: int = 25,
    ma20_offset_pct: float = 0.0,
    prev_close_vs_current_pct: float = 0.0
) -> list:
    """
    创建模拟 K 线数据

    Args:
        base_price: 基础价格
        count: K 线数量
        ma20_offset_pct: 最新价格 (current_price) 相对 MA20 的偏移百分比
                        正值表示 current_price > MA20，负值表示 current_price < MA20
        prev_close_vs_current_pct: prev_close 相对 current_price 的偏移百分比
                                   正值表示 prev_close > current_price
                                   负值表示 prev_close < current_price
    """
    candles = []
    timestamp_base = 1709900000000

    # 确保至少有 22 根 K 线
    if count < 22:
        count = 22

    # 简化方法：
    # 1. 设 MA20 = 100 (目标值)
    # 2. current_price = 100 * (1 + ma20_offset_pct/100)
    # 3. prev_close = current_price * (1 + prev_close_vs_current_pct/100)
    # 4. 前 19 根价格设为 x，使得 (19*x + prev_close)/20 = 100

    target_ma20 = 100.0
    current_price = target_ma20 * (1 + ma20_offset_pct / 100)
    prev_close = current_price * (1 + prev_close_vs_current_pct / 100)

    # (19*x + prev_close) / 20 = target_ma20
    # 19*x = 20 * target_ma20 - prev_close
    # x = (20 * target_ma20 - prev_close) / 19
    base_for_ma20 = (20 * target_ma20 - prev_close) / 19

    # 先创建前 19 根 K 线
    prices = [base_for_ma20] * 19
    # 第 20 根是 prev_close (index 19)
    prices.append(prev_close)
    # 第 21 根是 current_price (index 20) - 最后一根
    prices.append(current_price)

    # 如果 count > 21，在 prev_close 之前插入额外的 K 线
    # 这样确保最后两根始终是 prev_close 和 current_price
    while len(prices) < count:
        prices.insert(19, base_for_ma20)  # 在 prev_close 之前插入

    for i in range(len(prices)):
        price = prices[i]
        candles.append(Candlestick(
            timestamp=timestamp_base + i * 900000,
            open=price * 0.999,
            high=price * 1.002,
            low=price * 0.998,
            close=price,
            volume=1000.0
        ))

    return candles


class TestSignalDetector(unittest.TestCase):
    """测试信号检测器"""

    def setUp(self):
        self.detector = SignalDetector()

    def test_calculate_ma20(self):
        """测试 MA20 计算"""
        candles = create_mock_candles(base_price=100.0, count=25, ma20_offset_pct=0.0)
        ma20 = self.detector.calculate_ma20(candles)
        self.assertIsNotNone(ma20)
        self.assertAlmostEqual(ma20, 100.0, delta=1.0)

    def test_calculate_ma20_insufficient_data(self):
        """测试数据不足时 MA20 返回 None"""
        # 直接创建不足 20 根的 K 线数据
        candles = [
            Candlestick(
                timestamp=1709900000000 + i * 900000,
                open=100.0,
                high=101.0,
                low=99.0,
                close=100.5,
                volume=1000.0
            )
            for i in range(15)
        ]
        ma20 = self.detector.calculate_ma20(candles)
        self.assertIsNone(ma20)

    def test_buy_signal(self):
        """测试买入信号"""
        # 创建价格高于 MA20 0.15% 的场景，且 prev_close < current_price
        # prev_close_vs_current_pct 为负表示 prev_close < current_price
        candles = create_mock_candles(
            base_price=100.0,
            count=25,
            ma20_offset_pct=0.15,  # current_price 高于 MA20 0.15%
            prev_close_vs_current_pct=-0.1  # prev_close 低于 current_price 0.1%
        )

        result = self.detector.check_signal(
            candles=candles,
            buy_range=(0.1, 0.2),
            sell_range=(-0.2, -0.1),
            inst_id='BTC-USDT',
            bar='15m'
        )

        self.assertEqual(result.signal, SignalType.BUY)
        self.assertEqual(result.inst_id, 'BTC-USDT')
        self.assertGreater(result.price_ma_ratio, 0.1)
        self.assertLess(result.price_ma_ratio, 0.2)

    def test_sell_signal(self):
        """测试卖出信号"""
        # 创建价格低于 MA20 0.15% 的场景，且 prev_close > current_price
        # prev_close_vs_current_pct 为正表示 prev_close > current_price
        candles = create_mock_candles(
            base_price=100.0,
            count=25,
            ma20_offset_pct=-0.15,  # current_price 低于 MA20 0.15%
            prev_close_vs_current_pct=0.1  # prev_close 高于 current_price 0.1%
        )

        result = self.detector.check_signal(
            candles=candles,
            buy_range=(0.1, 0.2),
            sell_range=(-0.2, -0.1),
            inst_id='BTC-USDT',
            bar='15m'
        )

        self.assertEqual(result.signal, SignalType.SELL)
        self.assertLess(result.price_ma_ratio, -0.1)
        self.assertGreater(result.price_ma_ratio, -0.2)

    def test_no_signal_outside_range(self):
        """测试无信号 - 价格超出区间"""
        candles = create_mock_candles(
            base_price=100.0,
            count=25,
            ma20_offset_pct=0.5,  # 高于 MA20 0.5%，超出买入区间
            prev_close_vs_current_pct=-0.1  # prev_close < current_price
        )

        result = self.detector.check_signal(
            candles=candles,
            buy_range=(0.1, 0.2),
            sell_range=(-0.2, -0.1),
            inst_id='BTC-USDT',
            bar='15m'
        )

        self.assertEqual(result.signal, SignalType.NONE)

    def test_no_signal_wrong_direction(self):
        """测试无信号 - 方向不对"""
        # 价格在买入区间，但是 prev_close > current_price（应该 prev_close < current_price 才触发买入）
        candles = create_mock_candles(
            base_price=100.0,
            count=25,
            ma20_offset_pct=0.15,  # current_price 高于 MA20 0.15%
            prev_close_vs_current_pct=0.1  # prev_close > current_price
        )

        result = self.detector.check_signal(
            candles=candles,
            buy_range=(0.1, 0.2),
            sell_range=(-0.2, -0.1),
            inst_id='BTC-USDT',
            bar='15m'
        )

        # 价格在买入区间但方向不对，不应触发买入信号
        self.assertEqual(result.signal, SignalType.NONE)

    def test_insufficient_data(self):
        """测试数据不足"""
        # 直接创建只有 1 根的 K 线数据
        candles = [
            Candlestick(
                timestamp=1709900000000,
                open=100.0,
                high=101.0,
                low=99.0,
                close=100.5,
                volume=1000.0
            )
        ]

        result = self.detector.check_signal(
            candles=candles,
            buy_range=(0.1, 0.2),
            sell_range=(-0.2, -0.1),
            inst_id='BTC-USDT',
            bar='15m'
        )

        self.assertEqual(result.signal, SignalType.NONE)
        self.assertIn("数据不足", result.reason)


class TestSignalScheduler(unittest.TestCase):
    """测试信号调度器"""

    def test_add_pair(self):
        """测试添加交易对"""
        scheduler = SignalScheduler()
        scheduler.add_pair('BTC-USDT', '15m', lambda: [])

        self.assertIn(('BTC-USDT', '15m'), scheduler.monitored_pairs)

    def test_remove_pair(self):
        """测试移除交易对"""
        scheduler = SignalScheduler()
        scheduler.add_pair('BTC-USDT', '15m', lambda: [])
        scheduler.remove_pair('BTC-USDT', '15m')

        self.assertNotIn(('BTC-USDT', '15m'), scheduler.monitored_pairs)

    def test_default_ranges(self):
        """测试默认参数"""
        scheduler = SignalScheduler()
        self.assertEqual(scheduler.buy_range, (0.1, 0.2))
        self.assertEqual(scheduler.sell_range, (-0.2, -0.1))

    def test_custom_ranges(self):
        """测试自定义参数"""
        scheduler = SignalScheduler(
            buy_range=(0.05, 0.15),
            sell_range=(-0.15, -0.05)
        )
        self.assertEqual(scheduler.buy_range, (0.05, 0.15))
        self.assertEqual(scheduler.sell_range, (-0.15, -0.05))


class TestCandlestickDataclass(unittest.TestCase):
    """测试 K 线数据类"""

    def test_datetime_conversion(self):
        """测试时间戳转换"""
        candle = Candlestick(
            timestamp=1709900000000,
            open=100.0,
            high=101.0,
            low=99.0,
            close=100.5,
            volume=1000.0
        )
        dt_str = candle.datetime
        self.assertIsInstance(dt_str, str)
        self.assertEqual(len(dt_str), 19)  # YYYY-MM-DD HH:MM:SS


class TestSignalResultDataclass(unittest.TestCase):
    """测试信号结果数据类"""

    def test_signal_result_creation(self):
        """测试信号结果创建"""
        result = SignalResult(
            signal=SignalType.BUY,
            inst_id='BTC-USDT',
            bar='15m',
            current_price=50000.0,
            ma20=49900.0,
            price_ma_ratio=0.2,
            prev_close=49950.0,
            timestamp='2024-03-08 12:00:00',
            reason='Test signal'
        )

        self.assertEqual(result.signal, SignalType.BUY)
        self.assertEqual(result.inst_id, 'BTC-USDT')
        self.assertEqual(result.current_price, 50000.0)


if __name__ == '__main__':
    unittest.main()
