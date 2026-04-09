
import click
import uvicorn
from pystonic.log import add_console_handler

from deepinsight.agents.collector.manager import MANAGER
from deepinsight.common.config import CONF

levels = ["WARNING", "INFO", "DEBUG", "TRACE"]


@click.group(context_settings={"help_option_names": ["-h", "--help"], "show_default": True})
@click.option("-v", "--verbose", count=True)
@click.version_option(package_name="ai-shell")
def app(verbose: int):
    """DeepInsight 命令行工具"""

    if not CONF.log.file and verbose:
        add_console_handler(levels[min(verbose, len(levels) - 1)])


@app.command("api")
def api_cmd():
    """API 服务（开发模式）"""
    uvicorn.run("deepinsight.api.main:app", host="0.0.0.0", port=8000, reload=True)


@app.command("collect")
def collect_cmd():
    """收集线索"""
    MANAGER.run()
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(MANAGER.start())
    # asyncio.run(MANAGER.start())


def main():
    app()


if __name__ == "__main__":
    main()
