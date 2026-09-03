# Review checklist

Run before delivering `api-design.md`. Each unchecked item is either fixed or moved to Open questions with an owner. Do not deliver with silent failures.

- [ ] Every mutating operation states how idempotency works
- [ ] Every error in the catalog is returned by at least one operation, and every operation lists its errors
- [ ] Examples validate against the schemas they illustrate
- [ ] One naming convention, one pagination mechanism, one error shape
- [ ] No breaking change without a version or a deprecation path
- [ ] Every contested decision links a record; every inline decision has a one-line reason

General, every document skill:

- [ ] First section stands alone for a reader who reads nothing else
- [ ] No section is `missing` without a question asked or a default proposed
- [ ] `inferred` content says what it was inferred from
- [ ] Every decision record linked exists on disk and its status matches the table
- [ ] Changelog has a line for this round
