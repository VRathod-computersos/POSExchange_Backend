from graphene import ObjectType, String, Int, DateTime, List, Field
from ...database.connection import connect_to_database_master_db

class TermsAndConditionField(ObjectType):
    id = Int()
    title = String()
    terms_conditions = String()
    date_added = DateTime()
    date_modified = DateTime()

class TermsAndConditionMainTitle(ObjectType):
    main_title = Field(TermsAndConditionField)
    terms = List(TermsAndConditionField)

class TermsAndCondition(ObjectType):
    terms_and_conditions = Field(TermsAndConditionMainTitle)
    
    def resolve_terms_and_conditions(self, info):
        with connect_to_database_master_db() as master_db:
            with master_db.cursor() as master_cursor:
                main_title = None
                terms_data_list = []
                master_cursor.execute("SELECT id, Tiltle, Terms_Conditions, date_added, date_modified FROM Terms_And_Conditions")
                terms_data = master_cursor.fetchall()
                for term in terms_data:
                    id = term[0]
                    title = term[1]
                    terms_conditions = term[2]
                    date_added = term[3]
                    date_modified = term[4]

                    if id == 6:
                        main_title = TermsAndConditionField(
                            id=id,
                            title=title,
                            terms_conditions=terms_conditions,
                            date_added=date_added,
                            date_modified=date_modified
                        )
                    else:
                        terms_data_list.append(
                            TermsAndConditionField(
                                id=id,
                                title=title,
                                terms_conditions=terms_conditions,
                                date_added=date_added,
                                date_modified=date_modified
                            )
                        )
                
                return TermsAndConditionMainTitle(
                    main_title=main_title,
                    terms=terms_data_list
                )
