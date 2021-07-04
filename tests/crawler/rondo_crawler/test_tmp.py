import asyncclick as click
import trio
from asyncclick.testing import CliRunner


async def internal():
    await trio.sleep(1)


@click.command()
async def main():
   async with trio.open_nursery() as nursery:
       nursery.start_soon(internal)


async def test_hello_world():
  runner = CliRunner()
  result = await runner.invoke(main, catch_exceptions=False)
  assert result.exit_code == 0
