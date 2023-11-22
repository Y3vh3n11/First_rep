from setuptools import setup, find_namespace_packages

setup(name = 'clean_folder',                     # ім'я
        version = '0.6',               # версія
        description = 'sorting files in a folder',       # короткий опис
        url = 'https://github.com/Y3vh3n11/First_rep/blob/main/sort_files.py',                      # посилання на код
        author = 'Y3vh3n11',                 # ім'я автора
        author_email = 'my_email@gmail.com',     # email автора
        license = 'MIT',               # ліцензія
        packages = find_namespace_packages(),             # модулі які використовуються в коді
        install_requires = '',                  # залежності
        entry_points={'console_scripts': ['clean-folder = clean_folder.clean:main']}                     # список точок входу для запуску коду із командного рядка
        )