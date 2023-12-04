from typing import List
import click

import github
from utils.user import User
from utils.repository import Repository
from utils.issue import Issue


@click.group()
def main():
    pass


@main.command()
@click.argument("username", required=True, type=str)
def summary(username: str):
    res: dict = github.GitHubGraphQl().get_user_summary(name=username)
    user: User = User(res["data"]["user"])
    click.echo(click.style(f"Here short summary about {username}\n", fg="yellow"))
    click.echo(
        f"public name: {user.name}\n"
        + f"email: {user.email}\n"
        + f"company: {user.company}\n"
        + f"location: {user.location}\n"
        + f"bio: {user.bio}\n"
        + f"followers {user.followers}\n"
        + f"following {user.following}\n"
    )
    click.echo(
        click.style(f"{username}'s first ten repositories on GitHub", fg="yellow")
    )
    for repo in user.first_ten_repos:
        click.echo(f"${repo['name']}\n")

    click.echo(
        click.style(f"{username}'s first ten pinned items on GitHub", fg="yellow")
    )
    for pinnedItem in user.pinnedItems:
        if pinnedItem is not None:
            click.echo(f"${pinnedItem['name']}\n")


@main.group(invoke_without_command=True)
@click.pass_context
@click.argument("username")
def stalk(ctx, username):
    # ensure that ctx.obj exists and is a dict (in case `cli()` is called
    # by means other than the `if` block below)
    ctx.ensure_object(dict)
    ctx.obj["username"] = username


@stalk.group(name="repos", invoke_without_command=True)
@click.pass_context
@click.argument(
    "repo_name",
    required=False,
    type=str,
)
def repos(ctx: click.Context, repo_name: str):
    ctx.ensure_object(dict)
    ctx.obj["repo_name"] = repo_name

    if ctx.obj["repo_name"] == None:
        res: dict = github.GitHubGraphQl().get_repositories(
            name=ctx.obj["username"], count=100
        )
        user: User = User(res["data"]["user"])
        repos: List[Repository] = user.repositories

        if len(repos) != 0:
            click.echo(click.style(f'{ctx.obj["username"]} own repos:', fg="yellow"))
            user_repos = filter(
                lambda x: x.isInOrganization == False,
                repos,
            )
            for repo in user_repos:
                click.echo(
                    click.style(f"{repo.name}: | ", fg="green")
                    + "your star: "
                    + click.style(
                        "* | " if repo.viewerHasStarred else " | ", fg="yellow"
                    )
                    + "primary language: "
                    + (
                        f'{repo.primaryLanguage["name"]}'
                        if repo.primaryLanguage is not None
                        else ""
                    )
                    + "\n"
                )

            organization_repos = filter(lambda x: x.isInOrganization == True, repos)
            click.echo(
                click.style(
                    f'{ctx.obj["username"]}\'s organization repos:', fg="magenta"
                )
            )
            for org_repo in organization_repos:
                click.echo(
                    click.style(f"{org_repo.name}: | ", fg="green")
                    + "organization name: "
                    + f'{org_repo.owner["login"] } | '
                    + "your star: "
                    + click.style(
                        "* | " if org_repo.viewerHasStarred else " | ", fg="yellow"
                    )
                    + "primary language: "
                    + (
                        f'{org_repo.primaryLanguage["name"]}'
                        if org_repo.primaryLanguage is not None
                        else ""
                    )
                    + "\n"
                )
    else:
        res: dict = github.GitHubGraphQl().find_repo(
            name=ctx.obj["username"], repo_name=ctx.obj["repo_name"]
        )
        repo = Repository(**res["data"]["repository"])
        click.echo(click.style("Here short summary about the repo: \n", fg="yellow"))
        click.echo(
            click.style("Description: ", fg="magenta")
            + f"{repo.description}\n"
            + click.style("Stars: ", fg="magenta")
            + f"{repo.stargazerCount}\n"
            + click.style("Created At : ", fg="magenta")
            + f"{repo.createdAt}\n"
            + click.style("Updated At: ", fg="magenta")
            + f"{repo.updatedAt}\n"
            + click.style("Visibility: ", fg="magenta")
            + f"{repo.visibility}\n"
            + "\n"
        )
        issues: List[issue.Issue] = repo.issues
        if len(issues) != 0:
            click.echo(click.style("Last ten issue on this repo: \n", fg="red"))
            for issue in issues:
                click.echo(
                    f"Issue '{issue.title}' was created at: {issue.createdAt}, last update time is {issue.updatedAt}\n"
                    + "---> "
                    + click.style(f"{issue.url}", underline=True, bold=True)
                )


if __name__ == "__main__":
    main()
