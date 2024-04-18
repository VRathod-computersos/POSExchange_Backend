import graphene

class RegisterInput(graphene.InputObjectType):
    email = graphene.String(required=True)
    password = graphene.String(required=True)
    client_id = graphene.Int(required=True)
    license_key = graphene.String(required=True)
    company_name = graphene.String(required=True)
    pos_id = graphene.Int(required=True)
    tenant_id = graphene.String()
    number_of_license = graphene.Int()
    whether_free = graphene.String(required=True)
    trial_end_date = graphene.Date()
 
class POSField(graphene.ObjectType):
    pos_id = graphene.Int()
    pos_name = graphene.String()
    paid_plan_code = graphene.String()
    free_plan_code = graphene.String()
    pos_description = graphene.String()
