"""Each hook function logs what it received."""

from refgenie.plugins import Change, HookEvent

from refgenie_myplugin import my_post_build_func, my_post_update_func, my_pre_pull_func


class StubSettings:
    def __init__(self, values):
        self._values = values

    def settings(self, plugin):
        return dict(self._values.get(plugin, {}))


class StubRefgenie:
    """Just the part of `Refgenie` a plugin reads settings from."""

    def __init__(self, values=None):
        self.plugins = StubSettings(values or {})


def test_post_update_logs_each_change_with_the_greeting(caplog):
    event = HookEvent(
        "post_update",
        changes=(Change(action="asset_added", genome="g", asset_group="fasta", asset="default"),),
    )
    with caplog.at_level("INFO", logger="refgenie"):
        my_post_update_func(StubRefgenie({"myplugin": {"greeting": "hi"}}), event)
    assert "hi from refgenie_myplugin: asset_added g/fasta:default" in caplog.text


def test_post_update_default_greeting(caplog):
    event = HookEvent("post_update", changes=(Change(action="genome_removed", genome="g"),))
    with caplog.at_level("INFO", logger="refgenie"):
        my_post_update_func(StubRefgenie(), event)
    assert "hello from refgenie_myplugin: genome_removed" in caplog.text


def test_pre_pull_logs_the_target(caplog):
    with caplog.at_level("INFO", logger="refgenie"):
        my_pre_pull_func(object(), HookEvent("pre_pull", genome="hg38", asset_group="fasta"))
    assert "about to pull hg38/fasta" in caplog.text


def test_post_build_logs_the_result(caplog):
    with caplog.at_level("INFO", logger="refgenie"):
        my_post_build_func(
            object(), HookEvent("post_build", genome="hg38", asset_group="fasta", succeeded=False)
        )
    assert "build of hg38/fasta failed" in caplog.text
