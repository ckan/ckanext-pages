from setuptools import setup

setup(
    message_extractors={
        "ckanext": [
            ("**.py", "python", None),
            ("**.js", "javascript", None),
            ("**/pages/theme/**.html", "ckan", None),
        ]
    }
)
