import fileinput


def create_site(site_name: str) -> None:
    with open(site_name + ".html", "w") as site:
        site.write("<!DOCTYPE html>\n")
        site.write("<html>\n")
        site.write("<head>\n")
        site.write(f"<title>{site_name}</title>\n")
        site.write("</head>\n")
        site.write(f"<body><p>welcome to {site_name}</p></body>\n")
        site.write("</html>")


def add_to_index(site_name: str) -> None:
    with open("index.html", "r") as f:
        data = f.read()
    some_index_you_want_to_insert_at = data.index("<body>") + len("<body>")
    some_text_to_insert = f'<a href="{site_name}.html">{site_name}</a>\n'

    new_data = (
        data[:some_index_you_want_to_insert_at]
        + some_text_to_insert
        + data[some_index_you_want_to_insert_at:]
    )

    with open("index.html", "w") as f:
        f.write(new_data)


def main():
    new_site = input("Enter name of new site: ")
    create_site(new_site)
    add_to_index(new_site)


if __name__ == "__main__":
    main()
