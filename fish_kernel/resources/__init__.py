import glob
import pathlib

ICON_PATHS = glob.glob(
    f"{pathlib.Path(__file__).resolve().parent}/logo-*.png"
)
