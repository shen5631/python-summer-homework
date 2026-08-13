import pytest

from japan_trip_recommender import get_recommendations, get_region_summary, get_activity_recommendation


def test_hokkaido_region_recommendation():
    result = get_recommendations("홋카이도")
    assert "홋카이도" in result
    assert "니세코" in result or "후라노" in result
    assert "스키" in result or "눈" in result


def test_kyushu_region_summary_has_places():
    summary = get_region_summary()
    assert "홋카이도" in summary
    assert "규슈" in summary
    assert "후쿠오카" in summary or "벳푸" in summary


def test_activity_recommendation_for_onsen():
    result = get_activity_recommendation("온천/휴식")
    assert "벳푸" in result or "하코네" in result or "기노사키" in result
    assert "온천" in result or "휴식" in result
