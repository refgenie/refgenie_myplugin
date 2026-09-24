# Refgenie plugin template

This is a demo refgenie plugin. Copy this repository to start your own. A
refgenie plugin is a Python package with functions that refgenie calls during
specific refgenie actions.

The full reference is the plugin guide on refgenie.org:
<https://refgenie.org/refgenie/plugins/>.

## Hooks

| Hook | When it fires |
| --- | --- |
| `pre_pull` | before each asset pull |
| `post_pull` | after each asset pull |
| `pre_build` | before a build |
| `post_build` | after a build |
| `post_update` | once, after any command that changed local assets, aliases or genomes |

## 1. Register your functions in pyproject.toml

```toml
[project.entry-points."refgenie.hooks.post_update"]
myplugin = "refgenie_myplugin:my_post_update_func"
```

The format is `refgenie.hooks.<hook>` = `<name> = <package>:<function>`.

- `<hook>` must be one of the hooks above.
- `<name>` is your plugin's name. It is also the name for its settings.
- `<package>:<function>` points at the function to call.

## 2. Write the functions

Each function takes two arguments: `rg`, the `Refgenie` instance, and `event`,
a `refgenie.plugins.HookEvent` that says what happened. See
[refgenie_myplugin/refgenie_myplugin.py](refgenie_myplugin/refgenie_myplugin.py).

```python
from refgenie.plugins import HookEvent

def my_pre_pull_func(rg, event: HookEvent) -> None:
    print(f"about to pull {event.genome}/{event.asset_group}")
```

A plugin reads its settings from `rg`. This template's `post_update` function
reads a greeting, which you set with:

```
refgenie plugins set myplugin greeting=hi
```

## 3. Install it

```
pip install .
refgenie plugins
```

`refgenie plugins` should list `myplugin` with status `ok`.
