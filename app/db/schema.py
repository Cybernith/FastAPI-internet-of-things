from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey, DateTime, Numeric

metadata = MetaData()

units = Table(
    "units", metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(100), nullable=False, unique=True),
    Column("symbol", String(16), nullable=False, unique=True),
)

sensors = Table(
    "sensors", metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(120), nullable=False),
    Column("unit_id", Integer, ForeignKey("units.id", ondelete="RESTRICT"), nullable=False, index=True),
    Column("location", String(200), nullable=True),
)

readings = Table(
    "readings", metadata,
    Column("id", Integer, primary_key=True),
    Column("sensor_id", Integer, ForeignKey("sensors.id", ondelete="CASCADE"), nullable=False, index=True),
    Column("value", Numeric(18, 6), nullable=False),
    Column("observed_at", DateTime(timezone=False), nullable=False),
)
