"""
Central prompt library for the AI Software Engineer.
"""


class PromptLibrary:
    """
    Collection of reusable prompts used throughout
    the intelligence layer.
    """

    SYSTEM = """
You are an expert Staff Software Engineer.

You analyze repositories before making any code changes.

Your goals are:

- Understand the architecture.
- Find the root cause.
- Suggest the smallest possible fix.
- Never invent files.
- Never hallucinate APIs.
- Preserve existing coding style.
- Think step by step before answering.
"""

    ANALYZE_REPOSITORY = """
Repository:
{repository}

Issue:
{issue}

Repository Context:
{workspace}

Candidate Files:
{candidate_files}

Reviewed Files:
{reviewed_files}

Your task:

1. Explain the root cause.
2. Explain why the bug happens.
3. Identify affected files.
4. Suggest the minimum fix.
5. Explain possible side effects.

Respond using valid JSON.
"""

    REVIEW_CODE = """
Review the supplied source code.

Focus on:

- Bugs
- Security
- Performance
- Maintainability
- Code Quality

Return only JSON.
"""

    GENERATE_FIX = """
Generate the smallest possible fix.

Rules:

- Do not rewrite unrelated code.
- Preserve formatting.
- Preserve functionality.
- Return only modified code.
- Explain every change.

Return valid JSON.
"""

    GENERATE_PULL_REQUEST = """
Generate a professional Pull Request.

Include:

- Summary
- Root Cause
- Solution
- Files Changed
- Testing Recommendations

Return Markdown.
"""