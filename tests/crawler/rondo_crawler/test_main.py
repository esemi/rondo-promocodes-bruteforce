from asyncclick.testing import CliRunner

from app.rondo_crawler.crawler import main


async def test_smoke():
  runner = CliRunner()
  result = await runner.invoke(main, catch_exceptions=False)

  assert result.exit_code == 0
