import re


class PrimaryKeyExtractor:

    CALC_PATTERN = re.compile(
        r"CALC\s+USING\s+([A-Z0-9\-]+)",
        re.IGNORECASE
    )

    def extract(
        self,
        lines: list[str]
    ) -> str | None:

        for line in lines:

            match = (
                self.CALC_PATTERN.search(
                    line
                )
            )

            if match:

                return (
                    match.group(1)
                    .replace("-", "_")
                    .upper()
                )

        return None