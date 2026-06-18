import re

from idms_modernizer.domain.relationship_models import (
    SetMembership
)


class OwnerMemberExtractor:

    SET_PATTERN = re.compile(
        r"^\s*([A-Z0-9\-]+)\s+(?:INDEX\s+)?(OWNER|MEMBER)\b",
        re.IGNORECASE
    )

    def extract(
        self,
        record_name: str,
        lines: list[str]
    ) -> list[SetMembership]:

        memberships = []

        for line in lines:

            match = (
                self.SET_PATTERN.search(
                    line
                )
            )

            if match:

                memberships.append(
                    SetMembership(
                        set_name=match.group(1).upper(),
                        role=match.group(2).upper()
                    )
                )
            print(
                    f"{record_name}: "
                    f"{len(memberships)} memberships"
                )
            for membership in memberships:
                print(
                    f"{record_name} -> "
                    f"{membership.set_name} "
                    f"{membership.role}"
                )

        return memberships