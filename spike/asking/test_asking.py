"""RS7-U3 tests: quick, each bounded (a hung call is cut by `hang`, the whole test by `go`)."""

from __future__ import annotations

import anyio
from harness import Row, run

HANG = 2.0  # a call still waiting after this long is HUNG


def go(variant: str, tool: str, client: str, **kw) -> Row:
    async def main() -> Row:
        with anyio.fail_after(20):  # the whole test, server start and teardown included
            return await run(variant, tool, client, hang=kw.pop("hang", HANG), **kw)

    return anyio.run(main)


def hung(r: Row) -> bool:
    return r.outcome.startswith("HUNG")


def test_b1_baseline_works_for_a_client_that_reads_the_get_stream():
    r = go("B1", "b1_session", "A1 sdk-answers")
    assert not hung(r) and r.stream.startswith("GET") and '"accept"' in r.saw


def test_b1_baseline_hangs_for_a_post_only_client_and_is_dropped_on_the_server():
    for client in ("A4 raw-postonly", "A4s sdk-postonly"):
        r = go("B1", "b1_session", client)
        assert (
            hung(r) and r.stream.startswith("none: routed to GET stream") and "no prompt" in r.saw
        )


def test_b2_and_b3_reach_a_post_only_client():
    for tool in ("b2_related", "b3_ctx"):
        for client in ("A4 raw-postonly", "A4s sdk-postonly", "A1 sdk-answers"):
            r = go("B2", tool, client)
            assert not hung(r) and r.stream.startswith("POST") and '"accept"' in r.saw


def test_a_client_that_never_answers_hangs_the_call_without_a_server_timeout():
    r = go("B3", "b3_ctx", "A4q raw-silent")
    assert hung(r) and "prompt shown" in r.saw and r.stream.startswith("POST")


def test_a3_client_without_the_capability_is_not_asked():
    for tool in ("b1_session", "b2_related", "b3_ctx", "b6_url"):
        r = go("A3", tool, "A3 sdk-nocap")
        assert not hung(r) and "did not declare" in r.saw and r.server == "did not ask"


def test_b4_stateless_check_fails_and_the_answer_is_lost():
    r = go("B4", "b3_ctx", "A4 raw-postonly", stateless=True)
    assert "did not declare" in r.saw  # no initialize state to check
    r = go("B4", "b3_ctx", "A4 raw-postonly", stateless=True, check=False)
    assert hung(r) and "prompt shown" in r.saw and r.stream.startswith("POST")


def test_b5_json_response_cannot_carry_a_related_request():
    r = go("B5", "b3_ctx", "A4 raw-postonly", json_response=True)
    assert hung(r) and r.stream.startswith("none: routed to POST stream")


def test_b6_url_mode_over_post_stream():
    r = go("B6", "b6_url", "A4 raw-postonly")
    assert not hung(r) and r.stream.startswith("POST") and '"elicited": true' in r.saw


def test_b7_after_notifications_same_routing():
    assert go("B7", "b7_after_ctx", "A4 raw-postonly").stream.startswith("POST")
    assert hung(go("B7", "b7_after_session", "A4 raw-postonly"))


def test_b8_declared_capabilities_and_sdk_check():
    r = go("B8", "b8_caps", "A1 sdk-answers")
    assert '"declared": {"form": {}, "url": {}}' in r.saw
    r = go("B8", "b8_caps", "A3 sdk-nocap")
    assert '"declared": null' in r.saw and '"check_empty": false' in r.saw
    r = go("B8", "b8_caps", "R {url:{}}")
    assert '"check_form": true' in r.saw  # the SDK check does not look at sub-capabilities
    r = go("B8", "b8_nocheck", "A3 sdk-nocap")
    assert "Elicitation not supported" in r.saw


def test_b9_server_timeout_returns_a_fallback_for_both_routes():
    for tool in ("b9_timeout_session", "b9_timeout_ctx"):
        r = go("B9", tool, "A4q raw-silent", wait=0.5, hang=4)
        assert not hung(r) and "no answer in 0.5 s" in r.saw and "assistant_instruction" in r.saw


def test_b10_two_step_and_instruct_need_no_client_support():
    r = go("B10", "b10_flow", "A3 sdk-nocap")
    assert '"apply": true' in r.saw and '"replay": false' in r.saw and '"instruct": true' in r.saw


def test_b11_annotations_are_listed():
    r = go("B11", "tools/list", "A3 sdk-nocap")
    assert "b10_apply={'readOnlyHint': False, 'destructiveHint': True" in r.saw
