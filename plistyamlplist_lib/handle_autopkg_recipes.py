#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import OrderedDict


def optimise_autopkg_recipes(recipe):
    """If input is an AutoPkg recipe, optimise the yaml output in 3 ways to aid
    human readability:

    1. Adjust the Processor dictionaries such that the Comment and Arguments keys are
       moved to the end, ensuring the Processor key is first.
    2. Ensure the NAME key is the first item in the Input dictionary.
    3. Order the items such that the Input and Process dictionaries are at the end.
    """

    if "Process" in recipe:
        process = recipe["Process"]
        new_process = []
        for processor in process:
            processor = OrderedDict(processor)
            if "Comment" in processor:
                processor.move_to_end("Comment")
            if "Arguments" in processor:
                processor.move_to_end("Arguments")
            new_process.append(processor)
        recipe["Process"] = new_process

    if "Input" in recipe:
        input = recipe["Input"]
        if "NAME" in input:
            input = OrderedDict(reversed(list(input.items())))
            input.move_to_end("NAME")
        recipe["Input"] = OrderedDict(reversed(list(input.items())))

    desired_order = [
        "Comment",
        "Description",
        "Identifier",
        "ParentRecipe",
        "MinimumVersion",
        "Input",
        "Process",
        "ParentRecipeTrustInfo",
    ]
    desired_list = [k for k in desired_order if k in recipe]
    reordered_recipe = {k: recipe[k] for k in desired_list}
    reordered_recipe = OrderedDict(reordered_recipe)
    return reordered_recipe


def format_autopkg_recipes(output):
    """Add lines between Input and Process, and between multiple processes.
    This aids readability of yaml recipes"""
    # add line before specific processors
    for item in ["Input:", "Process:", "- Processor:", "ParentRecipeTrustInfo:"]:
        output = output.replace(item, "\n" + item)

    # remove line before first process
    output = output.replace("Process:\n\n-", "Process:\n-")

    recipe = []
    lines = output.splitlines()
    for line in lines:
        # convert quoted strings with newlines in them to scalars
        if "\\n" in line:
            spaces = len(line) - len(line.lstrip()) + 2
            print(spaces)
            space = " "
            line = line.replace(': "', ": |\n{}".format(space * spaces))
            line = line.replace("\\t", "    ")
            line = line.replace('\\n"', "")
            line = line.replace("\\n", "\n{}".format(space * spaces))
            line = line.replace('\\"', '"')
            if line[-1] == '"':
                line[:-1]
        # elif "%" in lines:
        #  handle strings that have AutoPkg %percent% variables in them
        # (these need to be quoted)

        # print(line)
        recipe.append(line)
    recipe.append("")
    # print("\n".join(recipe))
    return "\n".join(recipe)
