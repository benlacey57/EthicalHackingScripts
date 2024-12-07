import os
from scripts.log_manager import log_action

def test_log_action(tmp_path):
    challenge_path = tmp_path / "TestChallenge"
    challenge_path.mkdir()

    log_action(challenge_path, "Test log entry")
    
    log_file = challenge_path / "challenge.log"
    assert log_file.exists()
    with open(log_file, "r") as f:
        content = f.read()
    assert "Test log entry" in content
