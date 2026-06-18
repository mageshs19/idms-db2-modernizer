from idms_modernizer.domain.canonical_models import (
    CanonicalSchema,
)

from idms_modernizer.domain.db2_models import (
    DB2Column,
    DB2ForeignKey,
    DB2Model,
    DB2Table,
)

from idms_modernizer.services.name_normalizer import (
    NameNormalizer,
)


class DB2MappingService:

    TYPE_MAPPING = {
        "DISPLAY": "VARCHAR",
        "COMP": "INTEGER",
        "COMP-3": "DECIMAL",
        "BINARY": "BIGINT",
    }

    def build_db2_model(
        self,
        schema: CanonicalSchema
    ) -> DB2Model:

        tables = []

        for record in schema.records:

            table = DB2Table(
                name=self.normalize_name(
                    record.name
                ),
                columns=[],
                foreign_keys=[]
            )

            #
            # Columns
            #
            for field in record.fields:

                column = DB2Column(
                    name=self.normalize_name(
                        field.name
                    ),
                    datatype=self.map_datatype(
                        field
                    )
                )

                table.columns.append(
                    column
                )

            tables.append(
                table
            )

        #
        # Relationships → Foreign Keys
        #
        for set_def in schema.sets:

            owner_table = (
                self.find_table(
                    tables,
                    set_def.owner_record
                )
            )

            member_table = (
                self.find_table(
                    tables,
                    set_def.member_record
                )
            )

            if (
                owner_table is None
                or member_table is None
            ):
                continue

            fk_column = (
                f"{owner_table.name}_ID"
            )

            member_table.foreign_keys.append(
                DB2ForeignKey(
                    column_name=fk_column,
                    reference_table=owner_table.name,
                    reference_column="ID"
                )
            )

        return DB2Model(
            tables=tables
        )

    def map_datatype(
        self,
        field
    ) -> str:

        datatype = (
            field.datatype
            or "DISPLAY"
        )

        datatype = (
            datatype.upper()
        )

        if datatype == "DATE":
            return "DATE"

        if datatype in {"TIMESTAMP", "DATETIME"}:
            return "TIMESTAMP"

        #
        # COMP-3
        #
        if datatype == "COMP-3":

            precision = (
                field.length
                or 18
            )

            scale = (
                field.scale
                or 0
            )

            return (
                f"DECIMAL({precision},{scale})"
            )

        #
        # DISPLAY
        #
        if datatype == "DISPLAY":

            length = (
                field.length
                or 255
            )

            return (
                f"VARCHAR({length})"
            )

        #
        # COMP
        #
        if datatype == "COMP":

            return "INTEGER"

        #
        # fallback
        #
        return "VARCHAR(255)"

    def normalize_name(
        self,
        name: str
    ) -> str:

        return NameNormalizer.normalize(
            name
        )

    def find_table(
        self,
        tables,
        record_name
    ):

        if not record_name:
            return None

        normalized = (
            self.normalize_name(
                record_name
            )
        )

        for table in tables:

            if table.name == normalized:

                return table

        return None