import os
from string import Template
import requests
from dotenv import load_dotenv, dotenv_values

token = dotenv_values(".env").get("github_token")
headers = {"Authorization": f"Bearer {token}"}
GITHUB_URL = "https://api.github.com/graphql"


class GitHubGraphQl:
    def __init__(self):
        pass

    def _run_query(self, query: str, variables: dict) -> dict:
        response = requests.post(
            GITHUB_URL,
            json={"query": query, "variables": variables},
            headers=headers,
        )
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(
                f"Query failed to run by returning code of {response.status_code}, {query}"
            )

    def get_user_summary(self, name: str) -> dict:
        query = """
            query($name:String!){
                user(login:$name){
                        name
                        email
                        bio
                        company
                        location
                        followers(first:10){
                            totalCount
                        }
                        following(first:10){
                            totalCount
                        }
                        repositories(last: 10) {
                            nodes {
                                name
                            }
                        }
                        pinnedItems(first:10, types:[REPOSITORY, GIST]){
                            nodes{
                                ... on Repository{
                                    name
                                }
                                ... on Gist{
                                    name
                                }
                            }
                        }
                    }
                }
            """
        variables = {"name": name}
        response = self._run_query(query=query, variables=variables)
        return response

    def get_repositories(self, name: str, count: int, isFork: bool = False):
        # TODO: search nested queries to get Fork repos too.
        query = """
        query($name:String!, $first:Int!, $cursor:String){
            user(login:$name){
                repositories(
                    ownerAffiliations: [OWNER, ORGANIZATION_MEMBER, COLLABORATOR],
                    first: $first,
                    orderBy: {field:NAME, direction:ASC},
                    after: $cursor,
                    isFork: false
                    ){
                        totalCount
                        nodes{
                            name
                            owner{
                                login
                            }
                            isInOrganization
                            stargazerCount
                            viewerHasStarred
                            isFork
                            primaryLanguage{
                                name
                            }
                        }
                        pageInfo{
                            hasNextPage,
                            endCursor
                        }
                    }
                }
            }
        """
        variables = {"name": name, "first": count, "isFork": isFork}
        response = self._run_query(query=query, variables=variables)
        return response

    def find_repo(self, name: str, repo_name: str):
        query = """
        query($owner:String!, $name:String!){
            repository(owner:$owner, name:$name){
                isInOrganization
                description
                stargazerCount
                createdAt
                updatedAt
                visibility
                issues(last:10, states:[OPEN]){
                    nodes{
                        title
                        createdAt
                        updatedAt
                        url
                    }
                }
            }
        }
        """
        variables = {
            "owner": name,
            "name": repo_name,
        }
        response = self._run_query(query=query, variables=variables)
        return response


if __name__ == "__main__":
    gcli = GitHubGraphQl()
    result = gcli.get_user_summary("Badger-Embedded")
    print(result)
