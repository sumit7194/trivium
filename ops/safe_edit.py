"""Text edits that cannot silently no-op.

quantum's last unrescued item: edit-time asserts. Their reasoning was that the action is
"running the edit script", and there is no interception point -- the script is written
and run in one motion, and a hook on "running a script" is not a thing.

THE RIDE IS THE EDIT FUNCTION ITSELF, which is the same move they used for nulls. The
action that must happen for an edit to be used is CALLING SOMETHING THAT PERFORMS IT.
Put the verification inside that call and it cannot be skipped -- the caller does not
choose to check, they choose to edit.

    s = s.replace(old, new)        # silent no-op when `old` is absent
    edit(path, old, new)           # raises; there is no quiet path

Three silent no-ops today came from the first form -- two with no assert at all, one
where the assert fired and a later shell invocation committed anyway. This closes the
first two. The third is a control-flow gap and needs a pre-commit hook, not this.
"""
from pathlib import Path


class EditFailed(RuntimeError):
    pass


def edit(path, old, new, count=1, must_change=True):
    """Replace `old` with `new` in `path`. Raises rather than no-opping.

    Checks, in order, all of which have bitten someone today:
      - the file exists and is readable
      - `old` occurs at all                      (the classic silent no-op)
      - `old` occurs exactly `count` times       (a partial match edits the wrong site)
      - the text actually changed                (old == new is a no-op that "succeeds")
      - the write round-trips                    (verify by reading back, not by not-erroring)
    """
    p = Path(path)
    if not p.exists():
        raise EditFailed(f"{path}: does not exist")
    s = p.read_text()
    n = s.count(old)
    if n == 0:
        raise EditFailed(f"{path}: anchor not found -- {old[:60]!r}")
    if count is not None and n != count:
        raise EditFailed(f"{path}: anchor occurs {n}x, expected {count}x -- "
                         f"a partial match would edit the wrong site")
    if must_change and old == new:
        raise EditFailed(f"{path}: old == new, this edit is a no-op that would succeed")
    out = s.replace(old, new, count if count else -1)
    p.write_text(out)
    back = p.read_text()
    if back != out:
        raise EditFailed(f"{path}: write did not round-trip")
    if new not in back:
        raise EditFailed(f"{path}: replacement absent after write")
    return n


def append(path, text, marker=None):
    """Append, refusing if `marker` is already present -- the duplicate-section no-op."""
    p = Path(path)
    if marker and marker in p.read_text():
        raise EditFailed(f"{path}: marker already present -- {marker[:50]!r}; "
                         f"this append would duplicate it")
    with p.open("a") as f:
        f.write(text)
    if marker and marker not in p.read_text():
        raise EditFailed(f"{path}: marker absent after append")
