from __future__ import annotations

from _discloud import (
    Terminal, 
    Backup, 
    ApplicationManager
)

class DiscloudBot:
    def __init__(self, /, *, discloud_token: str, bot_id: int) -> None:
        if not isinstance(bot_id, int):
            raise ValueError(
                f"Expected int as app_id, not {bot_id.__class__!r}"
            ) from None

        self._terminal = Terminal(
            discloud_token=discloud_token,
            app_id=bot_id
        )
        self._backup = Backup(
            discloud_token=discloud_token,
            app_id=bot_id
        )
        self._actions = ApplicationManager(
            discloud_token=discloud_token,
            app_id=bot_id
        )

    @classmethod
    def create(cls, discloud_token: str, bot_id: int) -> DiscloudBot:
        return cls(
            discloud_token=discloud_token,
            bot_id=bot_id
        )

    def restart(self) -> None:
        self._actions.restart()
    
    def logs(self) -> str:
        return self._terminal.fetch_small()

    def get_backup(self) -> str:
        return self._backup.download_url
