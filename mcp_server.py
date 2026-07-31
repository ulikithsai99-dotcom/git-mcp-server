from mcp.server.fastmcp import FastMCP

from github import *
from github.replace import replace_code as replace_code_helper
from github.review_file import review_file as review_file_helper
from github.apply_fix import apply_fix as apply_fix_helper
from github.impact import impact_analysis as impact_analysis_helper
from github.replace_multiple import (
    replace_multiple_files as replace_multiple_files_helper
)
from github.find_symbol import (
    find_symbol as find_symbol_helper
)
from github.repository_map import (
    repository_map as repository_map_helper
)
from github.repository_analyzer import (
    repository_analyzer as repository_analyzer_helper
)
from github.dependency_graph import (
    dependency_graph as dependency_graph_helper
)
from github.workspace_context import (
    workspace_context as workspace_context_helper
)
from agent.workflow import SoftwareEngineerWorkflow

mcp = FastMCP("GitHub Toolkit")

class WorkflowTools:
    """
    Adapter exposing the methods required by SoftwareEngineerWorkflow.
    """

    workspace_context = staticmethod(workspace_context_helper)
    repository_map = staticmethod(repository_map_helper)
    review_file = staticmethod(review_file_helper)
    apply_fix = staticmethod(apply_fix_helper)

@mcp.tool()
def repositories():
    """
    List all GitHub repositories.
    """
    return list_repositories()


@mcp.tool()
def repository_details(repo_name: str):
    """
    Show information about a repository.
    """
    return get_repository(repo_name)


@mcp.tool()
def read_repository_readme(repo_name: str):
    """
    Read the README.md of a repository.
    """
    return read_readme(repo_name)


@mcp.tool()
def commits(repo_name: str):
    """
    Show the latest commits.
    """
    return list_commits(repo_name)


@mcp.tool()
def branches(repo_name: str):
    """
    Show repository branches.
    """
    return list_branches(repo_name)


@mcp.tool()
def issues(repo_name: str):
    """
    Show repository issues.
    """
    return list_issues(repo_name)


@mcp.tool()
def create_github_issue(repo_name: str, title: str, body: str):
    """
    Create a GitHub issue.
    """
    return create_issue(repo_name, title, body)


@mcp.tool()
def files(repo_name: str):
    """
    List files and folders in the root directory.
    """
    return list_files(repo_name)


@mcp.tool()
def file_contents(repo_name: str, file_path: str):
    """
    Read the contents of a file.
    """
    return read_file(repo_name, file_path)


@mcp.tool()
def repo_tree(repo_name: str):
    """
    Return the complete repository tree.
    """
    return repository_tree(repo_name)


@mcp.tool()
def search_repository(repo_name: str, keyword: str):
    """
    Search for a keyword in the repository.
    """
    return search_code(repo_name, keyword)


@mcp.tool()
def file_history(repo_name: str, file_path: str):
    """
    Show commit history for a file.
    """
    return get_file_history(repo_name, file_path)


@mcp.tool()
def new_branch(repo_name: str, branch_name: str):
    """
    Create a new Git branch.
    """
    return create_branch(repo_name, branch_name)


@mcp.tool()
def new_pull_request(
    repo_name: str,
    title: str,
    body: str,
    head: str
):
    """
    Create a GitHub Pull Request.
    """
    return create_pull_request(
        repo_name,
        title,
        body,
        head
    )


@mcp.tool()
def update_file(
    repo_name: str,
    file_path: str,
    new_content: str,
    commit_message: str
):
    """
    Update a file in GitHub.
    """
    return write_file(
        repo_name,
        file_path,
        new_content,
        commit_message
    )


@mcp.tool()
def repository_review(repo_name: str):
    """
    Read the important files required for a complete repository review.
    Returns the repository tree together with the contents of key files.
    """
    return repository_review_context(repo_name)


@mcp.tool()
def review_file(
    repo_name: str,
    file_path: str
):
    """
    Read a single file for detailed review.
    """
    return review_file_helper(
        repo_name,
        file_path
    )


@mcp.tool()
def replace_code(
    repo_name: str,
    file_path: str,
    old_code: str,
    new_code: str,
    commit_message: str
):
    """
    Replace a specific code snippet in a file and commit the change.
    """
    return replace_code_helper(
        repo_name,
        file_path,
        old_code,
        new_code,
        commit_message
    )


@mcp.tool()
def apply_fix(
    repo_name: str,
    file_path: str,
    old_code: str,
    new_code: str,
    commit_message: str
):
    """
    Review a file and apply a fix.
    """
    return apply_fix_helper(
        repo_name,
        file_path,
        old_code,
        new_code,
        commit_message
    )

@mcp.tool()
def impact_analysis(
    repo_name: str,
    symbol: str
):
    """
    Find every place where a symbol is used.
    """
    return impact_analysis_helper(
        repo_name,
        symbol
    )

@mcp.tool()
def replace_multiple_files(
    repo_name: str,
    edits: list,
    commit_message: str,
    branch: str = "main"
):
    """
    Replace code snippets across multiple files.
    """

    return replace_multiple_files_helper(
        repo_name,
        edits,
        commit_message,
        branch
    )

@mcp.tool()
def find_symbol(
    repo_name: str,
    symbol: str
):
    """
    Find where a symbol is defined or referenced.
    """

    return find_symbol_helper(
        repo_name,
        symbol
    )

@mcp.tool()
def repository_map(repo_name: str):
    """
    Generate a high-level map of the repository.
    """

    return repository_map_helper(repo_name)

@mcp.tool()
def repository_analyzer(
    repo_name: str
):
    """
    Analyze repository architecture.
    """

    return repository_analyzer_helper(
        repo_name
    )

@mcp.tool()
def dependency_graph(
    repo_name: str
):
    """
    Build the dependency graph of a repository.
    """

    return dependency_graph_helper(repo_name)

@mcp.tool()
def workspace_context(
    repo_name: str
):
    """
    Return the complete repository context for AI.
    """

    return workspace_context_helper(
        repo_name
    )

@mcp.tool()
def repair_repository(
    repo_name: str,
    issue: str
):
    """
    Analyze a repository, generate a repair plan,
    apply fixes, and prepare a pull request.
    """

    workflow = SoftwareEngineerWorkflow(
        WorkflowTools()
    )

    plan = workflow.execute(
        repo_name,
        issue
    )

    return {
        "completed": plan.completed,
        "summary": plan.summary,
        "proposed_changes": [
            change.model_dump()
            for change in plan.proposed_changes
        ],
        "fix_results": plan.fix_results,
        "pull_request": plan.pull_request,
    }

if __name__ == "__main__":
    print("Run http_server.py instead.")