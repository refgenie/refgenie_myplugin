"""A template refgenie plugin. Copy this package and replace these functions.

refgenie calls each function as ``func(rg, event)``: ``rg`` is the ``Refgenie``
instance and ``event`` is a ``refgenie.plugins.HookEvent``.
"""

import logging

from refgenie.plugins import HookEvent

#: The entry-point name, which is also this plugin's settings name.
PLUGIN_NAME = "myplugin"

# A child of the "refgenie" logger, so messages show up with refgenie's own.
_LOGGER = logging.getLogger("refgenie.plugins.myplugin")


def my_post_update_func(rg, event: HookEvent) -> None:
    """Runs once after any refgenie command that changed local assets."""
    # Settings are stored with: refgenie plugins set myplugin greeting=hi
    greeting = rg.plugins.settings(PLUGIN_NAME).get("greeting", "hello")
    for change in event.changes:
        _LOGGER.info(
            f"{greeting} from refgenie_myplugin: {change.action} "
            f"{change.genome}/{change.asset_group}:{change.asset}"
        )


def my_pre_pull_func(rg, event: HookEvent) -> None:
    """Runs before each asset pull."""
    _LOGGER.info(f"refgenie_myplugin: about to pull {event.genome}/{event.asset_group}")


def my_post_build_func(rg, event: HookEvent) -> None:
    """Runs after each build, whether it worked or not."""
    result = "succeeded" if event.succeeded else "failed"
    _LOGGER.info(f"refgenie_myplugin: build of {event.genome}/{event.asset_group} {result}")
