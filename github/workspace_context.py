from .review import repository_review_context
from .repository_analyzer import repository_analyzer
from .repository_map import repository_map
from .dependency_graph import dependency_graph


def workspace_context(repo_name):
    """
    Return a complete repository context for AI analysis.
    """

    review = repository_review_context(repo_name)

    analyzer = repository_analyzer(repo_name)

    repo_map = repository_map(repo_name)

    dependencies = dependency_graph(repo_name)

    return {

        "repository": repo_name,

        "review": review,

        "architecture": analyzer,

        "repository_map": repo_map,

        "dependency_graph": dependencies

    }