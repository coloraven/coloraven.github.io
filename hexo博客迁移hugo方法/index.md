# Hexo博客迁移Hugo方法

## 区别点
1. `Markdown`文件的`frontmatter`不同，需要转换；
2. 可能插入超链接、图片链接不同，需要转换；

## `frontmatter`转换
```python
import yaml
import os
import glob
import re


def rename_key(dictionary, old_key, new_key):
    if old_key in dictionary:
        dictionary[new_key] = dictionary[old_key]
        del dictionary[old_key]

def delete_key(dictionary, old_key):
    if old_key in dictionary:
        del dictionary[old_key]


def check_and_increase_header_level(markdown_text):
    """
    Check if there are level-1 headers in the markdown text and increase the level of the headers if true.
    The function ignores headers inside code blocks.
    """
    # Replace code blocks with placeholders
    code_block_regex = r"```.*?```"
    code_blocks = re.findall(code_block_regex, markdown_text, re.DOTALL)
    replaced_text = markdown_text
    placeholders = []
    for i, code_block in enumerate(code_blocks):
        placeholder = f"<CODEBLOCK{i}>"
        placeholders.append(placeholder)
        replaced_text = replaced_text.replace(code_block, placeholder)

    # Check if there are level-1 headers
    level_1_headers = re.findall(r"^# .*$", replaced_text, re.MULTILINE)
    if level_1_headers:
        # Increase the level of the headers
        headers_regex = r"^(#{1,6})(.*)$"
        replaced_text = re.sub(headers_regex, lambda match: "#" + match.group(1) + match.group(2), replaced_text, flags=re.MULTILINE)
    
    # Replace placeholders with the original code blocks
    for placeholder, code_block in zip(placeholders, code_blocks):
        replaced_text = replaced_text.replace(placeholder, code_block)
        
    return replaced_text


def read_markdown_with_frontmatter(md_file_path):
    with open(md_file_path, 'r', encoding='utf-8') as file:
        # Read the entire file content
        md_content = file.read()

        # Split Frontmatter and Markdown content
        frontmatter, md_text = md_content.split("---\n", 2)[1:]

        # Parse Frontmatter using yaml
        frontmatter_data = yaml.safe_load(frontmatter)

    return frontmatter_data, md_text



def write_markdown_with_frontmatter(md_file_path, frontmatter_data, md_text):
    # Create a new Frontmatter string with desired order of fields
    new_frontmatter = ""
    fields_order = ["title", "date", "lastmod", "tags", "categories", "description",
                    "hidden", "image", "license", "math", "comments", "draft"]
    
    for field in fields_order:
        value = frontmatter_data.get(field)
        if value is not None:
            new_frontmatter += f"{field}: {value}\n"
        else:
            new_frontmatter += f"{field}: \n"
    
    md_text = check_and_increase_header_level(md_text)
    updated_md_content = f"---\n{new_frontmatter}---\n{md_text}"

    with open(md_file_path, 'w', encoding='utf-8') as file:
        # Write the updated content back to the file
        file.write(updated_md_content)


def work(md_file_path):
    frontmatter_data, md_content = read_markdown_with_frontmatter(md_file_path)
    if "tags" in frontmatter_data and type(frontmatter_data["tags"]) is str:
        frontmatter_data["tags"] = [frontmatter_data["tags"]]
    if "categories" in frontmatter_data and type(frontmatter_data["categories"]) is str:
        frontmatter_data["categories"] = [frontmatter_data["categories"]]
    rename_key(frontmatter_data,'updated','lastmod')
    delete_key(frontmatter_data,'keywords')
    delete_key(frontmatter_data,"top_img")
    delete_key(frontmatter_data,"highlight_shrink")
    delete_key(frontmatter_data,"cover")
    delete_key(frontmatter_data,"sticky")
    frontmatter_data["image"] = None
    frontmatter_data["math"] = False
    frontmatter_data["license"] = False
    frontmatter_data["hidden"] = False
    frontmatter_data["comments"] = False
    frontmatter_data["draft"] = False
    # frontmatter_data["tags"] = None
    # frontmatter_data["description"] = None
    # frontmatter_data["categories"] = None
    write_markdown_with_frontmatter(md_file_path, frontmatter_data, md_content)
if __name__ == "__main__":
    files = glob.glob(os.path.join('posts', "*.md"))
    for file in files:
        try:
            work(file)
        except Exception as e:
            print(file,e)
```

## `hugo`主题收集
1. `Stack`：https://github.com/CaiJimmy/hugo-theme-stack
<p>
效果见：

[如何优雅的从 Hexo 转移 Blog 到 Hugo](https://sdl.moe/post/hexo-transfer-to-hugo/)


2. `HBS theme`：https://hbs.razonyang.com/


