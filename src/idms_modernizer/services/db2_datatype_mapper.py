from idms_modernizer.services.business_datatype_inference import (
    BusinessDatatypeInference
)


class DB2DatatypeMapper:

    @staticmethod
    def map(field) -> str:

        datatype = (
            BusinessDatatypeInference.infer(
                field.name,
                field.datatype
            )
        )

        if datatype == "VARCHAR":

            length = (
                field.length
                if field.length
                else 255
            )

            return (
                f"VARCHAR({length})"
            )

        if datatype == "INTEGER":

            if (
                field.length
                and field.length <= 4
            ):
                return "SMALLINT"

            if (
                field.length
                and field.length <= 9
            ):
                return "INTEGER"

            return "BIGINT"

        if datatype == "DECIMAL":

            precision = (
                field.length
                if field.length
                else 10
            )

            scale = (
                field.scale
                if field.scale
                else 0
            )

            return (
                f"DECIMAL("
                f"{precision},"
                f"{scale}"
                f")"
            )

        return "VARCHAR(255)"