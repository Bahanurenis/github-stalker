# github-stalker

github-stalker is command line tool to retrieves data from GitHub GraphQL API for an GitHub user. It is using python requests package to post requests and it is using the click  package to create a beautiful command line interface.
### Installing:

Clone the repo and run the below command to create pip package
Add your GitHub Personal Access Token to environment.
	- the repo is using the dotenv package so you can add your .env file to the repo
	github_token="$YOUR_GITHUB_PAT_"

`pip install -e .`


### Usage:

1. Brief summary about the GitHub profile of the person

` github-stalker summary ($login_name)`
you will see with this comment:
* public name, email, company, location, bio, number of followers, number of following.
* Name of the first 10 repositories.
* Name of the first 10 pinned items.

** Don't forget some users don't have public name, so use the GitHub Account Name (e.g. use "Bahanurenis" instead of "Benis")


2. Now we are starting to stalk. Get first 100 repositories of user, you can see them in two different group like "$user own repos" and "$user's organization repos" group.

```

github-stalker stalk ($login_name) repos

```

with this command you will see the first 100 repositories as below:
*  The person's own repos:
	* with: name, primary language and you will see if you gave a star this repo before:
	* ![[Pasted image 20231204193921.png]]
 * If person has an organization and if he/she is a collaborator, you can see
	 * ![[Pasted image 20231204194102.png]]
 3. If you want to see specific repo, it is also easy.
 ```
 github-stalker stalk ($login_name) repos [repo_name]
```
 with this command you will see the repo's details:
 * description, total star count, creation date and the last update date, visibility
 * the last 10 open issues with title, creation date, last updated date and the url link
 *![[Pasted image 20231204194919.png]]

##### Attention:
github-stalker doesn't support the organization search with 1. and 2. usage. But if you will search a specific repo, the tool supports this. So you can stalk an organization's repo like below:
```
github-stalker stalk ($organization_login_name) repos ($repo_name)
```
![[Pasted image 20231204195319.png]]
