import asyncio

import pytest


@pytest.mark.asyncio
async def test_sanity():
    await asyncio.sleep(0.01)
    assert True
