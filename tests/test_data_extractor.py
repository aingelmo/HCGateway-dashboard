"""Test data extraction from HCGateway API."""

import os
from datetime import UTC, datetime, timedelta
from unittest.mock import MagicMock, patch

import pytest

import data_extractor

def mock_token_response(token="access123", refresh="refresh123", expiry=None):
    if expiry is None:
        expiry = (datetime.now(UTC) + timedelta(hours=1)).isoformat()
    return {"token": token, "refresh": refresh, "expiry": expiry}


def mock_fetch_response():
    return [{"id": "1", "value": "foo"}, {"id": "2", "value": "bar"}]


def test_fetch_data_env():
    hcg_username = os.getenv("HCGATEWAY_USERNAME")
    hcg_password = os.getenv("HCGATEWAY_PASSWORD")
    if not hcg_username or not hcg_password:
        pytest.skip("Environment variables for credentials not set.")
    method = "steps"
    queries = {}
    result = data_extractor.fetch_data(method, queries, hcg_username, hcg_password)
    assert isinstance(result, list), f"Result is not a list: {type(result)}"
    for item in result:
        assert isinstance(item, dict), f"List item is not a dict: {type(item)}"
        assert "token" not in item, "Result item should not expose tokens."


@patch("data_extractor.requests.post")
def test_get_access_token_success(mock_post):
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = mock_token_response()
    mock_post.return_value = mock_resp
    result = data_extractor.get_access_token("user", "pass")
    assert result["token"] == "access123"
    assert result["refresh"] == "refresh123"
    assert "expiry" in result


@patch("data_extractor.requests.post")
def test_refresh_access_token_success(mock_post):
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = mock_token_response(
        token="newtoken", refresh="newrefresh"
    )
    mock_post.return_value = mock_resp
    result = data_extractor.refresh_access_token("refresh123")
    assert result["token"] == "newtoken"
    assert result["refresh"] == "newrefresh"


@patch("data_extractor.get_access_token")
@patch("data_extractor.refresh_access_token")
def test_ensure_valid_token_refresh(mock_refresh, _):
    data_extractor.token_data["access_token"] = "expired"
    data_extractor.token_data["refresh_token"] = "refresh123"
    data_extractor.token_data["expiry"] = (
        datetime.now(UTC) - timedelta(seconds=10)
    ).isoformat()
    mock_refresh.return_value = mock_token_response(
        token="newtoken", refresh="refresh123"
    )
    data_extractor.ensure_valid_token("user", "pass")
    assert data_extractor.token_data["access_token"] == "newtoken"
    assert data_extractor.token_data["refresh_token"] == "refresh123"


@patch("data_extractor.get_access_token")
def test_ensure_valid_token_no_refresh(mock_get):
    data_extractor.token_data["access_token"] = None
    data_extractor.token_data["refresh_token"] = None
    data_extractor.token_data["expiry"] = None
    mock_get.return_value = mock_token_response(token="tok", refresh="ref")
    data_extractor.ensure_valid_token("user", "pass")
    assert data_extractor.token_data["access_token"] == "tok"
    assert data_extractor.token_data["refresh_token"] == "ref"


@patch("data_extractor.requests.post")
def test_fetch_data_success(mock_post):
    with patch("data_extractor.ensure_valid_token"):
        data_extractor.token_data["access_token"] = "access123"
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = mock_fetch_response()
        mock_post.return_value = mock_resp
        result = data_extractor.fetch_data("test", {"foo": "bar"}, "user", "pass")
        assert isinstance(result, list)
        for item in result:
            assert isinstance(item, dict)


@patch("data_extractor.token_data", {"expiry": None})
def test_is_token_expired_true():
    assert data_extractor.is_token_expired() is True


@patch(
    "data_extractor.token_data",
    {"expiry": (datetime.now(UTC) + timedelta(seconds=600)).isoformat()},
)
def test_is_token_expired_false():
    assert data_extractor.is_token_expired() is False


@patch(
    "data_extractor.token_data",
    {"expiry": (datetime.now(UTC) + timedelta(seconds=100)).isoformat()},
)
def test_is_token_expired_margin():
    assert data_extractor.is_token_expired() is True
