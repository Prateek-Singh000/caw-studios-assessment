from datetime import datetime, timezone
from sqlalchemy import String, Integer, DateTime, ForeignKey, Index
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class Link(Base):
    __tablename__ = "links"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String, unique=True, index=True)
    long_url: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    created_by: Mapped[str] = mapped_column(String, default="anonymous")
    
    clicks: Mapped[list["ClickEvent"]] = relationship(back_populates="link")

class ClickEvent(Base):
    __tablename__ = "click_events"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    link_id: Mapped[int] = mapped_column(ForeignKey("links.id"))
    clicked_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    user_agent: Mapped[str] = mapped_column(String, nullable=True)
    referrer: Mapped[str] = mapped_column(String, nullable=True)
    ip_hash: Mapped[str] = mapped_column(String, nullable=True)
    
    link: Mapped["Link"] = relationship(back_populates="clicks")

# Composite index for analytics (querying clicks by link over time)
Index("ix_click_events_link_id_clicked_at", ClickEvent.link_id, ClickEvent.clicked_at)
