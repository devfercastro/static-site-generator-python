from typing import List


def markdown_to_blocks(markdown: str) -> List[str]:
    blocks = []

    for block in markdown.split("\n\n"):
        stripped_block = block.strip()

        if stripped_block != "":
            # handle blocks with multiple indentated lines
            if "\n" in stripped_block:
                # remove indentation from each line
                outdented_lines = [line.strip() for line in stripped_block.split("\n")]
                blocks.append("\n".join(outdented_lines))

            else:
                # simple blocks just appends it
                blocks.append(stripped_block)

    return blocks
