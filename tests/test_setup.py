import os
import json
import pytest
from scripts.setup import create_challenge
from scripts.utils import load_config

@pytest.fixture
def base_dir(tmp_path):
    # Setup a temporary base directory for tests
    config = {"base_directory": str(tmp_path)}
    with open("config/base.json", "w") as f:
        json.dump(config, f)
    return tmp_path

def test_create_challenge(base_dir, monkeypatch):
    # Mock user inputs
    monkeypatch.setattr("builtins.input", lambda x: "TestChallenge" if "name" in x else "127.0.0.1")
    
    create_challenge()

    challenge_path = os.path.join(base_dir, "Testchallenge")
    assert os.path.exists(challenge_path)

    # Verify metadata
    metadata_file = os.path.join(challenge_path, "metadata.json")
    assert os.path.exists(metadata_file)
    with open(metadata_file, "r") as f:
        metadata = json.load(f)
    assert metadata["name"] == "Testchallenge"
    assert metadata["ip"] == "127.0.0.1"

