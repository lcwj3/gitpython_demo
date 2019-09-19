import os
import git
from unidiff import PatchSet
import json
## Module Constants
DATE_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S%z"
EMPTY_TREE_SHA = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"


def versions(path):
    """
    This function returns a generator which iterates through all commits of
    the repository located in the given path for the given branch. It yields
    file diff information to show a timeseries of file changes.
    """

    # Create the repository, raises an error if it isn't one.
    print(path)
    repo = git.Repo(path)
    branches = repo.branches

    # Iterate through every commit for the given branch in the repository
    parsed_commit = {}
    for branch in branches:

        for commit in repo.iter_commits(branch):
            commit_object = commit
            commit = commit.hexsha
            parsed_commit[commit] = {}
            parsed_commit[commit]['branch'] = branch.name

            #b = commit_object.data_stream
            message = commit_object.message
            parsed_commit[commit]['message'] = message
            a = repo.git.show(commit)
            #print(a)
            # encoding = a.headers.getparam('charset')
            patch = PatchSet(a)
            #print(patch)
            files = patch.modified_files
            parsed_commit[commit]['new_file'] = {}
            parsed_commit[commit]['del_file'] = {}
            parsed_commit[commit]['mod_file'] = {}
            for new_file in patch.added_files:
                pass
            for del_file in patch.removed_files:
                pass
            for modified_file in files:
                #print(modified_file)
                for i in range(int(len(modified_file))):
                    hunk = modified_file[i]
                    file_content = {}
                    file_content['section_header'] = hunk.section_header
                    print(file_content)
                    file_content['modified_lines'] = []
                    for j in range(int(len(hunk))):
                        x = hunk[j]
                        line = {'diff_line_no': x.diff_line_no, 'is_added':x.is_added, 'is_contect': x.is_context,
                                'is_removed': x.is_removed, 'line_type': x.line_type, 'source_line_no': x.source_line_no,
                                'target_line_no': x.target_line_no, 'value': x.value}

                        file_content['modified_lines'].append(line)
                parsed_commit[commit]['mod_file'][modified_file.path] = file_content
    with open('commit.json', 'w') as f:
        json.dump(parsed_commit, f)


def diff_size(diff):
    """
    Computes the size of the diff by comparing the size of the blobs.
    """
    if diff.b_blob is None and diff.deleted_file:
        # This is a deletion, so return negative the size of the original.
        return diff.a_blob.size * -1

    if diff.a_blob is None and diff.new_file:
        # This is a new file, so return the size of the new value.
        return diff.b_blob.size

    # Otherwise just return the size a-b
    return diff.a_blob.size - diff.b_blob.size


def diff_type(diff):
    """
    Determines the type of the diff by looking at the diff flags.
    """
    if diff.renamed: return 'R'
    if diff.deleted_file: return 'D'
    if diff.new_file: return 'A'
    return 'M'
p = '/home/chengwei/codes/graph_pipeline'
versions(p)

