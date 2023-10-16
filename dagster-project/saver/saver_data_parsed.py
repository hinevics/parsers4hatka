from typing import Dict, Any
import pickle


def saver(data: Dict[str, Any], path: str) -> None:
    with open(path, mode='wb', encoding='utf-8') as file:
        pickle.dump(data, file)
