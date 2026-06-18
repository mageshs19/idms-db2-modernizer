class BusinessDatatypeInference:

    IDENTIFIER_WORDS = {
        "PHONE",
        "ZIP",
        "POSTAL",
        "SSN",
        "SS_NUMBER",
        "ACCOUNT",
        "POLICY",
        "LICENSE",
        "CODE"
    }

    @staticmethod
    def infer(
        field_name: str,
        current_type: str
    ) -> str:

        upper_name = field_name.upper()

        for word in (
            BusinessDatatypeInference
            .IDENTIFIER_WORDS
        ):

            if word in upper_name:

                return "VARCHAR"

        return current_type