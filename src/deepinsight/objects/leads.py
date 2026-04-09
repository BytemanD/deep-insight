"""Lead Pydantic Models"""

from datetime import datetime
from typing import Any

from pydantic import BaseModel

from deepinsight.models._base import BaseObject


class Lead(BaseObject):
    """线索模型"""

    uuid: str
    name: str
    summary: str | None = None
    description: str | None = None
    type: str | None = None
    match_reason: str | None = None
    keywords: str | None = None
    source: str | None = None
    raw_file: str | None = None
    tags: dict[str, Any] | None = None
    region: str | None = None
    country: str | None = None
    stage: str | None = None
    estimated_value_mw: float | None = None
    estimated_value_mwh: float | None = None
    estimated_value_usd: float | None = None
    technology: str | None = None
    timing_window: str | None = None
    published_at: str | None = None
    developers: dict[str, Any] | None = None
    competitors: dict[str, Any] | None = None
    decision_makers: dict[str, Any] | None = None
    related_entities: dict[str, Any] | None = None
    priority: str | None = None
    overall_score: float = 0.0
    score_breakdown: dict[str, Any] | None = None
    pattern_id: str | None = None
    pattern_name: str | None = None
    pattern_group: str | None = None
    evidence_summary: dict[str, Any] | None = None
    source_signals: dict[str, Any] | None = None
    total_evidence_count: int | None = None
    source_urls: dict[str, Any] | None = None
    source_files: dict[str, Any] | None = None
    source_domains: dict[str, Any] | None = None
    recommended_action: str | None = None
    next_steps: dict[str, Any] | None = None
    status: str = "new"
    hypothesis_stage: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class LeadCreate(BaseObject):
    """创建线索请求"""

    name: str
    summary: str | None = None
    description: str | None = None
    type: str | None = None
    match_reason: str | None = None
    keywords: str | None = None
    source: str | None = None
    raw_file: str | None = None
    tags: dict[str, Any] | None = None
    region: str | None = None
    country: str | None = None
    stage: str | None = None
    estimated_value_mw: float | None = None
    estimated_value_mwh: float | None = None
    estimated_value_usd: float | None = None
    technology: str | None = None
    timing_window: str | None = None
    published_at: str | None = None
    developers: dict[str, Any] | None = None
    competitors: dict[str, Any] | None = None
    decision_makers: dict[str, Any] | None = None
    related_entities: dict[str, Any] | None = None
    priority: str | None = None
    overall_score: float = 0.0
    score_breakdown: dict[str, Any] | None = None
    pattern_id: str | None = None
    pattern_name: str | None = None
    pattern_group: str | None = None
    evidence_summary: dict[str, Any] | None = None
    source_signals: dict[str, Any] | None = None
    total_evidence_count: int | None = None
    source_urls: dict[str, Any] | None = None
    source_files: dict[str, Any] | None = None
    source_domains: dict[str, Any] | None = None
    recommended_action: str | None = None
    next_steps: dict[str, Any] | None = None
    status: str = "new"
    hypothesis_stage: str | None = None


class LeadUpdate(BaseModel):
    """更新线索请求"""

    name: str | None = None
    summary: str | None = None
    description: str | None = None
    type: str | None = None
    match_reason: str | None = None
    keywords: str | None = None
    source: str | None = None
    raw_file: str | None = None
    tags: dict[str, Any] | None = None
    region: str | None = None
    country: str | None = None
    stage: str | None = None
    estimated_value_mw: float | None = None
    estimated_value_mwh: float | None = None
    estimated_value_usd: float | None = None
    technology: str | None = None
    timing_window: str | None = None
    published_at: str | None = None
    developers: dict[str, Any] | None = None
    competitors: dict[str, Any] | None = None
    decision_makers: dict[str, Any] | None = None
    related_entities: dict[str, Any] | None = None
    priority: str | None = None
    overall_score: float | None = None
    score_breakdown: dict[str, Any] | None = None
    pattern_id: str | None = None
    pattern_name: str | None = None
    pattern_group: str | None = None
    evidence_summary: dict[str, Any] | None = None
    source_signals: dict[str, Any] | None = None
    total_evidence_count: int | None = None
    source_urls: dict[str, Any] | None = None
    source_files: dict[str, Any] | None = None
    source_domains: dict[str, Any] | None = None
    recommended_action: str | None = None
    next_steps: dict[str, Any] | None = None
    status: str | None = None
    hypothesis_stage: str | None = None


class LeadListResponse(BaseModel):
    """线索列表响应"""

    leads: list[Lead]
    total: int
