from jinja2 import Environment, FileSystemLoader


def main():
    j2_loader = FileSystemLoader('./')
    env = Environment(loader=j2_loader)
    j2_tmpl = env.get_template('ahri.j2')
    foxes = [{"name": "Ahri", "age": 18}, {"name": "Sokyoei", "age": 12}, {"name": "Nono", "age": 12}]
    result = j2_tmpl.render(foxes=foxes)

    print(result)


if __name__ == '__main__':
    main()
