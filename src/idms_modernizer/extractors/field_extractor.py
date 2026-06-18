import re

from idms_modernizer.domain.schema_models import (
    DataField
)


class FieldExtractor:

    FIELD_PATTERN = re.compile(
        r"^\s*(\d{2})\s+([A-Z0-9\-]+)\s+DISPLAY\s+([X9]\(\d+\)|9\(\d+\)V9\(\d+\)|9\(\d+\)|X\(\d+\))",
        re.IGNORECASE
    )

    def extract(
        self,
        lines: list[str]
    ) -> list[DataField]:

        fields = []

        for line in lines:

            match = self.FIELD_PATTERN.search(
                line
            )

            if not match:
                continue

            field_name = (
                match.group(2)
                .strip()
                .upper()
            )

            picture = (
                match.group(3)
                .strip()
                .upper()
            )

            datatype = "VARCHAR"
            length = None
            scale = None

            if picture.startswith("X("):

                datatype = "VARCHAR"

                length_match = re.search(
                    r"X\((\d+)\)",
                    picture
                )

                if length_match:
                    length = int(
                        length_match.group(1)
                    )

            elif picture.startswith("9("):

                datatype = "INTEGER"

                length_match = re.search(
                    r"9\((\d+)\)",
                    picture
                )

                if length_match:
                    length = int(
                        length_match.group(1)
                    )

                if "V" in picture:

                    datatype = "DECIMAL"

                    decimal_match = re.search(
                        r"V9\((\d+)\)",
                        picture
                    )

                    if decimal_match:
                        scale = int(
                            decimal_match.group(1)
                        )

            fields.append(
                DataField(
                    name=field_name,
                    datatype=datatype,
                    length=length,
                    scale=scale,
                    picture=picture,

                )
            )

        return fields