from setuptools import setup

setup(name="clean_folder",
      version="1",
      packages=["clean_folder"],
      author="Victor Yarcev",
      description="sorting and clearing folder in chosen directory",
      entry_point={
          "console_scripts": ["clean_folder = clean_folder.clean:main"]
      }
)