import os
import asyncio
import shutil
import re
from collections import Counter
import frontmatter
from pathlib import Path
from pprint import pprint


# 1. Define the processing logic for a single file
async def process_file(index, file, semaphore, attributes):

    originalIndex = index + 1

    with open(f"./build2/{file}", "r", encoding="utf-8") as f:
        htmlData = "\n".join(f.readlines()[0:20])
        match = re.search(r"<title>Chapter\s+(\d+)", htmlData)
        if match:
            index = int(match.group(1))
        else:
            index += 2000

    # if Path(f"./chapters/lotm/webnovel/{index:04d}.md").exists():
    #     print(f"file {index:04d}.md already exits [{index}] [{originalIndex}] [{file}] [{match.group(1)}]")

    async with semaphore:
        output_path = f"./chapters/lotm/webnovel/{index:04d}.md"
        source_path = f"./build2/{file}"

        # Async Pandoc Call
        proc = await asyncio.create_subprocess_exec(
            "pandoc",
            "-f",
            "html-native_divs-auto_identifiers",
            "-t",
            "markdown",
            "-o",
            output_path,
            source_path,
        )
        await proc.wait()

        def read_and_clean():
            with open(output_path, "r", encoding="utf-8") as f:
                content = f.read()

            # 1. run_1 & run_8 -> Bold-Italic (Emphasis/Thoughts)
            content = re.sub(r"\[([^\]]+)\]\{\.run_[18][^}]*\}", r"***\1***", content)

            # 2. run_2, run_3, run_5 -> Italic (Standard thought style)
            content = re.sub(r"\[([^\]]+)\]\{\.run_[235][^}]*\}", r"*\1*", content)

            # 3. run_4 -> Bold (Usually Chapter Title text)
            content = re.sub(r"\[([^\]]+)\]\{\.run_4[^}]*\}", r"**\1**", content)

            # 4. Handle multiple tags like [Text]{.run_4} {.heading_2}
            # This cleans up the "extra" braces without touching the text we just formatted
            content = re.sub(r"(\s*\{[^}]+\})", "", content)

            # 5. Final pass: Strip any square brackets that didn't have a class attached
            content = re.sub(r"\[([^\]]+)\]", r"\1", content)

            # Title Extraction
            # Strip bolding from the H2 header
            # Replaces "## Chapter 1: **Crimson**" with "## Chapter 1: Crimson"
            content = re.sub(r"^(## Chapter \d+: )\*\*([^*]+)\*\*", r"\1\2", content, flags=re.MULTILINE)
            title_match = re.search(r"^##\s+Chapter\s+\d+:\s*(.*)", content)
            title = title_match.group(1).strip() if title_match else "unknown"

            # Volume Logic
            if index <= 213:
                section, category = "vol1", "Volume 1"
            elif index <= 482:
                section, category = "vol2", "Volume 2"
            elif index <= 732:
                section, category = "vol3", "Volume 3"
            elif index <= 946:
                section, category = "vol4", "Volume 4"
            elif index <= 1150:
                section, category = "vol5", "Volume 5"
            elif index <= 1266:
                section, category = "vol6", "Volume 6"
            elif index <= 1353:
                section, category = "vol7", "Volume 7"
            elif index <= 1394:
                section, category = "vol8", "Volume 8"
            elif index <= 1430:
                section, category = "side", "Side Story"
            else:
                section, category = "unknown", "unknown"

            post = frontmatter.Post(
                content,
                **{
                    "index": index,
                    "slug": index,
                    "title": title,
                    "section": section,
                    "category": category,
                },
            )

            # Write back
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(frontmatter.dumps(post))

            return content

        content = await asyncio.to_thread(read_and_clean)

        # Analytics
        attributes.extend(re.findall(r"\{.*?\}", content))
        if originalIndex % 50 == 0:
            print(f"Index: {originalIndex}")


async def main():

    global originalIndex

    originalIndex = 0

    files = os.listdir("./build2")

    # shutil.rmtree("./chapters/lotm/webnovel")
    # os.mkdir("./chapters/lotm/webnovel")
    attributes = []

    # Semaphore limits concurrent Pandoc instances (set to 10-20)
    semaphore = asyncio.Semaphore(60)

    tasks = [process_file(i, f, semaphore, attributes) for i, f in enumerate(files)]
    await asyncio.gather(*tasks)

    print("Done!", originalIndex)
    pprint(Counter(attributes).most_common(50))


if __name__ == "__main__":
    asyncio.run(main())
