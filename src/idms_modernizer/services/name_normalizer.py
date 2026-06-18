import re


class NameNormalizer:

    @staticmethod
    def normalize(
        name: str
    ) -> str:

        name = name.strip().upper()
        name = name.replace("-", "_").replace(" ", "_")
        name = re.sub(r"_\d{4}$", "", name)
        name = re.sub(r"__+", "_", name)
        return name.strip("_")