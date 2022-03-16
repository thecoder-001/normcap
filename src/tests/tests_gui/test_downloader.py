import pytest

# Specific settings for pytest
# pylint: disable=redefined-outer-name,protected-access,unused-argument


@pytest.mark.skip_on_gh
@pytest.mark.parametrize("downloader", ["qt_network_downloader", "requests_downloader"])
def test_downloader_retrieves_website(qtbot, downloader, request):
    downloader = request.getfixturevalue(downloader)

    with qtbot.waitSignal(downloader.com.on_download_finished) as result:
        downloader.get("https://www.google.com")

    raw = result.args[0]
    assert isinstance(raw, str)
    assert "</html>" in raw.lower()


@pytest.mark.parametrize("downloader", ["qt_network_downloader", "requests_downloader"])
def test_downloader_handles_not_existing_url(caplog, qtbot, downloader, request):
    downloader = request.getfixturevalue(downloader)

    # Do not trigger download finished signal on error
    with qtbot.waitSignal(
        downloader.com.on_download_finished, raising=False, timeout=4000
    ) as result:
        downloader.get("https://not_existing_url.normcap")

    assert not result.args
    assert not result.signal_triggered
    assert "ERROR" in caplog.text

    # Do trigger download failed signal
    with qtbot.waitSignal(downloader.com.on_download_failed, timeout=4000) as result:
        downloader.get("https://not_existing_url.normcap")

    assert result.signal_triggered