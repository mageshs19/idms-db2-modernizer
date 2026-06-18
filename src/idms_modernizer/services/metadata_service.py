from idms_modernizer.parsers.text_extractor import (
    TextExtractor
)

from idms_modernizer.services.document_segmenter import (
    DocumentSegmenter
)

from idms_modernizer.extractors.owner_member_extractor import (
    OwnerMemberExtractor
)

from idms_modernizer.extractors.field_extractor import (
    FieldExtractor
)

from idms_modernizer.services.relationship_resolver import (
    RelationshipResolver
)

from idms_modernizer.domain.schema_models import (
    SchemaMetadata,
    Record
)

from idms_modernizer.extractors.primary_key_extractor import (
    PrimaryKeyExtractor
)


class MetadataService:

    def __init__(self):

        self.extractor = TextExtractor()

        self.segmenter = DocumentSegmenter()

        self.field_extractor = (
            FieldExtractor()
        )

        self.membership_extractor = (
            OwnerMemberExtractor()
        )

        self.relationship_resolver = (
            RelationshipResolver()
        )

        self.primary_key_extractor = (
            PrimaryKeyExtractor()
        )

    def build_metadata(
        self,
        pdf_path: str
    ) -> SchemaMetadata:

        document = (
            self.extractor.extract_document(
                pdf_path
            )
        )

        sections = (
            self.segmenter.segment(
                document
            )
        )

        metadata = SchemaMetadata()

        for section in sections:

            #
            # Debug EMPLOYEE section
            #
            if section.record_name == "EMPLOYEE":

                print("=" * 80)
                print("EMPLOYEE SECTION")

                for line in section.lines[:50]:

                    print(repr(line))

            #
            # Create Record directly
            #
            record = Record(
                name=section.record_name
            )

            #
            # Extract Fields
            #
            record.fields = (
                self.field_extractor.extract(
                    section.lines
                )
            )

            #
            # Extract OWNER/MEMBER memberships
            #
            record.set_memberships = (
                self.membership_extractor.extract(
                    section.record_name,
                    section.lines
                )
            )

            #
            # Extract Primary Key
            #
            record.primary_key = (
                self.primary_key_extractor.extract(
                    section.lines
                )
            )

            print(
                f"MetadataService: "
                f"{record.name} PK="
                f"{record.primary_key}"
            )

            metadata.records.append(
                record
            )

        #
        # Resolve Relationships
        #
        metadata.relationships = (
            self.relationship_resolver.resolve(
                metadata
            )
        )

        print(
            f"Relationships Found: "
            f"{len(metadata.relationships)}"
        )

        return metadata