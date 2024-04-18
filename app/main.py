import uvicorn 
from fastapi import FastAPI
from starlette_graphene3 import GraphQLApp
# from  .graphql.operations.registerSeller import  Query as RegisterUserQuery, Mutation as RegisterUserMutation
from .graphql.operations.registerSeller import Query as RegisterQuery, Mutation as RegisterMutation
from .graphql.operations.LoginUser import Query as LoginQuery, Mutation as LoginMutation
import graphene
from .graphql.operations.LoginUser import Query as LogoutQuery, Mutation as LogoutMutation
app = FastAPI()

app.add_route(
    "/register",
    GraphQLApp(
        schema=graphene.Schema(query=RegisterQuery, mutation=RegisterMutation)
    ),
)
app.add_route(
    "/login",
    GraphQLApp(schema=graphene.Schema(query=LoginQuery, mutation=LoginMutation)),
)
app.add_route(
    "/logout",
    GraphQLApp(schema=graphene.Schema(query=LogoutQuery, mutation=LogoutMutation)),
)


# if __name__ =="__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)