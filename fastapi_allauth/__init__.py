VERSION = (0, 1, 0, "dev", 0)

__title__ = "fastapi-allauth"
__version_info__ = VERSION
__version__ = ".".join(map(str, VERSION[:3])) + (
    "-{}{}".format(VERSION[3], VERSION[4]
                   or "") if VERSION[3] != "final" else ""
)
__author__ = "villain organization"
__license__ = "MIT"
__copyright__ = "Copyright 2023 villain organization and contributors"


from allauth_manager import AllauthManager