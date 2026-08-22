import sqlite3


DATABASE = "database/qmos.db"

# GSIS Institutional Volume Intelligence is advisory and bounded. Category A
# (price-independent) may inform confidence whenever valid volume data exists.
# Category B (price-dependent) is only enabled after CME-MT5 basis validation.
try:
    from volume_intelligence import VolumeAuthorityAdapter
except ImportError:  # Allows legacy environments to start before deployment.
    VolumeAuthorityAdapter = None


print("===================================")
print("QMOS ENGINE 7.7.1 - CONFIDENCE ENGINE")
print("CALIBRATED INTELLIGENCE MODEL")
print("VERSION 1.2 - VOLUME INTELLIGENCE")
print("===================================")


def create_table():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS confidence_model (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        symbol TEXT,
        timestamp INTEGER,
        regime_score REAL,
        structure_score REAL,
        alignment_score REAL,
        data_score REAL,
        volume_independent_score REAL DEFAULT 0,
        volume_price_dependent_score REAL DEFAULT 0,
        volume_authority_score REAL DEFAULT 0,
        volume_direction TEXT DEFAULT 'neutral',
        volume_price_dependent_enabled INTEGER DEFAULT 0,
        volume_data_quality TEXT DEFAULT 'unavailable',
        final_confidence REAL,
        confidence_state TEXT,
        UNIQUE(symbol,timestamp)
    )
    """)
    conn.commit()
    conn.close()


def state_to_score(state):
    if state is None:
        return 0
    state = state.upper()
    if "BULLISH_BREAK" in state or "STRONG_BULLISH" in state:
        return 1
    if "BEARISH_BREAK" in state or "STRONG_BEARISH" in state:
        return -1
    if "TRENDING_UP" in state:
        return 0.5
    if "TRENDING_DOWN" in state:
        return -0.5
    if "BULLISH" in state:
        return 0.5
    if "BEARISH" in state:
        return -0.5
    return 0


def confidence_label(value):
    if value >= 0.75:
        return "HIGH_CONFIDENCE"
    if value >= 0.45:
        return "MEDIUM_CONFIDENCE"
    return "LOW_CONFIDENCE"


def _volume_score_from_database(cursor, symbol, timestamp):
    """Read optional volume-authority fields when an upstream volume service is present.

    The confidence engine intentionally does not manufacture CME data. An upstream
    connector/adapter must persist validated volume intelligence before it can affect
    confidence. This preserves data integrity when CME connectivity is unavailable.
    """
    try:
        cursor.execute("""
            SELECT
                price_independent_score,
                price_dependent_score,
                combined_score,
                direction,
                price_dependent_enabled,
                data_quality
            FROM volume_authority
            WHERE symbol = ? AND timestamp = ?
            ORDER BY id DESC LIMIT 1
        """, (symbol, timestamp))
        row = cursor.fetchone()
    except sqlite3.OperationalError:
        return 0.0, 0.0, 0.0, "neutral", False, "unavailable"

    if not row:
        return 0.0, 0.0, 0.0, "neutral", False, "unavailable"

    independent, dependent, combined, direction, enabled, quality = row
    return (
        float(independent or 0.0),
        float(dependent or 0.0),
        float(combined or 0.0),
        direction or "neutral",
        bool(enabled),
        quality or "unknown",
    )


def run_engine():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        q.symbol,
        q.timestamp,
        q.macro_bias,
        q.trend_bias,
        q.execution_bias,
        m.regime,
        m.structure_state
    FROM qmos_state q
    JOIN market_intelligence m
      ON q.symbol = m.symbol
    """)
    rows = cursor.fetchall()
    processed = set()

    for row in rows:
        (
            symbol,
            timestamp,
            macro,
            trend,
            execution,
            regime,
            structure,
        ) = row

        key = (symbol, timestamp)
        if key in processed:
            continue
        processed.add(key)

        regime_score = abs(state_to_score(regime))
        structure_score = abs(state_to_score(structure))

        alignment_values = [
            state_to_score(macro),
            state_to_score(trend),
            state_to_score(execution),
        ]
        alignment_score = abs(sum(alignment_values) / len(alignment_values))

        # Do not claim external volume confidence when the volume feed is absent.
        base_data_score = 1.0
        (
            volume_independent,
            volume_dependent,
            volume_combined,
            volume_direction,
            volume_price_dependent_enabled,
            volume_quality,
        ) = _volume_score_from_database(cursor, symbol, timestamp)

        # Existing confidence model remains dominant. Volume Intelligence is an
        # additional, bounded evidence channel rather than an independent strategy.
        # Its maximum direct contribution is capped at 0.10 of total confidence.
        normalized_volume = min(max(volume_combined / 20.0, 0.0), 1.0)

        final_confidence = (
            regime_score * 0.36
            + structure_score * 0.27
            + alignment_score * 0.18
            + base_data_score * 0.09
            + normalized_volume * 0.10
        )

        label = confidence_label(final_confidence)

        cursor.execute("""
        INSERT OR REPLACE INTO confidence_model
        (
            symbol,
            timestamp,
            regime_score,
            structure_score,
            alignment_score,
            data_score,
            volume_independent_score,
            volume_price_dependent_score,
            volume_authority_score,
            volume_direction,
            volume_price_dependent_enabled,
            volume_data_quality,
            final_confidence,
            confidence_state
        )
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (
            symbol,
            timestamp,
            regime_score,
            structure_score,
            alignment_score,
            base_data_score,
            volume_independent,
            volume_dependent,
            volume_combined,
            volume_direction,
            int(volume_price_dependent_enabled),
            volume_quality,
            final_confidence,
            label,
        ))

        print("-----------------------------------")
        print(symbol)
        print("Regime Score:", round(regime_score, 2))
        print("Structure Score:", round(structure_score, 2))
        print("Alignment Score:", round(alignment_score, 2))
        print("Volume Independent:", round(volume_independent, 2))
        print("Volume Price-Dependent:", round(volume_dependent, 2))
        print("Volume Authority:", round(volume_combined, 2))
        print("Volume Direction:", volume_direction)
        print("Volume Price-Dependent Enabled:", volume_price_dependent_enabled)
        print("Final Confidence:", round(final_confidence, 2))
        print("State:", label)

    conn.commit()
    conn.close()


create_table()
run_engine()

print("-----------------------------------")
print("QMOS ENGINE 7.7.1 COMPLETE")
print("CONFIDENCE MODEL + VOLUME INTELLIGENCE COMPLETE")
print("-----------------------------------")
