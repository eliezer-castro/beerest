import pytest
from beerest.core.expect import ExpectError

def pytest_configure(config):
    config.option.tbstyle = "short"

def pytest_exception_interact(node, call, report):
    if call.excinfo.type is ExpectError:
        error_message = str(call.excinfo.value)
        test_name = node.name
        test_file = node.path.name
        
        if "Test Information:" not in error_message:
            header = (
                f"\n📋 Test Location:\n"
                f"   • File: {test_file}\n"
                f"   • Test: {test_name}\n"
                f"   • Line: {call.excinfo.traceback[-1].lineno}\n\n"
            )
            
            error_start = error_message.find("🔴 TEST ASSERTION FAILED")
            if error_start != -1:
                error_message = (
                    error_message[:error_start] + 
                    "🔴 TEST ASSERTION FAILED\n" +
                    "━" * 100 + "\n" +
                    header +
                    error_message[error_start + len("🔴 TEST ASSERTION FAILED\n") + 101:]
                )
        
        report.longrepr = error_message