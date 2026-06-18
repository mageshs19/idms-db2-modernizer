class DDLGenerator:

    def generate(
        self,
        db2_model
    ) -> str:

        ddl = []

        for table in db2_model.tables:

            ddl.append(
                f"CREATE TABLE {table.name}"
            )

            ddl.append("(")

            column_definitions = []

            #
            # Columns
            #
            for column in table.columns:

                definition = (
                    f"    {column.name} "
                    f"{column.datatype}"
                )

                if not column.nullable:

                    definition += (
                        " NOT NULL"
                    )

                column_definitions.append(
                    definition
                )

            #
            # Primary Key
            #
            if table.primary_key:

                column_definitions.append(
                    f"    PRIMARY KEY "
                    f"({table.primary_key})"
                )

            #
            # Foreign Keys
            #
            for fk in table.foreign_keys:

                column_definitions.append(
                    f"    FOREIGN KEY "
                    f"({fk.column_name}) "
                    f"REFERENCES "
                    f"{fk.reference_table}"
                    f"({fk.reference_column})"
                )

            ddl.append(
                ",\n".join(
                    column_definitions
                )
            )

            ddl.append(");")
            ddl.append("")

        return "\n".join(
            ddl
        )