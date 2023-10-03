# get text with .md file
def read_markdown_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            markdown_content = file.read()
        return markdown_content
    except Exception as e:
        print(f"Error reading Markdown file: {e}")
        return None

def extract_text_from_markdown(markdown_content):
    if markdown_content is None:
        return None

    text = ""
    lines = markdown_content.split('\n')
    for line in lines:

        text += line + '\n'

    return text


# get text with .csv file



# get text with .txt file




markdown_file_path = r'C:\Users\Admin\Desktop\Project\Inter_AI_2023\prj-economical-chatbot\file_upload\README.md'

markdown_content = read_markdown_file(markdown_file_path)

text_from_markdown = extract_text_from_markdown(markdown_content)

if text_from_markdown is not None:
    print(text_from_markdown)


