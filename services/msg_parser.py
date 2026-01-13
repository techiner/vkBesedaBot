import shlex
import re
from domain.commands import Commands

MENTION_PATTERN = re.compile(r'^\[club\d+\|@[^]]+\]\s*', re.IGNORECASE)

def is_mention(msg) -> bool:
    return delete_mention_text(msg) != msg 


def delete_mention_text(msg) -> str:
    return MENTION_PATTERN.sub('', msg)


def get_command(msg) -> Commands | None:
    shlexed = shlex.split(msg.strip())
    if len(shlexed) > 1:
        try:
            return Commands(shlexed[1])
        except ValueError:
            pass
    return None


def get_args_from_command(msg) -> str:
    shlexed = shlex.split(msg.strip())
    if len(shlexed) > 2:
        return " ".join(shlexed[2:])
    return ""
