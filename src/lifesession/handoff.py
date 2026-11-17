"""Local checks for the v1 handoff contract; not evidence verification."""


def check_handoff(record):
    """Return stable error codes, never input values. Do not mutate the record.

    Additional fields are allowed. Passing means structural consistency only,
    not approval, authenticity, secret detection or full session validation.
    """
    errors = []
    if not isinstance(record, dict):
        return ['record.object_required']
    if not _text(record.get('session_id')):
        errors.append('session_id.nonempty_required')
    handoff = record.get('handoff')
    if not isinstance(handoff, dict):
        return errors + ['handoff.object_required']
    if handoff.get('version') != '1':
        errors.append('handoff.version_unsupported')
    delivery = handoff.get('delivery_status')
    review = handoff.get('review_status')
    if delivery not in ('not_sent', 'sent', 'acknowledged'):
        errors.append('handoff.delivery_status_invalid')
    if review not in ('pending', 'accepted', 'changes_requested'):
        errors.append('handoff.review_status_invalid')
    if review in ('accepted', 'changes_requested') and delivery != 'acknowledged':
        errors.append('handoff.review_requires_acknowledgment')
    if not _text(handoff.get('next_action')):
        errors.append('handoff.next_action_required')
    blockers = handoff.get('blockers')
    if not isinstance(blockers, list) or any(not _text(item) for item in blockers):
        errors.append('handoff.blockers_invalid')
    evidence = handoff.get('evidence')
    if not isinstance(evidence, list) or not evidence:
        errors.append('handoff.evidence_required')
    else:
        for item in evidence:
            if not isinstance(item, dict):
                errors.append('handoff.evidence_item_invalid')
                continue
            for field in ('kind', 'scope', 'limitations'):
                if not _text(item.get(field)):
                    errors.append('handoff.evidence_' + field + '_required')
            if item.get('result') not in ('passed', 'failed', 'not_run', 'blocked'):
                errors.append('handoff.evidence_result_invalid')
    # Keep diagnostics deterministic and compact even for many invalid entries.
    return list(dict.fromkeys(errors))


def _text(value):
    return isinstance(value, str) and bool(value.strip())
