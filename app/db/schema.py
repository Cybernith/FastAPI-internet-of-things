from sqlalchemy import (
    MetaData, Table, Column, Integer, String, ForeignKey, DateTime, Numeric, Index
)

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
    Column("unit_id", Integer, ForeignKey("units.id"), nullable=False),
    Column("location", String(200), nullable=True),
)

readings = Table(
    "readings", metadata,
    Column("id", Integer, primary_key=True),
    Column("sensor_id", Integer, ForeignKey("sensors.id", ondelete="CASCADE"), nullable=False, index=True),
    Column("value", Numeric(18, 6), nullable=False),
    Column("observed_at", DateTime(timezone=False), nullable=False),
)

Index("ix_readings_sensor_observed_id_desc",readings.c.sensor_id, readings.c.observed_at.desc(), readings.c.id.desc())
