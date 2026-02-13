import os
from typing import Any
def fs_read(filepath: str, max_size = 2000) -> dict[str, Any]:

    if not os.path.exists(filepath):
        return f''
    
