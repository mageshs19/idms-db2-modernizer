from pathlib import Path

import streamlit as st

from idms_modernizer.core.config import settings
from idms_modernizer.core.utils import ensure_directory

from idms_modernizer.services.metadata_service import (
    MetadataService
)
from idms_modernizer.services.db2_datatype_mapper import (
    DB2DatatypeMapper
)

from idms_modernizer.services.name_normalizer import (
    NameNormalizer
)

from idms_modernizer.services.date_field_consolidator import (
    DateFieldConsolidator
)

from idms_modernizer.services.db2_datatype_mapper import (
    DB2DatatypeMapper
)

from idms_modernizer.services.er_diagram_generator import (
    generate_er_diagram
)

from idms_modernizer.core.constants import (
    ER_DIAGRAM_FILE
)

from idms_modernizer.services.canonical_schema_builder import (
    CanonicalSchemaBuilder
)

from idms_modernizer.services.db2_model_builder import (
    DB2ModelBuilder
)
from idms_modernizer.services.db2_model_builder import (
    DB2ModelBuilder
)
from idms_modernizer.generators.ddl_generator import (
    DDLGenerator
)


def initialize_directories() -> None:

    ensure_directory(settings.input_dir)
    ensure_directory(settings.output_dir)
    ensure_directory(settings.temp_dir)


def save_uploaded_file(
    uploaded_file,
    target_folder: str
) -> str:

    target_path = (
        Path(target_folder)
        / uploaded_file.name
    )

    with open(
        target_path,
        "wb"
    ) as file:

        file.write(
            uploaded_file.getbuffer()
        )

    return str(target_path)



def main() -> None:

    initialize_directories()

    st.set_page_config(
        page_title="IDMS DB2 Modernizer",
        layout="wide"
    )

    st.title(
        "IDMS ➜ DB2 Modernizer"
    )

    st.markdown(
        """
        Upload:

        1. IDMS Schema Listing PDF

        2. Bachman Diagram PDF

        Generate:

        - DB2 Data Model
        - DB2 DDL
        - ER Diagram
        - Migration Report
        """
    )

    schema_pdf = st.file_uploader(
        "Upload IDMS Schema PDF",
        type=["pdf"]
    )

    diagram_pdf = st.file_uploader(
        "Upload Bachman Diagram PDF",
        type=["pdf"]
    )

    if st.button(
        "Generate DB2 Model"
    ):

        if not schema_pdf:

            st.error(
                "Please upload Schema PDF"
            )

            st.stop()

        if not diagram_pdf:

            st.error(
                "Please upload Diagram PDF"
            )

            st.stop()

        schema_path = save_uploaded_file(
            schema_pdf,
            settings.input_dir
        )

        diagram_path = save_uploaded_file(
            diagram_pdf,
            settings.input_dir
        )

        st.success(
            "Files uploaded successfully"
        )

        st.write(
            f"Schema PDF: {schema_path}"
        )

        st.write(
            f"Diagram PDF: {diagram_path}"
        )

        st.info(
            "Processing started..."
        )

        try:

            metadata_service = (
                MetadataService()
            )

            metadata = (
                metadata_service.build_metadata(
                    schema_path
                )
            )

            canonical_builder = (
                CanonicalSchemaBuilder()
            )

            canonical_schema = (
                canonical_builder.build(
                    metadata
                )
            )

            db2_builder = (
                DB2ModelBuilder()
            )

            db2_model = (
                db2_builder.build(
                    canonical_schema
                )
            )
            print("=" * 80)
            print("APP CANONICAL SCHEMA")
            print("=" * 80)

            for record in canonical_schema.records:
                print(
                    f"{record.name} "
                    f"PK={record.primary_key}"
                )

            st.subheader("DB2 Model Debug")

            for table in db2_model.tables:
                st.write(
                    f"{table.name} -> PK = {table.primary_key}"
                )

            ddl_generator = (
                DDLGenerator()
            )

            ddl_text = (
                ddl_generator.generate(
                    db2_model
                )
            )

            relationships = metadata.relationships

        except Exception as ex:

            st.exception(ex)

            st.stop()

        record_count = len(
            metadata.records
        )

        all_sets = set()

        for record in metadata.records:

            for membership in record.set_memberships:

                all_sets.add(
                    membership.set_name
                )

        set_count = len(all_sets)

        relationship_count = len(
        relationships
    )

        st.subheader(
            "Summary"
        )

        col1, col2, col3 = (
            st.columns(3)
        )

        with col1:

            st.metric(
                "Records",
                record_count
            )

        with col2:

            st.metric(
                "Sets",
                set_count
            )

        with col3:

            st.metric(
                "Relationships",
                relationship_count
            )

        st.subheader(
            "Detected Sets"
        )

        for set_name in sorted(all_sets):

            st.write(set_name)

        st.subheader(
            "Relationships"
        )

        if relationships:

            for rel in relationships:

                st.write(
                    f"{rel.owner_record}"
                    f" --> "
                    f"{rel.member_record}"
                    f" ({rel.set_name})"
                )

        else:

            st.info(
                "Relationship extraction not implemented yet"
            )

        st.subheader(
            "Records & Fields"
        )

        for record in metadata.records:

            with st.expander(
                record.name
            ):

                st.write(
                    f"Fields Found: {len(record.fields)}"
                )

                st.json(
                    [
                        field.name
                        for field in record.fields
                    ]
                )

        ddl_text = (
            ddl_generator.generate(
                db2_model
            )
        )

        st.subheader(
            "Generated DDL Preview"
        )

        st.code(
            ddl_text,
            language="sql"
        )

        output_dir = Path(
            settings.output_dir
        )

        ddl_file = (
            output_dir
            / "db2_ddl.sql"
        )

        ddl_file.write_text(
            ddl_text,
            encoding="utf-8"
        )

        with open(
            ddl_file,
            "rb"
        ) as file:

            st.download_button(
                label="Download DB2 DDL",
                data=file,
                file_name="db2_ddl.sql",
                mime="text/sql"
            )

        # Write canonical metadata as JSON for download
        canonical_file = output_dir / "canonical_model.json"

        try:
            canonical_file.write_text(
                canonical_schema.model_dump_json(
                    indent=2
                ),
                encoding="utf-8"
            )

            with open(canonical_file, "rb") as jf:
                st.download_button(
                    label="Download Canonical Model (JSON)",
                    data=jf,
                    file_name="canonical_model.json",
                    mime="application/json"
                )

        except Exception:
            st.warning("Failed to write canonical model JSON")

        # Generate ER diagram and provide download
        er_path = output_dir / ER_DIAGRAM_FILE

        try:
            png_path = generate_er_diagram(
                metadata,
                str(er_path)
            )

            with open(png_path, "rb") as imgf:
                img_bytes = imgf.read()

            st.subheader("ER Diagram")
            st.image(img_bytes)

            st.download_button(
                label="Download ER Diagram",
                data=img_bytes,
                file_name=ER_DIAGRAM_FILE,
                mime="image/png"
            )

        except Exception as ex:
            st.warning(f"ER diagram generation failed: {ex}")


if __name__ == "__main__":

    main()