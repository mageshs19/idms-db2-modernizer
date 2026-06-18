from idms_modernizer.domain.db2_models import (
    DB2Model,
    DB2Table,
    DB2Column,
    DB2ForeignKey
)

from idms_modernizer.services.db2_datatype_mapper import (
    DB2DatatypeMapper
)


class DB2ModelBuilder:

    def build(
        self,
        canonical_schema
    ) -> DB2Model:
        print("=" * 80)
        print("DB2ModelBuilder.build() CALLED")
        print("=" * 80)

        model = DB2Model()

        #
        # Tables
        #
        for record in canonical_schema.records:

            table = DB2Table(
                name=record.name,
                columns=[],
                primary_key=record.primary_key
            )

            for field in record.fields:

                is_pk = (
                    record.primary_key is not None
                    and field.name == record.primary_key
                )

                table.columns.append(
                    DB2Column(
                        name=field.name,
                        datatype=DB2DatatypeMapper.map(field),
                        nullable=not is_pk,
                        primary_key=is_pk
                    )
                )
            print(
                    f"DB2ModelBuilder: "
                    f"{table.name} "
                    f"PK={table.primary_key}"
                )

            model.tables.append(table)
        #
        # Foreign Keys
        #
        for rel in (
            canonical_schema.relationships
        ):

            parent_table = (
                self.find_table(
                    model,
                    rel.parent_record
                )
            )

            child_table = (
                self.find_table(
                    model,
                    rel.child_record
                )
            )

            if (
                parent_table is None
                or child_table is None
            ):
                continue

            if (
                parent_table.primary_key
                is None
            ):
                continue

            child_table.foreign_keys.append(
                DB2ForeignKey(
                    column_name=(
                        parent_table.primary_key
                    ),
                    reference_table=(
                        parent_table.name
                    ),
                    reference_column=(
                        parent_table.primary_key
                    )
                )
            )

        return model

    def find_table(
        self,
        model,
        table_name
    ):

        for table in model.tables:

            if table.name == table_name:

                return table

        return None