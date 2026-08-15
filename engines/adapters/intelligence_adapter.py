"""
GSIS INTELLIGENCE ADAPTER
VERSION 1.3

Institutional Data Synchronization Layer
"""

from core.database import Database
from core.logger import Logger



class IntelligenceAdapter:


    def __init__(self):

        self.db = Database()

        self.logger = Logger(
            "INTELLIGENCE_ADAPTER"
        )



    def normalize(self,row):

        if not row:

            return None

        return dict(row)



    def get_market_state(self,symbol):


        return {

            "regime":
            self.get_regime(symbol),


            "structure":
            self.get_structure(symbol),


            "liquidity":
            self.get_liquidity(symbol),


            "confidence":
            self.get_confidence(symbol)

        }



    def get_regime(self,symbol):

        rows=self.db.fetch_all("""

        SELECT *

        FROM market_regime

        WHERE symbol=?

        ORDER BY timestamp DESC

        LIMIT 1

        """,(symbol,))


        return self.normalize(
            rows[0] if rows else None
        )




    def get_structure(self,symbol):


        rows=self.db.fetch_all("""

        SELECT *

        FROM market_structure_v2

        WHERE symbol=?

        AND timeframe IN
        ('H4','H1','M15','M5','M1')

        ORDER BY

        CASE timeframe

        WHEN 'H4' THEN 1

        WHEN 'H1' THEN 2

        WHEN 'M15' THEN 3

        WHEN 'M5' THEN 4

        WHEN 'M1' THEN 5

        END

        LIMIT 1


        """,(symbol,))


        return self.normalize(
            rows[0] if rows else None
        )





    def get_liquidity(self,symbol):


        rows=self.db.fetch_all("""

        SELECT *

        FROM liquidity_map

        WHERE symbol=?

        AND timeframe IN
        ('H4','H1','M15','M5','M1')

        ORDER BY

        CASE timeframe

        WHEN 'H4' THEN 1

        WHEN 'H1' THEN 2

        WHEN 'M15' THEN 3

        WHEN 'M5' THEN 4

        WHEN 'M1' THEN 5

        END

        LIMIT 1


        """,(symbol,))


        return self.normalize(
            rows[0] if rows else None
        )





    def get_confidence(self,symbol):


        rows=self.db.fetch_all("""

        SELECT *

        FROM confidence_model

        WHERE symbol=?

        ORDER BY timestamp DESC

        LIMIT 1


        """,(symbol,))


        return self.normalize(
            rows[0] if rows else None
        )
