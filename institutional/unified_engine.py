from __future__ import annotations

import importlib
import json
import math
import os
import sys
import time
import traceback
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean
from typing import Any, Optional

from intelligence.canonical_trade_signal import CanonicalTradeSignal
from intelligence.decision_governor_engine import DecisionGovernorEngine


@dataclass(frozen=True)
class GSISConfig:
    symbols: tuple[str, ...]
    timeframes: tuple[str, ...]
    loop_interval_seconds: float
    history_count: int
    risk_per_trade: float
    atr_multiplier: float
    reward_multiple: float
    minimum_signal_score: float
    execution_enabled: bool
    database_path: Path
    mt5_connector_path: Path
    allow_long: bool
    allow_short: bool
    max_open_trades: int
    max_pending_orders: int
    execution_mode: str
    order_type: str
    execution_timeout_seconds: float
    execution_retry_count: int
    cme_enabled: bool
    cme_start: Optional[str]
    cme_snapshot: bool
    cme_max_age_seconds: float
    basis_min_samples: int
    volume_max_score: float

    @classmethod
    def from_env(cls) -> "GSISConfig":
        def required(name: str) -> str:
            value = os.getenv(name, "").strip()
            if not value:
                raise RuntimeError(f"Missing required environment variable: {name}")
            return value
        def optional(name: str, default: str) -> str:
            return os.getenv(name, default).strip()
        def csv(name: str) -> tuple[str, ...]:
            values = tuple(x.strip().upper() for x in required(name).split(",") if x.strip())
            if not values:
                raise RuntimeError(f"{name} must contain at least one value")
            return values
        def positive_float(name: str, default: Optional[str] = None) -> float:
            value = float(required(name) if default is None else optional(name, default))
            if not math.isfinite(value) or value <= 0:
                raise RuntimeError(f"{name} must be a finite positive number")
            return value
        def positive_int(name: str, default: Optional[str] = None) -> int:
            value = int(required(name) if default is None else optional(name, default))
            if value <= 0:
                raise RuntimeError(f"{name} must be a positive integer")
            return value
        def nonnegative_int(name: str, default: str) -> int:
            value = int(optional(name, default))
            if value < 0:
                raise RuntimeError(f"{name} must be >= 0")
            return value
        def boolean(name: str, default: Optional[str] = None) -> bool:
            value = (required(name) if default is None else optional(name, default)).lower()
            if value not in {"true", "false"}:
                raise RuntimeError(f"{name} must be true or false")
            return value == "true"
        connector_path = Path(required("GSIS_MT5_CONNECTOR_PATH")).expanduser().resolve()
        if not connector_path.exists():
            raise RuntimeError(f"MT5 connector path does not exist: {connector_path}")
        risk = positive_float("GSIS_RISK_PER_TRADE")
        if risk > 1.0:
            raise RuntimeError("GSIS_RISK_PER_TRADE must be <= 1.0")
        return cls(
            symbols=csv("GSIS_SYMBOLS"), timeframes=csv("GSIS_TIMEFRAMES"),
            loop_interval_seconds=positive_float("GSIS_LOOP_INTERVAL_SECONDS"),
            history_count=positive_int("GSIS_HISTORY_COUNT"), risk_per_trade=risk,
            atr_multiplier=positive_float("GSIS_ATR_MULTIPLIER"),
            reward_multiple=positive_float("GSIS_REWARD_MULTIPLE"),
            minimum_signal_score=float(required("GSIS_MINIMUM_SIGNAL_SCORE")),
            execution_enabled=boolean("GSIS_EXECUTION_ENABLED", "false"),
            database_path=Path(required("GSIS_DATABASE_PATH")).expanduser().resolve(),
            mt5_connector_path=connector_path,
            allow_long=boolean("GSIS_ALLOW_LONG", "true"), allow_short=boolean("GSIS_ALLOW_SHORT", "true"),
            max_open_trades=positive_int("GSIS_MAX_OPEN_TRADES", "3"),
            max_pending_orders=nonnegative_int("GSIS_MAX_PENDING_ORDERS", "0"),
            execution_mode=optional("GSIS_EXECUTION_MODE", "MARKET"), order_type=optional("GSIS_ORDER_TYPE", "MARKET"),
            execution_timeout_seconds=positive_float("GSIS_EXECUTION_TIMEOUT_SECONDS", "10"),
            execution_retry_count=nonnegative_int("GSIS_EXECUTION_RETRY_COUNT", "1"),
            cme_enabled=boolean("GSIS_CME_ENABLED", "true"), cme_start=os.getenv("GSIS_CME_START", "").strip() or None,
            cme_snapshot=boolean("GSIS_CME_SNAPSHOT", "true"), cme_max_age_seconds=positive_float("GSIS_CME_MAX_AGE_SECONDS", "30"),
            basis_min_samples=positive_int("GSIS_BASIS_MIN_SAMPLES", "30"), volume_max_score=positive_float("GSIS_VOLUME_MAX_SCORE", "20"),
        )


class MT5UniversalConnectorAdapter:
    """The sole MT5 integration boundary. No market data is generated here."""
    def __init__(self, connector_path: Path) -> None:
        path = str(connector_path)
        if path not in sys.path: sys.path.insert(0, path)
        module = importlib.import_module("connector.mt5_connector")
        self.connector = module.MT5Connector()
    def connect(self) -> None:
        if not self.connector.connect(): raise RuntimeError(f"MT5 connection failed: {self.connector.last_error}")
    def tick(self, symbol: str) -> dict[str, Any]:
        value = self.connector.get_tick(symbol)
        if value is None: raise RuntimeError(f"Live tick unavailable for {symbol}: {self.connector.last_error}")
        return value
    def rates(self, symbol: str, timeframe: str, count: int) -> Any:
        value = self.connector.get_rates(symbol, timeframe, count)
        if value is None or len(value) == 0: raise RuntimeError(f"Live historical data unavailable for {symbol}/{timeframe}: {self.connector.last_error}")
        return value
    def account(self) -> dict[str, Any]:
        value = self.connector.get_account_info()
        if value is None: raise RuntimeError(f"Account data unavailable: {self.connector.last_error}")
        return value
    def symbol_info(self, symbol: str) -> dict[str, Any]:
        value = self.connector.get_symbol_info(symbol)
        if value is None: raise RuntimeError(f"Symbol metadata unavailable for {symbol}: {self.connector.last_error}")
        return value
    def status(self) -> dict[str, Any]: return self.connector.status()
    def open_positions(self) -> Optional[list[Any]]:
        for name in ("get_positions", "positions", "get_open_positions"):
            method = getattr(self.connector, name, None)
            if callable(method):
                value = method(); return [] if value is None else list(value)
        status = self.status()
        for key in ("positions", "open_positions"):
            if key in status and status[key] is not None: return list(status[key])
        return None
    def pending_orders(self) -> Optional[list[Any]]:
        for name in ("get_pending_orders", "pending_orders", "orders"):
            method = getattr(self.connector, name, None)
            if callable(method):
                value = method(); return [] if value is None else list(value)
        status = self.status()
        for key in ("pending_orders", "orders"):
            if key in status and status[key] is not None: return list(status[key])
        return None
    def execute_signal(self, signal: CanonicalTradeSignal) -> dict[str, Any]:
        """Execution accepts only the canonical signal."""
        if not signal.is_trade: raise RuntimeError("NON_TRADE_SIGNAL_CANNOT_EXECUTE")
        if signal.position_size is None or signal.entry is None or signal.stop_loss is None or not signal.take_profits:
            raise RuntimeError("CANONICAL_SIGNAL_TRADE_PLAN_INCOMPLETE")
        volume = float(signal.position_size); tp = float(signal.take_profits[0])
        if signal.decision == "BUY": return self.connector.buy(signal.symbol, volume, sl=float(signal.stop_loss), tp=tp)
        if signal.decision == "SELL": return self.connector.sell(signal.symbol, volume, sl=float(signal.stop_loss), tp=tp)
        raise RuntimeError("UNSUPPORTED_CANONICAL_DECISION")


class UnifiedOrderFlowEngine:
    name = "GSIS_MT5_ORDER_FLOW"
    def calculate(self, rates: Any) -> dict[str, Any]:
        rows=list(rates)
        if len(rows)<2: raise RuntimeError("Insufficient broker candle data for order-flow calculation")
        buy=sell=0.0; bullish=bearish=0; ranges=[]
        for row in rows:
            opening,closing=float(row["open"]),float(row["close"]); high,low=float(row["high"]),float(row["low"])
            names=getattr(getattr(row,"dtype",None),"names",None) or (); field="tick_volume" if "tick_volume" in names else "volume"; volume=float(row[field]); ranges.append(max(high-low,0.0))
            if closing>opening: buy+=volume; bullish+=1
            elif closing<opening: sell+=volume; bearish+=1
            else: buy+=volume/2; sell+=volume/2
        total=buy+sell
        if total<=0: raise RuntimeError("Broker supplied candles contain no usable volume")
        latest=rows[-1]; latest_range=max(float(latest["high"])-float(latest["low"]),0.0); body=abs(float(latest["close"])-float(latest["open"]))
        return {"buy_volume":buy,"sell_volume":sell,"delta":(buy-sell)/total,"bullish_candles":bullish,"bearish_candles":bearish,"average_range":mean(ranges),"body_strength":body/latest_range if latest_range else 0.0,"source":"MT5"}


class UnifiedMarketIntelligenceEngine:
    name="GSIS_MT5_MARKET_INTELLIGENCE"
    def analyze(self,rates:Any,order_flow:dict[str,Any])->dict[str,Any]:
        rows=list(rates); closes=[float(r["close"]) for r in rows]; highs=[float(r["high"]) for r in rows]; lows=[float(r["low"]) for r in rows]
        if len(closes)<2: raise RuntimeError("Insufficient broker candles for market intelligence")
        first,last=closes[0],closes[-1]; direction="BUY" if last>first else "SELL" if last<first else "WAIT"; movement=abs(last-first); atr=mean(max(h-l,0.0) for h,l in zip(highs,lows)); score=abs(order_flow["delta"])+(movement/atr if movement>atr and atr>0 else 0.0)
        return {"direction":direction,"first_close":first,"last_close":last,"movement":movement,"atr":atr,"score":score,"confidence":score,"pattern_match":score,"order_flow":order_flow,"source":"MT5"}


class UnifiedRiskEngine:
    name="GSIS_CANONICAL_RISK"
    def size(self,signal:CanonicalTradeSignal,account:dict[str,Any],symbol_info:dict[str,Any])->CanonicalTradeSignal:
        if not signal.is_trade:return signal
        if signal.entry is None or signal.stop_loss is None or signal.risk_fraction is None: raise RuntimeError("CANONICAL_RISK_INPUT_INCOMPLETE")
        equity=float(account.get("equity") or 0); tick_size=float(symbol_info.get("trade_tick_size") or 0); tick_value=float(symbol_info.get("trade_tick_value") or 0); vmin=float(symbol_info.get("volume_min") or 0); vmax=float(symbol_info.get("volume_max") or 0); step=float(symbol_info.get("volume_step") or 0); distance=abs(signal.entry-signal.stop_loss)
        if min(equity,tick_size,tick_value,vmin,vmax,step,distance)<=0: raise RuntimeError("BROKER_RISK_METADATA_INSUFFICIENT")
        raw=(equity*float(signal.risk_fraction))/((distance/tick_size)*tick_value); volume=min(math.floor(raw/step)*step,vmax)
        if volume<vmin: raise RuntimeError("CALCULATED_POSITION_BELOW_BROKER_MINIMUM")
        signal.position_size=volume; signal.risk_state="APPROVED"; signal.metadata["risk_engine"]=self.name; return signal


class UnifiedPersistence:
    def __init__(self,path:Path)->None:
        import sqlite3
        self.path=path; path.parent.mkdir(parents=True,exist_ok=True); self.connection=sqlite3.connect(path,check_same_thread=False)
        self.connection.execute("CREATE TABLE IF NOT EXISTS gsis_cycles (id INTEGER PRIMARY KEY AUTOINCREMENT,timestamp TEXT NOT NULL,symbol TEXT NOT NULL,status TEXT NOT NULL,payload TEXT NOT NULL)")
        self.connection.execute("CREATE TABLE IF NOT EXISTS gsis_execution_guard (signal_id TEXT PRIMARY KEY,timestamp TEXT NOT NULL,symbol TEXT NOT NULL,timeframe TEXT NOT NULL,side TEXT NOT NULL,result TEXT NOT NULL)"); self.connection.commit()
    def record(self,symbol:str,status:str,payload:dict[str,Any])->None:
        self.connection.execute("INSERT INTO gsis_cycles(timestamp,symbol,status,payload) VALUES(?,?,?,?)",(datetime.now(timezone.utc).isoformat(),symbol,status,json.dumps(payload,default=str))); self.connection.commit()
    def already_executed(self,signal_id:str)->bool:return self.connection.execute("SELECT 1 FROM gsis_execution_guard WHERE signal_id=?",(signal_id,)).fetchone() is not None
    def mark_executed(self,signal:CanonicalTradeSignal,result:dict[str,Any])->None:
        self.connection.execute("INSERT OR IGNORE INTO gsis_execution_guard(signal_id,timestamp,symbol,timeframe,side,result) VALUES(?,?,?,?,?,?)",(signal.signal_id,datetime.now(timezone.utc).isoformat(),signal.symbol,signal.timeframe,signal.decision,json.dumps(result,default=str))); self.connection.commit()


class GSISUnifiedEngine:
    name="GSIS_INSTITUTIONAL_UNIFIED_ENGINE"
    def __init__(self,config:GSISConfig)->None:
        self.config=config; self.market=MT5UniversalConnectorAdapter(config.mt5_connector_path); self.order_flow=UnifiedOrderFlowEngine(); self.intelligence=UnifiedMarketIntelligenceEngine(); self.governor=DecisionGovernorEngine(); self.risk=UnifiedRiskEngine(); self.persistence=UnifiedPersistence(config.database_path); self.cme_service=None; self.volume_profile=None; self.alignment=None; self.volume_authority=None; self.cme_thread=None; self.cme_error=None; self._setup_cme()
    def _setup_cme(self)->None:
        if not self.config.cme_enabled:return
        from adapters.cme import build_cme_intelligence_service
        from volume_intelligence import CrossMarketAlignmentEngine,VolumeAuthorityAdapter,VolumeProfileEngine
        self.cme_service=build_cme_intelligence_service(); self.volume_profile=VolumeProfileEngine(); self.alignment=CrossMarketAlignmentEngine(min_samples=self.config.basis_min_samples); self.volume_authority=VolumeAuthorityAdapter(max_score=self.config.volume_max_score)
    def _start_cme(self)->None:
        if not self.cme_service or self.cme_thread is not None:return
        import threading
        def runner():
            try:self.cme_service.run(start=self.config.cme_start,snapshot=self.config.cme_snapshot)
            except Exception as exc:self.cme_error=f"{type(exc).__name__}: {exc}"
        self.cme_thread=threading.Thread(target=runner,name="gsis-cme-feed",daemon=True); self.cme_thread.start()
    def _cme_snapshot(self,mt5_price:float,symbol:str,timeframe:str)->dict[str,Any]:
        if not all((self.cme_service,self.volume_profile,self.alignment,self.volume_authority)):return {"enabled":False,"status":"DISABLED"}
        trades=list(self.cme_service.trades); cme_signal=self.cme_service.latest_signal
        if not trades or cme_signal is None:return {"enabled":True,"status":"NO_CME_DATA"}
        latest=max(trades,key=lambda x:x.timestamp); age=(datetime.now(timezone.utc)-latest.timestamp).total_seconds()
        if age>self.config.cme_max_age_seconds:return {"enabled":True,"status":"STALE_CME_DATA","age_seconds":age,"microstructure":cme_signal.__dict__}
        from volume_intelligence import MarketTrade
        profile=self.volume_profile.build([MarketTrade(t.timestamp,t.price,t.quantity,t.aggressor_side) for t in trades],"CME_COMEX",symbol,timeframe); basis=self.alignment.observe(datetime.now(timezone.utc),latest.price,mt5_price); aligned=self.alignment.align(profile,basis); authority=self.volume_authority.evaluate(profile,aligned,mt5_price)
        return {"enabled":True,"status":"ALIGNED" if aligned.aligned else aligned.status,"age_seconds":age,"microstructure":cme_signal.__dict__,"profile":{"poc":profile.poc,"vah":profile.vah,"val":profile.val,"delta":profile.net_delta,"quality":profile.quality},"alignment":aligned.__dict__,"authority":authority.__dict__}
    def validate_runtime(self)->dict[str,Any]:
        self.market.connect(); account=self.market.account(); symbols={s:{"tick":self.market.tick(s),"symbol_info":self.market.symbol_info(s)} for s in self.config.symbols}
        if self.config.cme_enabled:self._start_cme()
        return {"engine":self.name,"connector":self.market.status(),"account":account,"symbols":symbols,"execution_enabled":self.config.execution_enabled,"cme_enabled":self.config.cme_enabled,"canonical_signal":"ACTIVE","decision_governor":"ACTIVE","status":"READY"}
    def _execution_guard(self,signal:CanonicalTradeSignal)->None:
        if signal.decision=="BUY" and not self.config.allow_long:raise RuntimeError("LONG_EXECUTION_DISABLED")
        if signal.decision=="SELL" and not self.config.allow_short:raise RuntimeError("SHORT_EXECUTION_DISABLED")
        positions=self.market.open_positions(); pending=self.market.pending_orders()
        if positions is None:raise RuntimeError("POSITION_STATE_UNAVAILABLE_FAIL_CLOSED")
        if len(positions)>=self.config.max_open_trades:raise RuntimeError("MAX_OPEN_TRADES_REACHED")
        if pending is None:raise RuntimeError("PENDING_ORDER_STATE_UNAVAILABLE_FAIL_CLOSED")
        if self.config.max_pending_orders>0 and len(pending)>=self.config.max_pending_orders:raise RuntimeError("MAX_PENDING_ORDERS_REACHED")
    def cycle(self)->dict[str,Any]:
        self.market.connect(); account=self.market.account(); results={}
        for symbol in self.config.symbols:
            tick=self.market.tick(symbol); info=self.market.symbol_info(symbol); mt5_price=float(tick.get("mid") or ((float(tick["bid"])+float(tick["ask"]))/2)); frames={}
            for timeframe in self.config.timeframes:
                rates=self.market.rates(symbol,timeframe,self.config.history_count); flow=self.order_flow.calculate(rates); intelligence=self.intelligence.analyze(rates,flow); cme=self._cme_snapshot(mt5_price,symbol,timeframe)
                authority=cme.get("authority") or {}; micro=cme.get("microstructure") or {}; fused=float(intelligence["score"])
                if authority.get("direction") in {"bullish","bearish"}: fused+=float(authority.get("combined_score",0))/20
                if micro.get("direction") not in (None,"neutral"):
                    same=(intelligence["direction"]=="BUY" and micro["direction"]=="bullish") or (intelligence["direction"]=="SELL" and micro["direction"]=="bearish"); fused+=abs(float(micro.get("score",0)))/20 if same else -abs(float(micro.get("score",0)))/20
                intelligence["confidence"]=fused; intelligence["pattern_match"]=fused; intelligence["governor_thresholds"]={"confidence":self.config.minimum_signal_score,"pattern":self.config.minimum_signal_score,"approval":1.0,"confidence_weight":0.5,"pattern_weight":0.5,"risk_weight":0.0}
                direction=intelligence["direction"]; signal_id=f"{symbol}:{timeframe}:{self._last_bar_id(rates)}"; atr=float(intelligence["atr"]); entry=float(tick["ask"] if direction=="BUY" else tick["bid"]); stop_distance=self.config.atr_multiplier*atr; target_distance=self.config.reward_multiple*stop_distance
                trade_plan={"signal_id":signal_id,"symbol":symbol,"timeframe":timeframe,"entry":entry if direction in {"BUY","SELL"} and atr>0 else None,"stop_loss":(entry-stop_distance if direction=="BUY" else entry+stop_distance) if direction in {"BUY","SELL"} and atr>0 else None,"take_profits":[entry+target_distance if direction=="BUY" else entry-target_distance] if direction in {"BUY","SELL"} and atr>0 else [],"risk_fraction":self.config.risk_per_trade}
                signal=self.governor.evaluate(intelligence,{"approved":atr>0,"state":"PRE_RISK_APPROVED" if atr>0 else "BLOCKED"},{"symbol":symbol,"timeframe":timeframe},trade_plan)
                if signal.is_trade:
                    if self.persistence.already_executed(signal.signal_id): signal.decision="WAIT"; signal.execution_status="BLOCKED"; signal.invalidation="DUPLICATE_SIGNAL_BLOCKED"
                    else:
                        signal=self.risk.size(signal,account,info)
                        if self.config.execution_enabled:
                            try:
                                self._execution_guard(signal); result=self.market.execute_signal(signal)
                                if isinstance(result,dict) and result.get("success") is False:raise RuntimeError(f"BROKER_REJECTED_ORDER: {result}")
                                signal.execution_status="EXECUTED"; self.persistence.mark_executed(signal,result)
                            except Exception as exc:
                                signal.execution_status="BLOCKED"; signal.invalidation=f"EXECUTION_BLOCKED: {type(exc).__name__}: {exc}"
                snapshot={"timestamp":datetime.now(timezone.utc).isoformat(),"canonical_signal":signal.to_dict(),"flow":flow,"intelligence":intelligence,"cme":cme}; self.persistence.record(symbol,"COMPLETE",snapshot); frames[timeframe]=snapshot
            results[symbol]=frames
        return {"engine":self.name,"timestamp":datetime.now(timezone.utc).isoformat(),"status":"CYCLE_COMPLETE","results":results}
    @staticmethod
    def _last_bar_id(rates:Any)->str:
        row=list(rates)[-1]
        for key in ("time","timestamp","datetime"):
            try:return str(row[key])
            except Exception:pass
        return str(row)
    def run_forever(self)->None:
        self.validate_runtime()
        while True:
            started=time.monotonic()
            try:print(json.dumps(self.cycle(),default=str))
            except Exception as exc:self.persistence.record("SYSTEM","ERROR",{"timestamp":datetime.now(timezone.utc).isoformat(),"error":f"{type(exc).__name__}: {exc}","traceback":traceback.format_exc(),"cme_error":self.cme_error})
            time.sleep(max(self.config.loop_interval_seconds-(time.monotonic()-started),0.0))
