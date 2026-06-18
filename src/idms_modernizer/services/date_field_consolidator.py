from idms_modernizer.domain.schema_models import (
    DataField
)

from idms_modernizer.services.name_normalizer import (
    NameNormalizer
)


class DateFieldConsolidator:

    DATE_PREFIXES = [
        "START",
        "FINISH",
        "BIRTH",
        "CLAIM",
        "SERVICE",
        "ADMIT",
        "DISCHARGE",
        "TERMINATION"
    ]

    @staticmethod
    def consolidate(fields):

        result = []

        consumed = set()

        field_lookup = {
            NameNormalizer.normalize(field.name): field
            for field in fields
        }

        #
        # Pass 1
        # Create consolidated date fields
        #
        for prefix in DateFieldConsolidator.DATE_PREFIXES:

            year_name = f"{prefix}_YEAR"
            month_name = f"{prefix}_MONTH"
            day_name = f"{prefix}_DAY"

            if (
                year_name in field_lookup
                and month_name in field_lookup
            ):

                result.append(
                    DataField(
                        name=f"{prefix}_DATE",
                        datatype="DATE"
                    )
                )

                consumed.add(year_name)
                consumed.add(month_name)

                if day_name in field_lookup:
                    consumed.add(day_name)

        #
        # Pass 2
        # Add all non-consumed fields
        #
        for field in fields:

            normalized_name = (
                NameNormalizer.normalize(
                    field.name
                )
            )

            if normalized_name in consumed:
                continue

            result.append(field)

        return result