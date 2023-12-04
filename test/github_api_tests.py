import pytest
import github


def test_github_get_summary():
    g_api = github.GitHubGraphQl()
    user_name = "talhaHavadar"
    public_name = "Talha Can Havadar"
    company = "@canonical "
    followers = 26
    following = 10
    result = g_api.get_user_summary(user_name)
    user = result["data"]["user"]
    assert type(result) is dict
    assert user["name"] == public_name
    assert user["company"] == company
    assert user["followers"]["totalCount"] == followers
    assert user["following"]["totalCount"] == following


def test_github_get_repositories():
    g_api = github.GitHubGraphQl()
    user_name = "talhaHavadar"
    name_first_repo = "aem-bundle-comperator"
    result = g_api.get_repositories(user_name, 1)
    assert type(result) is dict
    repositories = result["data"]["user"]["repositories"]["nodes"]
    assert len(repositories) == 1
    assert repositories[0]["name"] == name_first_repo
    result2 = g_api.get_repositories(user_name, 2)
    repositories2 = result2["data"]["user"]["repositories"]["nodes"]
    assert len(repositories2) == 2


def test_github_find_repo():
    g_api = github.GitHubGraphQl()
    user_name = "talhaHavadar"
    name_first_repo = "aem-bundle-comperator"
    result = g_api.find_repo(user_name, name_first_repo)
    assert type(result) is dict
    repo = result["data"]["repository"]
    assert repo["isInOrganization"] == False
    assert len(repo["issues"]["nodes"]) == 0
