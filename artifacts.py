import time
import logging
import shutil


# Getting Artifacts based on CONF_FILE
def get_artifacts(art_path, art_category):
    time.sleep(0.5)
    print(f"Copying: {art_path}")
    logging.info(f'Getting {art_category} from {art_path}')

    # Use Copy 2 to preserve metadata
    # https://docs.python.org/3/library/shutil.html
    shutil.copy2(art_path, art_category)
