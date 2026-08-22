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


def bulk_replace(paths, old, new, expect, protect):
    """Rename across many files, refusing the failure modes a bulk loop invites.

    quantum's finding: safe_edit refuses a silent no-op for a SINGLE edit, because
    old==new or a missing anchor is unambiguous. A LOOP reporting "changed 0 files" is a
    legitimate outcome, so nothing refuses it -- and a case-sensitivity mismatch produces
    exactly that. THE TOOL'S GUARANTEE DOES NOT EXTEND TO THE LOOP WRAPPED AROUND IT.
    I hit it: a case-sensitive rename reported 0 files while grep -i found two.

    And bridge's: A RENAME MUST NOT BE APPLIED TO THE TEXT THAT DOCUMENTS THE RENAME.
    That text is the only place the old term legitimately survives, so a global replace
    is *guaranteed* to destroy precisely the record you just added. The two operations
    conflict directly and a bulk tool loses one in either order.

      expect   required number of files to change. A mismatch RAISES -- so "0 files"
               and "more files than I meant" are both errors rather than outcomes.
      protect  substrings marking text that must keep the OLD term. Any file
               containing one is skipped and reported, not silently edited.

               *** REQUIRED, not defaulted. *** With a default of (), a caller who
               forgets it gets the destructive behaviour and a success message -- the
               decision-gated failure one level down, in the guard itself. Passing
               protect=() must be a deliberate statement that nothing documents the
               rename, not an omission. THE GUARD RIDES ON THE CALL ONLY IF THE CALL
               CANNOT OMIT IT.
    """
    from pathlib import Path
    changed, skipped = [], []
    for p in map(Path, paths):
        s = p.read_text()
        if old not in s:
            continue
        if any(m in s for m in protect):
            skipped.append(str(p)); continue
        p.write_text(s.replace(old, new))
        if new not in p.read_text():
            raise EditFailed(f"{p}: replacement absent after write")
        changed.append(str(p))
    if len(changed) != expect:
        raise EditFailed(
            f"expected {expect} file(s) to change, {len(changed)} did"
            f"{' (skipped as protected: ' + ', '.join(skipped) + ')' if skipped else ''}."
            f" A bulk rename that changes the wrong NUMBER of files has failed even when"
            f" every individual edit succeeded.")
    return changed, skipped
