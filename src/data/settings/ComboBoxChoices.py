from enum import StrEnum

from src.data.Currencies import Currencies


class DebugLevels(StrEnum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


debug_levels = {
    DebugLevels.DEBUG: "Debug",
    DebugLevels.INFO: "Info",
    DebugLevels.WARNING: "Warning",
    DebugLevels.ERROR: "Error",
    DebugLevels.CRITICAL: "Critical",
}


class ApplicationStyles(StrEnum):
    WINDOWS = ("Windows",)
    FUSION = ("Fusion",)
    GTKPLUS = "GTK+"


application_styles = {
    ApplicationStyles.WINDOWS: "Windows",
    ApplicationStyles.FUSION: "Fusion",
    ApplicationStyles.GTKPLUS: "GTK+",
}


currencies = {
    currency: currency for currency in Currencies
}
