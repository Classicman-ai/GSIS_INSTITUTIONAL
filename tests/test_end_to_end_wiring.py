from datetime import datetime, timedelta, timezone

from volume_intelligence import CrossMarketAlignmentEngine, MarketTrade, VolumeAuthorityAdapter, VolumeProfileEngine
from volume_intelligence.cme_market_microstructure import CMEBookEvent, CMEBookLevel, CMETrade, CMEMarketMicrostructureEngine


def test_cme_to_authority_pipeline():
    now = datetime.now(timezone.utc)
    trades = [CMETrade(now - timedelta(seconds=120 - i), 5000.0 + (i % 4) * 0.1, 1.0 + (i % 5), "buy" if i % 3 else "sell", 1, "TEST") for i in range(120)]
    levels = [CMEBookLevel(now, 5000.0 + i * 0.1, 100.0 - i * 2, "bid", i, 1, "TEST") for i in range(10)]
    levels += [CMEBookLevel(now, 5001.0 + i * 0.1, 40.0 + i * 2, "ask", i, 1, "TEST") for i in range(10)]
    events = [CMEBookEvent(now, str(i), 5000.0 + (i % 5) * 0.1, 5.0, "buy", "add" if i % 2 == 0 else "execute", 1, "TEST") for i in range(60)]
    micro = CMEMarketMicrostructureEngine(20.0, 0.10, 0.10, 0.10, 0.50).analyze(levels, events, trades)
    profile = VolumeProfileEngine().build([MarketTrade(t.timestamp, t.price, t.quantity, t.aggressor_side) for t in trades], "CME_COMEX", "XAUUSD", "M5")
    aligner = CrossMarketAlignmentEngine(min_samples=30)
    for i in range(31):
        basis = aligner.observe(now + timedelta(seconds=i), 5000.0, 4999.0)
    alignment = aligner.align(profile, basis)
    authority = VolumeAuthorityAdapter(20.0).evaluate(profile, alignment, 4999.0)
    assert micro.data_quality in {"good", "limited"}
    assert profile.total_volume > 0
    assert alignment.aligned
    assert authority.combined_score >= 0
