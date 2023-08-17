import subprocess
import sys
import os


def get_created_at(root, filename):
    sub = subprocess.Popen(f'git log --diff-filter=A --follow --format=%aI {filename}', shell=True, stdout=subprocess.PIPE,
                           cwd=root)
    ret = sub.communicate()
    return str(ret[0], encoding='utf-8').rstrip('\n')


def get_category(filename):
    return os.path.basename(os.path.dirname(os.path.abspath(filename)))


def get_title(f):
    f.seek(0)
    for line in f:
        if line.startswith("# "):
            return line[2:].rstrip('\n')
    return "Unknown"


def generate_digest(root, filename):
    real_path = os.path.join(root, filename)
    tmp_path = os.path.join(root, 'tmp_file.md')
    created = get_created_at(root, filename)
    category = get_category(real_path)
    with open(real_path, 'r') as f:
        first_line = f.readline()
        if first_line.startswith('---'):
            return
        with open(tmp_path, 'w') as f2:
            title = get_title(f)
            f2.write(f'---\n')
            f2.write(f'title: "{title}"\n')
            f2.write(f'categories: ["{category}"]\n')
            f2.write(f'tags: [""]\n')
            f2.write(f'date: {created}\n')
            f2.write(f'---\n')
            f2.write('\n')
            f.seek(0)
            f2.write(f.read())
    os.rename(tmp_path, real_path)


if __name__ == '__main__':
    for root, dirs, files in os.walk(os.path.dirname(os.path.abspath("your path"))):
        for f in files:
            if not f.endswith('.md'):
                continue
            generate_digest(root, f)
