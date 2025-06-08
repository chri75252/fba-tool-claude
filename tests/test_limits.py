import builtins
import io
import json
import os
import sys
from unittest.mock import AsyncMock, Mock
import pytest

import types

# Ensure repository root is on sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Provide dummy module for dependencies required by the workflow module
dummy_utils = types.ModuleType("utils.fba_calculator")
class DummyCalc:
    pass
dummy_utils.FBACalculator = DummyCalc
sys.modules["utils.fba_calculator"] = dummy_utils

import tools.passive_extraction_workflow_latest as wf

@pytest.mark.asyncio
async def test_run_workflow_main_passes_limits(monkeypatch):
    config_data = {"system": {"max_products_per_category": 3, "max_analyzed_products": 5}}
    config_json = json.dumps(config_data)

    orig_exists = os.path.exists
    def fake_exists(path):
        if path.endswith(os.path.join("config", "system_config.json")):
            return True
        return orig_exists(path)
    monkeypatch.setattr(os.path, "exists", fake_exists)

    orig_open = builtins.open
    def fake_open(path, *args, **kwargs):
        if path.endswith(os.path.join("config", "system_config.json")):
            return io.StringIO(config_json)
        return orig_open(path, *args, **kwargs)
    monkeypatch.setattr(builtins, "open", fake_open)

    mock_instance = Mock()
    mock_run = AsyncMock(return_value=[])
    mock_instance.run = mock_run
    monkeypatch.setattr(wf, "PassiveExtractionWorkflow", Mock(return_value=mock_instance))

    monkeypatch.setattr(sys, "argv", ["prog"])

    await wf.run_workflow_main()

    assert mock_run.call_count == 1
    kwargs = mock_run.call_args.kwargs
    assert kwargs["max_products_per_category"] == 3
    assert kwargs["max_analyzed_products"] == 5
