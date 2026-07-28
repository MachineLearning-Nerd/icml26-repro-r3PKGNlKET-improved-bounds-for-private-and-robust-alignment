# Historical judged baseline

Expected command:

```text
uv run --frozen python -m reproduction.runner
```

Expected outcome: the historical visibility audit exits zero while explicitly
reporting every scientific claim as BLOCKED. A nonzero exit means the protected
manifest, source record, verdict filter, or visibility record changed.
