from github_tools import (
    list_repositories,
    get_repository,
    read_readme,
    list_commits,
    list_branches,
    list_issues,
    create_issue,
    list_files,
    read_file,
    repository_tree,
    search_code,
    get_file_history,
    create_branch,
    create_pull_request,
    write_file,
)
print("=" * 40)
print("🚀 GitHub Toolkit")
print("=" * 40)

print("1. List Repositories")
print("2. Repository Details")
print("3. Read README")
print("4. List Commits")
print("5. List Branches")
print("6. List Issues")
print("7. Create Issue")
print("8. List Files")
print("9. Read File")
print("10. Repository Tree")
print("11. Search Code")
print("12. Get File History")
print("13. Create Branch")
print("14. Create Pull Request")
print("15. Write File")
choice = input("\nChoose an option: ")

if choice == "1":
    repos = list_repositories()

    print("\n📁 Your Repositories\n")

    for repo in repos:
        print(f"📂 Name       : {repo['name']}")
        print(f"⭐ Stars      : {repo['stars']}")
        print(f"🌍 Visibility : {repo['visibility']}")
        print("-" * 40)

elif choice == "2":
    repo = input("Repository: ")

    details = get_repository(repo)

    print("\n📦 Repository Details\n")

    print(f"📂 Name        : {details['name']}")
    print(f"📝 Description : {details['description']}")
    print(f"⭐ Stars       : {details['stars']}")
    print(f"🍴 Forks       : {details['forks']}")
    print(f"👀 Watchers    : {details['watchers']}")
    print(f"🌍 Visibility  : {details['visibility']}")
    print(f"🔗 URL         : {details['url']}")

elif choice == "3":
    repo = input("Repository: ")

    readme = read_readme(repo)

    print("\n" + "=" * 60)
    print("README")
    print("=" * 60)
    print(readme)

elif choice == "4":
    repo = input("Repository: ")

    commits = list_commits(repo)

    print("\n📝 Latest Commits\n")

    for commit in commits:
        print(f"🔖 SHA     : {commit['sha']}")
        print(f"👤 Author  : {commit['author']}")
        print(f"📅 Date    : {commit['date']}")
        print(f"💬 Message : {commit['message']}")
        print("-" * 50)

elif choice == "5":
    repo = input("Repository: ")

    branches = list_branches(repo)

    print("\n🌿 Repository Branches\n")

    for branch in branches:
        print(f"🌿 Branch : {branch['name']}")
        print(f"🔖 SHA    : {branch['sha']}")
        print("-" * 40)

elif choice == "6":
    repo = input("Repository: ")

    issues = list_issues(repo)

    if not issues:
        print("\n✅ No Issues Found.")
    else:
        print("\n🐞 Repository Issues\n")

        for issue in issues:
            print(f"🐞 Issue #{issue['number']}")
            print(f"📝 Title   : {issue['title']}")
            print(f"📌 State   : {issue['state']}")
            print(f"👤 Author  : {issue['author']}")
            print(f"📅 Created : {issue['created_at']}")
            print("-" * 50)

elif choice == "7":
    repo = input("Repository: ")
    title = input("Issue Title: ")
    body = input("Issue Description: ")

    issue = create_issue(repo, title, body)

    print("\n✅ Issue Created Successfully!\n")
    print(f"🐞 Issue #{issue['number']}")
    print(f"📝 Title : {issue['title']}")
    print(f"🔗 URL   : {issue['url']}")


elif choice == "8":
    repo = input("Repository: ")

    files = list_files(repo)

    print("\n📁 Repository Contents\n")

    for file in files:
        icon = "📄" if file["type"] == "file" else "📁"

        print(f"{icon} {file['path']}")

elif choice == "9":
    repo = input("Repository: ")
    path = input("File Path: ")

    content = read_file(repo, path)

    print("\nFile Contents\n")
    print(content)

elif choice == "10":

    repo = input("Repository: ")

    tree = repository_tree(repo)

    print("\nRepository Tree\n")

    for item in tree:

        icon = "📁" if item["type"] == "tree" else "📄"

        print(f"{icon} {item['path']}")

elif choice == "11":

    repo = input("Repository: ")
    keyword = input("Keyword: ")

    results = search_code(repo, keyword)

    print("\nSearch Results\n")

    if not results:
        print("No matches found.")

    else:
        for result in results:
            print(f"📄 {result['file']}")        

elif choice == "12":

    repo = input("Repository: ")
    path = input("File Path: ")

    history = get_file_history(repo, path)

    print("\nFile History\n")

    if not history:
        print("No history found.")

    else:
        for commit in history:

            print("-" * 50)
            print(f"SHA     : {commit['sha']}")
            print(f"Author  : {commit['author']}")
            print(f"Date    : {commit['date']}")
            print(f"Message : {commit['message']}")

elif choice == "13":

    repo = input("Repository: ")
    branch = input("Branch Name: ")

    result = create_branch(repo, branch)

    print("\nBranch Created\n")

    print(f"Branch : {result['branch']}")
    print(f"SHA    : {result['sha']}")

elif choice == "14":

    repo = input("Repository: ")
    title = input("PR Title: ")
    body = input("PR Description: ")
    head = input("Source Branch: ")

    pr = create_pull_request(
        repo,
        title,
        body,
        head
    )

    print("\nPull Request Created\n")

    print(f"PR #{pr['number']}")
    print(f"Title : {pr['title']}")
    print(f"State : {pr['state']}")
    print(f"URL   : {pr['url']}")

elif choice == "15":

    repo = input("Repository: ")
    path = input("File Path: ")

    print("\nEnter new content.")
    print("Finish by typing END on a new line.\n")

    lines = []

    while True:

        line = input()

        if line == "END":
            break

        lines.append(line)

    content = "\n".join(lines)

    message = input("\nCommit Message: ")

    result = write_file(
        repo,
        path,
        content,
        message
    )

    print("\nFile Updated Successfully\n")

    print(f"Commit : {result['commit']}")
    print(f"URL    : {result['url']}")

else:
    print("❌ Invalid choice")
